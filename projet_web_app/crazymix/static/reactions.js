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
            img = document.getElementById(data['reaction'].toLowerCase() + '/' + data['extrait_id'])
            img.style.width = '55px'
            img.name = 'active' + data['extrait_id']
            // img.setAttribute('width', '55px')
            //eventuellement aller chercher la réaction dans la liste de toutes les réactions et la changer
            // src = img.src
            // deconstruite = src.split('/')
            // srcACompleter = ""
            // for (let i = 0; i < deconstruite.length - 1; i++) {
            //     srcACompleter = srcACompleter.concat(deconstruite[i] + '/')
            // }
            // srcComplete = srcACompleter + data['reaction'].toLowerCase()
            // img.setAttribute('src', srcComplete)
        }
    })
}

async function modifierReaction(event) {

    extrait_id = event.target.id
    extrait_idContent = extrait_id.split('/')
    id = extrait_idContent[1]
    name = 'active' + id
    img = document.getElementsByName(name)
    if (img.length == 1) {
        // img[0].setAttribute('width', '43px')
        img[0].style.width = '43px';
            img[0].name = ""
        // img.setAttribute('border-radius', '20px')
    }


    reactionSrc = event.target.src
    reactionContent = reactionSrc.split('/')
    reactionImg = reactionContent[reactionContent.length - 1]
    reactionImgContent = reactionImg.split('.')
    reaction = reactionImgContent[0].toUpperCase()
    let body = JSON.stringify({'extrait_id': id, 'reaction': reaction})
    let data = await makeRequest('/crazymix/modifierReaction/', 'post', body)
    if (data) {

    }
}
