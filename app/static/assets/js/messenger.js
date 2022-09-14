

    // Msg JS
    document.addEventListener("DOMContentLoaded", function() {
        get_message($('.receiver_id').val())    
        
    });

    function updateScroll(){
        var element = document.getElementById("scroll");
        element.scrollTop = element.scrollHeight;
    }

    setInterval(updateScroll, 1000);
    setInterval(get_message($('.receiver_id').val()), 15000);

    function openMsg() {
        $(".contact-container1").show();
        $(".contact-container2").hide();
    }

    function closeMsg() {
        $(".contact-container1").hide();
        $(".contact-container2").show();
    }

    function select_chat(receiver_id){
        $('.receiver_id').val(receiver_id);
        openMsg()
        get_message(receiver_id)

    }

    function sendfile(elem){
        var size_max = 5 * 1024 * 1024;
		var file_size = `${elem.files[0].size}`;
        var receiver_id = $('.receiver_id').val();
        var object = $('#msgFile')[0].files[0];
        $('#msgFile').val('');

        if (file_size > size_max){
            $('#file_input').css({"border-color": "#ffdddd"});
        }else if(receiver_id==''){
            closeMsg()        
        }else{
            send(object, receiver_id, true )
        }          
	}

    function sendtext(){
        var text = $('#msgText').val();
        $('#msgText').val('');
        var receiver_id = $('.receiver_id').val();

        if (text == ''){
            $('#text_input').css({"border-color": "#ffdddd"});
        }else if(receiver_id==''){
            closeMsg()
        }else{
            send(text, receiver_id, false )
        }          
	}

    async function send(object, receiver_id, file_statut) {
        var url = $("#msgForm").attr('action');
        var message = new FormData()
        if(file_statut==true){
            message.append('msg_file', object)
        }else{
            message.append('msg_text', object)
        }
        message.append('receiver_id', receiver_id)
    	message.append('file_statut', file_statut)
            
        await fetch(url, {
            method: "POST", 
            body: message
        });
        get_message(receiver_id)
        
    }
        
    function get_message(receiver_id) {
		var url = $(".get_message_url").attr('href');
    		$.post(url, { receiver_id: receiver_id }, function(data, status) { 
                
                var chats_html=''
                var i
                for (i = 0; i < data['chats'].length; i++) {
                    var online
                    if(data["chats"][i]["author"]["id"]==data["user"]["id"]){

                        if(data["chats"][i]["receiver"]["is_active"]=="True"){
                            online = '<small class="fa fa-circle text-success float-right mt-1"></small>';
                        }else{
                            online = '<small class="fa fa-circle text-muted float-right mt-1"></small>';
                        }

                        chats_html = chats_html + '<p class="bg-light p-1 m-1" type="button" style="border-radius: 4px;"'+
                            'onclick="select_chat('+data["chats"][i]["receiver"]["id"]+')">'+data["chats"][i]["receiver"]["username"]+online+'</p>';
                    }else{
                        if(data["chats"][i]["author"]["is_active"]=="True"){
                            online = '<small class="fa fa-circle text-success float-right mt-1"></small>';
                        }else{
                            online = '<small class="fa fa-circle text-muted float-right mt-1"></small>';
                        }
                        chats_html = chats_html + '<p class="bg-light p-1 m-1" type="button" style="border-radius: 4px;"'+
                            'onclick="select_chat('+data["chats"][i]["author"]["id"]+')">'+data["chats"][i]["author"]["username"]+online+'</p>';
                    }
                }
                $(".contact-container2").html(chats_html);

                var messages_html=''
                var i
                for (i = 0; i < data['messages'].length; i++) {
                    var object
                    if(data["messages"][i]["file_statut"]=="True"){
                        object = '<i><a href="'+data["messages"][i]["file"]+'" download="pièce jointe" target="_blank">pièce jointe</a></i>';
                    }else{
                        object = data["messages"][i]["message"];
                    }

                    var sender=''
                    if(data["messages"][i]["author"]["id"]!=data["user"]["id"]){
                        sender = '<b>'+data["messages"][i]["author"]["username"]+':</b>';
                    }
                    messages_html = messages_html + '<p class="bg-light p-1 m-1" type="button" style="border-radius: 4px;">'+
                        '<small>'+object+' </small><br><small><i>'+sender+''+data["messages"][i]["timestamp"]+'</i></small></p>';
                }
                $(".contact-container1").html(messages_html);

            });


    }


    function check_message(){
        let regex_email = new RegExp('[a-z0-9]+@[a-z]+\.[a-z]{2,3}');

        let text = $('#msgText').val();
        // Split string using a whitespace
        let text_array = text.split(' ');
        let counter=[]
        
        text_array.forEach((word) => {          
            
            if (regex_email.test(word) == true){
                $('#msgText').css('border', '2px solid red')
                $('#text_input').attr('onclick', 'return false;')
                counter.append(1)
            } 
            
        });

        if(counter.length==0){
            $('#msgText').css('border', '2px solid dodgerblue')
            $('#text_input').attr('onclick', 'sendtext()')
        } else{
            counter=[]
        }

        let result1 = text.replace(/^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/, '')
        let result2 = result1.replace(/^\(?([0-9]{2})\)?[-. ]?([0-9]{2})[-. ]?([0-9]{2})[-. ]?([0-9]{2})[-. ]?([0-9]{2})$/, '')
        let result3 = result2.replace(/([0-9]{10})/, '')
        let result4 = result3.replace(/([0-9]{9})/, '')
        let result5 = result4.replace(/([0-9]{2})?[-. ]?([0-9]{2})[-. ]?([0-9]{2})[-. ]?([0-9]{2})[-. ]?([0-9]{2})/, '')

        $('#msgText').val(result5)
    }