from flask import Blueprint, jsonify, render_template, request, url_for, send_file
from random import choice
import os, traceback

from workCms.core.auxiliay import session_zsq
from workCms.databases.mysql_db import cursor, conn
from workCms import status_restful_api

documents = Blueprint('documents', __name__)


# url拼接视图
@documents.route('/documents/images/<imagesName>')
def initImages(imagesName):
    path = 'serviceall/documentsImages/' + imagesName
    return send_file(path)


@documents.route('/documents/images/upload', endpoint='/documents/images/upload', methods=['POST'])
@session_zsq
def uploadImages():
    all_images = list()
    images = request.files
    images_key = request.files.keys()
    # 拿到图片key
    images_key_list = list(images_key)
    for img in images_key_list:
        all_images.append(img)
        # 通过key保存对象
        file_value = images.get(img)
        file_value.save(os.path.join('workCms/serviceall/documentsImages', file_value.filename))
        saves_images = list(os.listdir('workCms/serviceall/documentsImages'))
        # print(saves_images)
        bools = img in saves_images
        if bools == True:
            return jsonify({"errno": 0, "data": [{"url": url_for("documents.initImages", imagesName=img),
                                                  "alt": img,
                                                  "href": ""}]
                            })
        else:
            traceback.format_exc()
            return jsonify({"errno": 1})


@documents.route('/documents/we', endpoint='/documents/we', methods=['POST', 'GET'])
@session_zsq
def documentsWrite():
    if request.method == 'GET':
        cursor.execute("select textlabel_title from textLabel")
        results = cursor.fetchall()
        return render_template('documentswe.html', title=results)
    else:
        try:
            title = request.form.get('title')
            classxz = request.form.get('classxz')
            context_html = request.form.get('content_html')
            cursor.execute("INSERT INTO documents (documents_title,documents_label,documents_text) VALUES "
                           "(%(title)s,%(label)s,%(text)s)", {"title": title, "label": classxz, "text": context_html})
            conn.commit()
            return jsonify({"code": status_restful_api.HttpCode.success, "message": "发布成功！"})
        except Exception:
            traceback.format_exc()
            return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "error发布失败！"})


@documents.route('/documents/rd', endpoint='/documents/rd', methods=['POST', 'GET'])
@session_zsq
def documentsRead():
    if request.method == 'GET':
        t_date = list()
        t_title = list()

        cursor.execute("select documents_date from documents  order by documents_id desc")
        results = cursor.fetchall()
        cursor.execute("select documents_title from documents  order by documents_id desc")
        results1 = cursor.fetchall()

        for k in results:
            for _, v in k.items():
                t_date.append(v)

        for i in results1:
            for _, s in i.items():
                t_title.append(s)
        date_title_dict = dict(zip(t_title, t_date))
        return render_template('documentsrd.html', rel=date_title_dict)
    else:
        t_date = list()
        t_title = list()

        searchRel = request.form.get('search')
        sql1 = """
            select documents_date from documents where documents_title like '%{title}%'  order by documents_id desc
        """.format(title=searchRel)
        sql2 = """
            select documents_title from documents where documents_title like '%{title}%'  order by documents_id desc
        """.format(title=searchRel)
        cursor.execute(sql1)
        rel1 = cursor.fetchall()
        cursor.execute(sql2)
        rel2 = cursor.fetchall()

        for k in rel1:
            for _, v in k.items():
                t_date.append(v)

        for i in rel2:
            for _, s in i.items():
                t_title.append(s)
        date_title_dict = dict(zip(t_title, t_date))
        return render_template('documentsrd.html', rel=date_title_dict)


@documents.route('/documents/catfiel/<filename>')
@session_zsq
def documentsCat(filename):
    cursor.execute("select documents_text from documents where documents_title=%(title)s", {"title": filename})
    results = cursor.fetchall()
    cursor.execute("select documents_date from documents where documents_title=%(title)s", {"title": filename})
    results1 = cursor.fetchall()
    filedate = results1[0]
    filedate = filedate['documents_date']
    musicDir = 'workCms/static/music'
    musicList = os.listdir(musicDir)
    # 随机抽取音乐
    music = choice(musicList)
    # print(music)
    return render_template('documentscat.html', fileRel=results, filename=filename, filedate=filedate, music=music)


@documents.route('/documents/class', endpoint='/documents/class')
@session_zsq
def documentsClass():
    title_list = list()
    thisTitleTextNum = list()
    cursor.execute("select textlabel_title from textLabel")
    rel = cursor.fetchall()
    for i in rel:
        for _, v in i.items():
            title_list.append(v)

    for i in title_list:
        cursor.execute("select documents_title from documents where documents_label=%(name)s", {"name": i})
        rel = cursor.fetchall()
        num = len(rel)
        thisTitleTextNum.append(num)
    title_num_dict = dict(zip(title_list, thisTitleTextNum))
    return render_template('documentsclass.html', title=title_list, textNum=thisTitleTextNum,
                           titleNumDict=title_num_dict)


@documents.route('/documents/create', endpoint='/documents/create', methods=['POST'])
@session_zsq
def labelCreate():
    label = request.form.get('label')
    # print(label)
    try:
        cursor.execute("INSERT INTO textLabel (textlabel_title) VALUES (%(label)s)", {"label": label})
        conn.commit()
        return jsonify({"code": status_restful_api.HttpCode.success, "message": "创建成功!"})
    except Exception:
        traceback.format_exc()
        return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "error创建失败!"})


@documents.route('/documents/del', endpoint='/documents/del', methods=['POST'])
@session_zsq
def delete_class():
    pass