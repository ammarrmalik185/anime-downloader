from bs4 import BeautifulSoup
from selenium import webdriver
import os
import webbrowser

if not os.path.exists("New Season Animes"):
    os.makedirs("New Season Animes")

def is_present(name):
    flag = False
    
    for x in valid_anime_list:
        x = x.lower()
        name = name.lower()
        if x in name or name in x:
            flag = True
            break
    return flag
    
    
def downloaded_anime_check(season):
    path = "cache\\recently downloaded animes " + season + ".txt"
    if os.path.isfile(path):
        file = open(path, "r")
        for line in file.readlines():
            if "\n" in line:
                line = line.replace("\n", "")
            downloaded_animes.append(line)
    else:
        open(path, "w")


def valid_anime_check(season):
    path = "New Season Animes\\New Animes " + season + ".txt"
    if os.path.isfile(path):
        file = open(path  , "r")
        for line in file.readlines():
            if "\n" in line:
                line = line.replace("\n", "")
            if line != "" and line != " ":
                valid_anime_list.append(line)
    else:
        open(path , "w")


def link_source_code_getter(url_list):
    source_codes = []
    if len(url_list) > 0:
        driver = webdriver.Chrome()
        for url in url_list:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            source_codes.append(soup)
        driver.quit()
    return source_codes


def download(list_1,choice):
      if len(list_1) > 0: 
            index = int(choice) - 1
            for li in list_1:
                webbrowser.open(str(li[index]))
            input(str(len(list_1)) + " animes are downloading.... Press Enter to continue ...")
      elif choice == "4":
            input("Not downloading animes.... Press Enter to continue ...")
      else:
            input("No animes to download.... Press Enter to continue ...")


def choice_getter():
    while True:
        print("1 - Lowest(360p or 480p)\n2 - Medium(720p)\n3 - High(1080p)\n4 - Exit")
        choice = input("In which quality do you want to download the Anime :")
        if choice == "1" or "2" or "3" or "4":
            break
        else:
            print("Option not available")
    return choice


def links_to_check(code):
    episode_no_list = []
    episode_name_list = []
    link_list = []
    release_date_list = []
    download_bol = []

    code = code.find("div", {"class": "latest-releases"})

    for e in code.findAll("li", {}):
        span = e.find("span", {"class": "latest-releases-date"})
        strong = e.find("strong", {})
        div = e.find("div", {})
        a = e.find("a", {})

        link = a["href"]
        resolutions = div.get_text()
        release_date = span.get_text()
        episode_no = strong.get_text()
        complete = e.get_text()

        episode_name = complete.replace(resolutions, "")
        episode_name = episode_name.replace(release_date, "")
        episode_name = episode_name.replace(episode_no, "")
        episode_name = episode_name[:-3]
        
        if is_present(episode_name):
            
            episode_no_list.append(episode_no)
            episode_name_list.append(episode_name)
            link_list.append("https://horriblesubs.info" + link)
            release_date_list.append(release_date)
            if episode_name in downloaded_animes:
                download_bol.append(False)
            else:
                download_bol.append(True)

    return episode_no_list, episode_name_list, link_list, release_date_list, download_bol


def code_to_links(code_list):
    link_list = []
    for e in code_list:
        e = e.find("div" ,{"class": "episode-container"})
        container = e.find("div", {"class": "rls-links-container"})
        links = []
        for e2 in container.findAll("div", {}):
            magnet = e2.find("a", {"title": "Magnet Link"})
            links.append(magnet["href"])
        link_list.append(links)

    return link_list


def save(downloaded_anime_name):
    text = ""
    count = 0
    while True:
        try:
            text += str(downloaded_anime_name[count]) + "\n"
            count += 1
        except IndexError:
            path = "cache\\recently downloaded animes " + season + ".txt"
            file = open(path, "w")
            file.write(text)
            file.close()
            break

def core():
    try:
        episode_no_list, episode_name_list, link_list, release_date_list, download_bol = \
            links_to_check(link_source_code_getter(["https://horriblesubs.info/"])[0])
        download_links = []
        for i in range(0, len(episode_no_list)):
            if download_bol[i]:
                download_links.append(link_list[i])
            
        
        save(episode_name_list)
        for i in range(0, len(episode_no_list)):
            print("")
            if download_bol[i]:
                print(str(i+1) + " - Downloading     : " + episode_name_list[i] +
                      "\n             Episode no  : " + episode_no_list[i] +
                      "\n             Released    : " + release_date_list[i])
            else:
                print(str(i+1) + " - Not Downloading : " + episode_name_list[i] +
                      "\n             Episode no  : " + episode_no_list[i] +
                      "\n             Released    : " + release_date_list[i])
        print("---------------------------------------------------------------------")
        choice = "1" #choice_getter()
        if choice != 4:
            codes = link_source_code_getter(download_links)
        else:
            codes = []
        
        download(code_to_links(codes),choice)
    except AttributeError:
        input("Internet not available ... press enter to continue")


valid_anime_list = []
downloaded_animes = []

season = input("Enter Season (must be same as file name) :")

valid_anime_check(season)
downloaded_anime_check(season)
core()
