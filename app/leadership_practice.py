"""Ultimate Leadership Principles module — All 16 LPs with deep behavioral scenarios."""
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

# ── Reference Tables ──
STAR_RUBRIC = Table("STAR_Method_Rubric", ("Component", "Focus", "Weak_Example", "Strong_Example"), (
    ("Situation", "Set the context and complexity", "My team was building a dashboard.", "In Q3, our logistics dashboard faced a 40% latency spike during peak holiday volume, threatening SLA compliance."),
    ("Task", "Your specific role and goal", "I had to fix it.", "As the lead BA, I needed to identify the data bottleneck and reduce latency to under 2 seconds without adding cloud compute costs."),
    ("Action", "What YOU did (use 'I', not 'We')", "We looked at the SQL and optimized it.", "I audited the query logs, found a Cartesian join in the legacy view, and rewrote the ETL pipeline to pre-aggregate daily metrics."),
    ("Result", "Quantifiable business impact", "It got faster and the manager was happy.", "Latency dropped from 15s to 1.2s, saving $50k in projected compute costs and eliminating SLA breaches for the quarter."),
))

LP_DOOR_MATRIX = Table("Decision_Matrix", ("Decision_Type", "Reversibility", "Data_Needed", "Action_LP"), (
    ("One-Way Door", "Irreversible (e.g., core architecture, pricing change)", "90%+", "Dive Deep, Are Right A Lot"),
    ("Two-Way Door", "Reversible (e.g., UI tweak, beta feature)", "70%", "Bias for Action"),
))

