# py-erfid
Super simple RFID sign in/sign out system

## Installation
1. Disable serial communication:
   * Launch raspi-config `sudo raspi-config`
   * Select `6. Interfacing Options`, then `P6. Serial.`
   * Select "No" for both "Would you like a login shell to be accessible over Serial?" and "Would you like the serial port hardware to be enabled?".
   * If you are prompted to reboot the Pi after saving, select "No".
   * Set `enable_uart=1` at the bottom of /boot/config.txt (add that line if it is not there).
   * Reboot (`sudo reboot`).

2. Install git, ntp, and pip if not already done:
   ```
   sudo apt install git ntp python-pip
   ```
   
3. Clone this repo in `/home/pi`:
   ```
   git clone https://github.com/nicoco007/py-erfid
   ```

3. Install requirements:
   ```
   pip install -r requirements.txt
   ```

   **Note:** if you get the error `TypeError: unsupported operand type(s) for -=: 'Retry' and 'int'` or pip fails to connect to https://www.piwheels.org/simple, you may need to edit the `/etc/pip.conf` and either comment out with a `#` or remove the line `extra-index-url=https://www.piwheels.org/simple`.

4. Install service:
   ```
   sudo bash install-service.sh
   ```
5. Run `read-only-fs.sh` and follow the instructions to make the system read-only and avoid issues when unplugging the Pi while it is running. We recommend using the boot-time read/write jumper set to GPIO 21. See [this Adafruit article](https://learn.adafruit.com/read-only-raspberry-pi/) for more information.

6. Done!
