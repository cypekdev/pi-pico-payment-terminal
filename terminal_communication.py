from urequests import post, get
from wlan_config import URL, SECRET
from time import ticks_ms

class TerminalCommunication:
    TIMEOUT_VALUE = 2

    def __init__(self):
        self._headers = {
            "Authorization": SECRET,
            "User-Agent": "RaspberryPiPico"
        }

    def check_server(self):
        try: 
            resp = get(f"{URL}/terminal-api/server-status.php", headers = self._headers, timeout = self.TIMEOUT_VALUE)
            parsedResp = resp.json()
            resp.close()
            return parsedResp
        except Exception as e:
            return e

    def card_transfer(self, cardId: str, amount: float, pin: int|None = None):
        body = {
            "cardId": cardId,
            "ammount": amount,
            "pin": pin            
        }

        try:
            resp = post(f"{URL}/terminal-api/card-transfer.php", json = body, headers = self._headers, timeout = self.TIMEOUT_VALUE)
            parsedResp = resp.json()
            resp.close()
            return parsedResp
        except Exception as e:
            return e
        
    def blik_transfer(self, blik_code: int, amount: float):
        body = {
            "blikCode": blik_code,
            "ammount": amount,
        }
                
        try:
            resp = post(f"{URL}/terminal-api/blik-transfer.php", json = body, headers = self._headers, timeout = self.TIMEOUT_VALUE)
            parsedResp = resp.json()
            resp.close()
            return parsedResp
        except Exception as e:
            return e
        

if __name__ == "__main__":
    tc = TerminalCommunication()
    start_time = ticks_ms()
    print(tc.blik_transfer(999999, 99.99))
    print(ticks_ms() - start_time)