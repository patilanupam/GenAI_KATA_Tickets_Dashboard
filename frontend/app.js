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

        resultJson = await res.json();

        // Show Summary tab by default
        updateTabContent("summary");

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
    if (!content) {
        tabContentEl.innerText = "No data generated yet.";
        return;
    }

    tabContentEl.innerText = Array.isArray(content)
        ? content.map(item => "• " + item).join("\n")
        : content;
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
    document.querySelector(".tab[data-tab='summary']").classList.add("active");
};
 