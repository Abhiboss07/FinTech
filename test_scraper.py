"""
Test script for Fintech Job Scraper
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fintech_job_scraper import FintechJobScraper
import pandas as pd
import json

def test_scraper():
    """Test the scraper with limited scope"""
    print("=== Testing Fintech Job Scraper ===")
    
    # Initialize scraper
    scraper = FintechJobScraper()
    
    # Limit to a few companies for testing
    scraper.fintech_companies = scraper.fintech_companies[:5]
    
    print(f"Testing with {len(scraper.fintech_companies)} companies")
    
    try:
        # Test company career pages scraping
        print("\n--- Testing Company Career Pages ---")
        scraper.scrape_company_career_pages()
        
        # Test data validation
        print("\n--- Testing Data Validation ---")
        scraper.verify_data_quality()
        
        # Test CSV export
        print("\n--- Testing CSV Export ---")
        if scraper.jobs_data:
            scraper.save_to_csv("test_fintech_jobs.csv")
            
            # Verify CSV was created and has data
            if os.path.exists("test_fintech_jobs.csv"):
                df = pd.read_csv("test_fintech_jobs.csv")
                print(f"✓ CSV created with {len(df)} rows and {len(df.columns)} columns")
                print(f"✓ Columns: {list(df.columns)}")
                
                # Show sample data
                print("\n--- Sample Job Data ---")
                for i, job in enumerate(scraper.jobs_data[:3]):
                    print(f"\nJob {i+1}:")
                    print(f"  Title: {job.get('title', 'N/A')}")
                    print(f"  Company: {job.get('company', 'N/A')}")
                    print(f"  Location: {job.get('location', 'N/A')}")
                    print(f"  Source: {job.get('source', 'N/A')}")
                    print(f"  HR Email: {job.get('hr_emails', 'N/A')}")
                    print(f"  HR Phone: {job.get('hr_phones', 'N/A')}")
            else:
                print("✗ CSV file was not created")
        else:
            print("No jobs data found during test")
        
        # Test individual components
        print("\n--- Testing Individual Components ---")
        
        # Test email extraction
        test_text = "Contact us at hr@company.com or careers@fintech.co.in"
        emails = scraper.extract_email_from_text(test_text)
        print(f"✓ Email extraction test: {emails}")
        
        # Test phone extraction
        test_text = "Call us at 9876543210 or +91-9876543210"
        phones = scraper.extract_phone_from_text(test_text)
        print(f"✓ Phone extraction test: {phones}")
        
        # Test job validation
        test_job = {
            'title': 'SDE Backend Developer',
            'company': 'Paytm',
            'description': 'We are hiring fresh SDE developers for our payment platform. PPO available for top performers.',
            'location': 'Bangalore'
        }
        is_valid = scraper.validate_job(test_job)
        print(f"✓ Job validation test: {is_valid}")
        
        print("\n=== Test Completed Successfully ===")
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if scraper.driver:
            scraper.driver.quit()

def test_data_quality():
    """Test data quality metrics"""
    print("\n=== Testing Data Quality ===")
    
    # Sample test data
    test_jobs = [
        {
            'title': 'SDE Backend Developer',
            'company': 'Paytm',
            'location': 'Bangalore',
            'description': 'Hiring fresh SDE developers for payment platform. Contact hr@paytm.com',
            'apply_link': 'https://paytm.com/careers/job1',
            'hr_emails': 'hr@paytm.com',
            'hr_phones': '9876543210',
            'source': 'company_career',
            'scraped_at': '2024-01-01T10:00:00'
        },
        {
            'title': 'Software Engineer Backend',
            'company': 'Razorpay',
            'location': 'Mumbai',
            'description': 'Looking for backend engineers. Apply at careers@razorpay.com',
            'apply_link': 'https://razorpay.com/careers/job2',
            'hr_emails': 'careers@razorpay.com',
            'hr_phones': '',
            'source': 'naukri',
            'scraped_at': '2024-01-01T11:00:00'
        }
    ]
    
    scraper = FintechJobScraper()
    scraper.jobs_data = test_jobs
    
    # Test verification
    scraper.verify_data_quality()
    
    # Test CSV export
    scraper.save_to_csv("quality_test_jobs.csv")
    
    if os.path.exists("quality_test_jobs.csv"):
        df = pd.read_csv("quality_test_jobs.csv")
        print(f"✓ Quality test CSV created with {len(df)} rows")
        print(f"✓ All required fields present: {all(col in df.columns for col in ['title', 'company', 'description'])}")
    
    print("✓ Data quality test completed")

if __name__ == "__main__":
    test_scraper()
    test_data_quality()
