$(document).ready(function () {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');



    $.ajax({
        type: 'POST',
        url: '/chat/ajax/getNumberOfUnreadChats/',
        contentType: 'application/json',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (result) {
            var unread = result['unread'];
            if (unread !== 0) {
                $("#unread-message-indicator").text(unread);
                $("#unread-message-indicator").removeAttr("hidden");
            }
        },
        error: function (result) {
            alert("Error connecting to the server, please reload");
        }
    });



});
