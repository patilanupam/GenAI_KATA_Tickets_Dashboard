let resultJson = {};

// Handle file upload + backend call
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("transcriptFile");
    if (!fileInput.files.length) {
        alert("Please select a transcript file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const res = await fetch("/process", { method: "POST", body: formData });

        if (!res.ok) {
            const err = await res.json();
            alert("Error: " + (err.error || "Something went wrong"));
            return;
        }

        const response = await res.json();
        resultJson = response.minutes || response;

        // Show Summary tab by default
        updateTabContent("executive_summary");

    } catch (error) {
        console.error(error);
        alert("Error connecting to backend.");
    }
});

// Tab switching
document.querySelectorAll(".tab").forEach(tab => {
    tab.addEventListener("click", () => {
        document.querySelector(".tab.active").classList.remove("active");
        tab.classList.add("active");
        updateTabContent(tab.dataset.tab);
    });
});

// Update content area based on selected tab
function updateTabContent(tab) {
    const content = resultJson[tab];

    const tabContentEl = document.getElementById("tabContent");
    if (!content || (Array.isArray(content) && content.length === 0)) {
        tabContentEl.innerText = "No data available.";
        return;
    }

    // Format based on content type
    if (Array.isArray(content)) {
        if (content.length > 0 && typeof content[0] === 'object') {
            // Array of objects - format nicely
            let html = '';
            content.forEach((item, index) => {
                html += `<div style="margin-bottom: 15px; padding: 10px; background: #f8f9fa; border-radius: 5px;">`;
                html += `<strong>#${index + 1}</strong><br>`;
                for (const [key, value] of Object.entries(item)) {
                    if (value !== null && value !== undefined) {
                        const displayKey = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
                        html += `<strong>${displayKey}:</strong> ${value}<br>`;
                    }
                }
                html += `</div>`;
            });
            tabContentEl.innerHTML = html;
        } else {
            // Array of strings
            tabContentEl.innerHTML = content.map(item => "• " + item).join("<br>");
        }
    } else if (typeof content === 'object') {
        // Single object
        let html = '';
        for (const [key, value] of Object.entries(content)) {
            if (value !== null && value !== undefined) {
                const displayKey = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
                html += `<strong>${displayKey}:</strong> ${value}<br>`;
            }
        }
        tabContentEl.innerHTML = html;
    } else {
        // Simple value
        tabContentEl.innerText = content;
    }
}

// Copy JSON to clipboard
document.getElementById("copyJson").onclick = () => {
    if (!resultJson || Object.keys(resultJson).length === 0) {
        alert("No data to copy.");
        return;
    }
    navigator.clipboard.writeText(JSON.stringify(resultJson, null, 2));
    alert("Copied JSON!");
};

// Download JSON file
document.getElementById("downloadJson").onclick = () => {
    if (!resultJson || Object.keys(resultJson).length === 0) {
        alert("No data to download.");
        return;
    }

    const blob = new Blob([JSON.stringify(resultJson, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "clarifymeet_output.json";
    a.click();
};

// Clear screen and reset data
document.getElementById("clearScreen").onclick = () => {
    resultJson = {};
    document.getElementById("tabContent").innerText = "No data generated yet.";
    document.querySelectorAll(".tab").forEach(tab => tab.classList.remove("active"));
    document.querySelector(".tab[data-tab='executive_summary']").classList.add("active");
};
 