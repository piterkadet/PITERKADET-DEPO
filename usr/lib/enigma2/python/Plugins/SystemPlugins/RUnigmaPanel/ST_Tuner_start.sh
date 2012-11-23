#!/bin/sh
   cp /etc/init.d/initmodules /var/initmodules
   sed 's/modprobe fe-core demod=stb0899 tuner=stb6100/modprobe fe-core.ko demod=stv090x tuner=stv6110x/' /var/initmodules >/etc/init.d/initmodules
   rm   /var/initmodules
   echo "Тюнер переведен в режим ST..."
   echo
   echo "Ваш ресивер сейчас будет перезагружен для применения изменений..."
   sleep 3
   reboot -f
   exit   









