        //表格添加行    
	function AddRow(table,name,key,level) {
	    var lastRow = table.rows[table.rows.length - 1];
	    var newRow = lastRow.cloneNode(true);  
	    var length = table.rows.length; 
	    table.tBodies[0].appendChild(newRow);
	    newRow.cells[0].innerHTML = "<input type=\"checkbox\" name=\"checkbox\" value=\"checkbox\">"; 
	    newRow.cells[0].setAttribute("id","new");
	    newRow.cells[1].innerHTML = name
	    newRow.cells[2].innerHTML = key
		newRow.cells[2].setAttribute("value","varchar");
		newRow.cells[3].innerHTML = level
            //设置表格行可编辑
	    //SetRowCanEdit(newRow);
	    return newRow;
	
	}
    function fresh() {
        DeleteRow(document.getElementById('filedTable'));
        message = 1
        namespace = '/test';
	    var socket = io.connect("http://"+document.domain+":"+ location.port +namespace);
	    socket.emit("to_fresh",message);

    }

    $(document).ready(function () {
	namespace = '/test';
	var socket = io.connect("http://"+document.domain+":"+ location.port +namespace);

    socket.on('to_fresh', function(msg){
	    console.log(msg);
        var length = msg.length;
        var i = length/3
        for (var j=0;j<i;j++)
        {
            if(msg[3*j+2] == 0)
                AddRow(document.getElementById('filedTable'),msg[3*j+0],msg[3*j+1],'管理部门');
            if(msg[3*j+2] == 1)
                AddRow(document.getElementById('filedTable'),msg[3*j+0],msg[3*j+1],'审核部门');
            if(msg[3*j+2] == 2)
                AddRow(document.getElementById('filedTable'),msg[3*j+0],msg[3*j+1],'普通用户');
        }



        });
	});
    
    function DeleteRow(table) {
        for (var i = table.rows.length - 1; i > 0; i--) {
                table.deleteRow(i);
        }
    }
            
    
    
    