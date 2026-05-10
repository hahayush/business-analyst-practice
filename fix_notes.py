import re

def fix_file(filename, new_notes):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Replace the old NOTES_BY_LESSON block with the new one
    # using regex to match from NOTES_BY_LESSON = { ... }
    pattern = r"NOTES_BY_LESSON = \{[^\}]+\}"
    content = re.sub(pattern, new_notes, content)
    
    with open(filename, 'w') as f:
        f.write(content)

excel_notes = """NOTES_BY_LESSON = {
    "vlookup-xlookup": "https://support.microsoft.com/en-us/office/xlookup-function-b7fd680e-6d10-43e6-84f9-88eae8bf5929",
    "index-match": "https://support.microsoft.com/en-us/office/index-function-a5dcf0dd-996d-40a4-a822-b56b061328bd",
    "pivot-tables": "https://support.microsoft.com/en-us/office/create-a-pivottable-to-analyze-worksheet-data-a9a84538-bfe9-40a9-a8e9-f99134456576",
    "conditional-functions": "https://support.microsoft.com/en-us/office/countifs-function-dda3dc6e-f74e-4aee-88bc-aa8c2a866842",
    "data-cleaning": "https://support.microsoft.com/en-us/office/trim-function-410388fa-c5df-49c6-b16c-9e5630b479f9",
    "date-functions": "https://support.microsoft.com/en-us/office/date-function-e36c0c8c-4104-49da-ab83-82328b832349",
    "advanced-formulas": "https://support.microsoft.com/en-us/office/iferror-function-c526fd07-caeb-47b8-8bb6-63f3e417f611",
    "dashboards-charts": "https://support.microsoft.com/en-us/office/available-chart-types-in-office-a6187218-807e-4103-9e0a-27cdb19afb90",
    "shortcuts": "https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-excel-1798d9d5-842a-42b8-9c99-9b7213f0040f",
    "dynamic-arrays": "https://support.microsoft.com/en-us/office/filter-function-f4f7cb66-82eb-4767-8f7c-4877ad80c759"
}"""

aptitude_notes = """NOTES_BY_LESSON = {
    "quant-expected-value": "https://plato.stanford.edu/entries/bayes-theorem/",
    "quant-unit-econ": "https://a16z.com/2015/08/21/16-metrics/",
    "quant-finance": "https://www.investopedia.com/terms/c/cagr.asp",
    "quant-algorithms": "https://www.bigocheatsheet.com/",
    "quant-fermi": "https://en.wikipedia.org/wiki/Fermi_problem",
    "quant-data-suff": "https://www.mba.com/exams/gmat-exam/about/verbal/data-sufficiency",
    "quant-stats": "https://www.investopedia.com/terms/s/sharperatio.asp",
    "quant-game-theory": "https://plato.stanford.edu/entries/game-theory/"
}"""

fix_file("app/excel_practice.py", excel_notes)
fix_file("app/aptitude_practice.py", aptitude_notes)

print("Fixed notes keys.")
