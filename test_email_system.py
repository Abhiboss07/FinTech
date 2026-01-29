"""
Test Email System - Safe testing without sending actual emails
"""

import pandas as pd
from email_automation import JobEmailAutomation
from email_config import *
import os

def test_email_generation():
    """Test email generation without sending"""
    print("🧪 Testing Email Generation System...")
    
    # Initialize email bot
    email_bot = JobEmailAutomation(GMAIL_USER, APP_PASSWORD)
    email_bot.update_personal_info(**PERSONAL_INFO)
    
    # Load sample job data
    try:
        df = pd.read_csv("fintech_jobs.csv")
        jobs_with_email = df[df['hr_emails'].notna() & (df['hr_emails'] != '')]
        
        if jobs_with_email.empty:
            print("❌ No jobs with HR emails found for testing")
            return
        
        print(f"📊 Testing with {len(jobs_with_email)} jobs")
        
        # Test email generation for each job
        for i, (_, job) in enumerate(jobs_with_email.iterrows(), 1):
            print(f"\n--- Test Email {i} ---")
            print(f"Company: {job['company']}")
            print(f"Position: {job['title']}")
            print(f"HR Email: {job['hr_emails']}")
            
            # Generate email
            email_data = email_bot.generate_personalized_email(job.to_dict())
            
            print(f"Subject: {email_data['subject']}")
            print(f"Body Length: {len(email_data['body'])} characters")
            print(f"Personalization: {'✅' if job['company'].lower() in email_data['body'].lower() else '❌'}")
            print(f"Skills Mentioned: {'✅' if any(skill.lower() in email_data['body'].lower() for skill in PERSONAL_INFO['skills']) else '❌'}")
            
            # Validate email content
            validation_score = validate_email_content(email_data, job)
            print(f"Content Quality: {validation_score}/10")
            
            if i >= 3:  # Test first 3 emails
                break
        
        print("\n✅ Email generation test completed successfully")
        
    except Exception as e:
        print(f"❌ Error in email generation test: {e}")

def validate_email_content(email_data, job_data):
    """Validate email content quality"""
    score = 0
    max_score = 10
    
    body = email_data['body'].lower()
    subject = email_data['subject'].lower()
    
    # Check for personalization
    if job_data['company'].lower() in body:
        score += 2
    if job_data['title'].lower() in body:
        score += 1
    
    # Check for professional elements
    if 'dear hiring manager' in body:
        score += 1
    if 'best regards' in body:
        score += 1
    if PERSONAL_INFO['name'].lower() in body:
        score += 1
    
    # Check for skills
    skills_mentioned = sum(1 for skill in PERSONAL_INFO['skills'] if skill.lower() in body)
    if skills_mentioned >= 3:
        score += 2
    elif skills_mentioned >= 1:
        score += 1
    
    # Check for contact information
    if PERSONAL_INFO['phone'] in body:
        score += 1
    if GMAIL_USER in body:
        score += 1
    
    return score

def test_gmail_connection():
    """Test Gmail connection without sending emails"""
    print("\n🧪 Testing Gmail Connection...")
    
    try:
        email_bot = JobEmailAutomation(GMAIL_USER, APP_PASSWORD)
        server = email_bot.connect_to_gmail()
        
        if server:
            print("✅ Gmail connection successful")
            server.quit()
            return True
        else:
            print("❌ Gmail connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gmail connection: {e}")
        return False

def test_csv_data():
    """Test CSV data loading and validation"""
    print("\n🧪 Testing CSV Data Loading...")
    
    try:
        df = pd.read_csv("fintech_jobs.csv")
        print(f"✅ CSV loaded successfully")
        print(f"📊 Total jobs: {len(df)}")
        
        # Check for required columns
        required_columns = ['title', 'company', 'hr_emails', 'description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            return False
        
        print("✅ All required columns present")
        
        # Check for HR emails
        jobs_with_email = df[df['hr_emails'].notna() & (df['hr_emails'] != '')]
        print(f"📧 Jobs with HR emails: {len(jobs_with_email)}")
        
        # Show sample data
        if not jobs_with_email.empty:
            print("\n📋 Sample job data:")
            sample_job = jobs_with_email.iloc[0]
            for col in ['title', 'company', 'hr_emails']:
                print(f"  {col}: {sample_job[col]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return False

def test_personal_info():
    """Test personal information configuration"""
    print("\n🧪 Testing Personal Information...")
    
    required_fields = ['name', 'phone', 'college', 'github', 'linkedin']
    missing_fields = [field for field in required_fields if PERSONAL_INFO.get(field) == f'Your {field.title()}' or not PERSONAL_INFO.get(field)]
    
    if missing_fields:
        print(f"⚠️  Please update these fields in email_config.py: {missing_fields}")
        return False
    
    print("✅ Personal information configured")
    print(f"📝 Name: {PERSONAL_INFO['name']}")
    print(f"📱 Phone: {PERSONAL_INFO['phone']}")
    print(f"🎓 College: {PERSONAL_INFO['college']}")
    print(f"🔗 GitHub: {PERSONAL_INFO['github']}")
    print(f"💼 LinkedIn: {PERSONAL_INFO['linkedin']}")
    
    return True

def main():
    """Run all tests"""
    print("🧪 EMAIL SYSTEM TESTING SUITE")
    print("=" * 50)
    
    tests = [
        ("CSV Data Loading", test_csv_data),
        ("Personal Information", test_personal_info),
        ("Email Generation", test_email_generation),
        ("Gmail Connection", test_gmail_connection)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System ready for email campaign.")
    else:
        print("⚠️  Some tests failed. Please fix issues before running email campaign.")
    
    return passed == total

if __name__ == "__main__":
    main()
