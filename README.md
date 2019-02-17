# py-erfid
Super simple RFID sign in/sign out system

## Installation
Install pip if not already done:
```
sudo apt install python-pip
```

Install requirements:
```
pip install -r requirements.txt
```

**Note:** if you get the error `TypeError: unsupported operand type(s) for -=: 'Retry' and 'int'` or pip fails to connect to https://www.piwheels.org/simple, you may need to edit the `/etc/pip.conf` and either comment out with a `#` or remove the line `extra-index-url=https://www.piwheels.org/simple`.

Install service:
```
$ sudo bash install-service.sh
```

Done!
