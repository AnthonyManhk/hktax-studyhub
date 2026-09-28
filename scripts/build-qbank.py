#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the ACCA TX-HKG Section A practice bank -> assets/qbank.json.

Computational questions take their answer AND their distractors from
qbank_tax.py, so the arithmetic cannot drift from the explanation. Distractors
model errors the examining team has actually reported rather than arbitrary
wrong numbers, which is what makes them worth getting wrong.

Weighting follows the real Section A: broad syllabus coverage, heaviest on
profits tax. Run from the project root:  python scripts/build-qbank.py
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qbank_tax as T  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "qbank.json")

AREAS = {
    "A": "Tax system and administration",
    "B": "Salaries tax",
    "C": "Profits tax",
    "D": "Property tax",
    "E": "Personal assessment",
}

BANK = []
_seq = [0]


def add(area, topic, q, options, answer, explain, ref="", difficulty="medium",
        kind="conceptual"):
    """Register one question. `answer` is the 0-based index of the right option."""
    assert 0 <= answer < len(options), "answer index out of range"
    assert len(options) == 4, "Section A questions have four options"
    assert len(set(map(str, options))) == 4, "duplicate options in %r" % (q[:60],)
    _seq[0] += 1
    BANK.append({
        "id": "Q%03d" % _seq[0],
        "area": area,
        "area_name": AREAS[area],
        "topic": topic,
        "difficulty": difficulty,
        "kind": kind,
        "q": q,
        "options": [str(o) for o in options],
        "answer": answer,
        "explain": explain,
        "ref": ref,
    })


def opts(correct, *wrong):
    """Build a four-option list with the correct answer rotated by position.

    Rotating stops the right answer clustering on one letter, which would let
    someone pass the bank without reading it.
    """
    all_ = [correct] + list(wrong)
    pos = _seq[0] % 4
    ordered = all_[:]
    ordered.insert(pos, ordered.pop(0))
    return ordered, pos


def M(x):
    return "$" + T.money(x)


# ===========================================================================
# AREA A - Tax system and administration  (target 45)
# ===========================================================================
def area_a():
    # --- statutory deadlines, the single most-reported weak spot ------------
    deadlines = [
        ("notify chargeability to profits tax where no return has been issued",
         "4 months after the end of the basis period", "s.51(2)",
         ["1 month after the end of the basis period",
          "3 months after the end of the basis period",
          "6 months after the end of the basis period"],
         "A person chargeable to tax who has not received a return must notify the "
         "Commissioner in writing within 4 months after the end of the basis period "
         "for the year of assessment concerned."),
        ("notify the commencement of an employee's employment",
         "3 months after the date of commencement", "s.52(4), Form IR56E",
         ["1 month after the date of commencement",
          "2 months after the date of commencement",
          "before the employee starts work"],
         "An employer must file Form IR56E within 3 months of employing anyone likely "
         "to be chargeable to salaries tax."),
        ("notify the cessation of an employee's employment",
         "1 month before the date of cessation", "s.52(5), Form IR56F",
         ["3 months after the date of cessation",
          "1 month after the date of cessation",
          "within 14 days of the date of cessation"],
         "Form IR56F is due not later than 1 month before the employee ceases to be "
         "employed."),
        ("notify that an employee is about to leave Hong Kong permanently",
         "1 month before the expected date of departure", "s.52(6), Form IR56G",
         ["1 month after the date of departure",
          "3 months before the expected date of departure",
          "on the date of departure"],
         "Form IR56G must be filed not later than 1 month before the expected date of "
         "departure. This is the obligation the June 2026 examining team reported "
         "candidates most often missed."),
        ("notify a change of the taxpayer's postal address",
         "1 month after the change", "s.51(8)",
         ["3 months after the change",
          "before the change takes effect",
          "at the time the next return is filed"],
         "Any person chargeable who changes address must inform the Commissioner in "
         "writing within 1 month."),
        ("apply for business registration after commencing business",
         "1 month after commencement", "Business Registration Ordinance",
         ["3 months after commencement",
          "before commencement",
          "4 months after the end of the first basis period"],
         "Business registration must be applied for within 1 month of commencing "
         "business, separately from the s.51(2) notification of chargeability."),
        ("lodge a valid notice of objection against an assessment",
         "1 month after the date of the notice of assessment", "s.64",
         ["1 month after the end of the year of assessment",
          "2 months after the date of the notice of assessment",
          "6 months after the date of the notice of assessment"],
         "An objection must be lodged in writing within 1 month of the date of the "
         "notice of assessment, and must state the precise grounds."),
        ("appeal to the Board of Review against the Commissioner's determination",
         "1 month after the determination is transmitted", "s.66",
         ["14 days after the determination",
          "2 months after the determination",
          "3 months after the determination"],
         "An appeal to the Board of Review must be lodged within 1 month of the "
         "Commissioner's written determination."),
    ]
    for what, right, ref, wrongs, why in deadlines:
        o, a = opts(right, *wrongs)
        add("A", "Statutory time limits",
            "Within what period must a taxpayer or employer %s?" % what,
            o, a, why, ref, "easy")

    # --- record keeping -----------------------------------------------------
    o, a = opts("7 years", "5 years", "6 years", "10 years")
    add("A", "Records",
        "For how long must a person carrying on a trade, profession or business in "
        "Hong Kong retain sufficient business records?",
        o, a,
        "Section 51C requires records sufficient to enable assessable profits to be "
        "readily ascertained to be kept for at least 7 years after the transaction. "
        "Failure carries a fine at level 6.", "s.51C", "easy")

    o, a = opts("7 years after the transaction to which they relate",
                "7 years after the end of the year of assessment",
                "6 years after the transaction",
                "Until the assessment for that year becomes final and conclusive")
    add("A", "Records",
        "From what point does the statutory retention period for business records run?",
        o, a,
        "The period runs for 7 years from the completion of the transaction, not from "
        "the year end or the date of assessment.", "s.51C")

    o, a = opts("Rent records, and records of rates and any irrecoverable rent",
                "Only the tenancy agreement",
                "Only bank statements showing rent received",
                "No records are required for property income")
    add("A", "Records",
        "A landlord letting a Hong Kong property is obliged to keep rental records. "
        "What must those records cover?",
        o, a,
        "Records must be sufficient to establish the assessable value: rent receivable, "
        "any premium, rates paid by the owner, and any rent treated as irrecoverable. "
        "June 2026 candidates could state the 7-year period but not what had to be kept.",
        "s.51D")

    # --- assessment time limits --------------------------------------------
    o, a = opts("6 years from the end of the year of assessment",
                "4 years from the end of the year of assessment",
                "7 years from the end of the year of assessment",
                "There is no time limit")
    add("A", "Additional assessment",
        "Within what period may the Assessor normally raise an additional assessment "
        "where income has been under-assessed?",
        o, a,
        "Six years from the end of the relevant year of assessment, extended to 10 "
        "years in a case of fraud or wilful evasion.", "s.60")

    o, a = opts("10 years", "6 years", "12 years", "No limit applies")
    add("A", "Additional assessment",
        "Where a taxpayer has been guilty of fraud or wilful evasion, within what "
        "period may an additional assessment be raised?",
        o, a, "The ordinary 6-year limit is extended to 10 years.", "s.60")

    # --- penalties, computational ------------------------------------------
    for tax, diff in [(11250, "medium"), (24000, "medium"), (8400, "easy"), (46500, "hard")]:
        right = T.s80_max_penalty(tax)
        o, a = opts(M(right), M(10000), M(3 * tax), M(10000 + tax))
        add("A", "Penalties",
            "A taxpayer failed to notify chargeability to tax under s.51(2) without "
            "reasonable excuse. The tax that would have been undercharged is %s. "
            "What is the maximum penalty on summary conviction?" % M(tax),
            o, a,
            "Section 80(2) imposes a fine at level 3 (%s) <strong>plus treble the tax "
            "undercharged</strong>: %s + (3 &times; %s) = %s. Answering %s alone - the "
            "fine without the treble-tax element - is the error the examining team "
            "reports most often on this question type."
            % (M(10000), M(10000), M(tax), M(right), M(10000)),
            "s.80(2)", diff, "computational")

    o, a = opts("Additional tax not exceeding treble the amount undercharged",
                "A fine of $10,000 only",
                "Imprisonment for up to 3 years",
                "A surcharge of 5% of the tax undercharged")
    add("A", "Penalties",
        "What is the maximum additional tax the Commissioner may assess under s.82A "
        "for an incorrect return made without reasonable excuse?",
        o, a,
        "Section 82A is an <strong>administrative</strong> penalty - no criminal intent "
        "need be proved - of up to treble the tax undercharged. It is assessed by the "
        "Commissioner, in place of prosecution.", "s.82A")

    o, a = opts("A fine of treble the tax undercharged and imprisonment for 3 years",
                "A fine of $10,000 and imprisonment for 6 months",
                "Additional tax of treble the amount undercharged only",
                "A surcharge of 15.5% of the tax")
    add("A", "Penalties",
        "What is the maximum penalty for wilfully and with intent evading tax, on "
        "conviction on indictment?",
        o, a,
        "Section 82 is the criminal provision: a fine of treble the tax undercharged "
        "plus imprisonment for up to 3 years. Distinguish it from s.82A, which is "
        "administrative and carries no imprisonment.", "s.82", "hard")

    # --- surcharge, computational ------------------------------------------
    for tax in [100000, 48000, 250000]:
        right = T.late_payment(tax, 7)
        five = T.late_payment(tax, 1)
        o, a = opts(M(right), M(tax * 1.15), M(five), M(tax * 1.10))
        add("A", "Late payment surcharge",
            "Tax of %s remained unpaid more than six months after the due date. What "
            "is the total amount now payable, including surcharges?" % M(tax),
            o, a,
            "A 5%% surcharge arises on the due date (%s), and a further 10%% is then "
            "charged on the tax <strong>plus that surcharge</strong> (%s), giving %s. "
            "The total surcharge is 15.5%% of the original tax, not 15%% - the second "
            "surcharge compounds on the first."
            % (M(tax * 0.05), M((tax * 1.05) * 0.10), M(right)),
            "s.71(5), s.71(5A)", "hard", "computational")

    o, a = opts("The second instalment becomes immediately due and the 5% surcharge "
                "applies to the whole outstanding balance",
                "Only the unpaid first instalment attracts the 5% surcharge",
                "The surcharge is deferred until the second instalment falls due",
                "No surcharge arises until 6 months after the second due date")
    add("A", "Late payment surcharge",
        "A demand note is payable in two instalments and the taxpayer misses the first. "
        "What is the consequence?",
        o, a,
        "Missing the first instalment accelerates the second, and the 5% surcharge is "
        "imposed on the entire outstanding balance - not merely on the instalment "
        "that was missed.", "s.71(5)", "hard")

    o, a = opts("Surcharges are still imposed on tax unpaid after the due date",
                "Surcharges are waived once the arrangement is approved",
                "Surcharges are halved",
                "Surcharges are deferred until the final instalment")
    add("A", "Late payment surcharge",
        "A taxpayer in financial difficulty applies successfully to pay tax by "
        "instalments. What is the effect on surcharges?",
        o, a,
        "IRD is explicit that an approved instalment arrangement does <strong>not</strong> "
        "stop the surcharge. It buys time and heads off recovery action; it is not a "
        "waiver.", "s.71", "medium")

    # --- recovery -----------------------------------------------------------
    recovery = [
        ("issue a recovery notice to a third party who owes money to the defaulter",
         "s.76", ["s.75", "s.77", "s.82A"],
         "A recovery notice under s.76 may be served on an employer, bank, tenant, "
         "debtor or customer, requiring them to pay the money to IRD instead."),
        ("apply to a District Judge to stop a defaulter leaving Hong Kong",
         "s.77", ["s.76", "s.75", "s.71"],
         "A departure prevention direction under s.77 lasts until the tax is paid or "
         "security is given."),
        ("sue for tax in default as a civil debt in the District Court",
         "s.75", ["s.76", "s.77", "s.80"],
         "Tax in default is recoverable as a civil debt, with the usual consequences of "
         "judgment including costs."),
    ]
    for what, right, wrongs, why in recovery:
        o, a = opts(right, *wrongs)
        add("A", "Recovery of tax",
            "Under which provision may the Commissioner %s?" % what,
            o, a, why, right, "medium")

    o, a = opts("Jointly and severally - any one owner may be pursued for the whole",
                "Severally only - each owner is liable for their own share",
                "Jointly only - all owners must be sued together",
                "Only the owner named first on the demand note is liable")
    add("A", "Recovery of tax",
        "Four people own a let property as co-owners in equal shares. How are they "
        "liable for the property tax?",
        o, a,
        "Liability is joint and several: IRD may pursue any one co-owner for the whole "
        "amount, not merely their quarter share. Once one pays in full, recovery "
        "against the others stops and tax is never collected twice.", "s.56A", "medium")

    # --- provisional tax ----------------------------------------------------
    o, a = opts("Not later than 28 days before the due date, or 14 days after the "
                "notice is issued, whichever is later",
                "Not later than 14 days before the due date",
                "At any time before the end of the year of assessment",
                "Within 1 month of the notice being issued")
    add("A", "Provisional tax",
        "By when must an application to hold over payment of provisional tax be made?",
        o, a,
        "The later of 28 days before the due date and 14 days after the notice. The "
        "grounds are prescribed - for instance a fall in income of more than 10%, "
        "cessation, or an election for personal assessment.", "s.63E", "hard")

    o, a = opts("Assessable income for the year is likely to be less than 90% of that "
                "of the preceding year",
                "The taxpayer expects a lower salary next year",
                "The taxpayer has already paid the first instalment",
                "The taxpayer objects to the amount of the provisional tax")
    add("A", "Provisional tax",
        "Which of the following is a valid statutory ground for holding over "
        "provisional salaries tax?",
        o, a,
        "A fall to below 90% of the preceding year's assessable income is one of the "
        "prescribed grounds. Mere disagreement with the amount is not.", "s.63E(2)")

    # --- assessment machinery ----------------------------------------------
    o, a = opts("An estimated assessment based on the best information available",
                "No assessment until the return is filed",
                "An automatic penalty of treble the tax",
                "A referral to the Board of Review")
    add("A", "Assessment",
        "What may the Assessor issue where a taxpayer fails to file a return?",
        o, a,
        "An estimated assessment under s.59(3). It protects the statutory time limit "
        "and is superseded once the actual figures are agreed, usually through an "
        "objection.", "s.59(3)")

    o, a = opts("It is not automatically suspended; a separate holdover application is "
                "needed",
                "It is automatically suspended until the objection is determined",
                "Half the tax must be paid and half is suspended",
                "The Commissioner must always accept security instead")
    add("A", "Objections",
        "What happens to the tax in dispute while an objection is under consideration?",
        o, a,
        "Lodging an objection does not suspend the tax. The taxpayer must separately "
        "apply to hold over the disputed portion, and the Commissioner may require "
        "security or purchase of a Tax Reserve Certificate.", "s.71(2)")

    o, a = opts("It may be rejected as invalid",
                "It is treated as valid but given lower priority",
                "The Assessor must request further particulars before rejecting it",
                "It automatically becomes an appeal to the Board of Review")
    add("A", "Objections",
        "A notice of objection is lodged in time but states no grounds. What is the "
        "consequence?",
        o, a,
        "An objection must state the <strong>precise grounds</strong>. A bare, "
        "unparticularised objection can be rejected as invalid even though it was "
        "lodged within the month.", "s.64(1)")

    o, a = opts("Departmental Interpretation and Practice Notes are not binding on "
                "taxpayers or the courts",
                "DIPNs have the force of law",
                "DIPNs bind the taxpayer but not the Commissioner",
                "DIPNs override the Inland Revenue Ordinance where they conflict")
    add("A", "Sources of tax law",
        "What is the status of a DIPN?",
        o, a,
        "DIPNs explain how IRD interprets and administers the law. They bind nobody - "
        "a taxpayer may object to a treatment set out in one. In the hierarchy of "
        "authority they sit below statute, case law and Board of Review decisions.",
        "DIPN practice", "easy")

    o, a = opts("Statute, then case law, then Board of Review decisions, then DIPNs, "
                "then advance rulings",
                "DIPNs, then statute, then case law",
                "Advance rulings, then DIPNs, then statute",
                "Case law, then statute, then DIPNs")
    add("A", "Sources of tax law",
        "Which sequence correctly ranks the authority of Hong Kong tax sources, "
        "highest first?",
        o, a,
        "Statute is supreme, followed by subsidiary legislation and case law, then "
        "Board of Review decisions, then DIPNs, with advance rulings least persuasive "
        "because they turn on their own facts.", "", "medium")

    o, a = opts("Tax avoidance uses lawful means; tax evasion is illegal",
                "They are the same thing",
                "Avoidance is illegal; evasion is lawful",
                "Avoidance applies to companies and evasion to individuals")
    add("A", "Avoidance and evasion",
        "What distinguishes tax avoidance from tax evasion?",
        o, a,
        "Avoidance arranges affairs lawfully to reduce tax; evasion involves deceit, "
        "concealment or false statements and is criminal. Note that general and "
        "specific anti-avoidance provisions are excluded from the TX-HKG syllabus.",
        "", "easy")

    o, a = opts("A ruling applies only to the applicant and the arrangement described",
                "A ruling binds all taxpayers in a similar position",
                "A ruling is published and may be relied on by anyone",
                "A ruling is binding on the courts")
    add("A", "Advance rulings",
        "What is the effect of a specific advance ruling issued by the Commissioner?",
        o, a,
        "A specific ruling may be relied on only by the applicant, and only for the "
        "arrangement and period described. Published versions are anonymised and are "
        "persuasive at best.", "Sch. 10", "medium")

    o, a = opts("The Commissioner", "The Financial Secretary",
                "The Chief Executive", "The Board of Review")
    add("A", "Administration",
        "Who is empowered to assess and collect tax under the Inland Revenue Ordinance?",
        o, a,
        "The Commissioner of Inland Revenue, who is also Collector of Stamp Revenue "
        "and Commissioner of Estate Duty.", "s.3", "easy")

    o, a = opts("An independent statutory body that hears tax appeals",
                "A division of the Inland Revenue Department",
                "A committee of the Legislative Council",
                "A branch of the District Court")
    add("A", "Board of Review",
        "What is the Board of Review?",
        o, a,
        "An independent statutory body constituted under s.65, with a chairman, deputy "
        "chairmen with legal training, and up to 150 members appointed by the Chief "
        "Executive. It hears appeals against the Commissioner's determinations.",
        "s.65", "easy")

    o, a = opts("A point of law only", "Any question of fact or law",
                "Questions of fact only", "Only the amount of the assessment")
    add("A", "Appeals",
        "On what basis may a Board of Review decision be appealed to the Court of "
        "First Instance by way of case stated?",
        o, a,
        "The Board is the final arbiter of fact. An appeal by case stated under s.69 "
        "lies on a question of law only.", "s.69", "medium")

    o, a = opts("31 August 2026 for paper filing and 2 October 2026 for electronic",
                "17 August 2026 and 17 September 2026 respectively",
                "30 April 2026 and 31 May 2026 respectively",
                "There is no extension for 'D' code returns")
    add("A", "Block Extension Scheme",
        "For 2025/26 profits tax returns with Accounting Date Code 'D', what were the "
        "extended lodgement dates announced by the Commissioner on 14 July 2026?",
        o, a,
        "Code 'D' covers accounting dates from 1 to 31 December. The paper deadline "
        "moved from 17 August to 31 August 2026, and the electronic deadline from 17 "
        "September to 2 October 2026. Codes 'N' and 'M' were unchanged.",
        "Circular to Tax Representatives, 14 Jul 2026", "hard")

    o, a = opts("Around 18 months after incorporation or commencement of business",
                "Within 1 month of incorporation",
                "Within 4 months of the first year end",
                "Only after the company notifies chargeability")
    add("A", "Returns and filing",
        "When is a newly incorporated Hong Kong company normally issued with its first "
        "profits tax return?",
        o, a,
        "Usually about 18 months after incorporation or commencement. The company must "
        "still notify chargeability under s.51(2) within 4 months of the basis period "
        "end if no return has arrived by then.", "s.51(1)", "medium")

    o, a = opts("Field assessments/audits, and desk audits and field investigations "
                "into offshore claims and transfer pricing risk",
                "IRD only ever reviews a return if the taxpayer itself requests it",
                "Every return is manually checked line by line before assessment",
                "Reviews are limited to companies with a history of late filing")
    add("A", "Compliance",
        "Besides simply processing what a return states, what compliance activity "
        "does the Inland Revenue Department carry out?",
        o, a,
        "IRD runs a risk-based programme of field audits and investigations - "
        "including into offshore profits claims and transfer pricing - as well as "
        "desk-based reviews, quite separately from the routine processing of "
        "assessments.", "", "medium")

    o, a = opts("A Hong Kong identity card, or - for a company - its certificate of "
                "incorporation and business registration certificate, plus supporting "
                "documents as requested",
                "A passport is always sufficient on its own",
                "No form of identification is ever required to file a return",
                "Only a bank statement is required")
    add("A", "Filing", "What must generally accompany the first return filed by a "
        "newly registered taxpayer, in addition to the return itself?",
        o, a, "Basic identification and registration documents - an HKID for an "
        "individual, or the certificate of incorporation and business registration "
        "certificate for a company - together with any supporting schedules IRD "
        "specifically requests.", "", "easy")


