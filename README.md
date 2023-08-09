**Features:**
- Multithreading (50 workers by default)
- MX-Record, HTML-Title and HTML-Description Tag lookups to detect (fraudulent) webpage changes (A-Record is included but not activated by default)
- Send automatically E-Mails about changed websites

**How to install:**
- git clone https://github.com/PAST2212/websitewatcher.git
- cd websitewatcher
- pip install -r requirements.txt

**How to run:**
- python3 websitewatcher.py

**How to update**: Type command in websitewatcher directory
- git pull
- In case of a Merge Error: Try "git reset --hard" before "git pull"

**Changelog**
- Please see Changelog for Updates:
- https://github.com/PAST2212/websitewatcher/blob/main/Changelog

**Authors**
- Patrick Steinhoff (https://www.linkedin.com/in/patrick-steinhoff-168892222/)

Written in Python 3.7

TO DO:
- Add Possibility to send screenshots of changed websites via mail as attachement 
- Add Possibility to parse arguments (e.g. workers for multithreading)
- Add other paramaters as MX-Record, HTML-Title, HTML-Description if that makes sense.
