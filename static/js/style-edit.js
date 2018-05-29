var STYLE_DICTS = []

function createStyleFromLocal(e) {
    let sel_id = this.id
    let selected = document.getElementById("LOCAL-" + sel_id);
    console.log(STYLE_DICTS)
    fetch(getHost() + "/ajax/style/add", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/json',
            'charset': 'utf-8',
        },
        body: JSON.stringify({
            name: selected.querySelector(".RE-STYLE-NAME").innerHTML,
            site: selected.querySelector(".RE-STYLE-SITE").innerHTML,
            styles: STYLE_DICTS[sel_id].styles,
        })
    })
    .then(responseJSON)
    .then(function (json) {
        createdLocalStyle = STYLE_DICTS[sel_id];
        window.postMessage({ msg: 'RESTYLE_UNINSTALL_THEME', id: createdLocalStyle.id }, '*')
        return json;
    })
    .then(function (json) {
        createdLocalStyle2 = STYLE_DICTS[sel_id];
        createdLocalStyle2.id = json.id;
        window.postMessage({ msg: 'RESTYLE_INSTALL_THEME', theme: createdLocalStyle2 }, '*')
        window.location.href = getHost();
    })
}

function appendLocalStyles(styles) {
    STYLE_DICTS = styles
    let htmlImportStyle = `
    <div class="card bg-card" id="LOCAL-{0}">
        <a class="card-header bg-card-header font-weight-bold RE-STYLE-NAME">{1}</a>
        <img class="card-img rounded-0" src="/media/images/style/not-exist.jpg">
        <ul class="list-group list-group-flush">
            <li class="list-group-item bg-card item-small text-muted"><b>Site:</b> <a class="RE-STYLE-SITE">{2}</a></li>
        </ul>
        <div class="card-body py-2">
            <div class="btn btn-outline-primary-2 w-100 btn-sm RE-STYLE-LOCAL" id="{0}">Upload</div>
        </div>
    </div>`;
    let localStyles = document.getElementById("local-styles");
    localStyles.innerHTML = "";
    for (let i = 0; i < styles.length; i++) {
        const element = styles[i];
        if (element.id > 0)
            continue;
        fetch(getHost() + "/ajax/site/get", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                'Content-Type': 'application/json',
                'charset': 'utf-8',
            },
            body: JSON.stringify({
                urls: element.domains,
            })
        })
        .then(responseJSON)
        .then(function (json) {
            let e = document.createElement("div");
            e.classList.add("col-sm-12", "col-md-6", "col-lg-4", "col-xl-3", "my-3");
            e.innerHTML = htmlImportStyle.format(i, element.name, json.site);
            e.querySelector(".RE-STYLE-LOCAL").addEventListener('click', createStyleFromLocal);
            localStyles.appendChild(e);
        })
    }
}

document.addEventListener("DOMContentLoaded", function (e) {
    document.getElementById("nav-style-source-tab").addEventListener('click', function (e) {
        window.postMessage({ msg: 'RESTYLE_GET_INSALLED_THEMES' }, '*');
    })
})