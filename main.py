from loadJson import loadDirs

loadDirs()

from loadJson import labels, dump_parameters
from collector import collectPerson
from classifier import findPerson
from server_requests import write_error, \
    get_parameters, get_current_user


if __name__ == "__main__":
    user = get_current_user()

    if user["code"] == "0":
        errorCount = 0
        for i in range(3):
            res = findPerson(labels)

            if res == user["number"]: break
            else: errorCount += 1

        if errorCount == 3:
            write_error(user["number"])
            exit(0)
        else:
            dump_parameters(get_parameters())
            collectPerson(user["number"])
    else:
        collectPerson(user["number"])
