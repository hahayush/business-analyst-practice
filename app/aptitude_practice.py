"""Ultimate Business Aptitude module — Deep, extensive Quant and Logic practice for top tier firms."""
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
    # ─── Chapter 1: Expected Value & Probability Models ───
    Lesson("quant-expected-value", 1, "Expected Value & Probability", ["Bayes Theorem", "EV", "Markov"], [], [
        Task("apt1-1", "A high-frequency trading algorithm has a 60% chance to make $10k and a 40% chance to lose $5k. What is the Expected Value (EV) of one trade?", "formula", "medium", "Goldman Sachs", "EV = (Prob_Win * Amount_Win) + (Prob_Loss * Amount_Loss)", "", "$4,000", "4000"),
        Task("apt1-2", "1% of transactions are fraudulent. Your ML model flags 99% of fraud, but has a 5% false positive rate on legitimate transactions. If a transaction is flagged, what is the probability it is actually fraud?", "quiz", "hard", "Stripe", options=("99%", "50%", "16.6%", "5%"), answer_index=2, explanation="Bayes Theorem: Out of 10,000 txns, 100 are fraud (99 flagged). 9,900 are legit (495 flagged). Total flagged = 594. True fraud = 99/594 = 16.6%."),
        Task("apt1-3", "You flip a fair coin until you get tails. What is the expected number of total flips?", "quiz", "hard", "Jane Street", options=("1", "2", "3", "Infinity"), answer_index=1, explanation="The expected value of a geometric distribution with p=0.5 is 1/p = 2 flips."),
        Task("apt1-4", "A project has a 30% chance of success generating $1M, and a 70% chance of failure costing $200k. What is the project's EV?", "formula", "medium", "McKinsey", "EV = (0.3 * 1,000,000) - (0.7 * 200,000)", "", "$160,000", "160000"),
        Task("apt1-5", "In a city, 40% of people use iOS, 60% Android. 80% of iOS users buy apps, while only 30% of Android users do. If a random app buyer is selected, what is the probability they use iOS?", "quiz", "hard", "Google", options=("64%", "32%", "40%", "80%"), answer_index=0, explanation="Total buyers = (0.4 * 0.8) + (0.6 * 0.3) = 0.32 + 0.18 = 0.50. Prob(iOS | Buyer) = 0.32 / 0.50 = 64%."),
        Task("apt1-6", "You play a game where you roll a 6-sided die. If you roll a 6, you win $30. If you roll a 1, you lose $12. Otherwise, you win $0. What is your EV?", "formula", "medium", "Citadel", "(1/6 * 30) - (1/6 * 12)", "", "$3", "3"),
        Task("apt1-7", "A machine produces defective parts 2% of the time. If you randomly select 3 parts, what is the probability that exactly 1 is defective? (Round to 3 decimal places)", "formula", "hard", "Amazon", "Binomial: 3C1 * (0.02)^1 * (0.98)^2", "", "0.058", "0.058"),
        Task("apt1-8", "There are 5 red balls and 5 blue balls in a bag. If you draw 2 without replacement, what is the probability they are the same color?", "quiz", "hard", "JPMorgan", options=("50%", "44.4%", "25%", "22.2%"), answer_index=1, explanation="P(Both Red) = (5/10)*(4/9) = 20/90. P(Both Blue) = 20/90. Total = 40/90 = 4/9 = 44.4%."),
    ]),

    # ─── Chapter 2: SaaS Unit Economics ───
    Lesson("quant-unit-econ", 2, "SaaS Unit Economics", ["LTV", "CAC", "Payback Period", "Churn"], [], [
        Task("apt2-1", "A B2B SaaS customer pays $200/month. The monthly churn rate is 2.5%. Gross margin is 80%. Calculate the Customer Lifetime Value (LTV).", "formula", "medium", "Plaid", "LTV = (ARPU * Gross Margin) / Churn Rate. (200 * 0.80) / 0.025", "", "$6,400", "6400"),
        Task("apt2-2", "If the Cost to Acquire a Customer (CAC) is $1,600 for the customer in the previous question, what is the Payback Period in months?", "formula", "medium", "Square", "Payback Period = CAC / (ARPU * Gross Margin). 1600 / 160", "", "10 months", "10"),
        Task("apt2-3", "Your marketing team wants to increase CAC by 50% to acquire 'premium' customers whose churn rate is half (1.25%). Does the overall LTV:CAC ratio improve or worsen?", "quiz", "hard", "Stripe", options=("Improves", "Worsens", "Stays exactly the same", "Cannot calculate"), answer_index=0, explanation="Old LTV/CAC: 6400/1600 = 4x. New LTV: (160/0.0125) = 12800. New CAC: 1600 * 1.5 = 2400. New LTV/CAC: 12800/2400 = 5.3x. It improves."),
        Task("apt2-4", "A company has an ARPU of $50, 90% Gross Margin, and 5% monthly churn. What is the maximum CAC they can afford if they require a 3:1 LTV:CAC ratio?", "formula", "hard", "Shopify", "LTV = (50*0.9)/0.05 = $900. Max CAC = 900/3 = 300.", "", "$300", "300"),
        Task("apt2-5", "What happens to the Payback Period if Gross Margin drops from 80% to 40% but CAC and ARPU remain constant?", "quiz", "medium", "", options=("It halves", "It doubles", "It stays the same", "It squares"), answer_index=1, explanation="Payback = CAC / (ARPU * GM). If GM halves, the denominator halves, making the payback period twice as long."),
        Task("apt2-6", "If annual net revenue retention (NRR) is 120%, what does this imply about the existing customer cohort?", "quiz", "medium", "Snowflake", options=("They are churning faster than they upgrade", "Upgrades and expansions from existing customers exceed the revenue lost to churn", "The company acquired 20% more new customers", "Total revenue grew by 20%"), answer_index=1, explanation="NRR > 100% means the revenue expansion from retained customers is greater than the revenue lost from churned or downgraded customers."),
        Task("apt2-7", "Calculate Monthly Recurring Revenue (MRR) for 500 users on a $20/mo plan and 100 users on a $120/year plan.", "formula", "easy", "", "MRR = (500*20) + (100 * 120/12)", "", "$11,000", "11000"),
        Task("apt2-8", "If LTV is $500, CAC is $100, and Marginal Cost of servicing the user is $200 over their lifetime, what is the true LTV:CAC if LTV didn't previously account for marginal cost?", "formula", "hard", "Amazon", "True LTV = 500 - 200 = 300. Ratio = 300 / 100.", "", "3", "3"),
    ]),

    # ─── Chapter 3: Financial Mathematics & CAGR ───
    Lesson("quant-finance", 3, "Financial Math & Compounding", ["CAGR", "Rule of 72", "NPV"], [], [
        Task("apt3-1", "A startup's revenue grew from $10M to $40M over exactly 4 years. What is the Compound Annual Growth Rate (CAGR)?", "quiz", "medium", "JPMorgan", options=("25%", "33%", "41.4%", "75%"), answer_index=2, explanation="CAGR = (Ending/Beginning)^(1/t) - 1. (40/10)^(1/4) - 1 = 4^(0.25) - 1 = 1.414 - 1 = 41.4%."),
        Task("apt3-2", "An investment fund promises a steady 12% annual return. Using the Rule of 72, approximately how long will it take for your investment to double?", "formula", "easy", "Morgan Stanley", "Years to double ≈ 72 / Interest Rate", "", "6 years", "6"),
        Task("apt3-3", "If a project requires a $100k initial investment and yields $30k per year for 4 years, what is its simple ROI?", "formula", "medium", "McKinsey", "Total Return = 120k. Net Profit = 20k. ROI = 20k/100k.", "", "20%", "20"),
        Task("apt3-4", "Which concept explains why receiving $10,000 today is more valuable than receiving $10,000 five years from now?", "quiz", "easy", "Goldman Sachs", options=("Inflation", "Time Value of Money (TVM)", "Opportunity Cost", "All of the above"), answer_index=3, explanation="TVM relies on the fact that money today can be invested to earn interest (Opportunity Cost) and inflation degrades purchasing power."),
        Task("apt3-5", "You borrow $5,000 at 10% compound interest annually. How much do you owe after 2 years?", "formula", "medium", "", "5000 * (1.10)^2 = 5000 * 1.21", "", "$6,050", "6050"),
        Task("apt3-6", "Company A has a P/E ratio of 15. If its Earnings Per Share (EPS) is $4, what is its stock price?", "formula", "easy", "", "Price = P/E * EPS", "", "$60", "60"),
        Task("apt3-7", "An asset depreciates by 20% each year. What percentage of its original value remains after 3 years?", "formula", "hard", "", "0.80 * 0.80 * 0.80 = 0.512", "", "51.2%", "51.2"),
        Task("apt3-8", "If you invest $1,000 at 5% simple interest for 10 years, and $1,000 at 4% compound interest for 10 years, which yields more total money?", "quiz", "hard", "Bain", options=("Simple Interest", "Compound Interest", "They yield the same", "Cannot be calculated"), answer_index=1, explanation="Simple: 1000 + (1000*0.05*10) = 1500. Compound: 1000 * (1.04)^10 = 1000 * 1.480 = 1480. Wait. 1500 > 1480. Therefore, Simple Interest yields more in this specific scenario!"),
    ]),

    # ─── Chapter 4: Algorithmic Logic & Scaling ───
    Lesson("quant-algorithms", 4, "Algorithmic Logic & Scaling", ["Throughput", "Concurrency", "Optimization"], [], [
        Task("apt4-1", "3 cloud servers can process 15,000 API requests in 5 seconds. Assuming linear scaling, how long will it take 5 servers to process 50,000 requests?", "formula", "hard", "AWS", "1 server processes 5,000 reqs in 5s (1,000 req/s). 5 servers = 5,000 req/s. 50,000 / 5,000 = 10s.", "", "10s", "10"),
        Task("apt4-2", "You have a 100-story building and 2 identical glass drops. You need to find the highest floor from which a drop won't break. What is the optimal maximum number of drops needed in the worst-case scenario?", "quiz", "hard", "Google", options=("50", "20", "14", "10"), answer_index=2, explanation="Classic DP puzzle. You step by n, then n-1, then n-2... solving n(n+1)/2 >= 100 yields n=14. The optimal maximum drops is 14."),
        Task("apt4-3", "A network cache hits 80% of the time, taking 1ms. If it misses, it takes 10ms to fetch from the DB. What is the average latency?", "formula", "medium", "Stripe", "(0.8 * 1) + (0.2 * 10) = 0.8 + 2.0", "", "2.8ms", "2.8"),
        Task("apt4-4", "You have 8 balls, one is slightly heavier. You have a balance scale. What is the minimum number of weighings to guarantee finding the heavy ball?", "quiz", "hard", "Jane Street", options=("2", "3", "4", "7"), answer_index=0, explanation="Weigh 3 vs 3. If equal, weigh the remaining 2 (total 2 weighings). If unequal, take the heavier 3, weigh 1 vs 1. If equal, it's the 3rd. (total 2 weighings). Minimum is 2."),
        Task("apt4-5", "An algorithm runs in O(N^2) time. If processing 1,000 items takes 2 seconds, roughly how long will 3,000 items take?", "formula", "medium", "Meta", "Input size grew by 3x. Time grows by 3^2 = 9x. 2 * 9 = 18s.", "", "18s", "18"),
        Task("apt4-6", "A pipe can fill a pool in A hours. Another pipe can empty it in B hours (where B > A). If both are open, how long to fill the pool?", "quiz", "medium", "", options=("(A*B)/(A+B)", "(A*B)/(B-A)", "(A+B)/(A*B)", "A-B"), answer_index=1, explanation="Rate = 1/A - 1/B = (B-A)/AB. Time is the reciprocal: AB/(B-A)."),
        Task("apt4-7", "If it takes 5 machines 5 minutes to make 5 widgets, how long does it take 100 machines to make 100 widgets?", "formula", "easy", "Amazon", "1 machine makes 1 widget in 5 minutes.", "", "5 minutes", "5"),
        Task("apt4-8", "A lily pad doubles in size every day. If it takes 30 days to cover the entire pond, how many days did it take to cover half the pond?", "formula", "easy", "McKinsey", "If it doubles every day, it was half the size the day before.", "", "29 days", "29"),
    ]),

    # ─── Chapter 5: Fermi Problems (Market Sizing) ───
    Lesson("quant-fermi", 5, "Fermi Problems & Estimation", ["Top-down", "Bottlenecks", "Market Sizing"], [], [
        Task("apt5-1", "When estimating the total daily revenue of a single busy Starbucks in NYC, what is the primary constraining variable (bottleneck)?", "quiz", "medium", "McKinsey", options=("The population of NYC", "The physical size of the store", "The speed of the espresso machine / barista throughput during peak hours", "The price of a latte"), answer_index=2, explanation="In retail estimation, peak throughput (transactions per hour) limits total daily volume much more than total city population or price."),
        Task("apt5-2", "Estimate the number of commercial airplanes in the air over the US at any given moment. Which approach is most robust?", "quiz", "medium", "Bain", options=("Bottom-up: (Total airports * planes taking off per hour * avg flight duration)", "Top-down: Population of US * % of people flying / plane capacity", "Both are equally robust", "Neither works"), answer_index=0, explanation="Bottom-up relies on supply-side physics (airports, runways) which is easier to estimate accurately than top-down demand assumptions for a single moment in time."),
        Task("apt5-3", "If estimating the number of ping pong balls that can fit in a Boeing 747, what is the most critical assumption?", "quiz", "hard", "Google", options=("The weight of a ping pong ball", "The volume of a Boeing 747 minus the seats/internal structures", "The packing fraction of spheres in a volume", "Both B and C"), answer_index=3, explanation="You need the usable internal volume (B) and the packing density coefficient for spheres (~0.64 to 0.74) to get an accurate estimate (C)."),
        Task("apt5-4", "A town has 100,000 people. Assuming average lifespan is 80 years, how many people are born each year (steady state)?", "formula", "medium", "BCG", "100,000 / 80", "", "1,250", "1250"),
        Task("apt5-5", "To estimate the number of smartphones sold in the US per year, what is the best formula?", "quiz", "medium", "", options=("Population / Replacement Rate (in years)", "Population * Average Price", "Number of Apple stores * phones per store", "Population / 365"), answer_index=0, explanation="If there are 300M people with phones, and they replace them every 3 years, sales = 300M / 3 = 100M/year."),
        Task("apt5-6", "Estimate the annual revenue of a hair salon. What is a reasonable constraint?", "quiz", "easy", "", options=("Number of chairs * hours open * utilization % * avg price", "Total hair in the city", "Number of scissors", "Weather"), answer_index=0, explanation="Capacity and utilization drive service business revenue."),
        Task("apt5-7", "If a car travels 60 miles at 30mph, and 60 miles back at 60mph, what is the average speed?", "formula", "hard", "Citadel", "Total Distance = 120m. Time1 = 2h. Time2 = 1h. Total Time = 3h. Avg = 120/3 = 40mph. (NOT 45mph).", "", "40mph", "40"),
        Task("apt5-8", "In a city of 1M households, if 20% order pizza once a month, how many pizzas are ordered annually?", "formula", "medium", "", "1,000,000 * 0.20 * 12", "", "2,400,000", "2400000"),
    ]),

    # ─── Chapter 6: Data Sufficiency (GMAT Level) ───
    Lesson("quant-data-suff", 6, "GMAT-Level Data Sufficiency", ["Logical bounds", "Sufficient vs Insufficient"], [], [
        Task("apt6-1", "Is the gross profit margin of Product A greater than Product B? (1) The retail price of A is 20% higher than B. (2) The COGS of A is 10% lower than B.", "quiz", "hard", "Capital One", options=("Statement 1 alone is sufficient", "Statement 2 alone is sufficient", "Both statements together are sufficient", "Data is insufficient"), answer_index=2, explanation="Margin depends on both Price and Cost. Since A has a higher price AND lower cost, its profit is absolutely higher than B. Both together are required."),
        Task("apt6-2", "What is the company's total annual revenue? (1) B2B revenue accounts for exactly 60% of total revenue. (2) B2C revenue is exactly $4 Million.", "quiz", "medium", "Bloomberg", options=("Statement 1 is sufficient", "Statement 2 is sufficient", "Both together are sufficient", "Data is insufficient"), answer_index=3, explanation="Wait! What if there is a B2G (Government) revenue stream? Unless we know B2B and B2C are the ONLY streams, data is insufficient. (Classic trap)."),
        Task("apt6-3", "Is integer x prime? (1) x is odd. (2) x < 10 and x > 5.", "quiz", "hard", "McKinsey", options=("Statement 1 is sufficient", "Statement 2 is sufficient", "Both together are sufficient", "Data is insufficient"), answer_index=3, explanation="From (2) x can be 6,7,8,9. From (1) x can be 7 or 9. 7 is prime, 9 is not. Insufficient."),
        Task("apt6-4", "What is the value of x? (1) x^2 = 36. (2) x is less than 0.", "quiz", "medium", "", options=("Statement 1 alone", "Statement 2 alone", "Both together", "Insufficient"), answer_index=2, explanation="1 gives 6 or -6. 2 restricts to -6. Both needed."),
        Task("apt6-5", "Is x > y? (1) x + y > 0. (2) x - y > 0.", "quiz", "hard", "", options=("Statement 1 alone", "Statement 2 alone", "Both together", "Insufficient"), answer_index=1, explanation="Statement 2 implies x > y directly. Statement 1 is useless for this."),
        Task("apt6-6", "How many employees does the company have? (1) The ratio of men to women is 3:2. (2) There are 50 more men than women.", "quiz", "medium", "Bain", options=("Statement 1 alone", "Statement 2 alone", "Both together", "Insufficient"), answer_index=2, explanation="3x - 2x = 50 => x = 50. Total = 5x = 250. Both needed."),
        Task("apt6-7", "What is the average age of a team? (1) The youngest is 20 and oldest is 40. (2) There are 5 members.", "quiz", "easy", "", options=("Statement 1 alone", "Statement 2 alone", "Both together", "Insufficient"), answer_index=3, explanation="We don't know the ages of the other 3 members. Insufficient."),
        Task("apt6-8", "Is the triangle a right triangle? (1) Sides are in ratio 3:4:5. (2) One angle is 90 degrees.", "quiz", "easy", "", options=("1 alone is sufficient", "2 alone is sufficient", "Each alone is sufficient", "Both needed"), answer_index=2, explanation="Both independently prove it is a right triangle."),
    ]),

    # ─── Chapter 7: Statistical & Risk Interpretation ───
    Lesson("quant-stats", 7, "Statistics & Risk Analysis", ["Standard Deviation", "Sharpe Ratio", "Variance"], [], [
        Task("apt7-1", "Portfolio A and B both have an Expected Return of 10%. The Risk-Free rate is 2%. Portfolio A has a Standard Deviation of 8%, while B is 16%. Which portfolio has the higher Sharpe Ratio?", "quiz", "medium", "Bridgewater", options=("Portfolio A", "Portfolio B", "They are equal", "Cannot be calculated"), answer_index=0, explanation="Sharpe Ratio = (Return - Risk-Free) / StdDev. A: (10-2)/8 = 1.0. B: (10-2)/16 = 0.5. Portfolio A offers better risk-adjusted returns."),
        Task("apt7-2", "A distribution of customer transaction values is highly 'Right-Skewed'. Which of the following is true?", "quiz", "medium", "Stripe", options=("Mean < Median", "Mean > Median", "Mean = Median", "Standard Deviation is zero"), answer_index=1, explanation="Right-skew (positive skew) means there is a long tail of very high values (whales), which drags the Mean higher than the Median."),
        Task("apt7-3", "If the variance of a dataset is 144, what is the standard deviation?", "formula", "easy", "", "Sqrt of 144", "", "12", "12"),
        Task("apt7-4", "In a normal distribution, approximately what percentage of data falls within 2 standard deviations of the mean?", "quiz", "medium", "Goldman Sachs", options=("68%", "95%", "99.7%", "50%"), answer_index=1, explanation="The empirical rule states 68% within 1 SD, 95% within 2 SDs, and 99.7% within 3 SDs."),
        Task("apt7-5", "You measure the correlation between Ice Cream sales and Shark Attacks and find an R-squared of 0.85. Does this mean ice cream causes shark attacks?", "quiz", "easy", "", options=("Yes", "No, it's a confounding variable (Summer)", "No, R-squared is too low", "Yes, correlation is causation"), answer_index=1, explanation="Correlation does not imply causation. Both are driven by a third variable: warm summer weather."),
        Task("apt7-6", "What is the primary difference between a population standard deviation and a sample standard deviation formula?", "quiz", "hard", "", options=("Sample divides by N, Population by N-1", "Sample divides by N-1, Population by N", "No difference", "Sample uses Median instead of Mean"), answer_index=1, explanation="Bessel's correction uses N-1 for samples to correct bias in the estimation of the population variance."),
        Task("apt7-7", "If the P-value of an A/B test is 0.03, and your alpha threshold is 0.05, what is the conclusion?", "quiz", "medium", "Amazon", options=("Accept Null Hypothesis", "Reject Null Hypothesis", "Inconclusive", "Run test longer"), answer_index=1, explanation="Since P (0.03) < Alpha (0.05), the result is statistically significant. We reject the null hypothesis."),
        Task("apt7-8", "An ML model has high precision but low recall. What does this mean?", "quiz", "hard", "Google", options=("It misses many true cases, but when it flags something, it's usually correct", "It flags everything, so it catches all true cases but has many false alarms", "It is perfectly accurate", "It is entirely useless"), answer_index=0, explanation="Low recall means it fails to find all the positive cases. High precision means the ones it DOES find are almost certainly positive."),
    ]),

    # ─── Chapter 8: Game Theory & Pricing Strategy ───
    Lesson("quant-game-theory", 8, "Game Theory & Pricing Strategy", ["Nash Equilibrium", "Prisoner's Dilemma"], [], [
        Task("apt8-1", "In a duopoly market, if both companies lower prices, both lose margin. If one lowers and the other keeps prices high, the lower-priced firm captures 100% of the market. What classic Game Theory concept does this represent?", "quiz", "easy", "McKinsey", options=("Zero-Sum Game", "Prisoner's Dilemma", "Tragedy of the Commons", "Pareto Optimal"), answer_index=1, explanation="This is the Prisoner's Dilemma. The rational self-interest of both firms drives them to lower prices, resulting in a worse outcome for both than if they colluded."),
        Task("apt8-2", "A 'Zero-Sum Game' is best described as:", "quiz", "medium", "Jane Street", options=("Everyone wins", "One person's gain is exactly equal to another person's loss", "Both sides lose", "Cooperative negotiation"), answer_index=1, explanation="In zero-sum games, the total utility remains constant. Poker is a classic example."),
        Task("apt8-3", "What is a 'Nash Equilibrium'?", "quiz", "hard", "Goldman Sachs", options=("When everyone cooperates perfectly", "When the market is a monopoly", "A state where no player can benefit by changing their strategy while the other players keep theirs unchanged", "When prices hit zero"), answer_index=2, explanation="In Nash Equilibrium, every player is making the optimal choice given the choices of others."),
        Task("apt8-4", "Uber's surge pricing strategy is a real-world application of matching supply and demand dynamically. When demand spikes, raising the price achieves what?", "quiz", "medium", "Uber", options=("Only increases revenue", "Reduces demand and incentivizes more drivers (supply) to come online to reach market equilibrium", "Decreases supply", "Angers customers permanently"), answer_index=1, explanation="Surge pricing is a dual-lever: it suppresses excess demand while simultaneously increasing supply (drivers)."),
        Task("apt8-5", "A software company gives away its basic product for free to gain market share, monetizing only on enterprise features. This is known as:", "quiz", "easy", "", options=("Skimming", "Freemium", "Penetration Pricing", "Loss Leader"), answer_index=1, explanation="Freemium uses a free tier for acquisition and a premium tier for monetization."),
        Task("apt8-6", "Which pricing strategy involves setting a high price initially to capture customers willing to pay a premium, then gradually lowering the price over time?", "quiz", "medium", "Apple", options=("Penetration Pricing", "Price Skimming", "Value-based Pricing", "Cost-plus Pricing"), answer_index=1, explanation="Price Skimming extracts maximum consumer surplus from early adopters before targeting more price-sensitive segments later."),
        Task("apt8-7", "If a good is highly 'price inelastic', what happens to total revenue if you raise the price?", "quiz", "hard", "Stripe", options=("Revenue increases", "Revenue decreases", "Revenue stays the same", "Demand drops to zero"), answer_index=0, explanation="Inelastic means demand drops proportionately less than the price increases. Thus, total revenue (P x Q) increases."),
        Task("apt8-8", "Two airlines are deciding whether to expand capacity. If both expand, prices collapse and both lose $10M. If neither expands, both make $20M. If one expands and the other doesn't, the expander makes $30M and the other loses $5M. If they cannot communicate, what is the likely outcome?", "quiz", "hard", "Bain", options=("Neither expands", "Both expand", "One expands randomly", "They merge"), answer_index=1, explanation="This is a Prisoner's Dilemma. Expanding is the dominant strategy for both individually, leading them to the worst mutual outcome (both lose $10M)."),
    ]),
]


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
    
    def norm(s): return str(s or "").strip().lower().replace(" ","").replace("%","").replace("$","").replace(",","").replace("months","").replace("years","").replace("s","").replace("mph","").replace("l","").replace("ms","")

    if t.kind == "quiz":
        correct = answer == t.answer_index
        return {"correct":correct,"message":"Correct!" if correct else "Not quite.","explanation":t.explanation,"expectedIndex":t.answer_index}
    
    user = norm(answer)
    expected = norm(t.expected)
    
    correct = expected in user or user == expected
    return {"correct":correct, "message":"Correct!" if correct else f"Not quite. Expected: {t.expected}", "explanation":t.explanation, "solution":t.solution}
