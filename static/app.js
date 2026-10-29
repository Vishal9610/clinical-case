
function showComingSoon() {
    const message = document.getElementById("actionMessage");

    if (message) {
        message.textContent =
            "This feature will be connected in the next development step.";
    }
}


document.addEventListener("DOMContentLoaded", function () {
    const typeSelect = document.getElementById("examination_type");
    const xraySection = document.getElementById("xraySection");
    const ecgSection = document.getElementById("ecgSection");

    if (!typeSelect || !xraySection || !ecgSection) {
        return;
    }

    function updateExaminationSections() {
        const type = typeSelect.value;

        xraySection.hidden = type === "ECG";
        ecgSection.hidden = type === "CHEST_XRAY";
    }

    typeSelect.addEventListener("change", updateExaminationSections);
    updateExaminationSections();
});
