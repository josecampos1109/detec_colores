import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk
import os

# Create a directory to save detected images
if not os.path.exists('detected_images'):
    os.makedirs('detected_images')

# Function to extract color range
def extractColor(frame, r):
    imagenNueva = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    altura, ancho = imagenNueva.shape[:2]
    H, S, V = [], [], []

    for i in range(altura):
        for j in range(ancho):
            pixel = imagenNueva[i, j]
            H.append(pixel[0])
            S.append(pixel[1])
            V.append(pixel[2])

    hMin, hMax = min(H), max(H)
    sMin, sMax = min(S), max(S)
    vMin, vMax = min(V), max(V)

    bajo = np.array([hMin, sMin, vMin], np.uint8)
    alto = np.array([hMax, sMax, vMax], np.uint8)
    return bajo, alto

# Function to start color detection
def start_detection():
    global conteo
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("Color Tracking", cv2.WINDOW_NORMAL)

    conteo = 0
    while conteo < 300:  # Capture 300 images
        res, frame = cam.read()
        if not res:
            break

        masterCopy = frame.copy()
        frameHSV = cv2.cvtColor(masterCopy, cv2.COLOR_BGR2HSV)

        if conteo == 10:
            roi = cv2.selectROI("Color Tracking", masterCopy)
            global bajo, alto
            bajo, alto = extractColor(frameHSV, roi)

        try:
            mask = cv2.inRange(frameHSV, bajo, alto)
            kernel = np.ones((3, 3), "uint8")
            mask = cv2.dilate(mask, kernel)
            contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contornos:
                area = cv2.contourArea(contornos[-1])
                if area > 100:
                    x, y, w, h = cv2.boundingRect(contornos[-1])
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Color detected", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

                    # Save the detected image
                    detected_image_path = f'detected_images/detected_{conteo}.png'
                    cv2.imwrite(detected_image_path, frame)
                    print(f"Saved detected image: {detected_image_path}")

        except Exception as e:
            print(f"Error: {e}")

        conteo += 1
        cv2.imshow("Color Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    print("Detection completed. Captured 300 images.")

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Color Detection")

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12), padding=10)

    label = ttk.Label(root, text="Press the button to start color detection", font=('Helvetica', 14))
    label.pack(pady=20)

    start_button = ttk.Button(root, text="Start Detection", command=start_detection)
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()