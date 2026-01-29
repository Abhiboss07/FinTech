"""
Email Automation Module for Fintech Job Applications
Sends personalized emails to HR contacts and applies for jobs automatically
"""

import smtplib
import pandas as pd
import time
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
import re
from typing import List, Dict, Optional

class JobEmailAutomation:
    def __init__(self, gmail_user: str, app_password: str):
        """
        Initialize email automation with Gmail credentials
        
        Args:
            gmail_user: Your Gmail address
            app_password: Gmail app password (not regular password)
        """
        self.gmail_user = gmail_user
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sent_emails = []
        self.failed_emails = []
        
        # Personal information for customization
        self.personal_info = {
            'name': 'Your Name',  # Update this
            'phone': 'Your Phone Number',  # Update this
            'education': 'Bachelor of Technology in Computer Science',
            'college': 'Your College Name',  # Update this
            'graduation_year': '2024',
            'skills': ['Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB'],
            'github': 'https://github.com/yourusername',  # Update this
            'linkedin': 'https://linkedin.com/in/yourprofile',  # Update this
            'portfolio': 'https://yourportfolio.com'  # Update this
        }

    def update_personal_info(self, **kwargs):
        """Update personal information for email customization"""
        self.personal_info.update(kwargs)

    def connect_to_gmail(self):
        """Establish connection to Gmail SMTP server"""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.gmail_user, self.app_password)
            return server
        except Exception as e:
            print(f"❌ Failed to connect to Gmail: {e}")
            return None

    def load_job_data(self, csv_file: str = "fintech_jobs.csv") -> List[Dict]:
        """Load job data from CSV file"""
        try:
            df = pd.read_csv(csv_file)
            # Filter jobs with HR emails
            jobs_with_email = df[df['hr_emails'].notna() & (df['hr_emails'] != '')]
            return jobs_with_email.to_dict('records')
        except Exception as e:
            print(f"❌ Error loading CSV file: {e}")
            return []

    def generate_personalized_email(self, job_data: Dict) -> Dict[str, str]:
        """Generate personalized email content based on job data"""
        
        company = job_data.get('company', 'the company')
        title = job_data.get('title', 'Software Developer')
        location = job_data.get('location', 'your location')
        description = job_data.get('description', '')
        
        # Extract key skills from job description
        job_skills = self.extract_skills_from_description(description)
        
        # Customize skills based on job requirements
        relevant_skills = self.get_relevant_skills(job_skills)
        
        # Generate email subject
        subject_options = [
            f"Application for {title} Position - {self.personal_info['name']}",
            f"Interested in {title} Role - {self.personal_info['name']} - {self.personal_info['education']}",
            f"Fresher Application for {title} - {self.personal_info['name']}",
            f"Job Application: {title} at {company} - {self.personal_info['name']}"
        ]
        
        subject = random.choice(subject_options)
        
        # Generate email body
        email_body = f"""Dear Hiring Manager,

I hope this email finds you well. I came across the {title} position at {company} through your careers page, and I'm excited to apply for this opportunity.

As a recent {self.personal_info['education']} graduate from {self.personal_info['college']}, I have been actively seeking opportunities to start my career in the fintech space. Your company's innovative work in {self.get_company_specialization(company)} particularly resonates with my interests and career aspirations.

My technical skills include:
{self.format_skills_list(relevant_skills)}

During my academic journey, I developed strong problem-solving abilities and a passion for building scalable backend systems. I've worked on several projects that demonstrate my capability in {self.get_key_projects(relevant_skills)}.

What excites me most about this role at {company} is {self.get_company_specific_interest(company, description)}. I believe my fresh perspective, combined with my technical foundation and eagerness to learn, would make me a valuable addition to your team.

I'm particularly interested in this fresher-friendly position and would welcome the opportunity to discuss how my skills and enthusiasm align with your team's needs. I'm available for immediate joining and excited about the possibility of contributing to {company}'s mission.

Key highlights:
• {self.personal_info['education']} from {self.personal_info['college']} ({self.personal_info['graduation_year']})
• Strong foundation in {', '.join(relevant_skills[:3])}
• Eager to learn and grow in a fintech environment
• Available for immediate joining
• Strong problem-solving and analytical skills

Please find my contact details below:
📧 Email: {self.gmail_user}
📱 Phone: {self.personal_info['phone']}
💼 LinkedIn: {self.personal_info['linkedin']}
🐙 GitHub: {self.personal_info['github']}
🌐 Portfolio: {self.personal_info['portfolio']}

I would appreciate the opportunity to discuss my application further. Thank you for considering my profile, and I look forward to hearing from you soon.

Best regards,

{self.personal_info['name']}
{self.personal_info['education']} Graduate
📱 {self.personal_info['phone']}
📧 {self.gmail_user}
💼 {self.personal_info['linkedin']}
🐙 {self.personal_info['github']}

---
P.S. I'm particularly excited about {company}'s work in the fintech sector and would love to contribute to your innovative solutions. I'm available for an interview at your earliest convenience."""

        return {
            'subject': subject,
            'body': email_body,
            'to_email': job_data.get('hr_emails', '').split(',')[0].strip()
        }

    def extract_skills_from_description(self, description: str) -> List[str]:
        """Extract relevant skills from job description"""
        all_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'angular', 'vue.js',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'git', 'ci/cd', 'microservices', 'api', 'rest',
            'graphql', 'backend', 'frontend', 'full stack', 'devops', 'blockchain',
            'machine learning', 'data structures', 'algorithms', 'system design'
        ]
        
        found_skills = []
        description_lower = description.lower()
        
        for skill in all_skills:
            if skill in description_lower:
                found_skills.append(skill)
        
        return found_skills

    def get_relevant_skills(self, job_skills: List[str]) -> List[str]:
        """Get relevant skills based on job requirements"""
        my_skills = [skill.lower() for skill in self.personal_info['skills']]
        relevant = []
        
        for job_skill in job_skills:
            for my_skill in my_skills:
                if job_skill in my_skill or my_skill in job_skill:
                    relevant.append(my_skill)
                    break
        
        # Add some default skills if no matches found
        if not relevant:
            relevant = ['Python', 'JavaScript', 'SQL']
        
        return list(set(relevant))

    def format_skills_list(self, skills: List[str]) -> str:
        """Format skills list for email"""
        if not skills:
            return "• Programming Languages: Python, JavaScript\n• Databases: SQL, MongoDB\n• Web Technologies: React, Node.js"
        
        formatted = "• " + "\n• ".join([skill.title() if len(skill.split()) == 1 else skill for skill in skills[:5]])
        return formatted

    def get_company_specialization(self, company: str) -> str:
        """Get company specialization based on name"""
        specializations = {
            'paytm': 'digital payments and financial services',
            'phonepe': 'UPI payments and digital transactions',
            'razorpay': 'payment gateway solutions',
            'cred': 'credit card rewards and financial management',
            'upstox': 'stock trading and investment platforms',
            'zerodha': 'discount brokerage and trading platforms',
            'groww': 'investment and wealth management',
            'policybazaar': 'insurance comparison and financial products',
            'payu': 'online payment processing',
            'cashfree': 'payment and banking solutions'
        }
        
        company_lower = company.lower()
        for key, value in specializations.items():
            if key in company_lower:
                return value
        
        return 'fintech innovation and digital financial solutions'

    def get_company_specific_interest(self, company: str, description: str) -> str:
        """Generate company-specific interest statement"""
        interests = {
            'paytm': 'the opportunity to work on India\'s largest digital payment ecosystem',
            'phonepe': 'the chance to contribute to UPI infrastructure and digital payment revolution',
            'razorpay': 'the ability to build robust payment processing systems',
            'cred': 'the innovative approach to credit card rewards and financial management',
            'upstox': 'the platform\'s approach to making stock trading accessible',
            'zerodha': 'the mission to democratize investment opportunities',
            'groww': 'the focus on simplifying investment for millennials',
            'policybazaar': 'the technology-driven approach to insurance comparison',
            'payu': 'the comprehensive payment solutions for businesses',
            'cashfree': 'the innovative banking and payment API solutions'
        }
        
        company_lower = company.lower()
        for key, value in interests.items():
            if key in company_lower:
                return value
        
        return 'the company\'s innovative approach to solving real-world financial problems'

    def get_key_projects(self, skills: List[str]) -> str:
        """Get relevant project descriptions based on skills"""
        projects = {
            'python': 'developing Python-based backend systems and APIs',
            'java': 'building enterprise-level Java applications',
            'javascript': 'creating interactive web applications and RESTful APIs',
            'react': 'building responsive frontend applications',
            'node.js': 'developing scalable server-side applications',
            'sql': 'designing and optimizing database systems',
            'mongodb': 'working with NoSQL databases and document storage'
        }
        
        mentioned_projects = []
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower in projects:
                mentioned_projects.append(projects[skill_lower])
        
        if not mentioned_projects:
            mentioned_projects = ['backend development', 'API design', 'database management']
        
        return ', '.join(mentioned_projects[:3])

    def send_email(self, to_email: str, subject: str, body: str, 
                   resume_path: Optional[str] = None) -> bool:
        """Send email via Gmail SMTP"""
        try:
            server = self.connect_to_gmail()
            if not server:
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach resume if provided
            if resume_path and os.path.exists(resume_path):
                self.attach_file(msg, resume_path)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.gmail_user, to_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending email to {to_email}: {e}")
            return False

    def attach_file(self, msg: MIMEMultipart, file_path: str):
        """Attach file to email"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            filename = os.path.basename(file_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            
            msg.attach(part)
            
        except Exception as e:
            print(f"❌ Error attaching file: {e}")

    def send_bulk_emails(self, csv_file: str = "fintech_jobs.csv", 
                        resume_path: Optional[str] = None, 
                        delay_between_emails: int = 30) -> Dict:
        """Send bulk emails to all HR contacts"""
        
        print("🚀 Starting Email Automation System...")
        print(f"📧 Sending from: {self.gmail_user}")
        print(f"📋 Loading job data from: {csv_file}")
        
        # Load job data
        jobs = self.load_job_data(csv_file)
        
        if not jobs:
            print("❌ No jobs with HR emails found!")
            return {'sent': 0, 'failed': 0, 'total': 0}
        
        print(f"📊 Found {len(jobs)} jobs with HR contacts")
        print(f"⏱️  Delay between emails: {delay_between_emails} seconds")
        
        sent_count = 0
        failed_count = 0
        
        for i, job in enumerate(jobs, 1):
            print(f"\n📧 [{i}/{len(jobs)}] Processing: {job.get('company', 'Unknown')}")
            
            # Generate personalized email
            email_data = self.generate_personalized_email(job)
            
            print(f"   📬 To: {email_data['to_email']}")
            print(f"   📝 Subject: {email_data['subject']}")
            
            # Send email
            success = self.send_email(
                email_data['to_email'],
                email_data['subject'],
                email_data['body'],
                resume_path
            )
            
            if success:
                sent_count += 1
                self.sent_emails.append({
                    'company': job.get('company'),
                    'email': email_data['to_email'],
                    'subject': email_data['subject'],
                    'sent_at': datetime.now().isoformat()
                })
                print(f"   ✅ Email sent successfully!")
            else:
                failed_count += 1
                self.failed_emails.append({
                    'company': job.get('company'),
                    'email': email_data['to_email'],
                    'error': 'Failed to send',
                    'attempted_at': datetime.now().isoformat()
                })
                print(f"   ❌ Failed to send email")
            
            # Delay between emails (except for last email)
            if i < len(jobs):
                print(f"   ⏳ Waiting {delay_between_emails} seconds...")
                time.sleep(delay_between_emails)
        
        # Save email logs
        self.save_email_logs()
        
        print(f"\n🎉 Email Campaign Completed!")
        print(f"✅ Successfully sent: {sent_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📊 Total processed: {len(jobs)}")
        
        return {'sent': sent_count, 'failed': failed_count, 'total': len(jobs)}

    def save_email_logs(self):
        """Save email sending logs"""
        try:
            # Save sent emails log
            if self.sent_emails:
                sent_df = pd.DataFrame(self.sent_emails)
                sent_df.to_csv('sent_emails.csv', index=False)
                print(f"📄 Sent emails log saved to sent_emails.csv")
            
            # Save failed emails log
            if self.failed_emails:
                failed_df = pd.DataFrame(self.failed_emails)
                failed_df.to_csv('failed_emails.csv', index=False)
                print(f"📄 Failed emails log saved to failed_emails.csv")
                
        except Exception as e:
            print(f"❌ Error saving email logs: {e}")

    def apply_directly(self, job_data: Dict) -> bool:
        """Attempt to apply directly through company career portal"""
        try:
            apply_link = job_data.get('apply_link', '')
            if not apply_link or apply_link == 'Not specified':
                return False
            
            # This would require Selenium automation for direct applications
            # For now, we'll focus on email applications
            print(f"🔗 Direct application link: {apply_link}")
            print("📝 Note: Direct application automation requires additional setup")
            
            return False
            
        except Exception as e:
            print(f"❌ Error with direct application: {e}")
            return False

    def create_resume_template(self) -> str:
        """Create a basic resume template (placeholder)"""
        resume_content = f"""
{self.personal_info['name']}
{self.personal_info['phone']} | {self.gmail_user}
{self.personal_info['linkedin']} | {self.personal_info['github']} | {self.personal_info['portfolio']}

