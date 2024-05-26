document.getElementById("loadingTitle").innerHTML = "กำลังลบข้อมูล ..."

document.getElementById("delete-chemicalSubstance").addEventListener("submit", function(event) {
  event.preventDefault();
  $('#modalDelete').modal('hide')
  $('#loadingModal').modal('show');
  var formData = new FormData(this);
  $.ajax({
    url: deleteUrl,
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    success: function(response) {
      $('#loadingModal').modal('hide')
      console.log('Success:', response);
      $('#deleteSuccessModal').modal('show');
      setTimeout(function() {
        window.location.reload()
      }, 2000);
    },
    error: function(xhr, status, error) {
      $('#loadingModal').modal({backdrop: '', keyboard: true})
      $('#loadingModal').modal('hide')
      console.error('Error:', error);
    }
  });
});