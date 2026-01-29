"""
Simple runner script for the Fintech Job Scraper
"""

from enhanced_scraper import EnhancedFintechJobScraper
import os

def main():
    """Main function to run the scraper"""
    print("=" * 60)
    print("🏦 FINTECH JOB SCRAPER FOR FRESHERS WITH PPO LETTERS")
    print("=" * 60)
    print("\nThis scraper will:")
    print("✓ Search major fintech companies for SDE/Backend roles")
    print("✓ Filter for fresher-friendly positions with PPO opportunities")
    print("✓ Extract HR contact information (emails, phones)")
    print("✓ Save comprehensive job details to CSV, Excel, and JSON")
    print("✓ Verify data quality and provide detailed reports")
    print("\n" + "=" * 60)
    
    # Initialize and run scraper
    scraper = EnhancedFintechJobScraper()
    scraper.run_scraper()
    
    # Show output files
    print("\n" + "=" * 60)
    print("📁 OUTPUT FILES CREATED:")
    print("=" * 60)
    
    output_files = [
        "fintech_jobs.csv",
        "fintech_jobs.xlsx", 
        "fintech_jobs.json"
    ]
    
    for filename in output_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✓ {filename} ({size} bytes)")
        else:
            print(f"✗ {filename} (not found)")
    
    print("\n" + "=" * 60)
    print("🎉 SCRAPING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open fintech_jobs.csv to view all job listings")
    print("2. Use fintech_jobs.xlsx for better formatting")
    print("3. Check fintech_jobs.json for programmatic access")
    print("4. Verify contact information before applying")
    print("5. Tailor your resume for each application")
    print("\nGood luck with your job search! 🚀")

if __name__ == "__main__":
    main()
