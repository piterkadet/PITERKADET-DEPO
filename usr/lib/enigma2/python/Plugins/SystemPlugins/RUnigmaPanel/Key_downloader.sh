#!/bin/sh
echo ""
echo "Загружаю ключи для РУнигмы3..."
echo ""
cd /tmp
#keys 
wget http://www.uydu.ws/deneme6.php?file=SoftCam.Key -O /tmp/SoftCam.Key
wget http://www.uydu.ws/deneme6.php?file=softcam.cfg -O /tmp/softcam.cfg
wget http://www.uydu.ws/deneme6.php?file=nagra -O /tmp/nagra
wget http://www.uydu.ws/deneme6.php?file=AutoRoll.Key -O /tmp/AutoRoll.Key
wget http://www.uydu.ws/deneme6.php?file=constant.cw -O /tmp/constant.cw
wget http://www.uydu.ws/deneme6.php?file=tps.au -O /tmp/tps.au
wget http://www.uydu.ws/deneme6.php?file=camd3.keys -O /tmp/camd3.keys
scce
wget http://www.uydu.ws/deneme6.php?file=keylist -O /tmp/keylist
wget http://www.uydu.ws/deneme6.php?file=rsakeylist -O /tmp/rsakeylist
wget http://www.uydu.ws/deneme6.php?file=constantcw -O /tmp/constantcw
wget http://www.skystar.org/arsiv/dailytps/tps.au -O /tmp/tps.au
wget http://www.skystar.org/arsiv/dailytps/tps.bin -O /tmp/tps.bin
echo "______________________________"
find /tmp/SoftCam.Key
find /tmp/softcam.cfg
find /tmp/nagra
find /tmp/AutoRoll.Key
find /tmp/constant.cw
find /tmp/tps.au
find /tmp/camd3.keys
find /tmp/keylist
find /tmp/rsakeylist
find /tmp/constantcw
echo ""
chmod 755 /tmp/SoftCam.Key
chmod 755 /tmp/softcam.cfg
chmod 755 /tmp/nagra
chmod 755 /tmp/AutoRoll.Key
chmod 755 /tmp/constant.cw
chmod 755 /tmp/tps.au
chmod 755 /tmp/camd3.keys
chmod 755 /tmp/keylist
chmod 755 /tmp/rsakeylist
chmod 755 /tmp/constantcw
echo ""
cp SoftCam.Key /var/keys/
cp softcam.cfg /var/keys/
cp nagra /var/keys/
cp AutoRoll.Key /var/keys/
cp constant.cw /var/keys/
cp tps.au /var/keys/
cp camd3.keys /var/keys/
cp keylist /var/scce/
cp rsakeylist /var/scce/
cp constantcw /var/scce/
echo ""
rm -rf /tmp/SoftCam.Key
rm -rf /tmp/softcam.cfg
rm -rf /tmp/nagra
rm -rf /tmp/AutoRoll.Key
rm -rf /tmp/constant.cw
rm -rf /tmp/tps.au
rm -rf /tmp/camd3.keys
rm -rf /tmp/keylist
rm -rf /tmp/rsakeylist
rm -rf /tmp/constantcw
echo ""
echo "Все ключи обновлены!!!"
echo ""
echo "Не забудьте перезапустить эмулятор..."
echo ""
exit 0
