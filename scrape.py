import requests
import os
from bs4 import BeautifulSoup


def get_writeup(num):
    url = f'https://ctftime.org/writeup/{num}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }

    response = requests.get(url, headers=headers)

    return response

def get_info(response):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser') 

        tags = soup.find_all(class_="label label-info")
        info_tags = []
        for tag in tags:
            info_tags.append(tag.text)
    else:
        print(f"Request failed with status code {response.status_code}")

    

def get_links(response):

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser') 
        binary_links = []
        solve_links = []
        links = []
        all_links = soup.find_all('a')
        for link in all_links:
            if 'href' in link.attrs:
                if "http" in link["href"]:
                    if "raw.githubusercontent.com" in link["href"]:
                        domain = link["href"].split("/")[1] 
                        print(f"Domain {domain}")
                        binary_links.append(link["href"])
                    if ".py" in link["href"]:
                        domain = link["href"].split("/")[1] 
                        print(f"Domain {domain}")
                        solve_links.append(link["href"])
                    if "wikipedia" not in link["href"]:
                        if "0.cloud.chals.io" not in link["href"]:
                            links.append(link["href"])

        print(solve_links, binary_links)
        return binary_links, solve_links
    else:
        print(f"Request failed with status code {response.status_code}")

def download_file(url, destination):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded {url} to {destination}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")


def get_writeups_by_tag():

    print("Enter the tags for your writeups:")


if __name__ == "__main__":

    writeup_num = 37910
    resp = get_writeup(writeup_num)
    get_info(resp)
    #print(resp.text)
    binary_links, solve_links = get_links(resp)

    base = os.getenv("CTF")

    for link in binary_links:
        file = link.split("/")[-1]
        destination_path = base + file
        download_file(link, destination_path)

    for link in solve_links:
        file = link.split("/")[-1]
        destination_path = base + file
        #link =  f"https://ctftime.org/writeup/{writeup_num}/" + file
        download_file(link, destination_path)
