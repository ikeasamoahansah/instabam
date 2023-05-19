const inputElement = document.getElementById('image-input');
const targetElement = document.getElementById('target-element');

// Event listener for the file input
inputElement.addEventListener('change', function (event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    // Event listener for FileReader's onload event
    reader.onload = function (e) {
        // Set the selected image as the background
        targetElement.style.backgroundImage = `url('${e.target.result}')`;
    };

    // Read the selected file as a data URL
    reader.readAsDataURL(file);
});


