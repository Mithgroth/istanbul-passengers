import os
import requests
from bs4 import BeautifulSoup

def fetch_webpage_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return response.text

def parse_download_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find_all('a', class_='btn-dwnld')

def download_csv_files(download_links, download_dir='data'):
    # Ensure the data directory exists
    os.makedirs(download_dir, exist_ok=True)

    total_files = 0
    downloaded_files = 0
    skipped_files = 0

    for link in download_links:
        href = link.get('href')
        if href and href.endswith('.csv'):  # Just to be sure we get only CSV links
            total_files += 1
            # Construct the full URL
            file_url = href if href.startswith('http') else f'https://data.ibb.gov.tr{href}'
            
            # Get the file name from the URL
            file_name = os.path.join(download_dir, os.path.basename(file_url))
            
            # Check if the file already exists
            if os.path.exists(file_name):
                skipped_files += 1
                continue
            
            # Download and save the CSV file
            print(f"Downloading {file_name} ...")
            file_response = requests.get(file_url)
            file_response.raise_for_status()  # Ensure we notice bad responses

            with open(file_name, 'wb') as file:
                file.write(file_response.content)
            downloaded_files += 1
            print(f"Saved to {file_name}")

    return total_files, downloaded_files, skipped_files

def fetch(url):
    html_content = fetch_webpage_content(url)
    download_links = parse_download_links(html_content)
    return download_csv_files(download_links)
