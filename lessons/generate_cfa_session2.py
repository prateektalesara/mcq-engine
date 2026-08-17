import json
import random
import math

# Templates for complex questions for Session 2
templates = [
    {
        "text": "An analyst is valuing {company} using the Gordon Growth Model. The company just paid a dividend (D0) of ${d0:.2f}. Dividends are expected to grow at a constant rate of {g}% indefinitely. If the required rate of return on the stock is {r}%, the intrinsic value of the stock is closest to:",
        "calc": "gordon",
        "hint": "Use the formula: V0 = D0 * (1 + g) / (r - g). Make sure r and g are decimals.",
        "explanation": "Calculation is performed using the Gordon Growth Model."
    },
    {
        "text": "A {n}-year, {coupon}% annual coupon bond has a par value of $1,000. If the market's required yield to maturity is {ytm}%, the current price of the bond is closest to:",
        "calc": "bond_price",
        "hint": "Calculate the present value of the annuity of coupon payments plus the present value of the par value.",
        "explanation": "The price of the bond is the sum of the present value of all future cash flows discounted at the yield to maturity."
    },
    {
        "text": "An investor enters into a {days}-day forward contract on an underlying asset that does not pay any dividends or generate cash flows. The current spot price of the asset is ${spot}. The continuously compounded risk-free rate is {r}%. The no-arbitrage forward price is closest to:",
        "calc": "forward_price",
        "hint": "Use the formula: F = S0 * e^(r * T), where T is time in years (days/365).",
        "explanation": "The no-arbitrage forward price is calculated by compounding the spot price at the continuous risk-free rate over the life of the contract."
    },
    {
        "text": "A hedge fund with ${aum} million in initial assets under management (AUM) charges a {m}% management fee (based on end-of-year AUM before incentive fees) and an {i}% incentive fee on returns strictly net of the management fee. There is no hurdle rate and the fund is well above its high-water mark. If the fund earns a gross return of {ret}% for the year, the total fees collected by the fund manager are closest to:",
        "calc": "hedge_fund_fees",
        "hint": "Calculate the end-of-year AUM before fees, apply the management fee, subtract it to find net profit, and then apply the incentive fee.",
        "explanation": "Management fee is based on AUM, and incentive fee is based on the profit after the management fee is deducted."
    },
    {
        "text": "{name} is evaluating the expected return of {company} stock. The risk-free rate is {rf}%, the expected return on the market is {rm}%, and the stock's beta is {beta}. According to the Capital Asset Pricing Model (CAPM), the expected return of the stock is closest to:",
        "calc": "capm",
        "hint": "Use the formula: E(R) = Rf + Beta * (Rm - Rf).",
        "explanation": "The Capital Asset Pricing Model calculates expected return based on the risk-free rate plus a risk premium determined by beta."
    },
    {
        "text": "A real estate investment trust (REIT) is evaluating a commercial property. The property is expected to generate a net operating income (NOI) of ${noi} next year. Comparable properties in the area are selling at capitalization (cap) rates of {cap_rate}%. Using the direct capitalization method, the estimated value of the property is closest to:",
        "calc": "real_estate_cap",
        "hint": "Property Value = NOI / Cap Rate.",
        "explanation": "Under the direct capitalization method, value is estimated by dividing the next year's NOI by the appropriate capitalization rate."
    }
]

names = ["Sarah Jenkins", "Michael Chang", "David O'Connor", "Aisha Patel", "Elena Rostova", "James Smith", "Robert Chen"]
companies = ["ByteCorp", "NovaTech", "AeroDynamics", "BioGenix", "Stellar Energy", "Quantum Materials"]

