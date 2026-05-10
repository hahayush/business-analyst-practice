import os
import re

FILES = [
    "app/powerbi_practice.py",
    "app/tableau_practice.py",
    "app/case_study_practice.py",
    "app/leadership_practice.py",
    "app/data_interp_practice.py",
    "app/aptitude_practice.py",
    "app/excel_practice.py",
]

NOTES = {
    "app/powerbi_practice.py": """
NOTES_BY_LESSON = {
    "modeling": "https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand",
    "power-query": "https://learn.microsoft.com/en-us/power-query/power-query-what-is-power-query",
    "dax-essentials": "https://learn.microsoft.com/en-us/dax/dax-overview",
    "calculate": "https://learn.microsoft.com/en-us/dax/calculate-function-dax",
    "time-intelligence": "https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax",
    "dax-optimization": "https://learn.microsoft.com/en-us/power-bi/guidance/dax-variables",
    "advanced-filtering": "https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls",
    "viz-best-practices": "https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-bookmarks"
}
""",
    "app/tableau_practice.py": """
NOTES_BY_LESSON = {
    "tableau-logic": "https://help.tableau.com/current/pro/desktop/en-us/functions_functions_logical.htm",
    "tableau-lod": "https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod_overview.htm",
    "tableau-table-calcs": "https://help.tableau.com/current/pro/desktop/en-us/calculations_tablecalculations.htm",
    "tableau-parameters": "https://help.tableau.com/current/pro/desktop/en-us/parameters_create.htm",
    "tableau-sets": "https://help.tableau.com/current/pro/desktop/en-us/sortgroup_sets_create.htm",
    "tableau-data-modeling": "https://help.tableau.com/current/pro/desktop/en-us/datasource_datamodel.htm",
    "tableau-ooo": "https://help.tableau.com/current/pro/desktop/en-us/order_of_operations.htm",
    "tableau-dashboards": "https://help.tableau.com/current/pro/desktop/en-us/dashboards.htm"
}
""",
    "app/case_study_practice.py": """
NOTES_BY_LESSON = {
    "rca-metrics": "https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/the-granularity-of-growth",
    "guesstimates": "https://igotanoffer.com/blogs/mckinsey-case-interview-blog/market-sizing-questions",
    "product-metrics": "https://a16z.com/2015/08/21/16-metrics/",
    "ab-testing": "https://hbr.org/2017/09/a-refresher-on-ab-testing",
    "market-entry": "https://www.investopedia.com/terms/p/porter.asp",
    "operations": "https://www.investopedia.com/terms/b/bottleneck.asp",
    "finance-cases": "https://www.investopedia.com/terms/e/ebitda.asp",
    "ethics": "https://gdpr.eu/what-is-gdpr/",
    "ma-synergy": "https://www.investopedia.com/terms/s/synergy.asp",
    "gtm-strategy": "https://hbr.org/2021/04/the-right-way-to-build-your-go-to-market-strategy",
    "war-gaming": "https://hbr.org/2004/10/blue-ocean-strategy",
    "vendor-negotiation": "https://www.pon.harvard.edu/daily/batna/translate-your-batna-to-the-current-deal/"
}
""",
    "app/leadership_practice.py": """
NOTES_BY_LESSON = {
    "customer-obsession": "https://www.aboutamazon.com/about-us/leadership-principles",
    "ownership": "https://www.aboutamazon.com/about-us/leadership-principles",
    "invent-simplify": "https://www.aboutamazon.com/about-us/leadership-principles",
    "right-a-lot": "https://www.aboutamazon.com/about-us/leadership-principles",
    "learn-curious": "https://www.aboutamazon.com/about-us/leadership-principles",
    "hire-develop": "https://www.aboutamazon.com/about-us/leadership-principles",
    "highest-standards": "https://www.aboutamazon.com/about-us/leadership-principles",
    "think-big": "https://www.aboutamazon.com/about-us/leadership-principles",
    "bias-for-action": "https://www.aboutamazon.com/about-us/leadership-principles",
    "frugality": "https://www.aboutamazon.com/about-us/leadership-principles",
    "earn-trust": "https://www.aboutamazon.com/about-us/leadership-principles",
    "dive-deep": "https://www.aboutamazon.com/about-us/leadership-principles",
    "disagree-commit": "https://www.aboutamazon.com/about-us/leadership-principles",
    "deliver-results": "https://www.aboutamazon.com/about-us/leadership-principles",
    "best-employer": "https://www.aboutamazon.com/about-us/leadership-principles",
    "success-scale": "https://www.aboutamazon.com/about-us/leadership-principles"
}
""",
    "app/data_interp_practice.py": """
NOTES_BY_LESSON = {
    "marketing-roi": "https://www.investopedia.com/terms/r/returnoninvestment.asp",
    "cohort-analysis": "https://clevertap.com/blog/cohort-analysis/",
    "ops-bottlenecks": "https://www.investopedia.com/terms/b/bottleneck.asp",
    "financial-pl": "https://www.investopedia.com/terms/p/plstatement.asp",
    "price-elasticity": "https://www.investopedia.com/terms/p/priceelasticity.asp",
    "simpsons-paradox": "https://plato.stanford.edu/entries/paradox-simpson/",
    "regressions": "https://hbr.org/2015/11/a-refresher-on-regression-analysis",
    "funnel-math": "https://mixpanel.com/blog/funnel-analysis/",
    "supply-chain": "https://www.investopedia.com/terms/e/economicorderquantity.asp",
    "mrr-waterfall": "https://baremetrics.com/academy/mrr-waterfall"
}
""",
    "app/aptitude_practice.py": """
NOTES_BY_LESSON = {
    "mental-math": "https://www.mathsisfun.com/numbers/percentage.html",
    "gmat-data-sufficiency": "https://www.mba.com/exams/gmat-exam/about/verbal/data-sufficiency",
    "bayes-theorem": "https://plato.stanford.edu/entries/bayes-theorem/",
    "saas-unit-economics": "https://a16z.com/2015/08/21/16-metrics/",
    "market-sizing-fermi": "https://en.wikipedia.org/wiki/Fermi_problem",
    "cagr-roi": "https://www.investopedia.com/terms/c/cagr.asp",
    "algorithm-scaling": "https://www.bigocheatsheet.com/",
    "game-theory": "https://plato.stanford.edu/entries/game-theory/"
}
""",
    "app/excel_practice.py": """
NOTES_BY_LESSON = {
    "excel-basics": "https://support.microsoft.com/en-us/excel",
    "vlookup": "https://support.microsoft.com/en-us/office/vlookup-function-0bbc8083-26fe-4963-8ab8-93a18ad188a1",
    "xlookup": "https://support.microsoft.com/en-us/office/xlookup-function-b7fd680e-6d10-43e6-84f9-88eae8bf5929",
    "index-match": "https://support.microsoft.com/en-us/office/index-function-a5dcf0dd-996d-40a4-a822-b56b061328bd",
    "if-statements": "https://support.microsoft.com/en-us/office/if-function-69aed7c9-4e8a-4755-a9bc-aa8bbff73be2",
    "nested-if": "https://support.microsoft.com/en-us/office/ifs-function-36329a26-37b2-467c-972b-4a39bd951d45",
    "countifs": "https://support.microsoft.com/en-us/office/countifs-function-dda3dc6e-f74e-4aee-88bc-aa8c2a866842",
    "sumifs": "https://support.microsoft.com/en-us/office/sumifs-function-c9e747f5-79d1-4ad9-a78c-06be5d496e57",
    "date-functions": "https://support.microsoft.com/en-us/office/date-function-e36c0c8c-4104-49da-ab83-82328b832349",
    "financial-functions": "https://support.microsoft.com/en-us/office/npv-function-8672cb67-2576-4d07-b67b-ac28acf2a568"
}
"""
}

def update_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Step 1: Insert NOTES_BY_LESSON before LESSON_BY_ID
    if "NOTES_BY_LESSON" not in content:
        content = content.replace("LESSON_BY_ID = ", NOTES[filename] + "\nLESSON_BY_ID = ")

    # Step 2: Update lesson_index
    old_index = 'return [{"id":l.id,"number":l.number,"title":l.title,"focus":l.focus,"taskCount":len(l.tasks)} for l in LESSONS]'
    new_index = 'return [{"id":l.id,"number":l.number,"title":l.title,"focus":l.focus,"taskCount":len(l.tasks),"notesUrl":NOTES_BY_LESSON.get(l.id,"")} for l in LESSONS]'
    content = content.replace(old_index, new_index)

    # Step 3: Update lesson_payload
    old_payload = '        "id":l.id,"number":l.number,"title":l.title,"focus":l.focus,'
    new_payload = '        "id":l.id,"number":l.number,"title":l.title,"focus":l.focus,"notesUrl":NOTES_BY_LESSON.get(l.id,""),'
    content = content.replace(old_payload, new_payload)

    with open(filename, 'w') as f:
        f.write(content)

for f in FILES:
    update_file(f)
    print(f"Updated {f}")

