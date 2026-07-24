import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(source): return nbf.v4.new_markdown_cell(source)
def code(source): return nbf.v4.new_code_cell(source)

# ─── SECTION 1 ─────────────────────────────────────────────
cells.append(md("""# 📰 Ethiopian Business News Scraper
## A Complete End-to-End Data Engineering Project in Python

**Source:** [New Business Ethiopia](https://newbusinessethiopia.com/)

---

> *"Data is the new oil — but only if you can find it, refine it, and use it."*

Welcome to this hands-on Data Engineering project! By the end of this notebook, you will have scraped real news articles from an Ethiopian business news website, cleaned and transformed the data, stored it in multiple formats, and extracted business insights using visualizations and Natural Language Processing (NLP).

This notebook is structured like a university bootcamp tutorial. **Every line of code is explained in beginner-friendly language.** No steps are skipped.

---

## Section 1: Project Introduction

### 🌐 What is Web Scraping?

**Web scraping** is the automated process of extracting information from websites. Instead of manually reading hundreds of web pages, we write a Python program that:

1. Visits a webpage (just like a browser does)
2. Reads the HTML code of that page
3. Finds the specific data we want (headlines, dates, authors, etc.)
4. Saves that data for further use

Think of it as a robot that reads thousands of newspaper pages and records the key facts in seconds.

---

### 🏗️ What is Data Engineering?

**Data Engineering** is the practice of designing, building, and maintaining systems that collect, store, and prepare data for analysis. A Data Engineer's job is to make sure that:
- Raw data is collected reliably from various sources
- Data is cleaned and standardized
- Data is stored in the right format and place
- Data is ready for analysts and data scientists to use

---

### 🔄 What is ETL?

**ETL** stands for **Extract → Transform → Load** — the three core steps of any data pipeline:

| Step | Meaning | In This Project |
|------|---------|-----------------|
| **Extract** | Collect raw data from a source | Scraping articles from the website |
| **Transform** | Clean, reshape, and enrich the data | Removing duplicates, cleaning text, parsing dates |
| **Load** | Store the data somewhere useful | Saving to CSV, JSON, and SQLite database |

---

### 💼 Why This Project is Useful

Ethiopia is one of the fastest-growing economies in Africa. Understanding business news from Ethiopian sources helps:
- **Investors** identify which sectors are attracting attention and capital
- **Entrepreneurs** spot emerging trends and opportunities
- **Researchers** study media coverage patterns and economic narratives
- **Policymakers** gauge public perception of key economic sectors

The website [newbusinessethiopia.com](https://newbusinessethiopia.com/) covers: Investment, Mining, Energy, Finance, Trade, Health, and more — making it a rich source of business intelligence.

---

### 📊 Business Insights We Can Gain

By scraping and analyzing this website we can answer:
- Which business sectors get the most coverage in Ethiopian media?
- Is the tone of financial news generally positive or negative?
- Which topics are trending this month?
- Who are the most active business journalists?
- How has coverage of specific sectors changed over time?

---
> **Let's get started! 🚀**
"""))

# ─── SECTION 2 ─────────────────────────────────────────────
cells.append(md("""---
## Section 2: Install Required Libraries

### What Are Libraries?

A **library** (also called a **package** or **module**) is a collection of pre-written code that gives your program extra capabilities. We use `pip` (Python's package manager) to install them.

### Library Reference Table

| Library | Purpose | ETL Stage |
|---------|---------|-----------|
| `requests` | Fetches web page HTML over the internet | Extract |
| `beautifulsoup4` | Parses HTML to find specific elements | Extract |
| `lxml` | Fast HTML parser (used by BeautifulSoup) | Extract |
| `pandas` | Stores and manipulates data in table form | Transform |
| `sqlite3` | Built-in Python module for SQLite databases | Load |
| `os` | Interacts with the file system | All |
| `time` | Pauses execution between requests | Extract |
| `datetime` | Handles date and time values | Transform |
| `re` | Regular expressions — text pattern matching | Transform |
| `langdetect` | Detects the language of a text string | Transform |
| `nltk` | Natural Language Toolkit — NLP operations | Analyze |
| `matplotlib` | Creates charts and visualizations | Analyze |
| `wordcloud` | Generates word cloud images from text | Analyze |
| `tqdm` | Shows progress bars for long-running loops | All |
| `newspaper3k` | Extracts full article text from news URLs | Extract |
| `Pillow` | Image processing (required by wordcloud) | Analyze |
| `scikit-learn` | Machine learning — topic modeling | Analyze |
| `textblob` | Simple NLP sentiment analysis | Analyze |
| `vaderSentiment` | Rule-based sentiment analyzer for news text | Analyze |

> **Note:** The `!` at the start of a Jupyter cell means "run this as a terminal command".
"""))

cells.append(code("""# Install all required libraries
# -q = quiet mode (less verbose output)
!pip install -q requests beautifulsoup4 pandas lxml tqdm langdetect \\
    newspaper3k matplotlib wordcloud Pillow scikit-learn nltk \\
    textblob vaderSentiment

print("✅ All libraries installed successfully!")
"""))

