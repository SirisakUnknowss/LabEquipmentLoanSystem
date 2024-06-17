
var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
var csrfToken = null
if (csrfTokenInput) {
  csrfToken = csrfTokenInput.value
} else {
  console.error('CSRF Token input field not found')
}

function confirmReturn()
{
  document.getElementById("loadingTitle").innerHTML = "กำลังอัพเดตข้อมูล ..."
  document.getElementById("successTitle").innerHTML = "ยืนยันการคืนอุปกรณ์สำเร็จ"
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show')
  var formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrfToken)
  formData.append('orderID', document.getElementById("orderID").value)
  sendRequest(confirmReturnUrl, formData, 'notifications')
}