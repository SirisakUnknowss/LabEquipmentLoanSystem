
var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
var csrfToken = null
if (csrfTokenInput) {
  csrfToken = csrfTokenInput.value
} else {
  console.error('CSRF Token input field not found')
}

function returnEquipments()
{
  document.getElementById("loadingTitle").innerHTML = "กำลังบันทึกข้อมูล ..."
  document.getElementById("successTitle").innerHTML = "ทำรายการสำเร็จ"
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show')
  var formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrfToken)
  formData.append('orderID', document.getElementById("orderID").value)
  sendRequest(returnUrl, formData, 'notifications')
}

function borrowingAgain()
{
  document.getElementById("loadingTitle").innerHTML = "กำลังบันทึกข้อมูล ..."
  document.getElementById("successTitle").innerHTML = "ทำรายการสำเร็จ"
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show')
  var formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrfToken)
  formData.append('orderID', document.getElementById("orderID").value)
  sendRequest(borrowingAgainUrl, formData, 'notifications')
}

function confirmBorrowing()
{
  document.getElementById("loadingTitle").innerHTML = "กำลังบันทึกข้อมูล ..."
  document.getElementById("successTitle").innerHTML = "ทำรายการสำเร็จ"
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show')
  var formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrfToken)
  sendRequest(confirmBorrowingUrl, formData, 'notifications')
}

function removeItem(id)
{
  document.getElementById("loadingTitle").innerHTML = "กำลังบันทึกข้อมูล ..."
  document.getElementById("successTitle").innerHTML = "ทำรายการสำเร็จ"
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show')
  var formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrfToken)
  formData.append('itemID', id)
  sendRequest(removeItemUrl, formData, 'cart')
}