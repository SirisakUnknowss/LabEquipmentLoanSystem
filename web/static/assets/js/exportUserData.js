function downloadUserData(event, name) {
    event.preventDefault()
    var nameFile = name + ".xlsx"
    loadContent(urlExportDataUser, nameFile)
}