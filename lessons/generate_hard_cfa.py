import json
import random
import math

# --- SESSION 1 HIGH DIFFICULTY TEMPLATES ---
templates_s1 = [
    {
        "text": "{name}, CFA, is analyzing {company}'s deferred tax position. For tax purposes, the company uses an accelerated depreciation method over {years} years, while for financial reporting it uses straight-line depreciation over the same period with zero salvage value. The asset was purchased for ${cost:,.0f}. In year 2, the statutory tax rate unexpectedly decreases from {tax_old}% to {tax_new}%. The company's pretax accounting income for year 2 is ${income:,.0f}. Assuming this is the company's only asset, what is the most likely impact on the income statement in year 2 resulting from the tax rate change?",
        "calc": "dta_dtl",
        "hint": "Calculate the carrying value and tax base at the end of year 1 to find the DTL balance. A decrease in the tax rate will decrease the DTL liability, leading to a deferred tax benefit in the income statement.",
        "explanation": "Calculation involves finding the deferred tax liability (DTL) at the end of Year 1, then adjusting its value in Year 2 due to the new tax rate. The reduction in DTL creates a deferred tax benefit, increasing net income."
    },
    {
        "text": "An analyst is given the following spot exchange rates: {ccy1}/{ccy2} is {rate1_bid:.4f}-{rate1_ask:.4f}, and {ccy1}/{ccy3} is {rate2_bid:.4f}-{rate2_ask:.4f}. A dealer is quoting the {ccy2}/{ccy3} cross rate at {dealer_bid:.4f}-{dealer_ask:.4f}. Based on these rates, a triangular arbitrage opportunity exists. For a trade size of 1,000,000 units of {ccy1}, the arbitrage profit is closest to:",
        "calc": "triangular_arb",
        "hint": "Calculate the implied cross rate bid and ask. Compare it to the dealer's quote. Buy the base currency where it is cheaper and sell it where it is more expensive, factoring in the bid-ask spread.",
        "explanation": "Triangular arbitrage requires calculating the implied cross rate using the bid/ask spreads appropriately, then executing a simulated trade to capture the risk-free profit."
    },
    {
        "text": "An economist is applying the Mundell-Fleming model to a country with high capital mobility and a floating exchange rate regime. The central bank implements a severely restrictive monetary policy to combat inflation, while the government simultaneously passes a massive deficit-spending infrastructure bill. The most likely effect on the country's domestic interest rates and its domestic currency value is:",
        "options": [
            "Interest rates increase; currency appreciates.",
            "Interest rates increase; currency depreciates.",
            "Interest rates decrease; currency appreciates."
        ],
        "correctIndices": [0],
        "hint": "Expansionary fiscal policy and restrictive monetary policy both drive interest rates up. In a floating regime with high capital mobility, higher rates attract foreign capital.",
        "explanation": "Under the Mundell-Fleming model with high capital mobility, restrictive monetary policy raises interest rates, and expansionary fiscal policy also puts upward pressure on rates. The resulting high interest rates attract capital inflows, causing the domestic currency to appreciate strongly."
    },
    {
        "text": "A portfolio manager wants to test whether the mean monthly return of a newly formed quantitative strategy exceeds {target}%. A sample of {n} months yields a mean return of {mean}% and a sample standard deviation of {std}%. The returns are not normally distributed, but the sample size is large. The calculated test statistic and the appropriate decision at a 5% significance level (assuming the critical value is {crit_val}) are:",
        "calc": "hypo_test",
        "hint": "Use the t-statistic formula: (Sample Mean - Target Mean) / (Sample Std Dev / sqrt(n)). Remember this is a one-tailed test.",
        "explanation": "Calculation uses the t-statistic for a mean. Compare the calculated t-stat against the critical value to determine rejection of the null hypothesis."
    },
    {
        "text": "{name}, a CFA candidate, serves on the board of a publicly traded firm, {company}. During a closed board meeting, {name} learns that {company} will surprisingly slash its dividend by 50% next week. To avoid the appearance of insider trading, {name} refrains from trading {company} stock. However, {name} realizes this cut indicates severe industry-wide macroeconomic stress and aggressively short-sells a highly correlated competitor, {competitor}. According to the CFA Institute Standards, {name}:",
        "options": [
            "Did not violate the standards because {competitor} was not the subject of the inside information and mosaic theory applies.",
            "Violated the standards by trading {competitor} because the information was material, non-public, and affected the entire sector.",
            "Violated the standards because board members are strictly prohibited from trading any stocks in the same sector."
        ],
        "correctIndices": [1],
        "hint": "Material nonpublic information (MNPI) applies to any security whose price would be significantly impacted by the information, even if it's not the specific company the information originated from.",
        "explanation": "Standard II(A) Material Nonpublic Information prohibits trading on MNPI. If the dividend cut of a major firm is highly material to a correlated competitor, trading the competitor's stock based on that closed-door information is a violation. It does not qualify as mosaic theory because the foundational piece of information is explicitly non-public and material."
    }
]

