import glob
import os
import cv2
import send_email as se
from threading import Thread

def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


video = cv2.VideoCapture(0)

first_frame = None
status_list = []
count = 0

while True:
    status = 0
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    threshold_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    dil_frame = cv2.dilate(threshold_frame, None, iterations=2)
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            num = int(len(all_images)/2)
            image_export = all_images[num]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=se.send_email, args=(image_export, ))
        email_thread.daemon = True

        email_thread.start()

    cv2.imshow("Capture", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()

clean_folder()
