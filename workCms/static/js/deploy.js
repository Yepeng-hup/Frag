$(function () {
    $("#tj").click(function (event) {
        var input_date = $("#date").val();
        var input_time = $("#time").val();
        var input_info = $("#info").val();
        var input_deployName = $("#deployName").val();
        if (input_date == '' || input_time == '' || input_info == '' || input_deployName == '') {
            alert('字段不允许为空！')
        } else (
            $.post({
                "url": "/deploy_w_database",
                "data": {
                    "date": input_date,
                    "time": input_time,
                    "info": input_info,
                    "deployName": input_deployName
                },

            }),

                alert('数据提交成功！')

        );

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
                    "table_type": "maintain_id",
                    "table": "maintain"
                },
                "success": function (data) {
                    if (data["code"] == 200) {
                        window.location = "/deploy_zs";
                        alert("status: " + data["code"] + "\n" + "message: " + data["message"]);
                    } else {
                        window.location = "/deploy_zs";
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
