"""Excel practice module — formula-writing tasks with data tables."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import re

@dataclass(frozen=True)
class Table:
    name: str
    columns: tuple[str, ...]
    rows: tuple[tuple[Any, ...], ...]

@dataclass(frozen=True)
class Task:
    id: str
    prompt: str
    kind: str  # "formula" | "quiz"
    difficulty: str = "medium"
    company: str = ""
    hint: str = ""
    starter: str = ""
    solution: str = ""
    expected: str = ""  # expected answer for formula tasks
    options: tuple[str, ...] = ()
    answer_index: int = 0
    explanation: str = ""
    tables: list[Table] = field(default_factory=list)  # task-specific tables override lesson tables

@dataclass(frozen=True)
class Lesson:
    id: str
    number: int
    title: str
    focus: list[str]
    tables: list[Table]
    tasks: list[Task]

# ── Shared data tables ──
PRODUCTS = Table("Products", ("ProductID","Name","Category","Price","Stock","Rating"), (
    (1,"Mechanical Keyboard","Electronics",89.99,34,4.7),
    (2,"USB-C Hub","Electronics",42.50,58,4.4),
    (3,"Noise Cancelling Headphones","Electronics",149.00,19,4.8),
    (4,"Standing Desk Mat","Office",36.00,41,4.2),
    (5,"Notebook Pack","Office",12.75,120,4.1),
    (6,"Desk Lamp","Office",36.00,64,4.3),
    (7,"Travel Mug","Kitchen",18.25,76,4.0),
    (8,"Pour Over Kit","Kitchen",31.80,22,4.6),
))

SALES = Table("Sales", ("OrderID","Date","Region","Product","Qty","Revenue","Channel"), (
    (101,"2024-01-05","North","Keyboard",2,179.98,"Web"),
    (102,"2024-01-09","South","USB-C Hub",3,127.50,"Store"),
    (103,"2024-01-11","North","Headphones",1,149.00,"Web"),
    (104,"2024-01-15","East","Desk Mat",4,144.00,"Web"),
    (105,"2024-02-10","West","Notebook",10,127.50,"Mobile"),
    (106,"2024-02-14","North","Desk Lamp",2,72.00,"Store"),
    (107,"2024-03-03","South","Travel Mug",5,91.25,"Web"),
    (108,"2024-03-09","East","Pour Over",3,95.40,"Mobile"),
    (109,"2024-03-15","North","Keyboard",1,89.99,"Web"),
    (110,"2024-04-01","West","Headphones",2,298.00,"Store"),
))

EMPLOYEES = Table("Employees", ("EmpID","Name","Department","Salary","JoinDate","Manager","Rating"), (
    (1,"Asha Rao","Analytics",85000,"2022-01-15","Priya",4.5),
    (2,"Noah Kim","Analytics",72000,"2023-02-20","Priya",3.8),
    (3,"Mia Chen","Marketing",68000,"2023-03-05","Raj",4.2),
    (4,"Luis Garcia","Engineering",95000,"2021-06-18","Raj",4.7),
    (5,"Emma Stone","Marketing",61000,"2023-04-22","Priya",3.5),
    (6,"Kabir Mehta","Analytics",78000,"2022-09-01","Priya",4.0),
    (7,"Zoe Miller","Engineering",88000,"2022-07-17","Raj",4.3),
    (8,"Ivy Tan","Marketing",65000,"2023-09-30","Raj",3.9),
))

LOOKUP_REF = Table("PriceList", ("SKU","ProductName","UnitPrice","Warehouse"), (
    ("SKU-101","Widget A",25.00,"Delhi"),
    ("SKU-102","Widget B",42.50,"Mumbai"),
    ("SKU-103","Gadget X",89.99,"Delhi"),
    ("SKU-104","Gadget Y",15.75,"Chennai"),
    ("SKU-105","Tool Z",63.00,"Mumbai"),
))

ORDERS_TBL = Table("Orders", ("OrderID","CustomerName","SKU","Qty","OrderDate","Status"), (
    (1001,"Asha","SKU-103",2,"2024-01-05","Delivered"),
    (1002,"Noah","SKU-101",5,"2024-01-09","Delivered"),
    (1003,"Mia","SKU-102",1,"2024-01-11","Cancelled"),
    (1004,"Luis","SKU-104",10,"2024-02-10","Delivered"),
    (1005,"Emma","SKU-105",3,"2024-02-14","Processing"),
    (1006,"Kabir","SKU-101",4,"2024-03-03","Delivered"),
    (1007,"Zoe","SKU-103",1,"2024-03-09","Delivered"),
    (1008,"Ivy","SKU-102",2,"2024-03-15","Cancelled"),
))

MONTHLY = Table("MonthlySales", ("Month","Region","Revenue","Orders","Returns"), (
    ("Jan","North",45000,120,8),("Jan","South",38000,95,12),("Jan","East",29000,78,5),("Jan","West",32000,88,7),
    ("Feb","North",48000,130,6),("Feb","South",41000,102,9),("Feb","East",31000,82,4),("Feb","West",35000,92,11),
    ("Mar","North",52000,145,10),("Mar","South",44000,110,7),("Mar","East",33000,89,6),("Mar","West",37000,98,8),
    ("Apr","North",47000,125,9),("Apr","South",39000,97,5),("Apr","East",30000,80,3),("Apr","West",34000,90,6),
))

# ── Lessons ──
LESSONS: list[Lesson] = [
    # ─── Chapter 1: VLOOKUP & XLOOKUP ───
    Lesson("vlookup-xlookup", 1, "VLOOKUP & XLOOKUP", ["VLOOKUP","XLOOKUP","exact match","error handling"], [LOOKUP_REF, ORDERS_TBL], [
        Task("v1","Write a VLOOKUP to find the UnitPrice of SKU-103 from the PriceList table.","formula","easy","Amazon",
             "Look up SKU-103 in column 1, return column 3, exact match.","","=VLOOKUP(\"SKU-103\",A:D,3,FALSE)","89.99"),
        Task("v2","Write a VLOOKUP to find which Warehouse stores SKU-101.","formula","easy","",
             "Warehouse is in column 4 of PriceList.","","=VLOOKUP(\"SKU-101\",A:D,4,FALSE)","Delhi"),
        Task("v3","Write an XLOOKUP to find the ProductName for SKU-104, returning 'Not Found' if missing.","formula","medium","Stripe",
             "XLOOKUP has a built-in if_not_found parameter.","","=XLOOKUP(\"SKU-104\",A:A,B:B,\"Not Found\")","Gadget Y"),
        Task("v4","A VLOOKUP returns #N/A. The lookup value has trailing spaces. Write the fix using TRIM.","formula","medium","Amazon",
             "Wrap the lookup value with TRIM to remove spaces.","","=VLOOKUP(TRIM(A2),PriceList,3,FALSE)","VLOOKUP(TRIM("),
        Task("v5","Write an XLOOKUP that searches the ProductName column and returns the SKU (reverse lookup).","formula","hard","Google",
             "XLOOKUP can search any column, not just the first.","","=XLOOKUP(\"Widget B\",B:B,A:A)","SKU-102"),
        Task("v6","Why can't VLOOKUP do a reverse lookup (search right, return left)?","quiz","easy","",
             hint="Think about which column VLOOKUP always searches.",
             options=("VLOOKUP is too slow","VLOOKUP always searches the leftmost column of the range","VLOOKUP only works with numbers","VLOOKUP requires sorted data"),
             answer_index=1,explanation="VLOOKUP always searches column 1 of the table_array and returns a column to its right. It cannot look left. Use INDEX-MATCH or XLOOKUP instead."),
        Task("v7","You need to look up a price but the SKU column is to the RIGHT of the price column. Which function(s) can handle this?","quiz","medium","PhonePe",
             options=("Only VLOOKUP","INDEX-MATCH or XLOOKUP","HLOOKUP","SUMIF"),
             answer_index=1,explanation="INDEX-MATCH and XLOOKUP can search and return from any columns regardless of position. VLOOKUP is limited to left-to-right."),
    ]),
    # ─── Chapter 2: INDEX MATCH ───
    Lesson("index-match", 2, "INDEX MATCH", ["INDEX","MATCH","two-way lookup","multi-criteria"], [LOOKUP_REF, ORDERS_TBL], [
        Task("im1","Write an INDEX-MATCH to find the UnitPrice for SKU-103.","formula","easy","Amazon",
             "MATCH finds the row, INDEX returns the value from that row.","","=INDEX(C:C,MATCH(\"SKU-103\",A:A,0))","89.99"),
        Task("im2","Write an INDEX-MATCH to find the Warehouse for the product named 'Tool Z'.","formula","medium","Stripe",
             "Search the ProductName column, return the Warehouse column.","","=INDEX(D:D,MATCH(\"Tool Z\",B:B,0))","Mumbai"),
        Task("im3","What does the third argument '0' in MATCH mean?","quiz","easy","",
             options=("Sort ascending","Approximate match","Exact match","Wildcard match"),
             answer_index=2,explanation="0 = exact match, 1 = less than (sorted asc), -1 = greater than (sorted desc)."),
        Task("im4","Write a formula to find how many units customer 'Noah' ordered (Qty from Orders table, using INDEX-MATCH).","formula","medium","Google",
             "Match 'Noah' in the CustomerName column, return Qty.","","=INDEX(D:D,MATCH(\"Noah\",B:B,0))","5"),
        Task("im5","Why is INDEX-MATCH preferred over VLOOKUP for large datasets?","quiz","medium","McKinsey",
             options=("It uses less memory","It can look up in any direction and handles column insertions gracefully","It automatically removes duplicates","It is a newer function"),
             answer_index=1,explanation="INDEX-MATCH uses separate ranges, so inserting/deleting columns doesn't break it. It can also look left, which VLOOKUP cannot."),
    ]),
    # ─── Chapter 3: Pivot Table Concepts ───
    Lesson("pivot-tables", 3, "Pivot Tables", ["aggregation","grouping","calculated fields","show values as"], [SALES], [
        Task("pv1","You have the Sales table. To see total Revenue by Region, where do you place the fields in a pivot table?","formula","easy","Amazon",
             "Think: which field is the grouping dimension, which is the measure?","","Region in Rows, Revenue in Values (Sum)","Region in Rows"),
        Task("pv2","Write the pivot table layout to see total Revenue by Region AND by Channel (cross-tab).","formula","medium","Stripe",
             "Two dimensions: one in Rows, one in Columns.","","Region in Rows, Channel in Columns, Sum of Revenue in Values","Region in Rows"),
        Task("pv3","The pivot shows Sum of Revenue. You want each region's percentage of grand total. What setting do you change?","quiz","medium","Amazon",
             options=("Change source data to percentages","Show Values As → % of Grand Total","Add a calculated field","Replace Sum with Count"),
             answer_index=1,explanation="'Show Values As' lets you display values as % of Grand Total, % of Row Total, Running Total, etc. without modifying source data."),
        Task("pv4","Your pivot table shows every individual date. You want monthly totals. How do you fix this?","quiz","easy","PhonePe",
             options=("Delete extra rows manually","Right-click the date field → Group → Month","Create a helper column","Use SUMIF"),
             answer_index=1,explanation="Right-click grouping on date fields lets you group by Month, Quarter, Year, etc. Much faster than helper columns."),
        Task("pv5","Write a Calculated Field formula for Profit if your pivot has Revenue and Cost fields.","formula","medium","McKinsey",
             "Calculated fields reference other pivot fields.","","= Revenue - Cost","Revenue - Cost"),
        Task("pv6","You want to see the top 5 products by revenue in your pivot table. How?","quiz","medium","Google",
             options=("Manually delete rows below 5","Value Filters → Top 10 → set to Top 5 by Sum of Revenue","Sort and hide rows","Use LARGE function"),
             answer_index=1,explanation="Value Filters → Top 10 (adjustable) lets you filter to Top/Bottom N items by any measure."),
    ]),
    # ─── Chapter 4: IF / COUNTIF / SUMIF ───
    Lesson("conditional-functions", 4, "IF, COUNTIF, SUMIF Family", ["IF","COUNTIF","SUMIF","AVERAGEIF","nested IF"], [EMPLOYEES, SALES], [
        Task("cf1","Write an IF formula: if an employee's Salary > 80000, return 'Senior', otherwise 'Junior'. (Salary is in column D)","formula","easy","Amazon",
             "Basic IF: =IF(condition, true_value, false_value)","","=IF(D2>80000,\"Senior\",\"Junior\")","IF(D2>80000"),
        Task("cf2","Write a nested IF: Rating >= 4.5 → 'Exceeds', >= 4.0 → 'Meets', else 'Below'. (Rating is column G)","formula","medium","Stripe",
             "Nested IFs cascade: IF(cond1, val1, IF(cond2, val2, val3))","","=IF(G2>=4.5,\"Exceeds\",IF(G2>=4,\"Meets\",\"Below\"))","IF(G2>=4.5"),
        Task("cf3","Write a COUNTIF to count how many employees are in the Analytics department.","formula","easy","",
             "COUNTIF(range, criteria)","","=COUNTIF(C:C,\"Analytics\")","3"),
        Task("cf4","Write a SUMIF to sum salaries of all employees in the Marketing department.","formula","medium","Amazon",
             "SUMIF(criteria_range, criteria, sum_range)","","=SUMIF(C:C,\"Marketing\",D:D)","194000"),
        Task("cf5","Write a COUNTIFS to count employees in Analytics with Rating > 4.0.","formula","medium","Google",
             "COUNTIFS handles multiple criteria (AND logic).","","=COUNTIFS(C:C,\"Analytics\",G:G,\">4\")","2"),
        Task("cf6","Write an AVERAGEIF to find the average salary of employees with Rating >= 4.0.","formula","medium","PhonePe",
             "AVERAGEIF(criteria_range, criteria, average_range)","","=AVERAGEIF(G:G,\">=4\",D:D)","average salary where rating >= 4"),
        Task("cf7","What is the difference between SUMIF and SUMIFS?","quiz","easy","",
             options=("No difference","SUMIF handles one criterion; SUMIFS handles multiple criteria","SUMIFS is slower","SUMIF only works with text"),
             answer_index=1,explanation="SUMIF takes one criteria pair. SUMIFS takes multiple pairs with AND logic. Note: in SUMIFS, the sum_range comes FIRST."),
    ]),
    # ─── Chapter 5: Data Cleaning ───
    Lesson("data-cleaning", 5, "Data Cleaning & TEXT Functions", ["TRIM","CLEAN","TEXT","SUBSTITUTE","duplicates"], [PRODUCTS], [
        Task("dc1","Cell A1 has '  Widget A  ' with extra spaces. Write a formula to clean it.","formula","easy","Amazon",
             "TRIM removes leading, trailing, and extra internal spaces.","","=TRIM(A1)","TRIM(A1)"),
        Task("dc2","Write a formula that removes both non-printable characters AND extra spaces from A1.","formula","medium","Stripe",
             "Combine CLEAN (non-printable) and TRIM (spaces).","","=TRIM(CLEAN(A1))","TRIM(CLEAN("),
        Task("dc3","Cell A1 contains the number 0.156. Write a TEXT formula to display it as '15.6%'.","formula","medium","McKinsey",
             "TEXT(value, format_code) — the % format multiplies by 100.","","=TEXT(A1,\"0.0%\")","15.6%"),
        Task("dc4","You have dates stored as text '15-Jan-2024'. Write a formula to convert to a proper Excel date.","formula","medium","PhonePe",
             "DATEVALUE converts text that looks like a date into a serial date number.","","=DATEVALUE(A1)","DATEVALUE("),
        Task("dc5","Write a SUBSTITUTE formula to replace all spaces in A1 with hyphens.","formula","easy","",
             "SUBSTITUTE(text, old, new)","","=SUBSTITUTE(A1,\" \",\"-\")","SUBSTITUTE(A1"),
        Task("dc6","What is the fastest built-in way to remove duplicate rows in Excel?","quiz","easy","Amazon",
             options=("Manually delete them","Data tab → Remove Duplicates","Use COUNTIF and filter","Sort and use IF to flag"),
             answer_index=1,explanation="Data → Remove Duplicates is the built-in one-click solution. It lets you choose which columns to check."),
    ]),
    # ─── Chapter 6: Date Functions ───
    Lesson("date-functions", 6, "Date Functions", ["EDATE","EOMONTH","NETWORKDAYS","DATEDIF","date math"], [EMPLOYEES], [
        Task("df1","Write a formula to get the date 3 months from the JoinDate in E2.","formula","easy","Amazon",
             "EDATE shifts a date by N months.","","=EDATE(E2,3)","EDATE(E2,3)"),
        Task("df2","Write a formula to find the last day of the month for the date in E2.","formula","medium","Stripe",
             "EOMONTH(start_date, months) — use 0 for current month's end.","","=EOMONTH(E2,0)","EOMONTH(E2,0)"),
        Task("df3","Write a formula to calculate working days between JoinDate (E2) and today, excluding weekends.","formula","medium","Google",
             "NETWORKDAYS counts business days between two dates.","","=NETWORKDAYS(E2,TODAY())","NETWORKDAYS("),
        Task("df4","Write a formula to find years of service: difference in years between JoinDate (E2) and today.","formula","medium","Amazon",
             "DATEDIF(start, end, unit) with 'Y' for complete years.","","=DATEDIF(E2,TODAY(),\"Y\")","DATEDIF("),
        Task("df5","Write a formula to extract just the month number from the date in E2.","formula","easy","",
             "MONTH() returns 1-12.","","=MONTH(E2)","MONTH(E2)"),
    ]),
    # ─── Chapter 7: Logical & Advanced ───
    Lesson("advanced-formulas", 7, "Advanced Formulas", ["AND","OR","IFERROR","SWITCH","array formulas"], [SALES, PRODUCTS], [
        Task("af1","Write a formula using AND: return 'High Value' if Revenue > 100 AND Qty > 2. (F=Revenue, E=Qty)","formula","medium","Amazon",
             "IF with AND: =IF(AND(cond1, cond2), true, false)","","=IF(AND(F2>100,E2>2),\"High Value\",\"Regular\")","AND(F2>100"),
        Task("af2","Wrap a VLOOKUP in IFERROR to return 'Missing' instead of #N/A.","formula","medium","Stripe",
             "IFERROR(formula, value_if_error)","","=IFERROR(VLOOKUP(A2,Products,3,FALSE),\"Missing\")","IFERROR(VLOOKUP("),
        Task("af3","Write a formula: if Channel is 'Web' return 10% discount, 'Store' return 5%, 'Mobile' return 15%, else 0.","formula","hard","Google",
             "SWITCH matches exact values: SWITCH(expression, val1, result1, ..., default)","","=SWITCH(G2,\"Web\",0.1,\"Store\",0.05,\"Mobile\",0.15,0)","SWITCH("),
        Task("af4","What does IFERROR do?","quiz","easy","",
             options=("Checks if a cell is empty","Returns an alternative value when a formula produces an error","Counts errors","Removes errors from data"),
             answer_index=1,explanation="IFERROR(value, value_if_error) traps any error (#N/A, #DIV/0!, #VALUE!, etc.) and returns the fallback value instead."),
        Task("af5","Write a formula using OR: flag as 'Review' if Rating < 4.0 OR Stock = 0.","formula","medium","McKinsey",
             "IF with OR: =IF(OR(cond1, cond2), true, false)","","=IF(OR(F2<4,E2=0),\"Review\",\"OK\")","OR("),
    ]),
    # ─── Chapter 8: Dashboard & Charts ───
    Lesson("dashboards-charts", 8, "Dashboards & Charts", ["chart selection","conditional formatting","sparklines","best practices"], [MONTHLY], [
        Task("dc8-1","You want to show how total revenue is split across 4 regions. Which chart type is best?","quiz","easy","Amazon",
             options=("Line chart","Scatter plot","Pie chart or Stacked bar","Waterfall chart"),
             answer_index=2,explanation="For part-to-whole with 4 categories, pie chart works well. Stacked bar is also excellent and more precise."),
        Task("dc8-2","You need to show monthly revenue trends over 4 months. Best chart type?","quiz","easy","",
             options=("Pie chart","Line chart","Treemap","Gauge"),
             answer_index=1,explanation="Line charts are the gold standard for time-series trends. They show direction, rate of change, and seasonality."),
        Task("dc8-3","Write a Conditional Formatting rule: highlight cells in Revenue column red if value < 35000.","formula","medium","Stripe",
             "In conditional formatting, you write the condition formula.","","=C2<35000","<35000"),
        Task("dc8-4","A chart shows y-axis starting at 90 instead of 0, making a 2% change look dramatic. What is this called?","quiz","medium","Google",
             options=("Normal scaling","Truncated y-axis — misleading visualization","Zoom feature","Logarithmic scale"),
             answer_index=1,explanation="Truncated y-axis exaggerates small changes. A 2% change (92→94) looks massive when y-axis shows 90-95 instead of 0-100."),
        Task("dc8-5","Write the formula to calculate Return Rate for each row (Returns / Orders × 100). Returns=col E, Orders=col D.","formula","medium","PhonePe",
             "Simple percentage calculation.","","=E2/D2*100","E2/D2"),
    ]),
    # ─── Chapter 9: Excel Shortcuts & Efficiency ───
    Lesson("shortcuts", 9, "Shortcuts & Productivity", ["keyboard shortcuts","efficiency","tips"], [PRODUCTS], [
        Task("sh1","What does Ctrl+Shift+L do in Excel?","quiz","easy","Amazon",
             options=("Locks cells","Toggles AutoFilter on/off","Opens Find & Replace","Inserts a chart"),
             answer_index=1,explanation="Ctrl+Shift+L toggles filter dropdowns on column headers. Essential for quick data exploration."),
        Task("sh2","What shortcut fills down (copies formula to cells below)?","quiz","easy","",
             options=("Ctrl+D","Ctrl+F","Ctrl+Shift+D","Alt+D"),
             answer_index=0,explanation="Ctrl+D fills down from the cell above. Select the range first, then Ctrl+D."),
        Task("sh3","You want to convert a formula to its computed value (paste as value). What shortcut?","quiz","medium","Stripe",
             options=("Ctrl+C then Ctrl+V","Ctrl+C then Ctrl+Shift+V","Ctrl+C then Alt+E,S,V,Enter","Both B and C work"),
             answer_index=3,explanation="Ctrl+Shift+V (newer Excel) or Alt+E,S,V,Enter (classic) both paste as values, removing formulas."),
        Task("sh4","F4 while editing a cell reference does what?","quiz","easy","Google",
             options=("Deletes the cell","Cycles through absolute/relative references ($A$1 → A$1 → $A1 → A1)","Repeats last action","Opens help"),
             answer_index=1,explanation="F4 cycles through reference types. Essential for locking rows/columns when copying formulas."),
        Task("sh5","What does Ctrl+` (backtick) do?","quiz","medium","",
             options=("Inserts a formula","Toggles formula view — shows all formulas instead of results","Opens VBA editor","Adds a comment"),
             answer_index=1,explanation="Ctrl+` toggles between showing formula results and the actual formulas in cells. Great for auditing."),
    ]),
    # ─── Chapter 10: FILTER, SORT, UNIQUE (Dynamic Arrays) ───
    Lesson("dynamic-arrays", 10, "Dynamic Arrays", ["FILTER","SORT","UNIQUE","SORTBY","spill ranges"], [SALES], [
        Task("da1","Write a FILTER formula to show only rows where Region = 'North'. (Data in A1:G10)","formula","medium","Amazon",
             "FILTER(array, include, [if_empty])","","=FILTER(A2:G10,C2:C10=\"North\")","FILTER("),
        Task("da2","Write a UNIQUE formula to get all unique regions from column C.","formula","easy","",
             "UNIQUE returns distinct values.","","=UNIQUE(C2:C10)","UNIQUE(C2"),
        Task("da3","Write a SORT formula to sort the Sales data by Revenue (column F) in descending order.","formula","medium","Stripe",
             "SORT(array, sort_index, sort_order) — -1 for descending.","","=SORT(A2:G10,6,-1)","SORT("),
        Task("da4","Write a FILTER with two conditions: Region = 'North' AND Revenue > 100.","formula","hard","Google",
             "Multiply conditions for AND logic: (cond1)*(cond2)","","=FILTER(A2:G10,(C2:C10=\"North\")*(F2:F10>100))","FILTER("),
        Task("da5","What is a 'spill range' in Excel?","quiz","easy","Amazon",
             options=("A range with errors","The range of cells that a dynamic array formula automatically fills with results","A named range","A print area"),
             answer_index=1,explanation="Dynamic array formulas (FILTER, SORT, UNIQUE) return multiple values that 'spill' into adjacent cells automatically."),
    ]),
]


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

LESSON_BY_ID = {l.id: l for l in LESSONS}

def _serialize_table(t: Table) -> dict:
    return {"name":t.name,"columns":list(t.columns),"rows":[list(r) for r in t.rows],"total":len(t.rows)}

def lesson_index() -> list[dict[str, Any]]:
    return [{"id":l.id,"number":l.number,"title":l.title,"focus":l.focus,"taskCount":len(l.tasks),"notesUrl":NOTES_BY_LESSON.get(l.id,"")} for l in LESSONS]

def lesson_payload(lesson_id: str) -> dict[str, Any]:
    l = LESSON_BY_ID.get(lesson_id, LESSONS[0])
    return {
        "id":l.id,"number":l.number,"title":l.title,"focus":l.focus,"notesUrl":NOTES_BY_LESSON.get(l.id,""),
        "tables":[_serialize_table(t) for t in l.tables],
        "tasks":[{
            "id":t.id,"prompt":t.prompt,"kind":t.kind,"difficulty":t.difficulty,
            "company":t.company,"hint":t.hint,"starter":t.starter,
            "options":list(t.options) if t.options else [],
            "tables":[_serialize_table(tb) for tb in t.tables] if t.tables else [],
        } for t in l.tasks],
    }

def check_answer(lesson_id: str, task_id: str, answer: int | str | None) -> dict:
    l = LESSON_BY_ID.get(lesson_id, LESSONS[0])
    t = next((t for t in l.tasks if t.id == task_id), l.tasks[0])
    if t.kind == "quiz":
        correct = answer == t.answer_index
        return {"correct":correct,"message":"Correct!" if correct else "Not quite.","explanation":t.explanation,"expectedIndex":t.answer_index,"solution":t.solution}
    # formula task — check if user's formula contains key parts of the expected answer
    # Normalize by removing spaces, $, and converting to upper
    def normalize(s):
        return str(s or "").strip().upper().replace(" ","").replace("$","")
    
    user = normalize(answer)
    expected_key = normalize(t.expected)
    solution_key = normalize(t.solution)
    
    # Check if the key functional part is present
    correct = expected_key in user or solution_key in user or user == expected_key or user == solution_key
    return {"correct":correct,
            "message":"Correct!" if correct else "Not quite — check the expected formula.",
            "explanation":t.explanation,"solution":t.solution,"expected":t.expected}
