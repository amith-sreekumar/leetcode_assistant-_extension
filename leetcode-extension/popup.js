document.getElementById("fetchBtn").addEventListener("click", getHints);

async function getHints() {
    //gets the current tab
    let tabs = await chrome.tabs.query({active: true, currentWindow: true});
    let tab= tabs[0];

    //starts a call to inject and run code inside another tab
    chrome.scripting.executeScript({
        target: {tabId: tab.id},
        //function that will run inside the leetcode page
        func: ()=>{
            let el = document.querySelector('[data-track-load="description_content"]') ||
                    document.querySelector('[data-cy="question-content"]') ||
                    document.querySelector('.question-content__JfgR');
            return el ? el.innerText : "No problem found";
        }
    }, async (results) => {        //runs after the script finishes executing leetcode tab
        let problem = results[0].result; 

        //send to your flask backend
        let res = await fetch("http://127.0.0.1:5000",{
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                problem: problem
            })
        });

        let data = await res.json();

        let output = document.getElementById("output");
        output.innerHTML="";

        data.keyword_results.forEach(hint => {
            let li = document.createElement("li");
            li.textContent = hint;
            output.appendChild(li);            
        });

    }
);
}