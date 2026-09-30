#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate ACCA TX-HKG Section B - OT case questions -> assets/qbank-b.json.

Mirrors the exam's real Section B format: 3 independent case scenarios, each
followed by 5 linked MCQs (2 marks each = 30 marks), rather than Section A's
single-fact standalone questions. Every figure in every case is computed with
scripts/qbank_tax.py and cross-checked in this file's own header comment
before being typed into a question, exactly like Section A - the arithmetic
in one question must stay consistent with the arithmetic implied by the
others in the same case, which is the whole point of a case question.

Verified against qbank_tax.py directly (see chat/build log), all figures
below match:
  Case 1 (Ms Fiona Ng):      rental value 96,000; salaries tax 136,870;
                             property tax 25,140; PA payable 165,362
                             (worse than 162,010 without electing)
  Case 2 (Golden Horizon):   DA 380,000; R&D extra deduction 2,000,000;
                             donation cap 1,081,500 (150,000 allowed);
                             assessable profit 2,940,000; tax 320,100
  Case 3 (Harbour Partners): Tam's share tax 270,000; Silver Bay's 198,000;
                             total 468,000; late payment (7mo) 311,850

Run from the project root:  python scripts/build-qbank-b.py
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "qbank-b.json")

_seq = [0]


def opts(correct, *wrong):
    """Four-option list, correct answer rotated by position so the right
    letter doesn't cluster (same convention as Section A's build-qbank.py)."""
    all_ = [correct] + list(wrong)
    pos = _seq[0] % 4
    ordered = all_[:]
    ordered.insert(pos, ordered.pop(0))
    return ordered, pos


def M(x):
    return "$" + "{:,.0f}".format(round(x))


def q(topic, text, options, answer, explain, ref=""):
    _seq[0] += 1
    assert len(options) == 4
    assert len(set(map(str, options))) == 4, "duplicate options in %r" % text[:60]
    assert 0 <= answer < 4
    return {
        "id": "B%03d" % _seq[0], "topic": topic, "q": text,
        "options": [str(o) for o in options], "answer": answer,
        "explain": explain, "ref": ref,
    }


CASES = []


