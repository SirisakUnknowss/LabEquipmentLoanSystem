const dismissModalEquipmentDelete = document.querySelector("#dismissModalEquipmentDelete")

function showConfirmDelete(id)
{
    var data = equipmentsJson.find(function(item) { return item.pk == id })
    const nameDelete = document.querySelector("#nameDelete")
    const equipmentDelete = document.querySelector("#equipmentDelete")
    equipmentDelete.value = data.pk
    nameDelete.innerHTML = data.fields.name
    
    $('#modalEquipmentDelete').modal('show')
}

dismissModalEquipmentDelete.onclick = function() {
    $('#modalEquipmentDelete').modal('hide')
  }