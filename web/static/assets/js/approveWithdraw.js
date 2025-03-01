var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
var csrfToken = null
if (csrfTokenInput) {
  csrfToken = csrfTokenInput.value
} else {
  console.error('CSRF Token input field not found')
}

function approvalWithdraw(status) {
  document.getElementById("loadingTitle").innerHTML = "กำลังบันทึกข้อมูล ..."
  document.getElementById("successTitle").innerHTML = "บันทึกรายการสำเร็จ"
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show')
  var formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrfToken)
  formData.append('orderID', document.getElementById("orderID").value)
  formData.append('status', status)
  sendRequest(approvalUrl, formData, 'notifications')
}