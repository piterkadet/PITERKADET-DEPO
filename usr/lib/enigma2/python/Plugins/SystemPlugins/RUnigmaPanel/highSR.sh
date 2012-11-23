#!/bin/sh

. /var/config/language.conf

#-------------------------------------------------------------------------------
#language section
#-------------------------------------------------------------------------------

if [ $lang == en ]; then

  info1="Patch activated"
  info2="Patch deactivated"
  info3="Restart box to save changes!"

elif [ $lang == ru ]; then

  info1="Изменения внесены"
  info2="Изменения отменены"
  info3="Перезагрузите ресивер для вступления изменений в силу!"  

fi
#-------------------------------------------------------------------------------
#script section
#-------------------------------------------------------------------------------

highSR_on()
{
 echo highSR=on >/var/config/highSR.conf
 sync
 echo "$info1"
 echo "\n$info3" 
} 

highSR_off()
{
 echo highSR=off >/var/config/highSR.conf
 sync
 echo "$info2"
 echo "\n$info3" 
}

#-------------------------------------------------------------------------------
#use section
#-------------------------------------------------------------------------------

case "$1" in
 'on')
    highSR_on
    ;;
 'off')
    highSR_off
    ;;
 *)
    echo -e "\nUse: highSR.sh on|off"
    ;;
esac

echo ""
exit 0