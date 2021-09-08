#!/bin/bash
#echo pid info

if [ -z $1 ];then
echo please input string
exit
fi

pid=$(ps -ef |grep $1 |grep -v grep|grep -v stop.sh|awk '{print $2}')

total=0
for p in ${pid}
do
 total=$[total + 1]
done



if [ $total -eq 0 ]
then
echo **not found!**
exit
fi

echo ""
echo **CAULTION: $total PROCESSES WILL BE KILLED**
echo ""

for p in ${pid}
do
 ps $p|grep $1 |grep -v grep
done

read  -p "kill all [yes/no]:" mainmenuinput

if [[ -n $mainmenuinput && $mainmenuinput == yes ]]
then

 for p in ${pid}
 do
 echo **kill... $p**
 ps $p |grep $1|grep -v grep
 kill $p
 tail --pid=$p -f /dev/null
 done

else

echo **skipped!**
exit

fi

echo **all killed**
