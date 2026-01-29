# Email Automation Setup Guide

## 🚀 Quick Setup Instructions

### 1. Update Your Personal Information

Edit `email_config.py` and update the following:

```python
# Gmail Configuration
GMAIL_USER = "abhicps19@gmail.com"  # UPDATE THIS

# Personal Information
PERSONAL_INFO = {
    'name': 'Abhishek Yadav',  # UPDATE THIS
    'phone': '+91-9580818926',  # UPDATE THIS
    'college': 'Veer Bahadur Singh Purvanchal University',  # UPDATE THIS
    'github': 'https://github.com/Abhiboss07',  # UPDATE THIS
    'linkedin': 'https://www.linkedin.com/in/abhishek-yadav-4738032b7/',  # UPDATE THIS
    'portfolio': 'https://portfolio-abhishek-01.vercel.app/'  # UPDATE THIS
}
```

### 2. Gmail App Password Setup

Since you provided the app password, here's how to ensure it works:

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" for app and "Other (Custom name)" for device
   - Enter "Fintech Job Scraper" as the name
   - Copy the 16-character password

3. **Update App Password** in `email_config.py` if needed

### 3. Test the System

Run the test suite:

```bash
python test_email_system.py
```

### 4. Run Email Campaign

Once all tests pass:

```bash
python run_email_campaign.py
```

## 📧 Email Features

### ✅ What the System Does:

- **Personalized Emails**: Each email is customized for the specific company and role
- **Professional Templates**: Humanized, professional email content
- **Contact Extraction**: Automatically uses HR emails from your CSV data
- **Skill Matching**: Highlights relevant skills based on job descriptions
- **Company Research**: Includes company-specific information in emails
- **Resume Attachment**: Optionally attaches your resume
- **Email Tracking**: Logs sent and failed emails
- **Rate Limiting**: Respects email sending limits with delays

### 📊 Email Content Includes:

- Personalized greeting
- Company-specific introduction
- Skills and experience highlights
- Education background
- Contact information
- Professional signature
- Call to action

### 🎯 Personalization Features:

- **Company Name**: References the specific company
- **Job Title**: Mentions the exact position
- **Skills Matching**: Highlights relevant technical skills
- **Company Specialization**: References company's focus area
- **Location Awareness**: Considers job location
- **Professional Tone**: Maintains professional communication

## 📈 Campaign Management

### Before Sending:

1. **Review Personal Info**: Ensure all details are accurate
2. **Test Connection**: Verify Gmail connectivity
3. **Preview Emails**: Check email content before sending
4. **Prepare Resume**: Have resume ready if attaching

### During Campaign:

- **Progress Tracking**: Real-time progress updates
- **Error Handling**: Automatic retry for failed emails
- **Rate Limiting**: 30-second delays between emails
- **Logging**: Detailed logs of all activities

### After Campaign:

- **Sent Emails Log**: `sent_emails.csv`
- **Failed Emails Log**: `failed_emails.csv`
- **Response Tracking**: Monitor your Gmail for responses
- **Follow-up**: Send follow-up emails after 7 days

## 🔧 Configuration Options

### Email Settings:
- `DELAY_BETWEEN_EMAILS`: Time between emails (default: 30 seconds)
- `ATTACH_RESUME`: Whether to attach resume file
- `RESUME_PATH`: Path to your resume file

### Content Settings:
- `USE_PERSONALIZED_TEMPLATES`: Enable personalization
- `INCLUDE_COVER_LETTER`: Include cover letter in body
- `SEND_FOLLOW_UP_EMAILS`: Enable follow-up emails

### Logging Settings:
- `SAVE_EMAIL_LOGS`: Save email activity logs
- `LOG_FILE_PATH`: Directory for log files

## 📋 Sample Email Content

The system generates emails like this:

```
Subject: Application for SDE Backend Developer Position - Your Name

Dear Hiring Manager,

I came across the SDE Backend Developer position at Paytm through your careers page, and I'm excited to apply for this opportunity.

As a recent Bachelor of Technology in Computer Science graduate from Your College, I have been actively seeking opportunities to start my career in the fintech space. Your company's innovative work in digital payments and financial services particularly resonates with my interests and career aspirations.

My technical skills include:
• Python
• JavaScript
• SQL
• MongoDB
• React
• Node.js

During my academic journey, I developed strong problem-solving abilities and a passion for building scalable backend systems...

[Continue with professional content]

Best regards,

Your Name
Bachelor of Technology in Computer Science Graduate
📱 +91-9876543210
📧 your.email@gmail.com
💼 https://linkedin.com/in/yourprofile
🐙 https://github.com/yourusername
```

## ⚠️ Important Notes

### Email Best Practices:
- **Professional Tone**: Maintain professional communication
- **Personalization**: Each email is customized
- **No Spam**: Only send to legitimate HR contacts
- **Follow Guidelines**: Respect email sending limits

### Legal Considerations:
- **Consent**: Only email companies with published HR contacts
- **Professional Use**: Use for legitimate job applications
- **Data Privacy**: Respect company data and privacy

### Technical Notes:
- **Gmail Limits**: Gmail has daily sending limits
- **App Password**: Use app password, not regular password
- **2FA Required**: 2-factor authentication required
- **Internet Connection**: Stable connection required

## 🆘 Troubleshooting

### Common Issues:

1. **Gmail Authentication Error**:
   - Enable 2-factor authentication
   - Generate new app password
   - Check email and password accuracy

2. **No HR Emails Found**:
   - Check CSV file for hr_emails column
   - Ensure emails are in valid format
   - Run scraper again to get fresh data

3. **Email Sending Failed**:
   - Check internet connection
   - Verify Gmail credentials
   - Check for spam filters

4. **Personalization Not Working**:
   - Update personal info in config
   - Check CSV data format
   - Verify company names match

## 📞 Support

If you encounter issues:

1. **Run Tests**: `python test_email_system.py`
2. **Check Logs**: Review error messages
3. **Verify Config**: Ensure all settings are correct
4. **Test Connection**: Verify Gmail connectivity

## 🎉 Success Tips

1. **Complete Profile**: Fill in all personal information
2. **Professional Resume**: Have a polished resume ready
3. **Customize Skills**: Update skills to match your profile
4. **Monitor Responses**: Check Gmail for replies
5. **Follow Up**: Send follow-up emails when appropriate

---

**Ready to start your job application campaign?** 🚀

1. Update `email_config.py` with your details
2. Run `python test_email_system.py` to verify setup
3. Execute `python run_email_campaign.py` to send emails