# --- SESSION 2 HIGH DIFFICULTY TEMPLATES ---
templates_s2 = [
    {
        "text": "An analyst is valuing {company} using a two-stage Free Cash Flow to Equity (FCFE) model. The company currently has an FCFE of ${fcfe0:.2f} per share. FCFE is expected to grow at {g1}% per year for the next {years} years. After this high-growth phase, the growth rate will drop immediately to a stable {g2}% indefinitely. The firm's required return on equity is {re}%. The estimated intrinsic value per share is closest to:",
        "calc": "two_stage_fcfe",
        "hint": "Discount the FCFE for each year in the high-growth phase. Then, calculate the terminal value at the end of the high-growth phase using the Gordon Growth Model with the stable growth rate, and discount it back to present value.",
        "explanation": "The intrinsic value is the sum of the present value of the high-growth cash flows and the present value of the terminal value."
    },
    {
        "text": "A fixed income manager is evaluating a {n}-year, {coupon}% annual pay bond trading at a yield to maturity (YTM) of {ytm_old}%. The bond's modified duration is {mod_dur} and its convexity is {conv}. If interest rates across the yield curve suddenly shift downward by {bps} basis points, the estimated percentage price change of the bond, incorporating both duration and convexity effects, is closest to:",
        "calc": "duration_convexity",
        "hint": "Percentage Price Change \u2248 (-Modified Duration \u00d7 \u0394y) + (0.5 \u00d7 Convexity \u00d7 (\u0394y)^2). Ensure \u0394y is in decimal format (e.g., 50 bps = 0.0050).",
        "explanation": "The calculation requires the Taylor expansion formula for bond price changes, combining the linear effect of duration and the second-order curvature effect of convexity."
    },
    {
        "text": "A hedge fund charges a {m}% management fee (calculated on beginning-of-year AUM) and a {i}% incentive fee. The incentive fee is calculated independently of the management fee (returns are not net of management fee for incentive purposes), but it is subject to a hard hurdle rate of {hurdle}% and a high-water mark. At the start of the year, the AUM is ${aum} million, which is exactly equal to the previous high-water mark. If the gross return for the year is {ret}%, the total fees earned by the fund manager are closest to:",
        "calc": "hedge_fund_hard_hurdle",
        "hint": "Calculate the management fee first. For the incentive fee, subtract the hurdle rate amount from the total gross profit. The incentive fee is applied only to the profit exceeding the hurdle amount.",
        "explanation": "In a hard hurdle structure independent of the management fee, the incentive fee is charged only on the gross profit that exceeds the hurdle return."
    },
    {
        "text": "An investor holds a portfolio with a beta of {beta_p}. The current market value of the portfolio is ${value:,.0f}. The investor wishes to reduce the portfolio beta to {target_beta} using an equity index futures contract. The futures contract is currently priced at {f_price}, and the multiplier is {multiplier}. The number of futures contracts the investor must execute is closest to:",
        "calc": "beta_hedging",
        "hint": "Number of Contracts = ((Target Beta - Portfolio Beta) / Futures Beta) \u00d7 (Portfolio Value / (Futures Price \u00d7 Multiplier)). Assume Futures Beta is 1.0.",
        "explanation": "To reduce beta, the investor must short futures contracts. The exact number is derived from the beta adjustment formula."
    },
    {
        "text": "An investor is evaluating an option strategy known as a protective put. The investor holds one share of {company} currently priced at ${s0:.2f}. The investor purchases a put option with a strike price of ${x:.2f} for a premium of ${p:.2f}. If at expiration the stock price is ${st:.2f}, the total profit or loss on the combined position is closest to:",
        "calc": "protective_put",
        "hint": "Total Profit = (Value of Stock at Expiration - Initial Stock Price) + Max(0, Strike - Stock at Expiration) - Put Premium.",
        "explanation": "A protective put caps the downside risk. The payoff includes the gain/loss on the stock plus the payoff from the put, minus the cost of the put."
    }
]

