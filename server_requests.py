import requests


def write_parameters(num, params):
    user_d = {
        "user_number": num,
        "parameters": {
            "left": params[0],
            "right": params[1],
            "seat": params[2]
        },
        "current_user": "-"
    }

    requests.post(
        "http://192.168.100.3:8000/currentuser/",
        json=user_d
    )


def write_error(num):
    requests.post(
        "http://192.168.100.3:8000/currentuser/handle",
        json={"user_number": num}
    )


def get_parameters():
    return requests.get(
        "http://192.168.100.3:8000/currentuser/handle"
    ).json().values()


def get_current_user():
    return requests.get(
        "http://192.168.100.3:8000/currentuser/"
    ).json()
