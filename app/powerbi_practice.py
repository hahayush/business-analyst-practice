"""Senior-Level Power BI practice module — Modeling, DAX, and Power Query."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

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
    expected: str = ""
    options: tuple[str, ...] = ()
    answer_index: int = 0
    explanation: str = ""
    tables: list[Table] = field(default_factory=list)

@dataclass(frozen=True)
class Lesson:
    id: str
    number: int
    title: str
    focus: list[str]
    tables: list[Table]
    tasks: list[Task]

# ── Data Tables ──
SALES_FACT = Table("FactSales", ("OrderID", "Date", "ProductID", "CustomerID", "Qty", "Revenue"), (
    (101, "2024-01-01", 1, 501, 2, 200),
    (102, "2024-01-15", 2, 502, 1, 50),
    (103, "2023-12-01", 1, 501, 4, 400),
    (104, "2023-11-20", 3, 503, 2, 300),
))

PRODUCT_DIM = Table("DimProduct", ("ProductID", "Name", "Category", "SubCategory", "Cost"), (
    (1, "Widget X", "Electronics", "Parts", 60),
    (2, "Gadget Y", "Office", "Paper", 20),
    (3, "Tool Z", "Hardware", "HandTools", 90),
))

DATE_DIM = Table("DimDate", ("Date", "Year", "Month", "Quarter", "IsWeekend"), (
    ("2024-01-01", 2024, "Jan", 1, 0),
    ("2024-01-15", 2024, "Jan", 1, 0),
    ("2023-12-01", 2023, "Dec", 4, 0),
))

# ── Lessons ──
LESSONS: list[Lesson] = [
    # ─── Chapter 1: Data Modeling (Star Schema) ───
    Lesson("modeling", 1, "Data Modeling & Star Schema", ["Relationships", "Cardinality", "Direction"], [SALES_FACT, PRODUCT_DIM, DATE_DIM], [
        Task("pbi1-1", "In a standard Star Schema, what is the recommended relationship cardinality between DimProduct and FactSales?", "quiz", "easy", "Amazon", options=("One-to-One", "Many-to-Many", "One-to-Many (1:*)", "Many-to-One (*:1)"), answer_index=2, explanation="Dimensions (1) filter Facts (*). A 1:* relationship from Dim to Fact is the backbone of Power BI modeling."),
        Task("pbi1-2", "Why is 'Bi-directional' cross-filtering generally discouraged in complex models?", "quiz", "medium", "Stripe", options=("It makes the file larger", "It can cause ambiguity and performance degradation in large models", "It only works with SQL sources", "It disables DAX"), answer_index=1, explanation="Bi-directional filters can create circular paths and performance issues. Use single-direction filters unless specific many-to-many scenarios require otherwise."),
        Task("pbi1-3", "You have two fact tables (Sales and Budget) at different granularities. What is the best way to model this?", "quiz", "hard", "Google", options=("Create a direct Many-to-Many relationship", "Use a shared Dimension table (e.g., DimDate) to filter both", "Merge them into one table in Power Query", "Bi-directional filter between facts"), answer_index=1, explanation="Shared dimensions (Conformed Dimensions) are the correct way to bridge multiple fact tables at different granularities."),
        Task("pbi1-4", "What happens if you have an active relationship between DimDate and FactSales on 'OrderDate', but you also need a relationship on 'ShipDate'?", "quiz", "medium", "Microsoft", options=("Create a second active relationship", "Create an inactive relationship and use USERELATIONSHIP in DAX", "Merge the dates in Power Query", "Delete the DimDate table"), answer_index=1, explanation="Power BI only allows one active relationship between two tables. Additional relationships must be inactive and activated inside DAX measures via USERELATIONSHIP."),
        Task("pbi1-5", "Which of the following describes a 'Snowflake' schema?", "quiz", "medium", "", options=("Fact tables connected directly to other Fact tables", "Dimension tables connected to other Dimension tables (normalized)", "A single large flat table", "Tables without any relationships"), answer_index=1, explanation="Snowflaking normalizes dimensions into sub-dimensions (e.g., DimProduct -> DimCategory). It saves space but makes queries more complex."),
        Task("pbi1-6", "What is the primary risk of using a Many-to-Many relationship (*:*)?", "quiz", "hard", "JPMorgan", options=("It crashes Power BI", "Values might be double-counted if not properly handled with bridge tables", "It forces direct query mode", "It deletes duplicate rows"), answer_index=1, explanation="Many-to-many relationships can lead to double-counting because a single row in one table might match multiple rows in the other, duplicating aggregated results."),
        Task("pbi1-7", "When should you use a Bridge Table in Power BI?", "quiz", "hard", "McKinsey", options=("To connect two Fact tables directly", "To resolve a Many-to-Many relationship between a Fact and a Dimension", "To change colors on a dashboard", "To connect to an Excel file"), answer_index=1, explanation="Bridge tables (often containing unique IDs) sit between a Fact and a Dimension in a Many-to-Many scenario to allow filters to pass through safely."),
    ]),
    
    # ─── Chapter 2: Power Query & M ───
    Lesson("power-query", 2, "Power Query (ETL) & M", ["Unpivot", "Merge vs Append", "Conditional Columns"], [SALES_FACT], [
        Task("pbi2-1", "You have columns 'Jan_Sales', 'Feb_Sales', 'Mar_Sales'. Which Power Query transformation converts these into 'Month' and 'Sales' columns?", "quiz", "easy", "Amazon", options=("Transpose", "Pivot Column", "Unpivot Columns", "Group By"), answer_index=2, explanation="Unpivot takes wide data and makes it long/thin, which is ideal for tabular modeling."),
        Task("pbi2-2", "What is the difference between 'Merge' and 'Append' in Power Query?", "quiz", "easy", "", options=("Merge adds rows; Append adds columns", "Merge adds columns (Join); Append adds rows (Union)", "Merge is for Excel; Append is for SQL", "No difference"), answer_index=1, explanation="Merge is a horizontal operation (Join), Append is a vertical operation (Union)."),
        Task("pbi2-3", "Write an M-code snippet for a Conditional Column: If [Qty] > 10 then 'High' else 'Low'.", "formula", "medium", "", "Syntax: if [Col] > X then 'A' else 'B'", "", "if [Qty] > 10 then \"High\" else \"Low\"", "if [Qty] > 10"),
        Task("pbi2-4", "Query Folding refers to:", "quiz", "hard", "Microsoft", options=("Folding columns to save space", "Pushing transformations back to the source database (like SQL Server) rather than processing them locally", "Hiding query steps in the UI", "Combining two queries into one"), answer_index=1, explanation="Query folding translates M code into native SQL. This drastically improves refresh performance by letting the database do the heavy lifting."),
        Task("pbi2-5", "Which transformation will immediately break Query Folding in most SQL databases?", "quiz", "hard", "Capital One", options=("Filtering Rows", "Removing Columns", "Adding a Native SQL query or custom M function like Table.Buffer", "Changing Data Types"), answer_index=2, explanation="Adding custom M logic, buffering, or writing native SQL blocks the engine from folding subsequent steps."),
        Task("pbi2-6", "How do you handle a scenario where a folder contains 12 monthly CSV files and you need them in one table?", "quiz", "medium", "", options=("Merge Queries", "Use the 'Get Data from Folder' connector and Combine Files", "Manually copy-paste them in Excel first", "Append them 11 times manually"), answer_index=1, explanation="'From Folder' automatically sets up a helper function to iterate through the folder and append the files dynamically."),
        Task("pbi2-7", "What does the M function `Table.Buffer` do?", "quiz", "hard", "", options=("Deletes the table", "Loads the table into memory to prevent it from being re-evaluated during downstream complex merges", "Sorts the table alphabetically", "Writes the table back to SQL"), answer_index=1, explanation="Table.Buffer forces Power Query to load the data into RAM, stopping query folding but potentially speeding up complex self-joins or multiple downstream references."),
    ]),

    # ─── Chapter 3: Essential DAX ───
    Lesson("dax-essentials", 3, "Essential DAX (Measures vs Columns)", ["Row Context", "Filter Context", "SUMX"], [SALES_FACT, PRODUCT_DIM], [
        Task("pbi3-1", "Write a DAX measure for Total Revenue.", "formula", "easy", "", "SUM(Table[Column])", "Total Revenue = ", "SUM(FactSales[Revenue])", "SUM(FactSales[Revenue])"),
        Task("pbi3-2", "Write an Iterator measure (SUMX) to calculate Total Cost (Qty * Cost from DimProduct).", "formula", "hard", "Stripe", "SUMX(Table, Expression * RELATED(DimTable[Col]))", "Total Cost = ", "SUMX(FactSales, FactSales[Qty] * RELATED(DimProduct[Cost]))", "SUMX("),
        Task("pbi3-3", "When should you use a Calculated Column instead of a Measure?", "quiz", "medium", "Amazon", options=("Always", "For aggregations like Sum/Avg", "When you need the value as a Slicer or Row/Column grouping", "Never"), answer_index=2, explanation="Calculated columns are computed at refresh and stored in memory. They are required if you want to slice or group by the result. Measures are calculated at query time."),
        Task("pbi3-4", "What is the primary difference between SUM and SUMX?", "quiz", "medium", "Google", options=("SUMX is faster", "SUMX iterates row-by-row allowing for row-level expressions, SUM only aggregates a single column", "SUM only works on integers", "No difference"), answer_index=1, explanation="SUM is syntax sugar for SUMX(Table, Table[Column]). SUMX allows for complex row-by-row math like SUMX(Sales, Sales[Qty] * Sales[Price])."),
        Task("pbi3-5", "What DAX function do you use to pull a value from the '1' side of a 1:* relationship into the '*' side?", "quiz", "easy", "", options=("RELATED", "RELATEDTABLE", "LOOKUPVALUE", "CALCULATE"), answer_index=0, explanation="RELATED follows the relationship from the Many side to the One side. RELATEDTABLE goes the other way."),
        Task("pbi3-6", "Write a DAX expression to count the distinct number of CustomerIDs in FactSales.", "formula", "easy", "", "DISTINCTCOUNT(Table[Column])", "Unique Customers = ", "DISTINCTCOUNT(FactSales[CustomerID])", "DISTINCTCOUNT("),
        Task("pbi3-7", "Why might DISTINCTCOUNT be slow on a very large table, and what is a faster alternative if you only need an approximation?", "quiz", "hard", "", options=("APPROXIMATEDISTINCTCOUNT", "COUNTROWS", "CALCULATE", "SUMX"), answer_index=0, explanation="APPROXIMATEDISTINCTCOUNT uses a HyperLogLog algorithm. It's much faster for massive datasets but has a slight margin of error (usually ~2%)."),
    ]),

    # ─── Chapter 4: The CALCULATE Function ───
    Lesson("calculate", 4, "The Power of CALCULATE", ["Filter context", "ALL", "KEEPFILTERS"], [SALES_FACT, PRODUCT_DIM], [
        Task("pbi4-1", "Write a measure for 'Electronics Sales' using CALCULATE.", "formula", "medium", "Amazon", "CALCULATE(TotalMeasure, FilterExpression)", "Electronics Sales = ", "CALCULATE([Total Revenue], DimProduct[Category] = \"Electronics\")", "CALCULATE("),
        Task("pbi4-2", "Write a measure that ignores all filters on the Product table to show 'Grand Total' sales.", "formula", "hard", "Google", "Use the ALL function inside CALCULATE.", "All Product Sales = ", "CALCULATE([Total Revenue], ALL(DimProduct))", "ALL(DimProduct)"),
        Task("pbi4-3", "What does the function REMOVEFILTERS do?", "quiz", "medium", "", options=("Deletes data", "Alias for ALL() when used as a filter argument in CALCULATE", "Clears the slicer UI", "Stops the report from loading"), answer_index=1, explanation="REMOVEFILTERS is identical to ALL when used inside CALCULATE, but reads more intuitively as 'remove these filters'."),
        Task("pbi4-4", "What is Context Transition?", "quiz", "hard", "Microsoft", options=("Changing from DirectQuery to Import", "When CALCULATE transforms a Row Context into a Filter Context", "Moving a visual from one page to another", "Changing data types"), answer_index=1, explanation="Context transition happens when you use CALCULATE (or a measure reference) inside an iterator like SUMX. It turns the current row into a filter."),
        Task("pbi4-5", "By default, a filter argument in CALCULATE will overwrite existing filters on that column. How do you ADD to the filter instead of overwriting?", "quiz", "hard", "Stripe", options=("Use ALL", "Use KEEPFILTERS() around the filter argument", "Use FILTER()", "It's not possible"), answer_index=1, explanation="KEEPFILTERS modifies CALCULATE so that the new filter intersects (AND logic) with the existing filter, rather than replacing it."),
        Task("pbi4-6", "Write a measure using CALCULATE to compute Sales but ONLY for the year 2024 (hardcoded).", "formula", "medium", "", "CALCULATE([Measure], YearCol = 2024)", "2024 Sales = ", "CALCULATE([Total Revenue], DimDate[Year] = 2024)", "CALCULATE("),
        Task("pbi4-7", "What does ALLEXCEPT do?", "quiz", "medium", "", options=("Removes all columns", "Removes all filters on a table EXCEPT for the columns specified", "Throws an error", "Filters out blank rows"), answer_index=1, explanation="ALLEXCEPT(Table, Table[Col1]) means 'Ignore all slicers on this table except the slicer for Col1'. Useful for calculating totals at specific groupings."),
    ]),

    # ─── Chapter 5: Time Intelligence ───
    Lesson("time-intelligence", 5, "Time Intelligence DAX", ["YTD", "Prior Year", "Running Total"], [SALES_FACT, DATE_DIM], [
        Task("pbi5-1", "Write a measure for Year-to-Date (YTD) Revenue.", "formula", "medium", "Amazon", "TOTALYTD(Expression, DateColumn)", "YTD Revenue = ", "TOTALYTD([Total Revenue], DimDate[Date])", "TOTALYTD("),
        Task("pbi5-2", "Write a measure to calculate Revenue from the Previous Year (Same period).", "formula", "hard", "Stripe", "CALCULATE(Measure, SAMEPERIODLASTYEAR(Dates))", "PY Revenue = ", "CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date]))", "SAMEPERIODLASTYEAR"),
        Task("pbi5-3", "What is strictly required for DAX Time Intelligence functions to work correctly?", "quiz", "medium", "Microsoft", options=("A standard Date table with no gaps, marked as a 'Date Table'", "Only the Fact table with a DateTime column", "Excel as a source", "At least 10 years of data"), answer_index=0, explanation="Time Intelligence requires a contiguous Calendar/Date table (every single day represented) and it must be marked as the official Date Table in the model."),
        Task("pbi5-4", "Write a measure using DATEADD to go back exactly 1 month.", "formula", "hard", "JPMorgan", "CALCULATE([Measure], DATEADD(Dates, -1, MONTH))", "Prev Month = ", "CALCULATE([Total Revenue], DATEADD(DimDate[Date], -1, MONTH))", "DATEADD("),
        Task("pbi5-5", "What happens if you use SAMEPERIODLASTYEAR but your date table only has data up to today, and you are comparing a leap year (Feb 29)?", "quiz", "hard", "", options=("Error", "It maps Feb 29 to Feb 28 of the non-leap year", "It returns Blank", "It maps to March 1"), answer_index=1, explanation="DAX handles leap years gracefully by shifting Feb 29 to Feb 28 when looking at a standard year."),
        Task("pbi5-6", "Write a DAX measure for a 30-day rolling average of Sales.", "formula", "hard", "Amazon", "Use AVERAGEX, DATESINPERIOD, LASTDATE", "Rolling 30 = ", "CALCULATE([Total Revenue], DATESINPERIOD(DimDate[Date], LASTDATE(DimDate[Date]), -30, DAY)) / 30", "DATESINPERIOD("),
        Task("pbi5-7", "If your fiscal year starts in July, how do you adjust TOTALYTD to match?", "quiz", "medium", "", options=("Write custom M code", "Pass a string like '06-30' as the third argument to TOTALYTD", "It's not possible", "Change your Windows clock"), answer_index=1, explanation="TOTALYTD( [Measure], Dates, \"06-30\" ) sets June 30th as the end of the year, so July 1 resets the YTD calculation."),
    ]),

    # ─── Chapter 6: DAX Variables & Optimization ───
    Lesson("dax-optimization", 6, "Variables & Optimization", ["VAR/RETURN", "Performance Analyzer", "DIVIDE"], [SALES_FACT], [
        Task("pbi6-1", "Why are DAX Variables (VAR) recommended for complex measures?", "quiz", "medium", "Amazon", options=("They make the code colorful", "They improve readability and performance by caching the result (evaluated only once)", "They are required for ALL function", "They save storage space"), answer_index=1, explanation="Variables are evaluated once at the point they are defined, and that result is reused. This prevents Power BI from re-calculating the exact same math multiple times in one measure."),
        Task("pbi6-2", "Write a measure using VAR to calculate Profit (Revenue - Cost) and return it.", "formula", "medium", "", "VAR R = ... VAR C = ... RETURN R - C", "Profit = ", "VAR Rev = [Total Revenue] VAR Cost = [Total Cost] RETURN Rev - Cost", "VAR"),
        Task("pbi6-3", "Which function is safer for division to avoid #DIV/0! errors?", "quiz", "easy", "", options=("/", "DIVIDE", "QUOTIENT", "SPLIT"), answer_index=1, explanation="DIVIDE(Numerator, Denominator) handles division by zero safely by returning BLANK (or an optional alternate result)."),
        Task("pbi6-4", "When using VAR, can the variable dynamically change its value inside a CALCULATE statement further down in the RETURN block?", "quiz", "hard", "Microsoft", options=("Yes, variables respond to CALCULATE", "No, variables are evaluated in the context they are defined and remain static", "Yes, if you use KEEPFILTERS", "Only if it is a string"), answer_index=1, explanation="This is a crucial concept. Variables are constants. If you define VAR x = SUM(Sales), and later do RETURN CALCULATE(x, Region='West'), it will NOT filter x by West. x was already calculated."),
        Task("pbi6-5", "What is the best tool inside Power BI Desktop to find out exactly how long a DAX measure takes to run?", "quiz", "medium", "McKinsey", options=("Task Manager", "Query Editor", "Performance Analyzer", "DAX Studio"), answer_index=2, explanation="Performance Analyzer records every action, showing time spent on DAX, Visual Display, and Other. (DAX Studio is an external tool, also excellent)."),
        Task("pbi6-6", "To optimize a model, you should remove Auto Date/Time in settings. Why?", "quiz", "hard", "", options=("It looks ugly", "It creates a hidden date table for EVERY date column in the model, massively bloating memory", "It causes timezone issues", "It stops you from using DAX"), answer_index=1, explanation="Auto Date/Time generates hidden tables that eat up RAM. Always disable it and use a single, centralized DimDate table."),
        Task("pbi6-7", "What is 'VertiPaq'?", "quiz", "medium", "", options=("A visualization type", "The underlying columnar in-memory database engine for Power BI / Analysis Services", "A DAX function", "A premium licensing tier"), answer_index=1, explanation="VertiPaq compresses columns using dictionary encoding and run-length encoding, which makes aggregation incredibly fast."),
    ]),

    # ─── Chapter 7: Advanced Filtering (RLS & Context) ───
    Lesson("advanced-filtering", 7, "Security & Advanced Context", ["RLS", "USERPRINCIPALNAME", "CALCULATETABLE"], [], [
        Task("pbi7-1", "What is Row-Level Security (RLS) used for?", "quiz", "easy", "Amazon", options=("Protecting the file with a password", "Restricting data access for specific users based on roles and DAX filters", "Hiding columns", "Speeding up reports"), answer_index=1, explanation="RLS allows you to define DAX filters on tables that restrict which rows a user can see based on their identity or role."),
        Task("pbi7-2", "Which DAX function is commonly used in Dynamic RLS to identify the logged-in user?", "quiz", "medium", "Google", options=("USERNAME()", "USERPRINCIPALNAME()", "WHOAMI()", "Both A and B"), answer_index=3, explanation="Both return user info, but USERPRINCIPALNAME() is generally preferred for cloud deployment as it reliably returns the user's UPN/email format."),
        Task("pbi7-3", "If User A is in 'West Region' role and 'East Region' role, what data do they see?", "quiz", "medium", "Microsoft", options=("Nothing, conflict error", "Only West", "Only East", "The union of both (West AND East)"), answer_index=3, explanation="If a user belongs to multiple roles, the RLS filters are combined using an OR operator. They see the union of the datasets."),
        Task("pbi7-4", "What does CALCULATETABLE do?", "quiz", "medium", "", options=("Same as CALCULATE, but it returns a Table instead of a scalar value", "Calculates the size of a table", "Exports a table to Excel", "Creates a visual table"), answer_index=0, explanation="Used heavily in DAX queries or inside iterator functions when you need to filter a table expression rather than a measure."),
        Task("pbi7-5", "To implement Object-Level Security (OLS) to hide a specific column (like Salary) from a group, where must it be configured?", "quiz", "hard", "Capital One", options=("Power BI Desktop UI", "Power BI Service Security Tab", "External tools like Tabular Editor", "DAX formula"), answer_index=2, explanation="As of recent versions, true OLS (hiding objects entirely so they throw an error if queried by unauthorized users) requires Tabular Editor via XMLA endpoints."),
        Task("pbi7-6", "Write an RLS DAX filter expression that restricts the DimRegion table to the logged-in user's email in the 'ManagerEmail' column.", "formula", "medium", "", "ManagerEmail = USERPRINCIPALNAME()", "", "ManagerEmail = USERPRINCIPALNAME()", "USERPRINCIPALNAME()"),
        Task("pbi7-7", "Why is it recommended to apply RLS on Dimension tables rather than Fact tables?", "quiz", "hard", "JPMorgan", options=("Fact tables don't support RLS", "Filtering Dimensions is faster and leverages existing relationships to naturally filter Fact tables", "Fact tables are too small", "It doesn't matter"), answer_index=1, explanation="Filtering a small Dim table (e.g., DimRegion) is fast. The 1:* relationship automatically propagates that filter to the massive Fact table."),
    ]),

    # ─── Chapter 8: Visualization Best Practices ───
    Lesson("viz-best-practices", 8, "Visualization & Storytelling", ["Chart Selection", "Tooltips", "Drillthrough"], [], [
        Task("pbi8-1", "You want to show the contribution of 3-4 categories to a total. Which chart is best?", "quiz", "easy", "", options=("Line Chart", "Donut/Pie Chart", "Scatter Plot", "Gantt Chart"), answer_index=1, explanation="Part-to-whole for a small number of categories is the ideal use case for Pie/Donut charts. (Avoid if > 5 categories)."),
        Task("pbi8-2", "What is the purpose of a 'Drillthrough' page in Power BI?", "quiz", "medium", "Amazon", options=("To delete data", "To allow users to right-click a data point and navigate to a detailed page filtered to that specific item", "To export to PDF", "To change the theme"), answer_index=1, explanation="Drillthrough creates a context-aware navigation path from a summary visual to a detailed report page."),
        Task("pbi8-3", "A user wants to see additional metrics when they hover over a bar chart, without cluttering the screen. What feature should you use?", "quiz", "easy", "", options=("Slicer", "Bookmark", "Report Page Tooltip", "Drilldown"), answer_index=2, explanation="Report Page Tooltips allow you to design a custom, mini-report page that pops up on hover, showing extra charts/metrics filtered to that specific data point."),
        Task("pbi8-4", "What is a major performance downside of having too many visuals (e.g., 30+ card visuals) on a single page?", "quiz", "hard", "Microsoft", options=("It crashes Excel", "Each visual generates its own DAX query, causing massive parallel execution bottlenecks and slow rendering", "It uses up hard drive space", "No downside"), answer_index=1, explanation="Every visual fires a separate DAX query. High visual counts cause query queuing, making the page incredibly slow. Grouped cards or custom HTML/SVG visuals are better."),
        Task("pbi8-5", "To toggle between two entirely different views (e.g., Map View vs Table View) using a button, you should use:", "quiz", "medium", "", options=("Drillthrough", "Bookmarks and Selection Pane", "Slicers", "Cross-filtering"), answer_index=1, explanation="Bookmarks capture the visibility state of visuals. You can use the Selection pane to hide/show visuals, save as a bookmark, and link it to a button."),
        Task("pbi8-6", "Which visual is best for showing the correlation and distribution of two numerical variables (e.g., Price vs Margin)?", "quiz", "easy", "", options=("Line Chart", "Scatter Plot", "Tree Map", "Gauge Chart"), answer_index=1, explanation="Scatter plots are the standard for XY numerical correlation."),
        Task("pbi8-7", "What does 'Edit Interactions' allow you to do?", "quiz", "medium", "Google", options=("Change the data source", "Control whether selecting a bar on Chart A filters, highlights, or ignores Chart B", "Write DAX", "Share the report"), answer_index=1, explanation="Edit Interactions provides granular control over how visuals interact with each other on the same page (Filter, Highlight, or None)."),
    ]),
]

LESSON_BY_ID = {l.id: l for l in LESSONS}

def _serialize_table(t: Table) -> dict:
    return {"name":t.name,"columns":list(t.columns),"rows":[list(r) for r in t.rows],"total":len(t.rows)}

def lesson_index() -> list[dict[str, Any]]:
    return [{"id":l.id,"number":l.number,"title":l.title,"focus":l.focus,"taskCount":len(l.tasks)} for l in LESSONS]

def lesson_payload(lesson_id: str) -> dict[str, Any]:
    l = LESSON_BY_ID.get(lesson_id, LESSONS[0])
    return {
        "id":l.id,"number":l.number,"title":l.title,"focus":l.focus,
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
    
    def norm(s): return str(s or "").strip().lower().replace(" ","").replace("$","").replace("'","").replace("[","").replace("]","").replace("\"","")

    if t.kind == "quiz":
        correct = answer == t.answer_index
        return {"correct":correct,"message":"Correct!" if correct else "Not quite.","explanation":t.explanation,"expectedIndex":t.answer_index}
    
    user = norm(answer)
    expected = norm(t.expected)
    solution = norm(t.solution)
    
    correct = expected in user or solution in user or user == expected
    return {"correct":correct, "message":"Correct!" if correct else f"Not quite. Expected logic: {t.expected}", "explanation":t.explanation, "solution":t.solution}
