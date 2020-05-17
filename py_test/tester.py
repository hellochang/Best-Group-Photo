import cv2
import requests

cap = cv2.VideoCapture(0)
URL = 'https://ruhacks-277400.nn.r.appspot.com/'
#URL = 'http://127.0.0.1:5000/'


try:
    while(True):
        ret, frame = cap.read()
        imgdata = cv2.imencode('.jpg', frame)[1].tostring()
        files = {'image':imgdata}
        response = requests.post(URL, files=files)
        print(response.text)
        cv2.putText(frame, response.text, (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('tester', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt as e:
    cap.release()
    cv2.destroyAllWindows()
    exit()
cap.release()
cv2.destroyAllWindows()