# ===========================================================================
# CASE 1 - Ms Fiona Ng: employment, rented-out property, personal assessment
# ===========================================================================
def case1():
    scenario = (
        "Fiona Ng is employed as marketing manager by Silverline Retail Ltd, a "
        "company centrally managed and controlled in Hong Kong. Her annual salary "
        "for the year of assessment 2026/27 is $960,000. Silverline provides her "
        "with a self-contained flat, rent free, for the whole year; Fiona has no "
        "outgoings deductible under s.12(1)(a) against her salary.<br><br>"
        "Separately, Fiona wholly owns a second residential flat, which she lets "
        "out (unconnected with her employer) for the whole year at $18,000 a "
        "month. She personally paid rates of $6,500 for the year on that flat. "
        "She is single and claims only the basic allowance ($145,000 for "
        "2026/27); she has no mortgage on either property and no other income, "
        "deductions or losses."
    )
    items = []

    o, a = opts(M(96000), M(76800), M(38400), M(960000))
    items.append(q(
        "Rental value",
        "What rental value must be included in Fiona's assessable income for "
        "the flat Silverline provides rent free?",
        o, a,
        "The flat is self-contained accommodation, so the rate is 10%% of income "
        "after s.12(1)(a) outgoings. With no outgoings to deduct, that base is "
        "her full salary: %s &times; 10%% = %s." % (M(960000), M(96000)),
        "s.9(2)"))

    o, a = opts(M(1056000), M(960000), M(1152000), M(1036800))
    items.append(q(
        "Assessable income",
        "What is Fiona's total assessable income from her employment for the "
        "year (salary plus the rental value of the flat)?",
        o, a,
        "%s salary + %s rental value = %s. Omitting the rental value entirely, "
        "or computing it at the wrong percentage (8%% applies to two hotel "
        "rooms, not a self-contained flat), are the two errors this question "
        "is designed to catch." % (M(960000), M(96000), M(1056000)),
        "s.9(1)(a), s.9(2)"))

    o, a = opts(M(25140), M(25920), M(31425), M(32400))
    items.append(q(
        "Property tax",
        "What is the property tax payable on Fiona's own let flat for the "
        "year?",
        o, a,
        "Assessable value %s (%s &times; 12); less rates paid <strong>by the "
        "owner</strong> %s = %s; less the 20%% statutory allowance %s = net "
        "assessable value %s; &times; 15%% = %s. Forgetting the rates "
        "deduction, forgetting the 20%% allowance, or forgetting both and "
        "taxing the gross rent, each give one of the other three options."
        % (M(216000), M(18000), M(6500), M(209500), M(41900), M(167600),
           M(25140)),
        "ss.5, 5(1A)"))

    o, a = opts(M(136870), M(158400), M(161520), M(136650))
    items.append(q(
        "Salaries tax computation",
        "Ignoring any election for personal assessment, what is Fiona's "
        "salaries tax payable for the year?",
        o, a,
        "Progressive rates on net chargeable income (%s &minus; %s allowance "
        "= %s) give %s; the standard rate on net income <strong>before</strong> "
        "allowances (%s) gives %s. Salaries tax payable is the lower of the "
        "two: %s. Applying the standard rate to income <em>after</em> "
        "allowances instead of before (giving %s) is a close-looking but "
        "wrong alternative route to this figure."
        % (M(1056000), M(145000), M(911000), M(136870), M(1056000), M(158400),
           M(136870), M(136650)),
        "s.13"))

    o, a = opts(
        "No — total tax without electing ($162,010) is lower than with "
        "personal assessment ($165,362): there is no mortgage interest or "
        "loss for the election to unlock, and her income already sits in "
        "the 17% marginal band",
        "Yes — personal assessment always reduces tax for a taxpayer "
        "with property income",
        "Yes — electing lets her claim both the basic allowance and a "
        "separate property allowance",
        "It makes no difference either way")
    items.append(q(
        "Personal assessment",
        "Should Fiona elect personal assessment for the year?",
        o, a,
        "Without electing: salaries tax %s + property tax %s = %s. Electing "
        "aggregates both incomes (%s) less the same one basic allowance, "
        "computed at progressive rates capped by the standard rate on "
        "reduced total income: %s. Aggregating drags the property income "
        "into her 17%% marginal band, above the flat 15%% property tax rate, "
        "and there is nothing else (no mortgage interest, no loss) for the "
        "election to unlock — so electing costs her %s more, not less. "
        "Compute both ways; never assume personal assessment helps."
        % (M(136870), M(25140), M(162010), M(1223600), M(165362),
           M(165362 - 162010)),
        "s.41-43"))

    return dict(id="case1", label="Ms Fiona Ng", scenario=scenario, questions=items)