def generate_question(q_id):
    template = random.choice(templates)
    
    if template["calc"] == "gordon":
        d0 = random.uniform(1.0, 5.0)
        g = random.randint(2, 6)
        r = random.randint(g + 2, 12)  # Ensure r > g
        
        value = (d0 * (1 + g/100)) / ((r/100) - (g/100))
        
        opt1 = f"${value * random.uniform(0.8, 0.9):.2f}"
        opt2 = f"${value:.2f}"
        opt3 = f"${value * random.uniform(1.1, 1.2):.2f}"
        opts = [opt1, opt2, opt3]
        
        q_text = template["text"].format(company=random.choice(companies), d0=d0, g=g, r=r)
        return {
            "id": q_id,
            "text": q_text,
            "options": opts,
            "correctIndices": [1],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} The exact intrinsic value is ${value:.2f}."
        }
        
    elif template["calc"] == "bond_price":
        n = random.randint(5, 30)
        coupon = random.randint(3, 8)
        ytm = random.randint(2, 10)
        
        c = coupon * 10
        price = 0
        for i in range(1, n + 1):
            price += c / ((1 + ytm/100)**i)
        price += 1000 / ((1 + ytm/100)**n)
        
        opt1 = f"${price * random.uniform(0.85, 0.95):.2f}"
        opt2 = f"${price:.2f}"
        opt3 = f"${price * random.uniform(1.05, 1.15):.2f}"
        opts = [opt1, opt2, opt3]
        
        q_text = template["text"].format(n=n, coupon=coupon, ytm=ytm)
        return {
            "id": q_id,
            "text": q_text,
            "options": opts,
            "correctIndices": [1],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} The exact bond price is ${price:.2f}."
        }
        
    elif template["calc"] == "forward_price":
        days = random.choice([30, 60, 90, 180])
        spot = random.randint(50, 150)
        r = round(random.uniform(2.0, 6.0), 1)
        
        fwd = spot * math.exp((r/100) * (days/365))
        
        opt1 = f"${fwd * random.uniform(0.95, 0.98):.2f}"
        opt2 = f"${fwd:.2f}"
        opt3 = f"${fwd * random.uniform(1.02, 1.05):.2f}"
        opts = [opt1, opt2, opt3]
        
        q_text = template["text"].format(days=days, spot=spot, r=r)
        return {
            "id": q_id,
            "text": q_text,
            "options": opts,
            "correctIndices": [1],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} The exact forward price is ${fwd:.2f}."
        }
        
    elif template["calc"] == "hedge_fund_fees":
        aum = random.choice([50, 100, 200, 500])
        m = random.choice([1, 1.5, 2])
        i_fee = random.choice([15, 20])
        ret = random.randint(8, 25)
        
        end_aum_gross = aum * (1 + ret/100)
        mgt_fee = end_aum_gross * (m/100)
        net_profit_before_incentive = end_aum_gross - aum - mgt_fee
        inc_fee = net_profit_before_incentive * (i_fee/100) if net_profit_before_incentive > 0 else 0
        total_fees = mgt_fee + inc_fee
        
        opt1 = f"${total_fees * random.uniform(0.7, 0.9):.2f} million"
        opt2 = f"${total_fees:.2f} million"
        opt3 = f"${total_fees * random.uniform(1.1, 1.3):.2f} million"
        opts = [opt1, opt2, opt3]
        
        q_text = template["text"].format(aum=aum, m=m, i=i_fee, ret=ret)
        return {
            "id": q_id,
            "text": q_text,
            "options": opts,
            "correctIndices": [1],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} Management fee is ${mgt_fee:.2f}M, incentive fee is ${inc_fee:.2f}M, total is ${total_fees:.2f}M."
        }
        
    elif template["calc"] == "capm":
        rf = round(random.uniform(1.5, 4.5), 1)
        rm = round(random.uniform(7.0, 12.0), 1)
        beta = round(random.uniform(0.6, 1.8), 2)
        
        exp_ret = rf + beta * (rm - rf)
        
        opt1 = f"{exp_ret * random.uniform(0.8, 0.9):.2f}%"
        opt2 = f"{exp_ret:.2f}%"
        opt3 = f"{exp_ret * random.uniform(1.1, 1.2):.2f}%"
        opts = [opt1, opt2, opt3]
        
        q_text = template["text"].format(name=random.choice(names), company=random.choice(companies), rf=rf, rm=rm, beta=beta)
        return {
            "id": q_id,
            "text": q_text,
            "options": opts,
            "correctIndices": [1],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} The exact CAPM expected return is {exp_ret:.2f}%."
        }

    elif template["calc"] == "real_estate_cap":
        noi = random.randint(100, 900) * 1000
        cap_rate = round(random.uniform(5.0, 10.0), 1)
        
        val = noi / (cap_rate / 100)
        
        opt1 = f"${val * random.uniform(0.7, 0.85):,.0f}"
        opt2 = f"${val:,.0f}"
        opt3 = f"${val * random.uniform(1.15, 1.3):,.0f}"
        opts = [opt1, opt2, opt3]
        
        q_text = template["text"].format(noi=f"{noi:,}", cap_rate=cap_rate)
        return {
            "id": q_id,
            "text": q_text,
            "options": opts,
            "correctIndices": [1],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} The exact property value is ${val:,.0f}."
        }


def generate_paper(filename, paper_num):
    questions = []
    for i in range(1, 91):
        questions.append(generate_question(i))
        
    paper = {
        "id": f"cfa-level-1-session-2-paper-{paper_num}",
        "title": f"CFA Level I - Session 2 Mock Exam (Paper {paper_num})",
        "description": "Full-length 90-question, professional-grade mock exam featuring complex vignettes, realistic calculations, and deep-dive scenarios replicating the true CFA exam difficulty for Session 2 topics (Equity, Fixed Income, Derivatives, Alternatives, Portfolio Management).",
        "durationMinutes": 135,
        "questions": questions
    }
    
    with open(filename, 'w') as f:
        json.dump(paper, f, indent=4)
        
for i in range(1, 4):
    path = f"/Users/prateektalesara/Documents/GitHub/mcq-engine/lessons/cfa-level-1-session-2-paper-{i}.json"
    generate_paper(path, i)
    print(f"Generated {path} with 90 questions.")