# ── Lessons ──
LESSONS: list[Lesson] = [
    # ─── Chapter 1: Customer Obsession ───
    Lesson("customer-obsession", 1, "Customer Obsession", ["Working Backwards", "Trust over short-term revenue"], [STAR_RUBRIC], [
        Task("lp1-1", "You are the BA for a new subscription product. Marketing wants to hide the 'Cancel' button deep in the settings to boost retention metrics for the upcoming quarterly review. What is the Amazon-aligned response?", "quiz", "hard", "Amazon", options=("Agree, delivering results is the top priority.", "Compromise by adding a 'Call to Cancel' requirement so it's not totally hidden.", "Push back forcefully using data on how dark patterns destroy long-term customer trust and LTV, insisting cancellation be frictionless.", "Escalate to HR."), answer_index=2, explanation="Customer Obsession mandates earning and keeping trust. Short-term metric hacking destroys long-term trust. Work backwards from the customer."),
        Task("lp1-2", "A major enterprise client requests a custom feature that will generate $1M in ARR. However, building it requires pausing a platform upgrade that will improve load times for your 50,000 small business users. What is the right approach?", "quiz", "hard", "AWS", options=("Build the custom feature; $1M ARR justifies the delay.", "Politely decline the enterprise client.", "Dive deep to see if the custom feature can be generalized to benefit the 50,000 users, or find a frugal workaround to unblock the client without pausing the core upgrade.", "Ask the client to pay $2M instead."), answer_index=2, explanation="Customer Obsession means obsessing over ALL customers. You don't blindly say no to $1M, but you don't sacrifice the core user base. You invent and simplify to serve both."),
        Task("lp1-3", "Your product has a bug that overcharged 100 customers by $5 each. It will cost $10,000 in engineering time to build a refund script. What do you do?", "quiz", "medium", "Amazon", options=("Ignore it, the cost to fix exceeds the damage.", "Give them $5 in store credit.", "Build the script and refund the money to their credit cards, even though the ROI on the engineering time is negative.", "Wait for them to complain."), answer_index=2, explanation="Earning trust means making the customer whole, regardless of the internal cost to correct a company error."),
        Task("lp1-4", "A customer proposes a feature idea that sounds terrible and contradicts your product roadmap. How do you respond?", "quiz", "medium", "Amazon", options=("Politely dismiss them.", "Tell them it's not on the roadmap.", "Listen intently, Dive Deep into the *underlying pain point* driving their request, and see if your roadmap solves that pain in a better way.", "Build exactly what they asked for."), answer_index=2, explanation="Customers are usually right about their pain, but often wrong about the solution. Obsess over the pain point."),
    ]),

    # ─── Chapter 2: Ownership ───
    Lesson("ownership", 2, "Ownership", ["Long-term value", "Never 'Not my job'"], [], [
        Task("lp2-1", "During an audit, you notice a downstream data engineering team has been manually refreshing a table every morning, leading to occasional errors that impact your reports. It is strictly their domain. What do you do?", "quiz", "medium", "Amazon", options=("Report the errors to their manager.", "Add a disclaimer to your reports.", "Draft a script or propose an automated architecture, and offer to help them implement the automation.", "Ignore it."), answer_index=2, explanation="Owners never say 'that's not my job.' They act on behalf of the entire company, beyond just their own team."),
        Task("lp2-2", "You are leaving the company in 2 weeks. A critical project you lead is only 50% complete. What is your focus?", "quiz", "medium", "Amazon", options=("Coast until your last day.", "Rush the remaining 50% so you can say you finished it.", "Meticulously document every decision, transition all context to your successor, and set up the project for long-term success without you.", "Hand it to a junior analyst to finish."), answer_index=2, explanation="Owners think long-term. Success is defined by how well the project runs after you leave."),
        Task("lp2-3", "A mistake was made on a public-facing report. You didn't make the mistake, but you are the final approver. Who is at fault?", "quiz", "easy", "Amazon", options=("The person who made the mistake.", "The software that didn't catch it.", "You.", "No one, mistakes happen."), answer_index=2, explanation="Owners take full accountability for the outcomes of their team and processes."),
        Task("lp2-4", "Your team hits its Q4 goal in November. Do you relax in December?", "quiz", "easy", "Amazon", options=("Yes, celebrate.", "No, raise the bar and set a new stretch goal for December to maximize company value.", "Yes, but pretend to be busy.", "Take PTO for the whole month."), answer_index=1, explanation="Owners don't stop when the quota is met; they continuously drive value."),
    ]),

    # ─── Chapter 3: Invent and Simplify ───
    Lesson("invent-simplify", 3, "Invent and Simplify", ["Innovation", "External Awareness", "Simplicity"], [], [
        Task("lp3-1", "Your team is tasked with building a complex machine learning model to predict inventory shortages. You realize a simple moving-average formula built in SQL achieves 95% of the accuracy of the ML model with 1% of the maintenance overhead. What do you do?", "quiz", "medium", "Amazon", options=("Build the ML model because it looks better on your resume.", "Propose the SQL moving-average solution, highlighting the massive reduction in technical debt.", "Build both and let the business decide.", "Outsource the ML model."), answer_index=1, explanation="Invent and Simplify means looking for the simplest possible solution to a complex problem."),
        Task("lp3-2", "You need a new internal tool. A vendor sells exactly what you need for $5k/year, but your engineers want to build it in-house for 'free' (it will take them 3 months). What do you recommend?", "quiz", "medium", "AWS", options=("Let the engineers build it.", "Buy the vendor tool to save 3 months of expensive engineering time and avoid maintenance overhead.", "Don't do the project.", "Build it, but offshore the work."), answer_index=1, explanation="Leaders are externally aware. They do not suffer from 'Not Invented Here' syndrome. Buy commodity software, build differentiators."),
        Task("lp3-3", "A process currently takes 15 steps and 3 approvals. You are asked to digitize it. What do you do first?", "quiz", "hard", "Amazon", options=("Hire a developer to build a 15-step app.", "Challenge the process itself: ask WHY 3 approvals are needed, and eliminate steps BEFORE digitizing.", "Refuse the project.", "Add more approvals for security."), answer_index=1, explanation="Never digitize a broken process. Simplify first, then automate."),
        Task("lp3-4", "When pitching a radical new idea, you are met with 'That will never work here.' How do you proceed?", "quiz", "medium", "Amazon", options=("Drop the idea.", "Argue with them.", "Build a small, cheap prototype or run a localized test to generate data that proves the concept works.", "Escalate to the CEO."), answer_index=2, explanation="Innovation is often misunderstood for long periods of time. Use data to overcome institutional resistance."),
    ]),

    # ─── Chapter 4: Are Right, A Lot ───
    Lesson("right-a-lot", 4, "Are Right, A Lot", ["Strong judgment", "Disconfirming beliefs"], [], [
        Task("lp4-1", "You strongly believed a new feature would increase conversion by 10%. After a 3-week A/B test, the data shows a 2% decrease. You spent months advocating for this. How do you present this to leadership?", "quiz", "hard", "Amazon", options=("Wait another 3 weeks.", "Blame marketing.", "Proactively share the failure in a business review, detail exactly why your initial hypothesis was wrong, and outline the new direction.", "Quietly kill the feature."), answer_index=2, explanation="Being 'Right, A Lot' includes the ability to rapidly admit when you are wrong and update your mental models without ego."),
        Task("lp4-2", "You must make a critical pricing decision, but you only have 50% of the data you usually rely on. The deadline is tomorrow. What do you do?", "quiz", "hard", "Amazon", options=("Delay the decision.", "Guess blindly.", "Combine the available data with your strong business judgment and historical instincts to make the best possible call, outlining the risks.", "Ask the CEO to decide."), answer_index=2, explanation="Leaders have strong judgment and good instincts. They don't freeze in ambiguity; they use judgment to bridge the data gap."),
        Task("lp4-3", "What is the best way to ensure your business hypotheses are correct?", "quiz", "medium", "Amazon", options=("Only hire people who agree with you.", "Actively seek out diverse perspectives and data that disconfirm your beliefs.", "Trust your gut always.", "Only look at data that supports your claim."), answer_index=1, explanation="Leaders seek diverse perspectives and work to disconfirm their beliefs to avoid confirmation bias."),
        Task("lp4-4", "A junior analyst presents data that contradicts a strategy you just announced. What is your reaction?", "quiz", "easy", "Amazon", options=("Fire them.", "Ignore the data.", "Publicly thank them, dive deep into their data, and change the strategy if the data is sound.", "Tell them to keep it quiet."), answer_index=2, explanation="Ego has no place in decision making. The data wins, no matter who brings it."),
    ]),

    # ─── Chapter 5: Learn and Be Curious ───
    Lesson("learn-curious", 5, "Learn and Be Curious", ["Continuous learning", "Exploring new domains"], [], [
        Task("lp5-1", "You are a BA heavily reliant on Tableau. The company decides to migrate entirely to Power BI. You have never used it. What is your immediate action?", "quiz", "easy", "Amazon", options=("Complain.", "Wait for paid training.", "Immediately download Power BI, build a pilot dashboard using open-source data over the weekend, and read the docs.", "Ask to transfer."), answer_index=2, explanation="Leaders are self-driven in their curiosity and never done learning."),
        Task("lp5-2", "You notice a strange anomaly in a competitor's SEC filing that isn't relevant to your current project. What do you do?", "quiz", "medium", "Amazon", options=("Ignore it.", "Spend 30 minutes digging into it to understand their strategy, and share the insight with the relevant team.", "Tell your boss it's a distraction.", "Short their stock."), answer_index=1, explanation="Curiosity means exploring possibilities and sharing learnings, even outside strict job boundaries."),
        Task("lp5-3", "A new AI tool is released that could automate half your job. How do you view this?", "quiz", "easy", "Amazon", options=("As a threat to your job security.", "As an opportunity to learn the tool, 10x your output, and take on higher-level strategic work.", "Ban its use on your team.", "Ignore it until forced to use it."), answer_index=1, explanation="Curious leaders run toward new technology to understand how it can be leveraged."),
        Task("lp5-4", "During a meeting, an engineer mentions a term you don't know ('Kubernetes'). What do you do?", "quiz", "easy", "Amazon", options=("Pretend you know what it is.", "Nod along.", "Ask them to briefly explain it, or note it down to research thoroughly after the meeting.", "Tell them not to use jargon."), answer_index=2, explanation="Never pretend to know something you don't. Learn it."),
    ]),

    # ─── Chapter 6: Hire and Develop the Best ───
    Lesson("hire-develop", 6, "Hire and Develop the Best", ["Raising the bar", "Mentorship"], [], [
        Task("lp6-1", "You are interviewing a candidate. They are competent and can do the job on day one. However, they are 'average' compared to your current team. Do you vote to hire them?", "quiz", "medium", "Amazon", options=("Yes, a warm body is better than an empty seat.", "Yes, they seem nice.", "No. Every hire must raise the performance bar.", "Abstain from voting."), answer_index=2, explanation="The 'Bar Raiser' philosophy dictates that every new hire must be better than 50% of the people currently in that role."),
        Task("lp6-2", "A high-performing analyst on your team wants to transfer to a different department to learn new skills. Losing them will hurt your team's metrics this quarter. What do you do?", "quiz", "hard", "Amazon", options=("Block the transfer.", "Delay the transfer indefinitely.", "Actively support the transfer, help them network with the new manager, and backfill their role.", "Fire them for disloyalty."), answer_index=2, explanation="Leaders develop leaders. You must act in the best interest of the employee's career and the broader company, not just your team's short-term metrics."),
        Task("lp6-3", "You notice an employee struggling with a specific type of SQL query. What is the Amazon way to handle it?", "quiz", "medium", "Amazon", options=("Do the queries for them.", "Write a bad performance review.", "Sit down with them, explain the underlying logic, provide them with practice resources, and review their next few queries.", "Fire them."), answer_index=2, explanation="Leaders are serious about their role in coaching others."),
        Task("lp6-4", "How do you evaluate if a candidate is a good fit during an interview?", "quiz", "medium", "Amazon", options=("Gut feeling.", "Which college they went to.", "Rigorous behavioral questions forcing them to provide specific, data-backed STAR examples of past performance.", "Brainteasers."), answer_index=2, explanation="Amazon relies strictly on behavioral interviewing based on past data (STAR method), not hypotheticals or gut feelings."),
    ]),

    # ─── Chapter 7: Insist on the Highest Standards ───
    Lesson("highest-standards", 7, "Insist on the Highest Standards", ["Unreasonably high quality", "Fixing root causes"], [], [
        Task("lp7-1", "A junior analyst submits a weekly report to you before it goes to the VP. The data is correct, but the charts are misaligned and there are typos. What is your response?", "quiz", "medium", "Amazon", options=("Fix it yourself quickly.", "Send it as is.", "Return it, point out the flaws, explain why presentation quality reflects on data credibility, and have them fix it.", "Yell at them."), answer_index=2, explanation="Leaders have relentlessly high standards. They do not accept 'good enough' and coach teams to meet those standards."),
        Task("lp7-2", "Your team misses a critical SLA due to a known system bug. During the post-mortem, the team agrees to 'try harder next time.' Is this acceptable?", "quiz", "hard", "Amazon", options=("Yes, if they promise.", "No. You must insist on a systemic root-cause fix (e.g., automated alerting, code refactor) to ensure the defect cannot physically happen again.", "Yes, bugs happen.", "Fire the QA team."), answer_index=1, explanation="Highest Standards means fixing the root cause of problems so they stay fixed. 'Trying harder' is not a mechanism."),
        Task("lp7-3", "A product launch is scheduled for tomorrow. During final testing, you find a minor UI glitch. It doesn't break functionality, but it looks unpolished. The VP wants to launch. What do you do?", "quiz", "hard", "Amazon", options=("Launch it.", "Push back, citing that launching a flawed product violates the high standards expected by customers.", "Launch it but don't tell anyone about the glitch.", "Quit."), answer_index=1, explanation="Standards must be unreasonably high. If it's not ready, you fight to fix it, even if it delays a launch."),
        Task("lp7-4", "Why does Amazon require 6-page narratives instead of PowerPoint presentations?", "quiz", "medium", "Amazon", options=("To save money on Microsoft licenses.", "Because writing forces deep, structured thinking and exposes logical flaws that bullet points hide, ensuring the highest standard of strategic rigor.", "Because Jeff Bezos hates slides.", "To make meetings longer."), answer_index=1, explanation="The narrative format enforces a standard of deep, analytical rigor that bullet points cannot capture."),
    ]),

    # ─── Chapter 8: Think Big ───
    Lesson("think-big", 8, "Think Big", ["Bold direction", "Beyond incremental"], [], [
        Task("lp8-1", "Your team's goal is to reduce customer service call times by 5%. While analyzing data, you realize rewriting the FAQ could eliminate 40% of calls entirely. What do you do?", "quiz", "medium", "Amazon", options=("Focus on the 5% goal.", "Propose the FAQ rewrite as a bold alternative that changes the paradigm from 'faster calls' to 'zero calls'.", "Ignore the FAQ idea.", "Write it secretly."), answer_index=1, explanation="Thinking small is a self-fulfilling prophecy. Eliminating the need for a call is thinking much bigger than shortening a call."),
        Task("lp8-2", "You are asked to build a reporting dashboard for the US team. How do you Think Big?", "quiz", "medium", "Amazon", options=("Build exactly what the US team asked for.", "Build it so it's scalable, localized, and easily adoptable by the EU and APAC teams with zero extra engineering work.", "Add a lot of colors.", "Make it 3D."), answer_index=1, explanation="Thinking big means designing solutions that scale globally and solve problems beyond your immediate scope."),
        Task("lp8-3", "When brainstorming a new product, what is the best approach?", "quiz", "hard", "Amazon", options=("Look at what competitors are doing and copy it.", "Start with a blank slate, ignore current constraints, imagine the perfect customer experience 5 years from now, and work backwards to today.", "Ask sales what they can sell tomorrow.", "Focus only on cost reduction."), answer_index=1, explanation="Working backwards from a bold, unconstrained vision is the definition of Thinking Big."),
        Task("lp8-4", "A manager says, 'We can't do that, we don't have the budget.' How does a Think Big leader respond?", "quiz", "medium", "Amazon", options=("Agree and give up.", "Say 'If we prove the ROI is 10x, the budget will find us. Let's build the business case.'", "Steal budget from another team.", "Complain to leadership."), answer_index=1, explanation="Big ideas attract capital. Don't let current constraints dictate future strategy."),
    ]),

    # ─── Chapter 9: Bias for Action ───
    Lesson("bias-for-action", 9, "Bias for Action", ["Speed matters", "Two-way doors"], [LP_DOOR_MATRIX], [
        Task("lp9-1", "You want to test a new button color on the checkout page (a Two-Way Door). You have 60% certainty it will work. What should you do?", "quiz", "medium", "Amazon", options=("Spend 4 weeks in focus groups.", "Launch the A/B test immediately. Speed matters.", "Do nothing.", "Ask the CEO."), answer_index=1, explanation="For reversible decisions, waiting for 90% data is too slow. Act when you have ~70% of the data. Take calculated risks."),
        Task("lp9-2", "You notice a severe bug in production charging users twice. What is your immediate action?", "quiz", "easy", "Amazon", options=("Schedule a meeting for tomorrow to discuss it.", "Email your boss and wait for approval.", "Immediately trigger the rollback protocol or shut down the affected service to stop the bleeding, then notify stakeholders.", "Write a report."), answer_index=2, explanation="In emergencies, action supersedes hierarchy. Stop the bleeding immediately."),
        Task("lp9-3", "A project is stalled because two teams are arguing over which database technology to use. Both are viable. What do you do?", "quiz", "medium", "Amazon", options=("Let them argue until they agree.", "Form a committee to study it for 6 months.", "Force a decision (Disagree and Commit) so the teams can start building, as the delay is worse than choosing the slightly sub-optimal database.", "Cancel the project."), answer_index=2, explanation="Speed matters in business. Prolonged indecision is often worse than a suboptimal decision."),
        Task("lp9-4", "When is Bias for Action dangerous?", "quiz", "hard", "Amazon", options=("Never.", "When making a 'One-Way Door' decision (e.g., acquiring a company, permanently deleting data) without diving deep first.", "When writing code.", "During meetings."), answer_index=1, explanation="Irreversible decisions require extreme Dive Deep and Are Right A Lot. Bias for Action applies primarily to reversible decisions."),
    ]),

    # ─── Chapter 10: Frugality ───
    Lesson("frugality", 10, "Frugality", ["Doing more with less", "Resourcefulness"], [], [
        Task("lp10-1", "Data volume doubled, and your queries are timing out. Your first instinct should be to:", "quiz", "easy", "Amazon", options=("Request a $50k budget increase for larger cloud compute.", "Tell the business to wait longer.", "Audit your SQL queries, add indexing, and optimize partitions to make the current infrastructure handle the load.", "Delete old data."), answer_index=2, explanation="Frugality breeds resourcefulness. Try to optimize and invent a way out of the constraint first before spending money."),
        Task("lp10-2", "Your team wants to buy a $100k vendor tool to track employee sentiment. You realize a free Google Form sent weekly achieves the exact same business outcome. What do you do?", "quiz", "medium", "Amazon", options=("Buy the tool, it looks more professional.", "Use the Google Form, saving the company $100k while achieving the same result.", "Build a custom tool for $50k.", "Do neither."), answer_index=1, explanation="There are no extra points for growing headcount or budget. Spend money only on things that matter to customers."),
        Task("lp10-3", "Does Frugality mean buying the cheapest laptops for your software engineers?", "quiz", "hard", "Amazon", options=("Yes, save money everywhere.", "No. Giving engineers slow laptops decreases their output, costing the company vastly more in wasted salary than the laptop savings. Frugality is about ROI, not being cheap.", "Yes, unless they complain.", "No, give everyone a Mac Pro."), answer_index=1, explanation="Frugality is not about being cheap; it's about eliminating waste and maximizing resource allocation."),
        Task("lp10-4", "A project requires a specialized skill nobody on your team has. Instead of hiring a $200k contractor, what frugal action could you take?", "quiz", "medium", "Amazon", options=("Don't do the project.", "Find an internal expert in another department and ask them to host a 2-hour bootcamp for your team.", "Hire the contractor anyway.", "Use AI to write the code unverified."), answer_index=1, explanation="Leveraging internal resources and upskilling is the frugal, inventive way to solve capability gaps."),
    ]),

    # ─── Chapter 11: Earn Trust ───
    Lesson("earn-trust", 11, "Earn Trust", ["Listening", "Speaking candidly", "Admitting faults"], [], [
        Task("lp11-1", "You presented an analysis that led to a failed product launch. During the post-mortem, how do you frame your involvement?", "quiz", "hard", "Amazon", options=("Defend your data fiercely.", "Blame the market.", "Openly state 'I missed a key variable in my model. Here is exactly what I missed, and the mechanism I built to ensure it never happens again.'", "Stay quiet."), answer_index=2, explanation="Leaders are vocally self-critical. Earning trust requires admitting mistakes proactively and showing how you learned from them."),
        Task("lp11-2", "A colleague from another team takes credit for your work in a large meeting. How do you handle it?", "quiz", "medium", "Amazon", options=("Scream at them in the meeting.", "Ignore it.", "Address it privately after the meeting, assuming positive intent first, but being direct about the facts and boundaries.", "CC their manager on an angry email."), answer_index=2, explanation="Leaders treat others respectfully. Public humiliation destroys trust, but you must still have backbone and correct the record professionally."),
        Task("lp11-3", "Your team is failing to hit a deadline. The VP asks for a status update. What do you say?", "quiz", "easy", "Amazon", options=("Lie and say everything is fine.", "Say it's delayed but don't give a reason.", "Speak candidly: 'We are 2 weeks behind due to X. Here is our mitigation plan Y to catch up.'", "Blame your team."), answer_index=2, explanation="Leaders do not believe their or their team's body odor smells of perfume. They speak the truth, even when it's ugly."),
        Task("lp11-4", "You strongly disagree with a peer's approach, but they are the decision-maker. You've stated your case, but they proceed anyway. What do you do?", "quiz", "hard", "Amazon", options=("Sabotage the project.", "Commit fully to making their approach work, despite your disagreement.", "Keep telling everyone they are wrong.", "Refuse to help."), answer_index=1, explanation="This blends Earn Trust and Disagree and Commit. You earn trust by supporting your peers' decisions once made."),
    ]),

    # ─── Chapter 12: Dive Deep ───
    Lesson("dive-deep", 12, "Dive Deep", ["Details matter", "Data vs Anecdotes"], [], [
        Task("lp12-1", "The VP of Sales says, 'Customers are furious about delivery times!' Your dashboard shows a 99% on-time delivery rate. What is the Dive Deep approach?", "quiz", "hard", "Amazon", options=("Tell the VP they are wrong.", "Assume the dashboard is broken.", "Pull raw delivery logs for the VP's specific region, and manually audit 50 random 'on-time' orders to see if the tracking logic matches the actual customer experience.", "Ignore the VP."), answer_index=2, explanation="When anecdotes and data disagree, the data is usually wrong (or measuring the wrong thing). Dive deep into the raw inputs."),
        Task("lp12-2", "A metric drops by 15%. Your analyst tells you 'It's because of seasonality.' What do you ask?", "quiz", "medium", "Amazon", options=("Okay, thanks.", "Are you sure?", "Prove it. Show me the Year-over-Year (YoY) overlay for the last 3 years, and isolate the drop to ensure no other variables changed.", "Fire the analyst."), answer_index=2, explanation="Leaders operate at all levels and stay connected to the details. They do not accept superficial explanations without proof."),
        Task("lp12-3", "You are reviewing a 50-page financial model. How do you Dive Deep without reading every cell?", "quiz", "hard", "Amazon", options=("Just read the summary.", "Pick 3 random, critical assumptions (e.g., Churn Rate) and trace the math all the way down to the raw data source to audit the logic.", "Ask the creator if it's correct.", "Run an AI summary."), answer_index=1, explanation="Spot-checking critical paths end-to-end is a core Dive Deep technique for leaders to ensure systemic quality."),
        Task("lp12-4", "What tool is commonly associated with Dive Deep when investigating an outage?", "quiz", "easy", "Toyota", options=("The 5 Whys", "A hammer", "A SWOT analysis", "A focus group"), answer_index=0, explanation="Asking 'Why?' five times forces you past the symptoms down to the systemic root cause."),
    ]),

    # ─── Chapter 13: Have Backbone; Disagree and Commit ───
    Lesson("disagree-commit", 13, "Disagree and Commit", ["Challenging politely", "Full commitment"], [], [
        Task("lp13-1", "Your Director proposes a strategy you mathematically know will lose money. You presented the data, debated passionately, but the Director decides to proceed anyway. What is your next move?", "quiz", "medium", "Amazon", options=("Refuse to work on it.", "Constantly remind everyone 'I told you so'.", "Commit fully to the Director's decision and apply 100% of your effort to make it succeed.", "Go above the Director."), answer_index=2, explanation="Once a decision is made, you must commit wholly. Sabotaging the project violates this principle."),
        Task("lp13-2", "During a meeting, the CEO states a 'fact' about your product that you know is factually incorrect. What do you do?", "quiz", "hard", "Amazon", options=("Stay quiet, they are the CEO.", "Correct them respectfully but firmly using data, right there in the meeting.", "Send them an anonymous email later.", "Agree with them."), answer_index=1, explanation="Leaders have conviction and are tenacious. They do not compromise for the sake of social cohesion, even with the CEO."),
        Task("lp13-3", "You are exhausted from arguing with a peer team about an API design. Should you just give in to end the argument?", "quiz", "medium", "Amazon", options=("Yes, social cohesion is important.", "No. If you believe your approach is best for the customer, you must respectfully escalate the disagreement to management to force a resolution.", "Yes, let them have it.", "Quit the project."), answer_index=1, explanation="Do not exhaust yourself into submission. Escalate disagreements cleanly so a decision can be made."),
        Task("lp13-4", "What does a good 'Commit' look like?", "quiz", "hard", "Amazon", options=("Saying 'fine' and doing the bare minimum.", "Actively defending the decision to your own team as if it were your own idea, and dedicating resources to its success.", "Working on it but complaining.", "Delegating it."), answer_index=1, explanation="True commitment means taking ownership of the decision's success, completely putting aside your previous opposition."),
    ]),

    # ─── Chapter 14: Deliver Results ───
    Lesson("deliver-results", 14, "Deliver Results", ["Overcoming obstacles", "No excuses"], [], [
        Task("lp14-1", "Two key engineers quit the week before a massive compliance report is due. What do you tell stakeholders?", "quiz", "medium", "Amazon", options=("The report will be late.", "Cancel the report.", "Acknowledge the loss, but present a revised plan outlining how the remaining team will work overtime and prioritize critical metrics to deliver on time.", "Submit a blank report."), answer_index=2, explanation="Leaders rise to the occasion. Unforeseen obstacles happen, but Deliver Results means finding a way to get it done anyway."),
        Task("lp14-2", "Your team hits 100% of its goals for the year. How is this viewed?", "quiz", "hard", "Amazon", options=("Perfect.", "Failure. If you hit 100%, your goals were not aggressive enough. You should be hitting ~80% on stretch goals.", "Good, ask for a raise.", "Take a vacation."), answer_index=1, explanation="In high-performance cultures, goals should be uncomfortable. Hitting 100% easily implies Sandbagging."),
        Task("lp14-3", "A dependency team says they cannot deliver the API you need for your launch. What do you do?", "quiz", "medium", "Amazon", options=("Delay your launch and blame them.", "Escalate immediately, offer your own engineers to help them build it, or find a creative workaround to launch without them.", "Wait for them.", "Cancel your project."), answer_index=1, explanation="You own the result. You cannot let a dependency become an excuse for failure."),
        Task("lp14-4", "Which LP is most often in tension with Deliver Results?", "quiz", "hard", "Amazon", options=("Frugality", "Insist on the Highest Standards (Speed vs Quality)", "Learn and Be Curious", "Earn Trust"), answer_index=1, explanation="The classic tension is launching fast (Deliver Results) vs launching perfectly (Highest Standards). Good leaders balance both."),
    ]),

    # ─── Chapter 15: Strive to be Earth's Best Employer ───
    Lesson("best-employer", 15, "Earth's Best Employer", ["Safety", "Empathy", "Growth"], [], [
        Task("lp15-1", "To hit an aggressive quarterly goal, you realize your team will need to work 80-hour weeks for a month. What do you do?", "quiz", "hard", "Amazon", options=("Mandate the overtime.", "Push back on the goal, re-scope deliverables, and protect your team from burnout.", "Let the team decide.", "Threaten to fire them."), answer_index=1, explanation="Leaders lead with empathy and prioritize a safe, productive work environment over short-term metric hacking."),
        Task("lp15-2", "An employee tells you they are struggling with mental health due to a personal issue. How do you respond?", "quiz", "medium", "Amazon", options=("Tell them to focus on work.", "Immediately relieve them of critical deadlines, connect them with HR/EAP resources, and assure them their job is safe while they recover.", "Fire them.", "Ignore it."), answer_index=1, explanation="Leaders create a safe, empathetic environment. Human well-being supersedes operational output."),
        Task("lp15-3", "You notice your team's meetings are dominated by 2 loud individuals. What do you do?", "quiz", "easy", "Amazon", options=("Nothing, they are the smartest.", "Actively structure meetings to ensure quiet/introverted team members are explicitly asked for their opinions and given space to speak safely.", "Tell the loud people to shut up.", "Stop having meetings."), answer_index=1, explanation="Best Employers create inclusive environments where all voices are heard and valued."),
        Task("lp15-4", "An employee makes a mistake that costs the company money. They immediately confess to you. How do you react?", "quiz", "medium", "Amazon", options=("Fire them.", "Yell at them.", "Thank them for their honesty, focus on fixing the systemic root cause (not punishing the human), and treat it as a learning opportunity.", "Dock their pay."), answer_index=2, explanation="Blameless post-mortems build psychological safety. Punishing honest mistakes leads to a culture of hiding errors."),
    ]),

    # ─── Chapter 16: Success and Scale Bring Broad Responsibility ───
    Lesson("success-scale", 16, "Success and Scale Bring Broad Responsibility", ["Secondary impacts", "Communities"], [], [
        Task("lp16-1", "Your team builds an algorithm that optimizes delivery routes, saving millions in fuel. However, it routes heavy trucks through residential neighborhoods, causing noise complaints. What do you do?", "quiz", "medium", "Amazon", options=("Ignore the complaints; fuel savings are the KPI.", "Tell PR to handle it.", "Proactively redesign the algorithm to apply a heavy penalty to residential zones, sacrificing a small amount of efficiency to protect local communities.", "Wait for a lawsuit."), answer_index=2, explanation="Local communities matter. We must consider the secondary impacts of our scale on society."),
        Task("lp16-2", "A new packaging material will save $10M a year but is non-recyclable and harmful to the environment. Do you approve it?", "quiz", "easy", "Amazon", options=("Yes, $10M is a lot.", "No, the long-term cost to the planet outweighs the short-term financial gain.", "Yes, but donate $1M to charity.", "Let someone else decide."), answer_index=1, explanation="We must begin each day with a determination to make better, do better, and be better for the planet."),
        Task("lp16-3", "Your AI model requires massive computing power, increasing the company's carbon footprint. What is your responsibility?", "quiz", "hard", "Amazon", options=("None, you are just an engineer.", "To actively research and implement model optimization techniques (like quantization) to reduce compute waste and energy usage.", "To deny climate change.", "To buy carbon offsets and ignore the code."), answer_index=1, explanation="Broad responsibility means owning the environmental impact of your technical decisions and actively working to reduce waste."),
        Task("lp16-4", "As a large tech company, you have the power to squeeze small suppliers on price until they go out of business. Should you?", "quiz", "medium", "Amazon", options=("Yes, maximize margins.", "No, a healthy ecosystem of suppliers is necessary for long-term sustainability. Negotiate fairly to ensure mutual survival.", "Yes, then buy their assets.", "Only if they complain."), answer_index=1, explanation="Scale gives you power, but exploiting that power to destroy the ecosystem ultimately harms your own supply chain."),
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
    
    if t.kind == "quiz":
        correct = answer == t.answer_index
        return {"correct":correct,"message":"Correct!" if correct else "Not quite.","explanation":t.explanation,"expectedIndex":t.answer_index}
    
    return {"correct":False, "message":"Not implemented for behavioral."}
