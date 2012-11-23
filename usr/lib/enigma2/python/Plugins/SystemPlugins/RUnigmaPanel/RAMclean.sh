#!/bin/sh
if [ -e /proc/sys/vm/swappiness ]; then
	echo "100" > /proc/sys/vm/swappiness
fi

if [ -e /proc/sys/vm/vfs_cache_pressure ]; then
	echo "10" > /proc/sys/vm/vfs_cache_pressure
fi

if [ -e /proc/sys/vm/dirty_expire_centisecs ]; then
	echo "500" > /proc/sys/vm/dirty_expire_centisecs
fi

if [ -e /proc/sys/vm/dirty_writeback_centisecs ]; then
	echo "1000" > /proc/sys/vm/dirty_writeback_centisecs
fi

if [ -e /proc/sys/vm/dirty_ratio ]; then
	echo "90" > /proc/sys/vm/dirty_ratio
fi

if [ -e /proc/sys/vm/dirty_background_ratio ]; then
	echo "5" > /proc/sys/vm/dirty_background_ratio
fi
echo cfq > /sys/block/sda/queue/scheduler
echo "Состояние RAM до очистки"
echo ""
free
echo "Очищаю pagecache..."
sleep 2
sync
echo 1 > /proc/sys/vm/drop_caches
echo "Очищаю dentrie и inode кэши..."
sleep 2
sync
echo 2 > /proc/sys/vm/drop_caches
echo "Очищаю pagecache, dentrie и inode кэши..."
sync
echo 3 > /proc/sys/vm/drop_caches
sleep 3
echo ""
echo "Состояние RAM после очистки"
echo ""
free
exit 0
sleep 3
echo "================================================"
echo "Оперативная память очищена успешно!!!"
echo "================================================"
echo ""