cells.append(md("""### 📖 Installation Explained

- `!pip install` — Calls pip from inside the Jupyter notebook using the `!` shell escape
- Each library name after `install` is downloaded from the Python Package Index (PyPI)
- The `\\` at the end of a line continues the command on the next line (line continuation)
- Multiple library names separated by spaces installs them all in one command

**ETL Contribution:** This step prepares our entire toolkit before any data work begins.
"""))

# ─── SECTION 3 ─────────────────────────────────────────────
cells.append(md("""---
## Section 3: Import Libraries

### What Does "Importing" Mean?

After installing a library, you **import** it into your Python script. Think of installation as buying a book, and importing as opening it to the relevant chapter.

### Why Import at the Top?

Standard Python practice puts all imports at the very top so:
- Anyone reading the code immediately knows what tools you're using
- If a library is missing, you get an error immediately (not mid-execution)

---
"""))

cells.append(code("""# ── Standard Library Imports (built into Python — no install needed) ──
import os           # File system: create folders, build file paths
import re           # Regular expressions: advanced text pattern matching
import time         # Time utilities: pause execution with time.sleep()
import json         # JSON format: read and write .json files
import sqlite3      # SQLite database: lightweight, file-based SQL
from datetime import datetime  # Date and time manipulation

# ── Third-Party Imports (installed via pip) ──
import requests                         # HTTP requests: fetch web page HTML
from bs4 import BeautifulSoup           # HTML parser: navigate and search HTML
import pandas as pd                     # Data manipulation: DataFrames
from tqdm import tqdm                   # Progress bars for loops

# ── Language Detection ──
from langdetect import detect, LangDetectException  # Detect text language

# ── NLP (Natural Language Processing) ──
import nltk
from nltk.corpus import stopwords       # Common words to ignore
from nltk.tokenize import word_tokenize # Split text into individual words
from collections import Counter         # Count occurrences of items

# ── Sentiment Analysis ──
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ── Topic Modeling ──
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

# ── Visualization ──
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from wordcloud import WordCloud

# ── Newspaper Article Extraction ──
from newspaper import Article

# ── Download NLTK Data Files ──
nltk.download('punkt',        quiet=True)  # Tokenizer model
nltk.download('stopwords',    quiet=True)  # List of common stop words
nltk.download('vader_lexicon',quiet=True)  # VADER sentiment dictionary
nltk.download('punkt_tab',    quiet=True)  # Additional tokenizer data

print("✅ All libraries imported successfully!")
"""))

cells.append(md("""### 📖 Line-by-Line Explanation

#### Standard Library (No Installation Needed)
- `import os` — Access operating system features. We use `os.makedirs()` (create folders), `os.path.join()` (build file paths), `os.path.getsize()` (file sizes).
- `import re` — Regular Expressions (regex): a powerful language for text pattern matching. Example: `re.sub(r"\\s+", " ", text)` collapses multiple spaces into one.
- `import time` — Time utilities. We use `time.sleep(1)` to pause 1 second between requests — being polite to web servers.
- `import json` — Read and write JSON files. `json.dump()` saves data, `json.load()` reads it back.
- `import sqlite3` — Python's built-in SQLite database library. No separate database server required.
- `from datetime import datetime` — The `datetime` class lets us parse date strings and format dates.

#### Third-Party Libraries
- `import requests` — Sends HTTP GET requests to websites and receives HTML responses.
- `from bs4 import BeautifulSoup` — Imported from the package named `bs4`. Builds a searchable tree structure from raw HTML.
- `import pandas as pd` — The `as pd` creates a short **alias** — `pd.DataFrame()` instead of `pandas.DataFrame()`.
- `from tqdm import tqdm` — Wrap any loop: `for item in tqdm(my_list):` adds a live progress bar.

#### NLTK Downloads
- `nltk.download('punkt')` — Sentence/word tokenizer statistical model.
- `nltk.download('stopwords')` — List of ~150 common English words (the, and, is, etc.) to exclude from analysis.
- `nltk.download('vader_lexicon')` — Dictionary of 7,500+ words rated for sentiment.
- `quiet=True` — Don't print download messages to keep output clean.

**ETL Contribution:** Imports establish our complete toolbox for all three ETL stages.
"""))

