
var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
var csrfToken = null
if (csrfTokenInput) {
  csrfToken = csrfTokenInput.value
} else {
  console.error('CSRF Token input field not found')
}

function showConfirmDelete()
{
  document.getElementById("loadingTitle").innerHTML = "กำลังอัพเดตข้อมูล ..."
  document.getElementById("successTitle").innerHTML = "ยกเลิกรายการสำเร็จ"
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show')
  var formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrfToken)
  formData.append('orderID', document.getElementById("orderID").value)
  sendRequest(cancelUrl, formData, 'notifications')
}