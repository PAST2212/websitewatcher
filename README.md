# websitewatcher

Here you can trace changes for domains. websitewatcher will also send you automatically e-mails if any change on a domain was detected.

**Example Screenshot:**
![image](https://github.com/PAST2212/websitewatcher/assets/124390875/a97513c5-db6a-4278-81e7-9be0aed6a067)

**Features:**
- Multithreading (50 workers by default)
- MX-Record, HTML-Title and HTML-Description Tag lookups to detect (fraudulent) webpage changes (A-Record lookups are included but not activated by default)
- Send automatically E-Mails about changed websites

**Principles**
- "Webpage Content has been changed or added. New Website Title: " in E-Mail means that the **content of a webpage** has been changed. The Title of a Webpage is in the browser tab
  ![image](https://github.com/PAST2212/websitewatcher/assets/124390875/94436f80-1a95-4727-88de-c2b933011842)

- "Webpage Content has been changed or added. New Website Description: " in E-Mail means that **content of a webpage** has been changed. This Information is typically used by search engines and other web services

- "MX-Record has been changed or added. New Record: " in E-Mail means that the **mail server configuration** has been changed. This information is helpful to track changes on phishing domains which arent active but have a high possibility for being used in bad faith in the future (e.g. a third party registered look-a-like domain: tuiqroup.com instead of tuigroup.com (g=q))



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
- Add Deeplink / Webpath compability, for example observe fakedomain.com/business
