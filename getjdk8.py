#!/usr/bin/env python
from os import path, getcwd
from subprocess import call

prep_build = """
sudo apt-get install git mercurial zip bzip2 unzip tar curl
sudo apt-get install ccache make gcc g++ ca-certificates ca-certificates-java
sudo apt-get install libX11-dev libxext-dev libxrender-dev libxtst-dev
sudo apt-get install libasound2-dev libcups2-dev libfreetype6-dev
sudo apt-get install build-essential
sudo apt-get install openjdk-7-jdk
"""
prep_fpm = """
sudo apt-get install ruby-full
sudo apt-get install ruby1.9.1-full
"""
install_fpm = "gem install --no-ri --no-rdoc fpm\n"
clone_builder = """
mkdir ~/openjdkathome
cd ~/openjdkathome
git clone https://github.com/hgomez/obuildfactory.git
"""
build_builder = """
cd ~/openjdkathome
XUSE_FPM=true XPACKAGE=true XCLEAN=true XUSE_NEW_BUILD_SYSTEM=true XBUILD=true ./obuildfactory/openjdk8/linux/standalone-job.sh
"""
install_builder = """
cd ~/openjdkathome/OBF_DROP_DIR/openjdk8
sudo dpkg -i openjdk8_1.8.0-u192-b03_i386.deb
"""


def get_jdk8():
    # create script to dl & build OpenJDK8 for elive 3.0_x32
    with open('oj.sh', 'w') as f:
        f.write('#!/usr/bin/env bash\n')
        f.write('echo preparing to dl openjdk8\n')
        f.write(prep_build)
        f.write('echo preparing fpm\n')
        f.write(prep_fpm)
        f.write('echo installing FPM (for creating debian packages)\n')
        f.write(install_fpm)
        f.write('echo ...\n')
        f.write(clone_builder)
        f.write('echo ...building\n')
        f.write(build_builder)
        f.write('echo installing debian pkg')
        f.write(install_builder)
    f.close()
    call(['chmod', '+x', 'oj.sh'])
    return path.join(getcwd(), 'oj.sh')
