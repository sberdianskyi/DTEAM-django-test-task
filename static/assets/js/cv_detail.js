function initializeCVDetail(cvId, csrfToken) {
    document.getElementById("sendPdfForm").addEventListener("submit", function(e) {
        e.preventDefault();
        fetch(this.action, {
            method: "POST",
            body: new FormData(this),
            headers: {
                "X-CSRFToken": csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            Swal.fire({
                title: 'Success!',
                text: data.message,
                icon: 'success',
                confirmButtonText: 'OK'
            });
        })
        .catch(error => {
            Swal.fire({
                title: 'Error!',
                text: 'Error sending PDF',
                icon: 'error',
                confirmButtonText: 'OK'
            });
        });
    });

    document.getElementById('translateBtn').addEventListener('click', function() {
        const language = document.getElementById('languageSelect').value;
        const url = `/cv/${cvId}/translate/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `language=${language}`
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('translationResult').innerText = data.translated_text;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Translation failed');
        });
    });
}
