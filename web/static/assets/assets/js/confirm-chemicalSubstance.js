document.getElementById("successTitle").innerHTML = "บันทึกข้อมูลสำเร็จ"
document.getElementById("loadingTitle").innerHTML = "กำลังบันทึกข้อมูล ..."

document.getElementById("confirmForm").addEventListener("submit", function(event) {
  event.preventDefault()
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show')
  var formData = new FormData(this)
  sendData(formData)
})

function sendData(formData){
  $.ajax({
    url: confirmUrl,
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    success: function(response) {
      $('#loadingModal').modal('hide')
      console.log('Success:', response)
      $('#successModal').modal('show')
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
}

function refreshPage() {
  window.location.reload();
}