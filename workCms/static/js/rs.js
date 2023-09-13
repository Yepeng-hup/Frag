function redis_all(obj_array, s) {
        if (s == "str"){
            url_index = "/redisx/str";
        }else if (s == "list"){
            url_index = "/redisx/list";
        }else if (s == "hash"){
            url_index = "/redisx/hash";
        }else if (s == "set"){
            url_index = "/redisx/set";
        }else {
            url_index = "/redisx/zset";
        }

        $.post({
            "url": url_index,
            "data": {
                "k": obj_array[0],
                "v": obj_array[1],
                "k_time": obj_array[2],
                "cmd": obj_array[3],
                "index_s": obj_array[4],
                "index_end": obj_array[5],
            },
            "success": function (data) {
                if (data["code"] == 200) {
                    window.location = "/redisx/index";
                    alert("status: " + data["code"] + "\n" + "message: " + data["message"]);
                } else {
                    window.location = "/redisx/index";
                    alert("status: " + data["code"] + "\n" + "message: " + data["message"]);
                }
                console.log(data);
            },
            "fail": function (error) {
                console.log(error);
            }
        });
}


function fs(cmd) {
    // var command = document.querySelector('td').textContent;
    //var command=document.getElementById('del').textContent;
    let cmdArray = new Array();
    switch (cmd) {
        case "set":
            let set_key = $("#set_k").val();
            let set_value = $("#set_v").val();
            if (set_key == ''||set_value == ''){
                alert('字段不允许为空!!!')
            }else {
                cmdArray[0] = set_key;
                cmdArray[1] = set_value;
                cmdArray[3] = cmd;
                redis_all(cmdArray,"str")
            }
            break;
        case "del":
            let del_key = $("#del_k").val();
            if (del_key == ''){
                alert('字段不允许为空!!!')
            }else {
                cmdArray[0] = del_key;
                cmdArray[3] = cmd;
                redis_all(cmdArray,"str")
            }
            break;
        case "append":
            let append_key = $("#append_k").val();
            let append_value = $("#append_v").val();
            if (append_key == ''||append_value == ''){
                alert('字段不允许为空!!!')
            }else {
                cmdArray[0] = append_key;
                cmdArray[1] = append_value;
                cmdArray[3] = cmd;
                redis_all(cmdArray,"str")
            }
            break;
        case "get":
            let get_key = $("#get_k").val();
            if (get_key == ''){
                alert('字段不允许为空!!!')
            }else {
                cmdArray[0] = get_key;
                cmdArray[3] = cmd;
                redis_all(cmdArray,"str")
            }
            break;
        case "strlen":
            let strlen_key = $("#strlen_k").val();
            if (strlen_key == ''){
                alert('字段不允许为空!!!')
            }else {
                cmdArray[0] = strlen_key;
                cmdArray[3] = cmd;
                redis_all(cmdArray,"str")
            }
            break;
        case "setex":
            let setex_key = $("#setex_k").val();
            let setex_value = $("#setex_v").val();
            let setex_keyTime = $("#k_time").val();
            if (setex_key == ''||setex_value == ''||setex_keyTime == ''){
                alert('字段不允许为空!!!')
            }else {
                cmdArray[0] = setex_key;
                cmdArray[1] = setex_value;
                cmdArray[2] = setex_keyTime;
                cmdArray[3] = cmd;
                redis_all(cmdArray,"str")
            }
            break;
        default:
            window.location = '/redisx/index';
            alert("value is nil!");
            return
    }
}

function fList(cmd) {
    let cmdArray = new Array();
    switch (cmd) {
        case "lpush":
            let lpush_key = $("#lpush_k").val();
            let lpush_value = $("#lpush_v").val();
            if (lpush_key == '' || lpush_value == '') {
                alert('字段不允许为空!!!')
            } else {
                cmdArray[0] = lpush_key;
                cmdArray[1] = lpush_value;
                cmdArray[3] = cmd;
                redis_all(cmdArray, "list")
            }
            break;
        case "lindex":
            let lindex_key = $("#lindex_k").val();
            let lindex_i = $("#lindex_i").val();
            if (lindex_key == ''||lindex_i == '') {
                alert('字段不允许为空!!!')
            } else {
                cmdArray[0] = lindex_key;
                cmdArray[4] = lindex_i;
                cmdArray[3] = cmd;
                redis_all(cmdArray, "list")
            }
            break;
        case "lpop":
            let lpop_key = $("#lpop_k").val();
            if (lpop_key == '') {
                alert('字段不允许为空!!!')
            } else {
                cmdArray[0] = lpop_key;
                cmdArray[3] = cmd;
                redis_all(cmdArray, "list")
            }
            break;
        case "lrange":
            let lrange_key = $("#lrange_k").val();
            let lrange_i_s = $("#lrange_i_s").val();
            let lrange_i_end = $("#lrange_i_end").val();
            if (lrange_key == '' || lrange_i_s == '' || lrange_i_end == '') {
                alert('字段不允许为空!!!')
            } else {
                cmdArray[0] = lrange_key;
                cmdArray[3] = cmd;
                cmdArray[4] = lrange_i_s;
                cmdArray[5] = lrange_i_end;
                redis_all(cmdArray, "list")
            }
            break;
        default:
            window.location = '/redisx/index';
            alert("value is nil!");
            return
    }
}

