$(function () {
    $("#tj").click(function () {
        var input_date = $("#date").val();
        var input_info = $("#info").val();
        var input_eventName = $("#eventName").val();
        if (input_date == '' || input_info == '' || input_eventName == '') {
            alert('字段不允许为空！')
        } else (
            $.post({
                "url": "/event_w_database",
                "data": {
                    "date": input_date,
                    "info": input_info,
                    "eventName": input_eventName
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
            alert('ID不允许为空!!!');
        } else {
            $.post({
                "url": "/deletes",
                "data": {
                    "delete_id": dataID,
                    "table_type": "event_id",
                    "table": "event"
                },
                "success": function (data) {
                    if (data["code"] == 200) {
                        window.location = "/event_zs";
                        alert("status: " + data["code"] + "\n" + "message: " + data["message"]);
                    } else {
                        window.location = "/event_zs";
                        alert("status: " + data["code"] + "\n" + "message: " + data["message"]);
                    }
                },
                "fail": function (error) {
                    console.log(error);
                }
            });

        }

    });
});