'''
version: 0.1.0
date: 22:51 29.07.2019
updates: 00:40 01.08.2019
"this is script, for make animation from "revenge of the nerds" movie; beta version done at 28.07.2019, 03:09"
'''
import sys
import os
import time
import random
import numpy as np
import cv2
import winsound
import pkg_resources    # this is for read static package files


def script_path():
    ''' return and change directory, to current script path '''
    currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(currentPath)
    return currentPath
    
    
def static_file_path(dir, file):
    ''' get path of the specified file under dir
    https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
    https://stackoverflow.com/questions/39104/finding-a-file-in-a-python-module-distribution
    '''
    if False:
        # get content of specified file
        resource_package = __name__
        resource_path = '/'.join((dir, file))  # Do not use os.path.join()
        template = pkg_resources.resource_string(resource_package, resource_path)
        # or for a file-like stream:
        # template = pkg_resources.resource_stream(resource_package, resource_path)
    else:
        # get path of specified file
        # template = pkg_resources.resource_filename(__name__, file)
        resource_path = '/'.join((dir, file))  # Do not use os.path.join()
        template = pkg_resources.resource_filename(__name__, resource_path)
        # template = pkg_resources.resource_filename(dir, file)
        # from doc --> resource_filename(package_or_requirement, resource_name)
    return template
    
    
def random_codes():
    # codes = [random.randrange(21, 65) for x in range(5)]
    codes = [random.randrange(21, 112) for x in range(5)]
    return codes
    
    
def time_template():
    template = time.strftime("%Y%m%d_%H%M%S")
    return template
    
    
def show_image(title, image):
    '''
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    '''
    cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
    # cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def create_blank_image(height, width):
    image = np.zeros((height, width, 3), np.uint8)
    image += 55
    return image
    
    
def draw_tv_background_and_backlight(img):
    ''' think of some funny background '''
    # file = 'old_tv.png'
    # tv = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    # out = paste_image(tv, img, 0, 0)
    # return out
    return img
    
    
def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            if f.endswith('.png'):
                # yield os.path.abspath(os.path.join(dirpath, f))
                yield os.path.abspath(static_file_path(dirpath, f))
                
                
def get_views(key):
    ''' store here all views
        think of cut single view, to parts
        store data with alpha layer
        
        info - not used for now
    '''
    data = {
        'view_00': 1,
        'view_01': 1,
        'view_02': 1,
        'view_03': 1
        }
    return data[key]
    
    
def help_content():
    ''' commands possible for use. Need to be improved '''
    some = '''
    start                   --create window to draw image
    exit, quit              --finish drawing
    help                    --this help content
    save                    --save image as "drawing.png"
    draw                    --draw some random line
    clear                   --clear image
    refresh                 --refresh live mode
    resize                  --resize objects
    sound on/off            --turn on/off sound effects
    list_files              --list files from lines_only directory
    load <file> <x_pos>
         <y_pos> <size>     --load image
    set_color <color>       --just a name of color? like red, green...
    '''
    return some
    
    
def smooth_image(img, numberOfBlurs=5):
    '''
    based on:
        https://stackoverflow.com/questions/37409811/smoothing-edges-of-a-binary-image
    used for creating images
    '''
    ret, thresh = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY);
    blurredImage = cv2.pyrUp(thresh);
    for x in range(numberOfBlurs):
        # blurredImage = cv2.medianBlur(blurredImage, 7);
        blurredImage = cv2.medianBlur(blurredImage, 5);
    blurredImage = cv2.pyrDown(blurredImage);
    ret, thresh = cv2.threshold(blurredImage, 155, 255, cv2.THRESH_BINARY);
    return thresh
    # return blurredImage
    
    
def cat_images(img1, img2, axisVal):
    if not axisVal in (0, 1):
        return img1             # if wrong axisVal parameter, return first image
    return np.concatenate((img1, img2), axis=axisVal)
    
    
