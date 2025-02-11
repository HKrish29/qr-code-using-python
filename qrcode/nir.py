import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2  # For QR code scanning
import numpy as np

# Define function to create QR code
def createqr(*args):
    data = text_entry.get()
    if data:
        imge = qrcode.make(data)
        resized_img = imge.resize((280, 250))
        tkimage = ImageTk.PhotoImage(resized_img)
        qr_canvas.config(width=280, height=250)  # Set canvas size to match image
        qr_canvas.delete("all")
        qr_canvas.create_image(0, 0, anchor=tk.NW, image=tkimage)
        qr_canvas.image = tkimage  # Keep a reference to avoid garbage collection

# Define function to save QR code
def saveqr(*args):
    if hasattr(qr_canvas, 'image'):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                   filetypes=[("PNG files", "*.png"),
                                                              ("All files", "*.*")])
        if file_path:
            qr_img = qr_canvas.image._PhotoImage__photo.zoom(1, 1)  # Get the image
            qr_img.write(file_path, format="png")
            messagebox.showinfo("Saved", "QR code saved successfully!")
    else:
        messagebox.showwarning("Warning", "No QR code to save!")

# Define function to scan QR code using webcam
def scanqr(*args):
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        _, frame = cap.read()
        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            messagebox.showinfo("QR Code Data", f"Scanned QR code data: {data}")
            text_entry.delete(0, tk.END)  # Clear existing text
            text_entry.insert(0, data)  # Insert scanned data into text field
            break
        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Create main window
yas = tk.Tk()
yas.title("QR Code Generator & Scanner")
yas.geometry("300x380")
yas.config(bg="white")
yas.resizable(False, False)

# Create frames
frame1 = tk.Frame(yas, bd=2, relief=tk.RAISED)
frame1.place(x=10, y=0, width=280, height=250)

frame2 = tk.Frame(yas, bd=2, relief=tk.SUNKEN)
frame2.place(x=10, y=260, width=280, height=100)

# Initialize canvas
cover_img = ImageTk.PhotoImage(file="qr.jpg")   
qr_canvas = tk.Canvas(frame1, width=280, height=250)
qr_canvas.create_image(35, 20, anchor=tk.NW, image=cover_img)
qr_canvas.image = cover_img
qr_canvas.pack(fill=tk.BOTH)

# Text entry for QR code data
text_entry = ttk.Entry(frame2, width=30, justify=tk.CENTER)
text_entry.bind("<Return>", createqr)
text_entry.place(x=5, y=5)

# Create buttons
btn_1 = ttk.Button(frame2, text="Create", width=10, command=createqr)
btn_1.place(x=25, y=50)

btn_2 = ttk.Button(frame2, text="Save", width=10, command=saveqr)
btn_2.place(x=100, y=50)

btn_3 = ttk.Button(frame2, text="Exit", width=10, command=yas.quit)
btn_3.place(x=175, y=50)

btn_4 = ttk.Button(frame2, text="Scan QR", width=10, command=scanqr)
btn_4.place(x=100, y=80)

# Run the application
yas.mainloop()
