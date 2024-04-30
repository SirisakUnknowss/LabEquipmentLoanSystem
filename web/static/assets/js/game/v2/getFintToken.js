window.addEventListener('load', (event) => {
    deleteChallenge()
    if(!isAccessToken){
        return
    }
    getFintToken()
})

function deleteChallenge() {
    localStorage.removeItem('challenge');
    localStorage.removeItem('challengeCode');
}

function isAccessToken() {
    if (localStorage.getItem('finnoAccessToken')){
        return true
    }else{
        return false
    }
}

async function getFintToken() {
    // finnoRefreshToken()
    const response = await requestFintToken()
    console.log(response)
    let result = null
    if (response.status == 401) { 
        let newAccessToken = await finnoRefreshToken()
        const responseFintToken = await requestFintToken(newAccessToken)
        result = await responseFintToken.json()
        updateFintToken(result)
    }else if(response.status == 200 ){
        result = await response.json()
        updateFintToken(result)
    }else{
        throw new Error('Error Occured:' + response.statusText)
    }
}

async function requestFintToken(newAccessToken=null){
    console.log('-requestFintToken-')
    let accessToken = ''
    const url = document.getElementById('finnoGetFintTokenUrl').value
    if(newAccessToken == null)  {
        accessToken = localStorage.getItem('finnoAccessToken')
    }else{
        accessToken = newAccessToken
    }
    if (!accessToken) { throw new Error('Error Occured: No Access token') }

    let config = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer ' + accessToken
        }
    }
    
    const response = await fetch(url, config)
    return response
}

async function updateFintToken(result) {
    const finnoUpdateTokenUrl = document.getElementById('finnoUpdateFintTokenUrl').value
    const amount = result["data"]["token_outstanding"]
    let config = {
        method: 'POST',
        credentials: 'same-origin',

        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'

        },
        body: JSON.stringify({"amount": amount})
    }
    const updateResult = await fetch(finnoUpdateTokenUrl, config)
    return updateResult
}



async function reduceFintToken(amount){
    if (amount < 1) { throw new Error('Error Occured: Invalid amount of fintToken [' + amount + ']') }
    const url = document.getElementById('finnoDeductFintTokenUrl').value
    const accessToken = localStorage.getItem('finnoAccessToken')
    if (!accessToken) { throw new Error('Error Occured: No Access token') }

    let config = {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer ' + accessToken,
        },
        body: JSON.stringify({
            "redeem_amount": amount,
            "transaction_type": "DEDUCT_FINT_GAME"
        })
    }
    console.log(config)
    const response = await fetch(url, config)
    if (!response.ok) { throw new Error('Error Occured:' + response.statusText) }
    const jsonObject = await response.json()
    return jsonObject
}

async function finnoRefreshToken() {
    const accessToken = localStorage.getItem('finnoAccessToken')
    let url = document.getElementById('finnoRefreshTokenRequestDataUrl').value
    let config = {
        method: 'GET',
    }
    let response = await fetch(url, config)
    
    if (!response.ok) { throw new Error('Error Occured:' + response.statusText) }
    let data = await response.json()

    const formData = new URLSearchParams();
    formData.append('client_id', data['finnoClientID']);
    formData.append('refresh_token', data['finnoRefreshToken']);
    formData.append('grant_type', 'refresh_token');
    
    config = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer ' + accessToken,
        },
        body: formData
    }
    response = await fetch(data['refreshUrl'], config)
    
    if (!response.ok) { throw new Error('Error Occured:' + response.statusText) }
    const jsonObject = await response.json()
    const userID = await getUserID(jsonObject)
    await updateTokenOnServer(jsonObject, userID)
    return jsonObject["access_token"]
}

async function getUserID(jsonObject){
    const url = document.getElementById('finnoUserInfoUrl').value
    let config = {
        method: 'GET',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
          'Authorization': 'Bearer ' + jsonObject["access_token"]
        }
    }
    console.log(config)
    const response = await fetch(url, config)
    const result = await response.json()
    if (!response.ok) { throw new Error('Error Occured:' + response.statusText) }
    console.log(result)
    return result["data"]["external_id"]
}

async function updateTokenOnServer(jsonObject, userID){
    console.log('- updateTokenOnServer -')
    const finnoRefreshTokenCallbackUrl = document.getElementById('finnoRefreshTokenCallbackUrl').value
    let config = {
        method: 'POST',
        credentials: 'same-origin',

        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json; charset=UTF-8'

        },
        body: JSON.stringify({
            'finnoAccessToken': jsonObject["access_token"],
            'finnoExpiresIn': jsonObject["expires_in"],
            'finnoRefreshToken': jsonObject["refresh_token"],
            'finnoUserID': userID
        })
    }
    const updateResponse = await fetch(finnoRefreshTokenCallbackUrl, config)
    console.log(config)
    let result = await updateResponse.json()
    console.log(result)
    if (!result['success']){
        throw new Error('Error Occured:' + updateResponse['error'])
    }
    localStorage.setItem('finnoAccessToken', result['access_token'])
}

async function ajaxRequestPost(url, body=null ){
    let data = ''
    if (body != null){
        data = body
    }else{
        data = {payload: ''}
    }
    let config = {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken'),

        },
        body: JSON.stringify(body)
    }
    const response = await fetch(url, config)
    if (!response.ok) { throw new Error('Error Occured:' + response.statusText) }
    const jsonObject = await response.json()
    return jsonObject
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}
