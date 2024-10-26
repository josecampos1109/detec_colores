import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk
import os

# Define color ranges in HSV
color_ranges = {
    "Red": ([0, 100, 100], [10, 255, 255]),
    "Dark Red": ([0, 100, 50], [10, 255, 150]),
    "Light Red": ([0, 50, 200], [10, 255, 255]),
    "Green": ([40, 100, 100], [80, 255, 255]),
    "Dark Green": ([40, 50, 50], [80, 255, 150]),
    "Light Green": ([40, 100, 200], [80, 255, 255]),
    "Blue": ([100, 100, 100], [140, 255, 255]),
    "Dark Blue": ([100, 50, 50], [140, 255, 150]),
    "Light Blue": ([100, 100, 200], [140, 255, 255]),
    "Yellow": ([20, 100, 100], [40, 255, 255]),
    "Dark Yellow": ([20, 50, 50], [40, 255, 150]),
    "Light Yellow": ([20, 100, 200], [40, 255, 255]),
    "Orange": ([10, 100, 100], [20, 255, 255]),
    "Dark Orange": ([10, 50, 50], [20, 255, 150]),
    "Light Orange": ([10, 100, 200], [20, 255, 255]),
    "Purple": ([140, 100, 100], [160, 255, 255]),
    "Dark Purple": ([140, 50, 50], [160, 255, 150]),
    "Light Purple": ([140, 100, 200], [160, 255, 255]),
    "Pink": ([160, 100, 100], [180, 255, 255]),
    "Dark Pink": ([160, 50, 50], [180, 255, 150]),
    "Light Pink": ([160, 100, 200], [180, 255, 255]),
    "Brown": ([10, 100, 50], [20, 255, 150]),
    "Dark Brown": ([10, 50, 20], [20, 150, 100]),
    "Light Brown": ([10, 100, 100], [20, 255, 200]),
    "Cyan": ([80, 100, 100], [100, 255, 255]),
    "Dark Cyan": ([80, 50, 50], [100, 255, 150]),
    "Light Cyan": ([80, 100, 200], [100, 255, 255]),
    "Magenta": ([140, 100, 100], [160, 255, 255]),
    "Dark Magenta": ([140, 50, 50], [160, 255, 150]),
    "Light Magenta": ([140, 100, 200], [160, 255, 255]),
    "Gray": ([0, 0, 50], [180, 20, 200]),
    "Dark Gray": ([0, 0, 20], [180, 20, 100]),
    "Light Gray": ([0, 0, 100], [180, 20, 255]),
    "Olive": ([30, 100, 100], [60, 255, 150]),
    "Dark Olive": ([30, 50, 50], [60, 255, 100]),
    "Light Olive": ([30, 100, 200], [60, 255, 255]),
    "Teal": ([80, 100, 50], [100, 255, 150]),
    "Dark Teal": ([80, 50, 20], [100, 255, 100]),
    "Light Teal": ([80, 100, 200], [100, 255, 255]),
    "Lavender": ([140, 50, 200], [160, 255, 255]),
    "Dark Lavender": ([140, 20, 100], [160, 255, 150]),
    "Light Lavender": ([140, 100, 250], [160, 255, 255]),
    "Coral": ([0, 100, 200], [20, 255, 255]),
    "Dark Coral": ([0, 50, 100], [20, 255, 150]),
    "Light Coral": ([0, 100, 250], [20, 255, 255]),
    "Peach": ([10, 100, 200], [20, 255, 255]),
    "Dark Peach": ([10, 50, 100], [20, 255, 150]),
    "Light Peach": ([10, 100, 250], [20, 255, 255]),
    "Mint": ([80, 100, 200], [100, 255, 255]),
    "Dark Mint": ([80, 50, 100], [100, 255, 150]),
    "Light Mint": ([80, 100, 250], [100, 255, 255]),
}

# Function to classify color based on the image
def classify_color(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    for color_name, (lower, upper) in color_ranges.items():
        lower_np = np.array(lower, dtype=np.uint8)
        upper_np = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(hsv_image, lower_np, upper_np)
        if np.sum(mask) > 0:  # If the mask has any pixels
            return color_name
    return "Unknown"

# Function to start color classification
def start_classification():
    global running
    running = True
    classify_images()

# Function to stop color classification
def stop_classification():
    global running
    running = False

# Function to classify images in the detected_images folder
def classify_images():
    if not running:
        return

    detected_images_path = 'data_images'
    for filename in os.listdir(detected_images_path):
        if filename.endswith('.png'):
            image_path = os.path.join(detected_images_path, filename)
            image = cv2.imread(image_path)
            color_name = classify_color(image)
            print(f"Image: {filename}, Detected Color: {color_name}")
            # Display the detected color name in the GUI
            color_label.config(text=f"Detected Color: {color_name}")
            cv2.imshow("Image", image)
            cv2.waitKey(1000)  # Show each image for 1 second

    cv2.destroyAllWindows()

# Function to capture color from webcam and classify it
def capture_and_classify():
    global running
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while running:
        ret, frame = cam.read()
        if not ret:
            break

        color_name = classify_color(frame)
        color_label.config(text=f"Detected Color: {color_name}")

        cv2.imshow("Webcam Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

# GUI setup
def create_gui():
    global color_label
    root = tk.Tk()
    root.title("Color Classification")

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12), padding=10)

    label = ttk.Label(root, text="Color Classification from Detected Images", font=('Helvetica', 14))
    label.pack(pady=20)

    color_label = ttk.Label(root, text="Detected Color: None", font=('Helvetica', 14))
    color_label.pack(pady=10)

    start_button = ttk.Button(root, text="Iniciar Classification", command=lambda: [start_classification(), capture_and_classify()])
    start_button.pack(pady=10)

    stop_button = ttk.Button(root, text="Parar Classification", command=stop_classification)
    stop_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()