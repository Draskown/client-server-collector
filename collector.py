from os import mkdir, walk
from os.path import join as pathJoin, \
     exists as pathExists
from cv2 import CascadeClassifier, cvtColor, \
    COLOR_BGR2GRAY, imwrite, VideoCapture,\
    waitKey, destroyAllWindows
from server_requests import write_parameters
from loadJson import directories, pull_parameters
from threading import Thread
from time import time, sleep
from faces import train

stop = False
frame = []


def wait4command():
    print("Print \'s\' to stop operating")
    s = input()
    if s == "s":
        global stop
        stop = True
    else:
        wait4command()


def collect(number):
    if not pathExists(directories["train"]):
        mkdir(directories["train"])

    if not pathExists(directories["test"]):
        mkdir(directories["test"])

    labelTrainDir = pathJoin(directories["train"], number)
    labelTestDir = pathJoin(directories["test"], number)

    if not pathExists(labelTrainDir):
        mkdir(labelTrainDir)

    if not pathExists(labelTestDir):
        mkdir(labelTestDir)

    faceCascade = CascadeClassifier("Cascades/haarcascade_frontalface_alt2.xml")

    indexTest = find_last_index(labelTestDir)
    indexTrain = find_last_index(labelTrainDir)

    commonIndex = indexTest + indexTrain + 1

    while True:
        if len(frame) != 0:
            startTime = time()

            facesCascade = faceCascade.detectMultiScale(
                cvtColor(frame, COLOR_BGR2GRAY),
                scaleFactor=1.5,
                minNeighbors=5
            )

            if len(facesCascade) != 0:
                maxArea = (facesCascade[0, 0] + facesCascade[0, 2]) *\
                          (facesCascade[0, 1] + facesCascade[0, 3])
                for (x, y, w, h) in facesCascade:
                    area = (x + w) * (y + h)
                    if area > maxArea:
                        maxArea = area

                for (x, y, w, h) in facesCascade:
                    if (x + w) * (y + h) == maxArea:
                        roi = frame[y:y + h, x:x + w]

                        if commonIndex > 250:
                            commonIndex = 0
                        else:
                            commonIndex += 1

                        if commonIndex % 4 == 0:
                            imwrite(pathJoin(labelTestDir, str(indexTest) + ".png"), roi)
                            indexTest += 1
                        else:
                            imwrite(pathJoin(labelTrainDir, str(indexTrain) + ".png"), roi)
                            indexTrain += 1

                        print(str(commonIndex + 1) + " image(s) have been gathered.")

                sleep(1 - time() + startTime)

            if stop:
                break


def collectPerson(number):
    stopProgram = Thread(target=wait4command, daemon=True)
    collectImages = Thread(target=collect, args=(number, ), daemon=True)
    collectImages.start()
    stopProgram.start()

    cap = VideoCapture(0)

    while True:
        global frame, stop

        ret, frame = cap.read()
        if waitKey(20) and stop or \
                waitKey(20) and 0xFF == ord('q'):
            stop = True
            break

    cap.release()
    destroyAllWindows()
    train()

    write_parameters(number, pull_parameters())

    exit(0)


def find_last_index(directory):
    index = -1
    for _, _, files in walk(directory):
        for file in files:
            if (file.endswith("png") or file.endswith("jpg")) and \
                    index == -1:
                index = int(file[:len(file) - 4])

            if file.endswith("png") or file.endswith("jpg"):
                fileNum = int(file[:len(file) - 4])
                if fileNum > index:
                    index = fileNum

    return index
