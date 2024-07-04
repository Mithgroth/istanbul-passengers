import os
import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the webpage content
url = "https://data.ibb.gov.tr/dataset/hourly-public-transport-data-set"
response = requests.get(url)
response.raise_for_status()  # Ensure we notice bad responses

# Step 2: Parse the webpage to find all `a` tags with the class `btn-dwnld`
soup = BeautifulSoup(response.text, 'html.parser')
download_links = soup.find_all('a', class_='btn-dwnld')

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

total_files = 0
downloaded_files = 0
skipped_files = 0

# Step 3: Extract the `href` attributes and download each CSV file
for link in download_links:
    href = link.get('href')
    if href and href.endswith('.csv'):  # Just to be sure we get only CSV links
        total_files += 1
        # Construct the full URL
        file_url = href if href.startswith('http') else f'https://data.ibb.gov.tr{href}'
        
        # Get the file name from the URL
        file_name = os.path.join('data', os.path.basename(file_url))
        
        # Check if the file already exists
        if os.path.exists(file_name):
            print(f"File {file_name} already exists, skipping download.")
            skipped_files += 1
            continue
        
        # Step 4: Download and save the CSV file
        print(f"Downloading {file_name} ...")
        file_response = requests.get(file_url)
        file_response.raise_for_status()  # Ensure we notice bad responses

        with open(file_name, 'wb') as file:
            file.write(file_response.content)
        downloaded_files += 1
        print(f"Saved to {file_name}")

print(f"Total files available: {total_files}")
print(f"Files downloaded: {downloaded_files}")
print(f"Files skipped: {skipped_files}")