# ─── SECTION 4 ─────────────────────────────────────────────
cells.append(md("""---
## Section 4: Create Project Folder Structure

### Why Organize Files Into Folders?

A well-organized project is easier to maintain, share, and troubleshoot. This structure mirrors real-world Data Engineering pipelines:

```
project/
├── data/
│   ├── raw/          ← Exactly as scraped — NEVER modify this
│   ├── processed/    ← Cleaned, analysis-ready data
│   └── images/       ← Downloaded article featured images
├── database/         ← SQLite .db file
└── reports/          ← Charts, word clouds, analysis outputs
```

### Why Separate Raw and Processed Data?

| Raw Data | Processed Data |
|----------|---------------|
| Exactly as scraped — never modified | Cleaned, standardized, enriched |
| Your safety net if cleaning goes wrong | What analysts and dashboards consume |
| Equivalent to a **Data Lake** in enterprise | Equivalent to a **Data Warehouse** |

### Why Use a Database Instead of Just CSVs?

| CSV | SQLite Database |
|-----|----------------|
| Simple, universal | Supports SQL queries |
| No filtering built in | Fast WHERE/GROUP BY/JOIN |
| Entire file loads into memory | Reads only what you need |
| No data integrity rules | UNIQUE, NOT NULL constraints |

---
"""))

cells.append(code("""# Define all folder paths for this project
# os.path.join() builds file paths correctly on any OS
# Windows uses backslashes (data\\raw) — Mac/Linux use forward slashes (data/raw)
# os.path.join handles this automatically

FOLDERS = {
    "raw":       os.path.join("data", "raw"),         # Unmodified scraped data
    "processed": os.path.join("data", "processed"),   # Cleaned, transformed data
    "images":    os.path.join("data", "images"),       # Downloaded article images
    "database":  "database",                           # SQLite database file
    "reports":   "reports",                            # Charts and visualizations
}

# Create each folder
# exist_ok=True = don't raise an error if the folder already exists
# This makes the script safe to run multiple times
for name, path in FOLDERS.items():
    os.makedirs(path, exist_ok=True)
    print(f"📁 Created (or verified): {path}/")

print("\\n✅ Project folder structure is ready!")
"""))

cells.append(md("""### 📖 Line-by-Line Explanation

- `FOLDERS = {...}` — A Python **dictionary** mapping readable names to file system paths. Using a dictionary means if we rename a folder, we only change it in one place.
- `os.path.join("data", "raw")` — Joins path components correctly for the current operating system. Always prefer this over manually writing `"data/raw"` which would fail on Windows.
- `for name, path in FOLDERS.items()` — Loops through every key-value pair. `.items()` returns pairs like `("raw", "data/raw")`. `name` gets the key, `path` gets the value.
- `os.makedirs(path, exist_ok=True)` — Creates the directory **and any missing parent directories**. The `exist_ok=True` parameter suppresses the error that would normally occur if the directory already exists.
- `f"📁 Created: {path}/"` — An **f-string** (formatted string literal). The `f` prefix allows inserting variable values with `{variable_name}` syntax.

**ETL Contribution:** Infrastructure setup — like laying pipes before turning on the water. All ETL stages depend on these folders existing.
"""))

# ─── SECTION 5 ─────────────────────────────────────────────
cells.append(md("""---
## Section 5: Understand the Website Structure

### How Do Websites Work?

Every webpage is built from **HTML** (HyperText Markup Language) — a structured text document your browser reads and renders visually. When we scrape, we read that HTML and extract the parts we want.

### Key HTML Elements

| Element | Description | Example |
|---------|------------|---------|
| `<div>` | A container/box for grouping content | `<div class="article">...</div>` |
| `<a>` | A hyperlink | `<a href="/news/story">Read more</a>` |
| `class` | A label for styling/targeting an element | `<div class="post-title">` |
| `<h1>`–`<h6>` | Headings of decreasing size | `<h2>Article Title</h2>` |
| `<p>` | A paragraph of text | `<p>Article body...</p>` |
| `<img>` | An image | `<img src="/image.jpg" alt="photo">` |
| `<span>` | An inline container | `<span class="author">John</span>` |
| `<article>` | Semantic tag for a news article | `<article>...</article>` |
| `<time>` | A date/time value | `<time datetime="2024-01-15">Jan 15</time>` |
| `href` | Attribute on `<a>` — the link destination URL | `href="https://example.com"` |

### How BeautifulSoup Navigates HTML

BeautifulSoup turns raw HTML into a searchable **tree structure**:

```python
soup.find("h1")                          # First <h1> element
soup.find("div", class_="entry-title")   # First <div class="entry-title">
soup.find_all("a")                       # ALL <a> elements
soup.select("article h2 a")             # CSS selector: <a> inside <h2> inside <article>
element["href"]                          # Value of the href attribute
element.get_text(strip=True)             # All visible text, whitespace stripped
element.get("href", "")                  # Attribute value, or "" if missing
```

---
"""))

