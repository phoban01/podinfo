import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import hashlib

def generate_hash(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        file_hash = hashlib.md5(data).hexdigest()

        return file_hash

def download_asset(asset_url, output_dir):
    response = requests.get(asset_url, stream=True)

    if response.status_code == 200:
        file_name = os.path.basename(urlparse(asset_url).path)
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        # Generate a hash for the downloaded file
        file_hash = generate_hash(file_path)

        # Rename the file with the hash suffix
        file_ext = os.path.splitext(file_name)[1]
        new_file_name = f"{file_hash}{file_ext}"
        new_file_path = os.path.join(output_dir, new_file_name)
        os.rename(file_path, new_file_path)

        return new_file_name
    else:
        print(f"Failed to download asset: {asset_url}")

        return None

def download_assets(html_file_path, output_dir):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    asset_tags = soup.find_all(['link', 'script', 'img'])

    downloaded_assets = []

    for tag in asset_tags:
        if tag.has_attr('href'):
            asset_url = tag['href']

            if asset_url.startswith(('http://', 'https://')):
                downloaded_asset = download_asset(asset_url, output_dir)

                if downloaded_asset:
                    tag['href'] = downloaded_asset
                    downloaded_assets.append(downloaded_asset)
        elif tag.has_attr('src'):
            asset_url = tag['src']

            if asset_url.startswith(('http://', 'https://')):
                downloaded_asset = download_asset(asset_url, output_dir)

                if downloaded_asset:
                    tag['src'] = downloaded_asset
                    downloaded_assets.append(downloaded_asset)

    updated_html = soup.prettify()

    # Save the updated HTML to a file
    output_file_path = os.path.join(output_dir, 'index.html')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(updated_html)

    return downloaded_assets

def main():
    html_file_path = './ui/vue.html'  # Replace with the path to your HTML file
    output_directory = './pkg/assets/ui'  # Replace with the desired output directory

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    downloaded_assets = download_assets(html_file_path, output_directory)

    if downloaded_assets:
        print("Assets downloaded successfully:")

        for asset in downloaded_assets:
            print(asset)
    else:
        print("No assets downloaded.")

if __name__ == '__main__':
    main()
