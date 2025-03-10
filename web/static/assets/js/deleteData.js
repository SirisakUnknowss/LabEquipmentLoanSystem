document.getElementById("loadingTitle").innerHTML = "กำลังลบข้อมูล ..."

document.getElementById("formDeleteData").addEventListener("submit", function(event) {
  event.preventDefault()
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show')
  var formData = new FormData(this)
  $.ajax({
    url: deleteUrl,
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    success: function(response) {
      $('#loadingModal').modal('hide')
      console.log('Success:', response)
      $('#deleteSuccessModal').modal('show')
      setTimeout(function() {
        location.reload()
      }, 2000)
    },
    error: function(xhr, status, error) {
      $('#loadingModal').modal({backdrop: '', keyboard: true})
      $('#loadingModal').modal('hide')
      console.error('Error:', error)
    }
  })
})

function showConfirmDelete(id)
{
    const dataID = document.querySelector("#dataID")
    dataID.value = id
}