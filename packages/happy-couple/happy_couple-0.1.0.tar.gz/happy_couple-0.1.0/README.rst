Juster
===========
Script for create cover of animation from revenge of the nerds movie

Info
===========
For now script works with open-cv. I think of add some features in the future, and tkinter gui as option.

Install
===========

.. code-block:: python

    pip install happy_couple

Usage
===========

.. code-block:: python

    from happy_couple import animation

    animation(Fale)
    # then just press enter, or type some commands. Hardcoded sequence will be executed.
    
    animation(True)
    # use specified commands, to create expected animation
    
    
Fake sequence commands
===========
It can be use, to simulate real coding:

    - > this is very strange animation
    
    - > start
    
    - > glasses(20, some.glasses())
    
    - > eyes(2, 'big', 'center-left')
    
    - > hair('wavy', 'long')
    
    - > resize_down('right-corner')
    
    - > full_figure('legs', 'hands', 'feets')
    
    - > man_full_figure('head', 'body', 'legs', 'hands', 'feets', 'glasses')
    
    - > hand_up('man')
    
    - > hand_up('woman')
    
    - > walk(men, woman)
    
    - > dance('right-left', 'forward', 'sound'='on')
    
    
## screen from happy_couple animation

![image](happy_couple.png)
