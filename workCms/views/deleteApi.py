from flask import Blueprint, jsonify, request
import traceback

from workCms.core.auxiliay import session_zsq
from workCms.databases.mysql_db import conn, cursor
from workCms import status_restful_api

delete = Blueprint('delete', __name__)


def idSort(table, table_id):
    sql01 = """
    SET @i=0;
    """
    sql02 = f"""
    UPDATE `{table}` SET `{table_id}`=(@i:=@i+1);
    """
    sql03 = f"""
    ALTER TABLE `{table}` AUTO_INCREMENT=0;
    """
    sqlList = [sql01, sql02, sql03]
    for i in sqlList:
        cursor.execute(i)


@delete.route('/deletes', endpoint='deletes', methods=['POST'])
@session_zsq
def deletes():
    dataId = request.form.get("delete_id")
    typeTableId = request.form.get("table_type")
    tables = request.form.get("table")
    sql = """
        delete from {table} where {table_id}={id}
    """.format(table=tables, table_id=typeTableId, id=dataId)
    try:
        cursor.execute(sql)
        conn.commit()
        idSort(tables, typeTableId)
        return jsonify({"code": status_restful_api.HttpCode.success, "message": "删除成功!"})
    except:
        traceback.format_exc()
        return jsonify({"code": status_restful_api.HttpCode.serverError, "message": "error,sql执行失败!!!"})
