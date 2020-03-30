
import os
import eyed3
import requests
from sys import platform
from bs4 import BeautifulSoup


if platform.startswith('linux'):
    path = "/" + input("Enter path of your musics folder: ").replace("\\", "").strip("/") + "/"
    slash = "/"
    without_lyrics = os.getcwd() + "/without_lyrics/"
    def move_to_without_lyrics(file):
        os.system("mv \"" + file + "\" \"" + without_lyrics + "\"")

elif platform.startswith('win32'):
    path = input("Enter path of your musics folder: ").strip("\\") + "\\"
    slash = "\\"
    without_lyrics = os.getcwd() + "without_lyrics"
    def move_to_without_lyrics(file):
        os.system("move \"" + file + "\" \"" + without_lyrics + "\"")

else:
    print("\nSorry, it's not supported on your OS.\n")
    exit()


files = sorted(os.listdir(path))
if not files or path=="//" or not path:
    print("\n folder is empty!")
    exit()
if not os.path.exists(without_lyrics):
    os.system("mkdir \"" + without_lyrics + "\"")


added_lyrics = 0
not_added_lyrics = 0
def added():
    global added_lyrics
    added_lyrics += 1
def not_added(file=""):
    global not_added_lyrics
    not_added_lyrics += 1
    if file:
        move_to_without_lyrics(file)


def genius_search(tag, url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    lyrics = soup.find("div", {"class": "song_body column_layout"}).find_all("div")[2].get_text()
    if not lyrics:
        Error
    return ("genius", lyrics.strip())


def azlyrics_search(tag, url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    lyrics = soup.find("div", {"class": "col-xs-12 col-lg-8 text-center"}).find_all("div")[5].get_text()
    if not lyrics:
        Error
    return ("azlyrics", lyrics.strip())


def google_search(tag):
    q = '+'.join((tag.artist.replace(",", " ") + " " + tag.title + " lyrics").split()).replace("&", "and")
    url = "https://www.google.com/search?q=" + q + "&ie=utf-8&oe=utf-8"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    urls = []
    for link in soup.find_all('a'):
        link = link.get('href')
        if ("genius.com" in link or "azlyrics.com" in link) and "/url?q=https://" in link and "&sa" in link:
            urls.append(link[link.index("https"):link.index("&sa")])

    sites = ["genius", "azlyrics"]
    functions = [genius_search, azlyrics_search]
    for i in [0,1]:
        for url in urls:
            try:
                if sites[i] in url:
                    source, lyrics = functions[i](tag, url)
                    return (source, lyrics)
            except:
                continue
    else:
        Error


def set_lyrics_auto(path, file):
    try:
        tag = eyed3.load(file).tag
    except:
        not_added()
        return " X file not found: " + file[len(path):]
    try:
        source, lyrics = google_search(tag)
    except:
        not_added(file)
        return " X lyrics not found: " + file[len(path):]

    try:
        tag.lyrics.set(lyrics)
        tag.save(version=eyed3.id3.ID3_V2_4, encoding="utf8")
        added()
        return " | lyrics added from " + source + ": " + file[len(path):]
    except:
        not_added(file)
        return " X lyrics not added: " + file[len(path):]


def set_lyrics_manual(path, file):
        try:
            tag = eyed3.load(file).tag
        except:
            not_added()
            return " X file not found"
        try:
            user_input = input("  link: ")
            if "genius.com" in user_input.lower():
                source, lyrics = genius_search(tag, user_input)
            elif "azlyrics.com" in user_input.lower():
                source, lyrics = azlyrics_search(tag, uruser_inputl)
            else:
                return "   lyrics didn't change"
        except:
            not_added(file)
            return " X lyrics not found"

        try:
            tag.lyrics.set(lyrics)
            tag.save(version=eyed3.id3.ID3_V2_4, encoding="utf8")
            added()
            return " | lyrics added from " + source
        except:
            not_added(file)
            return " X lyrics didn't change"


def set_auto(path, files):
    print("\n" + "─"*len(path) + "──┐")
    print(" " + path + " │", len(files))
    print("─"*len(path) + "──┘")
    folders = []
    for file in files:
        file = path + file
        if os.path.isfile(file):
            print("", files.index(file[len(path):])+1, end = "")
            print(set_lyrics_auto(path, file))
        else:
            folders.append(file + slash)

    for path2 in folders:
        files2 = sorted(os.listdir(path2))
        set_auto(path2, files2)


def set_manual(path, files):
    print("\n\n" + "─"*len(path) + "──┐")
    print(" " + path + " │", len(files))
    print("─"*len(path) + "──┘")
    folders = []
    for file in files:
        file = path + file
        if os.path.isfile(file):
            print("\n", files.index(file[len(path):])+1, end = "\n ")
            print(file[len(path):])
            print(set_lyrics_manual(path, file))
        else:
            folders.append(file + slash)

    for path2 in folders:
        files2 = sorted(os.listdir(path2))
        set_manual(path2, files2)


def see_lyrics(path, files):
    print("\n" + "┌─" + "─"*len(path) + "─┐")
    print("│ " + path + " │")
    print("└─" + "─"*len(path) + "─┘")
    print("\n" + "─"*os.get_terminal_size()[0])
    folders = []
    for file in files:
        file = path + file
        if os.path.isfile(file):
            try:
                print("\n\n  ", files.index(file[len(path):])+1, "/", len(files), sep="",  end = " ")
                print(file[len(path):-4] + "\n\n")
                tag = eyed3.load(file).tag
                if len(tag.lyrics):
                    print(tag.lyrics[0].text)
            except:
                print("    file not found: " + file[len(path):])
            print("\n\n" + "─"*os.get_terminal_size()[0])
        else:
            folders.append(file + slash)

    for path2 in folders:
        files2 = sorted(os.listdir(path2))
        see_lyrics(path2, files2)


sss = input(" 1.Set lyrics (auto)\n 2.Set lyrics (manual)\n 3.See lyrics\n:")
print()
if sss == "1":
    set_auto(path, files)
    print("\n\n successfulls:", added_lyrics, "\n unsuccessfulls:", not_added_lyrics)
elif sss == "2":
    print("\n\n Enter genius or azlyrics link for each file\n or just press enter if you don't want to edit a file")
    set_manual(path, files)
    print("\n\n successfulls:", added_lyrics, "\n unsuccessfulls:", not_added_lyrics)
elif sss == "3":
    see_lyrics(path, files)
print()
