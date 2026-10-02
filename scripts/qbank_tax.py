# -*- coding: utf-8 -*-
"""Hong Kong tax computations used to generate and verify the question bank.

Every computational question in assets/qbank.json gets its correct answer AND
its distractors from these functions, so the arithmetic cannot drift from the
explanation. Distractors are modelled on errors the ACCA examining team has
actually reported, not on arbitrary wrong numbers.

Two bases are carried throughout. IRD publishes 2024/25 and 2025/26 as one
column, so the exam basis covers TX-HKG from June 2025 through December 2026.
"""

CURRENT_YA = "2026/27"
EXAM_YA = "2025/26"

ALLOWANCES = {
    "basic":            {"2026/27": 145000, "2025/26": 132000},
    "married":          {"2026/27": 290000, "2025/26": 264000},
    "child":            {"2026/27": 140000, "2025/26": 130000},
    "single_parent":    {"2026/27": 145000, "2025/26": 132000},
    "dep_parent_60":    {"2026/27": 55000,  "2025/26": 50000},
    "dep_parent_55":    {"2026/27": 27500,  "2025/26": 25000},
    "dep_sibling":      {"2026/27": 37500,  "2025/26": 37500},
    "personal_disab":   {"2026/27": 75000,  "2025/26": 75000},
    "disabled_dep":     {"2026/27": 75000,  "2025/26": 75000},
}

# Deduction ceilings (unchanged across both bases)
CAPS = {
    "self_education":   100000,
    "mpf_mandatory":    18000,
    "home_loan":        100000,
    "home_loan_child":  120000,
    "domestic_rent":    100000,
    "domestic_rent_ch": 120000,
    "elderly_care":     110000,
    "vhis_per_person":  8000,
    "annuity_tvc":      60000,
    "art":              100000,
    "donation_pct":     0.35,
}

PROG_BANDS = [(50000, 0.02), (50000, 0.06), (50000, 0.10), (50000, 0.14)]
PROG_REMAINDER = 0.17
STD_THRESHOLD = 5000000
STD_LOWER, STD_UPPER = 0.15, 0.16

PROFITS_FIRST_TIER = 2000000
CORP_RATES = (0.0825, 0.165)
UNINC_RATES = (0.075, 0.15)
PROPERTY_RATE = 0.15
STATUTORY_REPAIR = 0.20
PREMIUM_CAP_MONTHS = 36
IA_PLANT = 0.60
POOLS = (0.10, 0.20, 0.30)
IBA_INITIAL, IBA_ANNUAL, CBA_ANNUAL = 0.20, 0.04, 0.04


# --------------------------------------------------------------- salaries tax
def progressive(nci):
    """Salaries tax at progressive rates on net chargeable income."""
    tax, left = 0.0, max(0, nci)
    for width, rate in PROG_BANDS:
        slice_ = min(width, left)
        if slice_ <= 0:
            break
        tax += slice_ * rate
        left -= slice_
    if left > 0:
        tax += left * PROG_REMAINDER
    return round(tax, 2)


def standard_rate(net_income):
    """Two-tiered standard rate, in force from YA 2024/25."""
    n = max(0, net_income)
    if n <= STD_THRESHOLD:
        return round(n * STD_LOWER, 2)
    return round(STD_THRESHOLD * STD_LOWER + (n - STD_THRESHOLD) * STD_UPPER, 2)


def salaries_tax(net_income, allowances_total):
    """Payable is the lower of progressive on NCI and standard on net income."""
    nci = net_income - allowances_total
    return min(progressive(nci), standard_rate(net_income))


def rental_value(income_after_outgoings, kind="flat"):
    """10% self-contained, 8% two hotel rooms, 4% one room."""
    pct = {"flat": 0.10, "two_rooms": 0.08, "one_room": 0.04}[kind]
    return round(income_after_outgoings * pct, 2)


def donation_cap(base):
    return round(base * CAPS["donation_pct"], 2)


# --------------------------------------------------------------- property tax
def net_assessable_value(rent, rates_paid_by_owner=0, premium=0, lease_months=0,
                         months_let=12, irrecoverable=0, deposit_forfeited=0):
    """Assessable value less owner's rates less the 20% statutory allowance."""
    spread = 0.0
    if premium and lease_months:
        # spread over the lease term, capped at 36 months, then apportioned
        # to the months falling in this year of assessment
        spread = premium / min(lease_months, PREMIUM_CAP_MONTHS) * months_let
    av = rent + spread - max(0, irrecoverable - deposit_forfeited)
    after_rates = av - rates_paid_by_owner
    return round(after_rates * (1 - STATUTORY_REPAIR), 2)


