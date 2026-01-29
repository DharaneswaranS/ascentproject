let firstQuerySent = false;

function goToPassport() {
    window.location.href = "/passport-ui";
}

function uploadFile() {
    const file = document.getElementById("docFile").files[0];
    const formData = new FormData();
    formData.append("file", file);

    fetch("/upload", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            document.getElementById("status").innerText = data.message;
            if (data.status === "accepted") {
                document.getElementById("userInput").disabled = false;
                document.getElementById("sendBtn").disabled = false;
                addMessage("AI", "Document accepted. Start chatting.", "ai");
            }
        });
}

function sendQuery() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text) return;

    addMessage("You", text, "user");
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text })
    })
    .then(res => res.json())
    .then(data => {
        addMessage("AI", data.response, "ai");

        if (!firstQuerySent) {
            document.getElementById("downloadBtn").style.display = "inline-block";
            firstQuerySent = true;
        }
    });
}

function addMessage(sender, text, cls) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.className = `message ${cls}`;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function downloadPDF() {
    window.location.href = "/download";
}