# ===========================================================================
# CASE 2 - Golden Horizon Ltd: profits tax computation
# ===========================================================================
def case2():
    scenario = (
        "Golden Horizon Ltd, a Hong Kong trading company, reports an accounting "
        "profit before tax of $5,000,000 for the year ended 31 March 2027. Its "
        "accounts include depreciation of $300,000 and a fine of $20,000 for a "
        "pollution control breach, and it paid $150,000 in approved charitable "
        "donations, all charged as expenses.<br><br>"
        "During the year Golden Horizon bought qualifying plant for $500,000 "
        "(the 20% pool's written-down value brought forward was $200,000, and "
        "there were no disposals), and incurred $1,000,000 of qualifying Type B "
        "R&amp;D expenditure, which is included in the $1,000,000 already "
        "charged as an expense in arriving at the accounting profit above. The "
        "company has no connected entities for the two-tier regime."
    )
    items = []

    o, a = opts(M(380000), M(300000), M(80000), M(440000))
    items.append(q(
        "Depreciation allowances",
        "What is the total depreciation allowance available on the plant "
        "pool for the year?",
        o, a,
        "Initial allowance: %s additions &times; 60%% = %s. Reduced pool: "
        "%s + %s &minus; %s = %s. Annual allowance at 20%%: %s. Total = IA "
        "%s + AA %s = %s. Taking the IA alone, the AA alone, or computing "
        "the AA on the pool <strong>before</strong> deducting the IA, each "
        "give one of the other three options."
        % (M(500000), M(300000), M(200000), M(500000), M(300000), M(400000),
           M(80000), M(300000), M(80000), M(380000)),
        "s.39B; Sch. 3"))

    o, a = opts(M(2000000), M(3000000), M(1000000), M(1500000))
    items.append(q(
        "R&D deduction",
        "Beyond the $1,000,000 already charged as an expense in the "
        "accounts, what additional deduction is available for the qualifying "
        "Type B R&amp;D expenditure?",
        o, a,
        "Type B R&amp;D is enhanced at 300%% on the first $2,000,000: %s "
        "&times; 3 = %s total allowable deduction. %s of that is already in "
        "the accounting profit, so the <strong>additional</strong> deduction "
        "still to be made in the computation is %s &minus; %s = %s. Stating "
        "the total enhanced deduction (%s) as if it were the additional "
        "amount is the commonest error - it double-counts the %s already "
        "expensed."
        % (M(1000000), M(3000000), M(1000000), M(3000000), M(1000000),
           M(2000000), M(3000000), M(1000000)),
        "s.16B"))

    o, a = opts(M(150000), M(1081500), M(52500), M(0))
    items.append(q(
        "Donations",
        "What is the maximum charitable donation deduction Golden Horizon "
        "may claim?",
        o, a,
        "The allowable deduction is the <strong>lower</strong> of the amount "
        "paid (%s) and 35%% of assessable profits before donations (%s), so "
        "the full %s paid is deductible — well within the %s cap. "
        "Stating the cap itself, rather than the lower of the two, is a "
        "common error." % (M(150000), M(1081500), M(150000), M(1081500)),
        "s.16D"))

    o, a = opts(M(2940000), M(3090000), M(3470000), M(5470000))
    items.append(q(
        "Assessable profit",
        "What is Golden Horizon's assessable profit for the year?",
        o, a,
        "%s accounting profit + %s depreciation + %s donations + %s fine = "
        "%s. Less the additional R&amp;D deduction %s = %s. Less "
        "depreciation allowances %s = %s (the base for the donation cap). "
        "Less the donation deduction %s = assessable profit %s. Stopping "
        "before deducting the donation, or before deducting the "
        "depreciation allowances, gives one of the other two wrong figures."
        % (M(5000000), M(300000), M(150000), M(20000), M(5470000),
           M(2000000), M(3470000), M(380000), M(3090000), M(150000),
           M(2940000)),
        "s.14, s.16, s.17"))

    o, a = opts(M(320100), M(485100), M(242550), M(344850))
    items.append(q(
        "Two-tier profits tax",
        "What is Golden Horizon's profits tax payable for the year?",
        o, a,
        "The two-tier rates apply to the final assessable profit of %s: "
        "(%s &times; 8.25%%) + (%s &times; 16.5%%) = %s. Applying a flat "
        "16.5%% or flat 8.25%% to the whole profit, or applying the two-tier "
        "rates to the wrong (pre-donation) profit figure of %s, each give "
        "one of the other three options."
        % (M(2940000), M(2000000), M(940000), M(320100), M(3090000)),
        "s.14AA"))

    return dict(id="case2", label="Golden Horizon Ltd", scenario=scenario, questions=items)


