import os
import platform


def _escape_command_unix(command):
    return repr(command)[1:-1]


def run(command):
    system = platform.system().lower()
    if 'windows' in system:
        execute = \
            'alacritty -e powershell -NoExit -Command "{}"'.format(command)
    else:
        execute = 'alacritty -e "{}"'.format(_escape_command_unix(command))
    print(execute)
    res = os.system(execute)


def run_test():
    run('ancypwn attach -c \'/usr/bin/gdb /bin/echo\'')

if __name__ == '__main__':
    run_test()
