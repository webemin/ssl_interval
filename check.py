import pandas as pd
from datetime import datetime
from termcolor import colored
import os

def file_to_str(file_path):
    file_f = open(file_path, "r", encoding="utf8")
    file_l = file_f.readlines()
    file_str =""

    for file in file_l:
        file_str += file
    
    file_f.close()
    return file_str

domains = file_to_str("domains.txt")
domains_a = domains.split("\n")

less_than_90_count = 0

df_result_p = pd.DataFrame(columns=[colored('Domain', "yellow"), colored('Interval', "yellow"), colored('Start Date', "yellow"), 
colored('Finish Date', "yellow")])

df_result_f = pd.DataFrame(columns=['Domain', 'Interval', 'Start Date', 'Finish Date'])

for domain in domains_a:
    try:
        data = pd.read_html(f'https://crt.sh/?q={domain}')
    except:
        print("Couldn't Fetch the data, please try again.")
    
    df = pd.DataFrame(data = data[2])

    start_date = str(df.loc[0][2]).replace("-", "/")
    finish_date = str(df.loc[0][3]).replace("-", "/")
    domain = df.loc[0][4]

    d1 = datetime.strptime(start_date, "%Y/%m/%d")
    d2 = datetime.strptime(finish_date, "%Y/%m/%d")
    delta = d2 - d1
    
    if delta.days <= 90:
        alert_color = "green"
        less_than_90_count += 1
    else:
        alert_color = "red"

    df_result_f = pd.concat([df_result_f, pd.DataFrame.from_records([{'Domain': domain, 'Interval': delta.days, 'Start Date': start_date,
    'Finish Date': finish_date}])])

    df_result_p = pd.concat([df_result_p, pd.DataFrame.from_records([{colored('Domain', "yellow"): colored(domain, alert_color), 
    colored('Interval', "yellow"): colored(delta.days, alert_color), colored('Start Date', "yellow"): colored(start_date,alert_color), 
    colored('Finish Date', "yellow"): colored(finish_date, alert_color)}])])

    os.system("CLS")
    print(df_result_p)

percent = less_than_90_count/len(domains_a)*100
print(colored(f"\nLess than 90 days rate: %{percent}", "blue"))

a = df_result_f[df_result_f["Interval"] > 90]
b = df_result_f[df_result_f["Interval"] <= 90]

f = open("result.txt", "w", encoding="utf8")
f.write(f"Table of Greater Than 90 Days:\n\n{str(a)}\n\nTable of Less Than 90 Days\n\n{str(b)} \n\nLess than 90 days rate: %{percent}")
f.close()