document.getElementById("successTitle").innerHTML = "เพิ่มรายการสารเคมีสำเร็จ"


document.getElementById("add-chemicalSubstance").addEventListener("submit", function(event) {
  console.log(' ------------- Before ------------- ');
  event.preventDefault();
  console.log(' ------------- After ------------- ');
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
    }
  });
});

// document.addEventListener('DOMContentLoaded', function()
// {
//   const id_GHS = document.getElementById("id_GHS")
//   const id_unClass = document.getElementById("id_unClass")
//   const ghsList = document.getElementById("ghsList")
//   const unList = document.getElementById("unList")
//   var checkboxes = document.querySelectorAll('input[type="checkbox"]')

//   function resetCheckboxes() {
//     checkboxes.forEach(function(checkbox) {
//       checkbox.checked = false
//     })
//   }
  
//   id_GHS.addEventListener('click', function() {
//     resetCheckboxes()
//     if (this.checked) {
//       ghsList.className = "flex-container"
//       unList.className = "d-none"
//     }
//   })
  
//   id_unClass.addEventListener('click', function() {
//     resetCheckboxes()
//     if (this.checked) {
//       unList.className = "flex-container"
//       ghsList.className = "d-none"
//     }
//   })
// })