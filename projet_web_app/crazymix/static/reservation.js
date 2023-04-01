let schedulesSelected = []

async function makeRequest(url, method, body) {
    let headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }
    if (method == 'post') {
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value
        headers['X-CSRFToken'] = csrf
    }
    // let response = await fetch(url, {
    //     method: method,
    //     headers: headers,
    //     body: body
    // })
    fetch(url, {
        method: method,
        // credentials:'same-origin',
        headers: headers,
        body: body
    }).then(response => {
        // if(response.status==200){
        //         this.completeReservation(response.json());
        //
        // }

        return response.json()
    }).then(data => {
        data = data;
        if(data['Success']){
            makeRequest('/crazymix/sessions', 'get')
        }
    })
}


async function getOtherWeek(direction) {
    inputDirection=document.getElementsByName('direction')
    inputDirection[0].setAttribute('value', direction);

    // dateIndicator=document.getElementsByName('dateIndicator')
    // dateIndicator[0].setAttribute('value', dateIndicator[0].innerText)
    document.getElementById('reservationForm').submit();
}

// async function submitForm(e) {
//     e.preventDefault();
// document.getElementById('reservationForm').submit();
// }
async function bookReservation(e) {
    let body = JSON.stringify({'reservation': e.lastChild.innerText})
    let data = await makeRequest('/crazymix/reservation/new', 'post', body)
    if (data) {
    }
    // let other = await data['Success']
}

async function completeReservation(response) {
    if (response) {
        let redirect = '';
    }
}

async function selectSchedule(e) {
    let selectedSchedule = e
    let scheduleHours = selectedSchedule.children[0].innerHTML.trim().split('-')
    let date = selectedSchedule.children[0].attributes.name.nodeValue

    //si aucune sélection => sélectionne
    if (schedulesSelected.length == 0) {
        selectedSchedule.style.backgroundColor = "blue";
        schedulesSelected.push({'hDebut': scheduleHours[0], 'hFin': scheduleHours[1], 'date': date})
    }
    //si pas la même date que sélections précédentes => sélectionne que la nouvelle
    else if (date != schedulesSelected[0].date) {
        let schedulesWithBG = document.getElementsByName(schedulesSelected[0].date)
        schedulesWithBG.forEach(schedule => {
            schedule.parentElement.style.backgroundColor = ""
        })
        schedulesSelected = []
        selectedSchedule.style.backgroundColor = "blue";
        schedulesSelected.push({'hDebut': scheduleHours[0], 'hFin': scheduleHours[1], 'date': date})
    }
    //si une seule sélection
    else if (schedulesSelected.length == 1) {
        //si même case => désélectionne la journée
        if (schedulesSelected[0].hDebut == scheduleHours[0]) {
            selectedSchedule.style.backgroundColor = ""
            scheduleToRemove = schedulesSelected.findIndex(s => s.date == date)
            schedulesSelected.splice(scheduleToRemove)
        }
        //autrement => sélectionne la plage
        else {
            let schedulesWithBG = document.getElementsByName(schedulesSelected[0].date)

            let fillUp = false
            let additionnalValue = 1
            let hDebut = parseInt(schedulesSelected[0].hDebut.split(':'))
            let hSelected = parseInt(scheduleHours[0].split(':'))
            let index = findHourIndex(selectedSchedule.children[0].innerHTML.trim(), schedulesWithBG)
            let i = index
            if (hDebut < hSelected) {
                fillUp = true
                additionnalValue = -1
                schedulesSelected.push({'hDebut': scheduleHours[0], 'hFin': scheduleHours[1], 'date': date})

            } else {
                schedulesSelected.unshift({'hDebut': scheduleHours[0], 'hFin': scheduleHours[1], 'date': date})

            }
            let filled = false
            while (!filled && ((fillUp && i >= 0) || (!fillUp && i <= schedulesWithBG.length))) {
                let hour = schedulesWithBG[i].innerText.trim().split('-')
                hourNb = parseInt(hour[0].split(':'))
                if (hDebut == hourNb) {
                    filled = true
                } else if (fillUp) {
                    // let hDebut = parseInt(schedulesSelected[0].hDebut.split(':'))
                    if (hourNb > hDebut) {
                        schedulesWithBG[i].parentElement.style.backgroundColor = "blue"
                    }
                } else if (!fillUp) {
                    // let hDebut = parseInt(schedulesSelected[0].hDebut.split(':'))
                    if (hourNb < hDebut) {
                        schedulesWithBG[i].parentElement.style.backgroundColor = "blue"
                    }
                }
                i = i + additionnalValue
            }
        }
    }

    //si même journée mais période déja selectionnée => déselectionne tout
    else {
        let periodSelected = document.getElementsByName(date)
        periodSelected.forEach(schedule => {
            schedule.parentElement.style.backgroundColor = ""
        })
        schedulesSelected = []
        selectedSchedule.style.backgroundColor = "blue";
        schedulesSelected.push({'hDebut': scheduleHours[0], 'hFin': scheduleHours[1], 'date': date})
    }
    //ajoute le contenu de la réservation dans le bouton de soumission
    var button = document.getElementsByClassName('badge badge-light');
    var input= document.getElementsByName('reservation');
    if (schedulesSelected.length != 0) {
        var reservationFormat=date + ' de ' + schedulesSelected[0].hDebut + '-' + schedulesSelected[schedulesSelected.length - 1].hFin;
        button[0].innerText = reservationFormat;
        input[0].setAttribute('value', reservationFormat);
    } else {
        button[0].innerText = ""
        input[0].value="";
    }
}

function findHourIndex(hSelected, schedulesRow) {
    for (let i = 0; i < schedulesRow.length; i++) {
        if (schedulesRow[i].innerText == hSelected) {
            return i
        }
    }
    return null
}