chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  const activeTabUrl = tabs[0].url;
  getCurrentTabUrl(activeTabUrl);
});


let data;
async function getCurrentTabUrl(tabUrl) {
  const response = await fetch("http://127.0.0.1:5000/scrape", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scrape: tabUrl }),
  });

  data = response.json()
}

document.querySelector(".summarize-btn").addEventListener("click", ()=>{
  summarizeText(data)
});

async function summarizeText(text) {
  const response = await fetch("http://127.0.0.1:5000/openai", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({text: text}),
  });
  const data = await response.json();

  document.querySelector(".text").textContent = JSON.parse(data);
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
