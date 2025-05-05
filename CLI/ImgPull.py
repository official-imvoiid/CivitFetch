import os
import re
import sys
import time
import requests
from io import BytesIO
from PIL import Image
from typing import Dict, Tuple, Optional, Any
from requests.exceptions import RequestException, Timeout, ConnectionError

# Constants
API_BASE = "https://civitai.com/api/v1"
MAX_RETRIES = 5
RETRY_DELAY = 3
ROOT_FOLDER = "CivitImg"
REQUEST_TIMEOUT = 30

class CivitaiDownloader:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {'Authorization': f'Bearer {api_key}'}
        os.makedirs(ROOT_FOLDER, exist_ok=True)
    
    def prompt_mode(self) -> Dict[str, str]:
        """Prompt user for download mode."""
        while True:
            print("\n=== Download Mode ===")
            print("1) SFW only")
            print("2) NSFW only")
            print("3) Exit")
            
            try:
                choice = input("Choice: ").strip()
                if choice == '1': 
                    return {'nsfw': 'false'}
                elif choice == '2': 
                    return {'nsfw': 'true'}
                elif choice == '3':
                    print("Exiting program")
                    sys.exit(0)
                else:
                    print("Invalid choice. Please try again.")
            except KeyboardInterrupt:
                print("Program interrupted by user")
                sys.exit(0)
    
    def parse_url(self, url: str) -> Tuple[str, Optional[str]]:
        """Parse model ID and version ID from URL."""
        model_match = re.search(r"/models/(\d+)", url)
        version_match = re.search(r"modelVersionId=(\d+)", url)
        
        if not model_match:
            print("Invalid model URL format")
            raise ValueError("Error: Invalid model URL format. Expected URL like https://civitai.com/models/XXXXX")
            
        model_id = model_match.group(1)
        version_id = version_match.group(1) if version_match else None
        
        return model_id, version_id
    
    def make_api_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict:
        """Make API request with retry logic."""
        url = f"{API_BASE}/{endpoint}"
        retries = 0
        
        while retries < MAX_RETRIES:
            try:
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    params=params,
                    timeout=REQUEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429 or response.status_code == 524:
                    # Rate limiting
                    wait_time = int(response.headers.get('Retry-After', RETRY_DELAY))
                    print(f"Rate limit hit. Waiting {wait_time}s before retry.")
                    time.sleep(wait_time)
                    retries += 1
                elif response.status_code == 404:
                    print(f"Resource not found: {url}")
                    raise ValueError(f"Resource not found at {url}")
                else:
                    print(f"API request failed with status code: {response.status_code}")
                    if retries >= MAX_RETRIES - 1:
                        raise ConnectionError(f"Failed after {MAX_RETRIES} attempts. Last status: {response.status_code}")
                    retries += 1
                    time.sleep(RETRY_DELAY)
                    
            except (ConnectionError, Timeout) as e:
                print(f"Connection issue: {str(e)}. Retrying in {RETRY_DELAY}s...")
                if retries >= MAX_RETRIES - 1:
                    raise ConnectionError(f"Connection failed after {MAX_RETRIES} attempts: {str(e)}")
                retries += 1
                time.sleep(RETRY_DELAY)
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                raise
        
        raise ConnectionError(f"Failed to connect after {MAX_RETRIES} attempts")
    
    def fetch_model_info(self, model_id: str, version_id: Optional[str] = None) -> Dict:
        """Fetch model information including name."""
        try:
            if version_id:
                # Get specific version info
                version_data = self.make_api_request(f"model-versions/{version_id}")
                model_data = self.make_api_request(f"models/{model_id}")
                
                # Combine relevant info
                return {
                    "model_name": model_data.get("name", f"model_{model_id}"),
                    "version_name": version_data.get("name", f"version_{version_id}")
                }
            else:
                # Get model info only
                model_data = self.make_api_request(f"models/{model_id}")
                return {
                    "model_name": model_data.get("name", f"model_{model_id}"),
                    "version_name": None
                }
        except Exception as e:
            print(f"Error fetching model info: {str(e)}")
            return {
                "model_name": f"model_{model_id}",
                "version_name": f"version_{version_id}" if version_id else None
            }
    
    def sanitize_filename(self, name: str) -> str:
        """Sanitize string for use as filename."""
        # Remove invalid filename characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
        # Truncate to reasonable length
        return sanitized[:100]
    
    def download_image(self, url: str, filepath: str) -> bool:
        """Download and save an image with error handling."""
        retries = 0
        while retries < MAX_RETRIES:
            try:
                response = requests.get(url, stream=True, timeout=REQUEST_TIMEOUT)
                if not response.ok:
                    print(f"Failed to download image (HTTP {response.status_code}): {url}")
                    retries += 1
                    time.sleep(RETRY_DELAY)
                    continue
                
                # Process and save the image
                img = Image.open(BytesIO(response.content))
                img.convert("RGBA").save(filepath, "PNG")
                return True
                
            except Timeout:
                print(f"Timeout downloading image: {url}. Retrying...")
                retries += 1
                time.sleep(RETRY_DELAY)
            except ConnectionError:
                print(f"Connection error downloading image: {url}. Retrying...")
                retries += 1
                time.sleep(RETRY_DELAY)
            except Exception as e:
                print(f"Error processing image {url}: {str(e)}")
                return False
        
        print(f"Failed to download image after {MAX_RETRIES} attempts: {url}")
        return False
    
    def download_gallery(self, model_id: str, version_id: Optional[str], model_name: str, filters: Dict[str, str]) -> None:
        """Download all images from a model's gallery."""
        params = {
            'modelId': model_id,
            'limit': 200,
            'page': 1,
            **filters
        }
        
        if version_id:
            params['modelVersionId'] = version_id
        
        # Create model subfolder
        model_folder = os.path.join(ROOT_FOLDER, self.sanitize_filename(model_name))
        os.makedirs(model_folder, exist_ok=True)
        
        total_images = 0
        failed_images = 0
        
        try:
            while True:
                try:
                    print(f"Fetching page {params['page']} of gallery images...")
                    response_data = self.make_api_request("images", params)
                    
                    items = response_data.get('items', [])
                    if not items:
                        print("No more images available")
                        break
                    
                    print(f"Processing {len(items)} images from page {params['page']}")
                    
                    for i, img in enumerate(items):
                        url = img.get('url')
                        if not url:
                            print(f"Missing URL for image at index {i}")
                            continue
                        
                        # Extract original filename but use model name as prefix
                        base_filename = os.path.splitext(url.split('/')[-1])[0]
                        img_filename = f"{self.sanitize_filename(model_name)}_{base_filename}.png"
                        img_path = os.path.join(model_folder, img_filename)
                        
                        # Skip if file already exists
                        if os.path.exists(img_path):
                            print(f"Skipping existing file: {img_filename}")
                            continue
                        
                        # Download the image
                        print(f"Downloading: {img_filename}")
                        success = self.download_image(url, img_path)
                        
                        if success:
                            total_images += 1
                        else:
                            failed_images += 1
                    
                    # Check for next page
                    if len(items) < params['limit']:
                        print("Reached end of gallery")
                        break
                    
                    # Move to next page
                    params['page'] += 1
                    
                except KeyboardInterrupt:
                    print("Process interrupted by user")
                    break
                    
        except Exception as e:
            print(f"Error during gallery download: {str(e)}")
        
        print(f"Download complete: {total_images} images saved to {model_folder}/")
        if failed_images > 0:
            print(f"Failed to download {failed_images} images")

def main():
    try:
        print("\n=== CivitAI Gallery Downloader ===")
        api_key = input("API key: ").strip()
        
        if not api_key:
            print("Error: API key is required")
            return
        
        downloader = CivitaiDownloader(api_key)
        
        url = input("Model gallery URL: ").strip()
        if not url:
            print("Error: Model URL is required")
            return
        
        # Get filters (SFW/NSFW)
        filters = downloader.prompt_mode()
        
        # Parse URL
        try:
            model_id, version_id = downloader.parse_url(url)
            print(f"Model ID: {model_id}, Version ID: {version_id if version_id else 'None'}")
        except ValueError as e:
            print(str(e))
            return
        
        # Get model info including name
        try:
            model_info = downloader.fetch_model_info(model_id, version_id)
            model_name = model_info["model_name"]
            print(f"Model name: {model_name}")
        except Exception as e:
            print(f"Error: Failed to get model name: {str(e)}. Using default.")
            model_name = f"model_{model_id}"
        
        # Start download
        print(f"\nStarting download for: {model_name}")
        print(f"Images will be saved to: {ROOT_FOLDER}/{downloader.sanitize_filename(model_name)}/")
        
        downloader.download_gallery(model_id, version_id, model_name, filters)
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()