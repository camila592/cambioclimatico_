const fileInput = document.getElementById('fileInput');
const previewBox = document.getElementById('previewBox');
const previewImage = document.getElementById('previewImage');
const resultContainer = document.getElementById('resultContainer');

fileInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewBox.style.display = 'block'; // aquí mostramos el contenedor
            resultContainer.textContent = ''; // limpia resultado anterior
        }
        reader.readAsDataURL(file);
    }
});