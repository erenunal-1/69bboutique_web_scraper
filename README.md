# 69B Boutique Web Scraper

A Python web scraper for extracting product information from 69bboutique.com.

![69B Boutique](69bboutique.png)

## Overview

This scraper navigates through the pages of 69bboutique.com to gather details about each product, including product name, price, available sizes, collection name, collection description, and fabric type.

## Features

- Scrapes product information from each page of the website.
- Converts the scraped data into a pandas DataFrame for further analysis.
- Handles multiple pages by dynamically finding the total number of pages.
- Includes error handling for network requests and data extraction.

## Setup and Usage

### Requirements
- Python 3.6 or higher
- Required Python packages listed in `requirements.txt`

### Installation

1. Clone the repository:

```sh
git clone https://github.com/erenunal-1/69bboutique_scraper.git
cd 69bboutique_scraper

2. Install the required packages:

```sh
pip install -r requirements.txt
```

## Running the Script
