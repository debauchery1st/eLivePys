#!/usr/bin/env python
from os import path
from time import sleep
from alterjdk import check_jdk, NEWJDK, OLDJDK, parser, set_vars, relink_jdk
from getjdk8 import get_jdk8
from subprocess import call


if __name__ == "__main__":
    a, e, o, n = set_vars(parser.parse_args())
    dl_script = None
    if e == 0:
        print('creating dl script')
        dl_script = get_jdk8()
        sleep(.123)
    if dl_script is not None:
        if raw_input('Download and build OpenJDK8? (Yes/n) : ') == 'Yes':
            call([dl_script])
        else:
            print('skipping compilation\n\n')
    print('WORKING DIRECTORY: {}\nOLD: {}\nNEW: {}\n'.format(a, o, n))
    results = check_jdk(alt_wd=a, old_jdk=o, new_jdk=n)
    totals = len(results)
    if totals == 0:
        print('\nnothing to do.\nrun with "-r 0"  or "--reverse 0" to replace {} with {}'.format(NEWJDK, OLDJDK))
        exit(0)
    ans = raw_input('\n\ngenerate bash-script to replace {} symbolic links? (Yes/n) : '.format(totals))
    if ans == 'Yes':
        relink_jdk(results)
        doit = raw_input('\n\nrun ./o.sh with elevated privs? \ni.e.: sudo ./o.sh   :(Yes/n) : ')
        if doit == 'Yes':
            call(['sudo', './o.sh'])
            print('{} is no longer needed and can be removed at your leisure.'.format(path.join(getcwd(), 'o.sh')))
