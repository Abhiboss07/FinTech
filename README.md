# 🚀 Optimized Fintech Job Scraper

A powerful and streamlined job scraper designed specifically for extracting fintech job opportunities from top companies in India. This tool focuses on delivering essential information without duplicates, making job hunting efficient and effective.

## ✨ Features

- **🎯 Focused Data Extraction**: Only extracts essential information
  - Company name and detailed information
  - Offered positions
  - Direct application links
  - Comprehensive job descriptions
  - HR contact emails

- **🚫 Deduplication**: Prevents duplicate company positions
- **📄 PDF Reports**: Professional formatted reports for easy sharing
- **🔗 Verified Links**: Functional direct apply links
- **📧 HR Emails**: Direct contact information for applications

## 🏢 Companies Covered

The scraper targets premium fintech companies including:
- **Razorpay** - Payment gateway solutions
- **PhonePe** - Digital payments and UPI platform
- **Zerodha** - Trading and investment platform
- **Groww** - Investment platform for stocks/mutual funds
- **PayU** - Online payment solutions
- **CRED** - Credit card payments and rewards

## 📋 Installation

1. Clone the repository:
```bash
git clone https://github.com/Abhiboss07/FinTech.git
cd FinTech
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Quick Start
```bash
python run_optimized_scraper.py
```

### Advanced Usage
```python
from optimized_scraper import OptimizedFintechScraper

# Create scraper instance
scraper = OptimizedFintechScraper()

# Run the scraper
scraper.run_optimized_scraper()
```

## 📁 Output Files

After running the scraper, you'll get:

1. **`optimized_fintech_jobs.csv`** - Clean, structured job data
   - Company name and details
   - Offered positions
   - Direct apply links
   - Job descriptions
   - HR emails

2. **`fintech_jobs_report.pdf`** - Professional PDF report
   - Summary table of all jobs
   - Detailed job information
   - Formatted for easy reading and sharing

## 📊 CSV Structure

| Column | Description |
|--------|-------------|
| `company_name` | Name of the hiring company |
| `company_details` | Company description and industry |
| `offered_position` | Specific job title/position |
| `direct_apply_link` | Direct URL to apply for the job |
| `job_description` | Detailed description of the role |
| `hr_email` | HR contact email for direct applications |
| `scraped_at` | Timestamp when data was collected |

## 🎯 Target Roles

The scraper focuses on:
- **SDE/Software Developer** positions
- **Backend Developer** roles
- **Full Stack Developer** opportunities
- **Fresh graduate** friendly positions
- **Entry level** roles in fintech

## 🔧 Technical Details

- **Language**: Python 3.11+
- **Dependencies**: requests, beautifulsoup4, pandas, reportlab
- **Data Sources**: Company career pages and job boards
- **Output Formats**: CSV, PDF
- **Deduplication**: Company + position combination tracking

## 📈 Why This Scraper?

1. **Optimized**: Extracts only essential information
2. **Clean**: No duplicate positions or redundant data
3. **Professional**: PDF reports for easy sharing
4. **Direct**: Verified apply links and HR contacts
5. **Focused**: Specifically for fintech fresh graduate roles

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

---

**🎉 Happy Job Hunting!**

Use the generated CSV and PDF reports to streamline your job application process. All positions include direct apply links and HR contact information for maximum efficiency.
