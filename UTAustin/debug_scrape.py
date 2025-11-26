import requests

url = "https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/"
params = {
    'year': '2023',
    'semester': '9',
    'department': 'GOV',
    'course_number': '',
    'course_title': '',
    'unique': '',
    'instructor_first': '',
    'instructor_last': '',
    'course_type': ['In Residence', 'Extension'],
    'search': 'Search'
}

response = requests.get(url, params=params)
print(f"Status: {response.status_code}")
with open("debug_results.html", "w") as f:
    f.write(response.text)
