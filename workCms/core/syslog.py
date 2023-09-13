import os
import zipfile
import shutil

from workCms.core.auxiliay import date2, dates


def create_dir(s):
    os.chdir(s)
    os.mkdir(date2)


def zip_logs(log_directory, zip_file_name="frag_local.log.zip"):
    create_dir(log_directory)
    # 创建一个新的zip文件
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 将文件添加到zip文件中
            zipf.write("frag_local.log", os.path.relpath("frag_local.log", log_directory+"/"+date2))
    shutil.move(zip_file_name, date2)
    print(f"{dates} 日志文件已压缩为 {zip_file_name}")