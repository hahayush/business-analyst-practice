"""Senior-Level Data Interpretation module — Real-world, multi-step interview scenarios."""
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

# ── Complex Data Tables ──
MKTG_ROI = Table("MarketingPerformance", ("Campaign", "Channel", "Spend_USD", "Impressions", "Clicks", "Conversions", "Revenue_USD"), (
    ("Q1 Promo", "Social", 50000, 2000000, 40000, 2000, 150000),
    ("Retargeting", "Display", 15000, 500000, 5000, 800, 64000),
    ("Search Non-Brand", "SEM", 80000, 1000000, 80000, 4000, 240000),
    ("Influencer V1", "Social", 30000, 800000, 24000, 600, 45000),
))

COHORT_DATA = Table("UserCohortRetention", ("Cohort", "Users", "Month_1", "Month_2", "Month_3", "Month_6"), (
    ("Jan 2023", 10000, "45%", "30%", "25%", "18%"),
    ("Feb 2023", 12000, "48%", "32%", "26%", "19%"),
    ("Mar 2023", 15000, "35%", "20%", "15%", "10%"),
    ("Apr 2023", 11000, "50%", "35%", "30%", "22%"),
))

OPS_DATA = Table("FulfillmentOperations", ("Warehouse", "Capacity", "Received", "Shipped", "Breaches", "Defect_Rate"), (
    ("North (NY)", 5000, 5200, 5000, 400, "1.2%"),
    ("South (TX)", 8000, 6500, 6500, 50, "0.5%"),
    ("East (PA)", 3000, 2800, 2700, 150, "3.8%"),
    ("West (CA)", 10000, 9500, 9200, 450, "0.9%"),
))

FIN_SUMMARY = Table("FinancialSummary", ("Division", "Metric", "Y2021", "Y2022", "Y2023"), (
    ("Hardware", "Revenue", 500, 520, 510),
    ("Hardware", "COGS", 350, 380, 400),
    ("Software", "Revenue", 200, 300, 450),
    ("Software", "COGS", 40, 60, 90),
))

PRICING_EXP = Table("PricingElasticity", ("Region", "Old_Price", "New_Price", "Vol_Old", "Vol_New"), (
    ("NA", 100, 120, 50000, 40000),
    ("EU", 80, 90, 40000, 38000),
    ("APAC", 50, 55, 100000, 98000),
    ("LATAM", 40, 50, 80000, 50000),
))

SIMPSON_DATA = Table("HospitalSurvival", ("Hospital", "Condition", "Patients", "Survived"), (
    ("Hospital A", "Mild", 1000, 990),
    ("Hospital A", "Severe", 1000, 800),
    ("Hospital B", "Mild", 1800, 1764),
    ("Hospital B", "Severe", 200, 140),
))

