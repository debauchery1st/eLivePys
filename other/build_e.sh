#!/usr/bin/env bash

start=$(date +%Y%m%d%H%M%S);
su -c "apt install git sudo"
if [ "${1}" != "build" ]; then
  echo " this script will build Enlightenment on Debian 9 "
  echo " it should be run as a user and that user should be in the sudoers file"
  echo " if you have not done so already,"
  echo "        su -c visudo"
  echo " "
  echo " to continue building, add 'build' to the command line before pressing enter."
  exit 0
fi
echo "Enlightenment on Debian 9."
echo "[base development] Started at ${start}"
su -c "apt install autoconf autopoint libtool"
su -c "apt install gcc g++ check libssl-dev libsystemd-dev libjpeg-dev libglib2.0-dev libgstreamer1.0-dev libluajit-5.1-dev libfreetype6-dev libfontconfig1-dev libfribidi-dev libx11-dev libxext-dev libxrender-dev libgl1-mesa-dev libgif-dev libtiff5-dev libpoppler-dev libpoppler-cpp-dev libspectre-dev libraw-dev librsvg2-dev libudev-dev libmount-dev libdbus-1-dev libpulse-dev libsndfile1-dev libxcursor-dev libxcomposite-dev libxinerama-dev libxrandr-dev libxtst-dev libxss-dev libbullet-dev libgstreamer-plugins-base1.0-dev doxygen"
su -c "apt install libsdl2-dev"

echo "[required for python-efl bindings]"
su -c "apt install python-dbus-dev cython"

echo '[Enlightenment Foundation Libraries]'
git clone https://git.enlightenment.org/core/efl.git/
cd efl
./autogen.sh --prefix=/usr --enable-elua --enable-sdl --enable-ecore-buffer --with-opengl=full --with-dbus-services=/etc/init.d/
make
sudo make install
sudo ldconfig
cd ..
su -c "apt install python3-pip;pip3 install git+https://github.com/mesonbuild/meson.git;pip3 install ninja"
su -c "apt install libpam0g-dev libxcb-keysyms1-dev libcurl3 libcurl3-gnutls libcurl4-gnutls-dev"

echo '[Enlightenment]'
git clone https://git.enlightenment.org/core/enlightenment.git/
cd enlightenment
./autogen.sh --prefix=/usr -D mount-eeze=true -D buildtype=release
ninja -C build
sudo ninja -C build install

cd ..

echo '[evas_generic_loaders]'
git clone https://git.enlightenment.org/core/evas_generic_loaders.git/
cd evas_generic_loaders
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[rage]'
git clone https://git.enlightenment.org/apps/rage.git/
cd rage
./autogen.sh --prefix=/usr -D buildtype=release
ninja -C build
sudo ninja -C build install

cd ..

echo '[terminology]'
git clone https://git.enlightenment.org/apps/terminology.git/
cd terminology
./autogen.sh --prefix=/usr -D buildtype=release
ninja -C build
sudo ninja -C build install

cd ..

echo '[econnman]'
git clone https://git.enlightenment.org/apps/econnman.git/
cd econnman
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[ecrire]'
git clone https://git.enlightenment.org/apps/ecrire.git/
cd ecrire
mkdir build
cd build
cmake ..
make && sudo make install

cd ..

echo '[emprint]'
git clone https://git.enlightenment.org/apps/emprint.git/
cd emprint
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[ephoto]'
cd ephoto
git clone https://git.enlightenment.org/apps/ephoto.git/
./autogen.sh --prefix=/usr
ninja -C build && sudo ninja -C build install

cd ..

echo '[equate]'
git clone https://git.enlightenment.org/apps/equate.git/
cd equate
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[express]'
git clone https://git.enlightenment.org/apps/express.git/
cd express
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[extra]'
git clone https://git.enlightenment.org/apps/extra.git/
cd extra
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[desksanity]'
git clone https://git.enlightenment.org/enlightenment/modules/desksanity.git/
cd desksanity
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[python-efl]'
git clone https://git.enlightenment.org/bindings/python/python-efl.git/
cd python-efl
python setup.py build
sudo python setup.py install

cd ..

echo '[edgar]'
git clone https://git.enlightenment.org/enlightenment/modules/edgar.git/
cd edgar
sudo pip3 install python-efl
./autogen.sh --prefix=/usr PYTHON_VERSION=3.5 && make && sudo make install

cd ..

echo '[eenvader.fractal]'
git clone https://git.enlightenment.org/enlightenment/modules/eenvader.fractal.git/
cd eenvader.fractal
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[extramenu]'
git clone https://git.enlightenment.org/enlightenment/modules/extramenu.git/
cd extramenu
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[forecasts]'
git clone https://git.enlightenment.org/enlightenment/modules/forecasts.git/
cd forecasts
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[mem]'
git clone https://git.enlightenment.org/enlightenment/modules/mem.git/
cd mem
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[net]'
git clone https://git.enlightenment.org/enlightenment/modules/net.git/
cd net
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[penguins]'
git clone https://git.enlightenment.org/enlightenment/modules/penguins.git/
cd penguins
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[places]'
git clone https://git.enlightenment.org/enlightenment/modules/places.git/
cd places
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[presentator]'
git clone https://git.enlightenment.org/enlightenment/modules/presentator.git/
cd presentator
meson . build
ninja -C build
sudo ninja -C build install

cd ..

echo '[wallpaper2]'
git clone https://git.enlightenment.org/enlightenment/modules/wallpaper2.git/
cd wallpaper2
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[wlan]'
git clone https://git.enlightenment.org/enlightenment/modules/wlan.git/
cd wlan
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[libeweather]'
git clone https://git.enlightenment.org/libs/libeweather.git/
cd libeweather
$ ./autogen.sh --prefix=/usr && make && sudo make install

cd ..

echo '[emote]'
git clone https://git.enlightenment.org/devs/devilhorns/emote.git/
cd emote
./autogen.sh --prefix=/usr && make && sudo make install

cd ..

end=$(date +%Y%m%d%H%M%S);
elapsed=$(($end-$start));
echo 'finished building'
echo "Start  : ${start}\nStop   : ${end}\nElapsed: ${elapsed}"
