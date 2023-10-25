let unique_token = localStorage.getItem('unique_token');

fetch('/get_user_token').then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json(); 
}).then(data => {
    if (data.status === "success" && data.token) {
        localStorage.setItem('unique_token', data.token);
    } else {
        console.error('Error fetching token:', data.message);
    }
}).catch(error => {
    console.error('There was a problem fetching the token:', error);
});

// Detect and replace
function findNodeWithClass(node, className) {
    if (node.nodeType !== 1) return null; 
    if (node.classList.contains(className)) {
        return node;
    }

    for (let child of node.childNodes) {
        const result = findNodeWithClass(child, className);
        if (result) return result;
    }

    return null;
}

function callback(mutationsList, observer) {
    for(let mutation of mutationsList) {
        if(mutation.addedNodes.length) {
          for (let node of mutation.addedNodes) {
              const targetNode = findNodeWithClass(node, 'challenge-desc');
              if (targetNode) {
                  targetNode.innerHTML = targetNode.innerHTML.replace("##unique_token##", localStorage.getItem('unique_token'));
              }
          }
        }
    }
}

const observer = new MutationObserver(callback);
const config = { childList: true, subtree: true };
observer.observe(document.body, config);