cells.append(code("""# ── Define Global Constants ──

BASE_URL = "https://newbusinessethiopia.com"

# HTTP headers to mimic a real browser request
# Without this, some websites detect bots and block the request
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ── Helper Function: Safely Fetch a URL ──

def fetch_page(url, retries=3, delay=2):
    """
    Fetch a webpage and return a BeautifulSoup parse tree.
    
    Parameters:
        url     (str) : Full URL to fetch
        retries (int) : How many times to retry on failure (default 3)
        delay   (int) : Seconds to wait between retries (default 2)
    
    Returns:
        BeautifulSoup object, or None if all retries fail
    """
    for attempt in range(retries):   # Loop 0, 1, 2 (three attempts)
        try:
            # requests.get() sends an HTTP GET request — like typing a URL in a browser
            # timeout=15 means: give up if no response in 15 seconds
            response = requests.get(url, headers=HEADERS, timeout=15)
            
            # HTTP status codes:
            # 200 = OK (success)
            # 404 = Not Found
            # 403 = Forbidden (blocked)
            # 500 = Internal Server Error
            if response.status_code == 200:
                # BeautifulSoup parses the HTML bytes into a searchable tree
                # response.content = raw bytes; response.text = decoded string
                # Using .content is safer for non-UTF8 pages
                soup = BeautifulSoup(response.content, "lxml")
                return soup
            else:
                print(f"  ⚠️  HTTP {response.status_code} for: {url}")
                
        except requests.exceptions.Timeout:
            print(f"  ⏳ Attempt {attempt+1}/{retries} timed out.")
            time.sleep(delay)
            
        except requests.exceptions.ConnectionError:
            print(f"  🔌 Attempt {attempt+1}/{retries} — connection failed.")
            time.sleep(delay)
            
        except requests.exceptions.RequestException as e:
            # Catch ANY other requests-related error
            print(f"  ❌ Attempt {attempt+1}/{retries}: {e}")
            time.sleep(delay)
    
    return None   # All retries exhausted

# ── Test: Fetch and Inspect the Homepage ──
print(f"🌐 Fetching homepage: {BASE_URL}")
homepage_soup = fetch_page(BASE_URL)

if homepage_soup:
    title_tag = homepage_soup.find("title")
    print(f"✅ Page title: {title_tag.get_text() if title_tag else 'N/A'}")
    print(f"🔗 Total <a> links found: {len(homepage_soup.find_all('a'))}")
    print(f"🖼️  Total <img> tags found: {len(homepage_soup.find_all('img'))}")
    print(f"📝 Total <p> tags found:  {len(homepage_soup.find_all('p'))}")
    
    print("\\n📄 Sample HTML structure (first 600 characters):")
    print("-" * 50)
    print(str(homepage_soup)[:600])
else:
    print("❌ Failed to fetch homepage. Check your internet connection.")
"""))

cells.append(md("""### 📖 Line-by-Line Explanation

#### `BASE_URL` and `HEADERS`
- `BASE_URL` — A constant storing the website's root URL. Defined once at the top; used throughout the notebook. If the URL changes, you update it in exactly one place.
- `HEADERS["User-Agent"]` — Identifies our HTTP request as coming from a Chrome browser. Many websites check this header and block requests that don't look like real browsers. The string is a standard Chrome User-Agent string.

#### `def fetch_page(url, retries=3, delay=2):`
- `retries=3` — A **default parameter**. If you call `fetch_page(url)` without specifying retries, it uses 3. You can override it: `fetch_page(url, retries=5)`.
- `for attempt in range(retries):` — `range(3)` generates `[0, 1, 2]` — three iterations.

#### `requests.get(url, headers=HEADERS, timeout=15)`
- Sends an HTTP GET request (the same type your browser sends when you visit a URL)
- `headers=HEADERS` — Attaches our browser-like headers to the request
- `timeout=15` — Raises a `requests.exceptions.Timeout` error if no response in 15 seconds
- Returns a `Response` object with attributes like `.status_code`, `.content`, `.text`

#### `BeautifulSoup(response.content, "lxml")`
- `response.content` — The raw HTML as bytes (more reliable than `.text` for non-UTF-8 pages)
- `"lxml"` — Specifies the HTML parser to use. `lxml` is faster and more forgiving of malformed HTML than the built-in `html.parser`

#### Specific Exception Types
```python
except requests.exceptions.Timeout:     # Server too slow
except requests.exceptions.ConnectionError:  # No internet / DNS failure
except requests.exceptions.RequestException: # Any other network error
```
Catching specific exceptions lets us give more informative error messages and handle each case differently.

**ETL Contribution:** `fetch_page()` is the core **Extract** utility — every piece of data in this project flows through this function.
"""))

# ─── SECTION 6 ─────────────────────────────────────────────
cells.append(md("""---
## Section 6: Extract Category Links

### Why Do We Need Categories?

The website organizes articles into topic categories. Our strategy is a **multi-level crawl**:

```
Website Homepage
    └── Category: Investment  →  Article 1, Article 2, Article 3 ...
    └── Category: Finance     →  Article 4, Article 5, Article 6 ...
    └── Category: Energy      →  Article 7, Article 8, ...
    ...
```

Finding category URLs first gives us a structured map of the entire site.

### What We're Looking For in HTML

Category links in a WordPress site's navigation look like this:
```html
<li><a href="https://newbusinessethiopia.com/category/investment/">Investment</a></li>
```

We find them by searching for `<a>` tags whose `href` contains `/category/`.

---
"""))

