document.getElementById("successTitle").innerHTML = "บันทึกข้อมูลสำเร็จ"
document.getElementById("loadingTitle").innerHTML = "กำลังบันทึกข้อมูล ..."
var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
var csrfToken = null
if (csrfTokenInput) {
    csrfToken = csrfTokenInput.value;
    console.log('CSRF Token:', csrfToken);
} else {
    console.error('CSRF Token input field not found');
}

function showAddCartBtn(id, obj) {
  var btn = document.getElementById("addCart" + id)
  if (obj.value > 0)
  {
    btn.disabled = false
  }
  else
  {
    btn.disabled = true
  }
}

function addToCart(id) {
  var formData = new FormData();
  var quantity = document.getElementById('quantity'+id).value
  formData.append('csrfmiddlewaretoken', csrfToken)
  formData.append('id', id)
  formData.append('quantity', quantity)
  sendData(formData)
}

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