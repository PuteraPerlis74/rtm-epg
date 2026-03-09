import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Senarai channel TV & Radio RTM Klik
channels = {
    "TV1": "https://rtmklik.rtm.gov.my/tv1",
    "TV2": "https://rtmklik.rtm.gov.my/tv2",
    "Okey": "https://rtmklik.rtm.gov.my/okey",
    "BeritaRTM": "https://rtmklik.rtm.gov.my/berita",
    "MuzikAktif": "https://rtmklik.rtm.gov.my/muzikaktif",
    "Sports": "https://rtmklik.rtm.gov.my/sukan",
    "Parlimen": "https://rtmklik.rtm.gov.my/parlimen",
    "RadioKlasik": "https://rtmklik.rtm.gov.my/radioklasik",
    "NASIONALfm": "https://rtmklik.rtm.gov.my/nasionalfm",
    "AiFM": "https://rtmklik.rtm.gov.my/aifm",
    "TraxxFM": "https://rtmklik.rtm.gov.my/traxxfm",
    "MinnalFM": "https://rtmklik.rtm.gov.my/minnalfm",
    "KLfm": "https://rtmklik.rtm.gov.my/klfm",
    "AsyikFM": "https://rtmklik.rtm.gov.my/asyikfm",
    "Vfm": "https://rtmklik.rtm.gov.my/vfm",
    "WaiFM": "https://rtmklik.rtm.gov.my/waifm",
    "PerlisFM": "https://rtmklik.rtm.gov.my/perlisfm",
    "KedahFM": "https://rtmklik.rtm.gov.my/kedahfm",
    "KelantanFM": "https://rtmklik.rtm.gov.my/kelantanfm",
    "TerengganuFM": "https://rtmklik.rtm.gov.my/terengganufm",
    "PahangFM": "https://rtmklik.rtm.gov.my/pahangfm",
    "JohorFM": "https://rtmklik.rtm.gov.my/johorfm",
    "MelakaFM": "https://rtmklik.rtm.gov.my/melakafm",
    "NegeriSembilanFM": "https://rtmklik.rtm.gov.my/negerisembilanfm",
    "SelangorFM": "https://rtmklik.rtm.gov.my/selangorfm",
    "SarawakFM": "https://rtmklik.rtm.gov.my/sarawakfm",
    "SabahFM": "https://rtmklik.rtm.gov.my/sabahfm",
    "LabuanFM": "https://rtmklik.rtm.gov.my/labuanfm"
}

def scrape_channel(channel_id, url, f):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # cari elemen rancangan (ubah ikut struktur sebenar RTM Klik)
    programmes = soup.find_all("div", class_="programme-item")

    # tulis channel
    f.write(f'  <channel id="{channel_id}">\n')
    f.write(f'    <display-name>{channel_id}</display-name>\n')
    f.write(f'  </channel>\n')

    # tulis programme
    for p in programmes:
        title = p.find("h3").text.strip()
        time = p.find("span", class_="time").text.strip()

        # convert masa "HH:MM" → format EPG
        try:
            start_time = datetime.strptime(time, "%H:%M")
            stop_time = start_time + timedelta(hours=1)

            start_str = start_time.strftime("%Y%m%d%H%M%S +0800")
            stop_str = stop_time.strftime("%Y%m%d%H%M%S +0800")

            f.write(f'  <programme start="{start_str}" stop="{stop_str}" channel="{channel_id}">\n')
            f.write(f'    <title>{title}</title>\n')
            f.write(f'    <desc>{title} rancangan RTM Klik.</desc>\n')
            f.write(f'  </programme>\n')
        except Exception:
            # fallback kalau masa tak dapat parse
            f.write(f'  <programme start="20260310060000 +0800" stop="20260310070000 +0800" channel="{channel_id}">\n')
            f.write(f'    <title>{title}</title>\n')
            f.write(f'    <desc>{title} rancangan RTM Klik.</desc>\n')
            f.write(f'  </programme>\n')

def main():
    with open("rtmklik_all.xml", "w", encoding="utf-8") as f:
        f.write('<tv generator-info-name="DIY-EPG">\n')
        for channel_id, url in channels.items():
            scrape_channel(channel_id, url, f)
        f.write('</tv>\n')

if __name__ == "__main__":
    main()