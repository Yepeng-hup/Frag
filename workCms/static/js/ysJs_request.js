var xmlhttp;
//创建xmlhttprequest对象
function createXMLHttpRequest(){
  xmlhttp=new XMLHttpRequest();  //这里要判断IE的写法
}
function startRequest(name) {
  createXMLHttpRequest();
  xmlhttp.open("POST","/test",false);  //true:异步，false:同步
  xmlhttp.setRequestHeader("Content-Type","application/json")
  xmlhttp.onreadystatechange=handleStateChange;
  // console.log(name)
  xmlhttp.send(JSON.stringify(name));
}
function handleStateChange() {
  if(xmlhttp.readyState==4 && xmlhttp.status==200){
      var txt=xmlhttp.responseText;
      if(txt !=null && txt !=""){
        console.log(txt);
      }
  }
}