def create_new_dir(dir):
    currentPath = script_path()
    # dir = 'extracted_views'
    if not os.path.exists(dir):
        os.makedirs(dir)
    newPath = os.path.join(currentPath, dir)
    return newPath
    
    
def path_last_element(path):
    return os.path.basename(os.path.normpath(path))
    
    
def generate_images():
    ''' function was used in early stage '''
    currentPath = script_path()
    dir = 'extracted_views'
    if not os.path.exists(dir):
        os.makedirs(dir)
    newPath = os.path.join(currentPath, dir)
    
    
    files = [item for item in os.listdir() if item.startswith('view') and item.endswith('.png')]
    for key, file in enumerate(files):
        img = cv2.imread(file, 0)
        height, width = img.shape[:2]
        blank = create_blank_image(height, width)
        
        
        # ************** threshold **************
        '''
        # th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)
        th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)        # image save in this configuration
        # th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 19, 6)
        # cv2.imwrite(os.path.join(newPath, "th_{}".format(file)), th)
        show_image('th', th)
        '''
        
        
        # ************** contours **************
        '''
        # ret,thresh = cv2.threshold(img,127,255,0)
        thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 19, 6)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # To draw all the contours in an image:
        cv2.drawContours(blank, contours, -1, (0,255,0), 1)
        
        #To draw an individual contour, say 4th contour:
        # cv2.drawContours(blank, contours, 3, (0,255,0), 1)
        
        #But most of the time, below method will be useful:
        # cnt = contours[4]
        # cv2.drawContours(blank, [cnt], 0, (0,255,0), 1)
    
        show_image('blank', blank)
        '''
        
        
    # ************** make one-time smooth operation **************
    '''
    smoothedDir = create_new_dir('smoothed')
    paths = absoluteFilePaths('edited_manually')
    for file in paths:
        img = cv2.imread(file, 0)
        smoothed = smooth_image(img, 2)
        fileOut = os.path.join(smoothedDir, path_last_element(file))
        cv2.imwrite(fileOut, smoothed)
        print(fileOut)
        # out = cat_images(img, smoothed, 1)
        # show_image('out', out)
    '''
        
        
    # ************** extract colored lines **************
    # use it at the last stage
    '''
    lines_only = create_new_dir('lines_only')
    paths = absoluteFilePaths('colored')
    colors = (132, 170, 237)     # is it orange?
    colors = (62, 158, 255)     # is it orange?
    for file in paths:
        img = cv2.imread(file, 1)
        # https://pythonprogramming.net/color-filter-python-opencv-tutorial/
        lower_green = np.array([00, 150, 00])
        upper_green = np.array([255, 200, 255])
        mask = cv2.inRange(img, lower_green, upper_green)   # this extracts green elements
        B, G, R = [cv2.bitwise_and(mask+color, mask+color, mask=mask) for color in colors]
        
        alpha = mask*1
        BGR = cv2.merge((B, G, R, alpha)) # join layers
        # show_image('BGR', BGR)
        fileOut = os.path.join(lines_only, path_last_element(file))
        cv2.imwrite(fileOut, BGR)
    '''
    
    
    # ************** useful construct(s) **************
    # img[np.where(img > 50)] = [255]
    # masked_img = cv2.bitwise_and(img, img, mask=thresholded_img)
    # https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv
    
    
    
    # ************** paste image **************
    '''
    smaller = cv2.imread('pigeon.png', cv2.IMREAD_UNCHANGED)
    heightMain, widthMain = 1200, 900
    bigger = create_image(heightMain, widthMain)
    if False:
        out = paste_image(smaller, bigger, 580, 600)
        show_image('out', out)
    else:
        for x in range(90):
            out = paste_image(smaller, bigger, 10*x+200, 10*x)
            # show_image('out', out)
            cv2.imshow('out', out)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.01)     # is it really needed?
            # input()
        cv2.destroyAllWindows()
    '''
    
    
    # ************** check position - used when creating sequence **************
    # file1, pos1, file2, pos2 = 'th_view_01.png', (400, 400), 'th_view_02.png', (400, 376)
    # file1, pos1, file2, pos2 = 'th_view_02.png', (400, 376), 'th_view_03.png', (331, 139)
    # file1, pos1, file2, pos2 = 'small_head.png', (736, 40), 'th_view_04.png', (700, 9)
    # file1, pos1, file2, pos2 = 'th_view_04.png', (700, 9), 'th_view_05.png', (326, 14)
    # file1, pos1, file2, pos2 = 'th_view_07.png', (326, 14), 'walking_man_01.png', (341, 6)
    # file1, pos1, file2, pos2 = 'th_view_04.png', (700, 9), 'waiting_woman.png', (689, 14)
    # file1, pos1, file2, pos2 = 'waiting_woman.png', (689, 14), 'th_view_08.png', (477, 14)
    # file1, pos1, file2, pos2 = 'th_view_08.png', (477, 14), 'walking_man_02.png', (479, 1)
    # file1, pos1, file2, pos2 = 'th_view_08.png', (477, 14), 'th_view_10.png', (499, 10)
    # check_position(file1, pos1, file2, pos2)
    return True
    
    
