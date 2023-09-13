$(function(){
    $("#usercre").click(function(){
        var user = $("#user").val();
        var passwd = $("#passwd").val();
        var passwd1 = $("#passwd1").val();
        var qx = $("#qx").val();
        if (user == ''|| passwd == ''||passwd1 == ''){
            alert('字段不允许为空!!!');
			return;
        };
        if (user.length > 10){
            alert('用户名过长!');
			return;
        }else if (passwd.length < 8){
            alert('密码不能少于8位!');
			return;
        }else if (passwd != passwd1){
            alert('密码输入不一致!');
			return;
        }else{
                $.post({
                    "url": "/user/usercreate",
                    "data": {
                        "user": user,
                        "passwd": passwd,
                        "authority": qx
                    },
                    "success": function(data){
                        if (data["code"] == 200){
                            //跳转路由
                            window.location = "/user/usercreate";
                            alert("status: "+data["code"] +"\n"+"message: "+data["message"]);
                        }else {
                            window.location = "/user/usercreate";
                            alert("status: "+data["code"]+"\n"+"message: "+data["message"]);
                        }
                    },
                    "fail": function(error){
                        console.log(error);
                    }
                });
        }

    });
});


function deleteCheckbox() {
    var items=document.getElementsByClassName('cb');
    var len=items.length;
    for (var i=len-1; i>=0;i--) {
        var is_checkd = items[i].checked;
        if (is_checkd) {
            var divItems = items[i].parentNode.parentNode;
            var divlr = divItems.innerText
            $.post(
                {
                    "url": "/user/delete",
                    "data": {
                        "name": divlr
                    }
                },

            )
            divItems.parentNode.removeChild(divItems);
        }
    }
}


$(function(){
    $("#pwdupdate").click(function(){
        var user = $("#user").val();
        var passwd = $("#passwd").val();
        var passwd1 = $("#passwd1").val();
        if (user == ''|| passwd == ''||passwd1 == ''){
            alert('字段不允许为空!!!');
            return;

        };
        if (passwd != passwd1){
            alert('密码输入不一致!')
            return;
        }else{
                $.post({
                    "url": "/user/update",
                    "data": {
                        "user": user,
                        "passwd": passwd
                    },
                    "success": function(data){
                        if (data["code"] == 200){

                            window.location = "/user/userlist";
                            alert("status: "+data["code"] +"\n"+"message: "+data["message"]);
                        }else {
                            window.location = "/user/userlist";
                            alert("status: "+data["code"]+"\n"+"message: "+data["message"]);
                        }
                    },
                    "fail": function(error){
                        console.log(error);
                    }
                });
        }

    });
});