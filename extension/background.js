const SERVER_BASE_URL = 'http://127.0.0.1:6900'
const PROCESSING_API_ENDPOINT = '/process-elements'


/**
 * @typedef Message
 * @type {Object}
 * @property {string[]} anchors
 * @property {string[]} images
 * @property {string[]} buttons 
 * 
 * @param {Message} message 

 * @returns {Promise<Message>}
 */
async function generateAccessibleContent(message) {
    const resp = await fetch(SERVER_BASE_URL + PROCESSING_API_ENDPOINT, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            anchors: message.anchors,
            images: message.images,
            buttons: message.buttons
        })
    })
    const data = await resp.json()
    return data;
}

const isChrome = (typeof chrome !== 'undefined')
const webbrowser = isChrome ? chrome : browser;

webbrowser.runtime.onInstalled.addListener(() => {
    console.log(`accessify launched in ${ isChrome ? 'chrome' : 'firefox' }`);
});


webbrowser.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    generateAccessibleContent({
        anchors: message.urls,
        images: message.img,
        buttons: []
    })
        .then(data => sendResponse(data))

    return true;
});


