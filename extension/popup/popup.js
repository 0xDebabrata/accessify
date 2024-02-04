const key = "accessify-preferences"

function updatePreferencesUI() {
  const preferences = JSON.parse(localStorage.getItem(key) ?? "{}") 
  console.log(preferences)
  const images = document.querySelector("input[name='images']")
  const buttons = document.querySelector("input[name='buttons']")
  const anchors = document.querySelector("input[name='anchors']")
  const map = { images, buttons, anchors }

  for (const key of Object.keys(preferences)) {
    map[key].checked = preferences[key]
  }
}

function setPreferences(preferences) {
  localStorage.setItem(key, JSON.stringify(preferences))

  chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
    var activeTab = tabs[0];
    console.log(activeTab);
    chrome.tabs.sendMessage(activeTab.id, { preferences });
  });
}

function handleButtonClick() {
  const images = document.querySelector("input[name='images']")
  const buttons = document.querySelector("input[name='buttons']")
  const anchors = document.querySelector("input[name='anchors']")

  const value = {
    images: images.checked,
    anchors: anchors.checked,
    buttons: buttons.checked,
  }
  setPreferences(value)

  console.log("Preferences updated")
}

const button = document.getElementById("preferences-button")
button.addEventListener("click", handleButtonClick)

updatePreferencesUI()
