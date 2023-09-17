import subprocess
import os
import re
from collections import namedtuple
import configparser


def get_windows_saved_ssids():
    """Mengembalikan dafter SSID yang disimpan di mesin windows menggunakan perintah netsh"""
    # dapatkan semua profil wifi yang disimpa di pc
    output = subprocess.check_output("netsh wlan show profiles").decode()
    ssids = []
    profiles = re.findall(r"all user profile\s(.*)", output)
    for profile in profiles:
        # untuk setiap SSID, hilangkan spasi dan titik dua
        ssid = profile.strip().strip(":").strip()
        # tambahkan ke daftar
        ssids.append(ssid)
    return ssids


# print(get_windows_saved_ssids())


def get_windows_saved_wifi_passwords(verbose=1):
    ssids = get_windows_saved_ssids()
    Profile = namedtuple("profile", ["ssid", "chipers", "key"])
    profiles = []
    for ssid in ssids:
        ssid_details = subprocess.check_output(
            f"""netsh show profile"{ssid}" key=clear"""
        ).decode()
        # mendapatkan sandi
        chipers = re.findall(r"chiper\s(.*)", ssid_details)
        # kosongkan spaces and colon
        chipers = "/".join([c.strip().strip(":").strip() for c in chipers])
        # mendapatkan wifi password
        key = re.findall(r"key content\s(.*)", ssid_details)
        # kosongkan spaces and colon
        try:
            key = key[0].strip().strip(":").strip()
        except IndexError:
            key = "none"
        profile = Profile(ssid=ssid, chipers=chipers, key=key)
        if verbose >= 1:
            print_windows_profile(profile)
        profiles.append(profile)
    return profiles


def print_windows_profile(profile):
    """mencetak lebih dari satu profil di windows"""
    print(f"{profile.ssid:25}{profile.chipers:15}{profile.key:50}")


def print_windows_profiles(verbose):
    """mencetak semua SSID yang diekstrak beserta key di windows"""
    print("SSID           CHIPER(S)     KEY")
    print("-" * 50)
    get_windows_saved_wifi_passwords(verbose)


# untuk print profile wifi
def print_profiles(verbose=1):
    if os.name == "nt":
        print_windows_profiles(verbose)


if __name__ == "__main__":
    print_profiles()
