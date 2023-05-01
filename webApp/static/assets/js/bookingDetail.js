
const nameScientificInstrument = document.querySelector("#nameScientificInstrument")
const numberScientificInstrument = document.querySelector("#numberScientificInstrument")
const usernameBooking = document.querySelector("#usernameBooking")
const userIdBooking = document.querySelector("#userIdBooking")
const placeScientificInstrument = document.querySelector("#placeScientificInstrument")
const datetimeBooking = document.querySelector("#datetimeBooking")
const statusBooking = document.querySelector("#statusBooking")
const imageDisplay = document.querySelector("#imageDisplay")
const scientificInstrumentIDInput = document.querySelector("#scientificInstrumentIDInput")
const scientificInstrumentsSelect = document.querySelector("#scientificInstrumentsSelect")
const searchByID = document.querySelector("#searchByID")

function showDetail(id)
{    
    requestContent(urlGetBookingId + "?id=" + id)
    $('#modalBookingDetail').modal('show')
}

async function loadContent(url="")
{
    const response = await fetch(url, {
        method: 'GET',
        headers: {'Content-type': 'application/json'},
        cache: 'no-store'
    })
    if (!response.ok){
        isWorking = false
    }
    const jsonObject = await response.json()
    return jsonObject
}

async function requestContent(url="")
{
    loadContent(url)
    .then(jsonObject => display(jsonObject))
}

async function loadContentPost(url="", data)
{
    xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    console.log(csrf_token);
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.setRequestHeader("Content-Type", "text/plain;charset=UTF-8"); 
  
    xhr.send(data);
}

async function requestContentPost(url="", data)
{
    loadContentPost(url, data)
}

function display(jsonObject)
{
    console.log(jsonObject)
    var data = jsonObject.result
    nameScientificInstrument.innerHTML = data.scientificInstrument.name
    numberScientificInstrument.innerHTML = data.scientificInstrument.number
    usernameBooking.innerHTML = data.user.firstname + " " + data.user.lastname
    userIdBooking.innerHTML = data.user.studentID
    placeScientificInstrument.innerHTML = data.scientificInstrument.annotation
    datetimeBooking.innerHTML = data.dateBooking + " " + data.timeBooking
    setStatusBooking(data.status)

    imageDisplay.src = (data.scientificInstrument.image).replace("media/", "")
    if (data.scientificInstrument.image == "")
    {
        imageDisplay.src = urlPlaceHolder
    }
}
async function loadContentSelected(params = "") {
    const response = await fetch(urlScientificInstruments + params, {
        method: 'GET',
        headers: {'Content-type': 'application/json'},
        cache: 'no-store'
    })
    if (!response.ok){
        isWorking = false
    }
    const jsonObject = await response.json()
    return jsonObject
}

function onSelectSearch()
{
    var value = scientificInstrumentsSelect.options[scientificInstrumentsSelect.selectedIndex].value
    scientificInstrumentIDInput.value = value
    searchByID.submit()
    // requestContentPost(urlBookings, value)
}

window.addEventListener('load', (event) => {
    requestContentSelected()
})

async function requestContentSelected(params) {
    loadContentSelected(params)
    .then(jsonObject => displaySelected(jsonObject))
    // .then(() => {
    //     var value = scientificInstrumentsSelect.options[scientificInstrumentsSelect.selectedIndex].value
    //     requestContentPost(urlBookings, {"scientificInstrument=":value})
    // })
}

async function displaySelected(jsonObject)
{
    let result = jsonObject.result
    optionEle = document.createElement("option")
    optionEle.value = null
    optionEle.innerHTML = "--- ทั้งหมด ---"
    scientificInstrumentsSelect.appendChild(optionEle)
    if (result.length > 0)
    {
        for (let index=0; index < result.length; index++)
        {
            optionEle = document.createElement("option")
            optionEle.value = result[index].id
            optionEle.innerHTML = result[index].name
            if (String(result[index].id) == String(scientificInstrumentID)) { optionEle.setAttribute("selected", "selected") }
            scientificInstrumentsSelect.appendChild(optionEle)

            // optionSearchEle = document.createElement("option")
            // optionSearchEle.value = result[index].id
            // optionSearchEle.innerHTML = result[index].name
            // if (String(result[index].id) == String(scientificInstrumentID)) { optionSearchEle.setAttribute("selected", "selected") }
            // scientificInstrumentsSelect.appendChild(optionSearchEle)
        }
    }
}

function setStatusBooking(status)
{
    if (status == "waiting")
    {
        statusBooking.className = "btn badge badge-sm bg-gradient-warning w-50 w-md-50 w-sm-100"
        statusBooking.innerHTML = "รออนุมัติ"
    }
    else if (status == "approved")
    {
        statusBooking.className = "btn badge badge-sm bg-gradient-info w-50 w-md-50 w-sm-100"
        statusBooking.innerHTML = "อนุมัติแล้ว"
    }
    else if (status == "canceled")
    {
        statusBooking.className = "btn badge badge-sm bg-gradient-danger w-50 w-md-50 w-sm-100"
        statusBooking.innerHTML = "ยกเลิก"
    }
    else if (status == "disapproved")
    {
        statusBooking.className = "btn badge badge-sm bg-gradient-danger w-50 w-md-50 w-sm-100"
        statusBooking.innerHTML = "คำขอล้มเหลว"
    }
    else if (status == "completed")
    {
        statusBooking.className = "btn badge badge-sm bg-gradient-success w-50 w-md-50 w-sm-100"
        statusBooking.innerHTML = "คืนเรียบร้อยแล้ว"
    }
    else if (status == "overdued")
    {
        statusBooking.className = "btn badge badge-sm bg-gradient-danger w-50 w-md-50 w-sm-100"
        statusBooking.innerHTML = "เกินกำหนดคืน"
    }
    else if (status == "returned")
    {
        statusBooking.className = "btn badge badge-sm bg-gradient-warning w-50 w-md-50 w-sm-100"
        statusBooking.innerHTML = "คืนอุปกรณ์"
    }
}