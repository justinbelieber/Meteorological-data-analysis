function onload() {
    $(document).ready(function() {
        namespace='/test_conn'
        var socket = io.connect('ws://127.0.0.1:11000/test_conn');
        //或者使用 var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

        socket.on('server_response', function(res) {
            var msg = res.data;
            console.log(msg);
            document.getElementById("random").innerHTML = '<p>'+msg+'</p>';
        });

   	});
}

