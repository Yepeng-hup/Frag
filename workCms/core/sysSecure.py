import re
from collections import Counter

from workCms.core.conf import log_dir, sys_log_dir, ip_count_num


def filterate(log_file: str) -> list:
    with open(log_file, 'r') as f:
        content = f.read()
    # 正则表达式匹配IP地址
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    ip_addresses_list = re.findall(ip_pattern, content)
    return ip_addresses_list


def count_frag_access_ip() -> dict:
    frag_ip_dict = {}
    frag_log_file = log_dir + "/frag_local.log"
    ip_list = filterate(frag_log_file)
    # 计元素出现的次数
    counter = Counter(ip_list)
    # 获取出现次数前10的元素及其出现次数
    most_common_elements = counter.most_common(ip_count_num)

    for element, count in most_common_elements:
        frag_ip_dict[element] = count
    return frag_ip_dict


def count_sys_ip() -> dict:
    sys_log_file = sys_log_dir + "/secure"
    ip_list = filterate(sys_log_file)
    counter = Counter(ip_list)
    most_common_elements = counter.most_common(ip_count_num)
    sys_ip_dict = {}
    for element, count in most_common_elements:
        sys_ip_dict[element] = count
    return sys_ip_dict
