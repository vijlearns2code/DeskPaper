import json
import os
from datetime import datetime
from io import BytesIO

import requests
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
from wallpaperChanger import wallpaper
from wallpaperChanger.settings import ASSETS_DIR, CURRENT_THEME, ERROR_BG, GENERATED_DIR, OK_WALLPAPER, ERROR_WALLPAPER, \
    API_KEY, CITY, \
    TEMPLATE, PIC_URL, OFFLINE, ISWINDOWS, DOWNLOAD
import glob

pic_url = PIC_URL
CurrentUrl = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no"
weather_ID = 0
currentTheme = CURRENT_THEME
configurations = {
    "default": [(3350, 200), ["center", "center"], False, True, ["right", "top"], "Light"],
    "middle-left": [(3350, 200), ["left", "center"], False, True, ["right", "top"], "Light"],
    "middle-right": [(3350, 200), ["right", "center"], False, True, ["right", "top"], "Light"],
    "custom": [(3350, 200), ["left", "bottom"], True, False, ["right", "top"], "Medium"],
}
wallpaper_directory_day = 'C:/Users/User/PycharmProjects/show_project/assets/wallpapers/day/'
wallpaper_directory_night = 'C:/Users/User/PycharmProjects/show_project/assets/wallpapers/night/'

date_text_anchors = {
    "top": [6, 5.6],
    "bottom": [1.4, 1.4],
    "center": [2, 2],
    "right": [1.07, 1.055],
    "left": [12, 12],
}

font = ImageFont.truetype(
    str(ASSETS_DIR / "fonts/Montserrat/Montserrat-{}.ttf").format(configurations[currentTheme][5]), 120)
font2 = ImageFont.truetype(
    str(ASSETS_DIR / "fonts/Montserrat/Montserrat-{}.ttf").format(configurations[currentTheme][5]), 50)
font3 = ImageFont.truetype(
    str(ASSETS_DIR / "fonts/Montserrat/Montserrat-{}.ttf").format(configurations[currentTheme][5]), 70)
font4 = ImageFont.truetype(
    str(ASSETS_DIR / "fonts/Montserrat/Montserrat-{}.ttf").format(configurations[currentTheme][5]), 50)
font5 = ImageFont.truetype(str(ASSETS_DIR / "fonts/Montserrat/{}.ttf").format("NotoEmoji-Regular"), 70)

brightness = 0.4

clock = {
    1: "🕐",
    2: "🕑",
    3: "🕒",
    4: "🕓",
    5: "🕔",
    6: "🕕",
    7: "🕖",
    8: "🕗",
    9: "🕘",
    10: "🕙",
    11: "🕚",
    12: "🕛",
}


def refresh():
    img = Image.open(TEMPLATE)
    W, H = img.size
    draw = ImageDraw.Draw(img)
    now = datetime.now()
    if configurations[currentTheme][3]:
        w, h = getSize(draw, "{}".format(now.strftime("%H:%M")), font4)
        if ISWINDOWS:
            draw.text(((W - w) / date_text_anchors[configurations[currentTheme][4][0]][0] - 100,
                       (H - h) / date_text_anchors[configurations[currentTheme][4][1]][0] + 1655),
                      "{}".format(now.strftime("%#I:%M %p")), (255, 255, 255), font=font4)
        else:
            draw.text(((W - w) / date_text_anchors[configurations[currentTheme][4][0]][0] - 100,
                       (H - h) / date_text_anchors[configurations[currentTheme][4][1]][0] + 1655),
                      "{}".format(now.strftime("%-I:%M %p")), (255, 255, 255), font=font4)

        w, h = getSize(draw, clock[int(now.strftime("%I"))], font5)
        draw.text(((W - w) / date_text_anchors[configurations[currentTheme][4][0]][0] - 250,
                   (H - h) / date_text_anchors[configurations[currentTheme][4][1]][0] + 1650),
                  clock[int(now.strftime("%I"))], (255, 255, 255), font=font5)

    img.save(OK_WALLPAPER)
    wallpaper.set_wallpaper(OK_WALLPAPER)


