let selectedBot = "Medical_Bot";

function selectBot() {
    selectedBot = document.getElementById("botSelect").value;
}

function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") return;

    addMessage("You", userInput);

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        addMessage(selectedBot, data.response);
    });

    document.getElementById("userInput").value = "";
}

function addMessage(sender, message) {
    const chat = document.getElementById("chat");
    const messageDiv = document.createElement("div");
    messageDiv.textContent = `${sender}: ${message}`;
    chat.appendChild(messageDiv);
    chat.scrollTop = chat.scrollHeight;
}
