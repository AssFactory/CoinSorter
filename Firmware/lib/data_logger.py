import config

class DataLogger:
    def __init__(self):
        with open(self.filename, 'w') as f:
            f.write("Coin Sorting Data Log\n")
            f.write("Denomination,Count\n")

    def log_coin(self, denomination):
        with open(self.filename, 'a') as f:
            f.write(f"{denomination},1\n")