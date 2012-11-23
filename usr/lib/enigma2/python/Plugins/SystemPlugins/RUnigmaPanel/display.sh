#!/bin/sh
   cp /etc/init.d/initmodules /var/initmodules
   sed 's/#fp_control -nf 0/fp_control -nf 0/' /var/initmodules >/etc/init.d/initmodules
   fp_control -nf 0
   rm   /var/initmodules
   echo "Маленькие часы слева удалены..."
   echo
   echo "Вы всегда сможете вернуть их назад..."
   exit   




