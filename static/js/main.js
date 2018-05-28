let countForYobaTitle = 0;
function clickTitleToYobaTitle(e) {
    if (countForYobaTitle === 10) {
        this.innerHTML = "АЯЗ!";
        document.getElementById("t2").innerHTML = "Заебошь короч ахуенный слоган для рестайла.";
        document.getElementById("t3").innerHTML = "А то ты опять будешь бомбить, что я написал какой-то дуратский текст.";
        document.getElementById("t0").classList.add("best-jumbotron-bg");
    } else if (countForYobaTitle > 10) {
        this.innerHTML = "ReSTYLE";
        document.getElementById("t2").innerHTML = "Easy way to customize your web pages";
        document.getElementById("t3").innerHTML = "Change the appearance of your favorite web pages as you need";
        document.getElementById("t0").classList.remove("best-jumbotron-bg");
        countForYobaTitle = 0;
    }
    console.log(10 - countForYobaTitle);
    countForYobaTitle++;
}

document.addEventListener("DOMContentLoaded", function () {
    let t1 = document.getElementById("t1");
    t1.onclick = clickTitleToYobaTitle;
})