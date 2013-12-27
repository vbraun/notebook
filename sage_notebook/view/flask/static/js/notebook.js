$(document).ready(function(){                                            
    $('form').submit(function(event){                                    
        ws.send($('#input').val())                                        
        return false;                                                    
    });                                                                  
    if ("WebSocket" in window) {                                         
        ws = new WebSocket("ws://" + document.domain + ":5000/notebook/ws");                
        ws.onmessage = function (msg) {                                  
            $("#output").append("<div>"+msg.data+"</div>")                      
        };                                      
    } else {                                                             
        alert("WebSocket not supported");                                
    }                                                                    
});                                                                      
