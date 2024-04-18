

// const confirmBtn = document.getElementById("confirmBtn")
// $('#loadingModal').modal({backdrop: 'static', keyboard: false}) 
// confirmBtn.addEventListener("click", () => {
//     console.log("confirmBtn")
// })


function validateForm() {
    return false
    // Perform your validation logic here
    var name = document.forms["add-chemicalSubstance"]["name"].value
    if (name == "") {
      alert("Name must be filled out")
      return false // Prevent form submission
    }
    // If validation passes, you can submit the form
    return true
  }

document.addEventListener('DOMContentLoaded', function()
{
  const id_GHS = document.getElementById("id_GHS")
  const id_unClass = document.getElementById("id_unClass")
  const ghsList = document.getElementById("ghsList")
  const unList = document.getElementById("unList")
  var checkboxes = document.querySelectorAll('input[type="checkbox"]')

  function resetCheckboxes() {
    checkboxes.forEach(function(checkbox) {
      checkbox.checked = false
    })
  }
  
  id_GHS.addEventListener('click', function() {
    resetCheckboxes()
    if (this.checked) {
      ghsList.className = "flex-container"
      unList.className = "d-none"
    }
  })
  
  id_unClass.addEventListener('click', function() {
    resetCheckboxes()
    if (this.checked) {
      unList.className = "flex-container"
      ghsList.className = "d-none"
    }
  })
})