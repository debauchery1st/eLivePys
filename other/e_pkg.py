#!/usr/bin/env python
from time import sleep, time
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
kung_foo = 'sudo PREFIX=/usr DESTDIR={} ninja -C build install'
make_foo = 'sudo make DESTDIR={} install'
foo_order = ['efl', 'enlightenment', 'rage', 'terminology']


def dump_dirs(trunk, tmp='/var/tmp'):
    tmp_f = path.join(tmp, 'e_dir.sh')
    _src_dir = path.join(trunk, '*/')
    with open(tmp_f, 'w') as f:
        f.write("#!/bin/bash\nls -d {}\n".format(_src_dir))
    f.close()
    check_output('chmod +x {}'.format(tmp_f).split(' '))
    dir_list = check_output(tmp_f).split('\n')
    x = [y.split(trunk)[1].strip('/') for y in dir_list if len(y) > 1]
    sleep(.123)
    check_output(['rm', tmp_f])
    return x


def f_run(cmd_str, check=False):
    r = True
    f_name = '/tmp/f_run_{}.sh'.format(str(time()).replace('.', ''))
    with open(f_name, 'w') as f:
        f.write("#!/bin/bash\n{}\n".format(cmd_str))
    f.close()
    sleep(.5)
    call(['chmod', '+x', f_name])
    if check:
        r = check_output([f_name])
    else:
        call([f_name])
    sleep(.1)
    call(['rm', '-rf', f_name])
    return r


def create_debs(trunk, dl):
    print('trunk : {}'.format(trunk))
    last_location = str(getcwd())
    _digits = [str(n) for n in range(10)] + ['.']
    dirlist = foo_order + [str(foo.decode('utf8')) for foo in dl if foo not in foo_order]
    for k in dirlist:
        _src_dir = path.join(trunk, k)
        _vercmd = "grep PACKAGE_VERSION {}".format(path.join(_src_dir, "configure"))
        print(_vercmd)
        print('\n')
        _verstr = f_run(_vercmd, check=True).split('\n')[0].split('=').pop()
        cur_ver = ''.join([char for char in _verstr if char in _digits])
        pkg_name = control_fields['PACKAGE'].format(k)
        pkg_ver = control_fields['VERSION'].format(cur_ver)
        pkg_maintainer = control_fields['MAINTAINER'].format('{} developer(s)'.format(k))
        pkg_arch = control_fields['ARCHITECTURE'].format('amd64')
        pkg_desc = control_fields['DESCRIPTION'].format('local build')
        dest = '/tmp/{}'.format(k)
        # clean old /tmp/destination
        if path.isdir(dest):
            cont = raw_input("path {} already exists, may I remove it? (y/n): ".format(dest))
            if cont not in ['Y', 'y', 'Yes']:
                exit(0)
            call(['rm', '-rf', dest])
        make_fake = "mkdir -p {}".format(dest)
        # figure foo
        if path.isfile(path.join(_src_dir, 'meson.build')):
            foo = kung_foo.format(dest)
        else:
            foo = make_foo.format(dest)
        fake_inst = "cd {};{}".format(_src_dir, foo, dest)
        fpm_cmd = ' '.join(['fpm', '-s', 'dir', '-t', 'deb', '-v', cur_ver, '-C', dest, '--name', k])
        cli = ';'.join([make_fake, fake_inst, fpm_cmd])
        print('\n'.join([pkg_name, pkg_ver, pkg_maintainer, pkg_arch, pkg_desc, cli]))
        f_name = '/tmp/build_{}.sh'.format(k)
        f_run(cli.replace(';', '\n'))
        sleep(.5)
        f_run(' '.join(['mv', path.join(_src_dir, '*.deb'), last_location]))


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

