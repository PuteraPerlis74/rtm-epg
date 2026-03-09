import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_tv1(f):
    url = "https://rtmklik.rtm.gov.my/tv1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # tulis channel
    f.write('  <channel id="TV1">\n')
    f.write('    <display-name>TV1</display-name>\n')
    f.write('  </channel>\n')

    # cari rancangan (ubah ikut struktur sebenar RTM Klik)
    programmes = soup.find_all("div", class_="programme-item")

    for p in programmes:
        title = p.find("h3").text.strip()
        time = p.find("span", class_="time").text.strip()

        # convert masa "HH:MM" → format EPG
        try:
            start_time = datetime.strptime(time, "%H:%M")
            stop_time = start_time + timedelta(hours=1)

            start_str = start_time.strftime("%Y%m%d%H%M%S +0800")
            stop_str = stop_time.strftime("%Y%m%d%H%M%S +0800")

            f.write(f'  <programme start="{start_str}" stop="{stop_str}" channel="TV1">\n')
            f.write(f'    <title>{title}</title>\n')
            f.write(f'    <desc>{title} rancangan RTM Klik.</desc>\n')
            f.write('  </programme>\n')
        except Exception:
            # fallback kalau masa tak dapat parse
            f.write(f'  <programme start="20260310060000 +0800" stop="20260310070000 +0800" channel="TV1">\n')
            f.write(f'    <title>{title}</title>\n')
            f.write(f'    <desc>{title} rancangan RTM Klik.</desc>\n')
            f.write('  </programme>\n')

def main():
    with open("rtmklik_all.xml", "w", encoding="utf-8") as f:
        f.write('<tv generator-info-name="DIY-EPG">\n')
        scrape_tv1(f)
        f.write('</tv>\n')

if __name__ == "__main__":
    main()