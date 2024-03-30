from flask import Flask, render_template_string, request
from PyAccessPoint import pyaccesspoint
import urllib
import os
from write import writeTag

wifiApp = Flask("wifi")
spotiApp = Flask("spotipi")
access_point = pyaccesspoint.AccessPoint(ssid="SpotiPi Setup")


@wifiApp.route("/")
def index():
    return render_template_string(
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpotiPi</title>
</head>
<body>
    <form action="/wifi" method="post">
        <input type="text" name="ssid" placeholder="Wifi Name">
        <input type="text" name="password" placeholder="Password">
        <button type="submit">Connect</button>
    </form>
</body>
</html>
"""
    )


# wifi post with form data
@wifiApp.route("/wifi", methods=["POST"])
def wifi():
    ssid = request.form["ssid"]
    password = request.form["password"]
    print(ssid, password)
    access_point.stop()
    os.system("wpa_supplicant -B -c/etc/wpa_supplicant/wpa_supplicant.conf -i wlan0")
    connect_wifi(ssid, password)
    wifiApp.stop()
    start_spotipi()
    return "Connecting"


def connect_wifi(ssid, password):
    config_lines = [
        'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
        'update_config=1',
        'country=US',
        '\n',
        'network={',
        '\tssid="{}"'.format(ssid),
        '\tpsk="{}"'.format(password),
        '}'
        ]
    config = '\n'.join(config_lines)

    #give access and writing. may have to do this manually beforehand
    os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

    #writing to file
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
        wifi.write(config)

    print("Wifi config added. Refreshing configs")
    ## refresh configs
    os.popen("sudo wpa_cli -i wlan0 reconfigure")


@spotiApp.route("/")
def index():
    return render_template_string(
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpotiPi</title>
</head>
<body>
    <form action="/write" method="post">
        <input type="text" name="link" placeholder="Spotify Link">
        <button type="submit">Write</button>
    </form>
</body>
</html>
"""
    )

@spotiApp.route("/write", methods=["POST"])
def wifi():
    link = request.form["link"]
    print(link)
    writeTag(link)
    return "Written"


def start_spotipi():
    spotiApp.run(debug=False, host="0.0.0.0", port=4243)


def internet_on():
    try:
        urllib.request.urlopen("https://spotify.com", timeout=1)
        return True
    except:
        return False


if access_point.is_running():
    access_point.stop()


if not internet_on():
    access_point.start()
    wifiApp.run(debug=False, host="0.0.0.0", port=4242)
else:
    print("wifi connected")
    start_spotipi()

