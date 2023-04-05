let schedulesSelected = []
let premiereEntree=true
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
        if (data['Success']) {
            makeRequest('/crazymix/sessions', 'get')
        } else if (data['valid'] == 'invalid') {
                error = document.getElementById("invalid_username")
            error.innerText = "Nom d'utilisateur disponible"
            error.classList.remove('text-danger')
            error.classList.remove('invisible')
            error.classList.add('text-success')

        } else if (data['valid'] == 'valid') {
         error = document.getElementById("invalid_username")
            error.classList.remove('invisible')
            error.classList.remove('text-success')
            error.classList.add('text-danger')
            error.innerText = "Nom d'utilisateur indisponible"
        }
    })
}

window.addEventListener("load", (event) => {
    input = document.getElementById('id_username')
    if (input) {
        // input.addEventListener('focusout', validerUsername, true)
        input.addEventListener('input', validerUsername, true)
    }
});

async function validerUsername(e) {
    error = document.getElementById("invalid_username")
    if (e.type=='input'){
        input = document.getElementById('id_username')
        let body = JSON.stringify({'username': input.value})
        let data = await makeRequest('/crazymix/valider_username/', 'post', body)
        if (data) {
        }
    }
}
