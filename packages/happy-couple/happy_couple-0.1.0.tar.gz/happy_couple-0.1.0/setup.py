import sys
import os
import setuptools

currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(currentPath)

with open("README.rst", "r") as fh:
    long_description = fh.read()

# for now don't know the better way :(
images = [os.path.join('lines_only', item) for item in os.listdir('happy_couple/lines_only') if item.endswith('.png')]
sounds = [os.path.join('sounds', item) for item in os.listdir('happy_couple/sounds') if item.endswith('.wav')]

setuptools.setup(
    name='happy_couple',
    version='0.1.0',
    author="streanger",
    author_email="divisionexe@gmail.com",
    description="cover of scene from revenge of the nerds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/streanger/happy_couple",
    packages=['happy_couple',],
    # packages=['happy_couple', 'happy_couple.sounds', 'happy_couple.lines_only'],
    license='MIT',
    install_requires=['opencv-python', 'numpy', 'setuptools'],      # setuptools  is needed, when using pkg_resources
    include_package_data=True,
    package_data={  # Optional
        # 'happy_couple': ['sounds/smb_jump.wav', 'lines_only/small_head.png'],
        'happy_couple': images + sounds,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