# ── Lessons ──
LESSONS: list[Lesson] = [
    # ─── Chapter 1: Marketing Funnel & ROI ───
    Lesson("marketing-roi", 1, "Marketing Funnel & ROI", ["CAC", "ROAS", "CTR"], [MKTG_ROI], [
        Task("di1-1", "Which campaign has the highest Return on Ad Spend (ROAS)?", "quiz", "hard", "Amazon", options=("Q1 Promo", "Retargeting", "Search Non-Brand", "Influencer V1"), answer_index=1, explanation="ROAS = Revenue / Spend. Retargeting: 64k/15k = 4.26x."),
        Task("di1-2", "Calculate the Cost Per Acquisition (CAC) for the 'Influencer V1' campaign.", "formula", "medium", "Stripe", "CAC = Spend / Conversions", "", "50", "50"),
        Task("di1-3", "Which campaign gets cut if you eliminate the lowest Click-Through Rate (CTR)?", "quiz", "medium", "Google", options=("Q1 Promo", "Retargeting", "Search Non-Brand", "Influencer V1"), answer_index=1, explanation="CTR = Clicks / Impressions. Retargeting = 5k/500k = 1%."),
        Task("di1-4", "Calculate the Conversion Rate from Clicks for the Search Non-Brand campaign.", "formula", "easy", "", "4000 / 80000", "", "5%", "5"),
        Task("di1-5", "If Q1 Promo spend increases by 20% but CPC (Cost Per Click) remains identical, how many clicks will it generate?", "formula", "hard", "", "New Spend = 60000. CPC = 50000/40000 = $1.25. Clicks = 60000/1.25", "", "48000", "48000"),
        Task("di1-6", "Which channel has the lowest overall CAC?", "quiz", "medium", "", options=("Social", "Display", "SEM"), answer_index=1, explanation="Social CAC: (50k+30k)/(2k+600) = 80k/2600 = $30.7. Display: 15k/800 = $18.75. SEM: 80k/4k = $20. Display is lowest."),
        Task("di1-7", "What is the average Revenue Per Conversion for 'Q1 Promo'?", "formula", "easy", "", "150000 / 2000", "", "75", "75"),
    ]),

    # ─── Chapter 2: Cohort Analysis ───
    Lesson("cohort-analysis", 2, "Cohort & Retention Analysis", ["Retention Decay", "Anomalies"], [COHORT_DATA], [
        Task("di2-1", "How many users from the Jan 2023 cohort were still active in Month 6?", "formula", "medium", "McKinsey", "Users * Month 6 %", "", "1800", "1800"),
        Task("di2-2", "Which hypothesis best explains the anomaly in the Mar 2023 cohort?", "quiz", "hard", "Amazon", options=("Marketing budget was slashed", "A large influx of low-quality, heavily incentivized users were acquired", "The app crashed permanently", "Seasonality"), answer_index=1, explanation="March had highest acquisition (15k) but terrible retention (35% M1 vs normal 45-50%). Classic symptom of a viral campaign acquiring low-intent users."),
        Task("di2-3", "Calculate the absolute number of users lost between Month 1 and Month 2 for the Apr 2023 cohort.", "formula", "hard", "", "(M1 % - M2 %) * Acquired", "", "1650", "1650"),
        Task("di2-4", "Which cohort had the highest absolute number of retained users in Month 3?", "quiz", "medium", "", options=("Jan", "Feb", "Mar", "Apr"), answer_index=3, explanation="Jan: 2500. Feb: 3120. Mar: 2250. Apr: 3300."),
        Task("di2-5", "If the LTV of a user retained past Month 6 is $100, what is the 'Terminal Value' of the Feb 2023 cohort?", "formula", "medium", "", "12000 * 0.19 * 100", "", "228,000", "228000"),
        Task("di2-6", "What is the Month 1 to Month 6 churn rate for Jan 2023?", "formula", "hard", "", "Started M1 with 4500. Ended M6 with 1800. Lost 2700. Rate = 2700 / 4500 = 60%", "", "60%", "60"),
        Task("di2-7", "A 'Smile Graph' in retention implies:", "quiz", "medium", "Stripe", options=("Everyone churns", "Users churn early, but late-stage retained users start using the app MORE often over time", "Data is corrupted", "Revenue goes up"), answer_index=1, explanation="A smile graph shows initial decay, flattening, and then a slight uptick as the core power-users increase their usage frequency over years."),
    ]),

    # ─── Chapter 3: Operational Bottlenecks ───
    Lesson("ops-bottlenecks", 3, "Operational Bottlenecks & SLAs", ["Capacity", "Throughput"], [OPS_DATA], [
        Task("di3-1", "Which warehouse is operating OVER its daily capacity?", "quiz", "easy", "Amazon", options=("North (NY)", "South (TX)", "East (PA)", "West (CA)"), answer_index=0, explanation="North received 5200 but capacity is 5000."),
        Task("di3-2", "Calculate the SLA Breach Rate (Breaches / Shipped) for the East (PA) warehouse. Round to 1 decimal.", "formula", "medium", "", "150 / 2700 * 100", "", "5.6%", "5.6"),
        Task("di3-3", "If you must route 500 daily orders away from North (NY) to relieve capacity, which warehouse is the best candidate?", "quiz", "medium", "Amazon", options=("South (TX)", "East (PA)", "West (CA)", "None"), answer_index=0, explanation="South has 1500 unused capacity and the lowest defect rate (0.5%)."),
        Task("di3-4", "Calculate the total daily unused capacity across all warehouses.", "formula", "medium", "", "South: 1500. East: 200. West: 500. North: -200 (over). Total Unused = 2200.", "", "2200", "2200"),
        Task("di3-5", "Which warehouse has the highest absolute number of defective shipments?", "quiz", "medium", "", options=("North", "South", "East", "West"), answer_index=2, explanation="East: 2700 * 3.8% = 102.6. West: 9200 * 0.9% = 82.8. North: 5000 * 1.2% = 60."),
        Task("di3-6", "What is the overall SLA Breach Rate for the entire network?", "formula", "hard", "", "Total Breaches: 400+50+150+450 = 1050. Total Shipped: 5k+6.5k+2.7k+9.2k = 23,400. 1050 / 23400 = 4.48%", "", "4.5%", "4.5"),
        Task("di3-7", "If South (TX) capacity drops by 20% due to a storm, how much excess capacity remains there?", "formula", "medium", "", "New Cap = 8000 * 0.8 = 6400. Received = 6500. Excess = -100 (It is now over capacity).", "", "-100", "-100"),
    ]),

    # ─── Chapter 4: Financial P&L Breakdown ───
    Lesson("financial-pl", 4, "Deep P&L & Margin Shifts", ["YoY Growth", "Gross Margin"], [FIN_SUMMARY], [
        Task("di4-1", "Calculate the Gross Profit Margin % for the Software division in Y2023.", "formula", "medium", "Stripe", "(Revenue - COGS) / Revenue. (450 - 90) / 450", "", "80%", "80"),
        Task("di4-2", "Which statement accurately describes the company's trajectory from Y2021 to Y2023?", "quiz", "hard", "McKinsey", options=("Hardware drives profitability", "Transitioning from low-margin hardware to high-margin software", "Total revenue declining", "COGS growing faster than Revenue everywhere"), answer_index=1, explanation="Hardware is flat (500->510) with shrinking margins. Software more than doubled (200->450) with 80% margins."),
        Task("di4-3", "What is the Year-over-Year (YoY) total revenue growth rate from Y2022 to Y2023?", "formula", "hard", "Google", "Total Y22 = 820. Total Y23 = 960. Growth = (960-820)/820", "", "17%", "17"),
        Task("di4-4", "In Y2023, what percentage of total gross profit came from Software?", "formula", "hard", "", "Software Profit = 360. Hardware Profit = 110. Total = 470. 360/470 = 76.6%", "", "76.6%", "76.6"),
        Task("di4-5", "Calculate the CAGR for Software Revenue from Y2021 to Y2023 (2 years).", "formula", "hard", "Goldman Sachs", "(450/200)^(1/2) - 1 = 1.5 - 1", "", "50%", "50"),
        Task("di4-6", "What is the absolute dollar increase in Hardware COGS from Y2021 to Y2023?", "formula", "easy", "", "400 - 350", "", "50", "50"),
        Task("di4-7", "If Software COGS increases to 30% of revenue in Y2024, what will the gross margin be?", "formula", "easy", "", "100% - 30%", "", "70%", "70"),
    ]),

    # ─── Chapter 5: Price Elasticity ───
    Lesson("price-elasticity", 5, "Price Elasticity & Revenue Max", ["PED", "Cannibalization"], [PRICING_EXP], [
        Task("di5-1", "Calculate the Price Elasticity of Demand (PED) for the NA region. (Ignore negative sign)", "formula", "hard", "McKinsey", "% Change Q = (40k-50k)/50k = -20%. % Change P = (120-100)/100 = 20%. PED = 20/20 = 1", "", "1", "1"),
        Task("di5-2", "In which region did the price increase result in a DECREASE in total revenue?", "quiz", "hard", "Amazon", options=("NA", "EU", "APAC", "LATAM"), answer_index=3, explanation="LATAM Old Rev: 40*80k = 3.2M. LATAM New Rev: 50*50k = 2.5M. The massive volume drop destroyed revenue."),
        Task("di5-3", "Which market is the most 'inelastic' (volume dropped the least relative to price increase)?", "quiz", "medium", "", options=("NA", "EU", "APAC", "LATAM"), answer_index=2, explanation="APAC saw a 10% price increase but only a 2% volume drop. Highly inelastic."),
        Task("di5-4", "Calculate the absolute change in Total Revenue for the EU region.", "formula", "medium", "", "Old: 80*40k = 3.2M. New: 90*38k = 3.42M. Diff = +220k.", "", "220,000", "220000"),
        Task("di5-5", "If a market has a PED > 1, what happens to revenue when you raise prices?", "quiz", "hard", "Bain", options=("Revenue increases", "Revenue decreases", "Revenue stays flat", "Impossible to know"), answer_index=1, explanation="PED > 1 means it is Elastic. Demand drops faster than price rises, so total revenue falls."),
        Task("di5-6", "What is the new total global volume after the price changes?", "formula", "easy", "", "40k + 38k + 98k + 50k", "", "226,000", "226000"),
        Task("di5-7", "If variable cost per unit is $30 globally, did LATAM's total PROFIT increase or decrease after the price change?", "quiz", "hard", "", options=("Increase", "Decrease", "Stayed the same"), answer_index=1, explanation="Old Profit: (40-30)*80k = 800k. New Profit: (50-30)*50k = 1M. WAIT! Profit INCREASED from 800k to 1M, even though Revenue decreased!"),
    ]),

    # ─── Chapter 6: Statistical Fallacies (Simpson's Paradox) ───
    Lesson("simpsons-paradox", 6, "Statistical Fallacies", ["Simpson's Paradox", "Confounding"], [SIMPSON_DATA], [
        Task("di6-1", "Calculate the overall survival rate for Hospital A.", "formula", "easy", "", "(990+800) / 2000", "", "89.5%", "89.5"),
        Task("di6-2", "Calculate the overall survival rate for Hospital B.", "formula", "easy", "", "(1764+140) / 2000", "", "95.2%", "95.2"),
        Task("di6-3", "Calculate the survival rate for MILD cases in Hospital A.", "formula", "medium", "", "990 / 1000", "", "99%", "99"),
        Task("di6-4", "Calculate the survival rate for MILD cases in Hospital B.", "formula", "medium", "", "1764 / 1800", "", "98%", "98"),
        Task("di6-5", "Which hospital is better at treating Severe cases?", "quiz", "medium", "", options=("Hospital A", "Hospital B", "They are equal"), answer_index=0, explanation="A: 800/1000 = 80%. B: 140/200 = 70%. Hospital A is better."),
        Task("di6-6", "Hospital B has a higher overall survival rate, but Hospital A is better at treating BOTH Mild and Severe cases individually. What is this called?", "quiz", "hard", "McKinsey", options=("Survivorship Bias", "Simpson's Paradox", "Base Rate Fallacy", "Selection Bias"), answer_index=1, explanation="Simpson's Paradox. Hospital A gets way more severe (high mortality) cases (1000 vs 200), dragging its overall average down, even though its per-condition care is superior."),
        Task("di6-7", "What is the 'Confounding Variable' in this data?", "quiz", "hard", "Google", options=("The Hospitals", "The Patients", "The severity of the condition (Mix-shift)", "The Survival Rate"), answer_index=2, explanation="The severity of the condition dictates the baseline survival probability. Ignoring it confounds the aggregate metric."),
    ]),

    # ─── Chapter 7: Advanced Regressions ───
    Lesson("regressions", 7, "Advanced Regressions", ["R-Squared", "P-Value", "Correlation"], [], [
        Task("di7-1", "You run a regression: Sales = 50 + 2.5*(Ad Spend). If you spend $10, what is predicted Sales?", "formula", "easy", "", "50 + 2.5*10", "", "75", "75"),
        Task("di7-2", "The R-squared of your model is 0.85. What does this mean?", "quiz", "medium", "Stripe", options=("85% of your data is accurate", "Ad spend causes 85% of sales", "85% of the variance in Sales is explained by the variance in Ad Spend", "There is an 85% probability the model is right"), answer_index=2, explanation="R-squared measures the proportion of the variance in the dependent variable that is predictable from the independent variable."),
        Task("di7-3", "The P-value for Ad Spend is 0.02. Assuming alpha=0.05, is Ad Spend a statistically significant predictor?", "quiz", "medium", "Amazon", options=("Yes", "No", "Inconclusive"), answer_index=0, explanation="Since 0.02 < 0.05, we reject the null hypothesis. It is significant."),
        Task("di7-4", "If you add a useless variable (like 'Phase of the Moon') to your multiple regression model, what happens to R-squared?", "quiz", "hard", "JPMorgan", options=("It decreases", "It stays exactly the same", "It always increases or stays the same, which is why Adjusted R-squared is preferred", "It throws an error"), answer_index=2, explanation="Standard R-squared never decreases when you add variables, even useless ones. Adjusted R-squared penalizes you for adding non-predictive variables."),
        Task("di7-5", "What is Multicollinearity?", "quiz", "hard", "Goldman Sachs", options=("When independent variables are highly correlated with each other, destabilizing the coefficients", "When the model is too simple", "When R-squared is 1.0", "When P-values are negative"), answer_index=0, explanation="If you include 'Ad Spend in USD' and 'Ad Spend in EUR', they are perfectly correlated, confusing the model on which one is actually driving the result."),
        Task("di7-6", "A coefficient for 'Price' is -4.5. What does this mean?", "quiz", "medium", "", options=("Sales drop to zero", "For every $1 increase in Price, Sales decrease by 4.5 units", "Price is insignificant", "Sales increase by 4.5"), answer_index=1, explanation="Coefficients represent the marginal change in Y for a 1-unit change in X."),
        Task("di7-7", "What does a Correlation Coefficient (r) of -0.9 indicate?", "quiz", "easy", "", options=("Weak negative correlation", "Strong negative correlation", "No correlation", "Error"), answer_index=1, explanation="r ranges from -1 to 1. -0.9 is a very strong inverse relationship."),
    ]),

    # ─── Chapter 8: Funnel Drop-off Mathematics ───
    Lesson("funnel-math", 8, "Funnel Drop-off Mathematics", ["Conversion", "Throughput"], [], [
        Task("di8-1", "A funnel has 3 steps. Step 1->2 is 50%. Step 2->3 is 20%. What is the cumulative conversion rate?", "formula", "easy", "", "0.50 * 0.20", "", "10%", "10"),
        Task("di8-2", "If 100,000 users enter the funnel above, how many complete Step 3?", "formula", "easy", "", "100,000 * 0.10", "", "10,000", "10000"),
        Task("di8-3", "You optimize Step 2->3 from 20% to 40%. How much does total conversion increase (relative %)?", "formula", "medium", "Uber", "Old total = 10%. New total = 0.50 * 0.40 = 20%. Relative increase = 100%.", "", "100%", "100"),
        Task("di8-4", "If acquiring 100,000 top-of-funnel users costs $50,000, what is the effective Cost Per Acquisition (CPA) for a completed user (based on the original 10% conversion)?", "formula", "medium", "Stripe", "50,000 / 10,000 users", "", "$5", "5"),
        Task("di8-5", "Where is the absolute largest drop-off in a funnel with steps: 100k -> 20k -> 10k -> 9k?", "quiz", "easy", "", options=("Step 1 to 2", "Step 2 to 3", "Step 3 to 4", "Equal"), answer_index=0, explanation="100k to 20k is a loss of 80k users (80% drop)."),
        Task("di8-6", "If you must choose between improving Top-of-Funnel traffic by 10% or Bottom-of-Funnel conversion by 10% (relative), which yields more total conversions?", "quiz", "hard", "Meta", options=("Top of funnel", "Bottom of funnel", "They yield the exact same absolute number of conversions", "Cannot be determined"), answer_index=2, explanation="Since it's a multiplicative chain (Traffic * C1 * C2), a 10% relative increase to ANY factor increases the final product by exactly 10%."),
        Task("di8-7", "Why do PMs usually focus on Bottom-of-Funnel (BoF) first?", "quiz", "hard", "Amazon", options=("It's easier to code", "BoF users have high intent; fixing their friction has high ROI and doesn't require spending more on Ads (unlike Top-of-Funnel)", "They don't", "Because of SQL"), answer_index=1, explanation="Acquiring traffic is expensive. If the bottom of the funnel is a leaky bucket, buying more traffic is burning money. Fix the bucket first."),
    ]),

    # ─── Chapter 9: Supply Chain Inventory Analysis ───
    Lesson("supply-chain", 9, "Supply Chain Inventory Analysis", ["EOQ", "Turnover", "Lead Time"], [], [
        Task("di9-1", "If COGS is $1M and Average Inventory is $200k, what is the Inventory Turnover Ratio?", "formula", "easy", "Walmart", "1,000,000 / 200,000", "", "5", "5"),
        Task("di9-2", "What does an Inventory Turnover of 5 mean?", "quiz", "medium", "", options=("You hold 5 items", "You sell out and restock your entire inventory 5 times a year", "It takes 5 years to sell out", "You lose 5% to theft"), answer_index=1, explanation="Turnover measures velocity. Higher is generally better for cash flow."),
        Task("di9-3", "Calculate 'Days Sales of Inventory' (DSI) for the above scenario (assume 365 days).", "formula", "medium", "", "365 / 5", "", "73", "73"),
        Task("di9-4", "What is the primary risk of having a very high Inventory Turnover (e.g., 50)?", "quiz", "medium", "Amazon", options=("Too much cash", "Stockouts: running out of inventory and missing sales because you hold too little buffer stock", "Taxes", "Warehouse space"), answer_index=1, explanation="Operating too 'lean' makes you vulnerable to slight supply chain delays, causing stockouts."),
        Task("di9-5", "What does the Economic Order Quantity (EOQ) formula optimize?", "quiz", "hard", "McKinsey", options=("Marketing spend", "The exact order size that minimizes the total combined costs of ordering (shipping) and holding (storage) inventory", "Employee schedules", "Taxes"), answer_index=1, explanation="EOQ finds the mathematical minimum point on the total cost curve between ordering too often (high shipping costs) and ordering too much (high storage costs)."),
        Task("di9-6", "If Lead Time is 10 days, and Daily Demand is 50 units, what should the Reorder Point be (ignoring safety stock)?", "formula", "easy", "", "10 * 50", "", "500", "500"),
        Task("di9-7", "Why is Safety Stock necessary?", "quiz", "easy", "", options=("To look good", "To buffer against variability in Lead Time or Demand spikes", "To get bulk discounts", "To avoid taxes"), answer_index=1, explanation="Safety stock is insurance against supply chain variance."),
    ]),

    # ─── Chapter 10: Subscription / MRR Waterfalls ───
    Lesson("mrr-waterfall", 10, "Subscription / MRR Waterfalls", ["Expansion", "Contraction", "Net MRR"], [], [
        Task("di10-1", "Starting MRR = $100k. New MRR = $20k. Churn MRR = $5k. Contraction = $2k. Expansion = $10k. Calculate Ending MRR.", "formula", "medium", "Stripe", "100 + 20 - 5 - 2 + 10", "", "$123,000", "123000"),
        Task("di10-2", "Calculate the Net MRR Growth for the month.", "formula", "easy", "", "Ending - Starting = 123 - 100", "", "$23,000", "23000"),
        Task("di10-3", "What is 'Contraction MRR'?", "quiz", "medium", "Snowflake", options=("Customers cancelling entirely", "Existing customers downgrading to a cheaper tier or removing seats", "New customers negotiating discounts", "Taxes"), answer_index=1, explanation="Contraction is lost revenue from retained customers."),
        Task("di10-4", "Calculate Net Revenue Retention (NRR) for this month. (Starting = 100k, Churn = 5k, Contraction = 2k, Expansion = 10k).", "formula", "hard", "Salesforce", "NRR ignores New MRR. (100 - 5 - 2 + 10) / 100 = 103 / 100", "", "103%", "103"),
        Task("di10-5", "Since NRR > 100%, what happens if the sales team acquires 0 new customers next month?", "quiz", "medium", "Bain", options=("MRR drops to 0", "MRR stays flat", "Total MRR still grows because expansion from existing customers outpaces the churn/contraction", "The company goes bankrupt"), answer_index=2, explanation="This is the power of negative churn. The installed base grows on its own."),
        Task("di10-6", "Calculate Gross Revenue Retention (GRR).", "formula", "hard", "Capital One", "GRR ignores Expansion. (100 - 5 - 2) / 100 = 93 / 100", "", "93%", "93"),
        Task("di10-7", "Why do investors look at GRR in addition to NRR?", "quiz", "hard", "Sequoia", options=("They don't", "Because a massive NRR driven by 1 huge upsell can hide the fact that 30% of the customer base churned. GRR reveals the true 'leaky bucket' floor.", "GRR is easier to calculate", "Taxes"), answer_index=1, explanation="GRR maxes out at 100%. If GRR is 70% but NRR is 120%, the core product is flawed and highly reliant on whale accounts expanding."),
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
    
    def norm(s): return str(s or "").strip().lower().replace(" ","").replace("$","").replace("%","").replace(",","").replace("k","000").replace("m","000000")

    if t.kind == "quiz":
        correct = answer == t.answer_index
        return {"correct":correct,"message":"Correct!" if correct else "Not quite.","explanation":t.explanation,"expectedIndex":t.answer_index}
    
    user = norm(answer)
    expected = norm(t.expected)
    solution = norm(t.solution)
    
    correct = expected in user or (solution in user if solution else False) or user == expected
    return {"correct":correct, "message":"Correct!" if correct else f"Not quite. Expected logic: {t.expected}", "explanation":t.explanation, "solution":t.solution}
