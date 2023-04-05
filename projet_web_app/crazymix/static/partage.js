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
            if (data['partage'] == 'PUBLIC') {
                srcComplete = srcACompleter + 'community.png'
                texte = "Artistes"
            } else if (data['partage'] == 'COMMUNAUTE') {
                srcComplete = srcACompleter + 'private.png'
                texte = "Privé"
            } else if (data['partage'] == 'PERSONNEL') {
                srcComplete = srcACompleter + 'public.png'
                texte = "Public"
            }
            img.setAttribute('src', srcComplete)
            img.parentElement.parentElement.lastElementChild.innerHTML=texte
        }
    })
}

async function modifierPartage(event) {
    extrait_id = event.target.id
    let body = JSON.stringify({'extrait_id': extrait_id})
    let data = await makeRequest('/crazymix/changerPartage/', 'post', body)
    if (data) {

    }
}
