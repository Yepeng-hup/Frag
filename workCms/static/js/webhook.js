function hookSend() {
    var webhook_url = document.getElementById('hookUrl').value;
    var jsonData = document.getElementById('jsonData').value;
    if (jsonData == ''){
        alert('字段不允许为空！')
        return
    }
    $.ajax({
        url: "/webhook/send",
        type: "POST",
        data: {
            "webhook_url": webhook_url,
            "msg": jsonData
        },
        success: function(data) {
            if (data.status == 200) {
                alert("webhook发送成功!");
                window.location = '/webhook/index';
            } else {
                alert("webhook发送失败!");
            }
        },
        error: function() {
            alert("webhook请求失败！");
        }
    });
}

function SaveHookUrl() {
    var webhook_url = document.getElementById('url').value;
        if (webhook_url == ''){
        alert('字段不允许为空！')
        return
    }
    $.ajax({
        url: "/webhook/save",
        type: "POST",
        data: {
            "webhook_url": webhook_url,
        },
        success: function(data) {
            if (data.code == 200) {
                window.location = '/webhook/index';
            } else {
                alert("webhook添加失败!");
            }
        },
        error: function() {
            alert("webhook添加请求失败！");
        }
    })
}

function delHookUrl() {
    var webhook_url = document.getElementById('url').value;
        if (webhook_url == ''){
        alert('字段不允许为空！')
        return
    }
    $.ajax({
        url: "/webhook/del",
        type: "POST",
        data: {
            "webhook_url": webhook_url,
        },
        success: function(data) {
            if (data.code == 200) {
                window.location = '/webhook/index';
            } else {
                alert("webhook删除失败!");
            }
        },
        error: function() {
            alert("webhook删除请求失败！");
        }
    })
}