EDUCATION
{self.personal_info['education']} - {self.personal_info['college']}
Expected Graduation: {self.personal_info['graduation_year']}

SKILLS
{', '.join(self.personal_info['skills'])}

PROJECTS
[Add your projects here]

EXPERIENCE
[Add your experience here]

ACHIEVEMENTS
[Add your achievements here]
"""
        
        resume_path = "resume.txt"
        with open(resume_path, 'w') as f:
            f.write(resume_content)
        
        return resume_path

def main():
    """Main function to run email automation"""
    
    # Configuration
    GMAIL_USER = "your.email@gmail.com"  # Update with your Gmail
    APP_PASSWORD = "joew lgfh xoev jhpd"  # Your app password
    
    # Initialize email automation
    email_bot = JobEmailAutomation(GMAIL_USER, APP_PASSWORD)
    
    # Update personal information
    email_bot.update_personal_info(
        name="Your Name",
        phone="Your Phone Number",
        college="Your College Name",
        github="https://github.com/yourusername",
        linkedin="https://linkedin.com/in/yourprofile",
        portfolio="https://yourportfolio.com"
    )
    
    # Create resume template (optional)
    resume_path = email_bot.create_resume_template()
    print(f"📄 Resume template created: {resume_path}")
    print("⚠️  Please update the resume with your actual details before sending emails")
    
    # Send bulk emails
    result = email_bot.send_bulk_emails(
        csv_file="fintech_jobs.csv",
        resume_path=None,  # Set to resume_path if you want to attach resume
        delay_between_emails=30
    )
    
    print(f"\n📊 Final Results: {result}")

if __name__ == "__main__":
    main()
