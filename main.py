from operator import ge
from flask import Flask, render_template_string, request, redirect
from PyAccessPoint import pyaccesspoint
import urllib
import os
import threading
from write import writeTag
import RPi.GPIO as GPIO
from mfrc522 import ExtendedMFRC522
import time
from spotify import (
    get_auth_domain,
    get_access_token,
    print_top,
    get_ip_address,
    play_test,
)


wifiApp = Flask("wifi")
spotiApp = Flask("spotipi")
access_point = pyaccesspoint.AccessPoint(ssid="SpotiPi Setup")

SPOTIFY_PORT = 80


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
        "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev",
        "update_config=1",
        "country=US",
        "\n",
        "network={",
        '\tssid="{}"'.format(ssid),
        '\tpsk="{}"'.format(password),
        "}",
    ]
    config = "\n".join(config_lines)

    # give access and writing. may have to do this manually beforehand
    os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

    # writing to file
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
    <button onclick="location.href='/spotify'">Spotify</button>
    <form action="/write" method="post">
        <input type="text" name="link" placeholder="Spotify Link">
        <button type="submit">Write</button>
    </form>
</body>
</html>
"""
    )


@spotiApp.route("/test")
def test():
    try:
        print_top()
        play_test()
    except:
        print("no top")
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
    testin
</body>
</html>
"""
    )


@spotiApp.route("/write", methods=["POST"])
def wifi():
    global writing
    link = request.form["link"]
    print(link)
    writing = True
    writeTag(link)
    writing = False
    return "Written"


@spotiApp.route("/spotify")
def spotify():
    return redirect(
        get_auth_domain(f"http://{get_ip_address()}:{SPOTIFY_PORT}/spotify-callback")
    )


@spotiApp.route("/spotify-callback")
def spotifycallback():
    code = request.args.get("code")
    get_access_token(code)
    return redirect("/")


def reader(writing):
    reader = ExtendedMFRC522()
    reader.READER.logger.disabled = True
    try:
        while True:
            print("test", writing)
            time.sleep(1)
            while writing:
                pass
            id, text = reader.read_no_block()
            if id:
                text = urllib.parse.unquote(text)
                if text.startswith("https://open.spotify.com/"):
                    print(text)
                    play_test(text.split("/")[-1].split("?")[0])
                else:
                    print("not a spotify link: ", text)
    finally:
        print("cleaning up reader")
        GPIO.cleanup()


def start_spotipi():
    threading.Thread(target=reader, args=(writing,)).start()
    spotiApp.run(debug=False, host="0.0.0.0", port=SPOTIFY_PORT)


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
    writing = False
    print("wifi connected")
    start_spotipi()
