import requests
import json
import traceback
from flask import Blueprint, jsonify, request, render_template

from workCms.core.auxiliay import session_zsq
from workCms.views.user import file
from workCms.status_restful_api import HttpCode

webhooks = Blueprint("webhooks", __name__)


@webhooks.route("/webhook/index", endpoint="/webhook/index")
@session_zsq
def index_webhook():
    with open(file + "webhook_url.txt", "r", encoding='utf-8') as f:
        t = f.read()
        urlAll = t.split('\n')
    return render_template("hook.html", webhook_url=urlAll)


@webhooks.route("/webhook/send", endpoint="/webhook/send", methods=['POST'])
def send_webhook():
    webhook_url = request.form.get("webhook_url")
    # webhook_data = request.get_json()
    webhook_data = request.form.get("msg")
    if webhook_data == None:
        print("json is None!!!")
    webhook_data = json.loads(webhook_data)
    # response = requests.post(webhook_url, json=webhook_data)
    # return jsonify({'status': response.json()})
    response = requests.post(webhook_url, json=webhook_data)
    # print(response.status_code)
    return jsonify({'status': response.status_code})


@webhooks.route("/webhook/save", endpoint="/webhook/save", methods=['POST'])
@session_zsq
def saveHookUrl():
    url = request.form.get("webhook_url")
    try:
        with open(file + "webhook_url.txt", "a") as f:
            f.write(url + "\n")
        return jsonify({"code": HttpCode.success})
    except:
        print(traceback.format_exc())
        return jsonify({"code": HttpCode.serverError})


@webhooks.route("/webhook/del", endpoint="/webhook/del", methods=['POST'])
@session_zsq
def delWebhook():
    url = request.form.get("webhook_url")
    try:
        with open(file + "webhook_url.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i in lines:
                bools = url in i.replace('\n', ' ')
                if bools == True:
                    delIndex = lines.index(i)
                    del lines[int(delIndex)]
                    break
            f.close()
        with open(file + "webhook_url.txt", 'w', encoding='utf-8') as f:
            f.writelines(lines)
            f.close()
        return jsonify({"code": HttpCode.success})
    except Exception:
        print(traceback.format_exc())
        return jsonify({"code": HttpCode.serverError})


@webhooks.route("/webhook/rel", endpoint="/webhook/rel")
@session_zsq
def relWebhook():
    with open(file + "webhook_url.txt", "r", encoding='utf-8') as f:
        rel = f.read()
    return render_template("cmdRes.html", cmdResInfo=rel)
