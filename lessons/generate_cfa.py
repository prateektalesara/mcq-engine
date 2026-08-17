import json
import random
import os

# Templates for complex questions
templates = [
    {
        "text": "{name}, CFA, is a portfolio manager at {firm}. She recently received a non-public research report from her firm's equity analyst regarding a potential acquisition of {company}. The report concludes that {company} is severely undervalued. Before the report is distributed to clients, {name} purchases {shares1} shares of {company} for her personal account and {shares2} shares for her largest institutional client. According to the CFA Institute Standards of Professional Conduct, {name} has most likely violated the standard relating to:",
        "options": [
            "Priority of Transactions and Material Nonpublic Information.",
            "Loyalty, Prudence, and Care only.",
            "Fair Dealing and Diligence."
        ],
        "correctIndices": [0],
        "hint": "Consider the rules around trading on information before clients and trading on non-public info.",
        "explanation": "By trading for her personal account before clients, she violates Priority of Transactions. By acting on a non-public internal report regarding an acquisition, she may also be acting on material nonpublic information depending on the source."
    },
    {
        "text": "An analyst is evaluating a project with an initial outlay of ${outlay}. The project is expected to generate cash flows of ${cf1} in Year 1, ${cf2} in Year 2, ${cf3} in Year 3, and ${cf4} in Year 4. The company's weighted average cost of capital (WACC) is {wacc}%. The net present value (NPV) of the project is closest to:",
        "calc": "npv",
        "hint": "Discount each cash flow back to present value using the WACC.",
        "explanation": "NPV = -Outlay + CF1/(1+r) + CF2/(1+r)^2 + CF3/(1+r)^3 + CF4/(1+r)^4."
    },
    {
        "text": "A manufacturing firm operating under US GAAP reports the following financial data for the year ended December 31: Beginning Inventory of ${beg}, Purchases of ${purchases}, and Ending Inventory of ${end}. During the year, the firm recorded an inventory write-down of ${write_down} due to obsolescence. If the firm had used IFRS instead of US GAAP, and the net realizable value of the inventory subsequently recovered by ${recovery} in the following year, the most appropriate accounting treatment under IFRS would be to:",
        "options": [
            "Reverse the write-down up to the original cost of the inventory, decreasing COGS.",
            "Recognize the recovery as a direct increase to retained earnings.",
            "Ignore the recovery because inventory reversals are prohibited under IFRS."
        ],
        "correctIndices": [0],
        "hint": "IFRS allows reversals of inventory write-downs, unlike US GAAP.",
        "explanation": "Under IFRS, if the net realizable value of previously written-down inventory recovers, the write-down can be reversed. The reversal is recognized as a reduction in cost of goods sold (COGS) in the period it occurs, capped at the original cost."
    },
    {
        "text": "An economist observes that in the country of {country}, the central bank has recently engaged in open market {om_action} of government securities, {res_action} the reserve requirement from {res1}% to {res2}%, and {rate_action} the policy rate by {bps} basis points. Concurrently, the government has {gov_spend_action} infrastructure spending and {tax_action} corporate tax rates. The combined effect of these monetary and fiscal policies on {country}'s aggregate demand (AD) is most likely to be:",
        "options": [
            "Strongly contractionary.",
            "Strongly expansionary.",
            "Indeterminate without knowing the relative magnitudes."
        ],
        "correctIndices": [0], 
        "hint": "Analyze whether each policy increases or decreases the money supply and government injections.",
        "explanation": "Dynamic explanation based on randomized actions."
    },
    {
        "text": "Consider a portfolio composed of two risky assets, Asset A and Asset B. Asset A has an expected return of {retA}% and a standard deviation of {stdA}%. Asset B has an expected return of {retB}% and a standard deviation of {stdB}%. The correlation coefficient between the returns of the two assets is {corr}. If an investor allocates {weightA}% of her funds to Asset A and {weightB}% to Asset B, the expected standard deviation of the portfolio is closest to:",
        "calc": "portfolio_std",
        "hint": "Use the formula: sqrt(wA^2 * stdA^2 + wB^2 * stdB^2 + 2*wA*wB*stdA*stdB*corr)",
        "explanation": "Calculation is performed using the portfolio variance formula."
    },
    {
        "text": "{name}, a research analyst at {firm}, is preparing a report on the telecommunications sector. He incorporates several paragraphs from a recent industry journal article published by {author} into his report. {name} changes a few words in the copied text but does not cite the original author or the journal. According to the CFA Institute Standards of Professional Conduct, {name} has violated the Standard relating to:",
        "options": [
            "Misrepresentation (Plagiarism).",
            "Diligence and Reasonable Basis.",
            "Communication with Clients and Prospective Clients."
        ],
        "correctIndices": [0],
        "hint": "Using someone else's work without credit is a specific violation.",
        "explanation": "Standard I(C) Misrepresentation strictly prohibits plagiarism. Changing a few words without citing the original source still constitutes plagiarism."
    }
]

names = ["Sarah Jenkins", "Michael Chang", "David O'Connor", "Aisha Patel", "Elena Rostova", "James Smith", "Robert Chen"]
firms = ["Apex Investments", "Global Horizon Capital", "Meridian Wealth", "Vanguard Analytics", "Summit Partners"]
companies = ["ByteCorp", "NovaTech", "AeroDynamics", "BioGenix", "Stellar Energy"]
countries = ["Zephyria", "Avalon", "Eldoria", "Gondwana", "Mercia"]
authors = ["Dr. H. Markowitz", "Prof. E. Fama", "Dr. A. Smith", "J. Maynard Keynes"]

