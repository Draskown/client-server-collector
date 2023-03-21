from cv2 import CascadeClassifier, VideoCapture, cvtColor,\
    COLOR_BGR2GRAY, waitKey, destroyAllWindows, resize, \
    MORPH_OPEN, morphologyEx, LUT, bilateralFilter
from numpy import expand_dims, argmax
from keras.models import load_model
from loadJson import directories
from os.path import join
from numpy import average as npAvg, empty as npEmpty, \
    uint8, clip as npClip, ones as npOnes

model = load_model("Model/model1.h5")

labelsFreq = [0, 0, 0]

faceCascade = CascadeClassifier("Cascades/haarcascade_frontalface_alt.xml")

cap = VideoCapture(0)

i = 0
while i < 25:
    ret, frame = cap.read()

    faces = faceCascade.detectMultiScale(
        cvtColor(frame, COLOR_BGR2GRAY),
        scaleFactor=1.5,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:
        imgArray = frame[y:y + h, x:x + w]

        newArray = resize(imgArray, (64, 64)) / 255.0
        newArray = expand_dims(newArray, axis=0)

        result_1 = model.predict([newArray])
        result = argmax((result_1[0]))

        labelsFreq[result] += 1
        i += 1

    if waitKey(20) and 0xFF == ord('q'):
        break


cap.release()
destroyAllWindows()

print(labelsFreq)
