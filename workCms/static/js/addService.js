$(function () {
    $("#del").click(function () {
        var service = $("#service").val();
        if (service == '') {
            window.location = '/serviceone'
            alert('服务名不允许为空!!!');

        } else {
            $.post({
                "url": "/urldel",
                "data": {
                    "service": service
                },
                "success": function (data) {
                    if (data["code"] == 200) {
                        window.location = "/serviceone";
                        alert("status: " + data["code"] + "\n" + "message: " + data["message"]);
                    } else {
                        window.location = "/serviceone";
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