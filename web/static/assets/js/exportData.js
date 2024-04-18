
var nameFile = ""
async function loadContent(url="") {
    fetch(url)
    .then(response => response.blob())
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      // the filename you want
      
      a.download = nameFile;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    })
    .catch(() => alert("Error downloading the file!"));
}

async function requestContent(url="") {
    loadContent(url)
}

const exportUserButton = document.querySelector("#exportUserButton")
const exportAllOrderButton = document.querySelector("#exportAllOrderButton")
const exportApprovedOrderButton = document.querySelector("#exportApprovedOrderButton")
const exportCompletedOderButton = document.querySelector("#exportCompletedOderButton")
const exportWaittingOrderButton = document.querySelector("#exportWaittingOrderButton")
const exportReturnedOrderButton = document.querySelector("#exportReturnedOrderButton")
const exportCanceledOrderButton = document.querySelector("#exportCanceledOrderButton")
const exportDisapprovedOrderButton = document.querySelector("#exportDisapprovedOrderButton")
const exportOverduedOrderButton = document.querySelector("#exportOverduedOrderButton")
const exportMostEquipmentButton = document.querySelector("#exportMostEquipmentButton")

exportUserButton.addEventListener('click', (event) => {
    nameFile = "userData.xlsx"
    requestContent(urlExportDataUser)
})
exportAllOrderButton.addEventListener('click', (event) => {
    nameFile = "allOrderData.xlsx"
    requestContent(urlExportDataBorrowing + "?getData=")
})
exportCompletedOderButton.addEventListener('click', (event) => {
    nameFile = "completedOderData.xlsx"
    requestContent(urlExportDataBorrowing + "?getData=completed")
})
exportReturnedOrderButton.addEventListener('click', (event) => {
    nameFile = "returnedData.xlsx"
    requestContent(urlExportDataBorrowing + "?getData=returned")
})
exportWaittingOrderButton.addEventListener('click', (event) => {
    nameFile = "waittingApproveOrderData.xlsx"
    requestContent(urlExportDataBorrowing + "?getData=waiting")
})
exportApprovedOrderButton.addEventListener('click', (event) => {
    nameFile = "ApprovedOrderData.xlsx"
    requestContent(urlExportDataBorrowing + "?getData=approved")
})
exportCanceledOrderButton.addEventListener('click', (event) => {
    nameFile = "canceledOrderData.xlsx"
    requestContent(urlExportDataBorrowing + "?getData=canceled")
})
exportDisapprovedOrderButton.addEventListener('click', (event) => {
    nameFile = "disapprovedOrderData.xlsx"
    requestContent(urlExportDataBorrowing + "?getData=disapproved")
})
exportOverduedOrderButton.addEventListener('click', (event) => {
    nameFile = "overduedOrderData.xlsx"
    requestContent(urlExportDataBorrowing + "?getData=overdued")
})
exportMostEquipmentButton.addEventListener('click', (event) => {
    nameFile = "mostEquipmenData.xlsx"
    requestContent(urlExportData + "?getData=Most")
})