cells.append(code("""def get_categories(soup):
    """
    Extract all category names and URLs from the website navigation.
    
    Parameters:
        soup : BeautifulSoup object of the homepage
    
    Returns:
        dict: {category_name: category_url}
    """
    categories = {}  # Dictionary to store name → URL mapping
    
    if soup is None:
        return categories
    
    # soup.find_all("a", href=True) finds all <a> tags that have an href attribute
    # href=True means: only include <a> tags that actually have an href (not <a name="...">)
    all_links = soup.find_all("a", href=True)
    
    for link in all_links:
        href = link.get("href", "")          # Get href value, default "" if missing
        text = link.get_text(strip=True)     # Get visible link text, strip whitespace
        
        # Filter: only category links
        # "/category/" appears in WordPress category page URLs
        if "/category/" in href and text and len(text) < 60:
            name = text.strip()
            if name and name not in categories:  # Prevent duplicates
                categories[name] = href
    
    return categories


# ── Run Category Extraction ──
print(f"🔍 Extracting categories from: {BASE_URL}\\n")
categories = get_categories(homepage_soup)

if categories:
    print(f"✅ Found {len(categories)} categories:\\n")
    for name, url in sorted(categories.items()):
        print(f"  📂 {name:30s} → {url}")
else:
    # Fallback: define known categories manually
    print("⚠️  Auto-detection found 0 categories. Using known fallback list.")
    categories = {
        "Investment":        f"{BASE_URL}/category/investment/",
        "Finance":           f"{BASE_URL}/category/finance/",
        "Trade":             f"{BASE_URL}/category/trade/",
        "Energy":            f"{BASE_URL}/category/energy/",
        "Mining":            f"{BASE_URL}/category/mining/",
        "Oil & Gas":         f"{BASE_URL}/category/oil-gas/",
        "Health":            f"{BASE_URL}/category/health/",
        "Politics":          f"{BASE_URL}/category/politics/",
        "Hospitality":       f"{BASE_URL}/category/hospitality/",
        "Culture & Tourism": f"{BASE_URL}/category/culture-tourism/",
        "Travel":            f"{BASE_URL}/category/travel/",
        "NBE Blog":          f"{BASE_URL}/category/nbe-blog/",
    }
    print(f"\\nUsing {len(categories)} fallback categories.")
    for name, url in categories.items():
        print(f"  📂 {name:30s} → {url}")
"""))

cells.append(md("""### 📖 Line-by-Line Explanation

- `soup.find_all("a", href=True)` — Finds all `<a>` elements. The `href=True` argument filters to only links that *have* an href attribute. This is equivalent to `soup.find_all("a", attrs={"href": True})`.

- `link.get("href", "")` — Safely gets an attribute value. If the attribute is missing, returns `""` instead of `None`. Using `link["href"]` would throw a `KeyError` if href is missing.

- `link.get_text(strip=True)` — Returns all visible text inside the element with whitespace stripped. For `<a href="..."> Investment </a>`, this returns `"Investment"`.

- `if "/category/" in href` — The Python `in` operator checks if a substring exists in a string. This is the quickest way to filter for category URLs.

- `len(text) < 60` — Category names shouldn't be very long. This filters out long navigation text that might accidentally match our filter.

- `if name and name not in categories` — Double check:
  1. `name` is not empty
  2. We haven't already added this category (prevents duplicates from repeated navigation items)

**ETL Contribution:** Identifies all data sources (category pages) we need to visit. This is the "mapping" phase of Extract.
"""))

# ─── SECTION 7 ─────────────────────────────────────────────
cells.append(md("""---
## Section 7: Scrape All Article URLs

### What is Pagination?

When a category has more articles than fit on one page, the site splits them across multiple pages — called **pagination**.

- Page 1: `https://newbusinessethiopia.com/category/investment/`
- Page 2: `https://newbusinessethiopia.com/category/investment/page/2/`
- Page 3: `https://newbusinessethiopia.com/category/investment/page/3/`

### Our Pagination Strategy

```
Start at page 1
  → Find all article links on this page
  → Look for a "Next Page" link
  → If found: follow it and repeat
  → If not found: we've reached the last page — stop
```

### Why Use a Set for Deduplication?

A Python `set` only stores **unique values**. If you try to add an item that's already in the set, it simply does nothing. This automatically prevents duplicate URLs.

```python
seen = set()
seen.add("url1")  # set = {"url1"}
seen.add("url2")  # set = {"url1", "url2"}
seen.add("url1")  # set = {"url1", "url2"} — no change!
```

---
"""))

