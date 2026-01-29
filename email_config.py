"""
Email Configuration File
Update your personal information here
"""

# Gmail Configuration
GMAIL_USER = "your.email@gmail.com"  # UPDATE WITH YOUR GMAIL
APP_PASSWORD = "joew lgfh xoev jhpd"  # Your app password

# Personal Information
PERSONAL_INFO = {
    'name': 'Your Name',  # UPDATE: Your full name
    'phone': '+91-9876543210',  # UPDATE: Your phone number
    'education': 'Bachelor of Technology in Computer Science',
    'college': 'Your College Name',  # UPDATE: Your college name
    'graduation_year': '2024',  # UPDATE: Your graduation year
    'skills': [
        'Python', 'Java', 'JavaScript', 'React', 'Node.js', 
        'SQL', 'MongoDB', 'Git', 'Docker', 'REST APIs'
    ],  # UPDATE: Your technical skills
    'github': 'https://github.com/yourusername',  # UPDATE: Your GitHub profile
    'linkedin': 'https://linkedin.com/in/yourprofile',  # UPDATE: Your LinkedIn profile
    'portfolio': 'https://yourportfolio.com'  # UPDATE: Your portfolio website
}

# Resume Configuration
RESUME_PATH = "resume.pdf"  # Path to your resume file
ATTACH_RESUME = True  # Set to True to attach resume to emails

# Email Sending Configuration
DELAY_BETWEEN_EMAILS = 30  # Seconds to wait between emails (recommended: 30-60)
MAX_RETRIES = 3  # Maximum retry attempts for failed emails

# Email Templates Configuration
USE_PERSONALIZED_TEMPLATES = True  # Use personalized email templates
INCLUDE_COVER_LETTER = True  # Include cover letter in email body

# Logging Configuration
SAVE_EMAIL_LOGS = True  # Save sent/failed email logs
LOG_FILE_PATH = "email_logs/"  # Directory to save email logs

# Application Configuration
AUTO_APPLY_TO_PORTALS = False  # Auto-apply through job portals (requires additional setup)
SKIP_DUPLICATE_COMPANIES = True  # Skip if already applied to same company

# Email Content Configuration
EMAIL_SIGNATURE = """
Best regards,

{name}
{education} Graduate
📱 {phone}
📧 {email}
💼 {linkedin}
🐙 {github}
"""

# Follow-up Configuration
SEND_FOLLOW_UP_EMAILS = True  # Send follow-up emails after 7 days
FOLLOW_UP_DELAY_DAYS = 7  # Days to wait before sending follow-up
