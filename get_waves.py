''''
   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   -   Wave Legend - Map and Alert of Local Ocean Swells
`-'  `-'  `-'  `-'  `-'  `-'  `-'  `-'  `
   ,(   ,(   ,(   ,(   ,(   ,(   ,(   ,(   -    Using Latest NDBC NOAA Buoy Buoy Data
`-'  `-'  `-'  `-'  `-'  `-'  `-'  `-'  `
Details:  Selecting the NOAA buoy number of your choice, we search for the raw .txt file, clean up the data,
make decisions on the data, and if we like the wave data we send text message with the happy data.
Requires: requests
WIP:  Still building functionality and planning to add classes to scale.  maybe sqlalchemy.....
Author:  Clouds Weight
License: Git The Unlicense
'''
import requests
from send_text import send_text as send

#class Buoy(self, number):

# read the text file and create an array for data manipulation
def file_read(fname):
    content_array = []
    with open(fname) as f:
        for line in f:
            content_array.append(line)
            textArray = open("waveArray.txt", "w")
            textArray.write("%s" % content_array)
    return content_array #return our new array for data cleaning

def urlReq(buoy="46224"):  # argument could is buoy number
    buoy = buoy
    url = "https://www.ndbc.noaa.gov/data/realtime2/" + buoy + ".txt"
    page = requests.get("%s" % url)  # request built url
    content = page.content  # content is the webpage
    content = content.decode('utf-8')  # make nice
    text_file = open("waveFile.txt", "w")
    text_file.write("%s" % content)
    text_file.close()
    return "waveFile.txt"

def decision_to_surf(total):
    # period = int(period)
    height = list(total)[1]
    period = list(height)[1][1]
    swell = float(list(height)[1][0])
    swell_ft = swell*3
    if swell > 1.2:
        print(f"Surf!")
        send(1, swell_ft, period)

def clean(data):
    cleaned = []
    i =0
    for line in data:
        if i < 12:
            cleaned.append(line)
            i +=1
    return cleaned

def get_heights(clean_data):
    cleaned = clean_data
    time = []
    height = []
    period = []
    for i in cleaned[1:20]:
        time.append(i[10:16])
        height.append(i[33:36])
        period.append(i[39:42])
    waves = zip(height,period)
    total = zip(time, waves)
    return total


def main():
    file = urlReq()
    data = file_read(file)
    clean_data = clean(data)
    total = get_heights(clean_data)
    decision_to_surf(total)


if __name__ == '__main__':
   main()