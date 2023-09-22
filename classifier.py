from os.path import join
from loadJson import directories
from keras.models import load_model
from numpy import expand_dims, argmax
from cv2 import CascadeClassifier, VideoCapture, cvtColor,\
    COLOR_BGR2GRAY, waitKey, destroyAllWindows, resize


INDENT = 20


def findPerson(labels):
    model = load_model(join(directories["model"], "model1.h5"))

    labels = {v: k for k, v in labels.items()}
    labelsFreq = []
    for _ in labels:
        labelsFreq.append(0)

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

        print(labelsFreq)

        if waitKey(20) and 0xFF == ord('q'):
            break

    cap.release()
    destroyAllWindows()

    print(labelsFreq)

    return labels[labelsFreq.index(max(labelsFreq))]
