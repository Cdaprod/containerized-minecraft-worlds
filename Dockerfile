import os
import requests
import zipfile

# URLs to download the Minecraft world maps
world_urls = {
    "expansive_fantasy_survival": "https://example.com/path/to/expansive_fantasy_survival.zip",
    "radiant_city": "https://example.com/path/to/radiant_city.zip",
    "onechunk_survival": "https://example.com/path/to/onechunk_survival.zip",
    "kingdom": "https://example.com/path/to/kingdom.zip",
}

# Base directory to store the world maps
base_dir = "/data/worlds"

def download_and_extract(url, extract_to):
    # Download the file
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        zip_path = os.path.join(extract_to, 'temp.zip')
        with open(zip_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        # Remove the zip file after extraction
        os.remove(zip_path)
    else:
        print(f"Failed to download file from {url}")

def setup_world(world_name, url):
    world_dir = os.path.join(base_dir, world_name)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(world_dir):
        os.makedirs(world_dir)
    
    # Download and extract the world
    download_and_extract(url, world_dir)
    
    print(f"Setup complete for {world_name}")

def main():
    # Ensure the base directory exists
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Download and setup each world
    for world_name, url in world_urls.items():
        setup_world(world_name, url)

if __name__ == "__main__":
    main()