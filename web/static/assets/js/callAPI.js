function sendRequest(url, formData, location)
{
    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $('#loadingModal').modal('hide')
            console.log('Success:', response)
            $('#successModal').modal('show')
            setTimeout(function() {
                console.log(location)
                window.location.href = location
            }, 2000)
        },
        error: function(xhr, status, error) {
            $('#loadingModal').modal({backdrop: '', keyboard: true})
            $('#loadingModal').modal('hide')
            console.error('Error:', error);
            var response = JSON.parse(xhr.responseText);
            $('#errorTitle').html(response.error)
            $('#errorModal').modal('show')
        }
    })
}
  
function refreshPage()
{
    window.location.reload();
}