"""
Display Fintech Jobs in a properly formatted table
"""

import pandas as pd
from tabulate import tabulate
import os
import glob

def get_latest_csv_file():
    """Get the latest CSV file from data folder"""
    # First try to get the latest file
    latest_file = 'data/latest_fintech_jobs.csv'
    if os.path.exists(latest_file):
        return latest_file
    
    # If latest doesn't exist, get the most recent file
    pattern = os.path.join('data', 'fintech_jobs_*.csv')
    files = glob.glob(pattern)
    
    if not files:
        return None
    
    # Sort by modification time, get the latest
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def display_jobs_table():
    """Display jobs in a properly formatted table"""
    # Get the latest CSV file
    csv_file = get_latest_csv_file()
    
    if not csv_file:
        print("❌ No CSV files found. Please run the scraper first.")
        return
    
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Select relevant columns for display
        display_df = df[['company_name', 'offered_position', 'direct_apply_link', 'hr_email']]
        
        # Rename columns for better display
        display_df.columns = ['Company', 'Position', 'Apply Link', 'HR Email']
        
        # Display using tabulate for better formatting
        print("\n" + "="*120)
        print("🚀 FINTECH JOB OPPORTUNITIES")
        print(f"📁 Source: {csv_file}")
        print("="*120)
        
        # Create table with tabulate
        table = tabulate(display_df.values, headers=display_df.columns, 
                        tablefmt='grid', maxcolwidths=[15, 30, 35, 25])
        
        print(table)
        print("="*120)
        
        # Show detailed descriptions
        print("\n📋 DETAILED JOB DESCRIPTIONS:")
        print("="*120)
        
        for index, row in df.iterrows():
            print(f"\n🏢 {row['company_name']} - {row['offered_position']}")
            print("-" * 80)
            print(f"📧 HR Email: {row['hr_email']}")
            print(f"🔗 Apply Link: {row['direct_apply_link']}")
            print(f"\n📄 Description:")
            print(f"   {row['job_description']}")
            print()
        
        print("="*120)
        print(f"📊 Total Jobs: {len(df)}")
        print("🎉 Ready for applications!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def list_all_data_files():
    """List all data files in the data folder"""
    pattern = os.path.join('data', 'fintech_jobs_*.csv')
    files = glob.glob(pattern)
    
    if not files:
        print("❌ No data files found.")
        return
    
    print("\n📁 Available Data Files:")
    print("="*50)
    
    # Sort files by sequence number
    files.sort()
    
    for file in files:
        basename = os.path.basename(file)
        size = os.path.getsize(file)
        mtime = os.path.getmtime(file)
        time_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"📄 {basename} ({size} bytes) - {time_str}")
    
    # Also show latest file if it exists
    latest_file = 'data/latest_fintech_jobs.csv'
    if os.path.exists(latest_file):
        size = os.path.getsize(latest_file)
        mtime = os.path.getmtime(latest_file)
        time_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"🔄 latest_fintech_jobs.csv ({size} bytes) - {time_str} [CURRENT]")

if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        list_all_data_files()
    else:
        display_jobs_table()
