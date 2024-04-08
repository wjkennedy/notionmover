# Notion to Confluence Migration Tool

This Python script facilitates the automated migration of directories and files from a Notion export to Confluence spaces and pages. It is designed to recreate the directory structure of exported Notion content as spaces in Confluence, where Markdown files become Confluence pages and other file types are uploaded as attachments.

![](screenshot.png)

## Features

- **Automatic Space Creation**: Each directory in the export is created as a new Confluence space.
- **Page Creation from Markdown**: Markdown files are converted to Confluence pages.
- **Attachments**: Non-Markdown files are uploaded as attachments to the nearest Confluence page.
- **UUID Cleaning**: Removes UUIDs from file and directory names to clean up space and page titles in Confluence.

## Prerequisites

- Python 3.6 or higher
- Notion Export
- Confluence Cloud API access
- `requests` library for Python
- Access rights to create spaces and pages in your Confluence instance

## Setup

### 1. Clone the Repository

Clone this repository to your local machine.

### 2. Install Dependencies

Install the required Python packages by running:

    pip install requests markdown

### 3. Configure API Access

Edit the script to include your Confluence domain, API username, and API token:

Open notionmover.py with a text editor.

Find the base_url, username, and api_token variables.

Replace 'https://your-domain.atlassian.net/wiki', 'email@example.com', and 'your_api_token' with your actual Confluence API information.

4. Prepare Your Export

Ensure your Notion export is uncompressed and organized in a directory structure where:

- Each subdirectory represents a space.
- Markdown files are pages.
- Other files are attachments.

### Usage

Run the script from your terminal or command prompt:

    python3 notionmover.py

Make sure to set the root_directory variable in the script to the path where your Notion export is located.

### Troubleshooting

Authentication Errors: Ensure your API token is correct and has the necessary permissions.

File Not Found: Check the paths specified in the script are correct and accessible.

Rate Limits: If you encounter rate limiting by the Confluence API, you may need to add pauses or retry logic in the script.

### Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your improvements.

### License

This project is licensed under the MIT License
