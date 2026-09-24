# HK Tax Study Hub

A study aid for Hong Kong tax — profits tax, property tax, salaries tax, stamp
duty, depreciation allowances and IRD administration — built from the Inland
Revenue Department's own published guidance and from the Inland Revenue
Ordinance (Cap. 112) and Stamp Duty Ordinance (Cap. 117).

**Live site:** <https://anthonymankaho.github.io/hktax-studyhub/>

Static HTML, no server and nothing to install: open `index.html` in a browser.
It is a single self-contained file — the whole Hub, every page, one download.

## ⚠️ Disclaimer — read this first

**This is study material, not professional advice.** Nothing here is tax advice,
no adviser–client relationship is created by reading it, and no one maintaining
it will answer questions about your tax position.

It is written to an internal working standard for one finance team's own
learning and analysis. It is published openly because the underlying material is
public, not because it has been reviewed for anyone else's use. It will contain
mistakes, and it goes out of date whenever the law changes.

**Before relying on any figure or section reference for a filing position,
verify it against the Inland Revenue Ordinance (Cap. 112), the Stamp Duty
Ordinance (Cap. 117), and current IRD guidance.** Every page carries the same
warning for the same reason.

## Licence

Two different things, two different answers:

- **Code** — `scripts/`, `assets/js/`, `assets/css/`: MIT. See [`LICENSE`](LICENSE).
- **Study content** — the prose, tables and worked illustrations in
  `index.html` and `pages/`: **not licensed for redistribution.** These are
  study notes paraphrased from the sources cited inline. Read them, link to
  them; please do not republish them as your own.
- **Cited material** — IRD's DIPNs/SOIPNs, the ordinances, the BIR forms, and
  the textbook the illustrations derive from remain the property of their
  respective owners. This repository does **not** redistribute them; it links to
  the publishers' own copies.

## What this is for

1. **Tax computation / transaction analysis** — for financial-statement tax
   computations of Hong Kong incorporated companies, confirming under which
   IRO/SDO section a transaction is Taxable / Non-taxable / Deductible /
   Non-deductible. Use the **Transaction Checker** for this.
2. **Study material** — rules, tables, and worked illustrations per tax
   topic, drawn from IRD's own guidance (DIPNs/SOIPNs) and a professional
   taxation textbook (Module 9: Principles of Taxation, 4th ed.), with every
   figure cross-checked against current law.

## Start here

Open `index.html` (or the live site). From the card index you can reach:

| Page | Purpose |
|---|---|
| **IRD What's New** | Every item on IRD's What's New page, read against this Hub and marked **enacted** / **bill** / **proposed**, with the exact page each item changed. Open this first after any IRD refresh. |
| **Transaction Checker** | Search any transaction by keyword → Taxable/Non-taxable/Deductible/Non-deductible/Dutiable, with the exact section and a link to the full explanation. |
| **DIPN Index** | Searchable catalogue of all 73 currently-in-force DIPN/SOIPN/EDOIPN documents, with topic, summary, and whether it backs a full study page or is reference-only. |
| **Profits Tax / Property Tax / Salaries Tax / Stamp Duty / Depreciation & Allowances** | The five core topic pages — charging basis, rates, taxable/deductible tables, computation templates, all tied to exact IRO (Cap. 112) / Stamp Duty Ordinance (Cap. 117) sections. |
| **[Topic] — Worked Illustrations** | Companion page per topic (linked from each topic page's Illustrations section) with every worked example — DIPN-sourced and textbook-sourced — in one place. |
| **Profits Tax Return Guide** / **Box Finder** | Box-by-box walkthrough of the actual BIR51/52/54 return forms (linked from the Profits Tax page) — bridges "what the law says" to "what you type into the form," plus a keyword search over every box. |
| **IRD Administration** | Returns, assessment, objections/appeals, provisional tax, penalties — the process layer common to all taxes. |

## How it stays current

This is a **manual-refresh** tool by design — it does not, and cannot, live-fetch
ird.gov.hk from inside a browser-opened HTML file. The loop is:

1. **Download** an updated CAP112 / CAP117 / DIPN / SOIPN PDF and drop it into
   the matching `Data/` subfolder (see `Data/README.md` for the folder map).
2. **Run** `scripts\Refresh-Data-Manifest.bat` (double-click it) — it rescans
   `Data/` and rebuilds the file-date manifest the pages check against.
3. **Reload** the page. If a source file is now newer than that page's
   "last reviewed" date, the freshness banner at the top turns amber/red,
   telling you which page needs a re-check.
4. **Ask Claude** (in a Claude Code session) to re-read the updated source and
   refresh that page's content — step 2 only detects *that* something
   changed, not *what* changed.

### Checking IRD's What's New

Steps 1–3 watch the *saved PDFs*. They cannot see a new announcement on
ird.gov.hk. For that, ask Claude to read
<https://www.ird.gov.hk/eng/new/index.htm> and update the Hub. Claude should:

- Add or update rows in **`pages/ird-updates.html` §2** so the page records
  what was read, on what date, and which page changed.
- Mark each item **enacted** / **bill** / **proposed**. A Policy Address
  measure is *not* law on announcement day — keep the enacted figure as the
  Hub's primary statement and carry the change as a marked note beside it.
- Update the "read on" date in the banner at the top of `ird-updates.html`
  **and** `IRD_READ_DATE` in `scripts/build-combined.py`.
- Re-run the combined build (below).

Last read: **24 September 2026** (38 items, 1 Jun – 16 Sep 2026).

`elegislation.gov.hk` (for CAP112/CAP117) gates automated downloads behind a
JS/cookie check — a normal browser download works fine, but re-fetching it
programmatically does not, so step 1 for legislation is a manual download.

## Data sources already in `Data/`

- **`CAP112/`** — Inland Revenue Ordinance, consolidated, current to 6.6.2025 per page-level stamps in the text. Covers Profits Tax, Property Tax, Salaries Tax, Depreciation Allowances, and administration provisions.
- **`CAP117/`** — Stamp Duty Ordinance (a *separate* ordinance from Cap. 112), consolidated, current to 26.2.2026.
- **`DIPN/`** — all 64 current DIPNs (1–63 plus 13A), organized into subfolders by topic (`Profits-Tax/`, `Property-Tax/`, `Salaries-Tax/`, `Stamp-Duty/`, `Depreciation-Allowances/`, `Cross-Border-Transfer-Pricing/`, `Special-Regimes/`, `Other/`).
- **`IRD-Administration/`** — DIPN 6, 11, 31 (objections/appeals, field audit, advance rulings).
- Stamp Office notes (SOIPN 1–8) live under `DIPN/Stamp-Duty/`.
- **`PwC/`** — reserved for saved PwC Worldwide Tax Summaries pages (cross-check source; not yet populated with saved files).
- **`Forms/`** — BIR51/52/54 Profits Tax Return forms + Notes and Instructions, and IRC1952/1953 Notice to File forms, revision 4/2025.

See `Data/DIPN-CHECKLIST.md` for the full document-by-document status, and
`Data/README.md` for the refresh mechanics in more detail.

## What's fully built vs. reference-only

The **five core taxes** (Profits, Property, Salaries, Stamp Duty, Depreciation
& Allowances) have complete study pages: rules, taxable/deductible tables,
computation templates, and a dedicated worked-illustrations page each.

Everything else IRD publishes a DIPN on — transfer pricing, aircraft/ship
leasing concessions, corporate treasury, offshore funds, cross-border DTAs,
estate duty (historical) — is **downloaded and briefly summarized** in the
DIPN Index, but does not have that same depth of treatment yet. Ask Claude to
build a dedicated page for any of these if your team needs deeper coverage.

## Where the worked illustrations come from

Each topic's "Worked Illustrations" page draws on two kinds of source,
labelled inline:

- **From IRD DIPNs/SOIPNs** — official illustrative examples, paraphrased
  (not reproduced verbatim).
- **From Module 9: Principles of Taxation (4th ed.)** — a professional
  taxation qualification manual. Facts are paraphrased; every allowance/rate
  figure has been checked against current law and **corrected where the
  textbook was using a stale amount** (e.g. old personal allowances, the
  pre-2023 flat-15% stamp duty rate) — each correction is flagged inline as
  "Original book figure used X; current law is Y."

A second textbook — *Hong Kong Taxation and Tax Planning* (22nd ed., Ho & Mak)
— **can** now be used, correcting an earlier note here. It is still a scanned
PDF with no text layer and there is still no OCR, so text extraction returns
nothing. But PyMuPDF renders each page to an image, and those images can be
read directly. The workflow that works: locate pages through the book's own
index at the back, convert book page to PDF page (**PDF page = book page + 21**
for this file), render at ~135 dpi, then read. The
[Computation Formats](pages/computation-formats.html) page was built this way.

Two limits: reading is one page at a time, so target chapters rather than
sweeping all 920 pages; and the book states the law only **to 31 May 2024**, so
every rate and allowance taken from it must be re-checked against IRD.

## Folder structure

```
index.html                       GENERATED — the site's landing page; same app as below
combined.html                    GENERATED — identical, clean URL for sharing
HK Tax Study Hub - Combined.html GENERATED — identical, the name people recognise
                                 as an email attachment
pages/                           THE SOURCES. Edit these, then rebuild.
  ird-updates.html               IRD What's New, marked enacted / bill / proposed
  module9-extra-practice.html    Extra paraphrased Module 9 practice Q&A
  transaction-checker.html       Search tool: transaction → tax treatment
  dipn-index.html                Searchable catalogue of all 73 DIPN/SOIPN/EDOIPN docs
  profits-tax.html               + profits-tax-illustrations.html
  profits-tax-return-guide.html  + profits-tax-return-finder.html (BIR51/52/54 box guide + search)
  property-tax.html              + property-tax-illustrations.html
  salaries-tax.html              + salaries-tax-illustrations.html (incl. Personal Assessment)
  stamp-duty.html                + stamp-duty-illustrations.html
  depreciation-allowances.html   + depreciation-allowances-illustrations.html
  ird-administration.html        Returns, assessment, objections/appeals, penalties
assets/
  css/main.css                   Shared design system (light/dark aware)
  js/                            Freshness-check logic, search/filter logic, data files
scripts/
  build-combined.py              Rebuilds the single-file edition from pages/ + assets/
  Refresh-Data-Manifest.bat      Double-click after updating Data/ — rescans and re-stamps dates
  update-manifest.ps1            The PowerShell script the .bat wraps
Data/
  CAP112/, CAP117/               Legislation
  DIPN/<topic>/                  DIPNs + SOIPNs, organized by tax topic
  IRD-Administration/            Admin-specific DIPNs
  Forms/                         BIR51/52/54 return forms + notes
  README.md                      Refresh-workflow details and folder map
  DIPN-CHECKLIST.md              Document-by-document download status
```

## The two editions, and how to rebuild

There are two ways to read the Hub, from **one** set of sources:

- **Single-file app** — a tabbed frame: sticky topbar, a bilingual card index,
  one panel per page, jump-search and a dark-mode toggle. The build writes it
  to three paths, byte-identical:
  - `index.html` — the landing page of the published site
  - `combined.html` — same thing, clean URL for pasting into Slack or email
  - `HK Tax Study Hub - Combined.html` — same thing again; this is the name
    that makes it recognisable in someone's Downloads folder
- **Multi-file** — `pages/*.html` opened individually. These are the sources
  you edit, and they stay browsable on their own.

**All three outputs are generated. Never hand-edit them** — including
`index.html`, which used to be a hand-written hub page and no longer is. Edit
the page under `pages/` and rebuild:

```
python scripts\build-combined.py
```

The builder namespaces every `id`/anchor per page (`salaries-tax__allowances`),
rewrites cross-page links into tab links, inlines the three searchable data
tables, and prints a corruption check. A hand-built combined file previously
lost 994 em-dashes and mangled two Chinese passages by concatenating with the
wrong encoding; the builder reads the clean sources as UTF-8 and writes UTF-8,
so that failure cannot recur.

When adding a page, put it in `pages/`, add a row to `PAGES` in
`scripts\build-combined.py` (id, file, English label, Chinese label, group,
Chinese summary, search keywords), add its nav link to the other pages, and
rebuild.

## Caveats — read before relying on a figure for a filing position

- This is an **internal working document**, not a substitute for professional
  judgement or a final review against the primary legislation.
- CAP112's Part 6 (Depreciation Allowances) and the numbered Schedules did not
  extract cleanly from the currently-saved PDF — those pages' section numbers
  are cross-verified against DIPNs that quote the Ordinance directly, not
  re-derived from a direct grep. Re-verify against a fresh Cap. 112 download
  if you need precision on a specific sub-clause.
- Any figure tied to an **annual Budget measure** (one-off tax reductions,
  elderly-care expense caps, etc.) is flagged rather than guessed where the
  current year's figure wasn't independently confirmed — check the current
  Budget before treating those as final.
- Every page shows a "last reviewed" date and a freshness banner — check both
  before relying on a page for a filing decision.
- Items marked **proposed** on the IRD What's New page (currently the two 2026
  Policy Address measures — the $160,000 child allowance for second and
  subsequent children, and the $20,000 newborn-family stamp duty waiver) are
  **not law**. Each needs an amendment ordinance. Quote the enacted figure in
  any computation until the ordinance is gazetted.
