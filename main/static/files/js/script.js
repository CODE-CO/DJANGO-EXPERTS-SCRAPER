document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('scrape-form');
    const loadContentUrl = form.getAttribute('data-scrape-url');
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.getElementById('load-content-button').addEventListener('click', function(event) {
        event.preventDefault();
        loadContent(loadContentUrl);
    });

    function loadContent(url) {
        const selectedFilter = document.querySelector('input[name="filter"]:checked').value;

        var formData = new FormData();
        formData.append('filter', selectedFilter);
        formData.append('csrfmiddlewaretoken', csrfToken);

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            var contentDisplayDiv = document.getElementById('content-display');
            contentDisplayDiv.style.display = 'block'; // Ensure the content is displayed
            if (data.content) {
                displayContentSmoothly(data.content, contentDisplayDiv, selectedFilter);
            } else {
                contentDisplayDiv.innerText = data.error || 'Error loading content';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            var contentDisplayDiv = document.getElementById('content-display');
            contentDisplayDiv.innerText = 'An error occurred. Please try again.';
        });
    }

    function downloadFile(fileType, filter, delay = 0) {
        setTimeout(() => {
            const fileName = filter + (fileType === 'txt' ? '.txt' : '.vcf');
            const downloadUrl = `/static/files/txt/${fileName}`;

            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = downloadUrl;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(downloadUrl);
        }, delay);
    }

    function displayContentSmoothly(content, container, filter) {
        container.innerText = ''; // Clear previous content
        const lines = content.split('\n');
        let index = 0;
        const linesPerInterval = 20; // Number of lines to add per interval
        const interval = 50; // Interval in milliseconds
        function addNextLines() {
            if (index < lines.length) {
                let nextLines = '';
                for (let i = 0; i < linesPerInterval && index < lines.length; i++, index++) {
                    nextLines += lines[index] + '\n';
                }
                container.innerText += nextLines;
                container.scrollTop = container.scrollHeight; // Scroll to the bottom
                setTimeout(addNextLines, interval);
            } else {
                downloadFile('txt', filter); // Trigger text file download after all lines are displayed
                downloadFile('vcf', filter, 1500); // Trigger VCF file download 3 seconds later
            }
        }
        addNextLines();
    }
});
