chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  const activeTabUrl = tabs[0].url;
  getCurrentTabUrl(activeTabUrl);
});

async function getCurrentTabUrl(tabUrl) {
  document.querySelector(".y").textContent = tabUrl;

  await fetch("http://127.0.0.1:5000/scrape", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({scrape: tabUrl}),
  });
}


async function summarizeText() {
  const summarizeButton = document.querySelector(".summarize-btn");

  summarizeButton.addEventListener("click", async ()=> {

    const response = await fetch("http://127.0.0.1:5000/openai");
    const data = await response.json()
    document.querySelector(".content").textContent = data
    console.log(data)
  })
}

// function copyToClipboard(texts){
//   texts.forEach(text => {
    
//   });
// }

// Add a click event listener to the close icon
document.querySelector(".close").addEventListener("click", function () {
  // Close the extension popup window
  window.close();
});