# ===========================================================================
# CASE 3 - Harbour Partners: mixed partnership + late payment surcharge
# ===========================================================================
def case3():
    scenario = (
        "Harbour Partners is a Hong Kong partnership with two partners: Mr Tam, "
        "an individual, holding a 60% profit share, and Silver Bay Ltd, a "
        "corporate partner, holding the remaining 40%. The partnership's "
        "assessable profit for the year is $4,000,000, allocated in that "
        "profit-sharing ratio, with each partner's two-tier $2,000,000 band "
        "apportioned in the same ratio.<br><br>"
        "Mr Tam's own tax on his share remained unpaid more than six months "
        "after the due date - specifically 7 months overdue when he finally "
        "settled it."
    )
    items = []

    o, a = opts(M(2400000), M(1600000), M(4000000), M(2000000))
    items.append(q(
        "Partnership allocation",
        "What is Mr Tam's share of the partnership's assessable profit?",
        o, a,
        "%s &times; 60%% = %s. Using Silver Bay's 40%% share instead, using "
        "the whole partnership profit unallocated, or misapplying a 50:50 "
        "split, each give one of the other three options."
        % (M(4000000), M(2400000)),
        "s.22"))

    o, a = opts(M(198000), M(264000), M(132000), M(270000))
    items.append(q(
        "Corporate partner's tax",
        "What is Silver Bay Ltd's own profits tax payable on its 40% share, "
        "applying the two-tier rates to its apportioned band?",
        o, a,
        "Silver Bay's share is %s, with an apportioned first-tier band of "
        "%s (%s &times; 40%%) at the corporate rates: (%s &times; 8.25%%) + "
        "(%s &times; 16.5%%) = %s. Applying a flat 16.5%% or flat 8.25%% to "
        "the whole share, ignoring the apportioned band, or stating Mr "
        "Tam's figure instead, each give one of the other three options."
        % (M(1600000), M(800000), M(2000000), M(800000), M(800000), M(198000)),
        "s.14AA; DIPN 28"))

    o, a = opts(M(270000), M(198000), M(360000), M(180000))
    items.append(q(
        "Individual partner's tax",
        "What is Mr Tam's own profits tax payable on his 60% share, applying "
        "the two-tier rates to his apportioned band?",
        o, a,
        "Mr Tam's share is %s, with an apportioned first-tier band of %s "
        "(%s &times; 60%%) at the unincorporated rates: (%s &times; 7.5%%) "
        "+ (%s &times; 15%%) = %s. Applying a flat 15%% or flat 7.5%% to "
        "the whole share, or stating Silver Bay's figure instead, each give "
        "one of the other three options."
        % (M(2400000), M(1200000), M(2000000), M(1200000), M(1200000),
           M(270000)),
        "s.14AA; DIPN 28"))

    o, a = opts(M(468000), M(660000), M(495000), M(450000))
    items.append(q(
        "Total partnership tax",
        "What is the total profits tax payable in respect of Harbour "
        "Partners' profit for the year?",
        o, a,
        "The partnership is not itself taxed; the total is simply the sum "
        "of what each partner pays on their own apportioned share: %s + %s "
        "= %s. Applying one flat rate to the whole $4,000,000 as if it were "
        "a single corporate taxpayer (16.5%%), a single unincorporated "
        "taxpayer at the flat rate, or the two-tier corporate rates without "
        "regard to Mr Tam's individual rate, each give one of the other "
        "three - and each ignores that a mixed partnership has more than "
        "one type of partner." % (M(270000), M(198000), M(468000)),
        "s.14AA; DIPN 28"))

    o, a = opts(M(311850), M(283500), M(297000), M(310500))
    items.append(q(
        "Late payment surcharge",
        "Mr Tam's own tax of $270,000 on his share was paid 7 months after "
        "the due date. What is the total amount he actually had to pay, "
        "including surcharges?",
        o, a,
        "A 5%% surcharge arises on the due date: %s &times; 1.05 = %s. "
        "Because it remained unpaid beyond 6 months, a further 10%% is "
        "charged on the tax <strong>plus</strong> that first surcharge: %s "
        "&times; 1.10 = %s. Stopping at the first 5%% surcharge, applying a "
        "flat 10%% instead of the compounding two-step charge, or applying "
        "the second 10%% to the original tax rather than to tax-plus-first-"
        "surcharge, each give one of the other three options."
        % (M(270000), M(283500), M(283500), M(311850)),
        "s.71(5), s.71(5A)"))

    return dict(id="case3", label="Harbour Partners", scenario=scenario, questions=items)


