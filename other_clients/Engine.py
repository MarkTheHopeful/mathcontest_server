import requests, json
from game.game_state import deserialize_game_state


class Engine:
    host = ""
    SERVER_REACHABLE = 1
    SERVER_WORKS = 2

    def send_request(self, request_line, j_payload=None):
        if j_payload is None:
            conn = requests.get(self.host + request_line)
        else:
            conn = requests.post(self.host + request_line, json=j_payload)

        resp = conn.text
        stringed_json = resp.replace("'", '"')
        datum = json.loads(stringed_json)
        return datum['code'], datum['state'], datum['data']

    def test_host(self):
        try:
            code, state, data = self.send_request("/api/v1/service/status")
        except requests.exceptions.ConnectionError:
            return 0
        return 1 + 2 * (code == 200)

    def __init__(self, host="http://127.0.0.1:5000"):
        self.host = host
