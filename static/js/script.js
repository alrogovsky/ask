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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).ready(function() {
    $('.a_like').click(function () {
        var self = this;
        $.post("/rate/", {
            type: 'answer',
            action: 'like',
            id: $(self).attr('aid')
        }, function (data) {
            if (data.result == 'exists') {
                alert("Вы уже голосовали за этот ответ!");
            }
            if (data.result == 'done') {
                $(self).parent().find("button:disabled").text(data.new);
            }
        });
    });
});

$(document).ready(function() {
    $('.a_dislike').click(function () {
        var self = this;
        $.post("/rate/", {
            type: 'answer',
            action: 'dislike',
            id: $(self).attr('aid')
        }, function (data) {
            if (data.result == 'exists') {
                alert("Вы уже голосовали за этот ответ!");
            }
            if (data.result == 'done') {
                $(self).parent().find("button:disabled").text(data.new);
            }
        });
    });
});

$(document).ready(function() {
    $('.q_dislike').click(function () {
        var self = this;
        $.post("/rate/", {
            type: 'question',
            action: 'dislike',
            id: $(self).attr('qid')
        }, function (data) {
            if (data.result == 'exists') {
                alert("Вы уже голосовали за этот вопрос!");
            }
            if (data.result == 'done') {
                $(self).parent().find("button:disabled").text(data.new);
            }
        });
    });

    $('.q_like').click(function () {
        var self = this;
        $.post("/rate/", {
            type: 'question',
            action: 'like',
            id: $(self).attr('qid')
        }, function (data) {
            if (data.result == 'exists') {
                alert("Вы уже голосовали за этот вопрос!");
            }
            if (data.result == 'done') {
                $(self).parent().find("button:disabled").text(data.new);
            }
        });
    });
});