# ===========================================================================
# CASE 4 - Lau's Trading: sole proprietorship, s.17(2) and s.16AA
# ===========================================================================
def case4():
    scenario = (
        "Kenneth Lau runs Lau's Trading as a <strong>sole proprietorship</strong>. "
        "Its accounts for the year show a net profit of $1,800,000, after charging "
        "the following as expenses: a monthly “salary” of $50,000 drawn by "
        "Kenneth himself ($600,000 for the year), a salary of $240,000 paid to his "
        "wife, who works full time managing the shop, and depreciation of "
        "$80,000.<br><br>"
        "Depreciation allowances for the year have been computed at $120,000. "
        "Kenneth also made the mandatory MPF contribution of $18,000 in respect of "
        "himself as a self-employed person; this was <strong>not</strong> charged in "
        "the accounts above."
    )
    items = []

    o, a = opts(M(840000), M(600000), M(240000), M(0))
    items.append(q(
        "s.17(2) payments to the proprietor",
        "How much must be added back in respect of the salaries paid to Kenneth "
        "and to his wife?",
        o, a,
        "Both are added back: %s (Kenneth) + %s (his wife) = %s. A sole proprietor "
        "cannot be their own employee, and s.17(2) extends the same treatment to a "
        "payment to the proprietor's <strong>spouse</strong> — however genuinely "
        "she works in the business, husband and wife are not treated as at arm's "
        "length for this purpose. Adding back only one of the two is the error this "
        "question tests." % (M(600000), M(240000), M(840000)),
        "s.17(2)"))

    o, a = opts(M(18000), M(36000), M(0), M(60000))
    items.append(q(
        "s.16AA MPF deduction",
        "What deduction may the business claim for Kenneth's own mandatory MPF "
        "contribution as a self-employed person?",
        o, a,
        "Section 16AA allows the proprietor's own mandatory contribution as a "
        "deduction in the profits tax computation, capped at the statutory maximum "
        "of %s. It was not charged in the accounts, so it is deducted in the "
        "computation. Answering nil — on the reasoning that a proprietor's own "
        "payments are never deductible — confuses this with the s.17(2) salary "
        "rule; MPF is the deliberate exception." % M(18000),
        "s.16AA"))

    o, a = opts(M(2582000), M(2600000), M(2342000), M(2720000))
    items.append(q(
        "Assessable profit",
        "What is Lau's Trading's assessable profit for the year?",
        o, a,
        "%s net profit + %s salaries added back under s.17(2) + %s depreciation = "
        "%s; less depreciation allowances %s and the s.16AA MPF deduction %s = %s. "
        "Forgetting the MPF deduction, forgetting the wife's salary, or forgetting "
        "the depreciation allowances each give one of the other three options."
        % (M(1800000), M(840000), M(80000), M(2720000), M(120000), M(18000),
           M(2582000)),
        "ss.16, 16AA, 17(2)"))

    o, a = opts(M(237300), M(261030), M(387300), M(193650))
    items.append(q(
        "Two-tier profits tax",
        "What is the profits tax payable by Lau's Trading?",
        o, a,
        "A sole proprietorship is an <strong>unincorporated</strong> business, so "
        "the two-tier rates are 7.5%% and 15%%, not the corporate 8.25%%/16.5%%: "
        "(2,000,000 &times; 7.5%%) + (%s &times; 15%%) = %s. Using the corporate "
        "rates gives %s and is the commonest slip here."
        % (M(2582000 - 2000000), M(237300), M(261030)),
        "s.14AA"))

    o, a = opts(
        "Elect personal assessment, which lets the current-year business loss be "
        "set against his salary in the same year",
        "Nothing — a sole proprietor's loss can only ever be carried forward "
        "against future profits of the same business",
        "Carry the loss back against the previous year's profits",
        "Surrender the loss to his wife against her own income")
    items.append(q(
        "Loss relief",
        "Suppose instead that Lau's Trading had made a loss for the year, and "
        "Kenneth also had salary income from a part-time job. What could he do to "
        "relieve the loss against that salary in the same year?",
        o, a,
        "Within profits tax alone the loss is simply carried forward (s.19C) and "
        "cannot touch his salary. Electing <strong>personal assessment</strong> "
        "aggregates all his chargeable income, letting the current-year business "
        "loss shelter the salary. Hong Kong has no carry-back and no transfer of "
        "losses between spouses.",
        "ss.19C, 42(1)"))

    return dict(id="case4", label="Lau's Trading", scenario=scenario, questions=items)


