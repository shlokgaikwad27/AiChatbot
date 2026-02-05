const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

// Add message function
function addMessage(text, cls) {
    const div = document.createElement("div");
    div.className = "message " + cls;
    div.innerHTML = text + `<div class='time'>${new Date().toLocaleTimeString()}</div>`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Typing animation
function showTyping() {
    const div = document.createElement("div");
    div.className = "message bot";
    div.id = "typing";
    div.innerText = "Bot is typing...";
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
    const t = document.getElementById("typing");
    if (t) t.remove();
}


// Enter & Shift+Enter logic
input.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        let msg = input.value.trim();
        if (!msg) return;

        addMessage("You: " + msg, "user");
        input.value = "";

        showTyping();

        fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: msg})
        })
        .then(res => res.json())
        .then(data => {
            removeTyping();
            addMessage("Bot: " + data.reply, "bot");
        });
    }
});
