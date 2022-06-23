import datetime
from datetime import timedelta
import requests
from bs4 import BeautifulSoup

date_converter = {
    "stycznia": 1,
    "luty": 2,
    "marca": 3,
    "kwietnia": 4,
    "maja": 5,
    "czerwca": 6,
    "lipca": 7,
    "sierpnia": 8,
    "września": 9,
    "października": 10,
    "listopada": 11,
    "grudnia": 12
}


# converts alert data to datetime
def convert_date(date):
    date = date.split(" ")
    date[1] = date_converter[date[1]]
    # return date
    return datetime.datetime(int(date[2]), int(date[1]), int(date[0]))


# checks if alert is older than <period> old, where period is days
def check_date(date, period):
    time_delta = datetime.datetime.now() - date
    if time_delta < timedelta(days=period):
        #print("Różnica dni: ", (datetime.datetime.now() - date).days)
        return True
    return False


def parse_orange_alerts(period):
    absolute_url = "https://cert.orange.pl"
    alerts_url = "https://cert.orange.pl/ostrzezenia"
    content_image = "[]"
    author = "CERT Orange Polska"
    username = "@CERTOrange"
    avatar = "https://pbs.twimg.com/profile_images/1149688633521315841/iLxqVl1u_400x400.png"
    # get alerts page
    page = requests.get(alerts_url)
    soup = BeautifulSoup(page.content, "html.parser")

    # parse alerts
    alerts = []
    soup_alerts = soup.find_all("div", class_="block half")
    for soup_alert in soup_alerts:
        date = convert_date(soup_alert.find("div", class_="date").text)
        date_string = date.strftime("%d/%m/%Y")
        title = soup_alert.find("a", class_="title ellip2").text
        link = absolute_url + soup_alert.find("a", class_="uLink", href=True)['href']

        # append alert only if it is fresh enough
        if (check_date(date, period)):
            #alerts.append({"date": date_string, "title": title, "link": link})
            alerts.append({"content": title, "content_images":content_image,
                           "author": author, "author_link":absolute_url,"username":username,
                          "link":link,"date":date_string,"avatar":avatar})

    return alerts




def parse_nask_alerts(period):
    absolute_url = "https://cert.pl/"
    alerts_url = "https://cert.pl/zagrozenia/"
    content_image = "[]"
    author = "CERT Polska"
    username = "@CERT_Polska"
    avatar = "https://pbs.twimg.com/profile_images/458887776423776256/ZNVCXa8E_400x400.png"

    # get alerts page
    page = requests.get(alerts_url)
    soup = BeautifulSoup(page.content, "html.parser")

    # parse alerts
    alerts = []
    soup_alerts = soup.find_all("li", class_="grid-x")

    for soup_alert in soup_alerts:
        date = convert_date(soup_alert.find("span").text)
        date_string = date.strftime("%d/%m/%Y")
        title = soup_alert.find("h4").find("a", href=True).text
        link = absolute_url + soup_alert.find("h4").find("a", href=True)['href']

        # append alert only if it is fresh enough
        if (check_date(date, period)):
            alerts.append({"content": title, "content_images": content_image,
                           "author": author, "author_link": absolute_url, "username": username,
                           "link": link, "date": date_string, "avatar": avatar})
    return alerts