cells.append(code("""def get_article_urls_from_category(category_url, category_name, max_pages=10):
    """
    Scrape all article URLs from one category, following pagination.
    
    Parameters:
        category_url  (str) : URL of the first page of the category
        category_name (str) : Human-readable name (for logging only)
        max_pages     (int) : Safety ceiling — stop after this many pages
    
    Returns:
        list: All article URLs found in this category
    """
    article_urls = []        # Collect all article URLs here
    visited_pages = set()    # Track visited pages to prevent infinite loops
    current_url   = category_url
    page_number   = 1
    
    # Pagination loop: keep going until no "next page" link or we hit max_pages
    while current_url and page_number <= max_pages:
        
        # Guard against loops (e.g., a page linking back to itself)
        if current_url in visited_pages:
            break
        visited_pages.add(current_url)  # Mark as visited BEFORE fetching
        
        soup = fetch_page(current_url)
        if soup is None:
            print(f"    ⚠️  Could not fetch page {page_number}")
            break
        
        page_new_count = 0
        
        # ── Strategy 1: CSS Selectors (WordPress article titles) ──
        # WordPress themes wrap article titles in heading tags inside .entry-title
        for selector in [
            "h2.entry-title a",   # <h2 class="entry-title"><a href="URL">Title</a></h2>
            "h3.entry-title a",
            ".entry-title a",     # Any element with class="entry-title" containing <a>
            "article h2 a",       # <article> containing <h2> containing <a>
            "article h3 a",
            ".post-title a",
            "h2.post-title a",
        ]:
            matches = soup.select(selector)  # CSS selector search — returns list
            for tag in matches:
                url = tag.get("href", "")
                # Only collect URLs from this domain and not already seen
                if url and BASE_URL in url and url not in article_urls:
                    article_urls.append(url)
                    page_new_count += 1
        
        # ── Strategy 2: Broad URL pattern matching (fallback) ──
        # If CSS selectors found nothing, look for any site link that isn't
        # a category, tag, or pagination page
        if page_new_count == 0:
            for link in soup.find_all("a", href=True):
                url = link.get("href", "")
                if (BASE_URL in url
                    and url not in article_urls
                    and "/category/" not in url   # Skip category index pages
                    and "/page/"     not in url   # Skip pagination pages
                    and "/tag/"      not in url   # Skip tag archive pages
                    and "/author/"   not in url   # Skip author archive pages
                    and url.rstrip("/") != BASE_URL  # Skip homepage
                ):
                    article_urls.append(url)
                    page_new_count += 1
        
        print(f"    📄 Page {page_number}: +{page_new_count} articles "
              f"(running total: {len(article_urls)})")
        
        # ── Find "Next Page" link ──
        next_url = None
        for selector in [
            "a.next.page-numbers",  # Standard WordPress: <a class="next page-numbers">
            ".nav-next a",          # Twenty themes navigation
            "a[rel='next']",        # HTML rel="next" — semantic navigation
            ".pagination a.next",   # Generic pagination class
            "a:contains('Next')",   # Any link with text "Next"
        ]:
            next_tag = soup.select_one(selector)  # Returns first match or None
            if next_tag:
                next_url = next_tag.get("href")
                if next_url:
                    break
        
        current_url = next_url   # None = no more pages = loop ends
        page_number += 1
        time.sleep(1.5)          # Polite delay between page requests
    
    return article_urls


# ── Collect Article URLs From All Categories ──
print("🕷️  Starting URL collection from all categories...")
print("=" * 60)

all_article_data = []  # List of {"url": ..., "category": ...} dicts
seen_urls = set()      # Global deduplication set (across ALL categories)

for category_name, category_url in tqdm(categories.items(), desc="Categories"):
    print(f"\\n📂 {category_name}")
    print(f"   {category_url}")
    
    urls = get_article_urls_from_category(category_url, category_name, max_pages=5)
    
    # Add unique URLs to master list
    added = 0
    for url in urls:
        if url not in seen_urls:
            seen_urls.add(url)
            all_article_data.append({"url": url, "category": category_name})
            added += 1
    
    print(f"   ✅ Added {added} new unique articles")

print("\\n" + "=" * 60)
print(f"🎯 Total unique article URLs: {len(all_article_data)}")

# Save URL list — so we don't need to re-crawl if the notebook restarts
url_file = os.path.join(FOLDERS["raw"], "article_urls.json")
with open(url_file, "w", encoding="utf-8") as f:
    json.dump(all_article_data, f, indent=2, ensure_ascii=False)
print(f"💾 URL list saved: {url_file}")
"""))

