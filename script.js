const video = document.getElementById('video');
const colorNameDisplay = document.getElementById('colorName');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');

let isDetecting = false;
let videoStream;

// Define color ranges in RGB
const colorRanges = {
    "Rojo": { r: [200, 255], g: [0, 100], b: [0, 100] },
    "Verde": { r: [0, 100], g: [200, 255], b: [0, 100] },
    "Azul": { r: [0, 100], g: [0, 100], b: [200, 255] },
    "Amarillo": { r: [200, 255], g: [200, 255], b: [0, 100] },
    "Naranja": { r: [200, 255], g: [100, 150], b: [0, 100] },
    "Morado": { r: [100, 150], g: [0, 100], b: [200, 255] },
    "Negro": { r: [0, 50], g: [0, 50], b: [0, 50] },
    "Blanco": { r: [200, 255], g: [200, 255], b: [200, 255] },
    "Gris": { r: [100, 200], g: [100, 200], b: [100, 200] },
    "Cyan": { r: [0, 100], g: [200, 255], b: [200, 255] },
    "Magenta": { r: [200, 255], g: [0, 100], b: [200, 255] },
    "Rosa": { r: [200, 255], g: [150, 255], b: [200, 255] },
    "Marrón": { r: [100, 150], g: [50, 100], b: [0, 50] },
    "Beige": { r: [200, 255], g: [200, 255], b: [150, 200] },
    "Turquesa": { r: [0, 100], g: [150, 255], b: [150, 255] },
    "Oliva": { r: [100, 150], g: [100, 150], b: [0, 100] },
    "Lavanda": { r: [150, 200], g: [100, 150], b: [200, 255] },
    "Coral": { r: [200, 255], g: [100, 150], b: [100, 150] },
    "Púrpura": { r: [100, 150], g: [0, 50], b: [100, 150] },
    "Dorado": { r: [200, 255], g: [150, 200], b: [0, 50] },
    "Plateado": { r: [200, 255], g: [200, 200], b: [200, 255] },
    "Café": { r: [100, 150], g: [50, 100], b: [0, 50] },
    "Navy": { r: [0, 50], g: [0, 50], b: [100, 255] },
    "Verde Claro": { r: [100, 150], g: [200, 255], b: [100, 150] },
    "Verde Oliva Claro": { r: [100, 150], g: [150, 200], b: [0, 100] },
    "Gris Claro": { r: [150, 200], g: [150, 200], b: [150, 200] },
    "Gris Oscuro": { r: [50, 100], g: [50, 100], b: [50, 100] },
    "Verde Pastel": { r: [150, 200], g: [255, 255], b: [150, 200] },
    "Azul Pastel": { r: [150, 200], g: [150, 200], b: [255, 255] },
    "Rosa Pastel": { r: [200, 255], g: [150, 200], b: [200, 255] },
    "Amarillo Pastel": { r: [200, 255], g: [255, 255], b: [150, 200] },
    "Naranja Pastel": { r: [200, 255], g: [150, 200], b: [100, 150] },
    "Rojo Pastel": { r: [200, 255], g: [100, 150], b: [150, 200] },
    "Azul Claro": { r: [100, 150], g: [150, 200], b: [200, 255] },
    "Verde Menta": { r: [150, 200], g: [255, 255], b: [200, 255] },
    "Cyan Claro": { r: [0, 100], g: [200, 255], b: [200, 255] },
    "Magenta Claro": { r: [200, 255], g: [0, 100], b: [200, 255] },
    "Lavanda Claro": { r: [150, 200], g: [100, 150], b: [200, 255] },
    "Púrpura Claro": { r: [150, 200], g: [0, 100], b: [200, 255] },
};

// Start video stream
startButton.addEventListener('click', () => {
    if (!isDetecting) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                videoStream = stream;
                video.srcObject = stream;
                video.play();
                isDetecting = true;
                detectColor();
            })
            .catch(err => {
                console.error("Error accessing webcam: ", err);
            });
    }
});

// Stop video stream
stopButton.addEventListener('click', () => {
    if (isDetecting) {
        videoStream.getTracks().forEach(track => track.stop());
        video.srcObject = null;
        isDetecting = false;
        colorNameDisplay.textContent = "Color: Ninguno";
    }
});

// Function to detect color
function detectColor() {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    setInterval(() => {
        if (isDetecting) {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const frame = context.getImageData(0, 0, canvas.width, canvas.height);
            const pixel = frame.data;

            // Get the pixel color at the center of the video
            const x = Math.floor(canvas.width / 2);
            const y = Math.floor(canvas.height / 2);
            const index = (y * canvas.width + x) * 4;

            const r = pixel[index];
            const g = pixel[index + 1];
            const b = pixel[index + 2];

            const colorName = getColorName(r, g, b);
            colorNameDisplay.textContent = `Color: ${colorName}`;
        }
    }, 100);
}

// Function to get color name based on RGB values
function getColorName(r, g, b) {
    for (const [name, range] of Object.entries(colorRanges)) {
        if (r >= range.r[0] && r <= range.r[1] &&
            g >= range.g[0] && g <= range.g[1] &&
            b >= range.b[0] && b <= range.b[1]) {
            return name;
        }
    }
    return "Desconocido";
}