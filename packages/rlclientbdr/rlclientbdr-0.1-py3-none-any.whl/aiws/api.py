import requests

HOSTNAME = "192.168.3.9"
PORT = "80"
SERVER = "http://" + HOSTNAME + ":" + PORT + '/rl'


class RLClient:
    def __init__(self, name, password):
        self.TEAM_NAME = name
        self.TEAM_PASSWORD = password

    @staticmethod
    def validate_ids(run_id, request_number):
        if run_id < 0:
            raise ValueError("run_id has an invalid value of {}".format(run_id))

        if request_number < 0 or request_number > 9999:
            raise ValueError("request_number has an invalid value of {}".format(request_number))

    def get_context(self, run_id, request_number):
        self.validate_ids(run_id, request_number)

        params = {
            "team_id": self.TEAM_NAME,
            "team_password": self.TEAM_PASSWORD,
            "run_id": run_id,
            "request_number": request_number
        }

        r = requests.get(SERVER + "/get_context", params=params)
        if not r.status_code == 200:
            print(r.text)
            raise Exception("Something went wrong, see message above.")
        else:
            return r.json()

    def serve_page(self, run_id, request_number, header, language, adtype, color, price):
        self.validate_ids(run_id, request_number)

        data = {
            "team_id": self.TEAM_NAME,
            "team_password": self.TEAM_PASSWORD,
            "run_id": run_id,
            "request_number": request_number,
            "header": header,
            "language": language,
            "adtype": adtype,
            "color": color,
            "price": price
        }

        r = requests.post(SERVER + "/serve_page", data=data)
        if not r.status_code == 200:
            print(r.text)
            raise Exception("Something went wrong, see message above.")
        else:
            return r.json()

    def reset_leaderboard(self):
        data = {
            "team_id": self.TEAM_NAME,
            "team_password": self.TEAM_PASSWORD
        }
        r = requests.post(SERVER + "/reset_leaderboard", data=data)
        if not r.status_code == 200:
            print(r.text)
            raise Exception("Something went wrong, see message above.")
        else:
            return r.json()
