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
const exportEquipmentAllButton = document.querySelector("#exportEquipmentAllButton")

exportEquipmentAllButton.addEventListener('click', (event) => {
    nameFile = "equipmentAllData.csv"
    requestContent(urlExportData + "?getData=")
})