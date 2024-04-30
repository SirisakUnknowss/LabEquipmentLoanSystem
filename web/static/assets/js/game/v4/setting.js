function is_iPhone() { return ['iPhone'].includes(navigator.platform) }

var config
var scriptLoader = document.createElement("script")


config = {
    dataUrl: '/static/unity/'+gameVersion+'/App.data',
    frameworkUrl: '/static/unity/'+gameVersion+'/App.framework.js',
    codeUrl: '/static/unity/'+gameVersion+'/App.wasm',
    // memoryUrl: '/static/unity/'+gameVersion+'/App.asm.mem',
    streamingAssetsUrl: "StreamingAssets",
    companyName: "MSoft",
    productName: "Fintasy",
    productVersion: "Alpha " + gameVersion,
};
scriptLoader.src = '/static/unity/'+gameVersion+'/App.loader.js'


scriptLoader.type = 'application/javascript'
scriptLoader.onload = () => {
// var screenHeight = topnav.clientHeight + (topnav.clientHeight * 0.1)
// container.style.marginTop = screenHeight + "px"
canvas.style.background = "url('/static/images/game/App.png') center / cover";
const message = JSON.stringify({'walletAddress': walletAddress, 'urls':host, 'token':token, 'sessionId': sessionId, 'csrfCookie': csrf_token})
createUnityInstance(canvas, config, (progress) => {
    progressText.innerHTML = (100 * progress).toFixed(2) + "%"
    progressBar.style.width = 100 * progress + "%"
}).then((unityInstance) => {
    splashScreen.style.display = "none";
    unityInstance.SendMessage("UserInfo", "ReceiveAppData", message)
    gameInstance = unityInstance;
})
}

document.body.appendChild(scriptLoader)