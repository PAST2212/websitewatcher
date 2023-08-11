import os
import csv
import dns.resolver
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from requests.exceptions import HTTPError
import sys
import re

list_file_domains = []

# Lists for actual Elements
html_tags = []
a_records = []
mx_records = []

# Lists for previous Elements
html_titles_compare = []
html_description_compare = []
a_records_compare = []
mx_records_compare = []

mail_account = {}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}

desktop = os.path.join(os.path.expanduser('~'), 'websitewatcher')


def read_tracked_websites_file():
    try:
        file_domains = open(desktop + '/User Input/tracked_websites.txt', 'r', encoding='utf-8-sig')
        for my_domains in file_domains:
            domain = my_domains.replace("\n", "").lower().strip()
            list_file_domains.append(domain)
        file_domains.close()

    except Exception as e:
        print('Something went wrong with reading tracked_websites.txt Input File. Please check file.', e)
        sys.exit()


def read_mail_account():
    try:
        file_domains = open(desktop + '/User Input/mail_account.txt', 'r', encoding='utf-8-sig')
        for my_domains in file_domains:
            (key, val) = my_domains.split(':', 1)
            mail_account[key.strip()] = val.strip().lstrip('"').rstrip('"').replace("\n", "")
        file_domains.close()

    except Exception as e:
        print('Something went wrong with reading mail_account.txt Input File. Please check file.', e)
        sys.exit()

    if mail_account['sender_address'] == '' or mail_account['password'] == '' or mail_account['recipient_address'] == '':
        print('Something went wrong with reading mail_account.txt Input File. Please check if sender address, recipient address or password are not emtpy.')
        sys.exit()


def html_tag_lookup(domain):
    hey = []
    domains = 'http://' + domain
    request_session = requests.Session()
    request_session.keep_alive = False
    try:
        response = request_session.get(domains, headers=headers, allow_redirects=True, timeout=(5, 30))
        if response.raise_for_status() is None:
            soup = BeautifulSoup(response.text, 'lxml')
            hey.append(domain)
            title = soup.find('title')
            description = soup.find('meta', attrs={'name': 'description'})
            if title is not None:
                title_mod = re.sub(r'[\n\r\t\b\f\v]+', '', title.get_text())
                hey.append(title_mod.lower().strip())
            if description is not None:
                description_mod = re.sub(r'[\n\r\t\b\f\v]+', '', description['content'])
                hey.append(description_mod.lower().strip())

    except (TypeError, AttributeError, requests.exceptions.ReadTimeout, KeyError):
        print('Parsing Webpage Error. Something went wrong at scraping: ', domain)

    except (HTTPError, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.TooManyRedirects):
        print('Server Connection Error. Domain is probably not online: ', domain)

    except Exception as e:
        print('Other Error occured: ', e)

    return list(filter(None, hey))

def mx_record(domain):
    mx_temp = []
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    resolver.lifetime = 5
    resolver.nameservers = ['8.8.8.8']
    mx_temp.append(domain)
    try:
        content = ""
        MX = resolver.resolve(domain, 'MX')
        for answer in MX:
            content = content + " " + str(answer)
        mx_temp.append(sorted(content.lstrip().rstrip(".").split(". ")))

    except Exception as e:
        print(f'MX-Record lookup Error. Something went wrong by DNS lookup for domain {domain}', e)

    return list(filter(None, mx_temp))


def a_record(domain):
    a_temp = []
    resolver = dns.resolver.Resolver()
    resolver.timeout = 2
    resolver.lifetime = 2
    resolver.nameservers = ['8.8.8.8']
    a_temp.append(domain)
    try:
        content = ""
        A = resolver.resolve(domain, 'A')
        for answer in A:
            content = content + " " + str(answer)
        a_temp.append(sorted(content.split()))

    except Exception as e:
        print(f'A-Record lookup Error. Something went wrong by DNS lookup for domain {domain}', e)

    return list(filter(None, a_temp))


def html_tag_threading(n):
    thread_ex_list = [y for y in list_file_domains]
    print(len(thread_ex_list), 'Domains detected from file tracked_websites.txt\n')

    with ThreadPoolExecutor(n) as executor:
        results = executor.map(html_tag_lookup, thread_ex_list)
        for result in results:
            if result is not None and len(result) > 1:
                html_tags.append(result)

    return html_tags


def a_record_threading(n):
    thread_ex_list = [y for y in list_file_domains]

    with ThreadPoolExecutor(n) as executor:
        results = executor.map(a_record, thread_ex_list)
        for result in results:
            if result is not None and len(result) > 1:
                a_records.append(result)

    return a_records


def mx_record_threading(n):
    thread_ex_list = [y for y in list_file_domains]

    with ThreadPoolExecutor(n) as executor:
        results = executor.map(mx_record, thread_ex_list)
        for result in results:
            if result is not None and len(result) > 1:
                mx_records.append(result)

    return mx_records


def data_to_csv(input_data_csv, attribute_list):
    for y in attribute_list:
        if y[0] == input_data_csv and attribute_list == separate_into_html_title():
            return y[1]

        elif y[0] == input_data_csv and attribute_list == separate_into_html_description():
            return y[1]

        elif y[0] == input_data_csv:
            dummy = ','.join([str(elem) for elem in y[1]])
            return dummy


