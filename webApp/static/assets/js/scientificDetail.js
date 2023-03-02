
const nameInput = document.querySelector("#id_name")
const numberInput = document.querySelector("#id_number")
const placeInput = document.querySelector("#id_place")
const detailInput = document.querySelector("#id_detail")
const annotationInput = document.querySelector("#id_annotation")
const imageDisplay = document.querySelector("#imageDisplay")
function showDetail(id)
{
    var data = scientificInstrumentsJson.find(function(item) { return item.pk == id })
    nameInput.innerHTML = data.fields.name
    numberInput.innerHTML = data.fields.number
    placeInput.innerHTML = data.fields.place
    detailInput.innerHTML = data.fields.detail
    annotationInput.innerHTML = data.fields.annotation
    imageDisplay.src = data.fields.image
    if (data.fields.image == "")
    {
        imageDisplay.src = urlPlaceHolder
    }
}