def generate_question(q_id):
    template = random.choice(templates)
    
    if "calc" in template and template["calc"] == "npv":
        outlay = random.randint(400, 800) * 1000
        cf1 = random.randint(100, 200) * 1000
        cf2 = random.randint(150, 250) * 1000
        cf3 = random.randint(180, 300) * 1000
        cf4 = random.randint(200, 400) * 1000
        wacc = round(random.uniform(7.0, 12.0), 1)
        
        npv = -outlay + cf1/(1+wacc/100) + cf2/(1+wacc/100)**2 + cf3/(1+wacc/100)**3 + cf4/(1+wacc/100)**4
        
        opt1 = f"${npv * random.uniform(0.8, 0.9):,.0f}"
        opt2 = f"${npv:,.0f}"
        opt3 = f"${npv * random.uniform(1.1, 1.2):,.0f}"
        
        opts = [opt1, opt2, opt3]
        correct = 1
        
        q_text = template["text"].format(outlay=f"{outlay:,}", cf1=f"{cf1:,}", cf2=f"{cf2:,}", cf3=f"{cf3:,}", cf4=f"{cf4:,}", wacc=wacc)
        return {
            "id": q_id,
            "text": q_text,
            "options": opts,
            "correctIndices": [correct],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} The exact NPV is ${npv:,.0f}."
        }
    
    elif "calc" in template and template["calc"] == "portfolio_std":
        retA = random.randint(10, 15)
        stdA = random.randint(15, 25)
        retB = random.randint(5, 9)
        stdB = random.randint(8, 14)
        corr = round(random.uniform(-0.5, 0.8), 2)
        weightA = random.choice([40, 50, 60])
        weightB = 100 - weightA
        
        wa = weightA / 100
        wb = weightB / 100
        sa = stdA / 100
        sb = stdB / 100
        
        var = (wa**2 * sa**2) + (wb**2 * sb**2) + (2 * wa * wb * sa * sb * corr)
        std_dev = (var ** 0.5) * 100
        
        opt1 = f"{std_dev * random.uniform(0.7, 0.85):.2f}%"
        opt2 = f"{std_dev:.2f}%"
        opt3 = f"{std_dev * random.uniform(1.15, 1.3):.2f}%"
        
        opts = [opt1, opt2, opt3]
        
        q_text = template["text"].format(retA=retA, stdA=stdA, retB=retB, stdB=stdB, corr=corr, weightA=weightA, weightB=weightB)
        return {
            "id": q_id,
            "text": q_text,
            "options": opts,
            "correctIndices": [1],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} The portfolio standard deviation is {std_dev:.2f}%."
        }
        
    elif "{country}" in template["text"]:
        is_contractionary = random.choice([True, False])
        if is_contractionary:
            om_action = "sales"
            res_action = "increased"
            rate_action = "raised"
            gov_spend = "reduced"
            tax_action = "increased"
            ans_idx = 0
            explanation = "Open market sales, higher reserve requirements, higher policy rates, reduced spending, and higher taxes all act to contract the economy and reduce aggregate demand."
        else:
            om_action = "purchases"
            res_action = "decreased"
            rate_action = "lowered"
            gov_spend = "increased"
            tax_action = "decreased"
            ans_idx = 1
            explanation = "Open market purchases, lower reserve requirements, lower policy rates, increased spending, and lower taxes all act to expand the economy and increase aggregate demand."
            
        q_text = template["text"].format(
            country=random.choice(countries),
            om_action=om_action,
            res_action=res_action,
            res1=random.randint(8, 10),
            res2=random.randint(11, 13) if is_contractionary else random.randint(5, 7),
            rate_action=rate_action,
            bps=random.choice([25, 50, 75]),
            gov_spend_action=gov_spend,
            tax_action=tax_action
        )
        return {
            "id": q_id,
            "text": q_text,
            "options": template["options"],
            "correctIndices": [ans_idx],
            "hint": template["hint"],
            "explanation": explanation
        }
        
    else:
        q_text = template["text"].format(
            name=random.choice(names),
            firm=random.choice(firms),
            company=random.choice(companies),
            shares1=random.randint(1, 5) * 1000,
            shares2=random.randint(10, 50) * 1000,
            beg=random.randint(30, 50) * 1000,
            purchases=random.randint(100, 150) * 1000,
            end=random.randint(40, 60) * 1000,
            write_down=random.randint(5, 12) * 1000,
            recovery=random.randint(5, 15) * 1000,
            author=random.choice(authors)
        )
        return {
            "id": q_id,
            "text": q_text,
            "options": template["options"],
            "correctIndices": template["correctIndices"],
            "hint": template["hint"],
            "explanation": template["explanation"]
        }

def generate_paper(filename, paper_num):
    questions = []
    for i in range(1, 91):
        questions.append(generate_question(i))
        
    paper = {
        "id": f"cfa-level-1-session-1-paper-{paper_num}",
        "title": f"CFA Level I - Session 1 Mock Exam (Paper {paper_num})",
        "description": "Full-length 90-question, professional-grade mock exam featuring complex vignettes, realistic calculations, and deep-dive scenarios replicating the true CFA exam difficulty.",
        "durationMinutes": 135,
        "questions": questions
    }
    
    with open(filename, 'w') as f:
        json.dump(paper, f, indent=4)
        
for i in range(1, 4):
    path = f"/Users/prateektalesara/Documents/GitHub/mcq-engine/lessons/cfa-level-1-session-1-paper-{i}.json"
    generate_paper(path, i)
    print(f"Generated {path} with 90 questions.")
