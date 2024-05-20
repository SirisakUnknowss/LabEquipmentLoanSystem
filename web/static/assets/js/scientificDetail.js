
const nameInput = document.querySelector("#id_name")
const numberInput = document.querySelector("#id_number")
const placeInput = document.querySelector("#id_place")
const detailInput = document.querySelector("#id_detail")
const annotationInput = document.querySelector("#id_annotation")
const imageDisplay = document.querySelector("#imageDisplay")
function showDetail(id)
{
    var data = resultsJson.find(function(item) { return item.id === id })
    nameInput.innerHTML = data.name
    numberInput.innerHTML = data.number
    placeInput.innerHTML = data.place
    detailInput.innerHTML = data.detail
    annotationInput.innerHTML = data.annotation
    try {
        imageDisplay.src = data.image
    }catch {
        imageDisplay.src = urlPlaceHolder
    }
}

function imgError(image) {
    image.src = urlPlaceHolder
    return true;
}