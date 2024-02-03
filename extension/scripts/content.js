const getImages = () => {
    const imgs = document.getElementsByTagName("img")

    /**
     * @type {HTMLImageElement[]}
     */
    const imgTags = []

    /**
     * @type {string[]}
     */
    const filtered = []

    for (let e of imgs) {
        if (!e.alt) {
            if (e.src.endsWith('jpg') || e.src.endsWith('png')) {
                filtered.push(e.src)
                imgTags.push(e)
            }
        }
    }

    return {
        img: filtered,
        imgTags
    }

}

const getAnchorTags = () => {
    const links = document.getElementsByTagName("a")
    const regex = /\bhttps?:\/\/[-a-zA-Z0-9+&@#\/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#\/%=~_|]/;

    /**
     * @type {string[]}
     */
    const urls = []

    /**
     * @type {HTMLAnchorElement[]}
     */
    const anchorTags = []


    for (let a of links) {
        if (a.href && regex.test(a.href)) {
            urls.push(a.href)
            anchorTags.push(a)
        }
    }

    return {
        anchorTags,
        urls: urls
    }
}

const improveAccessibility = () => {
    const {urls, anchorTags} = getAnchorTags()
    const {img, imgTags} = getImages()

    /**
     * 
     * @param {Object} response 
     * @param {string[]} response.anchors
     * @param {string[]} response.buttons
     * @param {string[]} response.images
     */
    const handleResponse = (response) => {
        if (!response) {
            console.log("response is not defined, returning from content.js")
            return
        }

        for (let i = 0; i < response.anchors.length; i++) {
            anchorTags[i].ariaLabel = response.anchors[i]
        }
        for (let i = 0; i < response.images.length; i++) {
            imgTags[i].alt = response.images[i].substr(9, response.images[i].length - 6 - 11)
        }

        console.log("anchor and image tags updated successfully")
    }


    if (typeof chrome !== 'undefined') {
        chrome.runtime.sendMessage({urls, img}, handleResponse)
    } else if (typeof browser !== 'undefined') {
        browser.runtime
            .sendMessage({urls, img})
            .then(handleResponse, function (reason) {
                console.log(reason)
            })
    }

    return urls
}

improveAccessibility()
