#!/usr/bin/env bash

if [ `echo "$#"` != "1" ];then
  echo -e "\033[31;234mUse $0 ['start/stop/status']\033[0m"
  echo "  start    --  Start Service."
  echo "  stop     --  Stop service."
  echo "  status   --  View Service status."
  exit 1
fi

TP=$1

function check_py() {
    which python3 > /dev/null
    if [ `echo "$?"` != "0" ];then
      echo -e "\033[31;234merror: not install python3!\033[0m"
      exit 1
    fi
}
check_py


function start() {
    s=$(ps -ef|egrep -v "grep|frag_tp"|grep "frag")
    if [[ $s == "" ]];then
      nohup python3 ./frag_run.py > /dev/null 2>&1 &
      ps -ef|egrep -v "grep|frag_tp"|grep "frag"
      if [ `echo "$?"` == "0" ];then
        echo -e "\033[32;234mINFO: frag start success!\033[0m"
      else
        echo -e "\033[31;234merror: frag start fail!\033[0m"
      fi
    else
      echo -e "\033[32;234mINFO: frag server is run!\033[0m"
    fi
}

function stop() {
    frag_pid=$(ps -ef|egrep -v "grep|frag_tp"|grep "frag"|awk '{print $2}')
    for i in ${frag_pid};do
      kill "$i"
      if [ `echo "$?"` != "0" ];then
        kill -9 "$i"
      fi
    done
    echo -e "\033[32;234mINFO: frag server is stop!\033[0m"
}

function status() {
    pid=$(ps -ef|grep -v "grep"|grep "frag"|head -1|awk '{print $2}')
    if [[ ${pid} == "" ]];then
      echo -e "\033[31;234merror: frag server not is run!\033[0m"
      exit 1
    fi
    port=$(netstat -tanp|grep "$pid"|grep -w "LISTEN"|awk '{print $4}'|awk -F":" '{print $2}')
    if [ ! $port ];then
      echo -e "\033[32;234mINFO: STATUS --> LISTENPORT: None\033[0m"
    else
      echo -e "\033[32;234mINFO: STATUS --> LISTENPORT: ${port}\033[0m"
    fi
    netstat -tanp|grep "$pid"|grep -w "LISTEN"
}

if [ ${TP} == "start" ];then
  start
elif [ ${TP} == "stop" ];then
  stop
elif [ ${TP} == "status" ];then
  status
else
  echo -e "\033[31;234merror: not parameter!\033[0m"
  exit 1
fi