# ===========================================================================
# CASE 5 - Priya Sharma: share options, gratuity, concessionary deductions
# ===========================================================================
def case5():
    scenario = (
        "Priya Sharma has a Hong Kong employment with an annual salary of "
        "$1,200,000 for the year of assessment 2026/27.<br><br>"
        "During the year she exercised a share option granted to her by her "
        "employer in an earlier year. The market value of the shares on the date "
        "of exercise was $850,000 and she paid the exercise price of $500,000. On "
        "completing her fixed-term contract she also received a gratuity of "
        "$200,000, payable under the terms of that contract.<br><br>"
        "She paid $135,000 of mortgage interest on the flat she lives in herself, "
        "and made the mandatory MPF contribution of $18,000. She is married and her "
        "husband has no income; the married person's allowance is $290,000."
    )
    items = []

    o, a = opts(M(350000), M(850000), M(500000), "Nil — a gain on shares is capital")
    items.append(q(
        "Share options",
        "What amount of the share option gain is assessable to salaries tax?",
        o, a,
        "The charge falls on exercise, on the <strong>gain</strong>: market value at "
        "exercise %s less the exercise price paid %s = %s. Assessing the full market "
        "value, or treating the gain as a capital gain outside the charge, are both "
        "wrong — an employee share option gain is specifically brought into "
        "charge by s.9(1)(d)." % (M(850000), M(500000), M(350000)),
        "s.9(1)(d); DIPN 38"))

    o, a = opts(
        "Assessable in full — it is payable under the contract, so it rewards "
        "services",
        "Not assessable — it is compensation for loss of office",
        "Assessable at 50% as a terminal payment",
        "Not assessable because it was paid after the contract ended")
    items.append(q(
        "Termination payments",
        "How is the $200,000 contract-completion gratuity treated?",
        o, a,
        "A gratuity payable <strong>under the contract</strong> on completing it is a "
        "reward for services and is fully assessable. Contrast a genuine statutory "
        "severance or long service payment under the Employment Ordinance, which is "
        "compensation for loss of office and is not assessable — that is the "
        "distinction being tested.",
        "s.8(1)"))

    o, a = opts(M(100000), M(135000), M(120000), M(0))
    items.append(q(
        "Home loan interest",
        "What deduction may Priya claim for the $135,000 of home loan interest?",
        o, a,
        "Home loan interest on the taxpayer's own dwelling is deductible but capped "
        "at %s a year (the %s figure applies only where there is a qualifying "
        "child), so %s of the %s paid is allowed and the excess simply lapses."
        % (M(100000), M(120000), M(100000), M(135000)),
        "ss.26E, 26F"))

    o, a = opts(M(1632000), M(1750000), M(1602000), M(1732000))
    items.append(q(
        "Net income",
        "What is Priya's net income for the year, after deductions but before "
        "allowances?",
        o, a,
        "Assessable income %s salary + %s option gain + %s gratuity = %s; less the "
        "capped home loan interest %s and MPF %s = %s."
        % (M(1200000), M(350000), M(200000), M(1750000), M(100000), M(18000),
           M(1632000)),
        "ss.12, 26E, 26G"))

    o, a = opts(M(210140), M(244800), M(201300), M(263840))
    items.append(q(
        "Salaries tax payable",
        "What is Priya's salaries tax payable for the year?",
        o, a,
        "Progressive rates on net chargeable income (%s &minus; %s allowance = %s) "
        "give %s; the standard rate on net income <strong>before</strong> allowances "
        "(%s &times; 15%%) gives %s. The lower of the two is %s."
        % (M(1632000), M(290000), M(1342000), M(210140), M(1632000), M(244800),
           M(210140)),
        "s.13"))

    return dict(id="case5", label="Ms Priya Sharma", scenario=scenario, questions=items)