# ===========================================================================
# AREA B - Salaries tax  (target 75)
# ===========================================================================
def area_b():
    # --- source and scope ---------------------------------------------------
    o, a = opts("Where the contract was negotiated and is enforceable, the residence of "
                "the employer, and where remuneration is paid",
                "Where the employee lives, works and banks",
                "The nationality of the employee and the employer",
                "Where the employment was advertised and where tax is withheld")
    add("B", "Source of employment",
        "Under the totality of facts test in <em>Goepfert</em>, which three factors "
        "principally determine whether an employment is a Hong Kong employment?",
        o, a,
        "The three Goepfert factors. They are indicative, not conclusive - the test is "
        "the totality of the facts (DIPN 10).", "DIPN 10", "easy")

    o, a = opts("More than 60 days", "60 days or more", "More than 90 days",
                "More than 183 days")
    add("B", "60-day rule",
        "Income from services rendered wholly outside Hong Kong by a non-Government "
        "employee is excluded from salaries tax unless the person visited Hong Kong "
        "for what period during the basis period?",
        o, a,
        "Section 8(1B) brings the visit days back into charge where the person was in "
        "Hong Kong for <strong>more than 60 days</strong>. It is a cliff edge: 61 days "
        "loses the whole exemption, and both the arrival and departure day count in "
        "full, even for a same-day transit.", "s.8(1A)(b), s.8(1B)", "easy")

    o, a = opts("61", "60", "59", "62")
    add("B", "60-day rule",
        "An employee's ordinary visits to Hong Kong total 59 days. On two occasions he "
        "also departed very early in the morning on a connecting flight. How many days "
        "does he count as present?",
        o, a,
        "Both the day of arrival and the day of departure count as a full day each, "
        "even for a same-day transit. 59 + 2 = 61, which exceeds 60, so the s.8(1B) "
        "exemption fails entirely.", "s.8(1B)", "hard", "computational")

    for salary, months_out, foreign_tax in [(100000, 9, 180000), (120000, 10, 250000),
                                            (80000, 8, 150000)]:
        right = salary * (12 - months_out) + foreign_tax
        o, a = opts(M(right), M(salary * (12 - months_out)), M(foreign_tax),
                    M(salary * 12))
        add("B", "s.8(1A)(c) exclusion",
            "An employee has a Hong Kong employment with a company managed and "
            "controlled in Hong Kong. He spent %d months working in a territory with "
            "<strong>no</strong> double taxation arrangement with Hong Kong, and that "
            "salary bore local income tax of %s, which the employer paid on his "
            "behalf. His salary is %s a month. What is his assessable income?"
            % (months_out, M(foreign_tax), M(salary)),
            o, a,
            "Section 8(1A)(c) excludes income for services rendered in a non-DTA "
            "territory where tax of substantially the same nature has been paid there, "
            "so the %d months' salary drops out. But foreign tax <strong>borne by the "
            "employer is itself a taxable perquisite</strong>: (%s &times; %d) + %s = "
            "%s. Omitting the employer-paid tax is the commonest error."
            % (months_out, M(salary), 12 - months_out, M(foreign_tax), M(right)),
            "s.8(1A)(c)", "hard", "computational")

    o, a = opts("Always Hong Kong sourced, wherever the services are rendered",
                "Sourced where the director physically performs the duties",
                "Exempt if the director spends fewer than 60 days in Hong Kong",
                "Apportioned by time spent in Hong Kong")
    add("B", "Directors' fees",
        "How are directors' fees from a company resident in Hong Kong treated?",
        o, a,
        "A directorship is located where the company is centrally managed and "
        "controlled, so the fees are fully Hong Kong sourced regardless of where the "
        "director works. Time apportionment and the 60-day rule do not apply.",
        "s.8(1)(a)", "medium")

    # --- rental value, computational ---------------------------------------
    for base, kind, label, actual in [
            (998000, "flat", "a self-contained flat", 240000),
            (600000, "two_rooms", "two rooms in a hotel", 156000),
            (750000, "one_room", "a single hotel room", 132000),
            (1200000, "flat", "a rent-free house", 420000)]:
        right = T.rental_value(base, kind)
        wrong = [M(T.rental_value(base, k)) for k in ("flat", "two_rooms", "one_room")
                 if k != kind]
        o, a = opts(M(right), M(actual), *wrong)
        add("B", "Rental value",
            "An employee's income after allowable outgoings is %s. The employer "
            "provides %s rent free, at a cost to the employer of %s for the year. "
            "What rental value is assessable?" % (M(base), label, M(actual)),
            o, a,
            "Rental value is a percentage of income <strong>after</strong> s.12(1)(a) "
            "outgoings: 10%% for a flat or other self-contained accommodation, 8%% for "
            "two rooms in a hotel, hostel or boarding house, and 4%% for a single room. "
            "Here %s &times; %s = %s."
            % (M(base), {"flat": "10%", "two_rooms": "8%", "one_room": "4%"}[kind],
               M(right)),
            "s.9(2)", "medium", "computational")

    o, a = opts("It is deducted from the rental value, but only down to nil",
                "It is deducted from assessable income before the rental value is computed",
                "It has no effect on the computation",
                "It may create a negative rental value carried forward")
    add("B", "Rent suffered",
        "An employee pays part of the rent on employer-provided quarters. How is the "
        "'rent suffered' treated?",
        o, a,
        "Rent paid by the employee, less any rent refunded, reduces the rental value - "
        "but only to nil. It cannot create a negative figure or a loss.",
        "s.9(1)(b)", "medium")

    o, a = opts("10% of income after deducting the professional subscription",
                "10% of gross salary before any deduction",
                "10% of income after all concessionary deductions",
                "10% of net chargeable income after allowances")
    add("B", "Rental value",
        "On what base is the 10% rental value calculated?",
        o, a,
        "Income after s.12(1)(a) outgoings but <strong>before</strong> self-education "
        "and the concessionary deductions. Using gross salary, or income after "
        "concessionary deductions, both give the wrong figure.", "s.9(2)", "hard")

    # --- benefits -----------------------------------------------------------
    benefits = [
        ("Medical expenses reimbursed by the employer", True,
         "Reimbursement of an employee's own liability is assessable income. The June "
         "2026 report names failing to assess it as a common error."),
        ("Shipping costs and air fares paid by the employer to relocate a new employee "
         "and family to Hong Kong", False,
         "Genuine relocation expenses are not assessable - they are incurred for the "
         "employer's purposes, not as a reward for services."),
        ("Interest saved on an interest-free loan from the employer", False,
         "A benefit that is not convertible into money and does not discharge the "
         "employee's own liability is outside the charge."),
        ("A holiday journey paid for by the employer", True,
         "Section 9(2A)(c) assesses holiday journey benefits on the actual cost to the "
         "employer, whether or not convertible, apportioned for business-cum-holiday "
         "travel (DIPN 41)."),
        ("The employer settling the employee's personal credit card bill", True,
         "Discharging the employee's own liability is assessable under the s.9(1)(a)(iv) "
         "liability test, even though no cash passes to the employee."),
        ("A corporate club membership in the company's name, used by an employee", False,
         "Where the liability is the employer's and the benefit is not convertible into "
         "money, it falls outside the charge."),
        ("Reimbursement of an employee's deductible self-education expenses", False,
         "Reimbursed self-education expenses are not taxable; correspondingly no "
         "deduction is available for the reimbursed portion. Taxing them is a "
         "reported error."),
    ]
    for item, taxable, why in benefits:
        right = "Assessable" if taxable else "Not assessable"
        other = "Not assessable" if taxable else "Assessable"
        o, a = opts(right, other, "Assessable only if the employee is a director",
                    "Assessable only at 50% of the cost")
        add("B", "Fringe benefits",
            "How is the following treated for salaries tax purposes?<br><em>%s</em>" % item,
            o, a, why, "s.9; DIPN 16, 41", "medium")

    o, a = opts("The market value on the date the shares vest",
                "The market value on the date the award is granted",
                "The price paid by the employee",
                "The average of the grant and vesting values")
    add("B", "Share awards",
        "On what value is a share <em>award</em> benefit assessed?",
        o, a,
        "A share award is assessed on the market value when the shares "
        "<strong>vest</strong>. Using the grant-date value is named in the June 2026 "
        "report as a common error. Contrast a share <em>option</em>, which is assessed "
        "on the gain at exercise, assignment or release.", "s.9(1)(d); DIPN 38", "hard")

    for total_days, hk_days in [(730, 292), (1095, 365), (365, 146)]:
        pct = hk_days / total_days
        o, a = opts("%.0f%%" % (pct * 100), "%.0f%%" % ((1 - pct) * 100), "100%",
                    "%.0f%%" % (pct * 50))
        add("B", "Share options",
            "A share option has a vesting period of %d days, of which %d were spent "
            "working in Hong Kong. What proportion of the gain on exercise is "
            "assessable to Hong Kong salaries tax?" % (total_days, hk_days),
            o, a,
            "The gain is apportioned by reference to the days of the vesting period "
            "attributable to Hong Kong services: %d/%d = %.0f%%."
            % (hk_days, total_days, pct * 100),
            "DIPN 38", "medium", "computational")

    o, a = opts("Assessable in full as income from employment",
                "Exempt as a capital receipt",
                "Assessable at 50%",
                "Exempt if paid after the employment ends")
    add("B", "Termination payments",
        "How is a contractual gratuity payable on completion of a fixed-term contract "
        "treated?",
        o, a,
        "A gratuity payable under the contract is a reward for services and is fully "
        "assessable. Contrast genuine severance and long service payments under the "
        "Employment Ordinance, which are not.", "s.8(1)", "medium")

    o, a = opts("Not assessable, to the extent of the statutory entitlement",
                "Fully assessable as income from employment",
                "Assessable at 50%",
                "Assessable only if the employee is re-employed within 12 months")
    add("B", "Termination payments",
        "How is a statutory severance payment under the Employment Ordinance treated?",
        o, a,
        "Statutory severance and long service payments are compensation for loss of "
        "office rather than a reward for services, and are not assessable to the "
        "extent of the statutory entitlement.", "s.8(1)", "medium")

    # --- deductions ---------------------------------------------------------
    caps = [
        ("Self-education expenses", T.CAPS["self_education"], "s.12(1)(e)",
         "Capped at $100,000 a year. Reimbursed amounts are excluded."),
        ("Mandatory MPF contributions by an employee", T.CAPS["mpf_mandatory"], "s.26G",
         "Capped at $18,000 - the statutory maximum mandatory contribution."),
        ("Elderly residential care expenses, per parent or grandparent",
         T.CAPS["elderly_care"], "s.26D",
         "Capped at $110,000 per dependant, and mutually exclusive with the dependent "
         "parent allowance for the same person."),
        ("Home loan interest, without a qualifying child", T.CAPS["home_loan"],
         "ss.26E, 26F",
         "Capped at $100,000, for up to 20 years of assessment, and apportioned among "
         "joint owners or tenants in common by ownership share."),
        ("Qualifying premiums under a VHIS certified plan, per insured person",
         T.CAPS["vhis_per_person"], "ss.26H-26M",
         "Capped at $8,000 per insured person, with no limit on the number of insured "
         "persons."),
        ("Qualifying annuity premiums and MPF voluntary contributions combined",
         T.CAPS["annuity_tvc"], "ss.26N-26U",
         "A single combined cap of $60,000, with tax-deductible voluntary contributions "
         "deducted first."),
        ("Domestic rents for a non-owner-occupier, without a qualifying child",
         T.CAPS["domestic_rent"], "s.26K",
         "Capped at $100,000, rising to $120,000 where there is a qualifying child."),
        ("Assisted reproductive services expenses", T.CAPS["art"], "s.26L",
         "Capped at $100,000, available from YA 2024/25."),
    ]
    for item, cap, ref, why in caps:
        wrong = [c for c in (100000, 120000, 60000, 18000, 110000, 8000, 50000)
                 if c != cap][:3]
        o, a = opts(M(cap), *[M(w) for w in wrong])
        add("B", "Concessionary deductions",
            "What is the maximum annual deduction for the following?<br><em>%s</em>" % item,
            o, a, why, ref, "easy")

    for income, paid in [(1514700, 100000), (490000, 210000), (800000, 350000)]:
        cap = T.donation_cap(income)
        right = min(paid, cap)
        if right == paid:            # the cap bites nothing - claim in full
            o, a = opts(M(right), M(cap), M(paid * 0.35), M(income * 0.25))
        else:                        # the cap bites - the excess lapses
            o, a = opts(M(right), M(paid), M(paid - cap), M(income * 0.25))
        add("B", "Charitable donations",
            "A taxpayer's income after other deductions is %s and approved charitable "
            "donations of %s were paid. What deduction is allowed?" % (M(income), M(paid)),
            o, a,
            "Donations are capped at 35%% of income after the other deductions: 35%% "
            "&times; %s = %s, so the allowable amount is %s. Any excess simply lapses - "
            "there is no carry-forward for salaries tax deductions."
            % (M(income), M(cap), M(right)),
            "s.26C", "medium", "computational")

    o, a = opts("Wholly, exclusively and necessarily incurred in the production of the "
                "assessable income",
                "Incurred to the extent of producing the assessable income",
                "Reasonably incurred in connection with the employment",
                "Incurred for the convenience of the employer")
    add("B", "Deductible outgoings",
        "What is the statutory test for deducting an employee's outgoings and expenses?",
        o, a,
        "Section 12(1)(a) is deliberately stricter than the profits tax test: "
        "<strong>wholly, exclusively and necessarily</strong>, not merely 'to the "
        "extent'. Very few ordinary employment expenses pass it (DIPN 9).",
        "s.12(1)(a)", "medium")

    o, a = opts("Not deductible - it is a domestic or private expense",
                "Deductible in full",
                "Deductible at 50%",
                "Deductible up to $100,000")
    add("B", "Deductible outgoings",
        "How is the cost of travelling between home and the workplace treated?",
        o, a,
        "Home-to-work travel is a domestic or private expense and is expressly outside "
        "s.12(1)(a). Travel <em>between</em> two workplaces in the course of duties is "
        "deductible.", "s.12(1)(a); DIPN 9", "easy")

    # --- allowances ---------------------------------------------------------
    for key, label, ref in [("basic", "the basic allowance", "s.28"),
                            ("married", "the married person's allowance", "s.29"),
                            ("child", "the child allowance for each of the 1st to 9th child", "s.31"),
                            ("dep_parent_60", "the dependent parent allowance for a parent aged 60 or above, not residing with the taxpayer", "s.30"),
                            ("single_parent", "the single parent allowance", "s.32")]:
        cur = T.ALLOWANCES[key][T.CURRENT_YA]
        exam = T.ALLOWANCES[key][T.EXAM_YA]
        o, a = opts(M(exam), M(cur), M(exam * 2), M(cur // 2))
        add("B", "Personal allowances",
            "For the year of assessment <strong>2025/26</strong> - the basis examined "
            "in December 2026 - what is %s?" % label,
            o, a,
            "%s on the exam basis. On the current YA 2026/27 basis it is %s. IRD "
            "publishes 2024/25 and 2025/26 as a single column, so one figure covers "
            "TX-HKG from June 2025 through December 2026."
            % (M(exam), M(cur)),
            ref, "easy")

    o, a = opts("Exactly twice the basic allowance",
                "Two and a half times the basic allowance",
                "One and a half times the basic allowance",
                "The same as the basic allowance")
    add("B", "Personal allowances",
        "What is the relationship between the married person's allowance and the basic "
        "allowance?",
        o, a,
        "The married person's allowance is exactly double the basic. This is why joint "
        "assessment gives a couple nothing on allowances where both already absorb "
        "their own - it only helps where one spouse cannot.", "s.29", "medium")

    o, a = opts("No - the parent must be ordinarily resident in Hong Kong",
                "Yes - holding a Hong Kong identity card is sufficient",
                "Yes, provided the parent is aged 60 or above",
                "Yes, if the taxpayer contributes at least $12,000 a year")
    add("B", "Personal allowances",
        "A taxpayer's mother holds a Hong Kong identity card but lives permanently "
        "outside Hong Kong. Can the dependent parent allowance be claimed?",
        o, a,
        "The parent must be <strong>ordinarily resident in Hong Kong</strong>. An "
        "identity card is evidence, not the test. The June 2026 report names claiming "
        "the allowance for such a parent as a common error.", "s.30", "hard")

    o, a = opts("Only one of them may claim it, as agreed between them",
                "Each may claim half",
                "Both may claim it in full",
                "Neither may claim it")
    add("B", "Personal allowances",
        "Two siblings each contribute to the maintenance of the same dependent parent. "
        "How is the dependent parent allowance given?",
        o, a,
        "Only one person may claim the allowance for any one dependant in a year of "
        "assessment. Where more than one is eligible they must agree; if they cannot, "
        "no one gets it.", "s.30(4)", "medium")

    o, a = opts("Mutually exclusive - only one may be claimed for the same parent",
                "Both may be claimed in full for the same parent",
                "Both may be claimed but each is halved",
                "The allowance is available only if the deduction is not claimed in full")
    add("B", "Personal allowances",
        "What is the relationship between the dependent parent allowance and the "
        "deduction for elderly residential care expenses?",
        o, a,
        "They cannot both be claimed for the same parent in the same year. Compute both "
        "and take whichever is worth more.", "s.26D(5)", "hard")

    # --- computations -------------------------------------------------------
    for ni, allow, label in [(1396700, 145000, "single, basic allowance only"),
                             (266000, 145000, "single, basic allowance only"),
                             (1049800, 145000, "single, basic allowance only"),
                             (600000, 290000, "married, married person's allowance")]:
        prog = T.progressive(ni - allow)
        std = T.standard_rate(ni)
        right = min(prog, std)
        o, a = opts(M(right), M(max(prog, std)), M(T.standard_rate(ni - allow)),
                    M(prog + std))
        add("B", "Computation",
            "A taxpayer's net income before allowances is %s and the allowances claimed "
            "total %s (%s). What is the salaries tax payable, ignoring any one-off "
            "reduction?" % (M(ni), M(allow), label),
            o, a,
            "Compute twice and pay the lower: progressive rates on net chargeable "
            "income of %s give %s; the standard rate on net income of %s - "
            "<strong>before</strong> allowances - gives %s. The lower is %s. Applying "
            "the standard rate to net <em>chargeable</em> income is the single "
            "commonest error in this computation."
            % (M(ni - allow), M(prog), M(ni), M(std), M(right)),
            "s.13", "hard", "computational")

    o, a = opts("15% on the first $5,000,000 of net income and 16% on the remainder",
                "A flat 15% on net income",
                "A flat 16% on net income",
                "15% on net chargeable income")
    add("B", "Standard rate",
        "What is the salaries tax standard rate from the year of assessment 2024/25?",
        o, a,
        "The standard rate became <strong>two-tiered</strong> from YA 2024/25: 15% on "
        "the first $5,000,000 of net income, 16% above. It applies to net income before "
        "personal allowances, and the taxpayer pays the lower of this and the "
        "progressive computation.", "s.13(2)", "medium")

    o, a = opts("2%, 6%, 10% and 14% on four successive bands of $50,000, then 17%",
                "2%, 7%, 12% and 17% on four bands of $50,000",
                "5%, 10% and 15% on three bands of $40,000, then 17%",
                "A flat 15%")
    add("B", "Progressive rates",
        "What are the progressive rates applied to net chargeable income?",
        o, a,
        "Four bands of $50,000 at 2%, 6%, 10% and 14%, then 17% on the remainder. "
        "Unchanged on both the current and the exam basis.", "Sch. 2", "easy")

    o, a = opts("Where one spouse cannot fully absorb their own allowances",
                "Whenever both spouses have income",
                "Whenever the couple have children",
                "Whenever one spouse pays the standard rate")
    add("B", "Joint assessment",
        "When is an election for joint assessment under s.10(2) beneficial?",
        o, a,
        "Only where one spouse's income is too low to absorb their allowances, so the "
        "unused part shelters the other's income. Where both already absorb their own, "
        "the married person's allowance is exactly twice the basic and aggregating "
        "merely drags the lower earner's income into the higher marginal band.",
        "s.10(2)", "hard")

    o, a = opts("The spouse with the higher marginal rate and sufficient cap",
                "The spouse who actually paid them",
                "They must be split equally",
                "The spouse with the lower income")
    add("B", "Charitable donations",
        "A married couple are separately assessed. Which spouse should claim their "
        "approved charitable donations?",
        o, a,
        "Donations may be claimed by either spouse regardless of who paid. Allocate "
        "them to the spouse with the higher marginal rate <strong>and</strong> enough "
        "35% cap to absorb them. The June 2026 report notes candidates failed to "
        "advise this.", "s.26C(3)", "hard")

    # --- more benefits and edge cases -----------------------------------------
    more_benefits = [
        ("An air ticket provided once every two years under an employment contract, "
         "for the employee to visit their home country", True,
         "Home leave passage benefits are assessable in full, whether provided in "
         "kind or reimbursed, under s.9(1)(a) as a reward for services - there is no "
         "exemption for 'home leave' as such."),
        ("A low-interest loan from the employer, where the interest actually charged "
         "is below market rate but is not waived", False,
         "The interest saved on a loan is not itself convertible into money and does "
         "not discharge any liability of the employee, so - unlike a loan later "
         "waived in full or in part - it is outside the charge."),
        ("The employer waiving repayment of an employee loan", True,
         "Waiving a debt discharges the employee's own liability and is assessable "
         "under the s.9(1)(a)(iv) liability test, in contrast to the interest-saved "
         "scenario above where no liability is discharged."),
        ("A cash allowance paid to the employee to cover the cost of meals", True,
         "A cash allowance, however described, is simply additional cash pay and is "
         "fully assessable - contrast free meals provided in kind at the workplace, "
         "which DIPN 41 treats as a non-assessable benefit in specified "
         "circumstances."),
        ("Free meals provided at the employer's canteen on the business premises "
         "during working hours", False,
         "DIPN 41 accepts that meals provided in kind at the workplace are not "
         "assessable, unlike a cash meal allowance which is simply pay."),
        ("A cash bonus tied to the employee remaining in service until a future "
         "date, paid after that date", True,
         "A retention bonus is still a reward for services and is assessable when it "
         "accrues - normally the date the entitlement to it becomes vested, i.e. "
         "when the condition is satisfied, not the date of the underlying "
         "agreement."),
    ]
    for item, taxable, why in more_benefits:
        right = "Assessable" if taxable else "Not assessable"
        other = "Not assessable" if taxable else "Assessable"
        o, a = opts(right, other, "Assessable only if the employee is a director",
                    "Assessable only at 50% of the value")
        add("B", "Fringe benefits",
            "How is the following treated for salaries tax purposes?<br><em>%s</em>" % item,
            o, a, why, "s.9; DIPN 41", "medium")

    o, a = opts("The date the employee becomes entitled to the income - normally "
                "when the services giving rise to it have been rendered",
                "The date the income is actually paid into the employee's bank "
                "account",
                "The date the employment contract was originally signed",
                "The end of the year of assessment in which the amount is finally "
                "quantified")
    add("B", "Timing of income",
        "A discretionary bonus for the year ended 31 March 2026 is only decided by "
        "the board and paid in July 2026. In which year of assessment does it "
        "accrue?",
        o, a,
        "Income accrues when the employee becomes entitled to it. A discretionary "
        "bonus is not accrued until the discretion is actually exercised, so it falls "
        "into the year of assessment in which the board's decision is made and the "
        "entitlement crystallises - here 2026/27, not the earlier year the bonus "
        "related to and not simply the date of payment.", "s.11D", "hard")

    o, a = opts("Assessable in the year the option is granted, on its value at "
                "grant, with no further charge on exercise",
                "Assessable in the year the option is exercised, assigned or "
                "released, on the gain realised then",
                "Never assessable, being a capital gain on shares",
                "Assessable equally over the vesting period, year by year")
    add("B", "Share options",
        "How is a gain on a share option granted to an employee normally taxed, "
        "where the option itself has no ascertainable market value at grant?",
        o, a,
        "Where an option cannot be valued when granted - the usual case for an "
        "employee share option - no charge arises at grant. The charge instead falls "
        "in the year the option is exercised, assigned or released, on the "
        "difference between the market value of the shares and the exercise price "
        "paid.", "s.9(1)(d); DIPN 38", "medium")

    o, a = opts("The employee is treated as having elected to defer the option gain, "
                "but must include it within 3 years of the grant even if not yet "
                "exercised, assigned or released",
                "The gain simply escapes salaries tax if the option is still unexer"
                "cised after 3 years",
                "The employee must pay tax annually on the unrealised paper gain",
                "The 3-year rule only applies to options over shares in a listed "
                "company")
    add("B", "Share options",
        "What is the effect of the 'deemed exercise' rule where a share option "
        "remains unexercised for a long period?",
        o, a,
        "To stop indefinite deferral, an employee share option must be brought into "
        "charge within 3 years of the date of grant even if it has not by then been "
        "exercised, assigned or released, valuing the gain as if it had been "
        "exercised at that point.", "s.9(1)(d); DIPN 38", "hard")

    o, a = opts("Deductible up to the actual mandatory contribution, capped at "
                "$18,000, even where the employee is also a member of a "
                "recognised occupational retirement scheme",
                "Not deductible at all - only the employer's contributions count",
                "Deductible without limit",
                "Deductible only if the employee is self-employed")
    add("B", "MPF contributions",
        "An employee contributes to the mandatory tier of their MPF scheme. How is "
        "the deduction restricted?",
        o, a,
        "Section 26G caps the deduction at the amount that would be required as a "
        "mandatory contribution, currently capped at $18,000 a year - "
        "voluntary top-ups beyond the mandatory amount get no deduction at all under "
        "salaries tax.", "s.26G", "medium")

    o, a = opts("A person's total tax for the year is reduced by a percentage, up to "
                "a specified cap, announced separately each year in the Budget",
                "It is a permanent reduction in the tax rates, written into the "
                "Ordinance",
                "It applies automatically to provisional tax but never to final tax",
                "It applies only to taxpayers earning below the basic allowance")
    add("B", "One-off relief",
        "What is the nature of the one-off salaries tax reduction the Financial "
        "Secretary has announced in several recent Budgets?",
        o, a,
        "It is a one-off, Budget-announced concession - a percentage reduction of "
        "the final tax payable, subject to a specified dollar cap for that year of "
        "assessment - and needs separate legislation each time; it is not a "
        "permanent feature of the Inland Revenue Ordinance and a candidate should "
        "not assume it repeats automatically without being told.", "", "medium")

    o, a = opts("A married person whose spouse has little or no income of their own",
                "A married person whose spouse also earns a substantial salary and "
                "fully uses their own allowances",
                "An unmarried taxpayer with no dependants",
                "A taxpayer who has already elected personal assessment")
    add("B", "Joint assessment",
        "For which taxpayer is an election for joint assessment under s.10(2) most "
        "likely to be worthwhile?",
        o, a,
        "Joint assessment only helps where one spouse's own income cannot absorb "
        "their personal allowances - the unused portion then shelters the other "
        "spouse's income. Where both spouses already have enough income to use their "
        "own allowances, joint assessment achieves nothing and can even push income "
        "into a higher marginal band.", "s.10(2)", "medium")

    o, a = opts("A person is regarded as married throughout the year of assessment if "
                "married for any part of it, but the allowance is time-apportioned "
                "only in the year of marriage or divorce for certain allowances, not "
                "the married person's allowance itself",
                "The married person's allowance is always time-apportioned by the "
                "number of months of the marriage",
                "No allowance at all is given in the year of marriage",
                "The full married person's allowance requires the marriage to have "
                "subsisted for the whole year")
    add("B", "Personal allowances",
        "A couple marry partway through the year of assessment. How is the married "
        "person's allowance affected?",
        o, a,
        "The married person's allowance is an all-or-nothing allowance for the whole "
        "year if the couple were married for any part of the year of assessment - it "
        "is not time-apportioned by the number of months married, unlike some other "
        "reliefs that do prorate.", "s.29", "hard")

    o, a = opts("A child born during the year still qualifies for the full child "
                "allowance for that year - it is not time-apportioned either",
                "The child allowance is apportioned by the number of months the "
                "child was alive during the year",
                "No child allowance is given in the year of birth",
                "Only half the child allowance is given in the year of birth")
    add("B", "Personal allowances",
        "A taxpayer's child is born in November, partway through the year of "
        "assessment. How much child allowance can be claimed for that year?",
        o, a,
        "Like the married person's allowance, the child allowance is not "
        "time-apportioned - the full annual amount is given for the year of birth, "
        "and again for the year the child ceases to qualify (for instance turning "
        "18 without continuing full-time education).", "s.31", "medium")

    o, a = opts("An additional one-ninth of the basic child allowance for that child, "
                "given only in the year of birth",
                "Double the ordinary child allowance in the year of birth",
                "No additional allowance is available",
                "An additional allowance equal to the elderly residential care cap")
    add("B", "Personal allowances",
        "What additional, one-off allowance is available in the year a child is "
        "born, on top of the ordinary child allowance for that child?",
        o, a,
        "An additional child allowance is given for the year of birth - it is not "
        "an extra allowance in every year, only the birth year - to help offset the "
        "immediate costs of a new baby.", "s.31", "hard")

    o, a = opts("The taxpayer must have maintained the child, wholly or "
                "substantially at the taxpayer's own expense, and the child must be "
                "under 18, or under 25 and receiving full-time education, or "
                "incapacitated for work",
                "Only children under 12 qualify",
                "The child must live in the same household as the taxpayer at all "
                "times",
                "Only the taxpayer's own biological children qualify - not adopted "
                "or step-children")
    add("B", "Personal allowances",
        "What are the basic conditions for claiming the child allowance?",
        o, a,
        "The child must be maintained by the claimant, be unmarried, and be either "
        "under 18, or under 25 and still receiving full-time education, or "
        "incapacitated for work by physical or mental disability - and 'child' "
        "includes an adopted child, a step-child and an illegitimate child, not only "
        "a legitimate biological one.", "s.2, s.31", "medium")


# ===========================================================================
# AREA D - Property tax  (target 36)
# ===========================================================================
def area_d():
    o, a = opts("15% of the net assessable value", "15% of the assessable value",
                "16.5% of the net assessable value", "20% of the rent received")
    add("D", "Charge", "On what basis is property tax charged?",
        o, a,
        "Property tax is charged at the standard rate of 15% on the net assessable "
        "value of land or buildings in Hong Kong, on the owner.", "s.5", "easy")

    o, a = opts("Consideration payable to or for the benefit of the owner for the right "
                "to use the property",
                "The open market rental value of the property",
                "The rateable value assessed by the Rating and Valuation Department",
                "Rent actually received in cash during the year")
    add("D", "Assessable value", "What is the assessable value of a property?",
        o, a,
        "Section 5B(2) assesses the consideration <strong>payable</strong>, in money or "
        "money's worth, for the right of use - not the market rent, not the rateable "
        "value, and on an accruals rather than a receipts basis.", "s.5B(2)", "medium")

    for rent, rates in [(25000, 9000), (40000, 16000), (18000, 6500), (60000, 24000)]:
        av = rent * 12
        nav = T.net_assessable_value(rent=av, rates_paid_by_owner=rates)
        tax = T.property_tax(nav)
        o, a = opts(M(tax), M(av * 0.15), M((av - rates) * 0.15),
                    M(av * 0.8 * 0.15))
        add("D", "Computation",
            "A property was let for the whole year at %s a month. The owner paid rates "
            "of %s. The tenant paid management fees direct to the building manager. "
            "What is the property tax payable?" % (M(rent), M(rates)),
            o, a,
            "Assessable value %s; less rates paid <strong>by the owner</strong> %s = "
            "%s; less the 20%% statutory allowance %s = net assessable value %s; "
            "&times; 15%% = %s. Management fees paid by the tenant to a third party "
            "never enter the computation at all."
            % (M(av), M(rates), M(av - rates), M((av - rates) * 0.2), M(nav), M(tax)),
            "ss.5, 5(1A)", "medium", "computational")

    # Only terms longer than 36 months are used here: at 36 months or less the
    # 36-month cap and the actual term give the same figure, so there would be
    # no distractor to offer. The short-lease case is asked separately below.
    for premium, term in [(240000, 48), (300000, 60), (210000, 42), (480000, 72)]:
        per_year = premium / min(term, 36) * 12
        o, a = opts(M(per_year), M(premium / term * 12), M(premium), "Nil - a premium "
                    "is a capital receipt")
        add("D", "Premium",
            "A premium of %s is received on the grant of a lease for %d months. How "
            "much is included in the assessable value for a full year?"
            % (M(premium), term),
            o, a,
            "A premium is spread over the lease term <strong>but capped at 36 "
            "months</strong>: %s over %d months = %s a year. Spreading over the full "
            "%d months gives %s and is wrong wherever the term exceeds three years."
            % (M(premium), min(term, 36), M(per_year), term, M(premium / term * 12)),
            "s.5B(4)", "medium", "computational")

    o, a = opts("$60,000 - the same figure either way",
                "$120,000 - the premium is taxed in the year of receipt",
                "$40,000 - spread over 36 months regardless of the term",
                "Nil - a premium for a lease of under three years is exempt")
    add("D", "Premium",
        "A premium of $120,000 is received on the grant of a lease for 24 months. How "
        "much is included in the assessable value for a full year?",
        o, a,
        "The spread is over the lease term <strong>or</strong> 36 months, whichever is "
        "<em>shorter</em>. At 24 months the term is shorter, so $120,000 &divide; 24 "
        "&times; 12 = $60,000. The 36-month cap only bites on leases longer than three "
        "years.", "s.5B(4)", "medium", "computational")

    o, a = opts("In the year the rent is proved to be irrecoverable",
                "In the year the rent accrued",
                "Spread over the remaining term of the lease",
                "Only when the tenant is formally declared bankrupt")
    add("D", "Irrecoverable rent",
        "In which year of assessment is irrecoverable rent deducted?",
        o, a,
        "Section 7C(1) gives the deduction in the year the rent is <strong>recognised "
        "as irrecoverable</strong>, not the year it accrued.", "s.7C(1)", "medium")

    o, a = opts("Assessable in the year of recovery",
                "Related back to the year in which it was written off",
                "Not assessable, having already been taxed",
                "Assessable at 50% in the year of recovery")
    add("D", "Recovery of bad rent",
        "Rent previously deducted as irrecoverable is later recovered. How is it treated?",
        o, a,
        "It is treated as assessable value in the year of recovery. It is not related "
        "back to the year of the original deduction.", "s.7C(2)", "medium")

    o, a = opts("It is set off against the irrecoverable rent",
                "It is exempt as a capital receipt",
                "It is assessable in full in addition to the irrecoverable rent deduction",
                "It reduces the 20% statutory allowance")
    add("D", "Rental deposit",
        "A tenant defaults and the owner forfeits and retains the rental deposit. How "
        "is the forfeited deposit treated?",
        o, a,
        "The forfeited deposit is set off against the irrecoverable rent, reducing the "
        "deduction. Note the contrast: a deposit merely <em>taken</em> at the start of "
        "a lease is not assessable income at all - it is security held for the tenant. "
        "The June 2026 report names both errors.", "s.7C", "hard")

    o, a = opts("20% of the assessable value after deducting rates paid by the owner",
                "20% of the assessable value before deducting rates",
                "20% of the rent actually received",
                "The actual cost of repairs, up to 20%")
    add("D", "Statutory allowance",
        "How is the statutory allowance for repairs and outgoings computed?",
        o, a,
        "It is a fixed 20% of the assessable value <strong>after</strong> the owner's "
        "rates. Taking it before rates, or deducting irrecoverable rent after it, both "
        "corrupt the figure.", "s.5(1A)(b)(ii)", "medium")

    nondeduct = [
        ("Government rent paid by the owner", "Not deductible"),
        ("Mortgage interest paid by the owner", "Not deductible"),
        ("The actual cost of repairing the roof", "Not deductible"),
        ("The cost of replacing air-conditioners", "Not deductible"),
        ("Rates paid by the owner", "Deductible"),
        ("Rates paid by the tenant direct to the Government", "Not deductible"),
    ]
    for item, right in nondeduct:
        other = "Deductible" if right == "Not deductible" else "Not deductible"
        o, a = opts(right, other, "Deductible at 50%",
                    "Deductible only if supported by receipts")
        add("D", "Deductions",
            "In computing net assessable value, how is the following treated?"
            "<br><em>%s</em>" % item,
            o, a,
            "Only rates paid <strong>by the owner</strong> are deducted. Everything "
            "else - Government rent, mortgage interest, actual repairs, replacements - "
            "is deemed to be covered by the 20% statutory allowance, however much was "
            "really spent. There are no depreciation allowances under property tax.",
            "s.5(1A)", "medium")

    o, a = opts("No depreciation allowance is available under property tax",
                "An annual allowance of 4% of cost",
                "An initial allowance of 20% plus 4% annually",
                "A 100% deduction as a prescribed fixed asset")
    add("D", "Depreciation",
        "What depreciation allowance is available for plant installed in a property let "
        "by an individual and charged to property tax?",
        o, a,
        "None. Part 6 does not apply to the property tax charge - the 20% statutory "
        "allowance is the only relief. If the owner is a company carrying on business "
        "the income falls within profits tax instead, where allowances are available.",
        "Part 6", "hard")

    o, a = opts("Separately, property by property",
                "On the aggregate of all properties owned",
                "Separately, unless the properties are in the same building",
                "On the aggregate, with a single 20% allowance")
    add("D", "Multiple properties",
        "A taxpayer owns three let properties. How is property tax computed?",
        o, a,
        "Property by property: each gets its own assessable value, its own rates "
        "deduction and its own 20% allowance. Aggregating them is named in the June "
        "2026 report.", "s.5", "medium")

    o, a = opts("It may apply for exemption, the income being chargeable to profits tax "
                "instead",
                "It is exempt automatically with no application",
                "It pays both property tax and profits tax with no relief",
                "It pays property tax at 8.25%")
    add("D", "Corporate owners",
        "A Hong Kong company carrying on business lets a property it owns. What relief "
        "is available from property tax?",
        o, a,
        "Section 5(2)(a) allows a corporation carrying on a trade or business in Hong "
        "Kong to apply for exemption from property tax where the income is included in "
        "its profits tax computation. Without an application, property tax is charged "
        "and set off under s.25.", "s.5(2)(a)", "hard")

    o, a = opts("Set off against the profits tax payable",
                "Deducted as an expense in the profits tax computation",
                "Refunded automatically",
                "Carried forward as a tax credit indefinitely")
    add("D", "Set-off",
        "A company pays property tax on a let property and the rental income is also "
        "assessed to profits tax. How is the property tax relieved?",
        o, a,
        "Section 25 sets the property tax paid <strong>off against the profits tax "
        "payable</strong>. Separately, the property tax charged in the accounts must be "
        "added back in the computation - it is two adjustments in two places from one "
        "fact.", "s.25", "hard")

    o, a = opts("The owner", "The tenant", "The property manager",
                "Whoever actually receives the rent")
    add("D", "Chargeable person", "On whom is property tax charged?",
        o, a,
        "On the owner of the land or buildings, which includes a beneficial owner, a "
        "life tenant, a mortgagor in possession and a person holding under a Government "
        "lease.", "ss.2, 5", "easy")

    o, a = opts("Nothing is assessable for the rent-free months",
                "The market rent is assessed for the rent-free months",
                "The rent for the whole year is averaged across 12 months",
                "The rent-free period is ignored and full rent assessed")
    add("D", "Rent-free period",
        "A lease grants two rent-free months at the start. How are those months treated?",
        o, a,
        "No consideration is payable for those months, so nothing enters the assessable "
        "value. Including the rent-free period is named in the June 2026 report.",
        "s.5B(2)", "medium")

    o, a = opts("Corporation profits tax at 8.25%/16.5%, with a full credit for the "
                "property tax already paid, so the tax on the rental profit is not "
                "duplicated",
                "Both property tax and profits tax in full, with no relief at all",
                "Only property tax; the profits tax return simply omits the rent",
                "Only profits tax; property tax is waived automatically for companies")
    add("D", "Corporate owners",
        "A company lets a property and does not apply for the s.5(2)(a) property tax "
        "exemption. It reports the rental income in its profits tax computation as "
        "well. How does the tax actually payable work out?",
        o, a,
        "Property tax is charged in the ordinary way, and the rental profit is also "
        "brought into the profits tax computation (with the property tax itself added "
        "back as a disallowable expense), but s.25 then sets the property tax paid "
        "off against the profits tax payable, so the company is not really taxed "
        "twice on the same rent - it is simply an awkward two-step mechanism instead "
        "of a straightforward exemption.", "ss.5(2)(a), 25", "hard")

    o, a = opts("No - property tax has no concept of a loss; each property stands on "
                "its own and a negative net assessable value is simply nil",
                "Yes - the loss can be carried forward against future property tax",
                "Yes - the loss can be set against the same owner's salaries tax",
                "Yes - but only if the owner elects personal assessment for that "
                "year")
    add("D", "Losses",
        "A let property's outgoings (rates paid by the owner, for example) exceed "
        "the rent receivable for the year. Can the resulting 'loss' be used anywhere "
        "in the property tax system itself?",
        o, a,
        "Property tax simply has no loss concept - the 20% statutory allowance and "
        "owner's rates can reduce the assessable value to nil but never below it, and "
        "there is nothing to carry forward within property tax. The only route to any "
        "further relief is for the individual to elect personal assessment, which is "
        "a different tax mechanism entirely.", "s.5", "medium")

    o, a = opts("The market rent that would have been charged to an unconnected "
                "tenant, not the token rent actually paid",
                "The token rent actually paid, however low",
                "Nil - a nominal rent is treated as no consideration at all",
                "Half of the market rent as a compromise")
    add("D", "Assessable value",
        "A property is let to a relative at a nominal rent well below the market "
        "rate. On what value is property tax charged?",
        o, a,
        "Section 5B(2A) charges the property tax on the consideration that would "
        "have been payable if the letting were at arm's length, where the actual "
        "rent is less than the market rent because of the relationship between the "
        "parties.", "s.5B(2A)", "hard")

    o, a = opts("As if a new letting had started - a fresh assessable value is set "
                "based on the new agreed rent from the renewal date",
                "The original assessable value continues unchanged until the lease "
                "finally ends",
                "No property tax is chargeable during the renewal negotiation period",
                "The higher of the old and new rent is always used")
    add("D", "Lease renewal",
        "A tenancy is renewed at a materially higher rent partway through the year. "
        "How is the assessable value affected?",
        o, a,
        "The assessable value simply follows whatever consideration is actually "
        "payable for each part of the year - the old rent up to renewal, the new, "
        "higher rent from the renewal date - exactly as any change in the rent under "
        "the lease would be reflected.", "s.5B(2)", "medium")

    o, a = opts("The government rent is not deductible by the owner, whether paid by "
                "the owner or the tenant",
                "Government rent paid by the owner is deductible, just like rates",
                "Government rent is only deductible if the property is a flat",
                "Government rent is deducted before computing the assessable value, "
                "not after")
    add("D", "Deductions",
        "How does Government rent (as distinct from general rates) affect the "
        "property tax computation?",
        o, a,
        "Only <strong>rates</strong> paid by the owner are a specific deduction under "
        "s.5(1A). Government rent is not separately deductible at all - like "
        "mortgage interest and repair costs, it is deemed to be covered by the 20% "
        "statutory allowance, however much is actually paid.", "s.5(1A)", "medium")

    for rent, months_vacant in [(20000, 2), (35000, 3)]:
        av = rent * (12 - months_vacant)
        nav = T.net_assessable_value(rent=av)
        tax = T.property_tax(nav)
        o, a = opts(M(tax), M(T.property_tax(T.net_assessable_value(rent=rent * 12))),
                    M(round(av * 0.15, 2)), M(round(rent * 12 * 0.15, 2)))
        add("D", "Vacant periods",
            "A property let at %s a month stood genuinely vacant, with no tenant and "
            "no rent receivable, for %d months of the year. What is the property tax "
            "payable for the year?" % (M(rent), months_vacant),
            o, a,
            "No rent accrues for a period the property is genuinely vacant between "
            "tenancies, so the assessable value covers only the %d months it was "
            "actually let: %s &times; %d = %s. Charging property tax on a full "
            "12 months' notional rent, as if vacancy made no difference, is the "
            "error to avoid - property tax is not a tax on ownership, only on "
            "consideration actually receivable."
            % (12 - months_vacant, M(rent), 12 - months_vacant, M(av)),
            "s.5B(2)", "medium", "computational")

    o, a = opts("It has no bearing on property tax at all - property tax is a "
                "separate charge on the owner regardless of the tenant's own tax "
                "position",
                "The owner's property tax is reduced if the tenant also pays "
                "salaries tax",
                "Property tax is waived if the tenant is a charity",
                "The owner must obtain the tenant's tax reference number before "
                "filing")
    add("D", "Charge",
        "Does it make any difference to the owner's property tax whether the tenant "
        "uses the property for a business, as a residence, or as a charity's office?",
        o, a,
        "None. Property tax is charged on the owner by reference to the rent "
        "receivable, entirely independent of what the tenant does with the property "
        "or the tenant's own tax status.", "s.5", "easy")


# ===========================================================================
# AREA E - Personal assessment  (target 39)
# ===========================================================================
def area_e():
    o, a = opts("It is a relief, not a separate head of charge",
                "It is a fourth head of charge alongside the other three",
                "It is compulsory for anyone with more than one source of income",
                "It applies automatically where it reduces tax")
    add("E", "Nature", "What is personal assessment?",
        o, a,
        "Personal assessment is an <strong>election</strong> that re-computes income "
        "already chargeable under the three heads at progressive rates after "
        "allowances. It never makes non-chargeable income chargeable, and it is never "
        "automatic.", "s.41", "easy")

    o, a = opts("A taxpayer whose only income is employment income",
                "A sole proprietor with a mortgaged let property",
                "An individual partner with a share of a partnership loss",
                "A property owner paying mortgage interest")
    add("E", "When it helps",
        "For which of the following can electing personal assessment produce no benefit "
        "at all?",
        o, a,
        "Salaries tax already applies progressive rates and personal allowances, so "
        "there is nothing for the election to unlock. Personal assessment helps only "
        "where there is property income or unincorporated business profit charged at "
        "the standard rate with no allowances.", "s.41", "medium")

    o, a = opts("18, or under 18 if both parents are dead",
                "18 in all cases, with no exception",
                "21, or 18 if married",
                "There is no age requirement")
    add("E", "Eligibility", "What is the age requirement for electing personal assessment?",
        o, a, "The elector must be 18 or over, or under that age if both parents are "
        "dead.", "s.41(1)", "easy")

    o, a = opts("More than 180 days in the year, or more than 300 days in two "
                "consecutive years including the year of election",
                "More than 60 days in the year of assessment",
                "More than 183 days in the year of assessment",
                "At least 90 days in each of two consecutive years")
    add("E", "Eligibility", "What makes a person a 'temporary resident' for personal "
        "assessment?",
        o, a,
        "Either limb suffices. Contrast 'ordinarily resident', which is a factual test "
        "about residing voluntarily and for a settled purpose with sufficient "
        "continuity - a permanent identity card is evidence of it, not the test.",
        "s.41(4)", "hard")

    o, a = opts("The elector must personally be ordinarily resident or a temporary "
                "resident",
                "The elector or their spouse may satisfy the residence test",
                "Only Hong Kong permanent residents may elect",
                "There is no residence requirement")
    add("E", "Eligibility",
        "From the year of assessment 2018/19, how is the residence condition satisfied?",
        o, a,
        "From 2018/19 the elector must qualify on their <strong>own</strong> residence. "
        "Up to 2017/18 a married person could rely on the spouse's status; that route "
        "is closed.", "s.41(1)", "hard")

    o, a = opts("Either spouse may elect separately, or they may elect jointly",
                "The election must always be made by both spouses jointly",
                "Only the higher-earning spouse may elect",
                "Married persons cannot elect at all")
    add("E", "Married couples",
        "From the year of assessment 2018/19, how may a married person elect for "
        "personal assessment?",
        o, a,
        "The Inland Revenue (Amendment) (No. 9) Ordinance 2018 introduced separate "
        "election from YA 2018/19. Before that a joint election was mandatory where "
        "both had income, so one spouse could veto it.",
        "Inland Revenue (Amendment) (No. 9) Ordinance 2018", "hard")

    o, a = opts("The election must be made by them jointly",
                "Either may still elect separately",
                "Neither may elect",
                "Only the spouse with the higher income may elect")
    add("E", "Married couples",
        "A couple are jointly assessed under salaries tax. How must any personal "
        "assessment election be made?",
        o, a,
        "Where the couple is already jointly assessed under s.10(2), the personal "
        "assessment election must also be joint. They cannot split for one and not the "
        "other.", "s.41(1A)", "hard")

    o, a = opts("In the ratio of each spouse's reduced total income",
                "Equally between them",
                "In the ratio of their gross incomes",
                "Entirely to the spouse with the higher income")
    add("E", "Married couples",
        "Where a couple elect jointly, how is the total tax apportioned between them?",
        o, a,
        "In proportion to each spouse's <strong>reduced</strong> total income - after "
        "interest and concessionary deductions, not gross. Each then receives their own "
        "notice of assessment.", "s.42(2)", "hard")

    o, a = opts("The later of 2 years after the end of the year of assessment and 2 "
                "months after a notice of assessment",
                "Within 1 year of the end of the year of assessment",
                "Within 6 months of the notice of assessment",
                "Before the tax return for that year is filed")
    add("E", "Time limits", "By when must an election for personal assessment be made?",
        o, a,
        "For YA 2026/27 that means not later than 31 March 2029, or two months after a "
        "notice of assessment or additional assessment, whichever is later.",
        "s.41(2)", "medium")

    o, a = opts("Within 6 months of the date the personal assessment is issued",
                "Within 2 years of the end of the year of assessment",
                "Within 1 month of the assessment",
                "At any time before the assessment becomes final")
    add("E", "Time limits", "By when must an election for personal assessment be "
        "withdrawn?",
        o, a,
        "Six months, or such longer period as the Commissioner considers reasonable. "
        "Where the election was joint, the withdrawal must be joint too. After "
        "withdrawal the taxpayer may not elect again for that year without the "
        "Commissioner's agreement.", "s.41(3)", "hard")

    o, a = opts("His executor has the same right of election",
                "The right of election lapses on death",
                "Only the Commissioner may elect on the deceased's behalf",
                "The surviving spouse alone may elect")
    add("E", "Deceased taxpayer",
        "A person eligible to elect for personal assessment dies before doing so. What "
        "happens to the right of election?",
        o, a,
        "The executor has the same right over the deceased's total income as the "
        "deceased would have had.", "s.41", "medium")

    o, a = opts("Net assessable value, net assessable income, and net assessable profits",
                "Gross rent, gross salary and gross business receipts",
                "Assessable value, assessable income and assessable profits",
                "Only income charged at the standard rate")
    add("E", "Computation",
        "Which figures are aggregated to arrive at total income under personal "
        "assessment?",
        o, a,
        "Property enters at <strong>net assessable value</strong> - after rates and the "
        "20% allowance - employment at net assessable income, and business at net "
        "assessable profits after losses brought forward and donations already relieved. "
        "Bringing property in at gross rent is a reported error.", "s.42", "hard")

    o, a = opts("Restricted to the net assessable value of that property",
                "Unlimited",
                "Restricted to $100,000",
                "Restricted to 20% of the rent")
    add("E", "Interest deduction",
        "How much interest on money borrowed to produce property income may be deducted "
        "under personal assessment?",
        o, a,
        "Capped at the net assessable value of that individual property (Board of "
        "Review D51/04). The excess lapses; it cannot create or increase a loss. This "
        "is a different relief from home loan interest under ss.26E/26F, which is "
        "capped at $100,000 and relates to a dwelling the taxpayer occupies.",
        "s.42(1); D51/04", "hard")

    o, a = opts("The standard rate on reduced total income",
                "The standard rate on net chargeable income",
                "The progressive rates on reduced total income",
                "16.5% on assessable profits")
    add("E", "Computation",
        "Tax under personal assessment is the lower of the progressive rates on net "
        "chargeable income and what?",
        o, a,
        "The standard rate applies to <strong>reduced total income</strong> - before "
        "personal allowances. Applying it to net chargeable income uses the wrong base "
        "and understates the cap.", "s.43", "hard")

    for ti, interest, allow in [(1420000, 0, 145000), (1058400, 200000, 290000),
                                (884000, 42000, 145000)]:
        r = T.personal_assessment(ti, interest=interest, allowances_total=allow)
        o, a = opts(M(r["payable"]), M(max(r["progressive"], r["standard"])),
                    M(T.standard_rate(r["nci"])), M(r["progressive"] + r["standard"]))
        add("E", "Computation",
            "Total income under personal assessment is %s, interest to produce property "
            "income is %s, and allowances total %s. What is the tax payable?"
            % (M(ti), M(interest), M(allow)),
            o, a,
            "Reduced total income %s; less allowances = net chargeable income %s. "
            "Progressive rates give %s; the standard rate on <strong>reduced total "
            "income</strong> gives %s. The lower is %s."
            % (M(r["rti"]), M(r["nci"]), M(r["progressive"]), M(r["standard"]),
               M(r["payable"])),
            "s.43", "hard", "computational")

    o, a = opts("It can be set against the taxpayer's other income in the same year",
                "It must be carried forward against future business profits only",
                "It is lost",
                "It can be surrendered to a spouse only")
    add("E", "Business losses",
        "What is the effect of electing personal assessment on a sole proprietorship "
        "loss of the year?",
        o, a,
        "This is one of the two main reasons to elect. Without the election the loss is "
        "stranded in the profits tax computation and merely carried forward; personal "
        "assessment lets it shelter current-year salary and property income.",
        "s.42(1)", "medium")

    o, a = opts("It cannot be brought in - offshore profits were never chargeable",
                "It can be set against Hong Kong income in full",
                "It can be set against Hong Kong income at 50%",
                "It may be carried forward under personal assessment")
    add("E", "Business losses",
        "Can an offshore business loss be brought into a personal assessment "
        "computation?",
        o, a,
        "No. Personal assessment aggregates income <strong>chargeable</strong> under the "
        "three heads. Profits that were never chargeable bring no loss relief either - "
        "the rule cuts both ways.", "s.42", "hard")

    o, a = opts("No - the marginal progressive rate exceeds the standard rate",
                "Yes - progressive rates are always lower",
                "Yes - allowances always produce a saving",
                "It makes no difference to the tax payable")
    add("E", "When it helps",
        "A taxpayer with substantial salary income also owns an unmortgaged let "
        "property. Is personal assessment likely to be beneficial?",
        o, a,
        "Above roughly $200,000 of net chargeable income the marginal progressive rate "
        "is 17%, against a 15% standard rate. Aggregating the property income drags it "
        "up to 17%, and there is no mortgage interest or loss for the election to "
        "unlock. Compute both ways - never assume.", "s.43", "hard")

    o, a = opts("A company", "A sole proprietor", "An individual partner",
                "An individual with property income")
    add("E", "Eligibility", "Which of the following cannot elect for personal assessment?",
        o, a,
        "Personal assessment is available to <strong>individuals</strong> only. A "
        "corporate partner is assessed on its share at corporate rates and that is the "
        "end of it.", "s.41", "medium")

    o, a = opts("In writing, in the tax return or on Form IR76C",
                "Orally, by telephoning the Inland Revenue Department",
                "By simply paying the lower amount of tax",
                "By ticking a box on the demand note")
    add("E", "Making the election", "How must an election for personal assessment be made?",
        o, a, "The election must be in writing - in practice by completing the relevant "
        "section of the tax return, or on Form IR76C.", "s.41(2)", "easy")

    o, a = opts("The higher of the two allowances - not both",
                "Both allowances in full, one after the other",
                "Neither allowance, since personal assessment has its own separate "
                "scale",
                "Half of each allowance")
    add("E", "Computation",
        "A married couple elect for personal assessment. What allowance may they "
        "claim between them for their marital status?",
        o, a,
        "The married person's allowance under personal assessment works the same way "
        "as under salaries tax - one married couple gets one married person's "
        "allowance (or, unmarried, each their own basic allowance), never both a "
        "basic and a married allowance stacked together.", "s.42A", "medium")

    o, a = opts("Yes - each qualifying child allowance, dependent parent allowance and "
                "so on is available under personal assessment exactly as under "
                "salaries tax",
                "No - personal assessment allows only the basic or married allowance, "
                "with no allowance for children or dependants",
                "Only the child allowance is available; dependent parent and sibling "
                "allowances are not",
                "Allowances are halved under personal assessment")
    add("E", "Computation",
        "Are child, dependent parent, dependent sibling, and disability allowances "
        "available under a personal assessment computation?",
        o, a,
        "The full suite of personal allowances under Part V (basic, married, child, "
        "dependent parent, dependent sibling, single parent, disabled dependant, "
        "personal disability) is available to reduce reduced total income to net "
        "chargeable income, exactly as in a salaries tax computation.", "s.42A",
        "medium")

    o, a = opts("Yes - the same concessionary deductions (self-education expenses, "
                "home loan interest, MPF contributions, elderly residential care "
                "expenses, approved charitable donations, and so on) are all "
                "available",
                "No concessionary deductions are available under personal assessment",
                "Only home loan interest is available; the others are salaries-tax "
                "only",
                "Concessionary deductions are capped at half their normal limits "
                "under personal assessment")
    add("E", "Computation",
        "Are the concessionary deductions available under salaries tax (self-"
        "education expenses, home loan interest, elderly residential care expenses, "
        "MPF contributions, approved charitable donations) also available under "
        "personal assessment?",
        o, a,
        "Yes, at the same statutory caps, deducted from total income before "
        "arriving at reduced total income - alongside the personal-assessment-"
        "specific deductions for business losses and interest to produce property "
        "income that salaries tax alone does not offer.", "s.42", "medium")

    o, a = opts("No - each source of income keeps its own basis; property income is "
                "still computed on an accruals basis and business profits on the "
                "normal profits tax basis, merely aggregated afterwards",
                "Yes - personal assessment recomputes every source of income on a "
                "cash receipts basis",
                "Only property income is recomputed; business profits keep their "
                "normal basis",
                "Personal assessment abolishes the concept of a basis period "
                "entirely")
    add("E", "Computation",
        "Does electing personal assessment change how income from each individual "
        "source (property, employment, business) is itself computed?",
        o, a,
        "Personal assessment is purely a <strong>re-aggregation and re-rating</strong> "
        "mechanism. Each source's net assessable value, net assessable income or "
        "assessable profits is computed exactly as it would be under the ordinary "
        "property tax, salaries tax or profits tax rules, and only then are the "
        "results added together and taxed afresh.", "s.42", "medium")

    o, a = opts("A property is jointly owned by a married couple; only the spouse "
                "who elects personal assessment includes their own share",
                "A property is solely owned by one spouse and let for the whole year",
                "A sole trader's business runs at a loss for the year",
                "A taxpayer pays substantial home loan interest with little other "
                "income to absorb allowances")
    add("E", "When it helps",
        "In which of the following is personal assessment LEAST likely to produce "
        "any tax saving?",
        o, a,
        "Where a property is solely owned and let for the whole year with no "
        "mortgage, there is nothing for personal assessment to unlock - no loss to "
        "use, no interest to deduct beyond what property tax itself already sets off "
        "against rates, and the standard rate on that income alone is likely to beat "
        "the progressive computation once it is aggregated with other income. Always "
        "compute the tax both ways rather than assuming.", "", "hard")

    o, a = opts("The whole family's tax position, computed both with and without the "
                "election, for each spouse separately and jointly",
                "Only the spouse with the higher income",
                "The election is never worth comparing - it should always be made "
                "if available",
                "Only the spouse who owns the let property")
    add("E", "Practical approach",
        "In an exam question asking whether a married couple should elect for "
        "personal assessment, what should the answer actually compare?",
        o, a,
        "Compute the total family tax bill under each realistic combination - "
        "no election, each spouse electing separately, and a joint election - and "
        "recommend whichever gives the lowest total. There is no shortcut rule that "
        "always wins; election is a comparison exercise, not an automatic saving.",
        "", "medium")

    o, a = opts("The loss is still relievable, since personal assessment for a year "
                "can be elected up to two years after that year ends",
                "The loss is forfeited once the year of assessment for the loss has "
                "passed",
                "The loss must be relieved in the same year it is incurred or never "
                "at all",
                "Only losses incurred in the current year of assessment qualify")
    add("E", "Business losses",
        "A sole trader's business made a loss last year (say YA 2024/25), which "
        "was simply carried forward under the profits tax computation because no "
        "election was made at the time. Can personal assessment still be used now to "
        "relieve that loss against last year's other income?",
        o, a,
        "The time limit for electing personal assessment for a given year runs for "
        "two years after that year of assessment ends (or longer following a late "
        "assessment), so there is still time to go back and elect for YA 2024/25 "
        "itself, setting that year's loss against that year's other income, rather "
        "than only being able to use the loss against future profits.", "s.41(2)",
        "hard")

    o, a = opts("It is the total income of the individual, before deducting interest, "
                "concessionary deductions or losses - the starting point of the "
                "computation",
                "It is the same thing as net chargeable income",
                "It is total income after personal allowances only",
                "It is only the individual's salary income, excluding property and "
                "business income")
    add("E", "Computation",
        "In the personal assessment computation, what does 'total income' mean "
        "before it becomes 'reduced total income'?",
        o, a,
        "Total income is simply the sum of the individual's net assessable value, "
        "net assessable income and assessable profits from all sources - the "
        "starting point, before any of the personal-assessment-specific deductions "
        "(interest, concessionary deductions, losses) are subtracted to arrive at "
        "reduced total income.", "s.42", "medium")

    o, a = opts("It is included in full, since a corporate partner's own separate "
                "assessment is unaffected by what an individual partner elects",
                "It is excluded from the partnership computation entirely",
                "It is halved",
                "It is deferred until the corporate partner also elects personal "
                "assessment")
    add("E", "Partnership interaction",
        "An individual partner in a mixed partnership elects personal assessment. "
        "What happens to the corporate partner's share of the same partnership's "
        "profit?",
        o, a,
        "Each partner's share is assessed independently of what any other partner "
        "elects. The corporate partner's share of profit continues to be assessed "
        "under ordinary profits tax at the corporate rate, entirely unaffected by the "
        "individual partner's personal assessment election.", "s.41", "medium")

    o, a = opts("Yes - a non-Hong Kong-sourced loss cannot be brought in, but "
                "Hong Kong-sourced property, employment and business income can all "
                "still be aggregated even where some of it individually would be "
                "modest",
                "No - personal assessment requires at least two separate sources of "
                "chargeable income",
                "No - personal assessment is only available where property income "
                "exists",
                "Yes, but only where the taxpayer's total income exceeds $1,000,000")
    add("E", "Eligibility",
        "Must a taxpayer have more than one source of chargeable income before "
        "personal assessment is worth considering?",
        o, a,
        "There is no such requirement in the legislation - even a taxpayer with a "
        "single source can elect - but as a matter of practical benefit, personal "
        "assessment tends only to help where there is property or business income "
        "(with a loss, or mortgage interest, or no allowances of its own) to combine "
        "with something else; a single salary source alone gains nothing from "
        "electing.", "s.41", "medium")

    o, a = opts("The Commissioner may refuse to accept a late election, though in "
                "practice a reasonable excuse for the delay is usually accommodated",
                "A late election is always accepted with no discretion required",
                "A late election converts automatically into an objection instead",
                "There is no consequence, since personal assessment has no time "
                "limit at all")
    add("E", "Time limits",
        "What happens if an election for personal assessment is made after the "
        "statutory time limit in s.41(2) has passed?",
        o, a,
        "The election is out of time and the Commissioner is not obliged to accept "
        "it, though there is administrative practice of accepting a late election "
        "where there is a reasonable explanation - it should never be assumed as of "
        "right.", "s.41(2)", "medium")


# ===========================================================================
# AREA C - Profits tax  (target 105 - the heaviest-weighted area)
# ===========================================================================
def area_c():
    # --- charge and source ---------------------------------------------------
    o, a = opts("A person carrying on a trade, profession or business in Hong Kong, on "
                "profits arising in or derived from Hong Kong from that trade, "
                "profession or business",
                "Any person resident in Hong Kong, on worldwide profits",
                "A company incorporated in Hong Kong, on all profits wherever arising",
                "Any person carrying on business in Hong Kong, on all profits received "
                "in Hong Kong")
    add("C", "Charge", "Who is chargeable to profits tax and on what?",
        o, a,
        "Section 14(1) charges every person carrying on a trade, profession or "
        "business in Hong Kong, on profits arising in or derived from Hong Kong from "
        "that trade, profession or business. Hong Kong operates a strict territorial, "
        "source-based system - residence and place of incorporation are irrelevant, "
        "and offshore profits are outside the charge however the money is received.",
        "s.14(1)", "easy")

    o, a = opts("A question of fact, decided by looking at what the taxpayer did to "
                "earn the profit and where they did it",
                "Decided solely by where the contract of sale was signed",
                "Decided solely by where the taxpayer is incorporated",
                "Decided solely by where the goods are physically delivered")
    add("C", "Source", "How is the source of profits determined, following "
        "<em>HK-TVB v CIR</em> and later cases?",
        o, a,
        "The 'operations test': look at what the taxpayer actually did to earn the "
        "profit in question, and where. It is a practical, fact-specific enquiry, not "
        "a single mechanical rule - contract location and place of incorporation are "
        "each relevant but never decisive on their own.", "DIPN 21", "medium")

    o, a = opts("Where the contracts of purchase and sale are effected",
                "Where the goods are manufactured",
                "Where the goods are physically stored before sale",
                "Where the company's bank account is held")
    add("C", "Source - trading profits",
        "For a business of trading in goods, what is the primary factor in "
        "determining the source of the trading profit?",
        o, a,
        "For trading profits the place where the contracts of purchase and sale are "
        "effected is the key factor - not necessarily where they are signed, but where "
        "the effective negotiation happens. A contract effected outside Hong Kong "
        "points to an offshore claim.", "DIPN 21", "medium")

    o, a = opts("Manufacturing profits are apportioned between the processing and the "
                "trading/selling functions",
                "All profits are Hong Kong sourced because the company is Hong Kong "
                "incorporated",
                "All profits are offshore because the manufacturing takes place across "
                "the border",
                "The profit follows wherever the raw materials were bought")
    add("C", "Source - contract processing",
        "A Hong Kong company has goods manufactured under a contract-processing "
        "arrangement in the Mainland, and sells the goods from Hong Kong. How is the "
        "profit sourced?",
        o, a,
        "DIPN 21 apportions the profit 50:50 between the Mainland processing "
        "operation and the Hong Kong trading operation, reflecting that both "
        "contribute to earning it. An import-processing arrangement, by contrast, is "
        "not apportioned in the same way because the Mainland entity's own factory "
        "does the work.", "DIPN 21", "hard")

    o, a = opts("Fees for services are sourced where the services are rendered",
                "Fees for services are always Hong Kong sourced if invoiced from Hong "
                "Kong",
                "Fees for services are sourced where the client is based",
                "Fees for services are always apportioned 50:50")
    add("C", "Source - service income",
        "What is the basic rule for sourcing profits from the provision of services?",
        o, a,
        "Profits from services are sourced where the services are rendered - a "
        "different test from trading profits, which look at where contracts are "
        "effected.", "DIPN 21", "medium")

    o, a = opts("It is a badge of trade indicating a trading, not a capital, transaction",
                "It is conclusive proof of a capital transaction",
                "It is irrelevant to the trade/capital distinction",
                "It only matters for property transactions")
    for what, right2, wrongs in [
        ("A short period of ownership before resale",
         "It is a badge of trade indicating a trading, not a capital, transaction",
         ["It is conclusive proof of a capital transaction",
          "It is irrelevant to the trade/capital distinction",
          "It only matters for property transactions"]),
        ("The taxpayer's stated intention at the time of acquisition, taken with the "
         "surrounding circumstances",
         "It is one badge of trade among several, not conclusive on its own",
         ["It is the sole and conclusive test of trading",
          "It is irrelevant if not stated in writing",
          "It only applies to individuals, not companies"]),
        ("The number and frequency of similar transactions",
         "Repeated, systematic transactions point towards trading",
         ["A single transaction can never be trading",
          "Frequency is irrelevant to the badges of trade",
          "Only three or more transactions can amount to trading"]),
        ("An asset acquired to be modified or improved before resale",
         "Work done to make an asset more saleable is a badge of trade",
         ["Modification is only relevant to manufacturing businesses",
          "Modification always indicates a capital asset",
          "Modification is irrelevant unless done by a contractor"]),
    ]:
        o, a = opts(right2, *wrongs)
        add("C", "Badges of trade",
            "Which of the 'badges of trade' does the following describe?<br><em>%s"
            "</em>" % what,
            o, a,
            "The badges of trade (subject matter, length of ownership, frequency, "
            "supplementary work, circumstances of realisation, motive) are drawn from "
            "case law and none is conclusive alone - the question is always the "
            "overall impression from all the facts.", "", "medium")

    o, a = opts("A capital receipt, outside the scope of profits tax",
                "A trading receipt, taxable in full",
                "Taxable at 50% of the sum received",
                "Exempt only if received from a connected party")
    add("C", "Capital vs revenue",
        "A company receives a lump sum as compensation for the permanent loss of an "
        "agency it held, the agency being a capital asset of the business. How is the "
        "receipt treated?",
        o, a,
        "Compensation for the loss or sterilisation of a capital asset is itself "
        "capital, following <em>Van den Berghs v Clark</em>. Contrast compensation for "
        "loss of trading stock or lost profits, which is a revenue receipt.",
        "", "hard")

    o, a = opts("A revenue receipt, taxable in the year it accrues",
                "A capital receipt, outside the charge",
                "Taxable only when the goods are eventually resold",
                "Taxable at half the normal rate")
    add("C", "Capital vs revenue",
        "An insurer pays out for trading stock destroyed by fire. How is the payment "
        "treated?",
        o, a,
        "Compensation that replaces a revenue item - here, stock that would have been "
        "sold in the ordinary course - is itself revenue in nature and taxable.", "")

    # --- general deductions --------------------------------------------------
    o, a = opts("Outgoings and expenses to the extent incurred in the production of "
                "assessable profits",
                "Outgoings and expenses wholly, exclusively and necessarily incurred "
                "in the production of assessable profits",
                "Any expense recorded in the accounts",
                "Outgoings incurred wholly and exclusively for the purposes of the "
                "trade")
    add("C", "General deduction",
        "What is the statutory test for deducting an expense under profits tax?",
        o, a,
        "Section 16(1) is deliberately looser than the salaries tax test: expenses "
        "<strong>to the extent</strong> incurred in the production of profits. There "
        "is no 'wholly, exclusively and necessarily' requirement, so an expense with a "
        "dual purpose can still be apportioned and partly deducted.", "s.16(1)",
        "medium")

    o, a = opts("Capital expenditure", "Domestic or private expenditure",
                "Expenditure not incurred in the production of profits",
                "Rent of business premises")
    add("C", "Non-deductible expenditure",
        "Which of the following IS normally deductible under s.17?",
        o, a,
        "Section 17(1) specifically prohibits deducting capital expenditure, domestic "
        "or private expenditure, and expenses not incurred in the production of "
        "chargeable profits. Ordinary business rent is none of these and is "
        "deductible under s.16(1).", "s.17(1)", "easy")

    o, a = opts("Not deductible - it is capital expenditure",
                "Deductible in full as a trading expense",
                "Deductible over five years",
                "Deductible only if the taxpayer is a company")
    add("C", "Non-deductible expenditure",
        "A trader incurs legal costs in acquiring a new shop lease for the business. "
        "How is the expenditure treated?",
        o, a,
        "Costs of acquiring a capital asset - including the legal costs of acquiring "
        "it - are themselves capital and non-deductible, even though the asset itself "
        "(the lease) will be used to earn trading profits.", "s.17(1)(c)", "medium")

    o, a = opts("Deductible - it is incurred in defending the taxpayer's trading "
                "position",
                "Not deductible as it relates to litigation",
                "Deductible only up to $50,000",
                "Not deductible as legal costs are always capital")
    add("C", "Deductions",
        "A company incurs legal costs defending a claim brought by a customer over "
        "defective goods sold in the ordinary course of business. How are the costs "
        "treated?",
        o, a,
        "Legal costs take their character from what they protect. Costs incurred in "
        "the ordinary course of trade - defending a trading claim, recovering a "
        "trading debt - are revenue and deductible. Costs of acquiring or defending "
        "title to a capital asset are not.", "s.16(1)", "medium")

    for good, bad in [(500000, 30000), (280000, 15000), (900000, 60000)]:
        cap = round(good * 0.35, 2)
        right = min(bad, cap)
        if right == bad:
            o, a = opts(M(right), M(cap), M(good * 0.25), M(bad * 0.5))
        else:
            o, a = opts(M(right), M(bad), M(bad - cap), M(good * 0.25))
        add("C", "Donations",
            "A company's assessable profits before deducting donations are %s, and it "
            "made approved charitable donations of %s in the year. What deduction is "
            "allowed?" % (M(good), M(bad)),
            o, a,
            "Section 16D caps the deduction at 35%% of assessable profits "
            "<strong>before</strong> the donation itself is deducted: 35%% &times; %s "
            "= %s. Here the allowable amount is %s. The donation must also be at "
            "least $100 and not merely a payment for goods, advertising space or a "
            "dinner ticket at an inflated price."
            % (M(good), M(cap), M(right)), "s.16D", "medium", "computational")

    o, a = opts("Not deductible - it is capital in nature",
                "Deductible in full as a repair",
                "Deductible at 50%, the balance capitalised",
                "Deductible only if the roof was under one year old")
    add("C", "Repairs vs improvement",
        "A company replaces a factory's flat roof with a completely new and improved "
        "roof structure of superior design, rather than patching the original. How is "
        "the cost treated?",
        o, a,
        "A repair restores an asset; an improvement makes it better than before and is "
        "capital. Replacing with something of a materially superior specification "
        "tips this into capital expenditure, non-deductible under s.17(1)(c), though it "
        "may qualify for a depreciation allowance instead.", "s.16(1)(e); s.17(1)(c)",
        "hard")

    o, a = opts("Deductible - a specific provision for a debt reasonably estimated to "
                "be irrecoverable",
                "Not deductible - only debts formally written off are allowed",
                "Deductible only for banks",
                "Not deductible - a general provision")
    add("C", "Bad and doubtful debts",
        "A trader makes a specific provision against a named customer's debt, having "
        "reasonable grounds to believe it will not be paid. Is the provision "
        "deductible?",
        o, a,
        "Section 16(1)(d) allows a deduction for bad debts and doubtful debts "
        "<strong>specifically identified</strong> as estimated to be bad. A general, "
        "unspecific provision (e.g. 2% of all debtors) is never deductible.",
        "s.16(1)(d)", "medium")

    o, a = opts("Assessable as a trading receipt in the year recovered",
                "Not assessable, as it was never allowed as a deduction",
                "Related back to the year the debt was written off",
                "Assessable at half the amount recovered")
    add("C", "Bad and doubtful debts",
        "A bad debt previously allowed as a deduction is unexpectedly recovered in a "
        "later year. How is the recovery treated?",
        o, a,
        "The recovery is a trading receipt of the year it is received, taxable in "
        "full, mirroring the property tax treatment of recovered irrecoverable rent.",
        "s.15(1)(g)", "medium")

    o, a = opts("Deductible - interest on money borrowed for the purposes of producing "
                "chargeable profits, subject to the anti-avoidance conditions in s.16(2)",
                "Never deductible under profits tax",
                "Deductible only if paid to a Hong Kong bank",
                "Deductible only up to the amount of profits before interest")
    add("C", "Interest deduction",
        "Under what condition is interest expense generally deductible against profits "
        "tax?",
        o, a,
        "Section 16(1)(a) allows interest on borrowings used to produce chargeable "
        "profits, but s.16(2) imposes several conditions aimed at related-party and "
        "circular back-to-back arrangements - interest paid to an overseas associate "
        "not itself subject to Hong Kong profits tax on the interest, for instance, can "
        "be restricted.", "ss.16(1)(a), 16(2)", "hard")

    # --- depreciation allowances ----------------------------------------------
    o, a = opts("60% of the cost, in the year of purchase, regardless of how long the "
                "asset is used in the year",
                "60% of the cost, apportioned by the number of months of use",
                "20% of the cost, in the year of purchase",
                "There is no initial allowance for plant and machinery")
    add("C", "Depreciation allowances",
        "What initial allowance is available on qualifying capital expenditure on "
        "plant or machinery?",
        o, a,
        "Section 39B(1A) gives a flat 60% initial allowance in the year of purchase, "
        "with no time-apportionment for part of a year and no reduction for private "
        "use by a company - private use apportionment applies to sole traders and "
        "partnerships, not companies.", "s.39B(1A)", "medium")

    o, a = opts("10%, 20% or 30% a year on the reducing balance of each pool",
                "A flat 25% a year on the reducing balance",
                "20% a year on the original cost, straight line",
                "4% a year on the reducing balance")
    add("C", "Depreciation allowances",
        "At what rates is the annual allowance on plant and machinery computed?",
        o, a,
        "Assets are grouped into pools taxed at 10%, 20% or 30% depending on their "
        "prescribed class, each on the reducing balance of that pool's "
        "written-down value.", "s.39B; Sch. 3", "easy")

    for wdv, additions, disposals, rate in [
            (800000, 200000, 50000, 0.30), (1500000, 100000, 300000, 0.20),
            (0, 600000, 0, 0.10), (450000, 150000, 100000, 0.30)]:
        r = T.da_pool(wdv, additions, disposals, rate)
        o, a = opts(M(r["total"]), M(r["aa"]), M(r["ia"]),
                    M(round((wdv + additions - disposals) * rate, 2)))
        add("C", "Depreciation allowances",
            "A 30%%-pool has a written-down value brought forward of %s. During the "
            "year the business bought qualifying plant for %s and sold plant for %s. "
            "What is the total depreciation allowance for the year?"
            % (M(wdv), M(additions), M(disposals)) if rate == 0.30 else
            "A pool taxed at %d%% has a written-down value brought forward of %s. "
            "During the year the business bought qualifying plant for %s and sold "
            "plant for %s. What is the total depreciation allowance for the year?"
            % (int(rate * 100), M(wdv), M(additions), M(disposals)),
            o, a,
            "Additions %s less the 60%% initial allowance %s leaves %s; less "
            "disposal proceeds of %s = %s; the annual allowance is %d%% of that = %s. "
            "Total allowance = IA %s + AA %s = %s. Deducting disposal proceeds "
            "<strong>before</strong> the initial allowance, or omitting the IA "
            "entirely, are the two errors most often made."
            % (M(additions), M(r["ia"]), M(wdv + additions - r["ia"]), M(disposals),
               M(r["reduced"]), int(rate * 100), M(r["aa"]), M(r["ia"]), M(r["aa"]),
               M(r["total"])),
            "s.39B; Sch. 3", "hard", "computational")

    o, a = opts("A balancing charge, added back to assessable profits",
                "A balancing allowance, deducted from assessable profits",
                "No adjustment - the excess is simply ignored",
                "The excess is carried forward as a loss")
    add("C", "Depreciation allowances",
        "Disposal proceeds from selling the only asset in a pool exceed its "
        "written-down value brought forward, after also deducting the year's "
        "additions. What is the tax result?",
        o, a,
        "Where proceeds exceed the pool's residue, the excess is a "
        "<strong>balancing charge</strong> - effectively clawing back allowances "
        "given in earlier years - and is added back as if it were extra profit, "
        "capped at the total allowances actually given. Where proceeds are less than "
        "the residue and the pool ceases to have any asset in it, the shortfall "
        "is a balancing allowance instead.", "s.39B(4)", "hard")

    for deposit, paid_instalments, cap_per in [(60000, 6, 8000), (100000, 4, 12000),
                                               (40000, 9, 5000)]:
        ia, qual = T.hire_purchase_ia(deposit, paid_instalments, cap_per)
        full_price_ia = round((deposit + 12 * cap_per) * 0.60, 2)
        o, a = opts(M(ia), M(full_price_ia), M(round(qual * 0.20, 2)),
                    M(round(qual, 2)))
        add("C", "Depreciation allowances - hire purchase",
            "Plant is acquired on hire purchase with a deposit of %s, and %d monthly "
            "instalments are paid in the year, each with a capital element of %s. What "
            "initial allowance is available for the year?"
            % (M(deposit), paid_instalments, M(cap_per)),
            o, a,
            "For hire purchase, the initial allowance runs only on the capital sums "
            "<strong>actually paid</strong> in the year - the deposit plus the capital "
            "element of instalments paid - not on the full cash price of the asset: "
            "(%s + %d &times; %s) &times; 60%% = %s. Using the full cash price "
            "overstates the allowance."
            % (M(deposit), paid_instalments, M(cap_per), M(ia)),
            "s.39E; DIPN 13", "hard", "computational")

    o, a = opts("Straight-line: 20% initial allowance plus 4% annual allowance on cost",
                "Reducing balance at 4% a year",
                "A single 100% deduction in the year of completion",
                "There is no allowance for commercial buildings")
    add("C", "Commercial buildings allowance",
        "What allowance is available on capital expenditure on constructing a "
        "commercial building or structure used in the business?",
        o, a,
        "A 20% initial allowance in the year the expenditure is incurred, plus a 4% "
        "annual allowance on a straight-line basis (i.e. on cost, not "
        "written-down value) for 25 years, given to whoever owns the "
        "relevant interest at the end of the basis period. Industrial buildings "
        "attract the same rates under a parallel code.", "ss.34, 36A", "medium")

    o, a = opts("The cost of the land itself is excluded",
                "The whole purchase price qualifies, including the land",
                "Only 50% of the price qualifies",
                "The allowance is based on the rateable value")
    add("C", "Commercial/industrial buildings allowance",
        "A company buys a completed commercial building for use in its business. On "
        "what amount is the buildings allowance computed?",
        o, a,
        "Only the cost of <strong>construction</strong> qualifies - the value "
        "attributable to the land must be stripped out first, whether the building was "
        "constructed by the taxpayer or bought already built.", "s.40", "hard")

    o, a = opts("100% deduction in the year of purchase",
                "60% initial allowance plus a 20% pool rate",
                "20% initial allowance plus 4% annual allowance",
                "No allowance is available")
    add("C", "Prescribed fixed assets",
        "What allowance is available for capital expenditure on a prescribed fixed "
        "asset such as computer hardware and software, or manufacturing machinery "
        "specified by the Commissioner?",
        o, a,
        "Section 16G gives a 100% deduction in the year of purchase for prescribed "
        "fixed assets, in place of the normal pooled initial-plus-annual allowance "
        "system - though a specific exclusion applies to office furniture and "
        "fixtures, motor vehicles, and structures.", "s.16G", "medium")

    # --- R&D deduction ---------------------------------------------------------
    for a_amt, b_amt in [(400000, 2500000), (0, 3000000), (600000, 2400000)]:
        r = T.rnd_deduction(a_amt, b_amt)
        o, a = opts(M(r), M(a_amt + b_amt), M(a_amt + b_amt * 2),
                    M(a_amt + b_amt * 3))
        add("C", "R&D expenditure",
            "A company incurred Type A R&D expenditure of %s and Type B "
            "(qualifying) R&D expenditure of %s in the year. What total deduction is "
            "available under s.16B?" % (M(a_amt), M(b_amt)),
            o, a,
            "Type A gets a plain 100%% deduction: %s. Type B is enhanced - "
            "300%% on the first $2,000,000 and 200%% on the excess: "
            "(min(%s, 2,000,000) &times; 3) + (max(0, %s - 2,000,000) &times; 2). "
            "Total deduction = %s. Forgetting the enhancement tiers and simply "
            "deducting 100%% of the Type B spend is the commonest error - this is "
            "the exact scenario the examining team published a worked example on."
            % (M(a_amt), M(b_amt), M(b_amt), M(r)),
            "s.16B", "hard", "computational")

    o, a = opts("Type B must relate to one of the specified fields and either seek to "
                "extend general knowledge or have an industrial, agricultural or "
                "scientific purpose",
                "Type B is any expenditure on scientific research of any kind",
                "Type B is limited to expenditure carried out overseas",
                "Type B and Type A are simply two names for the same thing")
    add("C", "R&D expenditure",
        "What distinguishes 'Type B' qualifying R&D expenditure from 'Type A'?",
        o, a,
        "Type B research must fall within a field specified in Schedule 45 and meet "
        "the purpose test in s.2. Type A is a residual category - R&D expenditure that "
        "does not qualify as Type B still gets a plain 100% deduction rather than "
        "none, provided it otherwise relates to the trade.", "s.16B; Sch. 45", "hard")

    # --- trading losses ----------------------------------------------------
    o, a = opts("Carried forward indefinitely and set off against future assessable "
                "profits of the same trade",
                "Carried back one year against the preceding year's profits",
                "Lost if not used within 5 years",
                "Set off automatically against the owner's salaries tax")
    add("C", "Trading losses",
        "How is an unrelieved trading loss of a Hong Kong business normally treated?",
        o, a,
        "Losses are carried forward with no time limit and set off against future "
        "assessable profits, but there is no carry-back and (unlike personal "
        "assessment) no automatic set-off against the owner's other income.", "s.19C",
        "easy")

    o, a = opts("Only through electing personal assessment",
                "Automatically, in the profits tax computation itself",
                "By carrying it back against the previous year",
                "It cannot be relieved against any other income")
    add("C", "Trading losses",
        "A sole proprietor's business makes a loss for the year, and they also have "
        "rental income from a separate let property. How can the business loss be set "
        "against the rental income in the same year?",
        o, a,
        "Only by electing personal assessment, which aggregates all the individual's "
        "chargeable income and lets a current-year business loss shelter it. Within "
        "the profits tax computation alone, the loss is simply carried forward.",
        "s.42(1)", "medium")

    o, a = opts("They are shared among the partners in the profit-sharing ratio and "
                "each partner deals with their own share",
                "The loss belongs to the partnership and is carried forward at "
                "partnership level only",
                "The loss can only be used by the partner with the largest capital "
                "account",
                "The loss is forfeited if any partner leaves during the year")
    add("C", "Trading losses - partnerships",
        "How is a partnership's trading loss for a year treated?",
        o, a,
        "The loss is allocated to the partners in the agreed profit-sharing ratio, "
        "just like a profit would be. Each partner then carries forward, or otherwise "
        "relieves, their own share - an individual partner might elect personal "
        "assessment to set it against salary; a corporate partner simply carries its "
        "share forward against future profits.", "s.19C(4)", "hard")

    # --- two-tier rates, computational --------------------------------------
    o, a = opts("$2,000,000 &times; 8.25% = $165,000 - the two-tier system only "
                "changes the rate on profits above $2,000,000",
                "$2,000,000 &times; 16.5% = $330,000",
                "Nil - profits below $2,000,000 are exempt",
                "It depends on an annual election by the company")
    add("C", "Two-tier profits tax",
        "A Hong Kong company has assessable profits of exactly $2,000,000 for the "
        "year, with no connected entities. What profits tax is payable?",
        o, a,
        "At or below the $2,000,000 threshold the two-tier system makes no "
        "difference at all - the whole profit is simply taxed at 8.25%, the lower "
        "tier rate. The higher 16.5% rate only ever applies to the slice above "
        "$2,000,000.", "s.14AA", "easy", "computational")

    for profit in [2500000, 4200000, 8000000, 12000000]:
        right = T.two_tier(profit, corporate=True)
        flat_hi = round(profit * 0.165, 2)
        flat_lo = round(profit * 0.0825, 2)
        reversed_tiers = round(2000000 * 0.165 + (profit - 2000000) * 0.0825, 2)
        o, a = opts(M(right), M(flat_hi), M(flat_lo), M(reversed_tiers))
        add("C", "Two-tier profits tax - corporation",
            "A Hong Kong company (not connected with any other entity electing the "
            "two-tier regime) has assessable profits of %s for the year. What profits "
            "tax is payable?" % M(profit),
            o, a,
            "The first $2,000,000 is taxed at 8.25%%, and the excess at 16.5%%: "
            "(2,000,000 &times; 8.25%%) + (%s &times; 16.5%%) = %s. Applying 16.5%% "
            "to the whole profit, as if there were no two-tier relief, gives %s and "
            "overstates the tax by $%s."
            % (M(profit - 2000000), M(right), M(flat_hi),
               T.money(flat_hi - right)),
            "s.14AA", "medium", "computational")

    o, a = opts("Only one entity in a group of connected entities may benefit from the "
                "two-tier rates; the others pay flat 16.5%/15%",
                "Every company in a group benefits from the two-tier rates "
                "independently",
                "The two-tier rates are unavailable to any company in a group",
                "The $2,000,000 threshold is doubled for a group of two companies")
    add("C", "Two-tier profits tax",
        "How does the two-tier regime apply where several companies are 'connected "
        "entities' of one another?",
        o, a,
        "Connected entities must nominate only one of themselves to enjoy the "
        "two-tier rates for a year of assessment; the rest pay the flat rate (16.5% "
        "corporate, 15% unincorporated) on all their profits. This stops a group "
        "multiplying the $2,000,000 band by splitting into subsidiaries.",
        "s.14AA(4)", "hard")

    for profit in [2400000, 3600000, 5000000]:
        right = T.two_tier(profit, corporate=False)
        flat_hi = round(profit * 0.15, 2)
        flat_lo = round(profit * 0.075, 2)
        wrong_corp = T.two_tier(profit, corporate=True)
        o, a = opts(M(right), M(flat_hi), M(flat_lo), M(wrong_corp))
        add("C", "Two-tier profits tax - unincorporated business",
            "A sole proprietorship has assessable profits of %s. What profits tax is "
            "payable?" % M(profit),
            o, a,
            "For an unincorporated business the two-tier rates are 7.5%% on the first "
            "$2,000,000 and 15%% above: (2,000,000 &times; 7.5%%) + (%s &times; 15%%) "
            "= %s. Using the corporate rates of 8.25%%/16.5%% instead of 7.5%%/15%% is "
            "a common slip when candidates confuse the two sets of rates."
            % (M(profit - 2000000), M(right)), "s.14AA", "medium", "computational")

    # --- entity: sole trader -------------------------------------------------
    o, a = opts("As if the business and the owner's personal affairs were entirely "
                "separate - only business income is assessed to profits tax",
                "Together with the owner's salary, in one profits tax computation",
                "At the two-tier corporate rates",
                "Only if the business has a separate business registration number "
                "from the owner's HKID")
    add("C", "Sole trader",
        "How is a sole proprietor's business profit assessed to profits tax?",
        o, a,
        "The business is assessed on its own trading results at the unincorporated "
        "two-tier rates (7.5%/15%), entirely separately from any salaries tax on the "
        "owner's employment income - the two are only brought together if the owner "
        "elects personal assessment.", "s.14AA", "easy")

    o, a = opts("Drawings and a notional salary to the proprietor are not deductible - "
                "the whole profit, before any such appropriation, is assessable",
                "A reasonable salary to the proprietor is deductible, like an "
                "employee's salary",
                "Drawings are deductible but a notional salary is not",
                "Both are deductible provided they are recorded in the accounts")
    add("C", "Sole trader",
        "A sole trader draws a monthly 'salary' from the business and records it as an "
        "expense. How is this treated in the profits tax computation?",
        o, a,
        "A proprietor cannot be their own employee. Any salary, bonus or drawings "
        "taken by a sole proprietor (or by their spouse, under s.16(2)(e)) must be "
        "added back - the entire profit before that appropriation is what is "
        "assessable.", "s.17(2)", "medium")

    o, a = opts("Deductible, if the spouse genuinely works in the business and the "
                "amount is not excessive - subject to the same restriction as the "
                "proprietor's own salary",
                "Always deductible in full",
                "Never deductible under any circumstance",
                "Deductible only if the spouse holds a separate business registration")
    add("C", "Sole trader",
        "A sole trader pays a salary to their spouse, who works full-time managing the "
        "shop. Is the salary deductible?",
        o, a,
        "Section 17(2) treats salaries paid to the proprietor's spouse the same way as "
        "a payment to the proprietor - it is not deductible and must be added back, "
        "regardless of how genuinely the spouse works, because husband and wife are "
        "not treated as being at arm's length for this purpose.", "s.17(2)", "hard")

    # --- entity: partnership --------------------------------------------------
    o, a = opts("The partnership itself is not a separate chargeable person - it files "
                "one profits tax return, but the assessable profit is allocated to and "
                "assessed on each partner individually",
                "The partnership is assessed and pays the tax as a single entity, like "
                "a company",
                "Each partner is separately assessed with no reference to the "
                "partnership at all",
                "Only the precedent partner is assessed, on behalf of everyone")
    add("C", "Partnership",
        "How is a Hong Kong partnership assessed to profits tax?",
        o, a,
        "A partnership is not itself a person chargeable to tax, but it files one "
        "return covering the whole business (s.22), and the resulting assessable "
        "profit or loss is then divided among the partners according to their "
        "profit-sharing ratio, each partner being assessed on their own share.",
        "s.22", "medium")

    o, a = opts("Added back in the partnership computation, then reallocated to each "
                "partner as part of their share of profit",
                "Deductible in the partnership computation, like a normal salary "
                "expense",
                "Deductible for a partner who is a company, but not for an individual "
                "partner",
                "Deductible provided the partnership agreement specifies the amount")
    add("C", "Partnership",
        "Partners are paid a salary and interest on capital under the partnership "
        "agreement, both charged as expenses in the partnership accounts. How are "
        "these treated for profits tax?",
        o, a,
        "Section 16(2)(e)/(2A) treats any salary, interest on capital, or interest on "
        "loans from a partner as a mere appropriation of profit, not a real expense - "
        "it is added back in arriving at the partnership's total assessable profit, "
        "and then each partner's own salary/interest is added to their share when the "
        "profit is divided, so nothing is actually lost.", "s.16(2A)", "hard")

    for profit, shares in [
            (3000000, [(0.5, False), (0.3, False), (0.2, True)]),
            (5000000, [(0.6, False), (0.4, True)]),
            (4000000, [(0.3, False), (0.3, False), (0.4, True)])]:
        total, detail = T.two_tier_partnership(profit, shares)
        wrong1 = T.two_tier(profit, corporate=False)   # ignores the corporate partner
        wrong2 = round(profit * 0.15, 2)                # flat 15% on everything
        wrong3 = round(profit * 0.165, 2)               # flat 16.5% on everything
        o, a = opts(M(total), M(wrong1), M(wrong2), M(wrong3))
        n_partners = len(shares)
        mix = "a company"
        add("C", "Two-tier profits tax - mixed partnership",
            "A partnership with %d partners has assessable profits of %s for the "
            "year, shared %s. One partner is %s and the rest are individuals. What "
            "is the total profits tax payable, applying the two-tier rates "
            "separately to each partner's share?"
            % (n_partners, M(profit), " : ".join("%.0f%%" % (s * 100) for s, _ in shares),
               mix),
            o, a,
            "The $2,000,000 first-tier band is <strong>apportioned between the "
            "partners in the profit-sharing ratio</strong>, and each partner's slice "
            "of profit is then taxed at their own rates (7.5%%/15%% for an individual "
            "partner, 8.25%%/16.5%% for a corporate partner): total tax = %s. "
            "Applying one flat set of rates to the whole partnership profit, as if it "
            "had a single $2,000,000 band, ignores that a mixed partnership has more "
            "than one type of partner and is the error most often seen in this "
            "question." % M(total),
            "s.14AA; DIPN 28", "hard", "computational")

    o, a = opts("The individual partner's share is included in their personal "
                "assessment total income; the corporate partner's share never is",
                "Both partners' shares are included in personal assessment",
                "Neither partner's share can be included in personal assessment",
                "Only the precedent partner's share is included in personal "
                "assessment")
    add("C", "Partnership - personal assessment",
        "A partnership has one individual partner and one corporate partner. How does "
        "each partner's share of the partnership profit interact with personal "
        "assessment?",
        o, a,
        "Personal assessment is available only to individuals. The individual "
        "partner's share of assessable profit (or loss) is aggregated into their own "
        "personal assessment total income, alongside salary and property income; the "
        "corporate partner's share simply stays in the corporate profits tax "
        "computation and is assessed at corporate rates with no personal assessment "
        "route available to it.", "ss.41, 42", "hard")

    o, a = opts("Restricted to that partner's own share of the partnership's net "
                "assessable value or profit, mirroring the individual property/"
                "business rule",
                "Unlimited, the same as for a sole proprietor",
                "Always disallowed for a partner",
                "Capped at $100,000 regardless of the share of profit")
    add("C", "Partnership - personal assessment",
        "An individual partner elects personal assessment. How is interest paid by "
        "them personally to fund their share of the partnership's borrowings "
        "restricted?",
        o, a,
        "The same restriction that applies to a sole proprietor's or property owner's "
        "interest applies partner by partner: it cannot exceed that partner's own "
        "share of the relevant assessable profit or net assessable value, and cannot "
        "create or increase a loss.", "s.42(1)", "hard")

    # --- entity: common corporation ------------------------------------------
    o, a = opts("Only the two-tier corporate rates of 8.25%/16.5% - the unincorporated "
                "rates never apply to a company",
                "Whichever of the corporate or unincorporated rates gives the lower "
                "tax",
                "The unincorporated rates of 7.5%/15%",
                "A flat rate chosen by election each year")
    add("C", "Common corporation",
        "At what rates is an ordinary Hong Kong company (not a qualifying "
        "professional reinsurer, corporate treasury centre or similar concessionary "
        "case) taxed on its assessable profits?",
        o, a,
        "A company is always taxed at the corporate two-tier rates - 8.25% on the "
        "first $2,000,000 and 16.5% above - never at the unincorporated rates, which "
        "are reserved for sole proprietorships and partnerships (other than any "
        "corporate partner within one, who is still taxed at the corporate rates on "
        "their own share).", "s.14AA", "easy")

    o, a = opts("A director's remuneration is a deductible expense of the company - "
                "the director/shareholder is separately assessed to salaries tax on "
                "it",
                "A director's remuneration must be added back, exactly as a sole "
                "proprietor's drawings are",
                "A director's remuneration is deductible only up to 50% of profits",
                "A director's remuneration is deductible only if the director owns no "
                "shares")
    add("C", "Common corporation",
        "How does a company's payment of remuneration to its director, who is also "
        "its sole shareholder, differ in tax treatment from a sole trader's own "
        "drawings?",
        o, a,
        "A company is a separate legal person from its shareholders, so a director "
        "can validly be an employee of their own company: the remuneration is a "
        "normal deductible expense in the profits tax computation (subject to being "
        "reasonable in amount) and is separately taxed on the director as salaries "
        "tax. A sole proprietor has no such separate legal identity, so their own "
        "drawings are never deductible.", "", "medium")

    o, a = opts("Dividends paid by a Hong Kong company are not deductible in computing "
                "its own profits, and are not further taxed in the hands of the "
                "shareholder",
                "Dividends are deductible to the company but taxable to the "
                "shareholder",
                "Dividends are taxed twice: once to the company as a disallowed "
                "expense, and again to the shareholder",
                "Dividends are exempt only if paid to a corporate shareholder")
    add("C", "Common corporation",
        "How are dividends paid by a Hong Kong company treated for profits tax "
        "purposes?",
        o, a,
        "Dividends are a distribution of after-tax profit, not an expense, so they "
        "are never deductible to the paying company - and Hong Kong does not tax "
        "dividend income at all, so the recipient (individual or corporate) is not "
        "taxed on them either. There is no dividend withholding tax and no need for "
        "any relief against double taxation of the same profit.", "s.26(a)", "medium")

    # --- trading stock ---------------------------------------------------------
    o, a = opts("The lower of cost and net realisable value",
                "Net realisable value",
                "Original cost, regardless of any fall in value",
                "Replacement cost")
    add("C", "Trading stock",
        "On what basis is trading stock normally valued at the end of an accounting "
        "period, for both accounting and tax purposes?",
        o, a,
        "The lower of cost and net realisable value - a conservative basis that "
        "recognises a fall in value before the stock is sold, but never revalues stock "
        "upward above cost.", "s.15C; HKAS 2", "easy")

    o, a = opts("FIFO or a weighted average cost formula",
                "LIFO (last in, first out)",
                "The most recent purchase price applied to all units",
                "A base stock method")
    add("C", "Trading stock",
        "Which cost formulas are acceptable for valuing trading stock under Hong Kong "
        "tax and accounting practice?",
        o, a,
        "FIFO and weighted average are both accepted. LIFO is not permitted under "
        "HKAS 2 and is not accepted for Hong Kong tax purposes either.", "HKAS 2",
        "medium")

    o, a = opts("At its open market value on the date of the gift or appropriation",
                "At its original cost, with no profit recognised",
                "It has no tax consequence at all",
                "At half its market value")
    add("C", "Trading stock",
        "A trader takes stock out of the business for personal use, or gives it away, "
        "without any question of trade to trade sale. How is this treated for profits "
        "tax?",
        o, a,
        "Section 15C deems trading stock disposed of otherwise than in the ordinary "
        "course of business - including a gift or appropriation for personal use - to "
        "be sold at open market value on that date, bringing the notional profit into "
        "the computation.", "s.15C", "hard")

    # --- basis periods -----------------------------------------------------
    o, a = opts("The accounting year ending within that year of assessment",
                "The calendar year always",
                "The year of assessment itself, from 1 April to 31 March",
                "Whatever twelve months the taxpayer chooses each year")
    add("C", "Basis period",
        "For an established business preparing annual accounts, what is the basis "
        "period for a year of assessment?",
        o, a,
        "The basis period is normally the accounting year ending within the year of "
        "assessment - a company with a 31 December year end is assessed for YA "
        "2025/26 on the year ended 31 December 2025, not on the year of assessment "
        "itself.", "s.18C", "easy")

    o, a = opts("The whole period from commencement to the end of its first "
                "accounting period may be taxed twice, in the first two years of "
                "assessment, unless the taxpayer applies for relief",
                "The overlapping profit is automatically excluded",
                "No overlap can ever arise under Hong Kong's basis period rules",
                "The overlap is always resolved by extending the first accounting "
                "period to exactly 12 months")
    add("C", "Basis period - new business",
        "A business commences on 1 October 2025 and its first accounts are made up "
        "to 31 December 2026, a period of 15 months. What is the effect on the basis "
        "periods for the first two years of assessment?",
        o, a,
        "Because the first accounts straddle more than one year of assessment, part "
        "of the profit is included in the basis period for both YA 2025/26 (the whole "
        "first period, being the only accounts available) and YA 2026/27 (the 12 "
        "months to 31 December 2026) - the overlapping months are taxed twice unless "
        "the taxpayer successfully applies under s.18E for the assessments to be "
        "revised on a fair and just apportionment.", "ss.18B, 18E", "hard")

    o, a = opts("The basis period runs from the end of the previous basis period to "
                "the date of cessation",
                "The basis period is always a full 12 months",
                "No assessment is raised for the year of cessation",
                "The basis period is the same 12 months as the year before")
    add("C", "Basis period - cessation",
        "A business permanently ceases on 30 June 2026, having last made up accounts "
        "to 31 December 2025. What is the basis period for the year of assessment in "
        "which it ceases?",
        o, a,
        "On cessation the basis period is simply whatever period is left: from the "
        "end of the last basis period to the actual date of cessation, however short "
        "or long that turns out to be - here, 1 January to 30 June 2026.", "s.18D",
        "medium")

    o, a = opts("It must apply to the Commissioner, who may accept the change and "
                "issue directions on how the transitional basis periods are computed",
                "It may change its accounting date freely with no notification needed",
                "A change of accounting date is not permitted once a business has "
                "commenced",
                "It must revert to the original date within two years")
    add("C", "Basis period - change of accounting date",
        "What must a business do if it wants to change its accounting year end?",
        o, a,
        "Section 18C(3) requires the Commissioner to be satisfied of the change and "
        "to give directions on the resulting basis periods, to ensure no period of "
        "profit is missed and none is taxed twice as a result of the change.",
        "s.18C(3)", "medium")

    # --- provisional profits tax ---------------------------------------------
    for prior in [2400000, 3200000, 6000000]:
        est = T.two_tier(prior, corporate=True)
        o, a = opts(M(est), M(round(prior * 0.165, 2)), M(round(prior * 0.0825, 2)),
                    M(round(prior * 1.1 * 0.165, 2)))
        add("C", "Provisional profits tax",
            "A company's final assessable profits for the preceding year were %s, on "
            "which the two-tier rates were applied. In the absence of any estimate "
            "supplied by the company, on what figure will provisional profits tax for "
            "the current year normally be raised?" % M(prior),
            o, a,
            "Provisional profits tax is normally based on the <strong>preceding "
            "year's assessable profits</strong>, taxed at the current year's rates: "
            "%s, applying the two-tier rates exactly as they would to a final "
            "assessment. The company may instead apply to have it based on a lower "
            "estimate of the current year's actual profits, and must do so in writing "
            "before the return is due if it wants that lower figure used."
            % M(est), "s.63", "medium", "computational")

    o, a = opts("A note is served requiring immediate application within a set time; "
                "if refused, the excess already paid is refunded once the actual "
                "assessment is made",
                "Provisional tax is always automatically refunded in full",
                "The company forfeits the right to object to the final assessment",
                "No adjustment is possible until the following year")
    add("C", "Provisional profits tax",
        "A company's actual assessable profits turn out to be much lower than the "
        "figure on which provisional profits tax was charged. How is the provisional "
        "tax reconciled once the final assessment is made?",
        o, a,
        "Provisional tax already paid is set off against the final tax liability for "
        "that year, and any excess is refunded (or set against the following year's "
        "provisional tax). Before the final figures are known, the company can also "
        "apply under s.63E to hold over part of the provisional tax on prescribed "
        "grounds, such as profits being likely to be substantially lower.", "s.63",
        "medium")

    # --- group relief -------------------------------------------------------
    o, a = opts("No - each company in a group is separately assessed and a loss in "
                "one company cannot be set against profits of another",
                "Yes - losses can be surrendered between group companies with at "
                "least 75% common ownership",
                "Yes, but only between a parent and its wholly-owned subsidiary",
                "Yes, automatically, with no election needed")
    add("C", "Group relief",
        "Can a loss-making Hong Kong subsidiary surrender its trading loss to a "
        "profitable fellow group company, to reduce the group's overall tax?",
        o, a,
        "Hong Kong has <strong>no group loss relief</strong> at all. Each company is "
        "a separate person chargeable to profits tax in its own right; a loss simply "
        "carries forward within the loss-making company itself, however profitable "
        "the rest of the group may be. This is a frequently tested contrast with "
        "jurisdictions that do have group relief.", "", "medium")

    o, a = opts("Nil - inter-company management fees, royalties and interest are all "
                "assessed and deducted on normal profits tax principles, company by "
                "company",
                "The group is assessed as if it were one single taxpayer",
                "Inter-company charges are always disregarded for tax purposes",
                "Only the ultimate holding company is assessed")
    add("C", "Group relief",
        "What is the profits tax consequence of one group company charging another a "
        "management fee?",
        o, a,
        "There being no group relief or consolidated filing, each company remains "
        "separately assessed: the fee is ordinary assessable income to the recipient "
        "and an ordinary deductible expense to the payer (subject to the general "
        "deduction rules), exactly as if the companies were unconnected.", "s.16(1)",
        "medium")

    # --- offshore claims -----------------------------------------------------
    o, a = opts("The burden is on the taxpayer to prove the profit was not derived "
                "from Hong Kong",
                "The burden is on the Commissioner to prove the profit was derived "
                "from Hong Kong",
                "Profits are presumed offshore unless the Commissioner proves "
                "otherwise",
                "There is no burden of proof - the Board of Review decides on the "
                "balance of convenience")
    add("C", "Offshore claims",
        "Where a taxpayer claims that profits included in its Hong Kong accounts are "
        "in fact offshore and not chargeable, where does the burden of proof lie?",
        o, a,
        "Section 68(4) places the burden squarely on the taxpayer to satisfy the "
        "Commissioner (and, on appeal, the Board of Review) that the assessment is "
        "excessive or wrong - which in an offshore claim means proving what "
        "operations actually generated the profit and where they took place.",
        "s.68(4)", "medium")

    o, a = opts("Contemporaneous documentary evidence of what was actually done and "
                "where - correspondence, contracts, travel records, minutes",
                "A signed statement from the company's auditors",
                "The mere fact that the customer is based outside Hong Kong",
                "The mere fact that the company has no staff physically in Hong Kong")
    add("C", "Offshore claims",
        "What kind of evidence does the Inland Revenue Department expect to support "
        "an offshore profits claim?",
        o, a,
        "IRD wants to see the operations that actually earned the profit - where "
        "negotiations happened, who visited whom, where contracts were concluded - "
        "not bare assertions. A customer's location and the absence of local staff "
        "are each a factor but neither is decisive on its own; DIPN 21 stresses that "
        "the totality of the facts is what matters.", "DIPN 21", "medium")

    # --- exchange differences ------------------------------------------------
    o, a = opts("A revenue receipt or loss, if it arises on a revenue account (e.g. "
                "trade debtors or creditors in foreign currency)",
                "Always a capital item, outside the scope of profits tax",
                "Always assessable in full regardless of what it relates to",
                "Ignored entirely because Hong Kong dollar is the functional "
                "currency")
    add("C", "Exchange differences",
        "How is a foreign exchange gain or loss on a trade debtor denominated in a "
        "foreign currency treated for profits tax?",
        o, a,
        "An exchange difference takes the character of the underlying item: a "
        "difference on a revenue item (trading debtors, trading creditors, floating "
        "loan capital used as working capital) is itself revenue and is taxable or "
        "deductible; a difference on a capital item (a fixed loan for acquiring a "
        "capital asset) is capital and outside the charge.", "DIPN 42", "hard")

    o, a = opts("Capital - the borrowing itself is a fixed capital loan used to "
                "acquire a capital asset",
                "Revenue - all foreign currency loans are revenue in nature",
                "It depends only on the lender's location",
                "It is always split 50:50 between capital and revenue")
    add("C", "Exchange differences",
        "A company borrows in US dollars to fund the purchase of a new factory "
        "building. An exchange loss arises when the loan is partly repaid. How is the "
        "loss treated?",
        o, a,
        "Because the loan itself is fixed capital raised to buy a capital asset, an "
        "exchange difference on repaying it is capital and non-deductible, unlike a "
        "difference on a revenue-account trade debt.", "DIPN 42", "hard")

    # --- pre-trading and post-cessation ---------------------------------------
    o, a = opts("Not deductible, because the trade had not yet commenced when the "
                "expenditure was incurred",
                "Deductible in full in the first year of trading",
                "Deductible, spread over the first three years of trading",
                "Deductible if incurred within six months before commencement")
    add("C", "Pre-trading expenditure",
        "A company incurs marketing and staff recruitment costs while setting up a "
        "new business, several months before it actually starts trading. Are these "
        "costs deductible against the profits once trading begins?",
        o, a,
        "Section 16(1) only allows a deduction for expenses incurred in the "
        "production of chargeable profits - which requires the trade to already "
        "exist. Genuine pre-trading expenditure is outside the charge altogether and "
        "is never deductible, however necessary it was to get the business started.",
        "s.16(1)", "hard")

    o, a = opts("Still deductible, provided they relate to debts or liabilities of "
                "the trade that was carried on",
                "Never deductible once the trade has ceased",
                "Deductible only if paid within one month of cessation",
                "Deductible only against the final year's profit, never creating a "
                "loss")
    add("C", "Post-cessation expenditure",
        "A business pays a trade debt it still owed after it permanently ceased "
        "trading. Can this expense still be deducted?",
        o, a,
        "An expense does not lose its deductible character merely because the trade "
        "has since ceased, provided it genuinely relates to a liability of that "
        "trade - it is deducted in computing the profit or loss of the final basis "
        "period.", "s.18F", "hard")

    # --- badges of trade, computational context ------------------------------
    o, a = opts("A capital asset realised without any further trading intention - the "
                "gain is not taxable",
                "A trading transaction, taxable on the whole gain",
                "Taxable at 50% of the gain as a compromise",
                "Taxable only if the shares were held for less than a year")
    add("C", "Capital vs revenue",
        "A private investment holding company buys a block of shares intending to "
        "hold them long term for dividend income, and sells them years later at a "
        "large profit after an unsolicited takeover offer. How is the gain treated?",
        o, a,
        "Realising a genuine long-term investment - even profitably, and even where "
        "the sale was prompted by someone else's offer rather than the taxpayer's own "
        "initiative - remains a capital transaction. The stated investment intention, "
        "the long holding period, and the absence of any dealing pattern all point "
        "away from trading.", "", "medium")

    o, a = opts("A trading transaction - an isolated adventure in the nature of "
                "trade, taxable on the whole profit",
                "Always capital, because it was a one-off transaction",
                "Exempt, because the taxpayer's main business is unrelated",
                "Taxable only on 50% of the profit, as a one-off")
    add("C", "Capital vs revenue",
        "A property developer, in a transaction unrelated to its normal projects, "
        "buys a plot of land, obtains planning permission to increase its value, and "
        "resells it within the year at a profit, having taken out short-term finance "
        "for the purchase. How is the profit treated?",
        o, a,
        "Even a single, isolated transaction can amount to trading - an 'adventure "
        "in the nature of trade' - where the badges point that way: short ownership, "
        "supplementary work to enhance saleability (the planning permission), and "
        "short-term finance consistent with an intention to resell rather than hold.",
        "", "medium")

    # --- deeming provisions and non-residents ---------------------------------
    o, a = opts("Deemed to be a trading receipt of a trade carried on in Hong Kong, "
                "even though the recipient carries on no other business here",
                "Exempt, because the recipient has no permanent establishment in "
                "Hong Kong",
                "Taxable only if the recipient is a Hong Kong resident",
                "Taxable at half the standard rate as a concession")
    add("C", "Deeming provisions",
        "A foreign company, with no other presence in Hong Kong, licenses a patent "
        "to a Hong Kong manufacturer for use in Hong Kong and receives royalties for "
        "it. How is the royalty income treated?",
        o, a,
        "Section 15(1) deems specified sums - royalties for the use of intellectual "
        "property in Hong Kong being one - to be a trading receipt arising in Hong "
        "Kong, so as to bring a non-resident owner into charge even without any "
        "physical presence here. Special reduced deemed-profit percentages then apply "
        "under s.21A depending on whether the payer is an associate.", "s.15(1)",
        "hard")

    o, a = opts("30% of the gross royalty, taxed at the standard corporate rate - an "
                "effective rate of about 4.95% - or the full amount where paid to an "
                "associate that has claimed a Hong Kong deduction for it",
                "100% of the gross royalty",
                "The royalty is entirely exempt",
                "50% of the gross royalty in every case")
    add("C", "Deeming provisions",
        "Under s.21A, what proportion of a royalty paid to a non-resident (who is not "
        "an associate of the payer) for the use of intellectual property in Hong Kong "
        "is deemed to be the assessable profit?",
        o, a,
        "Only 30% of the gross sum is deemed assessable, taxed at the ordinary "
        "corporate rate, giving an effective rate of roughly 4.95% on the gross "
        "royalty. Where the recipient is an associate of the Hong Kong payer and the "
        "IP was previously owned by a person carrying on business in Hong Kong, the "
        "full 100% can instead be deemed assessable, closing off a straightforward "
        "profit-extraction route.", "s.21A", "hard")

    o, a = opts("The non-resident's agent, manager or representative in Hong Kong may "
                "be assessed and required to pay the tax on the non-resident's behalf",
                "No one can be assessed if the non-resident itself is untraceable",
                "Only the non-resident's bank can be assessed",
                "The Hong Kong customer who received the goods is automatically "
                "personally liable")
    add("C", "Non-resident businesses",
        "A non-resident person carries on a trade in Hong Kong through a local "
        "agent, and profits arise here. How does IRD collect the tax if the "
        "non-resident itself has no assets or presence in Hong Kong?",
        o, a,
        "Section 20B lets the Commissioner assess and collect the tax from the "
        "non-resident's agent, manager, or anyone else who transacts business with "
        "or on behalf of them in Hong Kong, in the name of the non-resident.",
        "s.20B", "medium")

    # --- double taxation relief -----------------------------------------------
    o, a = opts("Unilateral tax credit relief for the foreign tax paid, capped at the "
                "Hong Kong tax attributable to that income",
                "No relief of any kind is available",
                "A full deduction of the foreign tax as an expense, with no cap",
                "Automatic exemption of the foreign-sourced income")
    add("C", "Double taxation relief",
        "A Hong Kong resident's profits, already taxed in a country with which Hong "
        "Kong has no comprehensive double taxation agreement, are also taxed in Hong "
        "Kong because they are (unusually) treated as Hong Kong sourced. What relief "
        "is available under s.50?",
        o, a,
        "Unilateral tax credit relief allows the foreign tax paid to be credited "
        "against the Hong Kong tax on the same income, but the credit can never "
        "exceed the Hong Kong tax that would otherwise be payable on that income - it "
        "cannot be used to shelter unrelated Hong Kong profits.", "s.50", "hard")

    o, a = opts("It has no effect - profits genuinely sourced outside Hong Kong are "
                "outside the charge regardless of any treaty",
                "It brings all foreign profits into the Hong Kong charge",
                "It exempts all Hong Kong profits of the resident",
                "It replaces the territorial source test entirely")
    add("C", "Double taxation relief",
        "What is the practical effect of Hong Kong's comprehensive double taxation "
        "agreements on profits that are genuinely offshore under Hong Kong's own "
        "source rules?",
        o, a,
        "Hong Kong's territorial system already excludes genuinely offshore profits "
        "without needing a treaty. The DTA network mainly matters where profits "
        "would otherwise be taxed in both jurisdictions under each one's own rules, "
        "or to reduce foreign withholding tax on Hong Kong residents' cross-border "
        "income - it does not change what counts as Hong Kong-sourced in the first "
        "place.", "", "hard")

    # --- interest income ------------------------------------------------------
    o, a = opts("Taxable - the exemption for interest on a deposit was withdrawn for "
                "any person carrying on a trade, profession or business in Hong Kong",
                "Exempt in every case, regardless of who earns it",
                "Taxable only for individuals, never for companies",
                "Taxable only if the deposit is with an overseas bank")
    add("C", "Interest income",
        "A Hong Kong company deposits its surplus cash with a licensed Hong Kong "
        "bank and earns interest. Is the interest chargeable to profits tax?",
        o, a,
        "Since April 1998 the blanket exemption for Hong Kong-source deposit "
        "interest was withdrawn for any person carrying on business in Hong Kong: "
        "the interest is a trading receipt of the business and taxable, and, if the "
        "money deposited represents funds of the trade, it may even be considered "
        "sourced in Hong Kong on ordinary principles regardless of the deposit "
        "exemption question.", "s.15(1)(f)", "medium")

    # --- further deductions and computation practice --------------------------
    o, a = opts("Deductible - insurance premiums covering the trade's own risks are a "
                "normal revenue expense",
                "Never deductible - all insurance is treated as capital",
                "Deductible only for buildings, not for plant or stock",
                "Deductible only up to 10% of assessable profits")
    add("C", "Deductions",
        "A company insures its trading stock and premises against fire. Are the "
        "premiums deductible?",
        o, a,
        "Ordinary business insurance premiums, covering the risks of the trade "
        "itself, are incurred in the production of profits and deductible under "
        "s.16(1) like any other overhead.", "s.16(1)", "easy")

    o, a = opts("Not deductible - a fine or penalty for breaking the law is never an "
                "allowable expense, however closely connected with the trade",
                "Deductible in full, since it arose directly from carrying on the "
                "trade",
                "Deductible at 50%, split between the offence and the trade",
                "Deductible only if the taxpayer successfully appeals the fine")
    add("C", "Non-deductible expenditure",
        "A company is fined for breaching pollution control regulations while "
        "operating its factory. Is the fine deductible against its profits?",
        o, a,
        "A fine or penalty imposed for breaking the law is against public policy to "
        "allow as a deduction, and case law is consistent that it is never "
        "deductible, regardless of how directly it arose out of the trade.", "",
        "medium")

    o, a = opts("Deductible - a contribution to a recognised occupational retirement "
                "scheme or MPF scheme for employees, up to 15% of the employee's total "
                "emoluments for the year",
                "Deductible without limit",
                "Not deductible - only the employee's own contribution is allowed",
                "Deductible only for a scheme registered outside Hong Kong")
    add("C", "Deductions",
        "A company contributes to a retirement scheme for the benefit of its staff. "
        "What is the deduction limit for an ordinary (non-mandatory) employer "
        "contribution?",
        o, a,
        "Section 16A caps the deduction for an employer's ordinary annual "
        "contribution at 15% of the total emoluments of the employees concerned for "
        "the period - a special, more generous rule applies to the special "
        "contribution made when a scheme is first set up.", "s.16A", "hard")

    for wdv, additions, disposals in [(300000, 400000, 0), (900000, 150000, 200000)]:
        r = T.da_pool(wdv, additions, disposals, rate=0.20, initial=True)
        o, a = opts(M(r["total"]), M(r["aa"]), M(r["ia"]),
                    M(round((wdv + additions - disposals) * 0.20, 2)))
        add("C", "Depreciation allowances",
            "A 20%%-pool has a written-down value brought forward of %s. During the "
            "year the business bought qualifying plant for %s and sold plant for %s. "
            "What is the total depreciation allowance for the year?"
            % (M(wdv), M(additions), M(disposals)),
            o, a,
            "Additions %s less the 60%% initial allowance %s leaves a reduced pool "
            "of %s; the 20%% annual allowance on that gives %s. Total allowance = IA "
            "%s + AA %s = %s."
            % (M(additions), M(r["ia"]), M(r["reduced"]), M(r["aa"]), M(r["ia"]),
               M(r["aa"]), M(r["total"])),
            "s.39B; Sch. 3", "hard", "computational")

    o, a = opts("A trader has no general right to choose the pool rate for an "
                "asset - the rate is prescribed by the Board of Inland Revenue "
                "according to the asset's type",
                "The trader may elect any of the three rates for any asset",
                "All assets are pooled together at a single blended rate",
                "The rate depends on how the taxpayer classifies the asset in its "
                "own accounts")
    add("C", "Depreciation allowances",
        "Who determines which of the 10%, 20% or 30% pool an item of plant or "
        "machinery falls into?",
        o, a,
        "The rate for each type of asset is prescribed in the Inland Revenue Rules; "
        "a taxpayer cannot simply choose a more favourable rate for an asset that "
        "does not qualify for it.", "Sch. 3", "medium")

    o, a = opts("It is deductible - premiums for insuring against the risk of an "
                "employee's negligence or dishonesty causing loss to the trade are a "
                "normal business expense",
                "It is never deductible, being akin to a private expense",
                "It is deductible only if the employee is a director",
                "It is deductible only up to the amount of the excess/deductible "
                "under the policy")
    add("C", "Deductions",
        "A company takes out fidelity guarantee insurance against loss caused by "
        "employee dishonesty. Is the premium deductible?",
        o, a,
        "This protects the trade's own assets against a trading risk and is treated "
        "the same way as fire or other business insurance - a normal deductible "
        "overhead.", "s.16(1)", "medium")


if __name__ == "__main__":
    area_a()
    area_b()
    area_c()
    area_d()
    area_e()
    print("generated: %d questions" % len(BANK))
    for k in sorted(AREAS):
        print("   %s  %-34s %3d" % (k, AREAS[k], sum(1 for q in BANK if q["area"] == k)))

    # Duplicate-question guard: a copy-pasted loop body is the likeliest way two
    # questions end up identical. Compare on the question text plus its options,
    # since the same fact can legitimately be asked twice with different numbers.
    seen = {}
    dupes = []
    for q in BANK:
        key = (q["q"], tuple(q["options"]))
        if key in seen:
            dupes.append((seen[key], q["id"]))
        else:
            seen[key] = q["id"]
    if dupes:
        print("\nDUPLICATE QUESTIONS DETECTED:")
        for a_id, b_id in dupes:
            print("   %s == %s" % (a_id, b_id))
        sys.exit(1)

    topics = sorted(set(q["topic"] for q in BANK))
    print("\n%d distinct topics across %d questions" % (len(topics), len(BANK)))

    payload = {
        "title": "ACCA TX-HKG",
        "subtitle": "Section A Practice Question Bank",
        "generated": "2026-09-28",
        "count": len(BANK),
        "areas": AREAS,
        "questions": BANK,
    }
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print("\nwrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))
