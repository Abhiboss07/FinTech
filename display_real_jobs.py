"""
Display Real Fintech Jobs with direct job posting links
"""

import pandas as pd
from tabulate import tabulate
import os
import glob

def get_latest_real_csv_file():
    """Get the latest real CSV file from data folder"""
    latest_file = 'data/latest_real_fintech_jobs.csv'
    if os.path.exists(latest_file):
        return latest_file
    
    pattern = os.path.join('data', 'real_fintech_jobs_*.csv')
    files = glob.glob(pattern)
    
    if not files:
        return None
    
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def display_real_jobs_table():
    """Display real jobs with direct posting links"""
    csv_file = get_latest_real_csv_file()
    
    if not csv_file:
        print("❌ No real job CSV files found. Please run real_job_scraper.py first.")
        return
    
    try:
        df = pd.read_csv(csv_file)
        
        display_df = df[['company_name', 'offered_position', 'direct_apply_link', 'hr_email']]
        display_df.columns = ['Company', 'Position', 'Job Posting Link', 'HR Email']
        
        print("\n" + "="*140)
        print("🚀 REAL FINTECH JOB POSTINGS")
        print(f"📁 Source: {csv_file}")
        print("🔗 Direct links to actual job postings (like Grok)")
        print("="*140)
        
        table = tabulate(display_df.values, headers=display_df.columns, 
                        tablefmt='grid', maxcolwidths=[15, 30, 50, 20])
        
        print(table)
        print("="*140)
        
        print("\n📋 JOB DETAILS:")
        print("="*140)
        
        for index, row in df.iterrows():
            print(f"\n🏢 {row['company_name']} - {row['offered_position']}")
            print("-" * 100)
            print(f"🔗 Job Posting: {row['direct_apply_link']}")
            print(f"📧 HR Email: {row['hr_email']}")
            print(f"📄 Description: {row['job_description']}")
            print()
        
        print("="*140)
        print(f"📊 Total Jobs: {len(df)}")
        print("🎉 Click the Job Posting links to view full job details and apply directly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    display_real_jobs_table()
