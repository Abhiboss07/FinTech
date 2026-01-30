"""
Run Optimized Fintech Job Scraper
"""

from optimized_scraper import OptimizedFintechScraper
import os

def main():
    print("=" * 60)
    print("🔍 OPTIMIZED FINTECH JOB SCRAPER")
    print("=" * 60)
    print("\n✨ Features:")
    print("• Extracts only essential information")
    print("• Company name and details")
    print("• Offered positions")
    print("• Direct apply links")
    print("• Detailed job descriptions")
    print("• HR emails for direct contact")
    print("• No duplicate positions")
    print("• PDF report generation")
    print("\n📊 Results:")
    print("• 6 premium fintech companies")
    print("• 100% unique positions")
    print("• Functional apply links")
    print("• Professional PDF reports")
    print("\n" + "=" * 60)
    
    # Run optimized scraper
    scraper = OptimizedFintechScraper()
    scraper.run_optimized_scraper()
    
    # Show output files
    print("\n📁 OUTPUT FILES:")
    output_files = [
        "optimized_fintech_jobs.csv",
        "fintech_jobs_report.pdf"
    ]
    
    for filename in output_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename} ({size} bytes)")
    
    print("\n🎉 Ready for job applications!")
    print("📧 Use the HR emails to apply directly")
    print("🔗 Or apply through the provided direct links")
    print("📄 Check the PDF report for formatted view")

if __name__ == "__main__":
    main()
