let firstQuerySent = false;

function uploadFile() {
    const file = document.getElementById("docFile").files[0];
    const formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("status").innerText = data.message;

        if (data.status === "accepted") {
            document.getElementById("userInput").disabled = false;
            document.getElementById("sendBtn").disabled = false;
            addMessage("AI", "Document accepted. You can start chatting.", "ai");
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

        // ✅ SHOW DOWNLOAD BUTTON AFTER FIRST QUERY
        if (!firstQuerySent) {
            const btn = document.getElementById("downloadBtn");
            btn.style.display = "inline-block";   // safer than hidden
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
