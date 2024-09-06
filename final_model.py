import tkinter as tk
from tkinter import messagebox  
# Import messagebox
# from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from vidgear.gears import CamGear

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video Path", "*.mp4")])
    if file_path:
        videoinput_person_detection(file_path)

def videoinput_person_detection(video_path):
    cap = cv2.VideoCapture(video_path)
    count = 0

    # Define font and color for text overlay
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_color = (0, 255, 0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (800, 600))
        bbox, label, conf = cv.detect_common_objects(frame, model='yolov3-tiny')
        frame = draw_bbox(frame, bbox, label, conf)

        c = label.count('person')
        text = f"Crowd Count: {c}"

        # Trigger message box if count exceeds 
        if c > 11:
            messagebox.showwarning("Warning", "Crowd count has exceeded!")

        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_x, text_y = 10, 30

        cv2.rectangle(frame, (text_x - 1, text_y - text_height - 2),
                      (text_x + text_width + 2, text_y + 2), (255, 255, 255), -1)
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

        cv2.imshow("FRAME: OBJECT DETECTION AND CROWD COUNTING video input", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def yt_person_detection(video_path):
    stream = CamGear(source=video_path, stream_mode=True, logging=True).start()
    count = 0

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_color = (0, 255, 0)

    while True:
        frame = stream.read()
        # count += 1
        # if count % 6 != 0:
        #     continue

        frame = cv2.resize(frame, (800, 600))
        bbox, label, conf = cv.detect_common_objects(frame, model='yolov3-tiny')
        frame = draw_bbox(frame, bbox, label, conf)

        c = label.count('person')
        text = f"Crowd Count: {c}"

        # Trigger message box if count exceeds 5
        if c > 9:
            messagebox.showwarning("Warning", "Crowd count has exceeded!")

        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_x, text_y = 10, 30

        cv2.rectangle(frame, (text_x - 1, text_y - text_height - 2),
                      (text_x + text_width + 2, text_y + 2), (255, 255, 255), -1)
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

        cv2.imshow("FRAME: LIVE OBJECT DETECTION AND CROWD COUNTING", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    stream.stop()
    cv2.destroyAllWindows()

def submit():
    given_url = textbox.get()
    yt_person_detection(given_url)

# Creating the Main Window
root = tk.Tk()
root.title("Object Detection and Crowd Monitoring")

# Window size
root.geometry("600x500")
root.configure(bg='#B5ACCA')

label = tk.Label(root, text="Upload the video path", font=('Arial', 16), bg='azure', fg='black', padx=20)
label.pack(pady=(20, 10))

button = tk.Button(root, text="Upload", bg='azure', fg='black', command=upload_file)
button.pack(pady=20)

label = tk.Label(root, text="Give the Live YT Stream URL", font=('Arial', 16), bg='azure', fg='black', padx=20)
label.pack(pady=(20, 10))

textbox = tk.Entry(root)
textbox.pack(pady=5)

submit_button = tk.Button(root, text="Upload", bg='azure', fg='black', command=submit)
submit_button.pack(pady=20)

root.mainloop()
