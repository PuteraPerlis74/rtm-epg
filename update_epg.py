import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

channels = {
    "RTM_TV1": "https://rtmklik.rtm.gov.my/tv1",
    "RTM_TV2": "https://rtmklik.rtm.gov.my/tv2",
    "RTM_Okey": "https://rtmklik.rtm.gov.my/tvokey",
    "RTM_Berita": "https://rtmklik.rtm.gov.my/beritartm",
    "RTM_MuzikAktif": "https://rtmklik.rtm.gov.my/muzikaktif",
    "RTM_Sports": "https://rtmklik.rtm.gov.my/sukan",
    "RTM_Parlimen": "https://rtmklik.rtm.gov.my/parlimen"
}

xmltv = '<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="DIY-EPG">\n'

for channel_id, url in channels.items():
    xmltv += f'  <channel id="{channel_id}">\n    <display-name>{channel_id.replace("RTM_", "RTM ")}</display-name>\n  </channel>\n'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    programs = soup.find_all("div", class_="program-item")

    for i, prog in enumerate(programs):
        title = prog.find("h3").text.strip() if prog.find("h3") else "Rancangan RTM"
        desc = prog.find("p").text.strip() if prog.find("p") else "Tiada sinopsis"
        start_time = (datetime.now() + timedelta(hours=i)).strftime("%Y%m%d%H%M%S")
        stop_time = (datetime.now() + timedelta(hours=i+1)).strftime("%Y%m%d%H%M%S")

        xmltv += f'  <programme start="{start_time} +0800" stop="{stop_time} +0800" channel="{channel_id}">\n'
        xmltv += f'    <title lang="ms">{title}</title>\n'
        xmltv += f'    <desc lang="ms">{desc}</desc>\n'
        xmltv += '  </programme>\n'

xmltv += '</tv>'

with open("rtmklik_all.xml", "w", encoding="utf-8") as f:
    f.write(xmltv)
