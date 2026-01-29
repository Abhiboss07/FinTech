# 🔍 Verified Fintech Job Scraper

A comprehensive Python scraper that extracts **verified HR emails** and **direct apply links** for SDE/Backend roles from top fintech companies, specifically targeting fresher-friendly positions with PPO opportunities.

## ✨ Key Features

- 🔐 **Verified HR Emails Only** - Authentic contacts (careers@, hr@, talent@)
- 🔗 **Direct Apply Links** - Official application portals (Lever, Greenhouse, etc.)
- 🎯 **Smart Filtering** - Fintech + Fresher + SDE/Backend roles
- 📊 **Data Verification** - Comprehensive validation system
- 📧 **Email Validation** - Pattern matching for official HR contacts
- 🚀 **Multiple Export Formats** - CSV, Excel, JSON

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Verified Scraper
```bash
python run_verified_scraper.py
```

### 3. View Results
- `verified_fintech_jobs.csv` - Main dataset
- `verified_fintech_jobs.xlsx` - Excel version
- `verified_fintech_jobs.json` - JSON format

## 📊 What Gets Scraped

### 🔐 Verified HR Emails
- **Official Patterns**: `careers@`, `hr@`, `talent@`, `jobs@`, `recruitment@`
- **Company-Specific**: Custom patterns for each fintech
- **Authenticity Check**: Only emails provided by HR/company

### 🔗 Direct Apply Links
- **Official Portals**: Lever, Greenhouse, Workable, BambooHR
- **Application Forms**: Direct company career pages
- **Apply Buttons**: Extracts "Apply Now" links

### 🎯 Target Companies
- **Payment**: Paytm, PhonePe, Razorpay, PayU, Cashfree
- **Trading**: Upstox, Zerodha, Groww
- **Insurance**: PolicyBazaar
- **Banking**: Major fintech companies

## 📋 Data Fields

| Field | Description |
|-------|-------------|
| `title` | Job title and position |
| `company` | Company name |
| `hr_emails` | Verified HR emails only |
| `direct_apply_link` | Official application portals |
| `email_verified` | Boolean verification status |
| `apply_method` | email/portal/both |
| `location` | Job location |
| `description` | Full job description |

## 🔍 Verification Process

### 📧 Email Verification
```python
# Only accepts verified HR patterns
hr_patterns = [
    r'careers@company\.com',
    r'hr@company\.com',
    r'talent@company\.com'
]
```

### 🔗 Link Verification
```python
# Recognizes official platforms
apply_domains = [
    'lever.co', 'greenhouse.io', 
    'workable.com', 'bamboohr.com'
]
```

## 📈 Sample Output

```csv
title,company,hr_emails,direct_apply_link,email_verified,apply_method
SDE Backend Developer,Paytm,careers@paytm.com,https://jobs.paytm.com/apply,True,email
Backend Engineer,Razorpay,,https://jobs.lever.co/razorpay/12345,False,portal
```

## 🛠️ Technical Stack

- **Python 3.11+**
- **Requests** - HTTP library
- **BeautifulSoup** - HTML parsing
- **Selenium** - Dynamic content
- **Pandas** - Data processing
- **Fake UserAgent** - Anti-detection

## 📊 Quality Metrics

```
=== VERIFIED DATA QUALITY REPORT ===
Total jobs: 3
Jobs with verified HR emails: 2 (66.7%)
Jobs with direct apply links: 3 (100.0%)
Apply methods:
  email: 1
  portal: 1
  both: 1
```

## 🎯 Why Verified Data?

- ✅ **No Fake Emails** - Only authentic HR contacts
- ✅ **Higher Response Rates** - Direct contact with actual teams
- ✅ **Official Channels** - Legitimate application portals
- ✅ **Professional Standards** - Maintains credibility
- ✅ **Time Saving** - No wasted applications

## 📁 Project Structure

```
FinTech/
├── verified_scraper.py          # Main scraper
├── run_verified_scraper.py      # Execution script
├── requirements.txt              # Dependencies
├── verified_fintech_jobs.csv    # Main dataset
├── verified_fintech_jobs.xlsx    # Excel version
├── verified_fintech_jobs.json    # JSON format
└── README.md                    # This file
```

## 🚀 Usage Examples

### Basic Usage
```python
from verified_scraper import VerifiedFintechJobScraper

scraper = VerifiedFintechJobScraper()
scraper.run_verified_scraper()
```

### Custom Configuration
```python
# Update company-specific patterns
scraper.fintech_companies[0]['official_hr_patterns'] = [
    r'careers@newcompany\.com',
    r'hr@newcompany\.com'
]
```

## 📞 Support
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
