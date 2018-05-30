var STYLE_DICTS = []

function createStyleFromLocal(e) {
    let sel_id = this.id
    let selected = document.getElementById("LOCAL-" + sel_id);
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
        style = Object.assign({}, STYLE_DICTS[sel_id]);
        window.postMessage({ msg: 'RESTYLE_UNINSTALL_THEME', id: style.id }, '*');
        setTimeout(function () {
            style.id = json.id;
            window.postMessage({ msg: 'RESTYLE_INSTALL_THEME', theme: style }, '*');
            window.location.href = getHost();
        }, 100);
        return json;
    })
}

function updateStyleFromLocal(e) {
    let sel_id = this.id
    let selected = document.getElementById("LOCAL-" + sel_id);
    let updatable = null;
    for (let i = 0; i < STYLE_DICTS.length; i++) {
        const element = STYLE_DICTS[i];
        if (element.id === Number(sel_id))
            updatable = element
    }
    fetch(getHost() + "/ajax/style/update", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/json',
            'charset': 'utf-8',
        },
        body: JSON.stringify({
            id: sel_id,
            name: selected.querySelector(".RE-STYLE-NAME").innerHTML,
            styles: updatable.styles,
        })
    })
    .then(function (json) {
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
    let event = "";
    let updateID = -1;
    let localStyles = null;
    let localStylesCreate = document.getElementById("local-styles-create");
    let localStylesUpdate = document.getElementById("local-styles-update");
    if (localStylesCreate !== null){
        localStyles = localStylesCreate;
        event = "create";
    }
    if (localStylesUpdate !== null) {
        localStyles = localStylesUpdate;
        event = "update";
        updateID = Number(document.getElementsByTagName("update-id")[0].id)
    }
    localStyles.innerHTML = "";
    for (let i = 0; i < styles.length; i++) {
        const element = styles[i];
        if (event === "create" && element.id > 0)
            continue;
        if (event === "update" && element.id !== updateID)
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
            if (event === "create") {
                e.innerHTML = htmlImportStyle.format(i, element.name, json.site);
                e.querySelector(".RE-STYLE-LOCAL").addEventListener('click', createStyleFromLocal);
            }
            if (event === "update") {
                e.innerHTML = htmlImportStyle.format(styles[i].id, element.name, json.site);
                e.querySelector(".RE-STYLE-LOCAL").addEventListener('click', updateStyleFromLocal);
            }
            localStyles.appendChild(e);
        })
    }
}

document.addEventListener("DOMContentLoaded", function (e) {
    let elem = null;
    let create = document.getElementById("nav-style-create-tab");
    let update = document.getElementById("nav-style-update-tab");
    if (create !== null) {
        elem = create;
    }
    if (update !== null) {
        elem = update;
    }
    elem.addEventListener('click', function (e) {
        window.postMessage({ msg: 'RESTYLE_GET_INSALLED_THEMES' }, '*');
    })
})