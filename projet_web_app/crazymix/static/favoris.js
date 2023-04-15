async function makeRequest(url, method, body) {
    let headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }
    if (method == 'post') {
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value
        headers['X-CSRFToken'] = csrf
    }
    fetch(url, {
        method: method,
        // credentials:'same-origin',
        headers: headers,
        body: body
    }).then(response => {
        return response.json()
    }).then(data => {
        data = data;
        if (data['valid'] == 'valid') {
            img = document.getElementById(data['extrait_id'])
            src = img.src
            deconstruite = src.split('/')
            srcACompleter = ""
            for (let i = 0; i < deconstruite.length - 1; i++) {
                srcACompleter = srcACompleter.concat(deconstruite[i] + '/')
            }
            if (data['favoris'] == 'False') {
                srcComplete = srcACompleter + 'favoris.png'
            } else if (data['favoris'] == 'True') {
                srcComplete = srcACompleter + 'ajouter_favoris.png'
            }
            img.setAttribute('src', srcComplete)
        }
    })
}

async function modifierFavoris(event) {
    extrait_id = event.target.id
    favorisSrc=event.target.src
    let favoris='True'
    if(favorisSrc.includes("ajouter")){
        favoris="False"
    }
    let body = JSON.stringify({'extrait_id': extrait_id, 'favoris':favoris})
    let data = await makeRequest('/crazymix/modifierFavoris/', 'post', body)
    if (data) {

    }
}
