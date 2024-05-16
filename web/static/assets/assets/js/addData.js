document.getElementById("successTitle").innerHTML = "บันทึกข้อมูลสำเร็จ"
document.getElementById("loadingTitle").innerHTML = "กำลังบันทึกข้อมูล ..."


document.getElementById("addData").addEventListener("submit", function(event) {
  event.preventDefault();
  $('#successModal').modal({backdrop: 'static', keyboard: false})
  var formData = new FormData(this);

  $.ajax({
    url: confirmUrl,
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    success: function(response) {
      console.log('Success:', response);
      $('#successModal').modal('show');
      setTimeout(function() {
        window.location.href = response.result; // Replace with your URL
      }, 2000);
    },
    error: function(xhr, status, error) {
      console.error('Error:', error);
      var response = JSON.parse(xhr.responseText);
      $('#errorTitle').html(response.error)
      $('#errorModal').modal('show')
    }
  });
});

function refreshPage() {
  window.location.reload();
} 