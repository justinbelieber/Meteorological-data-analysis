function checkname()
{
	var nameEl = document.getElementById("username").value;
	var unameEl = document.getElementById("uname");
	var reg=/^[a-zA-Z0-9_]{3,12}$/;
	if(nameEl.length<3||nameEl.length>12)
	{
		unameEl.innerHTML="<font color='crimson'> ✘   用户名长度不能小于3大于12！</font>";
		return false;
	}
	if(reg.test(nameEl) == false)
	{
		unameEl.innerHTML="<font color='crimson'> ✘   用户名只能由数字、字母及_组成！</font>";
		return false;
	}
	unameEl.innerHTML="<font color='mediumseagreen'> ✔ </font>";
	return true;
}
function checkpassword()
{
	var passwordEl = document.getElementById("pass").value;
	var upasswordEl = document.getElementById("unpass");
	if(passwordEl.length<6 || passwordEl.length>18)
	{
		upasswordEl.innerHTML="<font color='crimson'> ✘   密码的长度不能小于6大于18！</font>";
		return false;
	}
	else
	{
		upasswordEl.innerHTML="<font color='mediumseagreen'> ✔  </font>";
		return true;
	} 
	
}
function againpassword()
{
	var passwordEl = document.getElementById("pass").value; 
	var apasswordEl = document.getElementById("upassword").value;
	var checkpass = document.getElementById("unpass2");
	if(passwordEl == ""||apasswordEl != passwordEl)
	{
		checkpass.innerHTML="<font color='crimson'> ✘   两次输入的密码不一致！</font>";
		return false;
	}
	else
	{
		checkpass.innerHTML="<font color='mediumseagreen'> ✔ </font>";
		return true;
	}
}

function allcheck()
{
	alert("完成注册，自动跳转到登录界面。");
	return checkname()&&checkpassword()&&againpassword()&&putcookie();
}
function changeBgColor(btn) {
	var btn = document.getElementById(btn);
	btn.style.backgroundColor = "#5B5B5B"
}

function recoverBgColor(btn) {
	var btn = document.getElementById(btn);
	btn.style.backgroundColor = "#080808"
}

function putcookie() { //写入文件
	var name = document.getElementById("username").value;
	var pass = document.getElementById("pass").value;
	var Days = 30;
	var exp = new Date(); 
	exp.setTime(exp.getTime() + Days*24*60*60*1000);
	document.cookie = name + " = " +pass+ ";expires=" + exp.toGMTString();
}

function getcookie() {  //读取文件
	var name = document.getElementById("username2").value;
	var pass = document.getElementById("pass2").value;
	var name_cookie, code_cookie, cookie;
	var cookie_arr = document.cookie.split(";");
	if(name=="admin"&&pass=="123456"){
		window.location.href="admin.html"
	}
	for(i=0; i<cookie_arr.length; i++) {
		cookie = cookie_arr[i].split("=");
		if(cookie[0]==name&&cookie[1]==pass) {
			
			
				alert(cookie[0]+"    "+cookie[1]);
				var virualcookie = cookie_arr[i+1].split("=");
				code_cookie = virualcookie[1];
				alert("登录成功");
				document.cookie="denglu=" + denglu;	
				window.location.replace("main.html");
				return true;
			
			
			}			
	else
			{	
				alert("账号或密码有误！") ;
				return false;
			}
}
}	


var code ;
//产生验证码  

window.onload = function createCode(){  
     code = "";   
     var codeLength = 4;
     var checkCode = document.getElementById("code");   
     var random = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',  
     'S','T','U','V','W','X','Y','Z');
     for(var i = 0; i < codeLength; i++) {
        var index = Math.floor(Math.random()*36);
        code += random[index];
    }  
    checkCode.value = code;
}  
//校验验证码
function validate(){
    var inputCode = document.getElementById("input").value.toUpperCase();
    var vali = document.getElementById("validate");
    if(inputCode == code)
    {
    	vali.innerHTML="<font color='mediumseagreen'>✔</font>";
    }
	else if(inputCode != code ) {
    	vali.innerHTML="<font color='crimson'>验证码输入错误！</font>";
        createCode();//刷新验证码
        document.getElementById("input").value = "";
    }
    else {
		vali.innerHTML="<font color='crimson'>验证码输入正确！</font>";
    }
}