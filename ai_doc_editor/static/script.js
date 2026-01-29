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
            document.getElementById("chatBox").style.display = "block";
        }
    });
}

function sendQuery() {
    const input = document.getElementById("userInput").value;

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({query: input})
    })
    .then(res => res.json())
    .then(data => {
        const chat = document.getElementById("chat");
        chat.innerHTML += `<p><b>You:</b> ${input}</p>`;
        chat.innerHTML += `<p><b>AI:</b> ${data.response}</p>`;
        document.getElementById("userInput").value = "";
    });
}
function downloadPDF() {
    window.location.href = "/download";
}

