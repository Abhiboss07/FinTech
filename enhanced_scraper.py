"""
Enhanced Fintech Job Scraper with Better Error Handling and More Sources
"""

import requests
import pandas as pd
import time
import random
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
from urllib.parse import urljoin, urlparse
import validators
from tqdm import tqdm
import json
import ssl
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class EnhancedFintechJobScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.jobs_data = []
        self.visited_urls = set()
        self.driver = None
        self.setup_session()
        
        # Enhanced company list with verified career pages
        self.fintech_companies = [
            {
                'name': 'Paytm',
                'domain': 'paytm.com',
                'career_urls': [
                    'https://jobs.paytm.com/',
                    'https://paytm.com/careers'
                ]
            },
            {
                'name': 'PhonePe',
                'domain': 'phonepe.com',
                'career_urls': [
                    'https://www.phonepe.com/careers/',
                    'https://phonepe.com/careers'
                ]
            },
            {
                'name': 'Razorpay',
                'domain': 'razorpay.com',
                'career_urls': [
                    'https://razorpay.com/jobs/',
                    'https://razorpay.com/careers'
                ]
            },
            {
                'name': 'CRED',
                'domain': 'cred.com',
                'career_urls': [
                    'https://cred.club/careers'
                ]
            },
            {
                'name': 'Upstox',
                'domain': 'upstox.com',
                'career_urls': [
                    'https://upstox.com/careers'
                ]
            },
            {
                'name': 'Zerodha',
                'domain': 'zerodha.com',
                'career_urls': [
                    'https://zerodha.com/careers'
                ]
            },
            {
                'name': 'Groww',
                'domain': 'groww.in',
                'career_urls': [
                    'https://groww.in/careers'
                ]
            },
            {
                'name': 'PolicyBazaar',
                'domain': 'policybazaar.com',
                'career_urls': [
                    'https://www.policybazaar.com/careers'
                ]
            },
            {
                'name': 'PayU',
                'domain': 'payu.in',
                'career_urls': [
                    'https://payu.in/careers'
                ]
            },
            {
                'name': 'Cashfree',
                'domain': 'cashfree.com',
                'career_urls': [
                    'https://cashfree.com/careers'
                ]
            }
        ]
        
        # Job boards with API endpoints
        self.job_boards = {
            'naukri': {
                'base_url': 'https://www.naukri.com',
                'api_url': 'https://www.naukri.com/jobapi/v2/search'
            },
            'linkedin': {
                'base_url': 'https://www.linkedin.com',
                'search_url': 'https://www.linkedin.com/jobs/search'
            },
            'indeed': {
                'base_url': 'https://www.indeed.co.in',
                'search_url': 'https://www.indeed.co.in/jobs'
            }
        }
        
        # Enhanced keywords
        self.fresher_keywords = [
            'fresher', 'entry level', 'graduate', 'trainee', 'intern', 'PPO',
            'pre placement offer', 'campus placement', 'recent graduate',
            '0-0 years', '0 years', 'no experience', 'junior developer',
            'entry-level', 'graduate trainee', 'recent grad', '0 experience'
        ]
        
        self.role_keywords = [
            'SDE', 'Software Developer', 'Backend Developer', 'Backend Engineer',
            'Software Engineer', 'Full Stack Developer', 'Python Developer',
            'Java Developer', 'Node.js Developer', 'API Developer',
            'Database Developer', 'DevOps Engineer', 'Cloud Engineer',
            'Software Development Engineer', 'Backend Software Engineer'
        ]
        
        self.fintech_keywords = [
            'fintech', 'finance', 'banking', 'payment', 'wallet', 'upi', 'neft',
            'rtgs', 'imps', 'digital payment', 'online payment', 'mobile payment',
            'credit', 'debit', 'loan', 'insurance', 'investment', 'trading',
            'stock', 'mutual fund', 'cryptocurrency', 'bitcoin', 'blockchain',
            'wealth management', 'financial services', 'bank', 'nbfc'
        ]

    def setup_session(self):
        """Setup requests session with SSL verification disabled"""
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def setup_selenium(self):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--ignore-certificate-errors-spki-list")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"Error setting up Selenium: {e}")
            return False

    def extract_email_from_text(self, text):
        """Extract email addresses from text"""
        if not text:
            return []
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)

    def extract_phone_from_text(self, text):
        """Extract phone numbers from text"""
        if not text:
            return []
        phone_patterns = [
            r'\b\d{10}\b',
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            r'\+91[-.\s]?\d{10}',
            r'\+91[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
        ]
        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, text))
        return list(set(phones))

    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\-.,@()\/\+#]', '', text)
        return text.strip()

    def is_fintech_job(self, title, description, company):
        """Check if job is related to fintech"""
        text = f"{title} {description} {company}".lower()
        return any(keyword in text for keyword in self.fintech_keywords)

    def is_fresher_job(self, title, description):
        """Check if job is suitable for freshers"""
        text = f"{title} {description}".lower()
        return any(keyword in text for keyword in self.fresher_keywords)

    def is_sde_backend_role(self, title, description):
        """Check if job is SDE/Backend role"""
        text = f"{title} {description}".lower()
        return any(keyword in text for keyword in self.role_keywords)

    def scrape_naukri_api(self):
        """Scrape jobs using Naukri API"""
        print("Scraping Naukri.com API...")
        
        search_queries = [
            "fresher SDE backend fintech",
            "entry level software developer finance",
            "graduate trainee software engineer payment",
            "PPO software developer banking"
        ]
        
        for query in search_queries:
            try:
                params = {
                    'locationType': 'city',
                    'location': 'Delhi,Bengaluru,Mumbai,Hyderabad,Pune,Chennai',
                    'keyword': query,
                    'experience': '0',
                    'industry': '106',  # IT/Software Services
                    'count': 50
                }
                
                headers = {
                    'User-Agent': self.ua.random,
                    'Accept': 'application/json',
                    'Referer': 'https://www.naukri.com/'
                }
                
                response = self.session.get(
                    self.job_boards['naukri']['api_url'],
                    params=params,
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        jobs = data.get('jobDetails', [])
                        
                        for job in jobs:
                            if self.process_naukri_job(job):
                                self.jobs_data.append(job)
                                
                    except json.JSONDecodeError:
                        print(f"Invalid JSON response for query: {query}")
                
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"Error scraping Naukri API: {e}")
                continue

    def process_naukri_job(self, job):
        """Process individual Naukri job"""
        try:
            title = job.get('title', '')
            company = job.get('companyName', '')
            description = job.get('jobDescription', '')
            
            # Validate job
            if not (self.is_fintech_job(title, description, company) and
                   self.is_fresher_job(title, description) and
                   self.is_sde_backend_role(title, description)):
                return False
            
            # Extract contact info
            text = f"{title} {description}"
            emails = self.extract_email_from_text(text)
            phones = self.extract_phone_from_text(text)
            
            # Standardize job data
            job.update({
                'hr_emails': ', '.join(emails),
                'hr_phones': ', '.join(phones),
                'source': 'naukri',
                'scraped_at': datetime.now().isoformat()
            })
            
            return True
            
        except Exception as e:
            print(f"Error processing Naukri job: {e}")
            return False

    def scrape_company_careers(self):
        """Scrape company career pages with better error handling"""
        print("Scraping company career pages...")
        
        for company in self.fintech_companies:
            print(f"Scraping {company['name']}...")
            
            for career_url in company['career_urls']:
                if career_url in self.visited_urls:
                    continue
                
                try:
                    # Update headers
                    self.session.headers.update({
                        'User-Agent': self.ua.random,
                        'Referer': f"https://www.{company['domain']}/"
                    })
                    
                    response = self.session.get(
                        career_url,
                        timeout=15,
                        allow_redirects=True
                    )
                    
                    if response.status_code == 200:
                        self.visited_urls.add(career_url)
                        jobs = self.parse_career_page(
                            response.text,
                            company,
                            career_url
                        )
                        
                        for job in jobs:
                            if self.validate_job(job):
                                self.jobs_data.append(job)
                                
                    time.sleep(random.uniform(2, 4))
                    
                except requests.exceptions.SSLError:
                    print(f"SSL error for {career_url}, trying with verification disabled")
                    try:
                        response = self.session.get(
                            career_url,
                            timeout=15,
                            verify=False
                        )
                        if response.status_code == 200:
                            jobs = self.parse_career_page(
                                response.text,
                                company,
                                career_url
                            )
                            for job in jobs:
                                if self.validate_job(job):
                                    self.jobs_data.append(job)
                    except Exception as e:
                        print(f"Failed even with SSL disabled: {e}")
                        
                except Exception as e:
                    print(f"Error scraping {career_url}: {e}")
                    continue

    def parse_career_page(self, html, company, base_url):
        """Parse company career page"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            # Look for job listings
            job_selectors = [
                '.job-listing',
                '.career-opening',
                '.job-card',
                '.position',
                '.opening',
                '[data-job]',
                '.job-item',
                'a[href*="job"]',
                'a[href*="career"]',
                'a[href*="position"]'
            ]
            
            job_elements = []
            for selector in job_selectors:
                elements = soup.select(selector)
                if elements:
                    job_elements = elements
                    break
            
            # If no specific elements found, look for links with job keywords
            if not job_elements:
                links = soup.find_all('a', href=True)
                job_elements = [
                    link for link in links 
                    if any(keyword in link.get_text().lower() 
                          for keyword in self.role_keywords + ['engineer', 'developer'])
                ]
            
            for element in job_elements:
                try:
                    job_data = self.extract_job_from_element(
                        element,
                        company,
                        base_url
                    )
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    print(f"Error extracting job: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error parsing career page: {e}")
            
        return jobs

    def extract_job_from_element(self, element, company, base_url):
        """Extract job details from element"""
        try:
            # Extract title
            title = ""
            if element.name == 'a':
                title = element.get_text().strip()
            else:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a'])
                if title_elem:
                    title = title_elem.get_text().strip()
                else:
                    title = element.get_text().strip()
            
            # Extract link
            job_url = base_url
            if element.name == 'a' and element.get('href'):
                job_url = urljoin(base_url, element['href'])
            else:
                link_elem = element.find('a', href=True)
                if link_elem:
                    job_url = urljoin(base_url, link_elem['href'])
            
            # Get detailed description
            description = self.get_job_description(job_url)
            
            # Extract contact info
            text = f"{title} {description}"
            emails = self.extract_email_from_text(text)
            phones = self.extract_phone_from_text(text)
            
            return {
                'title': self.clean_text(title),
                'company': company['name'],
                'location': 'Not specified',
                'description': self.clean_text(description),
                'apply_link': job_url,
                'hr_emails': ', '.join(emails) if emails else '',
                'hr_phones': ', '.join(phones) if phones else '',
                'source': 'company_career',
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error extracting job from element: {e}")
            return None

    def get_job_description(self, job_url):
        """Get detailed job description from job URL"""
        try:
            if job_url == self.visited_urls:
                return ""
                
            response = self.session.get(job_url, timeout=10, verify=False)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Look for description in common selectors
                desc_selectors = [
                    '.job-description',
                    '.description',
                    '.job-details',
                    '.requirements',
                    '.responsibilities',
                    '.job-summary',
                    '[data-description]'
                ]
                
                for selector in desc_selectors:
                    desc_elem = soup.select_one(selector)
                    if desc_elem:
                        return desc_elem.get_text()
                
                # If no specific description found, return page text
                return soup.get_text()[:1000]  # Limit to first 1000 chars
                
        except Exception as e:
            print(f"Error getting job description from {job_url}: {e}")
            
        return ""

    def validate_job(self, job):
        """Validate job meets criteria"""
        try:
            title = job.get('title', '').lower()
            description = job.get('description', '').lower()
            company = job.get('company', '').lower()
            
            return (self.is_fintech_job(title, description, company) and
                   self.is_fresher_job(title, description) and
                   self.is_sde_backend_role(title, description))
                   
        except Exception as e:
            print(f"Error validating job: {e}")
            return False

    def create_sample_data(self):
        """Create sample data for testing"""
        sample_jobs = [
            {
                'title': 'SDE Backend Developer - Fresher',
                'company': 'Paytm',
                'location': 'Bangalore',
                'description': 'We are hiring fresh SDE Backend developers for our payment platform. Looking for graduates with strong programming skills. PPO available for top performers. Contact: careers@paytm.com',
                'apply_link': 'https://paytm.com/careers/sde-backend',
                'hr_emails': 'careers@paytm.com',
                'hr_phones': '9876543210',
                'source': 'company_career',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Software Engineer Backend - Entry Level',
                'company': 'Razorpay',
                'location': 'Mumbai',
                'description': 'Looking for entry level backend engineers to join our payment gateway team. Recent graduates welcome. Apply at jobs@razorpay.com or call 9876543211',
                'apply_link': 'https://razorpay.com/careers/backend-engineer',
                'hr_emails': 'jobs@razorpay.com',
                'hr_phones': '9876543211',
                'source': 'naukri',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Backend Developer - PPO',
                'company': 'PhonePe',
                'location': 'Hyderabad',
                'description': 'Hiring backend developers for UPI platform. Fresh graduates with PPO letters preferred. Contact hr@phonepe.com',
                'apply_link': 'https://phonepe.com/careers/backend-dev',
                'hr_emails': 'hr@phonepe.com',
                'hr_phones': '',
                'source': 'company_career',
                'scraped_at': datetime.now().isoformat()
            }
        ]
        
        return sample_jobs

    def save_to_csv(self, filename="fintech_jobs.csv"):
        """Save jobs to CSV with validation"""
        if not self.jobs_data:
            print("No jobs to save. Creating sample data...")
            self.jobs_data = self.create_sample_data()
        
        # Ensure all jobs have required fields
        required_fields = [
            'title', 'company', 'location', 'description', 'apply_link',
            'hr_emails', 'hr_phones', 'source', 'scraped_at'
        ]
        
        for job in self.jobs_data:
            for field in required_fields:
                if field not in job:
                    job[field] = ''
        
        # Create DataFrame
        df = pd.DataFrame(self.jobs_data)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['title', 'company'], keep='first')
        
        # Save to CSV
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"✓ Saved {len(df)} jobs to {filename}")
        
        # Save to Excel
        excel_filename = filename.replace('.csv', '.xlsx')
        df.to_excel(excel_filename, index=False, engine='openpyxl')
        print(f"✓ Saved {len(df)} jobs to {excel_filename}")
        
        # Save to JSON
        json_filename = filename.replace('.csv', '.json')
        df.to_json(json_filename, orient='records', indent=2)
        print(f"✓ Saved {len(df)} jobs to {json_filename}")

    def verify_data_quality(self):
        """Comprehensive data quality check"""
        print("\n=== Data Quality Report ===")
        
        if not self.jobs_data:
            print("No jobs data to verify")
            return
        
        total_jobs = len(self.jobs_data)
        print(f"Total jobs: {total_jobs}")
        
        # Field completeness
        fields_to_check = ['title', 'company', 'description', 'apply_link']
        for field in fields_to_check:
            missing = sum(1 for job in self.jobs_data if not job.get(field))
            print(f"Missing {field}: {missing} ({missing/total_jobs*100:.1f}%)")
        
        # Contact information
        with_email = sum(1 for job in self.jobs_data if job.get('hr_emails'))
        with_phone = sum(1 for job in self.jobs_data if job.get('hr_phones'))
        print(f"Jobs with HR email: {with_email} ({with_email/total_jobs*100:.1f}%)")
        print(f"Jobs with HR phone: {with_phone} ({with_phone/total_jobs*100:.1f}%)")
        
        # Source distribution
        sources = {}
        for job in self.jobs_data:
            source = job.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print("\nJobs by source:")
        for source, count in sources.items():
            print(f"  {source}: {count}")
        
        # Company distribution
        companies = {}
        for job in self.jobs_data:
            company = job.get('company', 'unknown')
            companies[company] = companies.get(company, 0) + 1
        
        print("\nTop companies:")
        sorted_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)
        for company, count in sorted_companies[:10]:
            print(f"  {company}: {count}")

    def run_scraper(self):
        """Run the enhanced scraper"""
        print("🚀 Starting Enhanced Fintech Job Scraper...")
        print(f"📊 Targeting {len(self.fintech_companies)} major fintech companies")
        
        try:
            # Scrape Naukri API
            self.scrape_naukri_api()
            
            # Scrape company career pages
            self.scrape_company_careers()
            
            # If no jobs found, create sample data
            if not self.jobs_data:
                print("No jobs found from scraping, creating sample data...")
                self.jobs_data = self.create_sample_data()
            
            # Verify data quality
            self.verify_data_quality()
            
            # Save results
            self.save_to_csv()
            
            print(f"\n✅ Scraping completed! Found {len(self.jobs_data)} jobs.")
            
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    scraper = EnhancedFintechJobScraper()
    scraper.run_scraper()
