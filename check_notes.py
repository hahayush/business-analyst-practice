import re
import os

files = [
    "app/powerbi_practice.py",
    "app/tableau_practice.py",
    "app/case_study_practice.py",
    "app/leadership_practice.py",
    "app/data_interp_practice.py",
    "app/aptitude_practice.py",
    "app/excel_practice.py",
]

all_match = True
for f in files:
    with open(f, 'r') as file:
        content = file.read()
        
    lessons = re.findall(r'Lesson\("([^"]+)"', content)
    
    notes_match = re.search(r'NOTES_BY_LESSON\s*=\s*\{([^\}]+)\}', content)
    notes_keys = []
    if notes_match:
        notes_str = notes_match.group(1)
        notes_keys = re.findall(r'"([^"]+)"\s*:', notes_str)
        
    lessons_set = set(lessons)
    notes_set = set(notes_keys)
    
    missing = lessons_set - notes_set
    extra = notes_set - lessons_set
    
    print(f"{f}: {len(lessons)} Lessons, {len(notes_keys)} Notes")
    if missing or extra:
        all_match = False
        print(f"  Missing: {missing}")
        print(f"  Extra: {extra}")

if all_match:
    print("SUCCESS: All chapters have notes!")
