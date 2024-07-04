#!/bin/sh

git clone https://github.com/jwrdegoede/ipu6-drivers.git

cd ipu6-drivers

COMMIT=$(git rev-list HEAD -n1)
SHORTCOMMIT=$(echo ${COMMIT:0:7})
DATE=$(git log -1 --format=%cd --date=short | tr -d \-)

git clone https://github.com/intel/ivsc-driver.git
cp -r ivsc-driver/backport-include ivsc-driver/drivers ivsc-driver/include .
rm -rf ivsc-driver .git patch

cd ..

mv ipu6-drivers ipu6-drivers-$COMMIT

tar --remove-files -czf ipu6-drivers-$SHORTCOMMIT.tar.gz ipu6-drivers-$COMMIT

sed -i \
    -e "s|%global commit0.*|%global commit0 ${COMMIT}|g" \
    -e "s|%global date.*|%global date ${DATE}|g" \
    ipu6-kmod.spec

rpmdev-bumpspec -c "Update to latest snapshot." ipu6-kmod.spec
