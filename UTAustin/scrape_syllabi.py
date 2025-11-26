import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configuration
BASE_URL = "https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/"
OUTPUT_DIR = "syllabi"
YEARS = [2024, 2023, 2022, 2021]
SEMESTERS = {
    'Spring': '2',
    'Summer': '6',
    'Fall': '9'
}
DEPARTMENT = "GOV"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def scrape():
    ensure_dir(OUTPUT_DIR)
    
    for year in YEARS:
        for sem_name, sem_code in SEMESTERS.items():
            print(f"Scraping {sem_name} {year}...")
            
            params = {
                'year': str(year),
                'semester': sem_code,
                'department': DEPARTMENT,
                'course_number': '',
                'course_title': '',
                'unique': '',
                'instructor_first': '',
                'instructor_last': '',
                'course_type': ['In Residence', 'Extension'],
                'search': 'Search'
            }
            
            try:
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find the results table
                # The table doesn't have a unique ID for results, but it's inside a div with id="classlist" usually?
                # In the debug HTML: <div id="classlist"> ... <table border="1">
                
                classlist = soup.find('div', id='classlist')
                if not classlist:
                    print(f"No results found for {sem_name} {year}")
                    continue
                    
                table = classlist.find('table')
                if not table:
                    continue
                    
                rows = table.find_all('tr')
                count = 0
                
                # Skip header row
                for row in rows[1:]:
                    cols = row.find_all('td')
                    if len(cols) < 8:
                        continue
                        
                    # Extract info for filename
                    # 0: Type, 1: Sem, 2: Dept, 3: Number, 4: Title, 5: Unique, 6: Instr, 7: Syllabus
                    try:
                        dept = cols[2].get_text(strip=True)
                        course_num = cols[3].get_text(strip=True)
                        unique = cols[5].get_text(strip=True)
                        
                        syllabus_col = cols[7]
                        link = syllabus_col.find('a', href=True)
                        
                        if link:
                            href = link['href']
                            if "/download/" in href:
                                full_url = urljoin(BASE_URL, href)
                                
                                # Create directory
                                sem_dir = os.path.join(OUTPUT_DIR, str(year), sem_name)
                                ensure_dir(sem_dir)
                                
                                # Filename: Year_Sem_Dept_Number_Unique.pdf
                                filename = f"{year}_{sem_name}_{dept}_{course_num}_{unique}.pdf"
                                # Sanitize filename
                                filename = "".join([c for c in filename if c.isalnum() or c in ('_', '.', '-')])
                                
                                save_path = os.path.join(sem_dir, filename)
                                
                                if not os.path.exists(save_path):
                                    download_file(full_url, save_path)
                                    count += 1
                                    time.sleep(0.2) # Be nice
                    except Exception as e:
                        print(f"Error parsing row: {e}")
                        continue
                
                print(f"Found {count} documents for {sem_name} {year}")
                
            except Exception as e:
                print(f"Failed to scrape {sem_name} {year}: {e}")
            
            time.sleep(1)

if __name__ == "__main__":
    scrape()
