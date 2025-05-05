# CivitAI Fetch Toolkit

This toolkit provides command-line (CLI) and graphical user interface (GUI) tools for interacting with CivitAI, allowing you to download models and images.

## Overview

The toolkit consists of two main ways to achieve the same goal:

1.  **CLI (Command Line Interface):** Located in the `CLI` folder. This offers a more manual and flexible way to download models and images using Python scripts (`CiviFetch.py`, `ImgPull.py`) directly from your terminal or via the provided `CLI.bat` batch file.
2.  **GUI (Graphical User Interface):** Located in the `GUI` folder. This provides a standalone application (`app.py`) with a web-based graphical interface, launched via `webui.bat`. It includes the core functionalities of the CLI tools with an integrated README section.

The `Interfaces` folder contains screenshots of the CLI and GUI applications for visual reference.

## Features

* **Model Downloader (`CiviFetch.py` / GUI Tab):**
    * Download CivitAI models individually or in bulk using URLs or model IDs.
    * Creates an Excel report (`.xlsx`) in the `CivitData` folder, cataloging metadata like model name, tags, trigger words, base model, hashes (SHA256, AutoV1), file size, and NSFW status.
    * Handles SFW/NSFW filtering based on user preference and model tags.
    * Saves downloaded models to the `CivitModels` folder.
    * Provides download progress and status updates.
* **Image Downloader (`ImgPull.py` / GUI Tab):**
    * Download images from a specific CivitAI model's gallery.
    * Filter images based on SFW/NSFW preference.
    * Saves downloaded images to the `CivitImg` folder, organized by model name.
    * *Note:* Currently does not support GIF or video downloads.

## Installation

1.  Ensure you have Python 3.8+ installed.
2.  Run the `Install_requirements.bat` script. This will install the necessary Python libraries listed in `requirements.txt` using pip.
    ```bash
    # Alternatively, install manually:
    pip install -r requirements.txt
    ```

## Usage

### Prerequisites

* **CivitAI API Key:** You need an API key from your CivitAI account settings ([https://civitai.com/user/account](https://civitai.com/user/account)). This key is required for both CLI and GUI tools.

### CLI

1.  Navigate to the `CLI` directory in your terminal.
2.  **Model Download (`CiviFetch.py`):**
    * Run `python CiviFetch.py`.
    * Follow the prompts to enter your API key, choose single or bulk mode, provide model URLs/IDs (or a text file path for bulk), and decide whether to download NSFW models.
3.  **Image Download (`ImgPull.py`):**
    * Run `python ImgPull.py`.
    * Follow the prompts to enter your API key, the model gallery URL, and choose the SFW/NSFW download mode.
4.  **Batch File (`CLI.bat`):** (You may need to customize this batch file depending on how you want it to run the Python scripts).

### GUI

1.  Navigate to the `GUI` directory.
2.  Run the `webui.bat` script. This will launch the Gradio web interface in your browser.
3.  Enter your API Key in the respective tab ('Model Download' or 'Image Download').
4.  Follow the instructions within the GUI:
    * **Model Download:** Choose single/bulk, provide URL/ID or upload a `.txt` file, select content filter, and click "Start Download".
    * **Image Download:** Provide the model gallery URL, select the content filter, and click "Download Images".
5.  A 'README' tab is also available within the GUI application itself.

## Disclaimer & Terms of Use

* **Private Use Only:** This toolkit is intended strictly for personal, private use. Redistribution is not permitted.
* **Respect CivitAI ToS:** Users are solely responsible for adhering to CivitAI's Terms of Service and any applicable laws regarding the download, use, and distribution of AI models and images.
* **Developer Responsibility:** The developer (Shido/Voiid) is not responsible or liable for any actions taken by users with this tool or for the content downloaded using it. Use it responsibly and legally.
* **NSFW Content:** This tool *may* download NSFW content if your CivitAI account/API key has NSFW enabled *and* the content is not explicitly tagged as NSFW on CivitAI. Tagging can be inconsistent. To avoid NSFW content, ensure it is disabled in your CivitAI account and API key settings. Always review downloaded content.

## License

This project is licensed under the MIT License. See the `LICENSE.txt` file for details.
