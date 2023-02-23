
const idScientificInstrument = document.querySelector("#id_pk_scientificInstruments")
const imageScientificInstruments = document.querySelector("#image_scientificInstruments")
const nameDisplay = document.querySelector("#id_name_scientificInstruments")
const numberDisplay = document.querySelector("#id_number_scientificInstruments")
const dateBooking = document.querySelector("#id_dateBooking")
const timeStart = document.querySelector("#id_timeStart")
const confirmBooking = document.querySelector("#confirmBooking")
    
const today = new Date()
const tomorrow = new Date(today)
const lastMonth = new Date(today)
lastMonth.setMonth(tomorrow.getMonth() + 2)
const dayMin = tomorrow.getDate().toString().padStart(2, '0');;
const monthMin = (tomorrow.getMonth() + 1).toString().padStart(2, '0');; // Add 1 because the month is zero-indexed
const yearMin = tomorrow.getFullYear();
const dayMax = getLastDateOfMonth(lastMonth.getFullYear(), lastMonth.getMonth()).toString().padStart(2, '0');;
const monthMax = (lastMonth.getMonth()).toString().padStart(2, '0');; // Add 1 because the month is zero-indexed
const yearMax = lastMonth.getFullYear();
// dateBooking.min = `${yearMin}-${monthMin}-${dayMin}`;
dateBooking.setAttribute('min', `${yearMin}-${monthMin}-${dayMin}`);
dateBooking.setAttribute('max', `${yearMax}-${monthMax}-${dayMax}`);

dateBooking.addEventListener('input', () => {
    const selectedDate = dateBooking.value;
    console.log(selectedDate);
    requestContent(urlGetTimeCanBooking + "?id=" + idScientificInstrument.value + "&dateRequest=" + selectedDate)
  });

function getLastDateOfMonth(year, month) {
    const date = new Date(year, month, 0);
    return date.getDate();
}

function showBooking(id)
{
    var data = scientificInstrumentsJson.find(function(item) { return item.pk == id })
    console.log(data)
    idScientificInstrument.value = data.pk
    nameDisplay.innerHTML = data.fields.name
    numberDisplay.innerHTML = data.fields.number
    imageScientificInstruments.src = data.fields.image
}

async function loadContent(url="") {
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

async function requestContent(url="") {
    clearSelect()
    .then(() => loadContent(url)
    .then(jsonObject => display(jsonObject)))
}

async function clearSelect()
{
    while (timeStart.options.length > 1) {
        timeStart.remove(1);
    }
}

async function display(jsonObject) {
    console.log(jsonObject)
    console.log(typeof jsonObject.result)
    let result = jsonObject.result
    const dateError = document.querySelector("#dateError")
    dateError.innerHTML = ""
    if (result.length > 0)
    {
        for (let index=0; index < result.length; index++)
        {
            optionEle = document.createElement("option")
            optionEle.value = result[index]
            optionEle.innerHTML = result[index]
            timeStart.appendChild(optionEle)
        }
        return
    }
    dateError.innerHTML = jsonObject.error
    confirmBooking.disabled = true
}

function checkTimeSelect() {
    var selectedValue = timeStart.value
    if (selectedValue == "") confirmBooking.disabled = true
    else confirmBooking.disabled = false
  }