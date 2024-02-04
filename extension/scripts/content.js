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

const getUserPreferences = () => {
    const key = "accessify-preferences"

  chrome.storage.local.get(key, (response) => {
    console.log("Storage response", response.key)
  })

    const storedPreferences = localStorage.getItem(key)
    if (storedPreferences) {
        return JSON.parse(storedPreferences)
    } else {
        return {
            images: true,
            buttons: true,
            anchors: true,
        }
    }
}

const improveAccessibility = () => {
    let urls = [], anchorTags = [], img = [], imgTags = []
    const fetchedAnchorTags = getAnchorTags()
    urls = fetchedAnchorTags.urls
    anchorTags = fetchedAnchorTags.anchorTags
    const fetchedImageTags = getImages()
    img = fetchedImageTags.img
    imgTags = fetchedImageTags.imgTags
    /*
    const userPreferences = getUserPreferences()

    if (userPreferences.anchors) {
      const fetchedAnchorTags = getAnchorTags()
      urls = fetchedAnchorTags.urls
      anchorTags = fetchedAnchorTags.anchorTags
    }
    if (userPreferences.images) {
      const fetchedImageTags = getImages()
      img = fetchedImageTags.urls
      imgTags = fetchedImageTags.anchorTags
    }

    console.log(userPreferences)
    console.log(urls)
    */

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

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if(request.preferences) {
            console.log(request.preferences)
        }
    }
);
