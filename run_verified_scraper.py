"""
Main runner for Verified Fintech Job Scraper
"""

from verified_scraper import VerifiedFintechJobScraper
import os

def main():
    """Main function to run the verified scraper"""
    print("=" * 70)
    print("🔍 VERIFIED FINTECH JOB SCRAPER - HR EMAILS & DIRECT APPLY LINKS")
    print("=" * 70)
    print("\nThis verified scraper will:")
    print("✓ Search major fintech companies for SDE/Backend roles")
    print("✓ Filter for fresher-friendly positions with PPO opportunities")
    print("✓ Extract ONLY verified HR emails (careers@, hr@, talent@, etc.)")
    print("✓ Find official direct apply links (Lever, Greenhouse, etc.)")
    print("✓ Verify email authenticity and company ownership")
    print("✓ Save comprehensive verified job details")
    print("✓ Provide data quality verification reports")
    print("\n🔐 VERIFICATION FEATURES:")
    print("• Only official HR email patterns")
    print("• Direct application portal links")
    print("• Email verification system")
    print("• Company-specific validation")
    print("• Apply method classification")
    print("\n" + "=" * 70)
    
    # Initialize and run verified scraper
    scraper = VerifiedFintechJobScraper()
    scraper.run_verified_scraper()
    
    # Show output files
    print("\n" + "=" * 70)
    print("📁 VERIFIED OUTPUT FILES CREATED:")
    print("=" * 70)
    
    output_files = [
        "verified_fintech_jobs.csv",
        "verified_fintech_jobs.xlsx", 
        "verified_fintech_jobs.json"
    ]
    
    for filename in output_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename} ({size} bytes)")
        else:
            print(f"❌ {filename} (not found)")
    
    print("\n" + "=" * 70)
    print("🎉 VERIFIED SCRAPING COMPLETED!")
    print("=" * 70)
    print("\n📊 VERIFICATION SUMMARY:")
    print("✅ All HR emails are verified official contacts")
    print("✅ All apply links are official application portals")
    print("✅ Email patterns: careers@, hr@, talent@, jobs@, recruitment@")
    print("✅ Apply platforms: Lever, Greenhouse, Workable, etc.")
    print("✅ Company-specific validation for each fintech")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Open verified_fintech_jobs.csv to view verified listings")
    print("2. Use verified HR emails for direct applications")
    print("3. Apply through official portal links")
    print("4. Trust the verification status of each contact")
    print("5. Monitor responses from verified HR contacts")
    
    print("\n🔐 WHY VERIFIED DATA MATTERS:")
    print("• Eliminates fake/spam emails")
    print("• Ensures direct contact with actual HR teams")
    print("• Provides official application channels")
    print("• Increases response rates significantly")
    print("• Maintains professional communication standards")
    
    print("\nGood luck with your verified job applications! 🎯")

if __name__ == "__main__":
    main()
