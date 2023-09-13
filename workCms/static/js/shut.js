$(function () {

    $("#tj").click(function () {
        var input_date = $("#date").val();
        var input_time = $("#time").val();
        var input_info = $("#info").val();
        var input_hefuName = $("#hefuName").val();
        if (input_date == '' || input_time == '' || input_info == '' || input_hefuName == '') {
            alert('字段不允许为空！')
        } else (
            $.post({
                "url": "/hefu_w_database",
                "data": {
                    "date": input_date,
                    "time": input_time,
                    "info": input_info,
                    "hefuName": input_hefuName
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
                    "table_type": "hefu_id",
                    "table": "hefu"
                },
                "success": function (data) {
                    if (data["code"] == 200) {
                        window.location = '/hefu_zs'
                        alert("status: " + data["code"] + "\n" + "message: " + data["message"]);
                    } else {
                        window.location = '/hefu_zs'
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