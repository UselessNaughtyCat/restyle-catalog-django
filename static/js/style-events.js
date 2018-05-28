function subscriptionEvent() {
    let elem = this
    elem.disabled = true
    fetch(getHost() + "/ajax/subscription", {
        method: "POST",
        credentials: "same-origin", // !!! Fetch does not use cookie by default.
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/json',
            'charset': 'utf-8',
        },
        body: JSON.stringify({
            style_id: elem.id.match(/btnSub-(\d+)/)[1],
        })
    })
    .then(responseJSON)
    .then(function (json) {
        console.log("subscribed: " + json.subscribed)
        elem.innerHTML = json.subscribed ? "Uninstall" : "Install"
        document.getElementById("subs-count").innerHTML = json.subs_count
    })
    elem.disabled = false
}

function ratingEvent() {
    let elem = this
    fetch(getHost() + "/ajax/rating", {
        method: "POST",
        credentials: "same-origin", // !!! Fetch does not use cookie by default.
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/json',
            'charset': 'utf-8',
        },
        body: JSON.stringify({
            style_id: elem.id.match(/rate-(\d+)-([1-5])/)[1],
            rate: Number(elem.id.match(/rate-(\d+)-([1-5])/)[2]),
        })
    })
    .then(responseJSON)
    .then(function (json) {
        console.log("new average_rating: " + json.average_rating)
        document.getElementById("average-rating").innerHTML = json.average_rating
    })
}

document.addEventListener("DOMContentLoaded", function (e) {
    let elemSubs = document.querySelector('[id^="btnSub-"]')
    if (elemSubs !== null) {
        elemSubs.addEventListener("click", subscriptionEvent)
    }

    let elemsRate = document.getElementById("star-rating").querySelectorAll(".star");
    elemsRate.forEach(elemRate => {
        elemRate.addEventListener("click", ratingEvent)
    });
})