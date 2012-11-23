#!/bin/sh

. /var/config/emu.conf
. /var/config/swap.conf
. /var/config/language.conf

#-------------------------------------------------------------------------------
#language section
#-------------------------------------------------------------------------------

if [ $lang == en ]; then

  info4="Used:" 
  info6="Memory usage: "
  info7="Total:" 
  info8="Free:"
  info9="Net settings:"
  info10="IP address:"
  info11="Mask:"
  info12="Gate:"

 elif [ $lang == ru ]; then

  info4="Занято:"
  info6="ИСПОЛЬЗОВАНИЕ ПАМЯТИ: "
  info7="Всего:"
  info8="Свободно:"
  info9="УСТАНОВКИ СЕТИ:"
  info10="IP-адрес ресивера:"
  info11="Маска сети:"
  info12="DNS-адрес:"

fi

#-------------------------------------------------------------------------------
#script section
#-------------------------------------------------------------------------------

echo $info6
echo ""
free1=`free | grep Mem | awk '{print $2 "  " $3 "  " $4}'`
free2=`free | grep Swap | awk '{print $2 "  " $3 "  " $4}'`
free3=`free | grep Total | awk '{print $2 "  " $3 "  " $4}'`
echo "     $info7  $info4  $info8"
echo "Mem: $free1"
echo "Swap: $free2"
echo "SWAP: $swap"
echo ""                                   
echo $info9
echo ""
mac=`ifconfig eth0 | grep HWaddr | awk '{print $5}'`
echo "Mac-адрес ресивера: $mac"
adres=`ifconfig eth0 | grep addr: | awk '{gsub(/:/," "); print $3}'`
echo "$info10 $adres"
maska=`ifconfig eth0 | grep addr: | awk '{gsub(/:/," "); print $7}'`
echo "$info11 $maska"
dns=`cat /etc/resolv.conf | grep nameserver | awk '{gsub(/:/," "); print "DNS-адрес ресивера: "$2}'`
echo "$dns"
echo ""
echo "ЗАПУЩЕННЫЙ ЭМУЛЯТОР: $emu"
echo ""
 
exit 0
