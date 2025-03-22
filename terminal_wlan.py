from network import WLAN, STA_IF
from time import ticks_ms
from wlan_config import SAVED_NETWORKS

class TermialWLAN:
    def __init__(self) -> None:
        self._wlan = WLAN(STA_IF)
        self._wlan.active(True)
        self.lastReconnectTry = 0
        self.timeBetweenReconnects = 500
        self.reconnectAttempt = 0
        self.attemptsPerNetwork = 10
        self.currNetworkIndex = 0
        self.isTryingToConnect = False

    def process(self): 
        if (ticks_ms() - self.lastReconnectTry) >= self.timeBetweenReconnects:
            self.lastReconnectTry = ticks_ms()
            if not self._wlan.isconnected(): 
                self.isTryingToConnect = True
                if self.reconnectAttempt >= self.attemptsPerNetwork: 
                    self.currNetworkIndex += 1
                    self.reconnectAttempt = 0

                if self.currNetworkIndex >= len(SAVED_NETWORKS):
                    self.currNetworkIndex = 0

                if self.reconnectAttempt == 0:
                    self._wlan.connect(SAVED_NETWORKS[self.currNetworkIndex]["SSID"], SAVED_NETWORKS[self.currNetworkIndex]["PWD"])
                    
                self.reconnectAttempt += 1
            else:
                self.isTryingToConnect = False
                self.reconnectAttempt = 0

    