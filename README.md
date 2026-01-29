# Fintech Job Scraper for Freshers with PPO Letters

A comprehensive Python scraper that extracts SDE/Backend job opportunities for freshers from fintech companies, specifically targeting roles with PPO (Pre-Placement Offer) letters.

## Features

- **Multi-Source Scraping**: Scrapes from major job boards (Naukri, LinkedIn, Indeed) and company career pages
- **Smart Filtering**: Automatically filters for fintech companies, fresher-friendly roles, and SDE/Backend positions
- **Contact Extraction**: Extracts HR emails and phone numbers from job descriptions
- **Data Validation**: Comprehensive validation to ensure data quality
- **Anti-Detection**: Built-in measures to avoid being blocked by websites
- **Multiple Export Formats**: Saves data in CSV, Excel, and JSON formats
- **Data Verification**: Built-in quality checks and reporting

## Installation

1. Clone or download the project
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Install Chrome WebDriver (required for Selenium):
   - Download from: https://chromedriver.chromium.org/
   - Add to PATH or place in project directory

## Usage

### Basic Usage

```python
from fintech_job_scraper import FintechJobScraper

# Initialize scraper
scraper = FintechJobScraper()

# Run complete scraping process
scraper.run_scraper()
```

### Advanced Usage

```python
# Custom configuration
scraper = FintechJobScraper()

# Scrape specific sources
scraper.scrape_naukri()
scraper.scrape_linkedin()
scraper.scrape_company_career_pages()

# Verify data quality
scraper.verify_data_quality()

# Save to custom filename
scraper.save_to_csv("my_fintech_jobs.csv")
```

### Testing

Run the test script to verify functionality:

```bash
python test_scraper.py
```

## Output Files

The scraper generates multiple output files:

- `fintech_jobs.csv` - Main CSV file with all job data
- `fintech_jobs.xlsx` - Excel version with better formatting
- `fintech_jobs.json` - JSON format for programmatic access

## Data Fields

Each job entry includes:

- **Title**: Job title and position
- **Company**: Company name
- **Location**: Job location
- **Description**: Full job description
- **Apply Link**: Direct application URL
- **Salary**: Salary information (if available)
- **Experience**: Required experience
- **Skills**: Required skills/technologies
- **HR Emails**: Extracted HR contact emails
- **HR Phones**: Extracted HR contact numbers
- **Posted Date**: When job was posted
- **Source**: Where the job was found
- **Scraped At**: When data was collected

## Target Companies

The scraper targets major fintech companies including:

- **Payment**: Paytm, PhonePe, Razorpay, CRED, PayU, BillDesk, Cashfree
- **Trading**: Upstox, Zerodha, Groww
- **Insurance**: PolicyBazaar
- **Banking**: Traditional banks with tech roles
- **Emerging**: Slice, Niyo, Jupiter, Fi, Open, and many more

## Filtering Logic

The scraper uses intelligent filtering to find relevant jobs:

### Fintech Detection
- Keywords: fintech, finance, banking, payment, wallet, UPI, etc.
- Company domain matching
- Industry classification

### Fresher Detection
- Keywords: fresher, entry level, graduate, trainee, intern, PPO
- Experience requirements (0-0 years, 0 years)
- Recent graduate indicators

### Role Detection
- Keywords: SDE, Software Developer, Backend Developer, etc.
- Technology stack mentions
- Job function classification

## Configuration

Customize scraping behavior in `config.py`:

- User agents and delays
- Retry settings
- Filtering keywords
- Output file names
- Scraping limits

## Anti-Detection Features

- Random user agents
- Request delays between requests
- Headless browser options
- Cookie handling
- Proxy support (can be added)

## Data Quality

The scraper includes comprehensive data validation:

- Required field validation
- Duplicate detection
- Contact information verification
- Source tracking
- Quality reporting

## Error Handling

- Automatic retries for failed requests
- Graceful handling of missing data
- Logging of errors and warnings
- Continues scraping despite individual failures

## Legal and Ethical Considerations

- Respect robots.txt files
- Implement reasonable delays between requests
- Don't overload servers
- Use data responsibly
- Comply with website terms of service

## Troubleshooting

### Common Issues

1. **Chrome WebDriver Issues**
   - Ensure ChromeDriver version matches Chrome browser
   - Add ChromeDriver to system PATH

2. **Getting Blocked**
   - Increase delays in config.py
   - Use proxy servers if needed
   - Rotate user agents more frequently

3. **No Jobs Found**
   - Check internet connection
   - Verify target websites are accessible
   - Review filtering criteria

4. **Missing Contact Info**
   - Some companies don't publish contact details
   - Try additional scraping sources
   - Manual verification may be needed

### Performance Tips

- Limit number of companies for faster testing
- Use SSD for better I/O performance
- Ensure stable internet connection
- Consider running during off-peak hours

## Contributing

Feel free to contribute by:

- Adding new job sources
- Improving data extraction
- Enhancing filtering logic
- Adding new features
- Reporting bugs

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the test script for usage examples
3. Examine the configuration options
4. Check error logs for specific issues

## Disclaimer

This tool is for educational and legitimate job search purposes only. Users are responsible for:

- Complying with website terms of service
- Respecting rate limits and server loads
- Using scraped data ethically
- Verifying information accuracy

Always verify job information directly with employers before applying.

---

**Note**: Web scraping may be against some websites' terms of service. Use responsibly and at your own risk.