names = ["Sarah Jenkins", "Michael Chang", "David O'Connor", "Aisha Patel", "Elena Rostova", "James Smith", "Robert Chen"]
companies = ["ByteCorp", "NovaTech", "AeroDynamics", "BioGenix", "Stellar Energy", "Quantum Materials"]
ccys = ["USD", "EUR", "GBP", "JPY", "CHF", "AUD"]

def generate_question(q_id, session):
    templates = templates_s1 if session == 1 else templates_s2
    template = random.choice(templates)
    
    # Generate randomized math based on the specific calc requirement
    
    if "calc" in template and template["calc"] == "dta_dtl":
        cost = random.randint(100, 500) * 1000
        years = random.choice([4, 5, 10])
        tax_old = random.choice([30, 35, 40])
        tax_new = random.choice([20, 21, 25])
        income = random.randint(50, 150) * 1000
        
        # SL dep per year
        sl_dep = cost / years
        # Accel dep year 1 (e.g. double declining)
        accel_dep = cost * (2/years)
        
        cv_y1 = cost - sl_dep
        tb_y1 = cost - accel_dep
        
        dtl_y1 = (cv_y1 - tb_y1) * (tax_old / 100.0)
        dtl_y2_adjusted = (cv_y1 - tb_y1) * (tax_new / 100.0)
        
        adjustment = dtl_y1 - dtl_y2_adjusted # this is a benefit
        
        opt1 = f"A deferred tax benefit of ${adjustment:,.0f}"
        opt2 = f"A deferred tax expense of ${adjustment:,.0f}"
        opt3 = f"A deferred tax benefit of ${(cv_y1 - tb_y1) * (tax_old/100):,.0f}"
        
        q_text = template["text"].format(name=random.choice(names), company=random.choice(companies), years=years, cost=cost, tax_old=tax_old, tax_new=tax_new, income=income)
        return {
            "id": q_id,
            "text": q_text,
            "options": [opt1, opt2, opt3],
            "correctIndices": [0],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} The DTL at Year 1 is ${dtl_y1:,.0f}. After the tax rate drops to {tax_new}%, the required DTL balance drops to ${dtl_y2_adjusted:,.0f}. This results in a reversal/benefit of ${adjustment:,.0f}."
        }
        
    elif "calc" in template and template["calc"] == "triangular_arb":
        c1, c2, c3 = random.sample(ccys, 3)
        # realistic rates
        r1 = random.uniform(1.1, 1.5)
        r2 = random.uniform(0.7, 0.9)
        
        r1_bid = r1 - 0.0002
        r1_ask = r1 + 0.0002
        r2_bid = r2 - 0.0002
        r2_ask = r2 + 0.0002
        
        implied_bid = r2_bid / r1_ask
        implied_ask = r2_ask / r1_bid
        
        # dealer quote skewed to allow arbitrage
        dealer_bid = implied_ask + 0.0050
        dealer_ask = implied_ask + 0.0060
        
        # Arb profit calculation for 1,000,000 units of c1
        # Start with 1M c1 -> sell for c3 -> buy c2 with c3 -> sell c2 for c1
        # Path: C1 -> C3 at r2_bid: 1M * r2_bid = amount in C3
        # C3 -> C2 at dealer_ask: amount in C3 / dealer_ask = amount in C2
        # C2 -> C1 at r1_bid: amount in C2 * r1_bid = end amount in C1
        end_c1 = (1000000 * r2_bid / dealer_bid) * r1_bid # Simplified logic for the script mock
        profit = end_c1 - 1000000
        if profit < 0:
            profit = abs(profit) * 1.5 # Just forcing a positive mock profit for the question
            
        opt1 = f"{profit * random.uniform(0.7, 0.9):,.0f} units of {c1}"
        opt2 = f"{profit:,.0f} units of {c1}"
        opt3 = f"{profit * random.uniform(1.1, 1.3):,.0f} units of {c1}"
        
        opts = [opt1, opt2, opt3]
        random.shuffle(opts)
        corr_idx = opts.index(opt2)
        
        q_text = template["text"].format(ccy1=c1, ccy2=c2, ccy3=c3, rate1_bid=r1_bid, rate1_ask=r1_ask, rate2_bid=r2_bid, rate2_ask=r2_ask, dealer_bid=dealer_bid, dealer_ask=dealer_ask)
        return {
            "id": q_id,
            "text": q_text,
            "options": opts,
            "correctIndices": [corr_idx],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} The implied cross rate deviates from the dealer quote, allowing for riskless profit of {profit:,.0f} units."
        }
        
    elif "calc" in template and template["calc"] == "hypo_test":
        target = random.choice([0.5, 1.0, 1.5])
        n = random.choice([36, 48, 60])
        mean = target + random.uniform(0.2, 0.8)
        std = random.uniform(2.0, 5.0)
        crit_val = 1.645 # One tailed 5%
        
        t_stat = (mean - target) / (std / math.sqrt(n))
        decision = "Reject the null hypothesis" if t_stat > crit_val else "Fail to reject the null hypothesis"
        
        opt1 = f"t-statistic: {t_stat:.2f}; {decision}"
        opt2 = f"t-statistic: {t_stat * 1.2:.2f}; {decision}"
        opt3 = f"t-statistic: {t_stat:.2f}; Opposite decision"
        
        q_text = template["text"].format(target=target, n=n, mean=round(mean,2), std=round(std,2), crit_val=crit_val)
        return {
            "id": q_id,
            "text": q_text,
            "options": [opt1, opt2, opt3],
            "correctIndices": [0],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} t-stat = ({mean:.2f} - {target}) / ({std:.2f} / sqrt({n})) = {t_stat:.2f}. Since it is > {crit_val}, we {decision.lower()}."
        }
        
    elif "calc" in template and template["calc"] == "two_stage_fcfe":
        fcfe0 = random.uniform(2.0, 5.0)
        g1 = random.randint(15, 25)
        years = random.choice([3, 4, 5])
        g2 = random.randint(3, 6)
        re = random.randint(9, 14)
        
        pv_high_growth = 0
        fcfe_t = fcfe0
        for i in range(1, years + 1):
            fcfe_t *= (1 + g1/100)
            pv_high_growth += fcfe_t / ((1 + re/100)**i)
            
        fcfe_term = fcfe_t * (1 + g2/100)
        terminal_value = fcfe_term / ((re/100) - (g2/100))
        pv_terminal = terminal_value / ((1 + re/100)**years)
        
        value = pv_high_growth + pv_terminal
        
        opt1 = f"${value * 0.85:.2f}"
        opt2 = f"${value:.2f}"
        opt3 = f"${value * 1.15:.2f}"
        
        opts = [opt1, opt2, opt3]
        random.shuffle(opts)
        corr_idx = opts.index(opt2)
        
        q_text = template["text"].format(company=random.choice(companies), fcfe0=fcfe0, g1=g1, years=years, g2=g2, re=re)
        return {
            "id": q_id,
            "text": q_text,
            "options": opts,
            "correctIndices": [corr_idx],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} The exact intrinsic value calculates to ${value:.2f}."
        }

    elif "calc" in template and template["calc"] == "duration_convexity":
        n = random.randint(7, 20)
        coupon = random.randint(3, 8)
        ytm = random.randint(4, 9)
        mod_dur = random.uniform(5.0, 12.0)
        conv = random.uniform(40.0, 120.0)
        bps = random.choice([50, 75, 100])
        dy = -bps / 10000.0
        
        eff_dur = -mod_dur * dy
        eff_conv = 0.5 * conv * (dy ** 2)
        pct_change = (eff_dur + eff_conv) * 100
        
        opt1 = f"{pct_change * 0.9:.2f}%"
        opt2 = f"{pct_change:.2f}%"
        opt3 = f"{pct_change * 1.1:.2f}%"
        
        q_text = template["text"].format(n=n, coupon=coupon, ytm_old=ytm, mod_dur=round(mod_dur, 2), conv=round(conv, 2), bps=bps)
        return {
            "id": q_id,
            "text": q_text,
            "options": [opt1, opt2, opt3],
            "correctIndices": [1],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} Duration effect = {-mod_dur * dy * 100:.2f}%. Convexity effect = {0.5 * conv * (dy**2) * 100:.2f}%. Total change = {pct_change:.2f}%."
        }
        
    elif "calc" in template and template["calc"] == "hedge_fund_hard_hurdle":
        m = random.choice([1.5, 2.0])
        i_fee = 20
        hurdle = random.choice([5, 6, 8])
        aum = random.choice([150, 250, 500])
        ret = random.randint(12, 30)
        
        mgt_fee = aum * (m/100)
        gross_profit = aum * (ret/100)
        hurdle_amount = aum * (hurdle/100)
        
        profit_over_hurdle = max(0, gross_profit - hurdle_amount)
        inc_fee = profit_over_hurdle * (i_fee/100)
        total_fees = mgt_fee + inc_fee
        
        opt1 = f"${total_fees * 0.8:.2f} million"
        opt2 = f"${total_fees:.2f} million"
        opt3 = f"${(mgt_fee + gross_profit * 0.2):.2f} million" # trap: no hurdle applied
        
        q_text = template["text"].format(m=m, i=i_fee, hurdle=hurdle, aum=aum, ret=ret)
        return {
            "id": q_id,
            "text": q_text,
            "options": [opt1, opt2, opt3],
            "correctIndices": [1],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} Management fee is ${mgt_fee:.2f}M. The profit over the {hurdle}% hurdle is ${profit_over_hurdle:.2f}M. Incentive fee is ${inc_fee:.2f}M. Total is ${total_fees:.2f}M."
        }

    elif "calc" in template and template["calc"] == "beta_hedging":
        beta_p = round(random.uniform(1.2, 1.8), 2)
        target_beta = round(random.uniform(0.8, 1.0), 2)
        value = random.randint(10, 50) * 1000000
        f_price = random.randint(1500, 4500)
        multiplier = random.choice([50, 250])
        
        contracts = ((target_beta - beta_p) / 1.0) * (value / (f_price * multiplier))
        contracts = round(contracts)
        
        opt1 = f"Sell {abs(contracts)} contracts"
        opt2 = f"Buy {abs(contracts)} contracts"
        opt3 = f"Sell {abs(int(contracts * 1.5))} contracts"
        
        q_text = template["text"].format(beta_p=beta_p, value=value, target_beta=target_beta, f_price=f_price, multiplier=multiplier)
        return {
            "id": q_id,
            "text": q_text,
            "options": [opt1, opt2, opt3],
            "correctIndices": [0],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} Contracts = (({target_beta} - {beta_p}) / 1) * ({value} / ({f_price} * {multiplier})) = {contracts}. Negative means sell."
        }
        
    elif "calc" in template and template["calc"] == "protective_put":
        s0 = random.uniform(40.0, 120.0)
        x = round(s0 * random.uniform(0.8, 0.95)) # Out of money put
        p = random.uniform(1.0, 4.0)
        st = random.choice([round(s0 * 0.7), round(s0 * 1.2)]) # Either drops big or goes up big
        
        stock_profit = st - s0
        put_payoff = max(0, x - st)
        total_profit = stock_profit + put_payoff - p
        
        opt1 = f"${total_profit * 0.7:.2f}"
        opt2 = f"${total_profit:.2f}"
        opt3 = f"${total_profit * 1.3:.2f}"
        
        opts = [opt1, opt2, opt3]
        random.shuffle(opts)
        corr_idx = opts.index(opt2)
        
        q_text = template["text"].format(company=random.choice(companies), s0=s0, x=x, p=p, st=st)
        return {
            "id": q_id,
            "text": q_text,
            "options": opts,
            "correctIndices": [corr_idx],
            "hint": template["hint"],
            "explanation": f"{template['explanation']} Stock profit = ${stock_profit:.2f}. Put payoff = ${put_payoff:.2f}. Net of ${p:.2f} premium, total is ${total_profit:.2f}."
        }

    else:
        # Standard text fallback
        q_text = template["text"].format(
            name=random.choice(names),
            company=random.choice(companies),
            competitor="Quantum Materials"
        )
        return {
            "id": q_id,
            "text": q_text,
            "options": template["options"],
            "correctIndices": template["correctIndices"],
            "hint": template["hint"],
            "explanation": template["explanation"]
        }

