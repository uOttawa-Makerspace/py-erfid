import nfc
import time
import requests
from gpiozero import LED
import netifaces
from threading import Thread
import sys

green = LED(23)
red = LED(24)
yellow = LED(25)

green.on()
yellow.on()
red.on()

clf = nfc.ContactlessFrontend()
mac = netifaces.ifaddresses("wlan0")[netifaces.AF_LINK][0]["addr"]
print "MAC address: " + mac

try:
  clf.open('tty:S0:pn532')
except:
  print(sys.exc_info()[0])
  yellow.on()
  red.on()

print "Connected to RFID board"

thread = None
working = False

green.off()
yellow.off()
red.off()

def start_blink():
  global thread
  thread = Thread(target=blink)
  thread.start()

def stop_blink():
  global thread
  global working
  working = False

  if thread:
    thread.join()

def blink():
  global working
  working = True

  while working:
    green.on()
    yellow.on()
    red.on()
    time.sleep(0.05)
    green.off()
    yellow.off()
    red.off()
    time.sleep(0.05)

def success():
  for i in range(3):
    green.on()
    time.sleep(0.25)
    green.off()
    time.sleep(0.25)

def error():
  for i in range(3):
    red.on()
    time.sleep(0.25)
    red.off()
    time.sleep(0.25)

def warning():
  for i in range(3):
    yellow.on()
    time.sleep(0.25)
    yellow.off()
    time.sleep(0.25)

while True:
  tag = clf.connect(rdwr={'on-connect': lambda tag: False})

  if tag:
    try:
      id = tag.identifier.encode('HEX').upper()
      data = {"rfid": id, "mac_address": mac + "\n"} # newline for backwards compat with ruby version
      start_blink()
      res = requests.post("https://makerepo.com/rfid/card_number", json=data, headers={"Content-Type": "application/json"})
      stop_blink()

      if not res or res.status_code != 200:
        error()
        continue

      obj = res.json()

      if obj["success"] == "RFID sign in":
        success()
        continue
      elif obj["success"] == "RFID sign out":
        warning()
        continue

      # fallback to error
      error()
    except:
      print(sys.exc_info()[0])
      stop_blink()
      error()

  time.sleep(0.5)

clf.close()
