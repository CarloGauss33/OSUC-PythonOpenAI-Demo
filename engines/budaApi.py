import requests

class BudaAPI:
    def __init__(self) -> None:
        self.base_url = "https://www.buda.com/api/v2/markets"

    def get_bitcoin_price(self):
        bitcoin_url = f"{self.base_url}/btc-clp/ticker"
        response = requests.get(bitcoin_url).json()['ticker']['last_price']
        return ''.join(response)