cells.append(md("""### 📖 Line-by-Line Explanation

#### The `while` Loop for Pagination
```python
while current_url and page_number <= max_pages:
```
Two conditions must BOTH be True to continue:
1. `current_url` is not `None` (there's still a next page to fetch)
2. `page_number <= max_pages` (safety: don't crawl forever)

When `current_url = None` (no next page found), the `while` condition becomes `False` and the loop ends.

#### `visited_pages.add(current_url)` Before Fetching
We add the URL to `visited_pages` *before* fetching it, not after. This prevents a race condition where the same URL could be processed twice if the code is modified to run concurrently.

#### `soup.select(selector)` vs `soup.find_all()`
- `soup.select("h2.entry-title a")` — Uses **CSS selector syntax**, like in web development
  - `h2.entry-title` = `<h2>` element with class `entry-title`
  - `a` = contains an `<a>` descendant
- `soup.find_all("a", href=True)` — Uses BeautifulSoup's own search API

CSS selectors are more powerful and concise for complex searches.

#### URL Filtering Logic
```python
and "/category/" not in url   # These are category index pages, not articles
and "/page/"     not in url   # These are pagination pages
and "/tag/"      not in url   # These are tag archive pages
```
Each condition removes a class of non-article URLs. Using `and` means ALL conditions must be True.

#### `soup.select_one(selector)`
Returns the **first** matching element (or `None`). Equivalent to `soup.select(selector)[0]` but safe when no match exists (`.select()[0]` would crash with an IndexError).

#### `json.dump(all_article_data, f, indent=2, ensure_ascii=False)`
- `indent=2` — Pretty-prints JSON with 2-space indentation (human-readable)
- `ensure_ascii=False` — Saves non-ASCII characters (Amharic, accented letters) as themselves instead of Unicode escape sequences (`\\u1234`)

**ETL Contribution:** Completes the URL discovery phase of **Extract** — we now have a complete map of all articles to visit.
"""))

# ─── SECTION 8 ─────────────────────────────────────────────
cells.append(md("""---
## Section 8: Scrape Article Details

### What We Extract From Each Article

| Field | Source in HTML | Notes |
|-------|---------------|-------|
| `headline` | `<h1 class="entry-title">` | Also in `og:title` meta tag |
| `date` | `<time datetime="2024-01-15">` | Also in `article:published_time` meta |
| `author` | `<span class="author">` or `[rel=author]` | Sometimes missing |
| `image_url` | `<meta property="og:image">` | Featured image URL |
| `content` | `<div class="entry-content">` | Full article text |
| `language` | Computed by `langdetect` | Detected from text |

### Error Handling Philosophy

In production scraping, **some pages will always fail**. They may have been deleted, temporarily down, or have an unexpected structure. Instead of crashing on the first error, we use `try-except` to skip bad pages gracefully.

```python
try:
    result = risky_operation()   # Code that MIGHT fail
except Exception as e:
    result = None                # Safe fallback value
    # The script continues — it doesn't crash!
```

---
"""))

