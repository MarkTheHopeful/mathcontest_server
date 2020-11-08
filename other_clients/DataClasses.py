class ServerState:
    def __init__(self, json):
        self.state = json["State"]
        self.api_ver = json['API version']
        self.db_manager = json['DB manager']
        self.gm_manager = json['Game manager']
        self.games_cnt = json['Amount of games']
        self.queue_len = json['Queue length']

    def __str__(self):
        return f"State: {self.state}, Api version: {self.api_ver}, DB manager: {self.db_manager},\n " \
               f"Game manager: {self.gm_manager}, Games: {self.games_cnt}, Queue: {self.queue_len}"


class UserInfo:
    def __init__(self, json):
        self.username = json['username']
        self.bio = json['bio']
        self.rank = json['rank']
        self.gm_history = json['history']

    def __str__(self):
        return f"User {self.username}\n" \
               f"Bio: {self.bio}\n" \
               f"Rank: {self.rank}\n" \
               f"Game history: {self.gm_history}\n"
