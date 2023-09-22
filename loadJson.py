from os import walk
from json import load, dump
from os.path import join as pathJoin, dirname, \
    abspath, basename

labels = {}
directories = {}


def loadDirs():
    global labels, directories
    baseDir = dirname(abspath(__file__))
    modelDir = pathJoin(baseDir, "Model")
    imageDir = pathJoin(baseDir, "Images")
    trainDir = pathJoin(imageDir, "Train")
    testDir = pathJoin(imageDir, "Test")

    with open(pathJoin(modelDir, "mainInfo.json"), "r") as f:
        a = load(f)

    directories = {"base": baseDir,
                   "model": modelDir,
                   "images": imageDir,
                   "train": trainDir,
                   "test": testDir}

    currentId = 0
    for root, _, files in walk(directories["images"]):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                label = basename(root).replace(" ", "-").lower()
                if label not in labels:
                    labels[label] = currentId
                    currentId += 1

    a["directories"] = directories
    a["labels"] = labels

    with open(pathJoin(modelDir, "mainInfo.json"), "w") as f:
        dump(a, f, ensure_ascii=False, indent=4)


def dump_parameters(params=None):
    if "model" not in directories or \
            params is None:
        params = [0, 0, 0]

    v = list(map(int, params))

    with open(pathJoin(directories["model"], "mainInfo.json"), "r") as f:
        a = load(f)
        a["parameters"] = {"left": v[0], "right": v[1], "seat": v[2]}

    with open(pathJoin(directories["model"], "mainInfo.json"), "w") as f:
        dump(a, f, ensure_ascii=False, indent=4)


def pull_parameters():
    if "model" in directories:
        with open(pathJoin(directories["model"], "mainInfo.json"), "r") as f:
            return list(load(f)["parameters"].values())
    else:
        return [0, 0, 0]
