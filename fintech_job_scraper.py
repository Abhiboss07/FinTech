"""
Fintech Job Scraper for Freshers with PPO Letters
Scrapes SDE/Backend roles from various job boards and company career pages
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

class FintechJobScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.jobs_data = []
        self.visited_urls = set()
        self.driver = None
        self.setup_selenium()
        
        # Target job boards and fintech companies
        self.job_boards = [
            "https://www.naukri.com/",
            "https://www.linkedin.com/jobs/",
            "https://www.indeed.co.in/",
            "https://www.angel.co/",
            "https://www.hirist.com/",
            "https://www.cutshort.io/"
        ]
        
        # Major fintech companies in India
        self.fintech_companies = [
            "paytm.com",
            "phonepe.com", 
            "razorpay.com",
            "cred.com",
            "upstox.com",
            "zerodha.com",
            "groww.in",
            "policybazaar.com",
            "payu.in",
            "billdesk.com",
            "cashfree.com",
            "instamojo.com",
            "mobiKwik.com",
            "freecharge.in",
            "googlepay.com",
            "amazonpay.in",
            "slice.it",
            "niyo.solutions",
            "fi.money",
            "jupiter.money",
            "epifi.in",
            "open.money",
            "niyoglobal.com",
            "fampay.in",
            "walnut365.com",
            "simpl.in",
            "lazyPay.in",
            "earlysalary.com",
            "moneytap.in",
            "kissht.com",
            "cashe.in",
            "loanbaba.com",
            "loantap.in",
            "faircent.com",
            "lendbox.in",
            "monexo.in",
            "i2ifunding.com",
            "rupeecircle.com",
            "finway.in",
            "loanframe.com",
            "kredx.com",
            "m1xchange.com",
            "credable.in",
            "nirmaan.org",
            "tavant.com",
            "manappuram.com",
            "muthootfinance.com",
            "bajajfinserv.in",
            "tatacapital.com",
            "hdfc.com",
            "icicibank.com",
            "axisbank.com",
            "kotak.com",
            "sbi.co.in"
        ]
        
        # Keywords for freshers and PPO
        self.search_keywords = [
            "fresher", "entry level", "graduate", "trainee", "intern", "PPO",
            "pre placement offer", "campus placement", "recent graduate",
            "0-0 years", "0 years", "no experience", "junior developer"
        ]
        
        # Role keywords
        self.role_keywords = [
            "SDE", "Software Developer", "Backend Developer", "Backend Engineer",
            "Software Engineer", "Full Stack Developer", "Python Developer",
            "Java Developer", "Node.js Developer", "API Developer",
            "Database Developer", "DevOps Engineer", "Cloud Engineer"
        ]

    def setup_selenium(self):
        """Setup Selenium WebDriver with anti-detection measures"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            print(f"Error setting up Selenium: {e}")
            self.driver = None

    def get_random_headers(self):
        """Generate random headers to avoid detection"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

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
        fintech_keywords = [
            'fintech', 'finance', 'banking', 'payment', 'wallet', 'upi', 'neft',
            'rtgs', 'imps', 'digital payment', 'online payment', 'mobile payment',
            'credit', 'debit', 'loan', 'insurance', 'investment', 'trading',
            'stock', 'mutual fund', 'cryptocurrency', 'bitcoin', 'blockchain',
            'wealth management', 'financial services', 'bank', 'nbfc'
        ]
        return any(keyword in text for keyword in fintech_keywords)

    def is_fresher_job(self, title, description):
        """Check if job is suitable for freshers"""
        text = f"{title} {description}".lower()
        return any(keyword in text for keyword in self.search_keywords)

    def is_sde_backend_role(self, title, description):
        """Check if job is SDE/Backend role"""
        text = f"{title} {description}".lower()
        return any(keyword in text for keyword in self.role_keywords)

    def scrape_naukri(self):
        """Scrape jobs from Naukri.com"""
        print("Scraping Naukri.com...")
        base_url = "https://www.naukri.com"
        
        search_queries = [
            "fresher SDE backend fintech",
            "entry level software developer finance",
            "graduate trainee software engineer payment",
            "PPO software developer banking"
        ]
        
        for query in search_queries:
            try:
                search_url = f"{base_url}/jobapi/v2/search?locationType=city&location=Delhi%2C%20Bengaluru%2C%20Mumbai%2C%20Hyderabad%2C%20Pune%2C%20Chennai&keyword={query.replace(' ', '%20')}&experience=0&industry=106"
                
                headers = self.get_random_headers()
                response = self.session.get(search_url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get('jobDetails', [])
                    
                    for job in jobs:
                        if self.process_job(job, 'naukri'):
                            self.jobs_data.append(job)
                
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                print(f"Error scraping Naukri: {e}")
                continue

    def scrape_linkedin(self):
        """Scrape jobs from LinkedIn"""
        print("Scraping LinkedIn...")
        
        if not self.driver:
            print("Selenium not available, skipping LinkedIn")
            return
            
        search_queries = [
            "fintech SDE backend fresher",
            "software developer finance entry level",
            "backend engineer payment graduate"
        ]
        
        for query in search_queries:
            try:
                url = f"https://www.linkedin.com/jobs/search?keywords={query.replace(' ', '%20')}&location=India&f_E=2&f_TPR=r86400"
                
                self.driver.get(url)
                time.sleep(random.uniform(3, 6))
                
                # Scroll to load more jobs
                for _ in range(3):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                
                job_cards = self.driver.find_elements(By.CLASS_NAME, "job-card-container")
                
                for card in job_cards:
                    try:
                        job_data = self.extract_linkedin_job(card)
                        if job_data and self.validate_job(job_data):
                            self.jobs_data.append(job_data)
                    except Exception as e:
                        print(f"Error extracting LinkedIn job: {e}")
                        continue
                
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"Error scraping LinkedIn: {e}")
                continue

    def extract_linkedin_job(self, card):
        """Extract job details from LinkedIn job card"""
        try:
            title = card.find_element(By.CLASS_NAME, "job-card-list__title").text
            company = card.find_element(By.CLASS_NAME, "job-card-container__company-name").text
            location = card.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
            
            # Click to get more details
            card.click()
            time.sleep(2)
            
            try:
                description = self.driver.find_element(By.CLASS_NAME, "show-more-less-html__markup").text
            except:
                description = ""
            
            try:
                apply_link = self.driver.find_element(By.CLASS_NAME, "apply-button--link").get_attribute("href")
            except:
                apply_link = ""
            
            return {
                'title': self.clean_text(title),
                'company': self.clean_text(company),
                'location': self.clean_text(location),
                'description': self.clean_text(description),
                'apply_link': apply_link,
                'source': 'linkedin',
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error extracting LinkedIn job details: {e}")
            return None

    def scrape_company_career_pages(self):
        """Scrape individual fintech company career pages"""
        print("Scraping company career pages...")
        
        for company_domain in self.fintech_companies[:20]:  # Limit to first 20 for testing
            try:
                career_urls = [
                    f"https://www.{company_domain}/careers",
                    f"https://www.{company_domain}/jobs",
                    f"https://www.{company_domain}/careers/openings",
                    f"https://jobs.{company_domain}",
                    f"https://careers.{company_domain}"
                ]
                
                for career_url in career_urls:
                    if career_url in self.visited_urls:
                        continue
                        
                    try:
                        headers = self.get_random_headers()
                        response = self.session.get(career_url, headers=headers, timeout=10)
                        
                        if response.status_code == 200:
                            self.visited_urls.add(career_url)
                            jobs = self.parse_company_career_page(response.text, company_domain, career_url)
                            
                            for job in jobs:
                                if self.validate_job(job):
                                    self.jobs_data.append(job)
                                    
                        time.sleep(random.uniform(2, 4))
                        
                    except Exception as e:
                        print(f"Error scraping {career_url}: {e}")
                        continue
                        
            except Exception as e:
                print(f"Error processing {company_domain}: {e}")
                continue

    def parse_company_career_page(self, html, company_domain, base_url):
        """Parse company career page for job listings"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            # Look for job listings in various common selectors
            job_selectors = [
                '.job-listing',
                '.career-opening',
                '.job-card',
                '.position',
                '.opening',
                '[data-job]',
                '.job-item'
            ]
            
            job_elements = []
            for selector in job_selectors:
                elements = soup.select(selector)
                if elements:
                    job_elements = elements
                    break
            
            # If no specific job elements found, look for links with job-related text
            if not job_elements:
                links = soup.find_all('a', href=True)
                job_elements = [link for link in links if any(keyword in link.get_text().lower() 
                               for keyword in ['engineer', 'developer', 'sde', 'backend', 'software'])]
            
            for element in job_elements:
                try:
                    job_data = self.extract_job_from_element(element, company_domain, base_url)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    print(f"Error extracting job from element: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error parsing career page: {e}")
            
        return jobs

    def extract_job_from_element(self, element, company_domain, base_url):
        """Extract job details from a page element"""
        try:
            # Extract title
            title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'span'], 
                                    string=lambda text: text and any(keyword in text.lower() 
                                    for keyword in self.role_keywords))
            title = title_elem.get_text().strip() if title_elem else element.get_text().strip()
            
            # Extract link
            link = element.get('href') if element.name == 'a' else element.find('a', href=True)
            if link:
                job_url = urljoin(base_url, link.get('href') if isinstance(link, dict) else link)
            else:
                job_url = base_url
            
            # Get detailed job description if possible
            description = ""
            if job_url != base_url:
                try:
                    headers = self.get_random_headers()
                    response = self.session.get(job_url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        desc_soup = BeautifulSoup(response.text, 'lxml')
                        desc_selectors = [
                            '.job-description',
                            '.description',
                            '.job-details',
                            '.requirements',
                            '.responsibilities'
                        ]
                        for selector in desc_selectors:
                            desc_elem = desc_soup.select_one(selector)
                            if desc_elem:
                                description = desc_elem.get_text()
                                break
                except:
                    pass
            
            # Extract contact information
            page_text = f"{title} {description}"
            emails = self.extract_email_from_text(page_text)
            phones = self.extract_phone_from_text(page_text)
            
            return {
                'title': self.clean_text(title),
                'company': company_domain,
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

    def process_job(self, job_data, source):
        """Process and validate job data"""
        try:
            if isinstance(job_data, dict):
                # Standardize job data format
                processed_job = {
                    'title': job_data.get('title', ''),
                    'company': job_data.get('companyName', job_data.get('company', '')),
                    'location': job_data.get('locationDetails', job_data.get('location', '')),
                    'description': job_data.get('jobDescription', job_data.get('description', '')),
                    'apply_link': job_data.get('jdURL', job_data.get('apply_link', '')),
                    'salary': job_data.get('salary', ''),
                    'experience': job_data.get('experience', ''),
                    'skills': job_data.get('tags', job_data.get('skills', '')),
                    'posted_date': job_data.get('createdDate', job_data.get('posted_date', '')),
                    'source': source,
                    'scraped_at': datetime.now().isoformat()
                }
                
                # Extract contact info
                text = f"{processed_job['title']} {processed_job['description']}"
                processed_job['hr_emails'] = ', '.join(self.extract_email_from_text(text))
                processed_job['hr_phones'] = ', '.join(self.extract_phone_from_text(text))
                
                return self.validate_job(processed_job)
                
        except Exception as e:
            print(f"Error processing job: {e}")
            return False
            
        return False

    def validate_job(self, job_data):
        """Validate if job meets our criteria"""
        try:
            title = job_data.get('title', '').lower()
            description = job_data.get('description', '').lower()
            company = job_data.get('company', '').lower()
            
            # Check if it's a fintech job
            if not self.is_fintech_job(title, description, company):
                return False
            
            # Check if it's for freshers
            if not self.is_fresher_job(title, description):
                return False
            
            # Check if it's SDE/Backend role
            if not self.is_sde_backend_role(title, description):
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating job: {e}")
            return False

    def save_to_csv(self, filename="fintech_jobs.csv"):
        """Save jobs data to CSV file"""
        if not self.jobs_data:
            print("No jobs data to save")
            return
        
        # Ensure all jobs have the same keys
        all_keys = set()
        for job in self.jobs_data:
            all_keys.update(job.keys())
        
        # Create DataFrame with all possible columns
        df_data = []
        for job in self.jobs_data:
            row = {key: job.get(key, '') for key in all_keys}
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        
        # Reorder columns for better readability
        column_order = [
            'title', 'company', 'location', 'description', 'apply_link',
            'salary', 'experience', 'skills', 'hr_emails', 'hr_phones',
            'posted_date', 'source', 'scraped_at'
        ]
        
        # Only include columns that exist
        final_columns = [col for col in column_order if col in df.columns]
        remaining_columns = [col for col in df.columns if col not in final_columns]
        final_columns.extend(remaining_columns)
        
        df = df[final_columns]
        
        # Save to CSV
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Saved {len(df)} jobs to {filename}")
        
        # Also save as Excel for better formatting
        excel_filename = filename.replace('.csv', '.xlsx')
        df.to_excel(excel_filename, index=False, engine='openpyxl')
        print(f"Saved {len(df)} jobs to {excel_filename}")

    def verify_data_quality(self):
        """Verify the quality of scraped data"""
        print("\n=== Data Quality Report ===")
        
        if not self.jobs_data:
            print("No jobs data to verify")
            return
        
        total_jobs = len(self.jobs_data)
        print(f"Total jobs scraped: {total_jobs}")
        
        # Check for required fields
        missing_titles = sum(1 for job in self.jobs_data if not job.get('title'))
        missing_companies = sum(1 for job in self.jobs_data if not job.get('company'))
        missing_descriptions = sum(1 for job in self.jobs_data if not job.get('description'))
        
        print(f"Jobs missing title: {missing_titles}")
        print(f"Jobs missing company: {missing_companies}")
        print(f"Jobs missing description: {missing_descriptions}")
        
        # Check for contact information
        jobs_with_email = sum(1 for job in self.jobs_data if job.get('hr_emails'))
        jobs_with_phone = sum(1 for job in self.jobs_data if job.get('hr_phones'))
        
        print(f"Jobs with HR email: {jobs_with_email}")
        print(f"Jobs with HR phone: {jobs_with_phone}")
        
        # Check for duplicate jobs
        titles = [job.get('title', '') for job in self.jobs_data]
        companies = [job.get('company', '') for job in self.jobs_data]
        unique_combinations = set(zip(titles, companies))
        
        print(f"Unique job-title/company combinations: {len(unique_combinations)}")
        print(f"Potential duplicates: {total_jobs - len(unique_combinations)}")
        
        # Check source distribution
        sources = {}
        for job in self.jobs_data:
            source = job.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print("\nJobs by source:")
        for source, count in sources.items():
            print(f"  {source}: {count}")

    def run_scraper(self):
        """Run the complete scraping process"""
        print("Starting Fintech Job Scraper...")
        print(f"Targeting {len(self.fintech_companies)} fintech companies")
        print(f"Searching for: {', '.join(self.role_keywords[:3])}...")
        
        try:
            # Scrape job boards
            self.scrape_naukri()
            self.scrape_linkedin()
            
            # Scrape company career pages
            self.scrape_company_career_pages()
            
            # Verify data quality
            self.verify_data_quality()
            
            # Save results
            self.save_to_csv()
            
        except Exception as e:
            print(f"Error during scraping: {e}")
        
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    scraper = FintechJobScraper()
    scraper.run_scraper()