def get_weather_data():
    try:
        response = requests.get(CurrentUrl)
        response.raise_for_status()
        data = response.json()

        weather_ID = data['current']['condition']['code']
        temperature_celsius = data['current']['temp_c']
        is_day = data[ 'current']['is_day']

    except KeyError as e:
        print("KeyError: Missing key in response data:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

    return weather_ID, temperature_celsius, is_day


def get_nearest_wallpaper(temperature_celsius, is_day, weather_code):
    # Lists all wallpaper files in the directory
    if (is_day):
        wallpaper_files = glob.glob(os.path.join(os.path.join(wallpaper_directory_day, weather_code), '*.jpeg'))
    else:
        wallpaper_files = glob.glob(os.path.join(os.path.join(wallpaper_directory_night, weather_code), '*.jpeg'))

    for i in range(len(wallpaper_files)):
        lower_temp = 20 + i * 1
        upper_temp = lower_temp + 1
        if lower_temp <= temperature_celsius < upper_temp:
            return wallpaper_files[i]

    return ERROR_BG

def set_wallpaper_based_on_temperature(wallpaper_path):
    print(wallpaper_path)

    if os.name == 'posix':  # Unix/Linux
        os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{wallpaper_path}")
    elif os.name == 'nt':  # Windows
        import ctypes
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_path, 3)

    img = Image.open(wallpaper_path)  # open image
    img = img.point(lambda p: p * brightness)  # change image brightness

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    if (OFFLINE == False):
        try:
            # im1 = Image.open(urlopen(Request(url=pic_url, headers=headers)))  # get the weather widget
            response = requests.get(pic_url, headers)
            response.raise_for_status()
            im1 = Image.open(BytesIO(response.content))

            # crop image
            w, h = im1.size
            im1 = im1.crop((0, 0, w, h - 30))

            # resizing and positioning the weather widget
            baseheight = 600
            hpercent = (baseheight / float(im1.size[1]))
            wsize = int((float(im1.size[0]) * float(hpercent)))
            im1 = im1.resize((wsize, baseheight))

            img.paste(im1, (configurations[currentTheme][0]), im1)  # widget location
            img.save(DOWNLOAD)

        except requests.exceptions.RequestException as e:
            print(f"Request Exception while fetching weather widget: {e}")
        except Exception as e:
            print(f"Error processing weather widget image: {e}")

    draw = ImageDraw.Draw(img)
    now = datetime.now()

    # draw the day
    W, H = img.size
    w, h = getSize(draw, now.strftime("%A"), font)
    draw.text(((W - w) / date_text_anchors[configurations[currentTheme][1][0]][0],
               (H - h) / date_text_anchors[configurations[currentTheme][1][1]][0]),
              now.strftime("%A"), (255, 255, 255), font=font)

    # draw the date: month day year
    # w, h = draw.textlength(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2)
    w, h = getSize(draw, now.strftime("%B") + " " + str(now.day) + ", " + str(now.year), font2)
    draw.text(((W - w) / date_text_anchors[configurations[currentTheme][1][0]][1],
               (H - h) / date_text_anchors[configurations[currentTheme][1][1]][1] + 100),
              now.strftime("%B") + " " + str(now.day) + ", " + str(now.year), (255, 255, 255), font=font2)

    img.save(TEMPLATE)

    refresh()
    print(f"Desktop wallpaper set")


def main():
    global brightness, weather_ID
    try:
        weather_ID, temperature_celsius, is_day = get_weather_data()
        print(f"Weather ID: {weather_ID}")
        print(f"Temperature: {temperature_celsius}°C")
        if (is_day):
            print("It's Daytime")
        else:
            print("It's Night")

        if not Path(GENERATED_DIR / 'feed.json').exists():
            try:
                response = requests.get(CurrentUrl)
                with open(GENERATED_DIR / 'feed.json', 'wb') as file:
                    file.write(response.content)

            except requests.ConnectionError:
                weather_ID = 800
        else:
            with open(GENERATED_DIR / 'feed.json', 'rb') as file:
                data = json.load(file)

        if(is_day):
            brightness = 0.7
            print("is day: true")
        else:
            brightness = 0.4
            print("is day: false")

        weather_code = ""
        if 300 <= int(weather_ID) < 623:
            print("rain")
            weather_code = "rain"
        elif 700 < int(weather_ID) < 782:
            print("mist")
            weather_code = "mist"
        elif int(weather_ID) >= 800:
            print("clear")
            weather_code = "clear"
        elif 200 <= int(weather_ID) <= 232:
            print("thunder")
            weather_code = "thunder"

        wallpaper_path = get_nearest_wallpaper(temperature_celsius, is_day, weather_code)
        set_wallpaper_based_on_temperature(wallpaper_path)

    except Exception as e:
        print(e)
        getFailed()


def getFailed():
    try:
        img = Image.open(ERROR_BG)
        draw = ImageDraw.Draw(img)
        now = datetime.now()

        W, H = img.size

        # positioning date time text
        # w, h = draw.textlength(now.strftime("%A"), font=font)
        w, h = getSize(draw, now.strftime("%A"), font)
        draw.text(((W - w) / 2, (H - h) / 2), now.strftime("%A"), (255, 255, 255),
                  font=font)  # day text: what day it is

        # w, h = draw.textlength(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2)
        w, h = getSize(draw, now.strftime("%B") + " " + str(now.day) + ", " + str(now.year), font2)
        draw.text(((W - w) / 2, (H - h) / 2 + 100), now.strftime("%B") + " " + str(now.day) + ", " + str(now.year),
                  (255, 255, 255), font=font2)  # date text: the date

        img.save(ERROR_WALLPAPER)
    except Exception as e:  # the above code failed: perhaps the error.jpeg doesn't exist.
        print(e)  # debug

        w, h = 3936, 2424
        img = Image.new("RGB", (w, h))
        now = datetime.now()
        img1 = ImageDraw.Draw(img)
        img1.rectangle([(0, 0), img.size], fill=(220, 118, 51))  # draw the background as a plain colour

        W, H = img.size

        # positioning date time text
        # w, h = img1.textlength(now.strftime("%A"), font=font)
        w, h = getSize(img1, now.strftime("%A"), font)
        img1.text(((W - w) / 2, (H - h) / 2), now.strftime("%A"), (255, 255, 255), font=font)

        # w, h = img1.textlength(now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font=font2)
        w, h = getSize(img1, now.strftime("%B") + " " + str(now.day) + " " + str(now.year), font2)
        img1.text(((W - w) / 2, (H - h) / 2 + 100), now.strftime("%B") + " " + str(now.day) + " " + str(now.year),
                  (255, 255, 255), font=font2)  # date text

        img.save(ERROR_WALLPAPER)

    wallpaper.set_wallpaper(ERROR_WALLPAPER)


def getSize(draw, text, font):
    """Function to calculate text size."""
    _, _, W, H = draw.textbbox((0, 0), text=text, font=font)
    return W, H


if __name__ == '__main__':
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    main()
