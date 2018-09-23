#!/usr/bin/env python
from os import path, getcwd
from subprocess import check_output, call
from argparse import ArgumentParser

ALTWD = "/etc/alternatives"                                # alternatives working directory
OLDJDK = "/usr/lib/jvm/java-7-openjdk-i386"                # old jdk
NEWJDK = "/opt/obuildfactory/jdk-1.8.0-openjdk-i686"       # new jdk
INST = "cp ./install-java.sh /opt/obuildfactory;cd /opt/obuildfactory;chmod +x ./install-java.sh;./install-java.sh"

parser = ArgumentParser()
parser.add_argument("-r", "--reverse", help="new -> old")
parser.add_argument("-i", "--install", help="dont compile")
parser.add_argument("-m", "--manual", help="manually relink /etc/alternatives")


def set_vars(args):
    _use_alternatives = True
    _e = 0
    if args.__getattribute__('manual') is not None:
        _use_alternatives = False
    if args.__getattribute__('install') is not None:
        _e = 1
    if args.__getattribute__('reverse') is not None:
        print('reverse')
        return ALTWD, _e, NEWJDK, OLDJDK, _use_alternatives
    return ALTWD, _e, OLDJDK, NEWJDK, _use_alternatives


def old_check_jdk(alt_wd=ALTWD, old_jdk=OLDJDK, new_jdk=NEWJDK):
    relevant = {}
    missing = []
    for row in check_output(['ls', '-al', alt_wd]).split('\n'):
        if 'openjdk' in row:
            d = None
            a, b = row.split(' -> ')
            try:
                c = b.split(old_jdk)[-1]
                d = new_jdk + c
            except IndexError as e:
                pass
            if d is not None and path.exists(d):
                relevant[a.split(' ')[-1]] = d
            else:
                missing.append(row)
    docs = [m for m in missing if "man/man" in m]
    other = [o for o in missing if o not in docs and new_jdk not in o]
    if len(other) > 0:
        print("\n\npossibly missing alternatives (you may have to fix these by hand)\n")
        for _ in other:
            print('{}{}'.format('\t', _))
    return relevant


def tmp_link(results):
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


def relink_jdk(data, alt_wd=ALTWD):
    f = open('o.sh', 'w')
    f.write("#!/usr/bin/env bash\nORIGN=$(pwd)\ncd {}\nclear\npwd\n".format(alt_wd))
    for k, v in data.iteritems():
        _target_link = path.join(alt_wd, k)
        _new_link = v.replace('jre/', '') # fixes broken link
        try:
            assert path.exists(_target_link)
            assert path.exists(_new_link)
        except AssertionError as e:
            print(_target_link, _new_link)
            raise e
        f.write('rm {}\nln -s {} ./{}\n'.format(k, _new_link, k))
    f.close()
    call(['chmod', '+x', 'o.sh'])


if __name__ == "__main__":
    a, e, o, n, _automatic = set_vars(parser.parse_args())
    if not _automatic:
        print('WORKING DIRECTORY: {}\nOLD: {}\nNEW: {}\n'.format(a, o, n))
        tmp_link(old_check_jdk(alt_wd=a, old_jdk=o, new_jdk=n))
    else:
        call(['su', '-c', INST])
