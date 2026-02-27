import requests, csv, subprocess

response = requests.get("https://feodotracker.abuse.ch/downloads/ipblocklist.csv")
response.raise_for_status()

rule = 'netsh advfirewall firewall delete rule name="BadIP"'
subprocess.run(["powershell", "-Command", rule])

mycsv = csv.reader(filter(lambda x: not x.startswith("#"), response.text.splitlines()))

for row in mycsv:
    ip = row[1]
    if ip != "dst_ip":
        print("Added Rule to block:", ip)
        rule = f'netsh advfirewall firewall add rule name="BadIP" Dir=Out Action=Block RemoteIP={ip}'
        subprocess.run(["powershell", "-Command", rule])