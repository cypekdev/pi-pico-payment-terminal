from urequests import post, get
from wlan_config import URL, SECRET

class TerminalCommunication:
    def __init__(self):
        self._headers = {
            "Authorization": SECRET,
            "User-Agent": "RaspberryPiPico"
        }

    def check_server(self):
        try: 
            resp = get(f"{URL}/terminal-api/server-status.php", headers = self._headers)
            parsedResp = resp.json()
            resp.close()
            return parsedResp
        except Exception as e:
            return e

    def card_transfer(self, cardId, ammount, pin = None):
        body = {
            "cardId": cardId,
            "ammount": ammount,
            "pin": pin            
        }

        try:
            resp = post(f"{URL}/terminal-api/card-transfer.php", json = body, headers = self._headers)
            parsedResp = resp.json()
            resp.close()
            return parsedResp
        except Exception as e:
            return e
        
    def blik_transfer(self, blik_code, ammount):
        body = {
            "blikCode": blik_code,
            "ammount": ammount,
        }
                
        try:
            resp = post(f"{URL}/terminal-api/blik-transfer.php", json = body, headers = self._headers)
            parsedResp = resp.json()
            resp.close()
            return parsedResp
        except Exception as e:
            return e