function subscriptionEvent() {
    let elemSub = document.querySelector('[id^="btnSub-"]')
    elemSub.disabled = true
    fetch(getHost() + "/ajax/subscription", {
        method: "POST",
        credentials: "same-origin", // !!! Fetch does not use cookie by default.
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/json',
            'charset': 'utf-8',
        },
        body: JSON.stringify({
            style_id: elemSub.id.match(/btnSub-(\d+)/)[1],
        })
    })
    .then(responseJSON)
    .then(function (json) {
        let isStyleSubscribed = json['subscribed']
        elemSub.innerHTML = isStyleSubscribed ? "Отписаться" : "Подписаться"
    })
    elemSub.disabled = false
}

document.addEventListener("DOMContentLoaded", function (e) {
    let elemSub = document.querySelector('[id^="btnSub-"]')
    if (elemSub !== null) {
        elemSub.addEventListener("click", subscriptionEvent)
    }
})