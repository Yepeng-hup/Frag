from flask import render_template, request, Blueprint, jsonify, send_file
import os, traceback
from pathlib import Path

from workCms.core.auxiliay import session_zsq, dates
from workCms.core.conf import data_save

file = Blueprint('file', __name__)


@file.route('/push', endpoint='push')
@session_zsq
def push():
    backupDir = []

    systemSave_dir = data_save
    v = os.path.exists(systemSave_dir)
    if v == True:
        backupData = []
        files_dir = os.listdir(systemSave_dir)
        for i in files_dir:
            my_file = Path(systemSave_dir + "/" + i)
            if my_file.is_dir():
                backupData.append(i)
    else:
        return jsonify({"ERROR": {
            "status": "error",
            "errorInfo": "主目录不存在，请手动创建目录!",
            "tips": "配置frag.yaml中PushData_save_dir字段."
        }})

    files_dir = os.listdir(data_save)
    for file in files_dir:
        backupDir.append(file)
    return render_template('push.html', backupData=backupData, backupDir=backupDir)


@file.route('/push_w', endpoint='push_w', methods=['POST'])
@session_zsq
def push_w():
    backupData = []
    backupDir = []
    try:
        saveDir = request.form['num']
        file_data = request.files.getlist('file')
        for file in file_data:
            file.save(os.path.join(data_save + saveDir, file.filename))

        files_dir = os.listdir(data_save)
        for i in files_dir:
            my_dir = Path(data_save + i)
            if my_dir.is_dir():
                backupDir.append(i)

        datadir = os.listdir(data_save + saveDir)
        for x in datadir:
            backupData.append(x)

        return render_template('push.html', status="文件上传成功", backupDir=backupDir, backupData=backupData)
    except:
        print("push_w" + " " + dates + '  上传数据有错误！！！\n' + traceback.format_exc())

        files_dir = os.listdir(data_save)
        for file in files_dir:
            backupDir.append(file)
        return render_template('push.html', status="文件上传失败", backupDir=backupDir, backupData=backupData)


@file.route('/download', endpoint='/download')
@session_zsq
def download():
    # 浏览器下载链接: http://ip:port/download?file_name=1.sh&file_dir=test
    # linux下载链接: curl -# -o 1.txt http://ip:port/download?file_name=1.sh&file_dir=test
    file_name = request.args.get('file_name')
    file_dir = request.args.get('file_dir')
    path = data_save + file_dir + '/' + '%s' % file_name
    return send_file(path, as_attachment=True)
