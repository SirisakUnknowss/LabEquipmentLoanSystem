
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

const exportAllBookingButton = document.querySelector("#exportAllBookingButton")
const exportApprovedBookingButton = document.querySelector("#exportApprovedBookingButton")
const exportWaitingBookingButton = document.querySelector("#exportWaitingBookingButton")
const exportCanceledBookingButton = document.querySelector("#exportCanceledBookingButton")
const exportDisapprovedBookingButton = document.querySelector("#exportDisapprovedBookingButton")
const exportMostScientificInstrumentButton = document.querySelector("#exportMostScientificInstrumentButton")

exportAllBookingButton.addEventListener('click', (event) => {
    nameFile = "allBookingData.xlsx"
    requestContent(urlExportDataBooking + "?getData=")
})

exportWaitingBookingButton.addEventListener('click', (event) => {
    nameFile = "waitingApproveBookingData.xlsx"
    requestContent(urlExportDataBooking + "?getData=waiting")
})
exportApprovedBookingButton.addEventListener('click', (event) => {
    nameFile = "ApprovedBookingData.xlsx"
    requestContent(urlExportDataBooking + "?getData=approved")
})
exportCanceledBookingButton.addEventListener('click', (event) => {
    nameFile = "canceledBookingData.xlsx"
    requestContent(urlExportDataBooking + "?getData=canceled")
})

exportDisapprovedBookingButton.addEventListener('click', (event) => {
    nameFile = "disapprovedBookingData.xlsx"
    requestContent(urlExportDataBooking + "?getData=disapproved")
})
if (exportMostScientificInstrumentButton)
{
    exportMostScientificInstrumentButton.addEventListener('click', (event) => {
        nameFile = "mostScientificInstrumentData.xlsx"
        requestContent(urlExportData + "?getData=Most")
    })
}