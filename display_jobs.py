"""
Display Fintech Jobs in a properly formatted table
"""

import pandas as pd
from tabulate import tabulate

def display_jobs_table():
    """Display jobs in a properly formatted table"""
    try:
        # Read the CSV file
        df = pd.read_csv('optimized_fintech_jobs.csv')
        
        # Select relevant columns for display
        display_df = df[['company_name', 'company_details', 'offered_position', 'direct_apply_link', 'hr_email']]
        
        # Rename columns for better display
        display_df.columns = ['Company', 'Details', 'Position', 'Apply Link', 'HR Email']
        
        # Display using tabulate for better formatting
        print("\n" + "="*120)
        print("🚀 FINTECH JOB OPPORTUNITIES")
        print("="*120)
        
        # Create table with tabulate
        table = tabulate(display_df.values, headers=display_df.columns, 
                        tablefmt='grid', maxcolwidths=[15, 40, 25, 35, 20])
        
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
        
    except FileNotFoundError:
        print("❌ CSV file not found. Please run the scraper first.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    display_jobs_table()
