#!/bin/bash

#color define
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


#echo pid info
if [ -z $1 ];then
echo please input string
exit
fi

pid=$(ps -ef |grep $1 |grep -v grep|grep -v stop_process.sh|grep -v stop_process|awk '{print $2}')

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

echo -e *****************************************************************************${GREEN}
for p in ${pid}
do
 ps $p|grep $1 |grep -v grep
done
echo -e "${NC}*****************************************************************************"

echo ""
echo -e ${RED}** CAULTION: $total PROCESSES WILL BE KILLED **${NC}
echo ""


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
