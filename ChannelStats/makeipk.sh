#!/bin/sh

PLUGIN_NAME='ChannelStats'
PLUGIN_VER='0.1'
PLUGIN_ARCH='all'
PLUGIN_DIR='/usr/lib/enigma2/python/Plugins/SystemPlugins/ChannelStats/'
PLUGIN_DESC='Gathering statistics watching TV'
PLUGIN_SITE='vitaliy69@gmail.com'
PLUGIN_FILTER='pyo|ini'
PLUGIN_DEPENDS='python-requests'
BUILD_DIR='./BUILD_IPK'

rm -fR $BUILD_DIR
mkdir -p $BUILD_DIR/DATA
mkdir -p $BUILD_DIR/CONTROL
curdate=$(date +%d.%m.%Y)

echo '2.0' > $BUILD_DIR/debian-binary
echo 'Package: '$PLUGIN_NAME > $BUILD_DIR/CONTROL/control
echo 'Version: '$PLUGIN_VER'_'$curdate >> $BUILD_DIR/CONTROL/control
echo 'Section: misc' >> $BUILD_DIR/CONTROL/control
echo 'Priority: optional' >> $BUILD_DIR/CONTROL/control
echo 'Architecture: '$PLUGIN_ARCH >> $BUILD_DIR/CONTROL/control
echo 'Homepage: '$PLUGIN_SITE >> $BUILD_DIR/CONTROL/control
echo 'Depends: '$PLUGIN_DEPENDS >> $BUILD_DIR/CONTROL/control

for file in $(find $PLUGIN_DIR -type f | grep -E $PLUGIN_FILTER | sed -e '/\/\..*$/d')
    do
    dirBuild=$BUILD_DIR/DATA$(echo $file | sed 's/\(.*\)\/.*$/\1/')
    mkdir -p $dirBuild
    cp $file $dirBuild
    fl=$(echo $file | sed 's/.*\/\(.*$\)/\1/')
    filelist=$filelist'file://'$fl' ' 
#   tarlist=$tarlist' '$file
    done
echo 'Source: '$filelist >> $BUILD_DIR/CONTROL/control
echo 'Description: '$PLUGIN_DESC >> $BUILD_DIR/CONTROL/control

chmod 644 $BUILD_DIR/CONTROL/* $BUILD_DIR/debian-binary
tar -czf $BUILD_DIR/control.tar.gz -C $BUILD_DIR/CONTROL .
tar -czf $BUILD_DIR/data.tar.gz -C $BUILD_DIR/DATA .
namepk='./'$PLUGIN_NAME'_'$PLUGIN_VER'_'$curdate'_'$PLUGIN_ARCH'.ipk'
./ar -crf $namepk $BUILD_DIR/debian-binary $BUILD_DIR/data.tar.gz $BUILD_DIR/control.tar.gz
rm -fR $BUILD_DIR
