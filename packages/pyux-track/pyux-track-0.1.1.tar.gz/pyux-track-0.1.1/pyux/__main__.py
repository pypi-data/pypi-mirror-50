
from shutil import rmtree
from shutil import get_terminal_size
from time import sleep

from pyux.console import ColourPen
from pyux.console import ProgressBar
from pyux.console import Wheel
from pyux.logging import init_logger
from pyux.time import Chronos
from pyux.time import Timer


def _title_char(x):
    x = "\n===   %s   " % x
    x = x + '=' * (__width__ - len(x)) + '\n'
    return x


__pen__ = ColourPen()
__width__ = get_terminal_size()[0]

__welcome_message__ = """%s
    Welcome to pyux tools demo
%s""" % ("=" * __width__, "=" * __width__)
__intro__ = """
    All available tools in this package will now be demonstrated !
    Read the README to see the nitty gritty of using them."""

__title1__ = _title_char('1. Module console')
__intro1__ = """
    Classes available in console package help you with printing stuff
    when a script is running."""
__div_wheel__ = """
    Wheel : print a turning wheel within a for loop (or manually).
    The iteration counter or the iterated value is printed next to the wheel.
"""
__div_progress__ = """
    ProgressBar : inspired by tqdm package, print a progress bar
    within a for loop (or manually).
"""
__div_colour__ = """
    ColourPen : colourise and style text for terminal printing, with package
    colorama. This is what this demo uses to colour text !
"""

__title2__ = _title_char('2. Module time')
__intro2__ = """
    Classes available in time package are relative to time in a script : either
    making it wait, or timing durations."""
__div_timer__ = """
    Timer : print a timer for a given delay.
    A counter and a message can be printed too.
"""
__div_chronos__ = """
    Chronos : a stopwatch for your script or your loops.
    Can save results in a tsv file.
"""

__title3__ = _title_char('3. Module logging')
__intro3__ = """
    The logging module contains only function init_logger, that you can use to
    initiate a logger instance. You can specify name and destination folder for
    the log file. By defaut, the name changes at each execution so it creates
    a different log file by execution. You can give your own logging.conf or
    use the default format included."""
__div_logger__ = """
    init_logger : initiate a root logger that creates a different log file for
    each execution.
"""

__title_style__ = {'color': 'yellow', 'style': 'bright'}
__div_style__ = {'color': 'green', 'style': 'normal'}

__goodbye__ = """
    This demo has ended ! Thanks for using pyux and feel free to suggest
    improvements at https://gitlab.com/roamdam/pyux."""


def _user_yes(skip_char = 'p', action = 'pass'):
    global __pen__
    __pen__.write(color = 'white', style = 'dim')
    text = input('    Type any key to continue or %s to %s : ' % (skip_char, action))
    __pen__.write(style = 'reset_all')
    return False if text == skip_char else True


def _user_exit():
    global __pen__
    __pen__.write('\n    Do you want to continue the demo ?', color = 'red', newline = True, reset = True)
    if not _user_yes(skip_char = 'q', action = 'quit'):
        print('\n    Goodbye !')
        exit(0)
    else:
        return


def main():
    global __pen__
    __pen__\
        .write(message = __welcome_message__, style = 'bright', color = 'cyan', newline = True, reset = True)\
        .write(message = __intro__, newline = True)\
        
    __pen__\
        .write(message = __title1__, color = __title_style__['color'], style = __title_style__['style'], reset = True)\
        .write(message = __intro1__, newline = True)\
        .write(message = __div_wheel__, color = __div_style__['color'], style = __div_style__['style'], reset = True)
    if _user_yes():
        print("""
    You can print the number of iterations, here for 30 iterations""")
        for _ in Wheel(30):
            sleep(0.1)
        print("""
    Or the iterated value, here for an iteration over 30 paths""")
        sleep(2)
        paths = ['fakepath_%d' % index for index in range(30)]
        for _ in Wheel(paths, print_value = True):
            sleep(0.1)
    
    __pen__.write(message = __div_progress__, color = __div_style__['color'],
                  style = __div_style__['style'], reset = True)
    if _user_yes():
        print("""
    You can print a progress bar that will adjust to the window size,
    here for 2 500 iterations""")
        for _ in ProgressBar(2500):
            sleep(0.001)
    
    __pen__.write(message = __div_colour__, color = __div_style__['color'],
                  style = __div_style__['style'], reset = True)
    if _user_yes():
        print('\n    You can set colour and styles among predefined values :')
        __pen__\
            .write(message = '    This is a normal red', color = 'red', newline = True)\
            .write(message = '    This is a bright blue', color = 'cyan', style = 'bright', newline = True)\
            .write(reset = True)
        
        __pen__\
            .write('    You can also', color = 'green')\
            .write(' change colors within', color = 'magenta')\
            .write(' the same line !', color = 'yellow', reset = True, newline = True)
    _user_exit()

    # Section 2
    __pen__ \
        .write(message = __title2__, color = __title_style__['color'], style = __title_style__['style'], reset = True) \
        .write(message = __intro2__, newline = True) \
        .write(message = __div_timer__, color = __div_style__['color'], style = __div_style__['style'], reset = True)
    if _user_yes():
        print("\n    Use Timer to make a program wait and see where it is at.")
        Timer(delay = 5, message = "This is an example of a 5 seconds timer")
        print("""
    You can use also it for each iteration in a loop by decorating
    the iterable in a for statement.
    Here for a three iterations loop, pausing 3 seconds each time,
    and rewriting on the same line in terminal for each iteration
    (useful for big loops).""")
        sleep(8)
        for _ in Timer(3, delay = 3, pattern = 'iteration : ', overwrite = True):
            pass

    __pen__.write(message = __div_chronos__, color = __div_style__['color'],
                  style = __div_style__['style'], reset = True)
    if _user_yes():
        print("""
    Use Chronos to time stages of your script.
    You can also use it to time iterations within loops by decorating
    the iterable in the for statement.
    Here for a three iterations loop, with a pause equal to the iteration
    value.""")
        sleep(10)
        for _ in Chronos(range(1, 4), console_print = True):
            Timer(delay = _, message = "Iteration %d, waiting %d secs" % (_, _), overwrite = True)
    
    _user_exit()

    # Section 3
    __pen__ \
        .write(message = __title3__, color = __title_style__['color'], style = __title_style__['style'], reset = True) \
        .write(message = __intro3__, newline = True) \
        .write(message = __div_logger__, color = __div_style__['color'],
               style = __div_style__['style'], reset = True)
    if _user_yes():
        print("""
    A log file will be created in './tmp' with name demo_run_time-of-run.log.
    By default, the logger writes to file and to console (which can be coloured).""")
        logger = init_logger(folder = './tmp', filename = 'demo', run_name = 'run')
        sleep(5)
        logger.info('An info message without color.')
        sleep(1)
        __pen__.write(style = 'bright', color = 'red', newline = False)
        logger.critical('A critical message colored in bright red (in console only).')
        __pen__.write(
            message = "\n    A log file was created in './tmp'. Do you want to delete that folder ?",
            style = 'reset_all', newline = True
        )
        if _user_yes(skip_char = 'k', action = 'keep'):
            rmtree('./tmp')
            print("    ./tmp folder deleted !")
        
    __pen__.write(__goodbye__, color = 'yellow').close()
    

if __name__ == '__main__':
    main()
