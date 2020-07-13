        //表格添加行
	function AddRow(table,name) {
	    var lastRow = table.rows[table.rows.length - 1];
	    var newRow = lastRow.cloneNode(true);
	    var length = table.rows.length;
	    table.tBodies[0].appendChild(newRow);
	    newRow.cells[0].innerHTML = "<input type=\"checkbox\" name=\"checkbox\" value=\"checkbox\">";
	    newRow.cells[0].setAttribute("id","new");
	    newRow.cells[1].innerHTML = name
		newRow.cells[2].innerHTML = "<input type=\"checkbox\" name=\"checkbox\" value=\"checkbox\">";
		newRow.cells[3].innerHTML = "<input type=\"checkbox\" name=\"checkbox\" value=\"checkbox\">";
		newRow.cells[4].innerHTML = "<input type=\"checkbox\" name=\"checkbox\" value=\"checkbox\">";
		newRow.cells[5].innerHTML = "<input type=\"checkbox\" name=\"checkbox\" value=\"checkbox\">";
		console.log("************************************")
            //设置表格行可编辑
	    //SetRowCanEdit(newRow);
	    return newRow;

	}

	function myadd(table) {
		AddRow(document.getElementById('filedTable'),"管理部门")
		AddRow(document.getElementById('filedTable'),"审核部门")
        AddRow(document.getElementById('filedTable'),"普通用户")


	}

     function formSubmit() {
        var obj = document.getElementsByName("checkbox");
        var check_arr = [];
        for (var i = 0; i < obj.length; i++) {
            if (obj[i].checked)
                check_arr.push(1);
            else
                check_arr.push(0);

        }

        namespace = '/test';
	    var socket = io.connect("http://"+document.domain+":"+ location.port +namespace);
	    socket.emit("allrights",check_arr);

    }

    function fresh() {
        message = 1
        namespace = '/test';
	    var socket = io.connect("http://"+document.domain+":"+ location.port +namespace);
	    socket.emit("to_check",message);

    }

    $(document).ready(function () {
	namespace = '/test';
	var socket = io.connect("http://"+document.domain+":"+ location.port +namespace);

	socket.on('to_check', function(msg){
	var obj = document.getElementsByName("checkbox");

        document.getElementsByName("checkbox")[2].checked = Boolean(msg[1])
        document.getElementsByName("checkbox")[3].checked = Boolean(msg[2])
        document.getElementsByName("checkbox")[4].checked = Boolean(msg[3])
        document.getElementsByName("checkbox")[5].checked = Boolean(msg[4])
        document.getElementsByName("checkbox")[7].checked = Boolean(msg[6])
        document.getElementsByName("checkbox")[8].checked = Boolean(msg[7])
        document.getElementsByName("checkbox")[9].checked = Boolean(msg[8])
        document.getElementsByName("checkbox")[10].checked = Boolean(msg[9])
        document.getElementsByName("checkbox")[12].checked = Boolean(msg[11])
        document.getElementsByName("checkbox")[13].checked = Boolean(msg[12])
        document.getElementsByName("checkbox")[14].checked = Boolean(msg[13])
        document.getElementsByName("checkbox")[15].checked = Boolean(msg[14])





        });
	});




        //设置表格行可编辑
    function SetRowCanEdit(row) {
        for (var i = 0; i < row.cells.length; i++) {
            //当前单元格指定了编辑类型，允许编辑
            var editType = row.cells[i].getAttribute("EditType"); if (!editType) {
            //当前单元格没有指定，查看当前列是否指定
            editType = row.parentNode.rows[0].cells[i].getAttribute("EditType"); }
            if (editType) {
                row.cells[i].onclick = function() { EditCell(this); }
             }
        }
    }
    //设置指定单元格可编辑
    function EditCell(element, editType) {
        var editType = element.getAttribute("EditType");
        if (!editType) {
            //如果当前单元格没有指定，则查看当前列是否指定
            editType = element.parentNode.parentNode.rows[0].cells[element.cellIndex].getAttribute("EditType");
        }
        switch (editType) {
            case "TextBox":
                CreateTextBox(element, element.innerHTML);
                break;
            case "DropDownList":
                CreateDropDownList(element);
                break; default: break;
         }
     }
    //为单元格创建可编辑输入框
    function CreateTextBox(element, value) {
        //编辑状态，true为编辑状态
        var editState = element.getAttribute("EditState");
        if (editState != "true") {
            //创建文本框
            var textBox = document.createElement("INPUT");
            textBox.style="width:100%";
            textBox.type = "text";
            textBox.className = "EditCell_TextBox";
            //设置当前值
            if (!value) {
                value = element.getAttribute("Value");
            } textBox.value = value;
            //设置失去焦点事件
            textBox.onblur = function() {CancelEditCell(this.parentNode, this.value); }
            //向当前单元格添加文本框
            ClearChild(element);
            element.appendChild(textBox);
            textBox.focus(); textBox.select();
            //设置编辑状态
            element.setAttribute("EditState", "true");
            element.parentNode.parentNode.setAttribute("CurrentRow", element.parentNode.rowIndex); }
    }
    //为单元格创建选择框
    function CreateDropDownList(element, value) {
        //编辑状态， true为编辑状态
        var editState = element.getAttribute("EditState");
        if (editState != "true") {
            //创建下拉框
            var downList = document.createElement("Select");
            downList.style="width:100%";
            downList.className = "EditCell_DropDownList";
            //添加列表项
            var items = element.getAttribute("DataItems");
            if (!items) {
                items = element.parentNode.parentNode.rows[0].cells[element.cellIndex].getAttribute("DataItems");
            }
            if (items) {
                items = eval("[" + items + "]");
                for (var i = 0; i < items.length; i++) {
                    var oOption = document.createElement("OPTION");
                    oOption.text = items[i].text;
                    oOption.value = items[i].value; downList.options.add(oOption);
                }
            }
            //设置列表当前值
            if (!value) {
                value = element.getAttribute("Value");
            } downList.value = value;
            //设置下拉框失去焦点事件
            downList.onblur = function() {
                CancelEditCell(this.parentNode, this.value, this.options[this.selectedIndex].text);
            }
            //向当前单元格添加下拉框
            ClearChild(element);
            element.appendChild(downList);
            downList.focus();
            //设置编辑状态
            element.setAttribute("EditState", "true");
            element.parentNode.parentNode.setAttribute("LastEditRow", element.parentNode.rowIndex);
        }
    }
    //取消单元格编辑状态
    function CancelEditCell(element, value, text) {
        element.setAttribute("Value", value);
        if (text) {
            element.innerHTML = text;
        } else {
            element.innerHTML = value;
        } element.setAttribute("EditState", "false");
    }
    //清空指定对象的所有字节点
    function ClearChild(element) {
        element.innerHTML = "";
    }
    //删除行
    function DeleteRow(table) {
        for (var i = table.rows.length - 1; i > 0; i--) {
            var chkOrder = table.rows[i].cells[0].firstChild;
            if (chkOrder) {
                if (chkOrder.type = "CHECKBOX") {
                    if (chkOrder.checked) {
                        table.deleteRow(i);
                    }
                }
            }
        }
    }
    //提取表格所有值,JSON格式，可以将该值赋予一个隐藏的input标签，提交表单至后台进行处理
    function GetTableData() {
        var table = document.getElementById("filedTable");
        var Obj = {Mark:"",Columnname:"",Datatype:"",Length:"",Primarykey:"",Isnull:"",Comments:""};
        var datamodeldata = JSON.parse("{\"data\":[]}");
        for(var i=1;i<table.rows.length;i++){
            var Obj = new Object();
            Obj.Mark = table.rows[i].cells[0].id;
            Obj.Columnname = table.rows[i].cells[1].innerHTML;
            Obj.Datatype = table.rows[i].cells[2].innerHTML;
            Obj.Length = table.rows[i].cells[3].innerHTML;
            Obj.Primarykey = table.rows[i].cells[4].innerHTML;
            Obj.Isnull = table.rows[i].cells[5].innerHTML;
            Obj.Comments = table.rows[i].cells[6].innerHTML;
            datamodeldata.data.push(Obj);
        }
        return JSON.stringify(datamodeldata).toString();
    }
    //本表格数据为数据库字段数据
    //判断字段名称是否重复
    function ColumnnameDuplicate(){
        var table = document.getElementById("filedTable");
        var array = new Array();
        var b = false;
        for(var i=1;i<table.rows.length;i++){
            array.push(table.rows[i].cells[1].innerHTML);
        }
        var nary=array.sort();
        for(var i=0;i<array.length;i++){
            if (nary[i]==nary[i+1]){
                b = true;
            }
        }
        return b;
    }
    //提交表格时，判断是否存在数据行
    function TableRows(){
        var table = document.getElementById("filedTable");
        var length = table.rows.length;
        var b = false;
        if(length>=2){
            b=true;
        }
        return b;
    }
    //判断字段名称是否为空
    function ColumunameIsnull(){
        var table = document.getElementById("filedTable");
        var b = false;
        for(var i=1;i<table.rows.length;i++){
            if(table.rows[i].cells[1].innerHTML==""){
                b = true;
            }
        }
        return b;
    }
