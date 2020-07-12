function checkregister() {
	var s = document.cookie.split(";");
	for(var i=0;i<s.length;i++ )
	{
		if(s[i] == " yes")
		{
			document.getElementById("yincang").innerHTML = "隐藏内容！！！";
		}
	}
}