cells.append(code("""def scrape_article(url, category):
    """
    Scrape all details from a single article page.
    
    Parameters:
        url      (str) : Full URL of the article page
        category (str) : Category (already known from our URL list)
    
    Returns:
        dict: All extracted fields, or None on complete failure
    """
    soup = fetch_page(url)
    if soup is None:
        return None   # fetch_page already printed an error message
    
    # Initialize with safe defaults
    # Using None means "we know this field exists but we didn't find a value"
    article = {
        "headline":   None,
        "category":   category,
        "url":        url,
        "source":     "New Business Ethiopia",
        "date":       None,
        "author":     None,
        "language":   None,
        "image_url":  None,
        "content":    None,
        "word_count": 0,
    }
    
    # ── Extract HEADLINE ──────────────────────────────────
    try:
        for selector in ["h1.entry-title", "h1.post-title", "h1.article-title", "h1"]:
            tag = soup.select_one(selector)
            if tag:
                article["headline"] = tag.get_text(strip=True)
                break  # Stop at the first match
        
        # Open Graph fallback: <meta property="og:title" content="Title Here">
        if not article["headline"]:
            og = soup.find("meta", property="og:title")
            if og:
                article["headline"] = og.get("content", "").strip()
    except Exception:
        pass   # Keep None default — don't crash
    
    # ── Extract PUBLICATION DATE ──────────────────────────
    try:
        # <time class="entry-date published" datetime="2024-01-15T10:30:00+03:00">
        # The datetime attribute is the machine-readable ISO format
        time_tag = soup.find("time")
        if time_tag:
            article["date"] = time_tag.get("datetime") or time_tag.get_text(strip=True)
        
        # Open Graph fallback: <meta property="article:published_time" content="2024-01-15">
        if not article["date"]:
            og_date = soup.find("meta", property="article:published_time")
            if og_date:
                article["date"] = og_date.get("content", "")
    except Exception:
        pass
    
    # ── Extract AUTHOR ────────────────────────────────────
    try:
        for selector in [".author a", ".entry-author a", "[rel='author']", ".post-author"]:
            tag = soup.select_one(selector)
            if tag:
                article["author"] = tag.get_text(strip=True)
                break
        
        # <meta name="author" content="John Smith">
        if not article["author"]:
            meta_author = soup.find("meta", attrs={"name": "author"})
            if meta_author:
                article["author"] = meta_author.get("content", "").strip()
    except Exception:
        pass
    
    # ── Extract FEATURED IMAGE URL ────────────────────────
    try:
        # Open Graph image: <meta property="og:image" content="https://site.com/img.jpg">
        og_img = soup.find("meta", property="og:image")
        if og_img:
            article["image_url"] = og_img.get("content", "").strip()
        
        # Fallback: first <img> in article content
        if not article["image_url"]:
            content_area = soup.select_one(".entry-content, .post-content, article")
            if content_area:
                img = content_area.find("img")
                if img:
                    article["image_url"] = img.get("src", "")
    except Exception:
        pass
    
    # ── Extract ARTICLE CONTENT ───────────────────────────
    try:
        content_text = ""
        
        for selector in [".entry-content", ".post-content", ".article-content", "article"]:
            content_div = soup.select_one(selector)
            if content_div:
                # Find all <p> (paragraph) tags and join their text
                paragraphs = content_div.find_all("p")
                if paragraphs:
                    content_text = "\\n".join(
                        p.get_text(strip=True) for p in paragraphs
                        if p.get_text(strip=True)   # Skip empty paragraphs
                    )
                else:
                    content_text = content_div.get_text(separator="\\n", strip=True)
                break
        
        # Fallback: newspaper3k (dedicated news article parser)
        if len(content_text) < 100:
            try:
                art = Article(url)
                art.download()
                art.parse()
                if art.text:
                    content_text = art.text
            except Exception:
                pass
        
        if content_text:
            article["content"]    = content_text
            article["word_count"] = len(content_text.split())
    except Exception:
        pass
    
    # ── Detect LANGUAGE ───────────────────────────────────
    try:
        sample = (article["headline"] or "") + " " + (article["content"] or "")[:300]
        if sample.strip():
            article["language"] = detect(sample)
    except LangDetectException:
        article["language"] = "unknown"
    
    return article


# ── Scrape All Articles ──
print(f"🕷️  Scraping {len(all_article_data)} article pages...")
print("=" * 60)

scraped_articles = []
failed_count     = 0

for item in tqdm(all_article_data, desc="Scraping"):
    article = scrape_article(item["url"], item["category"])
    
    if article and article["headline"]:
        scraped_articles.append(article)
    else:
        failed_count += 1
    
    time.sleep(1)   # 1-second polite delay between requests

print("\\n" + "=" * 60)
print(f"✅ Scraped successfully: {len(scraped_articles)}")
print(f"❌ Failed:              {failed_count}")

# Save raw data immediately
raw_file = os.path.join(FOLDERS["raw"], "articles_raw.json")
with open(raw_file, "w", encoding="utf-8") as f:
    json.dump(scraped_articles, f, indent=2, ensure_ascii=False)
print(f"\\n💾 Raw data saved: {raw_file}")

# Preview first article
if scraped_articles:
    print("\\n📰 First article preview:")
    for k, v in scraped_articles[0].items():
        display = str(v)[:100] + "..." if len(str(v or "")) > 100 else str(v)
        print(f"  {k:12s}: {display}")
"""))

cells.append(md("""### 📖 Line-by-Line Explanation

#### Multiple Selectors Pattern
```python
for selector in ["h1.entry-title", "h1.post-title", "h1"]:
    tag = soup.select_one(selector)
    if tag:
        article["headline"] = tag.get_text(strip=True)
        break
```
We try multiple CSS selectors in order of specificity. The `break` statement exits the loop as soon as a match is found — we don't need to try the remaining selectors.

#### Open Graph Meta Tags
These are `<meta>` tags that websites add for social media sharing:
- `<meta property="og:title" content="Article Title Here">`
- `<meta property="og:image" content="https://site.com/image.jpg">`
- `<meta property="article:published_time" content="2024-01-15T10:30:00+00:00">`

`soup.find("meta", property="og:title")` — finds `<meta>` tags with a specific `property` attribute. Note: `property` is an attribute, so we pass it as a keyword argument.

#### `try: ... except Exception: pass`
The bare `pass` silently ignores any error. This is appropriate here because:
1. We have a safe default value (`None`) already set
2. Article scraping is best-effort — missing one field shouldn't stop us
3. We log the overall failure rate at the end

In production code you'd typically log these errors to a file for debugging.

#### `content_div.find_all("p")`
Finds all `<p>` (paragraph) tags inside the content area. News articles consist of paragraphs, so joining all `<p>` text gives us the full article body.

`"\n".join([...])` — Joins a list of strings with newline characters between each. This preserves paragraph breaks.

#### `len(content_text.split())`
`.split()` — Without arguments, splits on any whitespace and returns a list of words. `len()` counts the words. This gives us an approximate word count.

#### Newspaper3k Fallback
```python
art = Article(url)
art.download()
art.parse()
content_text = art.text
```
The `newspaper3k` library is specifically designed for news articles. It uses its own scraping algorithms and can handle many site structures. We use it only as a fallback when our custom selectors fail.

**ETL Contribution:** This section IS the core **Extract** stage — collecting the raw data that everything else depends on.
"""))

nb.cells = cells

import nbformat
with open("/home/claude/notebook_part1.ipynb", "w", encoding="utf-8") as f:
    nbformat.write(nb, f)
print("Part 1 written successfully")