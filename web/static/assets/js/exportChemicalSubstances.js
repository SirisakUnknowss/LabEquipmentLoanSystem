
function downloadUserData(event, arg) {
    event.preventDefault()
    var nameFile = "User_ChemicalSubstances.xlsx"
    loadContent(urlExportDataUser, nameFile)
}
function downloadOrderData(event, arg) {
    event.preventDefault()
    var nameFile = "Order_ChemicalSubstances.xlsx"
    loadContent(urlExportOrder, nameFile)
}
function downloadDataUses(event, serialNumber, name) {
    event.preventDefault()
    var url = urlExportDataUses
    var nameFile = "Uses_ChemicalSubstances.xlsx"
    if (serialNumber != null)
    {
        nameFile = "Uses_"+ name + ".xlsx"
        url = urlExportDataUses + "?serialNumber=" + serialNumber
    }
    var nameFile = "Uses_"+ name + ".xlsx"
    loadContent(url, nameFile)
}

function loadContent(url = "", nameFile) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.responseType = "blob";

    xhr.onload = function () {
        if (xhr.status === 200) {
            var blob = xhr.response;
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.style.display = "none";
            a.href = url;
            a.download = nameFile;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            alert("Error downloading the file!");
        }
    };

    xhr.onerror = function () {
        alert("Error downloading the file!");
    };

    xhr.send();
}