def property_tax(nav):
    return round(nav * PROPERTY_RATE, 2)


# ---------------------------------------------------------------- profits tax
def two_tier(assessable_profit, corporate=True):
    lo, hi = CORP_RATES if corporate else UNINC_RATES
    p = max(0, assessable_profit)
    return round(min(p, PROFITS_FIRST_TIER) * lo + max(0, p - PROFITS_FIRST_TIER) * hi, 2)


def two_tier_partnership(profit, shares):
    """Mixed partnerships: each partner's slice at their own rate, and the
    first-tier band apportioned in the profit-sharing ratio."""
    total = 0.0
    detail = []
    for share, is_corp in shares:
        p = profit * share
        band = PROFITS_FIRST_TIER * share
        lo, hi = CORP_RATES if is_corp else UNINC_RATES
        t = min(p, band) * lo + max(0, p - band) * hi
        detail.append((p, band, round(t, 2)))
        total += t
    return round(total, 2), detail


def rnd_deduction(type_a, type_b):
    """s.16B: Type A at 100%, Type B at 300% on the first $2m then 200%."""
    first = min(type_b, 2000000) * 3.0
    rest = max(0.0, type_b - 2000000) * 2.0
    return round(type_a + first + rest, 2)


def da_pool(wdv_bf, additions=0, disposals=0, rate=0.30, initial=True):
    """Order: additions -> initial allowance -> disposals -> annual allowance."""
    ia = additions * IA_PLANT if initial else 0.0
    after_ia = wdv_bf + additions - ia
    reduced = after_ia - disposals
    aa = max(0.0, reduced) * rate
    return {"ia": round(ia, 2), "reduced": round(reduced, 2),
            "aa": round(aa, 2), "cf": round(reduced - aa, 2),
            "total": round(ia + aa, 2)}


def industrial_building_allowance(cost, annual_years=1, initial=True):
    """Industrial building IA and AA on qualifying construction cost."""
    ia = cost * IBA_INITIAL if initial else 0.0
    aa = cost * IBA_ANNUAL * annual_years
    total = ia + aa
    return {"ia": round(ia, 2), "aa": round(aa, 2),
            "total": round(total, 2),
            "residue": round(cost - total, 2)}


def building_balancing_adjustment(residue, proceeds, allowances_granted):
    """Balancing adjustment on sale: positive charge, negative allowance."""
    diff = proceeds - residue
    if diff >= 0:
        return {"charge": round(min(diff, allowances_granted), 2),
                "allowance": 0.0}
    return {"charge": 0.0, "allowance": round(-diff, 2)}


def hire_purchase_ia(deposit, instalments_paid, capital_per_instalment):
    """IA runs on capital sums actually paid in the year, not the cash price."""
    qualifying = deposit + instalments_paid * capital_per_instalment
    return round(qualifying * IA_PLANT, 2), qualifying


# --------------------------------------------------------- personal assessment
def personal_assessment(total_income, interest=0, concessionary=0, losses=0,
                        allowances_total=0):
    rti = total_income - interest - concessionary - losses
    nci = rti - allowances_total
    return {"rti": round(rti, 2), "nci": round(nci, 2),
            "progressive": progressive(nci), "standard": standard_rate(rti),
            "payable": round(min(progressive(nci), standard_rate(rti)), 2)}


# ------------------------------------------------------------------- penalties
def s80_max_penalty(tax_undercharged):
    """Level 3 fine plus treble the tax undercharged."""
    return round(10000 + 3 * tax_undercharged, 2)


def late_payment(tax, months_overdue):
    """5% on the due date, a further 10% on tax-plus-surcharge after 6 months."""
    if months_overdue <= 0:
        return round(tax, 2)
    first = tax * 0.05
    if months_overdue < 6:
        return round(tax + first, 2)
    return round(tax + first + (tax + first) * 0.10, 2)


def money(x):
    """Format as the question bank displays it."""
    return "{:,.0f}".format(round(x))
