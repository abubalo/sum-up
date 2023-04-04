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

  data = await response.json()
}

document.querySelector(".summarize-btn").addEventListener("click", ()=>{
  summarizeText(data)
  if(!data){

    document.querySelector(".y").textContent = "no data to display"
  }else{
    document.querySelector(".y").textContent = data
  }
});

async function summarizeText(text) {
  const response = await fetch("http://127.0.0.1:5000/openai", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({text: text}), // Modified this line
  });
  const data = await response.json();

  if(!data){
    document.querySelector(".text").textContent = "There is not data to display"
  }else{
    document.querySelector(".text").textContent = data.choices[0].text
  }
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
