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