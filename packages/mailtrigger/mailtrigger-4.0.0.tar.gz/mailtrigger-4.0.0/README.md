# Mail Trigger

[![PyPI](https://img.shields.io/pypi/v/mailtrigger.svg?color=brightgreen)](https://pypi.org/project/mailtrigger/)
[![Travis](https://travis-ci.com/craftslab/mailtrigger.svg?branch=master)](https://travis-ci.com/craftslab/mailtrigger)
[![Coverage](https://coveralls.io/repos/github/craftslab/mailtrigger/badge.svg?branch=master)](https://coveralls.io/github/craftslab/mailtrigger?branch=master)
[![License](https://img.shields.io/github/license/craftslab/mailtrigger.svg?color=brightgreen)](https://github.com/craftslab/mailtrigger/blob/master/LICENSE)



## Requirements

- Python (3.7+)
- pip
- python-dev



## Installation

On Ubuntu / Mint, install *Mail Trigger* with the following commands:

```bash
apt update
apt install python3-dev python3-pip python3-setuptools
pip install mailtrigger
```

On OS X, install *Mail Trigger* via [Homebrew](https://brew.sh/) (or via [Linuxbrew](https://linuxbrew.sh/) on Linux):

```
TBD
```

On Windows, install *Mail Trigger* with the following commands:

```
pip install -U pywin32
pip install -U PyInstaller
pip install -Ur requirements.txt

pyinstaller --clean --name mailtrigger -F trigger.py
```



## Updating

```bash
pip install mailtrigger --upgrade
```



## Running

```bash
mailtrigger --auther-config auther.json --mailer-config mailer.json --scheduler-config scheduler.json --trigger-config trigger.json
```



## Settings

*Mail Trigger* parameters can be set in the directory [config](https://github.com/craftslab/mailtrigger/blob/master/mailtrigger/config).

An example of configuration in [auther.json](https://github.com/craftslab/mailtrigger/blob/master/mailtrigger/config/auther.json):

```
{
  "group": {
    "default": [
      "name@example.com"
    ],
    "ldap/name": "true"
  },
  "message": {
    "subject": "[trigger]"
  },
  "provider": {
    "ldap": {
      "base": "base",
      "host": "localhost",
      "pass": "pass",
      "port": 389,
      "user": "user"
    }
  }
}
```

An example of configuration in [mailer.json](https://github.com/craftslab/mailtrigger/blob/master/mailtrigger/config/mailer.json):

```
{
  "pop3": {
    "host": "pop.example.com",
    "pass": "pass",
    "port": 995,
    "ssl": true,
    "timeout": 10,
    "user": "user"
  },
  "smtp": {
    "host": "smtp.example.com",
    "pass": "pass",
    "port": 465,
    "ssl": true,
    "timeout": 10,
    "user": "user"
  }
}
```

An example of configuration in [scheduler.json](https://github.com/craftslab/mailtrigger/blob/master/mailtrigger/config/scheduler.json):

```
{
  "interval": 30
}
```

An example of configuration in [trigger.json](https://github.com/craftslab/mailtrigger/blob/master/mailtrigger/config/trigger.json):

```
{
  "gerrit": {
    "server": [
      {
        "host": "localhost",
        "pass": "pass",
        "port": 8080,
        "user": "user"
      }
    ]
  },
  "jenkins": {
    "server": [
      {
        "host": "localhost",
        "pass": "pass",
        "port": 8081,
        "user": "user"
      }
    ]
  },
  "printer": {
    "file": "output.xlsx",
  }
}
```



## Usage

### Subject

```
[trigger]: Write your description here
```

**Note: `[trigger]` is the reserved word in subject**



### Recipient

The recipient is mail receiver as *Mail Trigger*.



### Content

#### Gerrit Trigger

```
@gerrit abandon <host> <changenumber>
@gerrit help
@gerrit list
@gerrit query <host> <changenumber>
@gerrit rebase <host> <changenumber>
@gerrit restart <host>
@gerrit restore <host> <changenumber>
@gerrit review <host> <changenumber>
@gerrit reviewer <host> <changenumber> [add|remove] <reviewer>
@gerrit start <host>
@gerrit stop <host>
@gerrit submit <host> <changenumber>
@gerrit version <host>
```



#### Jenkins Trigger

```
TBD
```



#### Trigger Help

```
@help
```



## License Apache

Project License can be found [here](https://github.com/craftslab/mailtrigger/blob/master/LICENSE).
