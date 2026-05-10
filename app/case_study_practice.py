"""Senior-Level Case Studies practice module — Consulting & Fintech scenarios."""
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

# ── Lessons ──
LESSONS: list[Lesson] = [
    # ─── Chapter 1: Root Cause Analysis ───
    Lesson("rca-metrics", 1, "Root Cause Analysis (Metric Drops)", ["MECE", "Segmentation", "Funnel"], [], [
        Task("cs1-1", "Uber: 'Weekly active riders dropped by 10% WoW.' What is the most MECE (Mutually Exclusive, Collectively Exhaustive) way to split this metric first?", "quiz", "medium", "Uber", options=("By Geography and Demographics", "By Supply (Drivers) vs Demand (Riders)", "By Internal (App crash) vs External (Weather/Competitors)", "By iOS vs Android"), answer_index=2, explanation="Internal vs External is the standard MECE split for sudden metric drops to isolate technical/business changes from macro factors."),
        Task("cs1-2", "If the drop is purely Internal, what is the next logical cut?", "quiz", "medium", "Google", options=("Marketing spend vs Technical issues vs Operations", "Price vs Volume", "Fixed vs Variable cost", "Male vs Female"), answer_index=0, explanation="Internally, a metric drops because you spent less acquiring it (Marketing), the app broke (Technical), or supply failed (Operations)."),
        Task("cs1-3", "You find it's a technical issue on Android only. It's not a crash. What funnel step do you check?", "quiz", "hard", "Meta", options=("App open rate", "Search to Book conversion", "Payment success rate", "All of the above, mapped to the user journey"), answer_index=3, explanation="Once isolated to a platform, map the exact user funnel (Open -> Search -> Book -> Pay) to find the exact bottleneck step."),
        Task("cs1-4", "Stripe: 'Payment success rate dropped 300bps in Europe.' You find it's due to a specific acquiring bank. What is the immediate action?", "quiz", "medium", "Stripe", options=("Call the bank", "Route traffic to a fallback acquirer immediately", "Pause all European transactions", "Refund customers"), answer_index=1, explanation="In fintech, availability is critical. Failover/route away from the failing dependency immediately, then investigate."),
        Task("cs1-5", "Amazon: 'Conversion rate on product pages dropped 5%.' Traffic is stable. What is the most likely cause?", "quiz", "hard", "Amazon", options=("AWS outage", "Competitor launched a sale", "A UI change pushed the 'Buy' button below the fold or removed reviews", "Prime membership fee increased"), answer_index=2, explanation="Stable traffic but dropping conversion heavily implies a friction point was added to the specific page UX."),
        Task("cs1-6", "What is Simpson's Paradox in the context of RCA?", "quiz", "hard", "McKinsey", options=("When a metric drops, but revenue goes up", "A trend appears in different groups of data but disappears or reverses when these groups are combined", "When the CEO disagrees with the data", "When two metrics drop simultaneously"), answer_index=1, explanation="Simpson's Paradox occurs when a mix-shift hides the true performance. (e.g., Overall conversion drops, but conversion for both Mobile and Desktop went up individually. The drop is because a larger % of users shifted to the lower-converting Mobile)."),
        Task("cs1-7", "How do you investigate if cannibalization is the root cause of a product's sales drop?", "quiz", "medium", "", options=("Check if a newly launched sister product saw a proportional spike in volume", "Check competitors", "Check marketing spend", "Check seasonality"), answer_index=0, explanation="Cannibalization implies the volume didn't leave the company; it just shifted to a different SKU."),
        Task("cs1-8", "If daily active users (DAU) dropped, but monthly active users (MAU) remained flat, what does this indicate?", "quiz", "hard", "Meta", options=("Users churned completely", "Users are logging in less frequently, but still logging in within the month", "New user acquisition spiked", "Data pipeline is broken"), answer_index=1, explanation="DAU/MAU measures stickiness. If DAU drops but MAU holds, users haven't abandoned the app, their engagement frequency simply decreased."),
    ]),

    # ─── Chapter 2: Guesstimates & Market Sizing ───
    Lesson("guesstimates", 2, "Guesstimates & Market Sizing", ["Top-down", "Bottom-up", "Proxy"], [], [
        Task("cs2-1", "Estimate the number of Uber rides in NYC per day. What is the best starting proxy?", "quiz", "medium", "Uber", options=("Number of cars in NYC", "Population of NYC * % who commute * % who use rideshare", "Number of taxis in NYC", "Area of NYC"), answer_index=1, explanation="A top-down approach using population and frequency of use is standard for consumer tech volume estimation."),
        Task("cs2-2", "If NYC population is 8M, and you assume 25% use rideshare, and they take an average of 4 rides a month, what is the daily volume?", "formula", "easy", "McKinsey", "(8,000,000 * 0.25 * 4) / 30", "", "266,666", "266666"),
        Task("cs2-3", "Estimate the market size for toothbrushes in the US ($). What is the primary replacement cycle assumption?", "quiz", "medium", "Bain", options=("1 month", "3-4 months (dentist recommended)", "1 year", "5 years"), answer_index=1, explanation="Assume 300M people replace a $3 toothbrush every 4 months (3 per year). Market = 300M * 3 * $3 = $2.7B."),
        Task("cs2-4", "How many ping pong balls fit in a school bus? What volume equation do you use for the bus?", "formula", "medium", "Google", "Length * Width * Height", "", "L*W*H", "l*w*h"),
        Task("cs2-5", "When estimating B2B SaaS market size, which is more accurate?", "quiz", "hard", "Salesforce", options=("Top-down based on total global GDP", "Bottom-up: Number of target businesses in the vertical * average contract value (ACV)", "Number of internet users", "Number of computers sold"), answer_index=1, explanation="B2B is best sized bottom-up because the target customer pool (e.g., 'Hospitals with >500 beds') is countable and ACV is standard."),
        Task("cs2-6", "Estimate the weight of a commercial airplane. What is a good structural breakdown?", "quiz", "medium", "Boeing", options=("Wings, Engine, Fuselage, Fuel, Passengers/Cargo", "Metal, Plastic, Glass", "First class, Economy", "Empty weight, gross weight"), answer_index=0, explanation="Deconstructing the object into its physical, heavy sub-components makes estimation structured and logical."),
        Task("cs2-7", "How much revenue does the Golden Gate Bridge toll generate annually? (Assume $8 toll, 100k cars/day).", "formula", "easy", "Goldman Sachs", "8 * 100,000 * 365", "", "$292,000,000", "292000000"),
        Task("cs2-8", "What is the biggest flaw in estimating market size using '1% of a massive market'?", "quiz", "hard", "Sequoia", options=("It's too pessimistic", "It ignores the cost of acquisition and competitive dynamics required to actually capture that 1%", "It's too hard to calculate", "1% is too small"), answer_index=1, explanation="VCs hate the '1% of a $1 Trillion market' pitch because capturing 1% of a fragmented market might cost billions in CAC and face intense competition."),
    ]),

    # ─── Chapter 3: Product Metrics ───
    Lesson("product-metrics", 3, "Product Metrics (LTV/CAC)", ["Activation", "Retention", "Monetization"], [], [
        Task("cs3-1", "A freemium app has 1M MAU. 5% convert to paid. Paid users pay $10/mo. What is the MRR?", "formula", "easy", "Spotify", "1,000,000 * 0.05 * 10", "", "$500,000", "500000"),
        Task("cs3-2", "Which metric best indicates 'Product-Market Fit' for a consumer app?", "quiz", "medium", "A16Z", options=("Total registered users", "Customer Acquisition Cost", "Day 30 Retention Rate flattening out above zero", "Number of app store downloads"), answer_index=2, explanation="A flattening retention curve (the 'smile' or flat tail) proves a core group of users finds continuous value in the product."),
        Task("cs3-3", "What is the 'North Star Metric' for Airbnb?", "quiz", "medium", "Airbnb", options=("App downloads", "Nights booked", "Number of hosts", "Average price per night"), answer_index=1, explanation="Nights booked captures value delivered to both sides of the marketplace (Hosts get money, Guests get accommodation)."),
        Task("cs3-4", "If CAC is $50, and ARPU is $10/mo with 80% gross margin. Churn is 10%. Calculate LTV and the Payback Period.", "quiz", "hard", "Stripe", options=("LTV=$80, Payback=6.25mo", "LTV=$100, Payback=5mo", "LTV=$80, Payback=5mo", "LTV=$100, Payback=6.25mo"), answer_index=0, explanation="LTV = (10*0.8)/0.10 = $80. Payback = 50 / (10*0.8) = 6.25 months."),
        Task("cs3-5", "What is 'Negative Churn' in SaaS?", "quiz", "hard", "Snowflake", options=("When more customers cancel than sign up", "When expansion revenue from existing customers (upsells) exceeds the revenue lost from cancelling customers", "A math error", "When you refund customers"), answer_index=1, explanation="Net Revenue Retention > 100% is called negative churn. It is the holy grail of SaaS because the business grows even if 0 new customers are acquired."),
        Task("cs3-6", "How do you measure the success of a 'Referral Program' feature?", "quiz", "medium", "Robinhood", options=("K-factor (viral coefficient)", "DAU", "NPS", "Bounce rate"), answer_index=0, explanation="K-factor = (Invites sent per user) * (Conversion rate of invites). If K > 1, growth is exponential."),
        Task("cs3-7", "If a social network wants to increase Session Length, what is the trade-off risk?", "quiz", "hard", "Meta", options=("It costs more money", "It might decrease the frequency of sessions (users get exhausted and open the app fewer times per day)", "It increases retention", "It breaks the app"), answer_index=1, explanation="Optimizing for one metric (session length) often cannibalizes another (session frequency)."),
        Task("cs3-8", "What is DAU/MAU a proxy for?", "quiz", "easy", "Facebook", options=("Revenue", "Stickiness/Engagement frequency", "Acquisition", "Churn"), answer_index=1, explanation="If DAU/MAU is 50%, the average user logs in 15 out of 30 days. It measures habit formation."),
    ]),

    # ─── Chapter 4: A/B Testing ───
    Lesson("ab-testing", 4, "A/B Testing & Experimentation", ["Significance", "Sample Size", "Network Effects"], [], [
        Task("cs4-1", "You run an A/B test on a button color. The P-value is 0.08. Your alpha is 0.05. Do you roll out the change?", "quiz", "medium", "Amazon", options=("Yes", "No, it's not statistically significant", "Yes, but only to 50%", "Run it again"), answer_index=1, explanation="P > Alpha means you fail to reject the null hypothesis. The result is likely due to chance."),
        Task("cs4-2", "What is the danger of 'peeking' at an A/B test before the predetermined sample size is reached?", "quiz", "hard", "Netflix", options=("It slows down the database", "It inflates the False Positive rate (Type I error) because variance is high early in tests", "It decreases the P-value", "It creates bias"), answer_index=1, explanation="Peeking and stopping a test early when it 'looks' significant leads to massively inflated false positives."),
        Task("cs4-3", "How do you A/B test a feature in a 2-sided marketplace (e.g., Uber matching algorithm) where treating one user affects another?", "quiz", "hard", "Uber", options=("Standard randomized user split", "Switchback testing (time-based A/B/A/B) or Geo-spatial testing (City A vs City B)", "You can't test it", "Survey the users"), answer_index=1, explanation="Network effects break standard A/B tests (Stable Unit Treatment Value Assumption violation). You must isolate tests by Time or Geography."),
        Task("cs4-4", "If an A/B test increases Conversion by 2% but decreases Average Order Value (AOV) by 3%, what is the final decider?", "quiz", "medium", "Shopify", options=("Conversion wins", "AOV wins", "Revenue Per Visitor (RPV) or Net Profit", "Discard the test"), answer_index=2, explanation="You must look at the overall composite metric (RPV = Conversion * AOV) to determine net business impact."),
        Task("cs4-5", "What is a 'Novelty Effect' in A/B testing?", "quiz", "medium", "Meta", options=("A test that fails", "Users engaging with a new feature just because it's new, but the engagement decays over time", "A feature that only new users see", "A bug in the code"), answer_index=1, explanation="Novelty effects cause temporary spikes in metrics that do not hold long-term. You must run the test long enough for the novelty to wear off."),
        Task("cs4-6", "How do you determine the required Sample Size before running an A/B test?", "quiz", "hard", "Google", options=("Guess 10,000", "Run it for 2 weeks", "Power analysis using Baseline Conversion, Minimum Detectable Effect (MDE), Statistical Power (usually 80%), and Alpha (5%)", "Ask the PM"), answer_index=2, explanation="Sample size is mathematically derived. A smaller MDE requires a vastly larger sample size to detect."),
        Task("cs4-7", "What is a Type II error?", "quiz", "medium", "", options=("False Positive", "False Negative (Failing to detect a real difference)", "Syntax Error", "Calculation error"), answer_index=1, explanation="Type II is failing to reject the null hypothesis when the alternative hypothesis is actually true."),
        Task("cs4-8", "If you run 20 A/B tests simultaneously on the same page, what is the risk?", "quiz", "hard", "Amazon", options=("No risk", "Interaction effects between tests, and a high probability of a False Positive due to multiple testing (requires Bonferroni correction)", "The page will load slowly", "The P-value increases"), answer_index=1, explanation="Testing multiple hypotheses simultaneously increases the chance that at least one result will look significant purely by random chance."),
    ]),

    # ─── Chapter 5: Strategy & Market Entry ───
    Lesson("market-entry", 5, "Strategy & Market Entry", ["Frameworks", "Barriers", "Synergies"], [], [
        Task("cs5-1", "A US fintech wants to enter the UK market. What is the most critical initial framework to apply?", "quiz", "medium", "McKinsey", options=("4 P's", "SWOT", "Market Attractiveness vs. Competitive Advantage / Barriers to Entry", "Agile"), answer_index=2, explanation="Market entry requires sizing the market (Attractiveness), analyzing competitors, and understanding regulatory/capital barriers."),
        Task("cs5-2", "What is a major 'Barrier to Entry' for a new retail bank?", "quiz", "easy", "JPMorgan", options=("Office space", "Banking licenses and capital reserve requirements", "Marketing budget", "Hiring tellers"), answer_index=1, explanation="Regulatory hurdles and immense capital requirements prevent new entrants in traditional banking."),
        Task("cs5-3", "Should an e-commerce giant build its own delivery fleet or outsource to FedEx?", "quiz", "hard", "Amazon", options=("Outsource, it's cheaper", "Build, it's faster", "Analyze the 'Make vs Buy' trade-off: Long-term strategic control and unit cost at scale vs upfront CapEx and core competency", "Buy FedEx"), answer_index=2, explanation="Make vs Buy is a classic strategy case. If scale allows the unit economics of 'Make' to beat 'Buy', and it's core to the customer experience, build it."),
        Task("cs5-4", "A luxury brand is considering lowering prices to increase volume. What is the strategic risk?", "quiz", "medium", "Bain", options=("Brand dilution and alienating the core high-margin customer base", "Running out of inventory", "Making too much money", "Supply chain breakage"), answer_index=0, explanation="Luxury relies on exclusivity. Lowering prices can permanently destroy brand equity."),
        Task("cs5-5", "What is the 'Razor and Blades' business model?", "quiz", "easy", "Gillette", options=("Selling sharp things", "Selling a core product at a loss (razor) to drive high-margin recurring sales of consumables (blades)", "A subscription box", "B2B sales"), answer_index=1, explanation="Printers/ink, PlayStations/games, and Keurigs/pods all use this model."),
        Task("cs5-6", "How does a SaaS company create 'Switching Costs'?", "quiz", "hard", "Salesforce", options=("By raising prices", "By deeply integrating into the client's data infrastructure, training their staff, and customizing workflows so leaving is painfully expensive/disruptive", "By signing 1-month contracts", "By offering discounts"), answer_index=1, explanation="High switching costs create a 'moat' around the business, locking in revenue."),
        Task("cs5-7", "What are Porter's Five Forces used for?", "quiz", "medium", "Harvard", options=("Managing employees", "Analyzing the competitive intensity and profitability of an industry", "Writing code", "Financial auditing"), answer_index=1, explanation="Threat of New Entrants, Threat of Substitutes, Bargaining Power of Customers, Bargaining Power of Suppliers, Competitive Rivalry."),
        Task("cs5-8", "If a market is a 'Commodity', how do companies usually compete?", "quiz", "medium", "", options=("Brand loyalty", "Features", "Strictly on Price and Operational Efficiency", "Customer Service"), answer_index=2, explanation="Commodities have no differentiation. The lowest cost producer wins."),
    ]),

    # ─── Chapter 6: Operations & Supply Chain ───
    Lesson("operations", 6, "Operations & Supply Chain", ["Bottlenecks", "Throughput", "Capacity"], [], [
        Task("cs6-1", "In a factory, Machine A makes 10 parts/hr. Machine B processes 5 parts/hr. Machine C paints 20 parts/hr. What is the throughput of the system?", "quiz", "medium", "Amazon", options=("10 parts/hr", "5 parts/hr", "20 parts/hr", "35 parts/hr"), answer_index=1, explanation="A system's throughput is entirely constrained by its bottleneck. Machine B limits the whole factory to 5 parts/hr."),
        Task("cs6-2", "To double the factory's output to 10 parts/hr, what must you do?", "quiz", "easy", "", options=("Upgrade Machine A", "Upgrade Machine C", "Upgrade Machine B (add a second machine)", "Fire the manager"), answer_index=2, explanation="You only see system-level improvement by elevating the bottleneck."),
        Task("cs6-3", "What is 'Just-In-Time' (JIT) manufacturing?", "quiz", "medium", "Toyota", options=("Working late", "Minimizing inventory by receiving goods only as they are needed in the production process", "Shipping packages fast", "A software methodology"), answer_index=1, explanation="JIT reduces holding costs and waste, but is highly vulnerable to supply chain shocks."),
        Task("cs6-4", "A fulfillment center's 'Dock-to-Stock' time is too high. How do you analyze it?", "quiz", "hard", "Amazon", options=("Fire workers", "Map the process flow, measure time taken at receiving, QA, and put-away, and identify the slowest link", "Buy more trucks", "Ignore it"), answer_index=1, explanation="Process mapping and time-studies are standard operations tools to identify waste/idle time."),
        Task("cs6-5", "What is the 'Bullwhip Effect'?", "quiz", "hard", "McKinsey", options=("A type of conveyor belt", "Small fluctuations in retail demand causing massive, magnified fluctuations in wholesale/manufacturing orders upstream", "An employee motivation tactic", "A pricing strategy"), answer_index=1, explanation="Information asymmetry and ordering delays cause the supply chain to overreact to small demand changes."),
        Task("cs6-6", "How do you calculate Inventory Turnover?", "formula", "medium", "Walmart", "COGS / Average Inventory", "", "COGS/AvgInventory", "cogs"),
        Task("cs6-7", "If a restaurant has 50 seats, average meal time is 60 minutes, and it is open for 4 hours, what is the maximum nightly capacity (covers)?", "formula", "easy", "", "50 * (4/1)", "", "200", "200"),
        Task("cs6-8", "What is 'Shrinkage' in retail operations?", "quiz", "easy", "", options=("Clothes shrinking in the wash", "Loss of inventory due to theft, damage, or administrative errors", "Decreasing market share", "Lowering prices"), answer_index=1, explanation="Shrinkage directly hits the bottom line and requires security and auditing to mitigate."),
    ]),

    # ─── Chapter 7: Financial Case Studies ───
    Lesson("finance-cases", 7, "Financial Case Studies", ["P&L", "Margins", "ROI", "Breakeven"], [], [
        Task("cs7-1", "A company's Revenue went up 20%, but Gross Profit went down 5%. What mathematically MUST have happened?", "quiz", "medium", "Goldman Sachs", options=("Taxes increased", "Fixed costs increased", "Cost of Goods Sold (COGS) increased at a faster rate than Revenue", "They sold fewer units"), answer_index=2, explanation="Gross Profit = Revenue - COGS. If Rev went up but Gross Profit went down, COGS must have spiked massively."),
        Task("cs7-2", "Calculate the Breakeven Volume. Fixed Costs = $100k. Price per unit = $50. Variable Cost per unit = $30.", "formula", "medium", "JPMorgan", "Fixed Costs / Contribution Margin. 100k / (50-30)", "", "5,000 units", "5000"),
        Task("cs7-3", "A startup is deciding between leasing a server for $2k/mo or buying it for $50k (lasts 3 years). Which is financially better (ignoring TVM)?", "formula", "medium", "", "Lease = 2k * 36 = 72k. Buy = 50k. Buy is cheaper by 22k.", "", "Buy", "buy"),
        Task("cs7-4", "What is 'Working Capital'?", "quiz", "easy", "Morgan Stanley", options=("Money in the bank", "Current Assets minus Current Liabilities", "Total equity", "Debt"), answer_index=1, explanation="It measures a company's short-term liquidity and operational efficiency."),
        Task("cs7-5", "If a company extends its 'Days Payable Outstanding' (takes longer to pay suppliers), what happens to its cash flow?", "quiz", "hard", "Bain", options=("Cash flow decreases", "Cash flow improves (increases) in the short term", "No effect", "Profits increase"), answer_index=1, explanation="Delaying cash outflows keeps cash on the balance sheet longer, improving operational liquidity (though it may anger suppliers)."),
        Task("cs7-6", "What is EBITDA a proxy for?", "quiz", "medium", "", options=("Net Income", "Operating Cash Flow / Core Operational Profitability", "Gross Margin", "Debt"), answer_index=1, explanation="Earnings Before Interest, Taxes, Depreciation, and Amortization strips out capital structure and tax environments to show raw operating performance."),
        Task("cs7-7", "A retail chain has high EBITDA but is going bankrupt. How is this possible?", "quiz", "hard", "McKinsey", options=("It's not possible", "Massive debt obligations (Interest) or massive Capital Expenditures (CapEx) are draining all cash", "Taxes are zero", "Their margins are too high"), answer_index=1, explanation="EBITDA ignores Interest and CapEx. If a company is highly leveraged, interest payments will trigger bankruptcy regardless of strong EBITDA."),
        Task("cs7-8", "Calculate the Return on Investment (ROI) if you invest $500k and sell for $750k.", "formula", "easy", "", "(750-500)/500 * 100", "", "50%", "50"),
    ]),

    # ─── Chapter 8: Ethics & Compliance ───
    Lesson("ethics", 8, "Ethics & Compliance", ["Data Privacy", "Conflict of Interest"], [], [
        Task("cs8-1", "You discover a flaw in your pricing algorithm that overcharges customers by $0.01 per transaction. It generates $5M a year. It's too small for customers to notice. What do you do?", "quiz", "easy", "Amazon", options=("Keep it quiet to Deliver Results", "Patch it for the future but don't refund", "Patch it immediately, report to compliance/legal, and initiate a refund protocol", "Take a bonus"), answer_index=2, explanation="Customer Obsession and Earn Trust mandate complete transparency and correction, regardless of the financial hit."),
        Task("cs8-2", "Your manager asks you to pull a list of VIP clients' trading histories to help a friend's startup do market research. What is your response?", "quiz", "medium", "Goldman Sachs", options=("Do it, they are your boss", "Anonymize the data first", "Refuse, cite Data Privacy/GDPR/GLBA policies, and report to compliance if pressured", "Ask for equity in the startup"), answer_index=2, explanation="PII and financial records are strictly regulated. Accessing them for non-business purposes is a fireable/illegal offense."),
        Task("cs8-3", "A vendor offers you courtside NBA tickets while you are evaluating their software for a $1M contract. What do you do?", "quiz", "easy", "", options=("Accept them but remain unbiased", "Decline the tickets, citing company conflict of interest / anti-bribery policies", "Give them to your boss", "Ask for NFL tickets instead"), answer_index=1, explanation="Gifts during procurement create conflicts of interest and violate standard corporate ethics policies."),
        Task("cs8-4", "What is 'Insider Trading'?", "quiz", "medium", "SEC", options=("Trading inside a bank", "Buying/selling a public company's stock based on material, non-public information (MNPI)", "Trading stocks frequently", "Trading your own company's stock during an open window"), answer_index=1, explanation="Using MNPI to trade is a federal crime."),
        Task("cs8-5", "You are designing an AI model for loan approvals. It accurately predicts default risk but disproportionately denies loans to a specific minority group due to historic zip-code data. What must you do?", "quiz", "hard", "Capital One", options=("Deploy it, the math is the math", "Remove 'Race' from the inputs and deploy", "Halt deployment, as this is 'Disparate Impact'. The model is using zip-code as a proxy for race, violating Fair Lending laws. The model must be retrained.", "Lower the threshold for everyone"), answer_index=2, explanation="Algorithmic bias that results in disparate impact violates the Equal Credit Opportunity Act (ECOA), even if race wasn't explicitly inputted."),
        Task("cs8-6", "What does GDPR stand for and what is its core tenet?", "quiz", "medium", "", options=("Global Data Protocol Rules", "General Data Protection Regulation - users own their data and have the 'Right to be Forgotten'", "General Document Protection Rules", "Government Data Privacy Requirements"), answer_index=1, explanation="GDPR requires strict consent for data collection and gives EU citizens the right to have their data deleted."),
        Task("cs8-7", "If a data breach occurs, what is the standard compliance timeline to notify authorities under GDPR?", "quiz", "hard", "", options=("When convenient", "Within 30 days", "Within 72 hours of becoming aware", "Never, if no money was stolen"), answer_index=2, explanation="GDPR mandates a strict 72-hour notification window for data breaches."),
        Task("cs8-8", "What is a 'Chinese Wall' in banking?", "quiz", "medium", "JPMorgan", options=("A firewall software", "An information barrier preventing communication between the investment banking side (which has MNPI) and the trading/research side", "A trading strategy in Asia", "A physical wall in the office"), answer_index=1, explanation="Information barriers are legally required to prevent insider trading within large financial institutions."),
    ]),

    # ─── Chapter 9: M&A Synergy Analysis (NEW) ───
    Lesson("ma-synergy", 9, "M&A Synergy Analysis", ["Accretive", "Dilutive", "Integration"], [], [
        Task("cs9-1", "Disney acquired Pixar. Which of the following is a 'Revenue Synergy'?", "quiz", "medium", "McKinsey", options=("Firing duplicate HR staff", "Combining IT systems", "Selling Pixar toys in Disney theme parks", "Closing a Pixar office"), answer_index=2, explanation="Revenue synergies involve cross-selling or using distribution networks to generate *new* revenue. The others are Cost synergies."),
        Task("cs9-2", "If Acquirer A (P/E of 20) buys Target B (P/E of 10) using purely stock, is the deal mathematically Accretive or Dilutive to A's EPS?", "quiz", "hard", "Goldman Sachs", options=("Accretive", "Dilutive", "Neutral", "Cannot determine"), answer_index=0, explanation="A high P/E company buying a low P/E company with stock is generally accretive because they are using 'expensive' currency to buy 'cheap' earnings, instantly boosting blended EPS."),
        Task("cs9-3", "What is the biggest risk in realizing Cost Synergies post-merger?", "quiz", "medium", "Bain", options=("The stock market crashing", "Cultural clash and failure to integrate IT systems, leading to delayed or failed cost reductions", "Competitors lowering prices", "Revenue drops"), answer_index=1, explanation="Integration execution is the #1 reason M&A deals fail to deliver modeled synergies."),
        Task("cs9-4", "Company X buys Company Y for $100M. Company Y's hard assets are worth $40M. What is the remaining $60M recorded as on the balance sheet?", "quiz", "hard", "Morgan Stanley", options=("Debt", "Revenue", "Goodwill (Intangible Asset)", "Cash"), answer_index=2, explanation="The premium paid over the fair market value of net assets is recorded as Goodwill."),
        Task("cs9-5", "In a 'Build vs Buy' decision, why might a tech giant 'Buy' a startup for $1B instead of building the tech themselves for $100M?", "quiz", "hard", "Google", options=("They have too much cash", "Time-to-market. Building takes 3 years, during which they lose market share. Buying gets them the tech, the talent, and the user base instantly.", "To look good to Wall Street", "It's a tax write-off"), answer_index=1, explanation="In tech, speed is a massive competitive moat. Acquiring an established player eliminates development time and execution risk."),
        Task("cs9-6", "What is a 'Horizontal Integration'?", "quiz", "easy", "", options=("Buying a supplier", "Buying a competitor in the same industry/stage of production", "Buying a customer", "Expanding into a new country"), answer_index=1, explanation="E.g., Facebook buying Instagram. Vertical integration is buying the supply chain (e.g., Apple buying a chip manufacturer)."),
        Task("cs9-7", "Calculate the Net Synergies. Cost savings = $20M/yr. Revenue cross-sell = $10M/yr. Integration costs = $50M (Year 1 only). What is the Year 1 net impact?", "formula", "medium", "", "20 + 10 - 50", "", "-$20M", "-20"),
        Task("cs9-8", "Why do investment bankers apply a 'Discount Rate' when valuing future cash flows of a target company?", "quiz", "medium", "JPMorgan", options=("To account for inflation", "To account for the Time Value of Money and Risk (WACC)", "Because buyers want a discount", "To lower taxes"), answer_index=1, explanation="Future cash flows are inherently risky and worth less than cash today. The discount rate (often WACC) reflects this risk."),
    ]),

    # ─── Chapter 10: Go-to-Market Strategy (NEW) ───
    Lesson("gtm-strategy", 10, "Go-to-Market Strategy", ["Pricing", "Distribution", "Positioning"], [], [
        Task("cs10-1", "A SaaS startup is launching a new AI tool. They have two pricing options: $10/mo for everyone, or Free with a $50/mo Enterprise tier. The latter is an example of:", "quiz", "easy", "Stripe", options=("Skimming", "Penetration Pricing", "Freemium / Product-Led Growth (PLG)", "Value-based pricing"), answer_index=2, explanation="Freemium reduces the barrier to entry to zero, relying on massive user adoption to eventually upsell a small percentage to Enterprise."),
        Task("cs10-2", "When defining a Target Audience, what is a 'Buyer Persona' vs a 'User Persona' in B2B?", "quiz", "medium", "Salesforce", options=("They are the same", "The Buyer writes the check (e.g., CFO/CIO), the User operates the software (e.g., Analyst). GTM must address both.", "The Buyer is retail, the User is corporate", "The Buyer is older"), answer_index=1, explanation="In B2B, the person using the tool rarely has purchasing authority. Your marketing must convince the User of the utility, and the Buyer of the ROI."),
        Task("cs10-3", "What is a 'Channel Partner' strategy?", "quiz", "medium", "Microsoft", options=("Running TV ads", "Using third-party companies (e.g., agencies, consultants) to sell and implement your product for a commission", "Selling direct to consumer", "Opening a retail store"), answer_index=1, explanation="Microsoft and Salesforce rely heavily on channel partners to scale distribution globally without hiring thousands of direct sales reps."),
        Task("cs10-4", "A new luxury electric vehicle is launching. Should they use TV commercials or targeted events at high-net-worth locations?", "quiz", "easy", "Tesla", options=("TV commercials (broad reach)", "Targeted events (niche, high conversion)", "Radio", "Billboards"), answer_index=1, explanation="Mass marketing is inefficient for high-ticket luxury items. Targeted, experiential GTM strategies yield better ROI."),
        Task("cs10-5", "What is 'Cannibalization' in a GTM context?", "quiz", "medium", "Apple", options=("Competitors stealing your market share", "Your new product stealing sales from your existing, older product", "Failing to launch on time", "Pricing too high"), answer_index=1, explanation="E.g., The iPhone cannibalized iPod sales. Apple's philosophy: 'If you don't cannibalize yourself, someone else will.'"),
        Task("cs10-6", "How do you calculate Customer Acquisition Cost (CAC) for a specific marketing channel?", "formula", "easy", "", "Total Spend on Channel / Number of Customers Acquired from Channel", "", "Spend / Customers", "spend/"),
        Task("cs10-7", "What is 'Positioning'?", "quiz", "hard", "McKinsey", options=("Where the product is placed on a store shelf", "How the product is designed to be perceived in the minds of the target market relative to competitors", "The geographic location of the HQ", "The price of the product"), answer_index=1, explanation="Positioning is psychological real estate. (e.g., Volvo = Safety, Tesla = Innovation)."),
        Task("cs10-8", "If a product is highly complex and requires integration, which sales motion is best?", "quiz", "medium", "Snowflake", options=("Self-serve checkout online", "Inbound content marketing", "High-touch Enterprise Direct Sales", "Social media influencers"), answer_index=2, explanation="Complex, high-ACV products require Solution Architects and Enterprise Account Executives to guide the buyer through security and integration hurdles."),
    ]),

    # ─── Chapter 11: Competitor War Gaming (NEW) ───
    Lesson("war-gaming", 11, "Competitor War Gaming", ["Price Wars", "Defensive Strategy", "Moats"], [], [
        Task("cs11-1", "Your main competitor suddenly drops their price by 30%. What is your FIRST strategic move?", "quiz", "hard", "Bain", options=("Immediately drop your price by 30% to match", "Do nothing", "Analyze the competitor's unit economics to determine if it's a permanent structural advantage or a temporary loss-leader tactic to buy market share", "Sue them"), answer_index=2, explanation="Never react blindly. If they have a new structural cost advantage, you must innovate. If they are burning VC cash to buy share, you might wait them out or highlight your premium value."),
        Task("cs11-2", "To defend against a cheaper competitor, you launch a 'Fighter Brand' (a stripped-down, cheaper version of your product under a different name). What is the primary risk?", "quiz", "medium", "McKinsey", options=("It's illegal", "It distracts management and might cannibalize your premium brand if customers figure it out", "It increases overall market size", "It raises your prices"), answer_index=1, explanation="Fighter brands (like Intel's Celeron) protect the premium brand's margins but risk brand dilution and operational bloat."),
        Task("cs11-3", "What is a 'Network Effect' moat?", "quiz", "medium", "Meta", options=("Having a lot of servers", "A product becomes exponentially more valuable to existing users as new users join (e.g., Facebook, Uber)", "A patent", "High switching costs"), answer_index=1, explanation="Network effects are the strongest defensive moat in tech. A new social network with 0 users is useless, making it nearly impossible to displace an incumbent."),
        Task("cs11-4", "Competitor A locks their users into 3-year contracts. How do you attack their customer base?", "quiz", "hard", "Salesforce", options=("Wait 3 years", "Offer to pay their contract break fees or offer your software free for the remainder of their contract to incentivize switching now", "Lower your price", "Build more features"), answer_index=1, explanation="Aggressive challengers often buy out contracts or offer 'bridge' discounts to overcome the contractual switching cost moat."),
        Task("cs11-5", "What is a 'Blue Ocean' strategy?", "quiz", "easy", "", options=("Competing aggressively on price in a crowded market", "Creating a completely new, uncontested market space, making the competition irrelevant", "Operating in the shipping industry", "Merging with a rival"), answer_index=1, explanation="Instead of fighting a bloody 'Red Ocean' price war, you innovate to create a new category (e.g., Cirque du Soleil reinventing the circus)."),
        Task("cs11-6", "If your competitor has massive Economies of Scale, how do you compete?", "quiz", "hard", "BCG", options=("Compete on price", "Outspend them on marketing", "Niche down: Focus on a hyper-specific, underserved customer segment and offer a highly tailored, premium product they are too big to care about", "Give up"), answer_index=2, explanation="You cannot beat a scaled incumbent on price. You must compete on differentiation and niche focus."),
        Task("cs11-7", "What is 'First-Mover Advantage'?", "quiz", "medium", "", options=("Being the first to arrive at work", "Gaining brand recognition, locking up suppliers, and building switching costs before competitors enter", "Having the fastest website", "Being the first to go bankrupt"), answer_index=1, explanation="Being first allows you to define the category, though 'Fast Followers' often learn from the first mover's mistakes."),
        Task("cs11-8", "A rival tech company is stealing your top engineers. What is the best defensive response?", "quiz", "medium", "Google", options=("Sue the rival", "Counter-offer every engineer with more money", "Fix your internal culture, offer aggressive retention equity (Golden Handcuffs), and ensure engineers have clear growth paths", "Fire the engineers before they leave"), answer_index=2, explanation="Money is a temporary fix. Retention requires structural alignment (equity vesting) and cultural improvements."),
    ]),

    # ─── Chapter 12: Vendor Negotiation (NEW) ───
    Lesson("vendor-negotiation", 12, "Vendor Negotiation & Procurement", ["BATNA", "SLA", "Leverage"], [], [
        Task("cs12-1", "You are negotiating a multi-million dollar cloud hosting contract. What does BATNA stand for?", "quiz", "easy", "Harvard", options=("Best Alternative To a Negotiated Agreement", "Buy And Trade Network Assets", "Bilateral Agreement Terms Negotiated Annually", "Bank And Trust National Association"), answer_index=0, explanation="Your BATNA is your walk-away option. If your BATNA is strong (e.g., you can easily switch to AWS), you have massive negotiation leverage."),
        Task("cs12-2", "A vendor refuses to lower their SaaS pricing per user. What are alternate levers you can negotiate to improve the deal value?", "quiz", "hard", "Capital One", options=("Give up and pay", "Negotiate longer payment terms (Net 90), free implementation, extended SLA penalties, or a cap on future price increases", "Buy fewer licenses than you need", "Insult the vendor"), answer_index=1, explanation="Negotiation is multi-dimensional. If price is fixed, attack terms, support, training, and future caps."),
        Task("cs12-3", "What is a 'Most Favored Nation' (MFN) clause in a vendor contract?", "quiz", "hard", "Amazon", options=("The vendor must be located in the US", "A guarantee that the vendor will not offer a better price or terms to any other customer; if they do, you automatically get that better price", "A political agreement", "A tax loophole"), answer_index=1, explanation="Large enterprises use MFN clauses to guarantee they are always getting the absolute floor price in the market."),
        Task("cs12-4", "Why would a company prefer a 3-year contract with a vendor over a 1-year contract?", "quiz", "medium", "", options=("It's more flexible", "To lock in a steep discount and protect against annual price hikes", "To increase administrative work", "There is no reason"), answer_index=1, explanation="Term length is traded for discount depth and price predictability."),
        Task("cs12-5", "What is an SLA (Service Level Agreement) penalty?", "quiz", "medium", "Stripe", options=("A fee you pay the vendor", "A financial credit the vendor must issue to you if their system downtime exceeds the agreed threshold (e.g., 99.9% uptime)", "A government fine", "A late payment fee"), answer_index=1, explanation="SLAs protect the buyer from operational failure by hitting the vendor's wallet if they fail to deliver reliability."),
        Task("cs12-6", "You are heavily reliant on a single microchip supplier (Single Point of Failure). How do you mitigate this risk?", "quiz", "easy", "Apple", options=("Sign a longer contract with them", "Dual-sourcing: qualify and onboard a secondary supplier, even if slightly more expensive, to ensure supply chain resilience and create pricing leverage", "Buy all their inventory", "Stop using microchips"), answer_index=1, explanation="Dual-sourcing creates competition and prevents the supplier from holding you hostage during shortages or negotiations."),
        Task("cs12-7", "In procurement, what is a Request for Proposal (RFP)?", "quiz", "medium", "", options=("A marriage proposal", "A formal document soliciting bids from multiple vendors to create competitive tension before buying", "A legal contract", "A feature request"), answer_index=1, explanation="RFPs force vendors to outline their capabilities and pricing formally, allowing the buyer to compare apples to apples."),
        Task("cs12-8", "The vendor offers a 10% discount if you pay the $1M annual fee entirely upfront instead of monthly. Assuming your company's Cost of Capital (WACC) is 5%, should you do it?", "quiz", "hard", "JPMorgan", options=("Yes", "No", "It's exactly break-even", "Cannot calculate"), answer_index=0, explanation="The return on paying upfront (10% savings) is strictly greater than your cost of capital (5%). Financially, it is highly advantageous to take the discount."),
    ]),
]


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
    
    def norm(s): return str(s or "").strip().lower().replace(" ","").replace("$","").replace("'","").replace(",","").replace("k","000").replace("m","000000").replace("b","000000000")

    if t.kind == "quiz":
        correct = answer == t.answer_index
        return {"correct":correct,"message":"Correct!" if correct else "Not quite.","explanation":t.explanation,"expectedIndex":t.answer_index}
    
    user = norm(answer)
    expected = norm(t.expected)
    solution = norm(t.solution)
    
    correct = expected in user or (solution in user if solution else False) or user == expected
    return {"correct":correct, "message":"Correct!" if correct else f"Not quite. Expected logic: {t.expected}", "explanation":t.explanation, "solution":t.solution}
