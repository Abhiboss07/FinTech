"""
Main Email Campaign Runner
Execute this to send automated job applications
"""

import os
import sys
from datetime import datetime
import pandas as pd
from email_automation import JobEmailAutomation
from email_config import *

def setup_configuration():
    """Setup and validate configuration"""
    print("🔧 Setting up Email Campaign Configuration...")
    
    # Validate Gmail configuration
    if GMAIL_USER == "your.email@gmail.com":
        print("❌ Please update your Gmail address in email_config.py")
        return False
    
    if APP_PASSWORD == "joew lgfh xoev jhpd":
        print("⚠️  Using provided app password")
    
    # Validate personal information
    if PERSONAL_INFO['name'] == 'Your Name':
        print("❌ Please update your personal information in email_config.py")
        return False
    
    print("✅ Configuration validated successfully")
    return True

def preview_emails(csv_file="fintech_jobs.csv"):
    """Preview emails before sending"""
    print("\n📧 Email Preview Mode")
    print("=" * 50)
    
    # Load job data
    try:
        df = pd.read_csv(csv_file)
        jobs_with_email = df[df['hr_emails'].notna() & (df['hr_emails'] != '')]
        
        if jobs_with_email.empty:
            print("❌ No jobs with HR emails found in CSV")
            return
        
        print(f"📊 Found {len(jobs_with_email)} jobs with HR contacts")
        print("\n📋 Preview of first 3 emails:")
        
        # Initialize email bot
        email_bot = JobEmailAutomation(GMAIL_USER, APP_PASSWORD)
        email_bot.update_personal_info(**PERSONAL_INFO)
        
        for i, (_, job) in enumerate(jobs_with_email.head(3).iterrows()):
            print(f"\n--- Email {i+1} ---")
            print(f"Company: {job['company']}")
            print(f"To: {job['hr_emails']}")
            
            # Generate email preview
            email_data = email_bot.generate_personalized_email(job.to_dict())
            print(f"Subject: {email_data['subject']}")
            print(f"Body Preview: {email_data['body'][:200]}...")
            print("-" * 30)
        
        return True
        
    except Exception as e:
        print(f"❌ Error previewing emails: {e}")
        return False

def send_emails():
    """Send emails to all HR contacts"""
    print("\n🚀 Starting Email Campaign")
    print("=" * 50)
    
    # Initialize email bot
    email_bot = JobEmailAutomation(GMAIL_USER, APP_PASSWORD)
    email_bot.update_personal_info(**PERSONAL_INFO)
    
    # Check if resume exists
    resume_path = RESUME_PATH if ATTACH_RESUME and os.path.exists(RESUME_PATH) else None
    if ATTACH_RESUME and not resume_path:
        print(f"⚠️  Resume file '{RESUME_PATH}' not found. Sending emails without attachment.")
    
    # Send bulk emails
    result = email_bot.send_bulk_emails(
        csv_file="fintech_jobs.csv",
        resume_path=resume_path,
        delay_between_emails=DELAY_BETWEEN_EMAILS
    )
    
    return result

def show_campaign_summary():
    """Show campaign summary and logs"""
    print("\n📊 Campaign Summary")
    print("=" * 50)
    
    # Check for log files
    log_files = ['sent_emails.csv', 'failed_emails.csv']
    
    for log_file in log_files:
        if os.path.exists(log_file):
            df = pd.read_csv(log_file)
            print(f"\n📄 {log_file}:")
            print(f"   Total entries: {len(df)}")
            
            if log_file == 'sent_emails.csv' and not df.empty:
                print("   Companies contacted:")
                for company in df['company'].unique()[:5]:
                    print(f"   • {company}")
                if len(df['company'].unique()) > 5:
                    print(f"   ... and {len(df['company'].unique()) - 5} more")
        else:
            print(f"\n📄 {log_file}: Not found")

def main():
    """Main execution function"""
    print("🏦 FINTECH JOB EMAIL AUTOMATION")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Setup configuration
    if not setup_configuration():
        print("\n❌ Configuration setup failed. Please update email_config.py")
        return
    
    # Preview emails
    print("\n📋 Step 1: Preview Emails")
    if not preview_emails():
        return
    
    # Ask for confirmation
    print("\n" + "=" * 50)
    print("⚠️  READY TO SEND EMAILS")
    print("=" * 50)
    print(f"📧 From: {GMAIL_USER}")
    print(f"⏱️  Delay: {DELAY_BETWEEN_EMAILS} seconds between emails")
    print(f"📎 Resume: {'Attached' if ATTACH_RESUME else 'Not attached'}")
    
    confirm = input("\n🤔 Do you want to proceed with sending emails? (yes/no): ").lower().strip()
    
    if confirm not in ['yes', 'y']:
        print("❌ Email campaign cancelled")
        return
    
    # Send emails
    print("\n📋 Step 2: Send Emails")
    result = send_emails()
    
    # Show summary
    print("\n📋 Step 3: Campaign Summary")
    show_campaign_summary()
    
    print(f"\n🎉 Campaign completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Results: {result['sent']} sent, {result['failed']} failed, {result['total']} total")
    
    if result['sent'] > 0:
        print("\n✅ Success! Check your email inbox for sent messages.")
        print("📈 Monitor your responses and follow up as needed.")
    
    if result['failed'] > 0:
        print("\n⚠️  Some emails failed. Check failed_emails.csv for details.")
        print("🔄 You can retry failed emails later.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Email campaign interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
