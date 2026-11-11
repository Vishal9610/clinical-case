
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

        xraySection.hidden = !["CHEST_XRAY", "BOTH"].includes(type);
        ecgSection.hidden = !["ECG", "BOTH"].includes(type);
    }

    typeSelect.addEventListener("change", updateExaminationSections);
    updateExaminationSections();
});


// EXAMINATION IMAGE SELECTION AND PREVIEW
document.addEventListener("DOMContentLoaded", function () {
    const cameraInput = document.getElementById("cameraImages");
    const galleryInput = document.getElementById("galleryImages");
    const previewContainer = document.getElementById("examinationImagePreview");
    const message = document.getElementById("imageSelectionMessage");

    if (!galleryInput || !previewContainer || !message) {
        return;
    }

    let selectedImages = [];

    function renderImages() {
        previewContainer.replaceChildren();

        selectedImages.forEach(function (file, index) {
            const card = document.createElement("div");
            card.className = "content-card";

            const image = document.createElement("img");
            const imageUrl = URL.createObjectURL(file);

            image.src = imageUrl;
            image.alt = file.name;
            image.style.width = "100%";
            image.style.maxHeight = "220px";
            image.style.objectFit = "contain";

            image.addEventListener("load", function () {
                URL.revokeObjectURL(imageUrl);
            });

            const fileName = document.createElement("p");
            fileName.textContent = file.name;

            const fileSize = document.createElement("p");
            fileSize.textContent =
                (file.size / (1024 * 1024)).toFixed(2) + " MB";

            const removeButton = document.createElement("button");
            removeButton.type = "button";
            removeButton.textContent = "Remove Image";
            removeButton.className = "secondary-btn";

            removeButton.addEventListener("click", function () {
                selectedImages.splice(index, 1);
                syncSelectedFiles();
                renderImages();
            });

            card.append(image, fileName, fileSize, removeButton);
            previewContainer.appendChild(card);
        });

        message.textContent = selectedImages.length
            ? selectedImages.length + " image(s) selected."
            : "No images selected.";
    }

    function addImages(files) {
        const allowedTypes = ["image/jpeg", "image/png", "image/webp", "image/gif"];

        Array.from(files).forEach(function (file) {
            if (!allowedTypes.includes(file.type)) {
                alert(file.name + " is not a supported image format.");
                return;
            }

            if (file.size > 10 * 1024 * 1024) {
                alert(file.name + " exceeds the 10 MB per-image limit.");
                return;
            }

            const duplicate = selectedImages.some(function (existing) {
                return existing.name === file.name &&
                       existing.size === file.size &&
                       existing.lastModified === file.lastModified;
            });

            if (!duplicate) {
                selectedImages.push(file);
            }
        });

        syncSelectedFiles();
        renderImages();
    }

    function syncSelectedFiles() {
        const transfer = new DataTransfer();

        selectedImages.forEach(function (file) {
            transfer.items.add(file);
        });

        galleryInput.files = transfer.files;
    }

    galleryInput.addEventListener("change", function () {
        addImages(galleryInput.files);
    });

    const examinationForm = galleryInput.closest("form");

    if (examinationForm) {
        examinationForm.addEventListener("submit", function () {
            syncSelectedFiles();
        });
    }
});