def create_image(height, width):
    img = np.array(range(height*width), dtype=np.uint8).reshape((width, height))        # create one layer array
    out = np.stack((img,)*3, axis=-1)                                                   # convert 1 layer to 3 layer (gray -> rgb)
    return out
    
    
def draw_parts():
    ''' extract parts from image, which are not connected, and draw them one by one 
        not used for now. It may change animation a lot
    '''
    return True
    
    
def draw_up_down():
    ''' draw image from up to down, line by line
        not used for now. It may change animation a lot
    '''
    return True
    
    
def simple_resize_img(img, newSize):
    ''' newSize is int type; 0-99 -> resize down; 100 -> the same size; 101+ -> resize up '''
    height = round((img.shape[0])*(newSize/100))
    width = round((img.shape[1])*(newSize/100))
    resized = cv2.resize(img, (width, height))
    return resized
    
    
def paste_image(smaller, bigger, x_pos, y_pos):
    ''' paste some image with alpha channel, to another one '''
    
    # ************** handle position and size errors **************
    max_size_y , max_size_x = bigger.shape[:2]
    small_size_y, small_size_x = smaller.shape[:2]
    cut_x, cut_y = 0, 0
    if x_pos + small_size_x > max_size_x:
        cut_x = max_size_x - x_pos
        if cut_x < 1:
            return bigger
        smaller = smaller[:, 0:cut_x]
    if y_pos + small_size_y > max_size_y:
        cut_y = max_size_y - y_pos
        if cut_y < 1:
            return bigger
        smaller = smaller[0:cut_y, :]
    # print("cut_x: {:0=3d}, cut_y: {:0=3d}".format(cut_x, cut_y), end='\r', flush=True)
    
    
    # ************** paste smaller image into bigger, with including alpha channel **************
    B, G, R, alpha = cv2.split(smaller)
    smallerRGB = cv2.merge((B, G, R))
    mask_inv = cv2.bitwise_not(alpha)
    height, width = smallerRGB.shape[:2]
    
    roi = bigger[y_pos:y_pos+height, x_pos:x_pos+width]
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    img2_fg = cv2.bitwise_and(smallerRGB, smallerRGB, mask=alpha)
    
    dst = cv2.add(img1_bg, img2_fg)
    out = bigger.copy()         # we shouldn't change original image
    out[y_pos:y_pos+height, x_pos:x_pos+width] = dst
    return out
    
    