# ===========================================================================
# CASE 6 - Mr Wong: property tax with irrecoverable rent and a lease premium
# ===========================================================================
def case6():
    scenario = (
        "Wong Kwok-keung owns two properties in Hong Kong, both let in his own "
        "name.<br><br>"
        "<strong>Flat A</strong> was let for the whole year at $30,000 a month. "
        "Wong paid rates of $12,000 on it. The tenant defaulted and $60,000 of the "
        "year's rent was proved to be irrecoverable during the year.<br><br>"
        "<strong>Flat B</strong> was let under a new <strong>four-year</strong> "
        "lease granted at the start of the year, for which Wong received a premium "
        "of $360,000. No periodic rent is payable on Flat B, and the tenant pays "
        "the rates on it direct to the Government."
    )
    items = []

    o, a = opts(M(300000), M(360000), M(288000), M(240000))
    items.append(q(
        "Irrecoverable rent",
        "What is the assessable value of Flat A for the year, before deducting "
        "rates and the statutory allowance?",
        o, a,
        "Rent for the year %s (%s &times; 12) less the %s proved irrecoverable "
        "during the year = %s. Section 7C(1) gives the deduction in the year the "
        "rent is <strong>recognised as irrecoverable</strong>, not the year it "
        "accrued." % (M(360000), M(30000), M(60000), M(300000)),
        "ss.5B(2), 7C(1)"))

    o, a = opts(M(34560), M(43200), M(38880), M(45000))
    items.append(q(
        "Flat A property tax",
        "What is the property tax payable on Flat A?",
        o, a,
        "Assessable value %s; less rates paid by the owner %s = %s; less the 20%% "
        "statutory allowance %s = net assessable value %s; &times; 15%% = %s."
        % (M(300000), M(12000), M(288000), M(57600), M(230400), M(34560)),
        "ss.5, 5(1A)"))

    o, a = opts(M(120000), M(90000), M(360000), M(30000))
    items.append(q(
        "Lease premium",
        "How much of Flat B's premium falls into the assessable value for this "
        "year?",
        o, a,
        "A premium is spread over the lease term <strong>or 36 months, whichever "
        "is shorter</strong>. The lease runs four years (48 months), so the 36-month "
        "cap bites: %s &divide; 36 &times; 12 = %s for the year. Spreading over the "
        "full 48 months gives %s and is the error the cap exists to catch."
        % (M(360000), M(120000), M(90000)),
        "s.5B(4)"))

    o, a = opts(M(48960), M(34560), M(14400), M(45360))
    items.append(q(
        "Total property tax",
        "What is Wong's total property tax liability for the year on both "
        "properties?",
        o, a,
        "Property tax is computed <strong>property by property</strong>, each with "
        "its own rates deduction and its own 20%% allowance: Flat A %s + Flat B %s "
        "(net assessable value %s &times; 15%%) = %s. Flat B has no owner's rates to "
        "deduct because the tenant pays them direct."
        % (M(34560), M(14400), M(96000), M(48960)),
        "s.5"))

    o, a = opts(
        "Apply for exemption under s.5(2)(a), the rental income being included in "
        "its profits tax computation instead",
        "Nothing — a company pays both property tax and profits tax on the same "
        "rent with no relief",
        "Claim depreciation allowances on the building against the property tax",
        "Pay property tax at the corporate rate of 16.5% instead of 15%")
    items.append(q(
        "Corporate owners",
        "Suppose Flat B were instead owned by a Hong Kong company carrying on "
        "business here. What relief from property tax would be available?",
        o, a,
        "A corporation carrying on a trade or business in Hong Kong may apply under "
        "s.5(2)(a) for exemption from property tax where the income is brought into "
        "its profits tax computation. Without that application property tax is "
        "charged and then <strong>set off</strong> against the profits tax payable "
        "under s.25 — so the rent is not taxed twice either way, but the "
        "exemption is the cleaner route.",
        "ss.5(2)(a), 25"))

    return dict(id="case6", label="Mr Wong Kwok-keung", scenario=scenario, questions=items)


if __name__ == "__main__":
    CASES = [case1(), case2(), case3(), case4(), case5(), case6()]
    total_q = sum(len(c["questions"]) for c in CASES)

    # Duplicate guard, same convention as Section A.
    seen = {}
    dupes = []
    for c in CASES:
        for item in c["questions"]:
            key = (item["q"], tuple(item["options"]))
            if key in seen:
                dupes.append((seen[key], item["id"]))
            else:
                seen[key] = item["id"]
    if dupes:
        raise SystemExit("DUPLICATE QUESTIONS: %r" % dupes)

    payload = {
        "title": "ACCA TX-HKG", "subtitle": "Section B — OT Case Questions",
        "generated": "2026-09-28", "count": total_q, "cases": CASES,
    }
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print("wrote %s (%d bytes, %d cases, %d questions)"
          % (OUT, os.path.getsize(OUT), len(CASES), total_q))
