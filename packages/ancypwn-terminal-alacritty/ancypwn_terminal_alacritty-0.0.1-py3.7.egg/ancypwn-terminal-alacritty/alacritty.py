import os
import platform


def run(command):
    system = platform.system().lower()
    if 'windows' in system:
        execute = \
            'alacritty -e powershell -noexit -Command "{}"'.format(command)
    else:
        execute = 'alacritty -e "{}"'.format(command)
    os.system(execute)


def run_test():
    run('ls')