def check_position(file1, pos1, file2, pos2):
    ''' this function(like almost every other) need to be cleaned '''
    # ************** check position **************
    heightMain, widthMain = 900, 1200
    blank = create_blank_image(heightMain, widthMain)
    # blank = create_image(heightMain, widthMain)               # with some predefined background
    # img = draw_tv_background_and_backlight(blank)       # draw some background(for now return the same image)
    img = blank.copy()
    
    # read first image
    file = 'th_view_02.png'
    stable = cv2.imread(static_file_path('lines_only', file), cv2.IMREAD_UNCHANGED)
    # img = paste_image(stable, img, 400, 388)
    img = paste_image(stable, img, pos1[0], pos1[1])
    
    # read second image
    # second = 'th_view_03.png'
    loaded = cv2.imread(static_file_path('lines_only', file2), cv2.IMREAD_UNCHANGED)
    # pos_x, pos_y = 200, 200
    pos_x, pos_y = pos2
    size_y, size_x = loaded.shape[:2]
    
    firstTick = True
    while True:
        if firstTick:
            out = img*1
            firstTick = False
        else:
            try:
                if pos_x < 0:
                    pos_x = 0
                if pos_x > widthMain:
                    pos_x = widthMain
                    
                if pos_y < 0:
                    pos_y = 0
                if pos_y > heightMain:
                    pos_y = heightMain
                
                print("pos_x: {:4d}, pos_y: {:4d}".format(pos_x, pos_y), end='\r', flush=True)
                out = paste_image(loaded, img, pos_x, pos_y)
            except:
                continue
                
                
        cv2.imshow('out', out)
        
        # this could be handled some dictio way?
        key = cv2.waitKey(33)
        if key == -1:
            pass
            
        elif key == 119:
            # W - 119
            pos_y -= 1
            
        elif key == 115:
            # S - 115
            pos_y += 1
            
        elif key == 97:
            # A - 97
            pos_x -= 1
            
        elif key == 100:
            # D - 100
            pos_x += 1
            
        elif key == 116:
            # T - 116
            pos_y -= 10
            
        elif key == 103:
            # G - 103
            pos_y += 10
            
        elif key == 102:
            # F - 102
            pos_x -= 10
            
        elif key == 104:
            # H - 104
            pos_x += 10
            
        elif key == ord('q'):
            break
            
        else:
            # print(key)
            pass
            
    cv2.destroyAllWindows()
    print()
    return True
    
    
def handle_command(command):
    ''' to be done '''
    return command
    
    
