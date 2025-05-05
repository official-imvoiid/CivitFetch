# CivitAI Toolkit

A collection of tools to download models and images from CivitAI.

## Tools

1. **CiviFetch.py**  
   - Download models (single or bulk) from CivitAI.  
   - Catalog metadata (name, tags, hashes, NSFW status) into an Excel file.  
   - Handle SFW/NSFW filtering and retry failed downloads.  

2. **ImgPull.py**  
   - Download images from a model's gallery.  
   - Filter by SFW/NSFW content.  
   - ⚠️ **Does not support GIFs or videos.**  

---

## Prerequisites
- Python 3.8+  
- CivitAI API key ([get it here](https://civitai.com/user/account))  
- Required libraries:  
  ```bash
  pip install requests pandas tqdm openpyxl Pillow