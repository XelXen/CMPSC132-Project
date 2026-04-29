# LaptopScrappy

A simple command-line tool to scrape and browse laptop listings from B&H Photo Video.

## Features

- Search laptops by keyword
- Sort results using multiple criteria (price, rating, newest, etc.)
- Paginated browsing (next/previous navigation)
- Displays:
  - Name
  - Price
  - Key features
  - Rating and review count (if available)

## Installation

### Prerequisites

- Python 3.10+
- Install required packages:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the program:

```bash
python main.py
```

You’ll enter an interactive shell.

## Commands

### `view <query> <sort>`

View laptops with optional search and sorting.

Examples:

```bash
view
view asus rog
view asus rog SORT_PRICE_LOW_TO_HIGH
view SORT_BEST_SELLERS
```

### `sort`

List all available sorting options.

### `help`

Show help menu.

### `exit` / `quit`

Exit the program.

## Sorting Options

```
SORT_FEATURED
SORT_BEST_SELLERS
SORT_PRICE_LOW_TO_HIGH
SORT_PRICE_HIGH_TO_LOW
SORT_TOP_RATED
SORT_MOST_RATED
SORT_BRAND_A_TO_Z
SORT_BRAND_Z_TO_A
SORT_NEWEST
```

## Navigation (inside view mode)

```
n → next page
p → previous page
e → exit view mode
```

## Notes

- Scraping depends on the website structure and may break if the site updates.
- Results are fetched live, so speed depends on network latency.
- No caching or rate limiting is implemented.