def animation(commandMode=False):
    ''' use commandMode=True, to create animation on your own, with using commands '''
    currentPath = script_path()
    posZeroX, posZeroY = -100, 50       # where the coordinates starts from
    
    
    heightMain, widthMain = 900, 1200
    blank = create_blank_image(heightMain, widthMain)
    # blank = create_image(heightMain, widthMain)               # with some predefined background
    img = draw_tv_background_and_backlight(blank)       # draw some background(for now return the same image)
    # show_image('img', img)
    toStart = False
    # print("> type commands, to start drawing")
    print("> this is very strange animation")
    commandNo = 0
    while True:
        command = input("> ")
        
        if not commandMode:
            # sequence (for lazy people; make it optional)
            sequence = [
                'start',
                # 'help',                               # just to simulate that you are typing commands
                'load th_view_01.png 400 400',
                'load th_view_02.png 400 376',
                'load th_view_03.png 331 139',
                'resize',                               # resize and move head 
                'loadre th_view_04.png 700 9',          # clear & load full woman in low-res
                'load th_view_05.png 326 14',           # full man on left
                'loadre th_view_06.png 326 14',         # man move hand
                'loadre th_view_07.png 326 14',         # woman move hand
                'move',                                 # man move ahead for shaking hands
                'animation',                            # final animation :)
                'refresh',
            ]
            
            try:
                # 1/0   # this change sequence mode to command one
                command = sequence[commandNo]
            except IndexError:
                pass
            except:
                pass
            commandNo += 1

            
        if commandNo > 1:
            winsound.PlaySound(static_file_path('sounds', 'smb_jump.wav'), winsound.SND_ALIAS | winsound.SND_ASYNC)
            
        if commandMode:
            if command == 'start':
                commandNo += 2
                
                
        if command == 'help':
            content = help_content()
            print(content)
            
        elif command == 'draw':
            cv2.line(img, (random.randrange(heightMain), random.randrange(widthMain)),
                          (random.randrange(heightMain), random.randrange(widthMain)),
                          (155, 255, 155), 2)
                          
        elif command == 'start':
            toStart = True
            
        elif command in ('exit', 'quit'):
            break
            
        elif command == 'save':
            cv2.imwrite('drawing_{}.png'.format(time_template()), img)
            
        elif command == 'resize':
            ''' this is only for resize head in live mode '''
            # part = img[100:600, 100:600]
            loaded = cv2.imread(static_file_path('lines_only', 'th_view_03.png'), cv2.IMREAD_UNCHANGED)
            blank = create_blank_image(heightMain, widthMain)
            img = draw_tv_background_and_backlight(blank)
            for x in range(10):
                # if not x%5:
                sound = 'smb_touch.wav'
                if x==3:
                    winsound.PlaySound(static_file_path('sounds', sound), winsound.SND_ALIAS | winsound.SND_ASYNC)
                resized = simple_resize_img(loaded, 100-6*x)
                # append 4 layer
                # B, G, R = cv2.split(resized)
                # resized = cv2.merge((B, G, R, G.copy()))
                out = paste_image(resized, img, posZeroX + 331 + 45*x, posZeroY + 139 - 11*x)
                cv2.imshow('img', out)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                time.sleep(0.05)
            # print(331 + 45*x, 139 - 11*x)
            # cv2.imwrite('small_head.png', resized)
            img = out
            
        elif command == 'move':
            # print("(move scene is now executed)")
            '''
            clear whole screen
            draw waiting woman on right
            draw man on the left
            start animation of moving man, with using "walking_man_02.png" and "walking_man_03.png"
            after all replace it with "th_view_08.png"
            '''
            # clear screen
            blank = create_blank_image(heightMain, widthMain)
            img = draw_tv_background_and_backlight(blank)
            woman = cv2.imread(static_file_path('lines_only', 'waiting_woman.png'), cv2.IMREAD_UNCHANGED)
            
            # draw waiting woman on right
            img = paste_image(woman, img, posZeroX + 689, posZeroY + 14)
            # for x in range(11):
            for x in range(21):
                if not x:
                    # draw man on the left
                    man = cv2.imread(static_file_path('lines_only', 'walking_man_01.png'), cv2.IMREAD_UNCHANGED)
                    out = paste_image(man, img, posZeroX + 341, posZeroY + 6)
                else:
                    if x%2:
                        man = cv2.imread(static_file_path('lines_only', 'walking_man_02.png'), cv2.IMREAD_UNCHANGED)
                    else:
                        man = cv2.imread(static_file_path('lines_only', 'walking_man_03.png'), cv2.IMREAD_UNCHANGED)
                    # out = paste_image(man, img, posZeroX + 341+round(13.8*x), posZeroY + 6-1*(x//2))
                    out = paste_image(man, img, posZeroX + 341+round(6.9*x), posZeroY + 6-1*(x//4))
                    
                    # dst -> (479, 1)
                if not x%11:
                    sound = 'smb_jump.wav'
                    winsound.PlaySound(static_file_path('sounds', sound), winsound.SND_ALIAS | winsound.SND_ASYNC)
                cv2.imshow('img', out)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # time.sleep(0.05)
                time.sleep(0.03)
                
            
            # clear screen again
            blank = create_blank_image(heightMain, widthMain)
            img = draw_tv_background_and_backlight(blank)
            hands = cv2.imread(static_file_path('lines_only', 'th_view_08.png'), cv2.IMREAD_UNCHANGED)
            out = paste_image(hands, img, posZeroX + 477, posZeroY + 14)      # (477, 14) - position of pair with shaking hands
            
            sound = 'smb_coin.wav'
            winsound.PlaySound(static_file_path('sounds', sound), winsound.SND_ALIAS | winsound.SND_ASYNC)
            # print(331 + 45*x, 139 - 11*x)
            # cv2.imwrite('small_head.png', resized)
            img = out
            
        elif command == 'animation':
            # print("(final animation scene is now executed)")
            '''
            clear screen
            show in a loop four images
            '''
            
            # clear screen
            blank = create_blank_image(heightMain, widthMain)
            img = draw_tv_background_and_backlight(blank)
            stepSize = 25
            steps = [x for x in range(0, 200, stepSize)] + [x for x in range(-200, 201, stepSize)][::-1] + [x for x in range(-200, 0, stepSize)][1:]
            while True:
                for step in steps:
                    # print("current step: {}".format(step))
                    for x in range(4):
                        couple = cv2.imread(static_file_path('lines_only', 'th_view_1{}.png'.format(str(x))), cv2.IMREAD_UNCHANGED)     # this format is risky in some way
                        # out = paste_image(couple, img, posZeroX + 499, posZeroY + 10)   #(it should be -> 499, 10)
                        out = paste_image(couple, img, posZeroX + step + 449, posZeroY + 10)   #(it should be -> 499, 10)
                        
                        cv2.imshow('img', out)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                        # time.sleep(0.05)
                        time.sleep(0.25)
                        # cv2.imwrite('happy_couple_{}.png'.format(x), out)
                    sound = 'smb_touch.wav'
                    winsound.PlaySound(static_file_path('sounds', sound), winsound.SND_ALIAS | winsound.SND_ASYNC)
            # this loop never ends
            
        elif command == 'clear':
            blank = create_blank_image(heightMain, widthMain)
            img = draw_tv_background_and_backlight(blank)
            
        elif command == 'light':
            print("(put some light on the top of the image")
            
        elif command == 'refresh':
            img = img*1
            
        elif command == 'list_files':
            # paths = '\n\t'.join(absoluteFilePaths('lines_only'))
            paths = '\t' + '\n\t'.join(os.listdir('lines_only'))
            print(paths)
            
        elif command == 'resize':
            ''' we need to resize center of the image(head) and move it to the top-right corner '''
            pass
            
        
        elif command.startswith('load'):
            try:
            # if 1:
                _, file, x_pos, y_pos = command.split()[:4]
                x_pos = int(x_pos)
                y_pos = int(y_pos)
                loaded = cv2.imread(static_file_path('lines_only', file), cv2.IMREAD_UNCHANGED)
                if len(command.split()) == 5:
                    resizeX = int(command.split()[-1])
                    print(resizeX)
                    loaded = simple_resize_img(loaded, resizeX)
                if command.split()[0].endswith('re'):
                    blank = create_blank_image(heightMain, widthMain)
                    img = draw_tv_background_and_backlight(blank)
                img = paste_image(loaded, img, posZeroX + x_pos, posZeroY + y_pos)
            except:
            # else:
                print("failed to load image with command: {}".format(command))
            
        if toStart:
            # script need to update image when commands are typed
            
            # images need to be join, just before drawing
            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        time.sleep(0.1)     # is it really needed?
    cv2.destroyAllWindows()
    print("\n> drawing finished")
    return True
    
    
if __name__ == "__main__":
    args = sys.argv[1:]
    # some = static_file_path('sounds', 'smb_coin.wav')
    # some = static_file_path('lines_only', 'th_view_01.png')
    # args = ['--command']
    if '--help' in args or '-h' in args:
        print("use '--command' parameter, to run animation in command mode")
    if '--command' in args:
        mode = True
    else:
        mode = False
    animation(commandMode=mode)
    
    
'''
info:
    -humans originally are orange
    -make real tv background
    -store extracted data(from original views) in extracted_views directory
    -make function for tilting image
    -think of some sounds while drawing
    -every added image should exist as subimage, which let us to move it
    -for lazy people make sequence, which executes every time enter is typing into input
    -
    
todo:
    -add color specifying
    -add "sound on/off"
    -clean functions
    -make tv background
    -think of make a pypi package from it
    -
    
bugs:
    -when images are resizing, then white border appears
    -i need to resize(enlarge) files from "smoothed", and then convert to colored, and finally to lines_only
    -
    
'''
