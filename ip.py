import requests
from time import sleep
from bs4 import BeautifulSoup

############## USAGE #################
# from ip import ipLookup
# ip = "43.215.26.73"

# print(ipLookup(ip))
######################################

def ipLookup(ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'ipinfodb.com',
        'Referer': 'https://ipinfodb.com/',
        'Origin': 'https://ipinfodb.com/'
    }
    result = {
        "country": "",
        "region": "",
        "city": "",
        "isp": "",
        "coordinates_of_city": "",
        "domain_name": ""
    }
    if type(ip) != str or ip == "":
        print("Please provide a valid IP value.")
    data = {
      'ip': ip
    }
    try:
        response = requests.post('https://www.ipinfodb.com/', data=data, headers = headers)
    except requests.exceptions.RequestException:
        return result
    soup = BeautifulSoup(response.text, "html.parser")
    for i in ["Country", "Region", "City", "ISP", "Coordinates of City", "Domain Name"]:
        a = soup.find("strong", text = i)
        if a:
            a = a.findPrevious("td")
            if a:
                a = beautifyText(a.text.partition(i)[2])
                if i == "City":
                    a = a.partition(" Report Incorrect Location")[0]
                elif i == "Coordinates of City":
                    a = a.partition("(")[2].partition(")")[0]
                result[loower(i)] = a
    sleep(0.5)
    return result

def beautifyText(text):
    return " ".join([a for a in text.replace("\n", "").split() if not a == ""])

def loower(text):
    return "_".join(text.lower().split())