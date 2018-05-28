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

// let countForYobaTitle = 0;
// function clickTitleToYobaTitle(e) {
//     if (countForYobaTitle === 10) {
//         this.innerHTML = "АЯЗ!";
//         document.getElementById("t2").innerHTML = "Заебошь короч ахуенный слоган для рестайла.";
//         document.getElementById("t3").innerHTML = "А то ты опять будешь бомбить, что я написал какой-то дуратский текст.";
//     } else if (countForYobaTitle > 10) {
//         this.innerHTML = "ReSTYLE";
//         document.getElementById("t2").innerHTML = "Easy way to customize your web pages";
//         document.getElementById("t3").innerHTML = "Change the appearance of your favorite web pages as you need";
//         countForYobaTitle = 0;
//     }
//     console.log(10 - countForYobaTitle);
//     countForYobaTitle++;
// }

// document.addEventListener("DOMContentLoaded", function () {
//     let t1 = document.getElementById("t1");
//     t1.onclick = clickTitleToYobaTitle;
// })