import datetime as dt
import streamlit as st
import cv2


st.title("Video with date time")
start = st.button("Start Camera")

if start:
    st_img = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        clock = dt.datetime.now()
        date = clock.strftime("%d-%m-%Y")
        weekday = clock.strftime("%A")
        time = clock.strftime("%H:%M:%S")

        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.putText(img=frame, text=date, org=(50, 50),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5,
                    color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img=frame, text=weekday, org=(50, 75),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5,
                    color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img=frame, text=time, org=(50, 100),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5,
                    color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)

        st_img.image(frame)