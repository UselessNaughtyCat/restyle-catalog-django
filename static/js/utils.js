function getHost() {
    let url = window.location.href;
    let arr = url.split("/");
    return arr[0] + "//" + arr[2];
}

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

function responseJSON(response) {
    return response.json()
}

window.addEventListener('message', e => {
    if (e.data.msg === 'RESTYLE_THEMES') {
        console.log(e.data.themes);
    }
});