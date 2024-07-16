import os
import requests
import zipfile
import mimetypes

# URLs to download the Minecraft world maps
world_urls = {
    "expansive_fantasy_survival": "https://www.planetminecraft.com/project/expansive-fantasy-survival-15k-x-15k-adventure-survival-map/download/mirror/706763/",
    "kingdom": "https://www.curseforge.com/minecraft/worlds/the-kingdom-an-incredible-medieval-town/download/4631707",
    "saturns_orbit": "https://www.minecraftmaps.com/?task=download.send&id=50204:saturns-orbit&catid=2",
    "bessemer_city": "https://www.minecraftmaps.com/city?task=download.send&id=42123:bessemer-city&catid=13",
    "legend_of_the_blue_tide": "https://www.minecraftmaps.com/adventure?task=download.send&id=36166:the-legend-of-the-blue-tide-episode-i-the-myrefall-flats&catid=2"
}

# Base directory to store the world maps
base_dir = "/data/worlds"

def download_file(url, dest_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()  # Raise HTTPError for bad responses
    with open(dest_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    return dest_path

def extract_file(file_path, extract_to):
    # Determine the file type
    file_type, encoding = mimetypes.guess_type(file_path)
    print(f"File type of {file_path}: {file_type}")
    if file_type == 'application/zip':
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    else:
        print(f"Unsupported file type for {file_path}: {file_type}")
        raise ValueError(f"Unsupported file type: {file_type}")

def setup_world(world_name, url):
    try:
        world_dir = os.path.join(base_dir, world_name)
        # Create the directory if it doesn't exist
        if not os.path.exists(world_dir):
            os.makedirs(world_dir)
        
        # Download the world file
        file_path = os.path.join(world_dir, 'temp.file')
        download_file(url, file_path)

        # Extract the file if it is a zip file
        extract_file(file_path, world_dir)
        
        # Remove the downloaded file after extraction
        os.remove(file_path)

        print(f"Setup complete for {world_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
    except zipfile.BadZipFile as e:
        print(f"Error extracting {file_path}: {e}")
    except ValueError as e:
        print(f"Unsupported file type for {world_name}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    try:
        # Ensure the base directory exists
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        
        # Download and setup each world
        for world_name, url in world_urls.items():
            setup_world(world_name, url)
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()