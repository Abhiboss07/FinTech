"""
Configuration file for Fintech Job Scraper
"""

# User agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# Request delays (in seconds)
MIN_DELAY = 2
MAX_DELAY = 8

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5

# Output files
CSV_FILENAME = "fintech_jobs.csv"
EXCEL_FILENAME = "fintech_jobs.xlsx"
JSON_FILENAME = "fintech_jobs.json"

# Scraping limits
MAX_COMPANIES_TO_SCRAPE = 50
MAX_JOBS_PER_SOURCE = 100

# Data validation
MIN_TITLE_LENGTH = 5
MAX_TITLE_LENGTH = 200
MIN_DESCRIPTION_LENGTH = 50

# Keywords for filtering
FRESHER_KEYWORDS = [
    'fresher', 'entry level', 'graduate', 'trainee', 'intern', 'PPO',
    'pre placement offer', 'campus placement', 'recent graduate',
    '0-0 years', '0 years', 'no experience', 'junior developer',
    'entry-level', 'entry level', 'graduate trainee', 'recent grad'
]

ROLE_KEYWORDS = [
    'SDE', 'Software Developer', 'Backend Developer', 'Backend Engineer',
    'Software Engineer', 'Full Stack Developer', 'Python Developer',
    'Java Developer', 'Node.js Developer', 'API Developer',
    'Database Developer', 'DevOps Engineer', 'Cloud Engineer',
    'Software Development Engineer', 'Backend Software Engineer',
    'Application Developer', 'Systems Developer', 'Platform Engineer'
]

FINTECH_KEYWORDS = [
    'fintech', 'finance', 'banking', 'payment', 'wallet', 'upi', 'neft',
    'rtgs', 'imps', 'digital payment', 'online payment', 'mobile payment',
    'credit', 'debit', 'loan', 'insurance', 'investment', 'trading',
    'stock', 'mutual fund', 'cryptocurrency', 'bitcoin', 'blockchain',
    'wealth management', 'financial services', 'bank', 'nbfc',
    'financial technology', 'digital banking', 'online banking',
    'peer to peer lending', 'p2p lending', 'digital lending',
    'wealth tech', 'insurtech', 'regtech', 'paytech'
]

# Blacklisted companies/keywords to exclude
BLACKLIST_KEYWORDS = [
    'sales', 'marketing', 'business development', 'relationship manager',
    'insurance agent', 'loan officer', 'collection', 'recovery',
    'telecaller', 'customer support', 'operations', 'non technical'
]
