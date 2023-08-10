# websitewatcher

Here you can trace changes for domains. websitewatcher will also send you automatically reports via E-Mail if any change on a domain was detected.


**Background**

Regardless if legal, compliance, cyber security or fraud management department is monitoring for malicious domains. Due to the amount of registered domains on a daily base, many domain results can be produced on a weekly / monthly base. It is not uncommon for the majority of domains at the registration date to have no website or no server connect. It also also not uncommon for domains at the registration date to have no (receiving) mail server functionality. As a result, the analyst must keep track of all the results and the results may grow quite fast over the time. Its a waste of time to do it manually.

With help of this project you can track these domains for changes.


**Example Screenshot of a Mail Report that notified about changes of observed domains for illustration purposes:**

![image](https://github.com/PAST2212/websitewatcher/assets/124390875/d8e59195-97fb-40c2-be42-5eda7c29cf39)


**Features**
- Multithreading (50 workers by default)
- MX-Record, HTML-Title and HTML-Description Tag lookups to detect (fraudulent) webpage changes (A-Record lookups are included but not activated by default)
- Send automatically E-Mails about changed websites


**Principles**
- "Webpage Content has been changed or added. New Website Title: " in E-Mail means that the **content of a webpage** has been changed. The Title of a Webpage is in the browser tab
  ![image](https://github.com/PAST2212/websitewatcher/assets/124390875/94436f80-1a95-4727-88de-c2b933011842)

- "Webpage Content has been changed or added. New Website Description: " in E-Mail means that **content of a webpage** has been changed. This Information is typically used by search engines and other web services

- "MX-Record has been changed or added. New Record: " in E-Mail means that the **mail server configuration** has been changed. This information is helpful to track changes on phishing domains which arent active but have a high possibility for being used in bad faith in the future (e.g. a third party registered look-a-like domain: tuiqroup.com instead of tuigroup.com (g=q))


**Before the first run - How it Works:**
1. Put your domains into this TXT file "User Input/tracked_websites.txt" line per line for monitoring operations. Some domains are listed per default.

2. Create a new mail account and put your E-Mail address for sending reports, password and recipient address into this TXT file "User Input/mail_account.txt"
   - Either you create an account on your company side with a company address (e.g. domainbot@company.com) or
   - You create an account on another mail provider (e.g. GMAIL, as an example: https://mailtrap.io/blog/python-send-email-gmail/)
  

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
