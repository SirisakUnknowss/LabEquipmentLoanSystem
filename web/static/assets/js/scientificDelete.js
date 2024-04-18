const dismissModalScientificDelete = document.querySelector("#dismissModalScientificDelete")
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