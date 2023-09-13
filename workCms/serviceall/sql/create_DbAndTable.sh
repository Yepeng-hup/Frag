#!/bin/bash

read -p "是否开始执行脚本【yes/on】: " USE
if [ $USE == 'on' ]
then
    exit 0
fi
read -p "请输入数据库主机ip: " HOST
read -p "请输入数据库名字: " DBNAME
read -p "请输入数据库连接用户: " USERS
read -p "请输入数据库密码: " PASSWD
read -p "请输入数据库连接端口: " PORT

function main(){
    local db=$1
    mysql -u ${USERS} -p${PASSWD} -h $HOST -P $PORT $db < ./frag_tables.sql
    if [ `echo $?` -eq 0 ];then
        echo "数据表导入成功！" 
    else 
        echo "数据表导入失败！" 
    fi
}
main $DBNAME

