from flask import Blueprint, render_template, request, jsonify
import traceback

from workCms.core.auxiliay import session_zsq, execute_time_decorator
from workCms.core.sysSecure import count_frag_access_ip, count_sys_ip
from workCms.modeCls.iptablesModule import Iptables

secure = Blueprint('secure', __name__)


def frag() -> (list, dict):
    frag_ip_status = dict()
    frag_rel = count_frag_access_ip()
    for i in frag_rel:
        s = Iptables(i)
        b = s.show_cl_status()
        frag_ip_status[i] = b
    return frag_rel, frag_ip_status


def sys() -> (list, dict):
    sys_ip_status = dict()
    sys_rel = count_sys_ip()
    for i in sys_rel:
        s = Iptables(i)
        b = s.show_cl_status()
        sys_ip_status[i] = b
    return sys_rel, sys_ip_status


@secure.route('/secure/index/', endpoint='/secure/index')
@session_zsq
def secure_index():
    frag_rel, frag_ip_status = frag()
    sys_rel, sys_ip_status = sys()
    return render_template("secure.html", frag_ip_dict=frag_rel,
                           frag_ip_status=frag_ip_status,
                           sys_ip_dict=sys_rel,
                           sys_ip_status=sys_ip_status)


@secure.route('/secure/cl/drop/drop', endpoint='/secure/cl/drop/drop', methods=['POST'])
@session_zsq
def secure_cl_drop():
    use_status = request.form.get("drop_status")
    lists = use_status.split('\t')
    ip = lists[1]
    i = Iptables(ip)
    b = i.dorp()
    if b:
        return jsonify({"code": 200, "message": "禁止成功."})
    else:
        return jsonify({"code": 500, "message": "禁止失败."})


@secure.route('/secure/cl/drop/del', endpoint='/secure/cl/drop/del', methods=['POST'])
@session_zsq
def secure_cl_del_drop():
    del_status = request.form.get("delDrop_status")
    del_list = del_status.split('\t')
    ip = del_list[1]
    i = Iptables(ip)
    b = i.del_drop()
    if b:
        return jsonify({"code": 200, "message": "解封成功."})
    else:
        return jsonify({"code": 500, "message": "解封失败."})


@secure.route('/secure/ip/index', endpoint='/secure/ip/index')
@session_zsq
def ip_index():
    return render_template('ipInfo.html')


@secure.route('/secure/ip', endpoint='/secure/ip', methods=['POST'])
# @execute_time_decorator
# 访问格式 http://127.0.0.1:14000/secure/ip?addr=114.114.114.114
def show_ip_info():
    # ip = request.args.get("addr")
    ip = request.form.get("addr")
    s = Iptables(ip)
    try:
        c, f = s.get_country_by_ip()
        return render_template('ipInfo.html',
                               ip=ip,
                               country=c,
                               info=f
                               )
    except:
        print(traceback.format_exc())
        return render_template('ipInfo.html', error="ip addr query fail, network timeout.")