def postprocessing_outputfile():
    df = pd.read_csv(f'{desktop}/website_changes.csv', delimiter=',', encoding='utf-8-sig')
    df['MX-Record(s)'] = df.apply(lambda x: data_to_csv(x['Domains'], mx_records), axis=1)
    #df['A-Record(s)'] = df.apply(lambda x: data_to_csv(x['Domains'], a_records), axis=1)
    df['HTML-Title'] = df.apply(lambda x: data_to_csv(x['Domains'], separate_into_html_title()), axis=1)
    df['HTML-Description'] = df.apply(lambda x: data_to_csv(x['Domains'], separate_into_html_description()), axis=1)
    df.to_csv(f'{desktop}/website_changes.csv', index=False, encoding='utf-8-sig')


def model_csv_file():
    console_file_path = f'{desktop}/website_changes.csv'
    if not os.path.exists(console_file_path):
        with open(console_file_path, mode='w', newline='', encoding='utf-8-sig') as f:
            header = ['Domains', 'MX-Record(s)', 'HTML-Title', 'HTML-Description']
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for domain in list_file_domains:
                writer.writerow({'Domains': domain})

    else:
        file = open(console_file_path, mode='r', encoding='utf-8-sig')
        csvreader = csv.DictReader(file, delimiter=',')
        csv_domains = [row['Domains'] for row in csvreader]
        added_input_domain = [k for k in list_file_domains if k not in csv_domains]
        deleted_input_domains = [h for h in csv_domains if h not in list_file_domains]
        print('New Website(s) added to tracked_websites.txt file: ', added_input_domain)
        print('Old Website(s) deleted from tracked_websites.txt file: ', deleted_input_domains)
        file.close()

        if len(added_input_domain) > 0:
            file_1 = open(console_file_path, mode='a', newline='', encoding='utf-8-sig')
            writer = csv.writer(file_1, delimiter=',')
            for k in added_input_domain:
                writer.writerow([k])
            file_1.close()

        if len(deleted_input_domains) > 0:
            df = pd.read_csv(f'{desktop}/website_changes.csv', delimiter=',', encoding='utf-8-sig')
            for i in deleted_input_domains:
                df = df.drop(df[df['Domains'] == i].index)
            df.to_csv(f'{desktop}/website_changes.csv', index=False, encoding='utf-8-sig')


def load_old_attributes():
    with open(f'{desktop}/website_changes.csv', 'r', encoding='utf-8-sig') as f:
        csvreader = csv.DictReader(f, delimiter=',')
        for row in csvreader:
            mx_records_compare.append([row['Domains'], row['MX-Record(s)']])
            #a_records_compare.append([row['Domains'], row['A-Record(s)']])
            html_titles_compare.append([row['Domains'], row['HTML-Title']])
            html_description_compare.append([row['Domains'], row['HTML-Description']])


def group_tuples_first_value(input):
    out = {}
    for elem in input:
        try:
            out[elem[0]].extend(elem[1:])
        except KeyError:
            out[elem[0]] = list(elem)

    return [tuple(values) for values in out.values()]


def separate_into_html_title():
    html_titles = [(y[0], y[1]) for y in html_tags]
    return html_titles


def separate_into_html_description():
    html_description = [(y[0], y[2]) for y in html_tags if len(y) > 2]
    return html_description


def compare_changes():
    #a_record_changes = [(i[0], 'A-Record has been changed or added. New Record: "{}"'.format(x)) for k in a_records_compare for i in a_records if k[0] == i[0] and k[1].split(',') != i[1] for x in i[1] if x not in k[1].split(',')]
    mx_record_changes = [(i[0], 'MX-Record has been changed or added. New Record: "{}"'.format(x)) for k in mx_records_compare for i in mx_records if k[0] == i[0] and k[1].split(',') != i[1] for x in i[1] if x not in k[1].split(',')]
    html_title_changes = [(i[0], 'Webpage Content has been changed or added. New Website Title: "{}"'.format(i[1])) for k in html_titles_compare for i in html_tags if k[0] == i[0] and k[1] != i[1]]
    html_description_changes = [(i[0], 'Webpage Content has been changed or added. New Website Description: "{}"'.format(i[2])) for k in html_description_compare for i in html_tags if len(i) > 2 if k[0] == i[0] and k[1] != i[2]]
    sum_changes = mx_record_changes + html_title_changes + html_description_changes

    if len(sum_changes) > 0:
        output_changes = group_tuples_first_value(sum_changes)
        new_comprehension = "\n\n".join(str(row) for row in output_changes)
        return new_comprehension


def send_email_fct():
    fromaddr = mail_account['sender_address']
    mdpfrom = mail_account['password']
    toaddr = mail_account['recipient_address']

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Notification Website Watcher - Changes were detected"

    body_email = f"This Mail was automatically generated and provide information about detected changes of monitored websites in file tracked_websites.txt.\n\n" \
                 f"Quantity of current Websites to track changes: {len(list_file_domains)} Websites.\n\n" \
                 f"Following events have been changed or added: \n\n{compare_changes()}"

    msg.attach(MIMEText(body_email, 'plain'))

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, mdpfrom)
        try:
            s.sendmail(fromaddr, toaddr, msg.as_string())
            print('Email Sent')
        finally:
            s.quit()

    except Exception as E:
        print('Mail failed: {}'.format(str(E)))


if __name__=='__main__':
    read_tracked_websites_file()
    read_mail_account()
    model_csv_file()
    load_old_attributes()
    html_tag_threading(50)
    #a_record_threading(50)
    mx_record_threading(50)
    postprocessing_outputfile()
    if compare_changes() is not None:
        send_email_fct()
