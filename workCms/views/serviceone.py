from flask import render_template, Blueprint, request, jsonify
import traceback, logging

from workCms.core.auxiliay import session_zsq

serviceone = Blueprint('serviceone', __name__)

urlList = list()
urlName = list()
urlFileDir = "workCms/serviceall/txt/url.txt"


@serviceone.route('/serviceone', endpoint='/serviceone', methods=['POST', 'GET'])
@session_zsq
def serviceOne():
    if request.method == 'POST':
        url = request.form.get('url')
        serviceName = request.form.get('serviceName')
        if url == '':
            logging.error('error: url is null!')
        elif serviceName == '':
            logging.error('error: serverName is null!')
        else:
            with open(urlFileDir, 'a', encoding='utf-8') as f:
                f.write(f"{serviceName} {url}\n")
                f.close()

        urlList.clear()
        urlName.clear()
        f = open(urlFileDir, 'r', encoding='utf-8')
        try:
            url_all_text = f.read()
            urlAll = url_all_text.split('\n')
            for i in urlAll:
                if i != '':
                    x = i.split(' ')
                    urlName.append(x[0])
                    urlList.append(x[1])
            urldict = dict(zip(urlName, urlList))
        finally:
            f.close()
        return render_template('serviceOne.html', urls=urldict)
    else:
        urlList.clear()
        urlName.clear()
        f = open(urlFileDir, 'r', encoding='utf-8')
        try:
            url_all_text = f.read()
            urlAll = url_all_text.split('\n')
            for i in urlAll:
                if i != '':
                    x = i.split(' ')
                    urlName.append(x[0])
                    urlList.append(x[1])
            urldict = dict(zip(urlName, urlList))
        finally:
            f.close()
        return render_template('serviceOne.html', urls=urldict)


@serviceone.route('/urldel', endpoint='/urldel', methods=['POST'])
@session_zsq
def urldel():
    service = request.form.get('service')
    try:
        with open(urlFileDir, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i in lines:
                bools = service in i.replace('\n', ' ')
                if bools == True:
                    delIndex = lines.index(i)
                    del lines[int(delIndex)]
                    break
            f.close()
        with open(urlFileDir, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            f.close()
        return jsonify({"code": 200, "message": "删除成功!"})
    except Exception:
        print(traceback.format_exc())
        return jsonify({"code": 500, "message": "error,删除失败!"})
