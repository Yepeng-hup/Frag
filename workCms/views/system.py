from flask import Blueprint, render_template
import psutil
import platform

from workCms.databases.mysql_db import cursor
from workCms.core.auxiliay import session_zsq, get_size

system = Blueprint('system', __name__)


@system.route('/system_zs', endpoint='system_zs')
@session_zsq
def system_zs():
    cursor.execute(
        "select system_datetime,system_ResourcesNum from system where system_ResourcesName='CPU' order by system_id desc limit 40")
    results = cursor.fetchall()
    cursor.execute(
        "select system_datetime,system_ResourcesNum from system where system_ResourcesName='MEM' order by system_id desc limit 40")
    results_mem = cursor.fetchall()
    cpuInfo = []
    memInfo = []
    for i in results:
        for k, v in i.items():
            if k == 'system_ResourcesNum':
                cpuInfo.append(v)
    for mem in results_mem:
        for mem_k, mem_v in mem.items():
            if mem_k == 'system_ResourcesNum':
                mem_v = float(mem_v) / 1024
                # 保留小数点后2位
                memInfo.append(round(mem_v, 2))
    # 转换浮点
    cpuInfo = [float(i) for i in cpuInfo]
    memInfo = [float(i) for i in memInfo]

    uname = platform.uname()
    systemName = f"系统类型: {uname.system}"
    systemNodeName = f"系统主机名: {uname.node}"
    systemVer = f"系统版本: {uname.version}"
    machine = f"系统处理器架构: {uname.machine}"
    cpuCore = f"CPU总核: {psutil.cpu_count(logical=True)}核"
    mem = psutil.virtual_memory()
    memTotal = f"总内存: {get_size(mem.total)}"

    diskUses = {}
    partitions = psutil.disk_partitions()
    for i in partitions:
        try:
            partition_usage = psutil.disk_usage(i.mountpoint)
        except PermissionError:
            continue
        diskUses[i.mountpoint] = get_size(partition_usage.total)
    # diskK = diskUses.keys()
    # diskV = diskUses.values()
    return render_template('system_zs.html',
                           memUse=memInfo,
                           cpuUse=cpuInfo,
                           systemName=systemName,
                           systemNodeName=systemNodeName,
                           systemVer=systemVer,
                           machine=machine,
                           cpuCore=cpuCore,
                           memTotal=memTotal,
                           diskUses=diskUses
                           )
