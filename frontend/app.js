let resultJson = {};

// Handle file upload + backend call
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("transcriptFile");

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const res = await fetch("/process", {
        method: "POST",
        body: formData
    });

    resultJson = await res.json();
    updateTabContent("summary");
});

// Tab switching
document.querySelectorAll(".tab").forEach(tab => {
    tab.addEventListener("click", () => {
        document.querySelector(".tab.active").classList.remove("active");
        tab.classList.add("active");
        updateTabContent(tab.dataset.tab);
    });
});

// Update content area
function updateTabContent(tab) {
    const content = resultJson[tab] || "No data generated yet.";

    document.getElementById("tabContent").innerText =
        Array.isArray(content)
            ? content.map(i => "• " + i).join("\n")
            : content;
}

// Copy JSON
document.getElementById("copyJson").onclick = () => {
    navigator.clipboard.writeText(JSON.stringify(resultJson, null, 2));
    alert("Copied JSON!");
};

// Download JSON
document.getElementById("downloadJson").onclick = () => {
    const blob = new Blob(
        [JSON.stringify(resultJson, null, 2)],
        { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "clarifymeet_output.json";
    a.click();
};

// Clear screen
document.getElementById("clearScreen").onclick = () => {
    resultJson = {};
    document.getElementById("tabContent").innerText = "";
};
