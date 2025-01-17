document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; 
    }

    async function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === "") return;

        appendMessage("user", userMessage);
        userInput.value = "";

        const response = await fetch("/get_response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_input: userMessage }),
        });

        const data = await response.json();
        appendMessage("bot", data.response);
    }

    sendBtn.addEventListener("click", sendMessage);

    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });

    appendMessage("bot", "How can I help you?");
});
