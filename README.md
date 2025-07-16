# 🕷️ Web Scraping Tools

A comprehensive tool for collecting and analyzing web data, developed in Python. This project demonstrates advanced web scraping, data processing, and automated analysis techniques.

## 🚀 Features

- **📊 Multiple Scrapers**: Collects data from different sources
- Job openings
- E-commerce products
- News and articles
- **🔄 Retry System**: Automatic retries in case of failure
- **⏱️ Rate Limiting**: Speed control to avoid blocking
- **💾 Multiple Formats**: Exports data in CSV, JSON, Excel, and SQLite
- **📈 Automatic Analysis**: Statistics and insights from collected data
- **🎯 Rotating User Agent**: Prevents bot detection
- **📝 Full Logging**: Detailed process monitoring

## 🛠️ Technologies Used

- **Python 3.7+**
- **requests**: For HTTP requests
- **BeautifulSoup4**: For HTML parsing
- **pandas**: For data manipulation
- **fake-useragent**: For user agent rotation
- **sqlite3**: For database storage
- **logging**: For monitoring and debugging

## 📋 Prerequisites

```bash
Python 3.7 or higher
pip (Python package manager)
```

## 🔧 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-user/web-scraping-tools.git
cd web-scraping-tools
```

2. **Install the dependencies:**
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests beautifulsoup4 pandas fake-useragent
```

## 🚀 How to use

### Basic Execution

```bash
python main.py
```

### Usage Examples

#### 1. Job Scraping
```python
from web_scraper import JobScraper, ScrapingConfig

config = ScrapingConfig(delay=1.0, output_format='csv')
scraper = JobScraper(config)

jobs = scraper.scrape_jobs(['Python', 'Django'], 'São Paulo')
scraper.save_data(jobs, 'python_jobs')
```

#### 2. E-commerce Scraping
```python
from web_scraper import EcommerceScraper, ScrapingConfig

config = ScrapingConfig(delay=2.0, output_format='json')
scraper = EcommerceScraper(config)

products = scraper.scrape_products(['electronics', 'clothes'])
scraper.save_data(products, 'electronic_products')
```

#### 3. Data Analysis
```python
from web_scraper import DataAnalyzer

analyzer = DataAnalyzer(jobs_data)
stats = analyzer.get_basic_stats()
text_analysis = analyzer.analyze_text_data('title')

print(f"Total records: {stats['total_records']}")
print(f"Most common words: {text_analysis['most_common_words']}")
```

## ⚙️ Configuration

### ScrapingConfig Parameters

```python
config = ScrapingConfig(
delay=1.0, # Delay between requests (seconds)
timeout=10, # Request timeout
max_retries=3, # Maximum retries
use_random_agent=True, # Use random user agent
output_format='csv', # Output format (csv, json, excel, sqlite)
output_path='scraped_data' # Output directory
)
```

## 📁 Project Structure

```
web-scraping-tools/
├── main.py # Main file
├── web_scraper.py # Scraper classes
├── requirements.txt # Dependencies
├── README.md # Documentation
├── scraped_data/ # Data collected
│ ├── jobs_data.csv
│ ├── products_data.csv
│ └── news_data.csv
└── logs/ # System Logs
└── scraping.log
```

## 🎯 Advanced Features

### Intelligent Retry System
- Automatic retries in case of failure
- Exponential delay between attempts
- Detailed error logging

### Rate Limiting
- Customizable speed control
- Prevents server overload
- Reduces the chance of blocking

### Automatic Analysis
- Basic data statistics
- Automated text analysis
- Pattern identification

## 📊 Output Formats

### CSV
```python
config.output_format = 'csv'
# Outputs: file.csv
```

### JSON
```python
config.output_format = 'json'
# Generates: file.json
```

### Excel
```python
config.output_format = 'excel'
# Generates: file.xlsx
```

### SQLite
```python
config.output_format = 'sqlite'
# Generates: file.db
```

## 🔍 Examples of Data Collected

### Job Openings
```json
{
"title": "Junior Python Developer",
"company": "TechCorp",
"location": "São Paulo",
"salary": "R$ 4,500",
"requirements": "Python, Django, Git, SQL",
"posted_date": "2024-01-15",
"url": "https://example.com/job/123"
}
```

E-commerce Products
json{
"name": "Smartphone XYZ",
"category": "electronics",
"price": 1299.99,
"rating": 4.5,
"reviews_count": 150,
"availability": "In stock",
"brand": "Brand A"
}
🤝 Contributing

Fork the project
Create a branch for your feature (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

📝 Upcoming Features

Integration with proxy APIs
JavaScript scraping with Selenium
Web dashboard for visualization
Scheduler for automatic execution
Integration with external databases
Notification system
Sentiment analysis in Texts

⚠️ Disclaimer
This project is for educational and demonstration purposes only. Always respect the websites' terms of use and web scraping best practices:

Check the websites' robots.txt file
Implement appropriate delays
Respect rate limiting limits
Don't overload the servers

🐛 Reporting Bugs
If you find a bug, please open an issue with:

Detailed description of the problem
Steps to reproduce
Error messages (if any)
Environment (OS, Python version, etc.)

📄 License
This project is licensed under the MIT license. See the LICENSE file for more details. 👨‍💻 Author
Your Name

GitHub: @Jbreccio
LinkedIn: www.linkedin.com/in/josebreccio-dev-35b8292a4
Email: oibreccio@hotmail.com

🙏 Thanks

Python Community for the documentation
Developers of the libraries used
Project Contributors

⭐ If this project helped you, leave a star! ⭐
