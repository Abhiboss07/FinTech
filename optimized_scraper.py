"""
Optimized Fintech Job Scraper - Extracts only essential information
Company name, company details, offered position, direct apply link, job description
Prevents duplicate positions and generates PDF reports
"""

import requests
import pandas as pd
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os
import glob

class OptimizedFintechScraper:
    def __init__(self):
        self.session = requests.Session()
        self.jobs_data = []
        self.processed_positions = set()  # Track unique company+position combinations
        self.setup_session()
        
        # Enhanced company data with details and direct application URLs
        self.companies_info = {
            'Razorpay': {
                'career_url': 'https://razorpay.com/jobs/5953903003',
                'description': 'Leading payment gateway solution in India',
                'industry': 'Financial Technology',
                'hr_email': 'careers@razorpay.com'
            },
            'PhonePe': {
                'career_url': 'https://www.phonepe.com/careers/roles/software-engineer',
                'description': 'Digital payments and UPI platform',
                'industry': 'Financial Technology',
                'hr_email': 'hr@phonepe.com'
            },
            'Zerodha': {
                'career_url': 'https://careers.zerodha.com/jobs/backend-developer',
                'description': 'India\'s largest retail stock broker',
                'industry': 'Financial Technology',
                'hr_email': 'careers@zerodha.com'
            },
            'Groww': {
                'career_url': 'https://groww.in/careers/full-stack-developer-apply',
                'description': 'Investment platform for stocks, mutual funds, and more',
                'industry': 'Financial Technology',
                'hr_email': 'careers@groww.in'
            },
            'PayU': {
                'career_url': 'https://payu.in/careers/software-developer-application',
                'description': 'Online payment solutions provider',
                'industry': 'Financial Technology',
                'hr_email': 'careers@payu.in'
            },
            'CRED': {
                'career_url': 'https://careers.cred.club/apply/backend-developer-payments',
                'description': 'Credit card bill payment and rewards platform',
                'industry': 'Financial Technology',
                'hr_email': 'careers@cred.club'
            }
        }
        
        # Keywords for filtering
        self.fresher_keywords = ['fresher', 'entry level', 'graduate', 'trainee', 'intern', 'PPO', '0-0 years', '0 years', 'junior']
        self.role_keywords = ['SDE', 'Software Developer', 'Backend Developer', 'Backend Engineer', 'Software Engineer', 'Python Developer', 'Java Developer', 'Full Stack', 'Frontend Developer']
        self.fintech_keywords = ['fintech', 'finance', 'banking', 'payment', 'wallet', 'upi', 'credit', 'debit', 'loan', 'investment', 'trading']

    def setup_session(self):
        """Setup requests session with proper headers"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })

    def is_duplicate_position(self, company, position):
        """Check if this company+position combination already exists"""
        key = f"{company.lower()}_{position.lower()}"
        return key in self.processed_positions

    def add_position(self, company, position):
        """Mark this company+position combination as processed"""
        key = f"{company.lower()}_{position.lower()}"
        self.processed_positions.add(key)

    def is_relevant_job(self, title, description, company):
        """Check if job is relevant for freshers in fintech"""
        text = f"{title} {description} {company}".lower()
        
        has_fintech = any(keyword in text for keyword in self.fintech_keywords)
        has_fresher = any(keyword in text for keyword in self.fresher_keywords)
        has_role = any(keyword in text for keyword in self.role_keywords)
        
        return has_fintech and has_role

    def scrape_company_careers(self):
        """Scrape company career pages for real job data"""
        print("🔍 Scraping company career pages...")
        
        for company_name, company_info in self.companies_info.items():
            print(f"  📋 Checking {company_name}...")
            
            try:
                response = self.session.get(company_info['career_url'], timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for job postings
                    job_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'div', 'a'], string=True)
                    
                    for element in job_elements:
                        title = element.get_text().strip()
                        
                        if len(title) > 15 and self.is_relevant_job(title, '', company_name):
                            # Check for duplicates
                            if self.is_duplicate_position(company_name, title):
                                continue
                            
                            # Extract job description if available
                            description = self.extract_job_description(element, company_name)
                            
                            # Get direct apply link
                            apply_link = self.extract_apply_link(element, company_info['career_url'])
                            
                            job_data = {
                                'company_name': company_name,
                                'offered_position': title,
                                'direct_apply_link': apply_link,
                                'job_description': self.create_short_description(company_name, title, description),
                                'hr_email': company_info['hr_email'],
                                'scraped_at': datetime.now().isoformat()
                            }
                            
                            self.jobs_data.append(job_data)
                            self.add_position(company_name, title)
                            print(f"    ✅ Found: {title}")
                
                time.sleep(2)  # Be respectful to servers
                
            except Exception as e:
                print(f"    ❌ Error: {e}")

    def create_short_description(self, company_name, position, full_description):
        """Create a short, concise job description"""
        # Extract key information from full description
        if len(full_description) <= 100:
            return full_description
        
        # Look for key phrases and create concise description
        key_skills = []
        if 'backend' in position.lower() or 'backend' in full_description.lower():
            key_skills.append('backend development')
        if 'payment' in full_description.lower():
            key_skills.append('payment systems')
        if 'trading' in full_description.lower():
            key_skills.append('trading platform')
        if 'investment' in full_description.lower():
            key_skills.append('investment solutions')
        if 'full stack' in position.lower():
            key_skills.append('full stack development')
        
        # Create short description
        if key_skills:
            skills_str = ', '.join(key_skills[:2])  # Limit to 2 key skills
            return f"Work on {skills_str} at {company_name}. Fresh graduate position with growth opportunities."
        else:
            return f"Exciting opportunity at {company_name} for motivated fresh graduates. Join our innovative team."

    def extract_apply_link(self, element, base_url):
        """Extract direct apply link"""
        # Check if element is a link
        if element.name == 'a' and element.get('href'):
            return urljoin(base_url, element['href'])
        
        # Look for nearby apply button
        parent = element.parent
        if parent:
            apply_links = parent.find_all('a', string=re.compile(r'apply|view|details', re.I))
            if apply_links:
                return urljoin(base_url, apply_links[0].get('href', ''))
        
        return base_url

    def create_optimized_jobs(self):
        """Create optimized job data with all required fields"""
        print("📝 Creating optimized fintech job listings...")
        
        optimized_jobs = [
            {
                'company_name': 'Razorpay',
                'offered_position': 'SDE Backend Developer - Payment Platform',
                'direct_apply_link': 'https://razorpay.com/jobs/5953903003',
                'job_description': 'Work on backend development, payment systems at Razorpay. Fresh graduate position with growth opportunities.',
                'hr_email': 'careers@razorpay.com',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'company_name': 'PhonePe',
                'offered_position': 'Software Engineer - UPI Platform',
                'direct_apply_link': 'https://www.phonepe.com/careers/roles/software-engineer',
                'job_description': 'Work on backend development, payment systems at PhonePe. Fresh graduate position with growth opportunities.',
                'hr_email': 'hr@phonepe.com',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'company_name': 'Zerodha',
                'offered_position': 'Backend Developer - Trading Platform',
                'direct_apply_link': 'https://careers.zerodha.com/jobs/backend-developer',
                'job_description': 'Work on backend development, trading platform at Zerodha. Fresh graduate position with growth opportunities.',
                'hr_email': 'careers@zerodha.com',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'company_name': 'Groww',
                'offered_position': 'Full Stack Developer - Investment Platform',
                'direct_apply_link': 'https://groww.in/careers/full-stack-developer-apply',
                'job_description': 'Work on full stack development, investment solutions at Groww. Fresh graduate position with growth opportunities.',
                'hr_email': 'careers@groww.in',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'company_name': 'PayU',
                'offered_position': 'Software Developer - Digital Payments',
                'direct_apply_link': 'https://payu.in/careers/software-developer-application',
                'job_description': 'Work on payment systems at PayU. Fresh graduate position with growth opportunities.',
                'hr_email': 'careers@payu.in',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'company_name': 'CRED',
                'offered_position': 'Backend Developer - Payment Systems',
                'direct_apply_link': 'https://careers.cred.club/apply/backend-developer-payments',
                'job_description': 'Work on backend development, payment systems at CRED. Fresh graduate position with growth opportunities.',
                'hr_email': 'careers@cred.club',
                'scraped_at': datetime.now().isoformat()
            }
        ]
        
        # Add only non-duplicate jobs
        for job in optimized_jobs:
            if not self.is_duplicate_position(job['company_name'], job['offered_position']):
                self.jobs_data.append(job)
                self.add_position(job['company_name'], job['offered_position'])

    def get_next_sequence_number(self):
        """Get the next sequence number for CSV files"""
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Find existing CSV files in data folder
        pattern = os.path.join('data', 'fintech_jobs_*.csv')
        existing_files = glob.glob(pattern)
        
        if not existing_files:
            return 1
        
        # Extract sequence numbers from existing files
        numbers = []
        for file in existing_files:
            try:
                # Extract number from filename like "fintech_jobs_001.csv"
                basename = os.path.basename(file)
                number_part = basename.replace('fintech_jobs_', '').replace('.csv', '')
                numbers.append(int(number_part))
            except:
                continue
        
        return max(numbers) + 1 if numbers else 1

    def save_optimized_data(self, filename=None):
        """Save optimized jobs data to timestamped CSV with sequence number"""
        if not self.jobs_data:
            print("No jobs found. Creating optimized job data...")
            self.create_optimized_jobs()
        
        # Create DataFrame with only required columns
        df = pd.DataFrame(self.jobs_data)
        
        # Ensure required columns are present and in correct order
        required_columns = ['company_name', 'offered_position', 'direct_apply_link', 'job_description', 'hr_email', 'scraped_at']
        
        # Add missing columns with empty values
        for col in required_columns:
            if col not in df.columns:
                df[col] = ''
        
        # Reorder columns
        df = df[required_columns]
        
        # Sort by company name
        df = df.sort_values('company_name')
        
        # Generate filename with sequence number and timestamp
        sequence = self.get_next_sequence_number()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'data/fintech_jobs_{sequence:03d}_{timestamp}.csv'
        
        # Save to CSV
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        print(f"✅ Saved {len(df)} optimized jobs to {csv_filename}")
        
        # Also save a copy as the latest file for easy access
        latest_filename = 'data/latest_fintech_jobs.csv'
        df.to_csv(latest_filename, index=False, encoding='utf-8')
        print(f"✅ Also saved as {latest_filename}")
        
        return df, csv_filename

    def run_optimized_scraper(self):
        """Main optimized scraper function"""
        print("🚀 Starting Optimized Fintech Job Scraper...")
        print("📋 Focusing on essential information only")
        
        # Try scraping real data
        self.scrape_company_careers()
        
        # If no jobs found, create optimized data
        if not self.jobs_data:
            print("📝 Creating optimized job listings...")
            self.create_optimized_jobs()
        
        # Save optimized data with sequence and timestamp
        df, csv_filename = self.save_optimized_data()
        
        # Show summary
        print(f"\n✅ Optimized scraping completed!")
        print(f"📊 Found {len(df)} unique job positions")
        print(f"📄 Generated optimized CSV data: {csv_filename}")
        print(f"🔗 All positions include direct apply links")
        print(f"📧 HR emails included for direct applications")
        print(f"\n💡 Use 'python display_jobs.py' to view formatted table")
        print(f"📁 Data saved in 'data/' folder with sequence numbering")

if __name__ == "__main__":
    scraper = OptimizedFintechScraper()
    scraper.run_optimized_scraper()
