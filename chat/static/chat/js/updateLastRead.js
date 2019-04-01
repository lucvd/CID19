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

    var scrolldiv = $("#chat-scroll-div").get(0);
    scrolldiv.scrollTop = scrolldiv.scrollHeight;

    $('#id_message').focusin(function () {
        var participationID = $("#activeConversation").attr('data-participationID');
        $.ajax({
            type: 'POST',
            url: '/chat/ajax/updateLastRead/',
            contentType: 'application/json',
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            data: JSON.stringify({
                'participationID': participationID
            }),
            success: function (result) {
                var totalUnread = result['total_unread'];
                if (totalUnread === 0) {
                    $("#unread-message-indicator").hide();
                } else {
                    $("#unread-message-indicator").text(totalUnread);
                }
                $("#conversationCard"+participationID).hide();
            }
        });
    });

});
