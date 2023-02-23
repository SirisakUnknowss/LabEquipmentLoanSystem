
const nameInput = document.querySelector("#id_name")
const numberInput = document.querySelector("#id_number")
const placeInput = document.querySelector("#id_place")
const detailInput = document.querySelector("#id_detail")
const annotationInput = document.querySelector("#id_annotation")
const imageDisplay = document.querySelector("#imageDisplay")
const dismissModalScientificDelete = document.querySelector("#dismissModalScientificDelete")
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

function showConfirmDelete(id)
{
    var data = scientificInstrumentsJson.find(function(item) { return item.pk == id })
    const nameDelete = document.querySelector("#nameDelete")
    const scientificInstrumentDelete = document.querySelector("#scientificInstrumentDelete")
    scientificInstrumentDelete.value = data.pk
    nameDelete.innerHTML = data.fields.name
    
    $('#modalScientificDelete').modal('show')
}

dismissModalScientificDelete.onclick = function() {
    $('#modalScientificDelete').modal('hide')
  }