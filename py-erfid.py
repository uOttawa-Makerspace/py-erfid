import nfc
import time
import requests
from gpiozero import LED
import netifaces
from threading import Thread
import sys
import traceback
from signal import pause

class PyErfid:
  def __init__(self):
    self.green = LED(23)
    self.red = LED(24)
    self.yellow = LED(25)

    self.green.on()
    self.yellow.on()
    self.red.on()

    self.clf = nfc.ContactlessFrontend()
    self.mac = netifaces.ifaddresses("wlan0")[netifaces.AF_LINK][0]["addr"]
    print "MAC address: " + self.mac

    try:
      self.clf.open('tty:S0:pn532')
    except:
      traceback.print_exc()
      self.green.off()
      pause()
      exit()

    print "Connected to RFID board"

    self.thread = None
    self.working = False

    self.green.off()
    self.yellow.off()
    self.red.off()

  def start_blink(self):
    self.thread = Thread(target=self.run_blink)
    self.thread.start()

  def stop_blink(self):
    self.working = False

    if self.thread:
      self.thread.join()
      self.thread = None

  def run_blink(self):
    self.working = True

    while self.working:
      self.green.on()
      self.yellow.on()
      self.red.on()

      time.sleep(0.05)

      self.green.off()
      self.yellow.off()
      self.red.off()

      time.sleep(0.05)

  def success(self):
    for i in range(3):
      self.green.on()
      time.sleep(0.25)
      self.green.off()
      time.sleep(0.25)

  def error(self):
    for i in range(3):
      self.red.on()
      time.sleep(0.25)
      self.red.off()
      time.sleep(0.25)

  def warning(self):
    for i in range(3):
      self.yellow.on()
      time.sleep(0.25)
      self.yellow.off()
      time.sleep(0.25)

  def run(self):
    while True:
      try:
        tag = self.clf.connect(rdwr={'on-connect': lambda t: False})
      except:
        self.red.on()
        self.yellow.on()
        time.sleep(1)
        self.red.off()
        self.yellow.off()

      if tag:
        try:
          id = tag.identifier.encode('HEX').upper()
          data = {"rfid": id, "mac_address": self.mac + "\n"} # newline for backwards compat with ruby version
          self.start_blink()
          res = requests.post("https://makerepo.com/rfid/card_number", json=data, headers={"Content-Type": "application/json"})
          self.stop_blink()

          if not res or res.status_code != 200:
            self.error()
            continue

          obj = res.json()

          if obj["success"] == "RFID sign in":
            self.success()
            continue
          elif obj["success"] == "RFID sign out":
            self.warning()
            continue

          # fallback to error
          self.error()
        except:
          traceback.print_exc()
          self.stop_blink()
          self.error()

      time.sleep(0.5)

    clf.close()

if __name__ == "__main__":
  erfid = PyErfid()
  erfid.run()
