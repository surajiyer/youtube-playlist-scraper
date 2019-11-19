from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


def scrape_video_titles(playlist_url: str, opts: Options):
    # Load the url
    assert isinstance(playlist_url, str)
    # make sure the chromedriver executable is in the same folder as this script!!
    # Download from here: https://chromedriver.chromium.org/downloads
    # Download the same version as the Chrome version installed on your machine.
    driver = webdriver.Chrome(options=opts, executable_path='./chromedriver.exe')
    driver.get(playlist_url)

    # get html
    elem = driver.find_element_by_tag_name('html')
    elem.send_keys(Keys.END)
    time.sleep(3)
    elem.send_keys(Keys.END)
    innerHTML = driver.execute_script("return document.body.innerHTML")
    driver.close()

    # parse the html
    page_soup = bs(innerHTML, 'html.parser')
    res = page_soup.find_all('span', {'class': 'style-scope ytd-playlist-video-renderer'})

    # get titles
    titles = []
    for video in res:
        if video.get('title') != None:
            titles.append((video.get('title')))

    return titles


if __name__ == "__main__":
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    opts = Options()
    opts.add_argument(f'user-agent={user_agent}')
    urls = pd.read_csv('./youtube.csv')
    save_path = "./music_playlist_titles.txt"

    # get titles
    for url in urls.itertuples(index=False, name=None):
        print(f'Running for {url[2]}.')
        titles = scrape_video_titles(url[4], opts)

        # save to file
        with open(save_path, 'a', encoding="utf-8") as f:
            # write out the playlist name
            f.write(f'{url[2]}\n')

            # write out the music titles
            for t in titles:
                f.write(f'{t}\n')
