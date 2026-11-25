function verifyPassport() {
    const file = document.getElementById("passportFile").files[0];
    if (!file) {
        alert("Please upload a passport file");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("/passport", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            const result = document.getElementById("result");
            result.classList.remove("hidden");

            if (data.status !== "SUCCESS") {
                result.className = "result status-invalid";
                result.innerHTML = "❌ Verification failed";
                return;
            }

            const p = data.passport_data;
            result.className = `result ${data.valid ? "status-valid" : "status-invalid"}`;

            result.innerHTML = `
                <b>Name:</b> ${p.given_names} ${p.surname}<br>
                <b>Passport No:</b> ${p.passport_number}<br>
                <b>Nationality:</b> ${p.nationality}<br>
                <b>DOB:</b> ${p.date_of_birth}<br>
                <b>Expiry:</b> ${p.expiry_date}<br><br>

                <span class="badge ${data.photo_present ? "ok" : "fail"}">
                    Photo: ${data.photo_present ? "Present" : "Missing"}
                </span>

                <span class="badge ${data.signature_present ? "ok" : "fail"}">
                    Signature: ${data.signature_present ? "Present" : "Missing"}
                </span>

                <h3>${data.valid ? "✅ PASSPORT VALID" : "❌ PASSPORT INVALID"}</h3>
            `;
        });
}
