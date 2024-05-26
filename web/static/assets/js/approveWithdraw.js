var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
var csrfToken = null
if (csrfTokenInput) {
    csrfToken = csrfTokenInput.value
} else {
    console.error('CSRF Token input field not found')
}

document.getElementById("loadingTitle").innerHTML = "กำลังบันทึกข้อมูล ..."
document.getElementById("successTitle").innerHTML = "บันทึกรายการสำเร็จ"

function disapprovedWithdraw(id) {
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show')
  var formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrfToken)
  formData.append('orderID', id)
  formData.append('status', "disapproved")
  sendData(formData)
}

function approvalWithdraw(status) {
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show')
  var formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrfToken)
  formData.append('orderID', document.getElementById("dataID").value)
  formData.append('status', status)
  $.ajax({
    url: approvalUrl,
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    success: function(response) {
      $('#loadingModal').modal('hide')
      console.log('Success:', response)
      $('#successModal').modal('show')
      setTimeout(function() {
        location.href = "notifications"
      }, 2000)
    },
    error: function(xhr, status, error) {
      $('#loadingModal').modal({backdrop: '', keyboard: true})
      $('#loadingModal').modal('hide')
      $('#errorModal').modal('show')
      console.error('Error:', error)
    }
  })
}