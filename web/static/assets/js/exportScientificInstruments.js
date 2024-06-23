function downloadOrderData(event, arg) {
    event.preventDefault()
    var nameFile = "Order_Booking.xlsx"
    loadContent(urlExportOrder, nameFile)
}

function downloadDataUses(event, id, name) {
    event.preventDefault()
    var url = urlExportDataUses
    var nameFile = "Uses_ScientificInstruments.xlsx"
    console.log(id)
    if (id != null)
    {
        nameFile = "Uses_"+ name + ".xlsx"
        url = urlExportDataUses + "?id=" + id
    }
    loadContent(url, nameFile)
}