"""Senior-Level Tableau practice module — LODs, Table Calcs, and Parameters."""
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
SUPERSTORE_SALES = Table("Orders", ("OrderID", "Date", "Region", "Category", "SubCategory", "Sales", "Profit", "Customer"), (
    (1, "2024-01-01", "West", "Furniture", "Chairs", 500, 50, "Alice"),
    (2, "2024-01-05", "West", "Technology", "Phones", 1200, 200, "Alice"),
    (3, "2024-01-10", "East", "Office Supplies", "Paper", 20, 5, "Bob"),
    (4, "2024-02-01", "East", "Technology", "Phones", 1500, 300, "Charlie"),
    (5, "2024-02-15", "South", "Furniture", "Tables", 800, -100, "Dave"),
))

# ── Lessons ──
LESSONS: list[Lesson] = [
    # ─── Chapter 1: Calculations & Logic ───
    Lesson("tableau-logic", 1, "Calculated Fields & Logic", ["IF/THEN", "ZN", "CASE", "Aggregations"], [SUPERSTORE_SALES], [
        Task("tab1-1", "Write a formula to calculate Profit Margin.", "formula", "easy", "Amazon", "SUM(Profit) / SUM(Sales)", "Profit Margin = ", "SUM([Profit]) / SUM([Sales])", "SUM([Profit])/SUM([Sales])"),
        Task("tab1-2", "Write a formula that returns 'Loss' if Profit is negative, 'Breakeven' if 0, else 'Profit'.", "formula", "medium", "Stripe", "Use IF...ELSEIF...END", "Status = ", "IF [Profit] < 0 THEN 'Loss' ELSEIF [Profit] = 0 THEN 'Breakeven' ELSE 'Profit' END", "IF[Profit]<0"),
        Task("tab1-3", "What does the ZN() function do in Tableau?", "quiz", "easy", "", options=("Calculates Z-score", "Converts Nulls to Zero", "Returns the name of a field", "Zoom to Node"), answer_index=1, explanation="ZN() stands for Zero-Null. It is essential for ensuring calculations don't break when data is missing."),
        Task("tab1-4", "Why does SUM([Profit])/SUM([Sales]) work correctly at a rolled-up view level, but [Profit]/[Sales] does not?", "quiz", "hard", "JPMorgan", options=("[Profit]/[Sales] is a row-level calculation that gets summed (wrong), while SUM/SUM calculates the margin of the aggregate (correct).", "SUM is faster.", "[Profit]/[Sales] throws a syntax error.", "They both return the exact same thing."), answer_index=0, explanation="[Profit]/[Sales] calculates the ratio on every single row, and then Tableau sums those ratios up (which is mathematically meaningless). SUM/SUM calculates the total profit first, then divides by total sales."),
        Task("tab1-5", "Write a CASE statement to categorize 'West' as 'W', 'East' as 'E', else 'Other'.", "formula", "medium", "", "CASE [Region] WHEN ...", "ShortRegion = ", "CASE [Region] WHEN 'West' THEN 'W' WHEN 'East' THEN 'E' ELSE 'Other' END", "CASE[Region]"),
        Task("tab1-6", "What is the difference between COUNT and COUNTD?", "quiz", "easy", "", options=("COUNT counts columns, COUNTD counts rows", "COUNT counts all rows including nulls, COUNTD counts duplicates", "COUNT counts all non-null values, COUNTD counts unique non-null values", "No difference"), answer_index=2, explanation="COUNTD = Count Distinct."),
        Task("tab1-7", "If you write `IF [Category] = 'Furniture' THEN [Sales] END`, what happens to the rows that are NOT Furniture?", "quiz", "medium", "McKinsey", options=("They return 0", "They return Null", "They throw an error", "They return the string 'False'"), answer_index=1, explanation="In Tableau IF statements, if an ELSE clause is omitted, the default output for non-matching rows is Null."),
    ]),

    # ─── Chapter 2: Level of Detail (LOD) Expressions ───
    Lesson("tableau-lod", 2, "LOD Expressions (The 'Heavy' Logic)", ["FIXED", "INCLUDE", "EXCLUDE"], [SUPERSTORE_SALES], [
        Task("tab2-1", "Write a FIXED LOD to calculate the total sales for each Customer, regardless of view filters.", "formula", "hard", "Google", "{ FIXED [Dim] : SUM(Measure) }", "Customer Lifetime Sales = ", "{ FIXED [Customer] : SUM([Sales]) }", "{FIXED[Customer]"),
        Task("tab2-2", "When using a FIXED LOD, does it ignore 'Dimension Filters' in the filter shelf?", "quiz", "hard", "Amazon", options=("Yes, it is calculated before Dimension Filters", "No, it follows all filters", "Only if it is a Measure filter", "Only if it is Blue"), answer_index=0, explanation="FIXED LODs are calculated before Dimension filters in Tableau's Order of Operations. To filter a FIXED LOD, you must use a 'Context Filter'."),
        Task("tab2-3", "Which LOD expression would you use to calculate values at a higher level than the viz (e.g. ignoring Sub-Category while Sub-Category is in the viz)?", "quiz", "medium", "Stripe", options=("FIXED", "INCLUDE", "EXCLUDE", "TOTAL"), answer_index=2, explanation="EXCLUDE removes a dimension from the level of detail aggregation, letting you compare a row against a higher-level category."),
        Task("tab2-4", "Write an INCLUDE LOD that calculates the Average Sales per OrderID, to be averaged across Regions.", "formula", "hard", "Capital One", "AVG( { INCLUDE [OrderID] : SUM([Sales]) } )", "Avg Order Size = ", "AVG({ INCLUDE [OrderID] : SUM([Sales]) })", "{INCLUDE[OrderID]"),
        Task("tab2-5", "You want to find the date of a customer's very first purchase. Write the FIXED LOD for this.", "formula", "medium", "Amazon", "{ FIXED [Customer] : MIN([Date]) }", "First Purchase Date = ", "{ FIXED [Customer] : MIN([Date]) }", "MIN([Date])"),
        Task("tab2-6", "What happens if you use a FIXED LOD without declaring a dimension, e.g., `{ FIXED : SUM([Sales]) }`?", "quiz", "medium", "", options=("Syntax error", "It calculates the grand total of Sales across the entire dataset", "It calculates Sales at the row level", "It returns Null"), answer_index=1, explanation="A table-scoped LOD `{ SUM([Sales]) }` or `{ FIXED : SUM([Sales]) }` ignores all dimensions in the view and returns the absolute grand total."),
        Task("tab2-7", "If a dimension filter is NOT added to Context, how does it affect an INCLUDE LOD?", "quiz", "hard", "McKinsey", options=("It ignores the filter", "The INCLUDE LOD is filtered because INCLUDE evaluates AFTER Dimension Filters", "It throws an error", "It forces the filter to become Context"), answer_index=1, explanation="Unlike FIXED LODs, both INCLUDE and EXCLUDE evaluate AFTER Dimension filters in the Order of Operations."),
    ]),

    # ─── Chapter 3: Table Calculations ───
    Lesson("tableau-table-calcs", 3, "Advanced Table Calculations", ["Running Total", "Percent of Total", "Rank", "Window"], [SUPERSTORE_SALES], [
        Task("tab3-1", "You want to calculate the 'Running Total' of Sales. Which function is used for this as a calculated field?", "formula", "medium", "", "RUNNING_SUM(SUM([Sales]))", "Running Sales = ", "RUNNING_SUM(SUM([Sales]))", "RUNNING_SUM("),
        Task("tab3-2", "What is the difference between 'Table (Across)' and 'Table (Down)'?", "quiz", "easy", "", options=("Colors vs Shapes", "The direction in which the calculation is computed relative to the layout", "The file format", "No difference"), answer_index=1, explanation="Table Calculations are computed relative to the visual layout. 'Across' moves horizontally; 'Down' moves vertically."),
        Task("tab3-3", "Write a formula to calculate each Category's Percent of Total Sales.", "formula", "hard", "Amazon", "SUM([Sales]) / TOTAL(SUM([Sales]))", "% of Total = ", "SUM([Sales]) / TOTAL(SUM([Sales]))", "TOTAL(SUM("),
        Task("tab3-4", "Which function looks at the row exactly 1 position above the current row to calculate month-over-month growth?", "quiz", "medium", "Stripe", options=("PREVIOUS()", "LOOKUP(SUM([Sales]), -1)", "WINDOW_MAX()", "OFFSET()"), answer_index=1, explanation="LOOKUP allows you to specify a relative offset. -1 looks at the previous row (or column, depending on compute direction)."),
        Task("tab3-5", "If you filter out December data using a standard Dimension filter, will a Table Calculation for a 12-month Moving Average still calculate correctly?", "quiz", "hard", "Google", options=("Yes", "No, because Table Calculations happen last, the data is already filtered out and unavailable", "Yes, if it's a Context filter", "Tableau will crash"), answer_index=1, explanation="Table Calcs operate on the data that is currently in the 'view'. If you filter data out early, the Table Calc can't see it. You must use a Table Calc filter (e.g., LOOKUP) to hide data without filtering it out of the underlying table."),
        Task("tab3-6", "Write a formula using WINDOW_AVG to calculate a 3-period moving average (previous 2 periods + current period).", "formula", "hard", "JPMorgan", "WINDOW_AVG(SUM([Sales]), -2, 0)", "Moving Avg = ", "WINDOW_AVG(SUM([Sales]), -2, 0)", "WINDOW_AVG("),
        Task("tab3-7", "What does the RANK() function do if there is a tie, and you use the default RANK() instead of RANK_DENSE()?", "quiz", "medium", "", options=("Assigns random ranks", "Assigns identical ranks, but skips the next number (e.g., 1, 2, 2, 4)", "Assigns identical ranks and doesn't skip (e.g., 1, 2, 2, 3)", "Throws an error"), answer_index=1, explanation="Standard RANK skips numbers after a tie (1, 2, 2, 4). RANK_DENSE does not skip (1, 2, 2, 3)."),
    ]),

    # ─── Chapter 4: Parameters & Dynamic Control ───
    Lesson("tableau-parameters", 4, "Parameters & Dynamic Control", ["User Input", "Dynamic Measures", "Top N"], [], [
        Task("tab4-1", "What is a Parameter in Tableau?", "quiz", "easy", "Stripe", options=("A type of filter", "A global placeholder value that users can change to drive logic", "A database table", "A chart type"), answer_index=1, explanation="Parameters are dynamic inputs that can be used in filters, calculated fields, and reference lines."),
        Task("tab4-2", "To create a 'Top N' filter where the user can choose the value of N, you must use a:", "quiz", "medium", "Amazon", options=("Set", "Group", "Parameter", "Calculated Field"), answer_index=2, explanation="Parameters allow the 'N' in Top N to be interactive rather than hard-coded."),
        Task("tab4-3", "You create a parameter called [Select Measure]. Write a CASE statement to swap between SUM(Sales) and SUM(Profit).", "formula", "hard", "McKinsey", "CASE [Select Measure] WHEN 'Sales' THEN ...", "Dynamic Measure = ", "CASE [Select Measure] WHEN 'Sales' THEN SUM([Sales]) WHEN 'Profit' THEN SUM([Profit]) END", "CASE[SelectMeasure]"),
        Task("tab4-4", "Can a parameter update automatically when the underlying database adds new rows?", "quiz", "medium", "", options=("No, never", "Yes, in modern Tableau using 'When workbook opens' in the parameter list settings", "Only if using an Extract", "Only if it is a string parameter"), answer_index=1, explanation="Tableau added Dynamic Parameters which allow the list of values to refresh from a field when the workbook opens."),
        Task("tab4-5", "Why would you use a Parameter instead of a standard quick filter?", "quiz", "hard", "Google", options=("Parameters are faster", "Parameters can affect multiple disparate data sources simultaneously, whereas filters usually apply to a single source", "Parameters look better", "You shouldn't"), answer_index=1, explanation="Parameters are global to the workbook. They are the best way to drive changes across multiple blended or unrelated data sources."),
        Task("tab4-6", "Write a calculated field to color rows differently if their Sales are greater than a [Target Sales] parameter.", "formula", "medium", "", "IF SUM([Sales]) > [Target Sales] THEN 'Above' ELSE 'Below' END", "Color Status = ", "IF SUM([Sales]) > [Target Sales] THEN 'Above' ELSE 'Below' END", "IFSUM([Sales])>[TargetSales]"),
        Task("tab4-7", "What is a 'Parameter Action'?", "quiz", "hard", "Capital One", options=("Clicking a button to delete a parameter", "Allowing a user to click a mark on a visual, which updates the value of a parameter", "Automating parameter creation", "A database trigger"), answer_index=1, explanation="Parameter actions allow users to visually interact with a chart (e.g., clicking a state) to drive a parameter value, changing the logic of the entire dashboard."),
    ]),

    # ─── Chapter 5: Sets, Groups, and Bins ───
    Lesson("tableau-sets", 5, "Sets, Groups, and Bins", ["Cohorts", "Logical Subsets", "Histograms"], [SUPERSTORE_SALES], [
        Task("tab5-1", "What is the primary difference between a Group and a Set?", "quiz", "medium", "Google", options=("Sets are static; Groups are dynamic", "Groups create new categories; Sets create In/Out boolean logic", "Sets only work with numbers", "No difference"), answer_index=1, explanation="Groups create a new dimension with consolidated items. Sets create a logical subset (In/Out) which can be dynamic (based on conditions)."),
        Task("tab5-2", "You want to create a Histogram. Which feature should you use to create the X-axis ranges?", "quiz", "easy", "", options=("Groups", "Bins", "Sets", "Calculated Fields"), answer_index=1, explanation="Bins take a continuous measure and divide it into discrete 'buckets' for histograms."),
        Task("tab5-3", "How do you create a 'Combined Set'?", "quiz", "medium", "", options=("Write a calculated field", "Select two sets on the same dimension, right click, and choose Create Combined Set (Union, Intersect, Except)", "Blend the data", "You cannot combine sets"), answer_index=1, explanation="Tableau natively allows combining two sets to find overlapping cohorts (e.g., Customers who bought in 2023 AND 2024)."),
        Task("tab5-4", "Can a Set be used inside a Calculated Field?", "quiz", "easy", "Stripe", options=("Yes, it resolves to True (In) or False (Out)", "No, it is purely visual", "Only for Top N", "Only in text tables"), answer_index=0, explanation="Because sets are essentially boolean arrays, you can write IF [Set Name] THEN ... END."),
        Task("tab5-5", "What is a 'Set Action'?", "quiz", "hard", "Amazon", options=("Deleting a set", "Allowing users to visually select marks to dynamically add or remove them from a Set", "Automating set calculations", "Grouping fields"), answer_index=1, explanation="Set actions make sets interactive. Selecting bars on a chart can redefine who is 'IN' the set, instantly updating proportional brushing on other charts."),
        Task("tab5-6", "Write a formula using a Set called [Top Customers] to return Sales only for those customers.", "formula", "medium", "", "IF [Top Customers] THEN [Sales] END", "Top Sales = ", "IF [Top Customers] THEN [Sales] END", "IF[TopCustomers]THEN[Sales]"),
        Task("tab5-7", "If you group states into 'East Coast' and 'West Coast', does this create a new column in the underlying database?", "quiz", "medium", "", options=("Yes, it alters the SQL", "No, it creates a virtual dimension within the Tableau workbook memory", "Yes, if it's an extract", "No, it deletes the old column"), answer_index=1, explanation="Groups are calculated locally in Tableau and do not mutate the source database."),
    ]),

    # ─── Chapter 6: Relationships vs Joins ───
    Lesson("tableau-data-modeling", 6, "Relationships vs Joins", ["Logical Layer", "Physical Layer", "Blending"], [], [
        Task("tab6-1", "In newer Tableau versions, what is the 'Noodle' relationship called?", "quiz", "easy", "Stripe", options=("Physical Join", "Logical Relationship", "Data Blending", "Cross-database join"), answer_index=1, explanation="Relationships exist in the Logical layer. They are more flexible than Joins because they only query the necessary tables at the correct granularity."),
        Task("tab6-2", "When should you use 'Data Blending' instead of a Join or Relationship?", "quiz", "hard", "Amazon", options=("When tables are from different data sources and cannot be joined (e.g., published server data vs local excel)", "When you want to save space", "Always", "Never"), answer_index=0, explanation="Blending is a left-join-like operation performed after aggregation, useful when tables from separate sources cannot be related directly."),
        Task("tab6-3", "What is a primary advantage of Logical Relationships over traditional Left Joins?", "quiz", "hard", "JPMorgan", options=("They are older", "They automatically handle different levels of granularity without duplicating data (no double counting)", "They look like noodles", "They force Inner Joins"), answer_index=1, explanation="If you join Sales (daily) to Quota (monthly), traditional joins duplicate the Quota. Relationships keep them at their native granularity until viz time."),
        Task("tab6-4", "In Data Blending, what does the orange link icon mean?", "quiz", "medium", "", options=("Broken link", "Active linking field between the primary and secondary source", "Extract needed", "Primary key"), answer_index=1, explanation="The orange chain link indicates the dimension is being used to join the aggregated secondary data to the primary data."),
        Task("tab6-5", "Can you use an INCLUDE LOD expression on a field from a secondary blended data source?", "quiz", "hard", "Google", options=("Yes", "No, LODs cannot be used across blended sources", "Only if it is a FIXED LOD", "Only if the sources are Excel"), answer_index=1, explanation="Data Blending aggregates data before joining. LODs require row-level access. Thus, LODs do not work across blended data sources."),
        Task("tab6-6", "What happens in the Physical Layer of Tableau's data model?", "quiz", "medium", "", options=("Noodles are formed", "Traditional Venn-diagram joins (Inner, Left, Right, Full) and Unions are defined", "Dashboard layouts are saved", "Nothing"), answer_index=1, explanation="Double-clicking a logical table opens the physical layer, where you dictate hard SQL joins."),
        Task("tab6-7", "If you do a Left Join between Customers (100 rows) and Orders (500 rows), how many rows does the resulting physical table have?", "quiz", "easy", "", options=("100", "500", "600", "At least 500, possibly more if there are unmatched orders"), answer_index=3, explanation="A Left Join from Customers to Orders will return all 500 orders, plus any customers who have 0 orders."),
    ]),

    # ─── Chapter 7: Order of Operations ───
    Lesson("tableau-ooo", 7, "The Order of Operations", ["Context Filters", "Dimension Filters", "Table Calcs"], [], [
        Task("tab7-1", "Place these in the correct order of execution (first to last): A) Dimension Filters, B) Context Filters, C) Extract Filters.", "quiz", "hard", "Google", options=("A -> B -> C", "C -> B -> A", "B -> C -> A", "C -> A -> B"), answer_index=1, explanation="Extract Filters happen first, then Data Source filters, then Context Filters, then LODs/Dimension Filters."),
        Task("tab7-2", "You have a FIXED LOD and a filter. You want the filter to apply *before* the LOD. What should you do?", "quiz", "hard", "Amazon", options=("Make it a Dimension Filter", "Add to Context", "Make it a Measure Filter", "Use a Parameter"), answer_index=1, explanation="Context Filters are calculated before FIXED LODs. Standard Dimension filters are calculated after."),
        Task("tab7-3", "Where do Table Calculation Filters sit in the Order of Operations?", "quiz", "hard", "McKinsey", options=("At the very beginning", "In the middle, with Dimension filters", "At the very end, after all other filters and aggregations", "They don't exist"), answer_index=2, explanation="Table Calc Filters (like LOOKUP(MIN([Date]),0)) are executed last. They hide data from the visual without removing it from the underlying computations."),
        Task("tab7-4", "Why is the Order of Operations critical for Top N filters?", "quiz", "medium", "Stripe", options=("It isn't", "Because a Dimension filter is applied AFTER a Top N filter. To filter the list BEFORE calculating the Top N, the filter must be added to Context.", "Because Top N only works on Fridays", "Top N is calculated first"), answer_index=1, explanation="Top N filters sit right below Context filters but above Dimension filters. If you want the Top 10 Customers in 'West', 'Region = West' must be a Context filter."),
        Task("tab7-5", "You create an INCLUDE LOD. Which filter type will apply to it?", "quiz", "medium", "", options=("Extract Filters only", "Context Filters only", "Both Context and Dimension Filters", "None"), answer_index=2, explanation="INCLUDE and EXCLUDE LODs evaluate after Dimension filters, meaning they respect all standard filters in the view."),
        Task("tab7-6", "Are Measure Filters applied before or after Dimension Filters?", "quiz", "easy", "", options=("Before", "After", "At the same time", "Measure filters don't exist"), answer_index=1, explanation="Measure filters (e.g., filtering out SUM(Sales) < 1000) happen after Dimensions are filtered and LODs are calculated."),
        Task("tab7-7", "What is a 'Data Source Filter'?", "quiz", "medium", "", options=("A filter that applies to the entire workbook, executing right after Extract filters and before Context filters", "A filter on a specific dashboard", "A parameter", "An action"), answer_index=0, explanation="Data Source filters globally restrict data across all sheets before any worksheet-level logic runs."),
    ]),

    # ─── Chapter 8: Dashboarding & Optimization ───
    Lesson("tableau-dashboards", 8, "Dashboard Design & Performance", ["Actions", "Containers", "Optimization"], [], [
        Task("tab8-1", "Which 'Action' allows you to send a user to a specific website based on a data point click?", "quiz", "easy", "", options=("Filter Action", "Highlight Action", "Go to URL Action", "Set Action"), answer_index=2, explanation="Go to URL actions are used for external linking."),
        Task("tab8-2", "What is one primary way to improve a slow Tableau dashboard?", "quiz", "medium", "Amazon", options=("Add more quick filters", "Use an Extract instead of Live connection", "Use more images", "Add more worksheets"), answer_index=1, explanation="Extracts are highly optimized for Tableau's Hyper engine and are generally much faster than live database queries."),
        Task("tab8-3", "Why is it recommended to minimize 'Relevant Values' quick filters?", "quiz", "hard", "Capital One", options=("They look ugly", "They generate a complex database query every time ANY filter changes, massively slowing down performance", "They limit the number of colors", "They don't work on mobile"), answer_index=1, explanation="When filters are set to 'Only Relevant Values', changing one filter forces Tableau to query the database to figure out what values to show in the other filter, causing severe lag."),
        Task("tab8-4", "What is the purpose of Layout Containers (Horizontal/Vertical)?", "quiz", "medium", "", options=("To store data", "To group visuals together so they resize dynamically and collapse when a visual is hidden", "To write calculations", "To export as PDF"), answer_index=1, explanation="Containers are essential for neat alignments and for UI tricks like swapping sheets (because hidden sheets collapse inside containers)."),
        Task("tab8-5", "What is the 'Performance Recording' feature?", "quiz", "medium", "JPMorgan", options=("A microphone tool", "A built-in Tableau tool that generates a workbook showing exactly how many milliseconds each query, layout, and render step took", "A cloud backup", "An excel macro"), answer_index=1, explanation="Help -> Settings and Performance -> Start Performance Recording is the primary debugging tool for slow Tableau workbooks."),
        Task("tab8-6", "How does using high-cardinality discrete dimensions (like millions of Order IDs) on the Detail mark affect performance?", "quiz", "hard", "Stripe", options=("It speeds it up", "It forces Tableau to render millions of individual SVG marks, destroying browser memory and rendering speed", "It changes the colors", "No effect"), answer_index=1, explanation="Rendering a large number of marks is the #1 cause of client-side browser freezes in Tableau. Aggregate data before visualizing."),
        Task("tab8-7", "What is the benefit of publishing Data Sources separately from Workbooks on Tableau Server?", "quiz", "medium", "", options=("It creates backups", "It creates a Single Source of Truth, allowing multiple workbooks to connect to the same certified, scheduled extract", "It hides the data", "It reduces license costs"), answer_index=1, explanation="Published Data Sources enable reusability, governance, and reduce server load because the extract is only refreshed once for many workbooks."),
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
    
    def norm(s): return str(s or "").strip().lower().replace(" ","").replace("$","").replace("'","").replace("[","").replace("]","").replace("{","").replace("}","").replace("\"","")

    if t.kind == "quiz":
        correct = answer == t.answer_index
        return {"correct":correct,"message":"Correct!" if correct else "Not quite.","explanation":t.explanation,"expectedIndex":t.answer_index}
    
    user = norm(answer)
    expected = norm(t.expected)
    solution = norm(t.solution)
    
    correct = expected in user or solution in user or user == expected
    return {"correct":correct, "message":"Correct!" if correct else f"Not quite. Expected logic: {t.expected}", "explanation":t.explanation, "solution":t.solution}
