
const category  = document.getElementById('id_category')
const branch    = document.getElementById('id_branch')

addInputOtherCategory(category.selectedIndex)
addInputOtherBranch(branch.selectedIndex)

branch.onchange = function() {
    var index = this.selectedIndex
    addInputOtherBranch(index)
}
category.onchange = function() {
    var index = this.selectedIndex
    addInputOtherCategory(index)
}
function checkInp()
{
    firstname = document.forms["formSignin"]["firstname"].value
    lastname = document.forms["formSignin"]["lastname"].value
    if (!isNaN(firstname) || !isNaN(lastname)) 
    {
        alert("กรอกเฉพาะตัวอักษรเท่านั้น")
        return false
    }
}

function addInputOtherCategory(index)
{
    var valueText = category.children[index].value.trim()
    if (valueText == "other") {
        document.getElementById("categoryOther").className = "input-group input-group-outline mb-3 is-filled"
        document.getElementById("id_categoryOther").setAttribute('required', '')
    }
    else {
        document.getElementById("categoryOther").className = "d-none"
        document.getElementById("id_categoryOther").removeAttribute('required')
        document.getElementById("id_categoryOther").value = null
    }
}

function addInputOtherBranch(index)
{
    var valueText = branch.children[index].value.trim()
    if (valueText == "other") {
        document.getElementById("branchOther").className = "input-group input-group-outline mb-3 is-filled"
        document.getElementById("id_branchOther").setAttribute('required', '')
    }
    else {
        document.getElementById("branchOther").className = "d-none"
        document.getElementById("id_branchOther").removeAttribute('required')
        document.getElementById("id_branchOther").value = null
    }
}