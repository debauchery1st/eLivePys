#!/bin/sh
(
lookforJdks=$PWD
echo "Directory: $lookforJdks"
jdks=`test -e ./javac || find $lookforJdks -type d -iname '*jdk-1.*' 2> /dev/null`
#set -e
echo 'which jdk do you want to choose? looking for jdks. This might take a while'
echo "$jdks" | awk '{printf("%5d : %s\n", NR,$0)}'
read choose
test -e ./javac || cd `echo "$jdks" | tr '\n' ',' | cut -d',' -f $choose`/bin
for e in appletviewer extcheck idlj jar jarsigner java javac javadoc javah javap jconsole \
 jdb jhat jinfo jmap jps jrunscript jsadebugd jstack jstat jstatd native2ascii rmic \
 schemagen serialver wsgen wsimport xjc jvisualvm jmc; do sudo update-alternatives \
 --install /usr/bin/$e $e $(readlink -f ./$e) 100; done
)

echo "RUN update-alternatives --config java"

