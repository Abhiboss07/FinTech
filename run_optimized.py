"""
Run Optimized Fintech Job Scraper
"""

from optimized_scraper import OptimizedFintechScraper
import os

def main():
    print("=" * 60)
    print("🚀 OPTIMIZED FINTECH JOB SCRAPER")
    print("=" * 60)
    print("\n✨ Features:")
    print("• Verified HR emails only")
    print("• Direct apply links")
    print("• Clean & efficient code")
    print("• No unnecessary dependencies")
    print("• Fast scraping")
    print("\n" + "=" * 60)
    
    # Run scraper
    scraper = OptimizedFintechScraper()
    scraper.run_scraper()
    
    # Show output files
    print("\n📁 OUTPUT FILES:")
    output_files = [
        "optimized_fintech_jobs.csv",
        "optimized_fintech_jobs.xlsx",
        "optimized_fintech_jobs.json"
    ]
    
    for filename in output_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename} ({size} bytes)")
    
    print("\n🎉 Ready for job applications!")

if __name__ == "__main__":
    main()