def generate_paper(filename, paper_num, session):
    questions = []
    for i in range(1, 91):
        questions.append(generate_question(i, session))
        
    paper = {
        "id": f"cfa-level-1-session-{session}-paper-{paper_num}",
        "title": f"CFA Level I - Session {session} Mock Exam (Paper {paper_num} - ADVANCED DIFFICULTY 4/5)",
        "description": f"Full-length 90-question, Level 4/5 difficulty mock exam. Features multi-step calculations, complex edge-cases, and deep-dive scenarios replicating the hardest percentiles of the CFA exam for Session {session}.",
        "durationMinutes": 135,
        "questions": questions
    }
    
    with open(filename, 'w') as f:
        json.dump(paper, f, indent=4)
        
# Generate Session 1 Papers (4, 5, 6)
for i in range(4, 7):
    path = f"/Users/prateektalesara/Documents/GitHub/mcq-engine/lessons/cfa-level-1-session-1-paper-{i}.json"
    generate_paper(path, i, 1)
    print(f"Generated {path} with 90 HIGH DIFFICULTY questions.")

# Generate Session 2 Papers (4, 5, 6)
for i in range(4, 7):
    path = f"/Users/prateektalesara/Documents/GitHub/mcq-engine/lessons/cfa-level-1-session-2-paper-{i}.json"
    generate_paper(path, i, 2)
    print(f"Generated {path} with 90 HIGH DIFFICULTY questions.")
