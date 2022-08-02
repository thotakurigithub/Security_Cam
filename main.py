import cv2
import winsound
cam = cv2.VideoCapture('http://root:root@192.168.10.204:80/mjpeg')
image = cv2.VideoCapture('http://root:root@192.168.10.204:80/mjpeg')
count = 0
#cam = cv2.VideoCapture('http://192.168.10.204/view/viewer_index.shtml?id=1')
#cam = cv2.VideoCapture(0)


while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)


    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
        cv2.imwrite("frame%d.jpg" % count, image)
        success, image = cam.read()
        print('Read a new frame: ', success)
        count += 1


    if cv2.waitKey(10) == ord('q'):
       break

    cv2.imshow('Security Cam', frame1)


