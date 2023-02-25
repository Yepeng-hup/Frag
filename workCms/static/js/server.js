$(function () {

    $("#tj").click(function () {
        var input_datetime = $("#datetime").val();
        var input_serverName = $("#serverNameIp").val();
        var input_dataBackup = $("#dataBakup").val();
        var input_serverStatus = $("#serverStatus").val();
        var input_policeNum = $("#policeNum").val();
        var input_policeInfo = $("#policeInfo").val();
        var input_checkName = $("#checkName").val();
        if (input_datetime == '' || input_serverName == '' || input_dataBackup == '' || input_serverStatus == '' || input_policeNum == '' || input_policeInfo == '' || input_checkName == '') {
            alert('字段不允许为空！');
        } else {
            $.post({
                "url": "/server_w_database",
                "data": {
                    "datetime": input_datetime,
                    "serverName": input_serverName,
                    "dataBackup": input_dataBackup,
                    "serverStatus": input_serverStatus,
                    "policeNum": input_policeNum,
                    "policeInfo": input_policeInfo,
                    "checkName": input_checkName
                }
            });
            alert('数据提交成功！');
        }

    });
});


$(function () {
    $("#delete_table").click(function () {
        var dataID = $("#data").val();
        if (dataID == '') {
            alert('ID不允许为空!!!')

        } else {

            $.post({
                "url": "/deletes",
                "data": {
                    "delete_id": dataID,
                    "table_type": "server_id",
                    "table": "server"
                },
                "success": function (data) {
                    if (data["code"] == 200) {
                        window.location = "/server_zs";
                        alert("status: " + data["code"] + "\n" + "message: " + data["message"]);
                    } else {
                        window.location = "/server_zs";
                        alert("status: " + data["code"] + "\n" + "message: " + data["message"]);
                    }
                    console.log(data);
                },
                "fail": function (error) {
                    console.log(error);
                }
            });
        }

    });
});