import os
import requests
import zipfile

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

def download_and_extract(url, extract_to):
    try:
        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses
        zip_path = os.path.join(extract_to, 'temp.zip')
        with open(zip_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        # Remove the zip file after extraction
        os.remove(zip_path)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        raise
    except zipfile.BadZipFile as e:
        print(f"Error extracting {zip_path}: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def setup_world(world_name, url):
    try:
        world_dir = os.path.join(base_dir, world_name)
        # Create the directory if it doesn't exist
        if not os.path.exists(world_dir):
            os.makedirs(world_dir)
        
        # Download and extract the world
        download_and_extract(url, world_dir)
        
        print(f"Setup complete for {world_name}")
    except Exception as e:
        print(f"Error setting up world {world_name}: {e}")

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