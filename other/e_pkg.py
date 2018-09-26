#!/usr/bin/env python
from time import sleep
from os import path, getcwd
from sys import argv
from subprocess import check_output, call

install_fpm = "sudo apt-get install ruby ruby-dev rubygems build-essential;sudo gem install --no-ri --no-rdoc fpm"
control_fields = {'PACKAGE': 'Package: {}',
                  'VERSION': 'Version: {}',
                  'MAINTAINER': 'Maintainer: {}',
                  'ARCHITECTURE': 'Architecture: {}',
                  'DESCRIPTION': 'Description: {}'
                  }
kung_foo = 'DESTDIR={} ninja install .'
make_foo = 'make DESTDIR={} install'


def dump_dirs(trunk, tmp='/var/tmp'):
    tmp_f = path.join(tmp, 'e_dir.sh')
    _src_dir = path.join(trunk, '*/')
    with open(tmp_f, 'w') as f:
        f.write("#!/bin/bash\nls -d {}\n".format(_src_dir))
    f.close()
    check_output('chmod +x {}'.format(tmp_f).split(' '))
    dir_list = check_output(tmp_f).decode('utf8').split('\n')
    x = [y.split(trunk)[1].strip('/') for y in dir_list if len(y) > 1]
    sleep(.123)
    check_output(['rm', tmp_f])
    return x


def create_debs(trunk, dirlist):
    print('trunk : {}'.format(trunk))
    last_location = str(getcwd())
    for k in dirlist:
        print('\n')
        pkg_name = control_fields['PACKAGE'].format(k)
        pkg_ver = control_fields['VERSION'].format('0.0')
        pkg_maintainer = control_fields['MAINTAINER'].format('{} developer(s)'.format(k))
        pkg_arch = control_fields['ARCHITECTURE'].format('all')
        pkg_desc = control_fields['DESCRIPTION'].format('local build')
        dest = '/tmp/{}'.format(k)
        make_fake = "mkdir {}".format(dest)
        # figure foo
        _src_dir = path.join(trunk, k)
        if path.isfile(path.join(_src_dir, 'meson.build')):
            foo = kung_foo.format(dest)
        else:
            foo = make_foo.format(dest)
        fake_inst = "cd {};{}".format(_src_dir, foo, dest)
        fpm_cmd = ' '.join(['fpm', '-s', 'dir',
                            '-t', 'deb', '-C', dest, '--name', k,
                            '--depends', 'debian_dependency1'])
        cli = ';'.join([make_fake, fake_inst, fpm_cmd])
        print('\n'.join([pkg_name, pkg_ver, pkg_maintainer, pkg_arch, pkg_desc, cli]))
        f_name = '/tmp/build_{}.sh'.format(k)
        with open(f_name, 'w') as f:
            f.write("#!/bin/bash\n" + cli.replace(';', '\n') + '\n')
        f.close()
        sleep(.5)
        call(['chmod', '+x', f_name])
        call([f_name])
        sleep(.5)


if __name__ == "__main__":
    if len(argv) < 2:
        print("\nInstalling Dependencies\n")
        f_name = '/tmp/inst_fpm.sh'
        with open(f_name, 'w') as f:
            f.write("#!/bin/bash\n" + install_fpm + '\n')
        f.close()
        call(['chmod', '+x', f_name])
        call([f_name])
        print("[EXAMPLE]\ndir/\ndir/efl\ndir/enlightenment\ndir/terminology\ndir/[etc..]")
        print("\n[USAGE]:\n{} /absolute/path/to/dir/\n".format(path.abspath(__file__)))
        exit(1)
    create_debs(argv[1], dump_dirs(argv[1]))
