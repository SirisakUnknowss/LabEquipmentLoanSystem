document.getElementById("loadingTitle").innerHTML = "กำลังลบข้อมูล ..."
document.getElementById("successTitle").innerHTML = "ยกเลิกรายการสำเร็จ"
var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
var csrfToken = null
if (csrfTokenInput) {
    csrfToken = csrfTokenInput.value
} else {
    console.error('CSRF Token input field not found')
}

function showConfirmDelete(id)
{
    $('#modalDelete').modal('hide')
    $('#loadingModal').modal('show')
    var formData = new FormData()
    formData.append('csrfmiddlewaretoken', csrfToken)
    formData.append('orderID', document.getElementById("dataID").value)
    $.ajax({
      url: cancelUrl,
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        $('#loadingModal').modal('hide')
        console.log('Success:', response)
        $('#successModal').modal('show')
        setTimeout(function() {
          // location.href = "notifications"
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