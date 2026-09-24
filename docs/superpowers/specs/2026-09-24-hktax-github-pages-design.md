# HK Tax Study Hub: Public Site on GitHub Pages

## Summary / 摘要

Publish the HK Tax Study Hub as an openly public study site at
`https://anthonymankaho.github.io/hktax-studyhub/`, using GitHub Pages served
directly from the existing repository. No second repo, no login gate, no build
pipeline — the repo is already public and the site is already static HTML.

把 HK Tax Study Hub 以公開學習網站形式發布於
`https://anthonymankaho.github.io/hktax-studyhub/`，直接由現有 repo 透過
GitHub Pages 寄存。不另開 repo、不設登入閘、不加建置流程——該 repo 本來就公開，
網站本來就是靜態 HTML。

**This differs deliberately from [MEYERGPR](../../../../Global%20Purchase%20Report%20Claude/docs/superpowers/specs/2026-09-24-meyergpr-public-dashboard-design.md).**
That spec kept a confidential source repo private and mirrored only the finished
artifact into a new public repo behind a login gate, because the Global Purchase
Report contains vendor names and prices. This project has **no company or client
data** — it is tax legislation, IRD guidance and study notes. The user reviewed
the exposure audit below and chose an open site. The cost of that choice is that
the attribution and redistribution housekeeping in §3 becomes **mandatory**, not
optional.

**本規格刻意與 MEYERGPR 不同。** 該規格因採購報表含供應商名稱及價格，故保持原始
repo 私密、只把成品鏡像到新的公開 repo 並加登入閘。本專案**不含任何公司或客戶
資料**，只有稅務法例、稅務局指引及學習筆記。使用者已檢視下方的暴露評估並選擇公開
網站。代價是 §3 的署名與再發布整理工作變成**必須完成**，而非可選。

## Exposure audit / 暴露評估

Measured 2026-09-24, not estimated.

| Item | Finding |
|---|---|
| Company or client data | **None.** Every tracked text file scanned; the only "password" matches are the IRD fraud-alert text this Hub itself wrote. |
| Credentials, tokens, API keys | **None.** |
| Third-party PDFs redistributed | **83 files, ~34 MB** — Cap. 112 (24 MB), Cap. 117, 73 DIPN/SOIPN, BIR forms. |
| Derived textbook content | Module 9: Principles of Taxation (4th ed.), paraphrased throughout and flagged inline. |
| Repo's own stated policy | README says *"Internal, team-only reference and study tool — not for external distribution or publication."* Contradicts the site. |
| Duplicate | `AnthonyManhk/hktax-studyhub` is a second public copy of the same content. |

The first two rows are why this can be an open site at all. Rows 3–6 are what §3
has to resolve first.

前兩項是本專案可以公開的原因；第 3 至 6 項是 §3 必須先處理的事。

## Decisions / 已定決策

| Decision | Choice |
|---|---|
| GitHub plan | Free |
| Hosting repo | **Existing** `anthonymankaho/hktax-studyhub` — no new repo |
| Repo visibility | Public (unchanged) |
| Login gate | **None** — open study resource |
| Search indexing | **Allowed** — this is the opposite of MEYERGPR |
| Deployment | Pages, deploy from branch `master`, folder `/` (root). No Actions. |
| Build step | None at deploy time. `scripts/build-combined.py` stays a local, pre-commit step. |
| Update trigger | Push to `master`; Pages redeploys automatically |
| Custom domain | Not now — revisit only if the team wants a branded URL |

## Non-goals / 非目標

- **Not a professional advice service.** The site stays an internal-standard
  study aid that happens to be readable by others. No claim of authority, no
  advice offered, no reader relationship implied.
- **Not a mirror of IRD.** After §3.2 the site links to ird.gov.hk rather than
  rehosting its PDFs. Keeping a full DIPN archive online is IRD's job, not ours.
- **No CI/CD, no Actions, no server, no database.** Static files only.
- **Not automatic.** Publishing a content change is still an explicit
  `build → review → commit → push`, matching this project's established pacing.

**非專業意見服務。** 網站僅為學習輔助，不提供意見、不建立顧問關係。
**非稅務局鏡像。** 完成 §3.2 後只連結 ird.gov.hk，不再自行寄存其 PDF。
**無 CI/CD、無後端。** 純靜態檔案。
**非自動化。** 仍維持「建置→審閱→提交→推送」的明確步驟。

## 3. Prerequisites — must complete before enabling Pages / 啟用 Pages 前必須完成

Enabling Pages takes about ninety seconds. These four items are the actual work,
and the reason to do them *first* is that once the site is indexed, undoing a
mistake means waiting for search engines to re-crawl.

啟用 Pages 只需約九十秒；以下四項才是實際工作。必須先做的原因是：一旦被搜尋引擎
收錄，改正錯誤就要等待重新檢索。

### 3.1 Rewrite the README's framing

The current opening line directly contradicts a public site. Replace the
"internal, team-only, not for external distribution" framing with:

- what the site is (a study aid for HK tax, built from IRD's own published
  guidance and legislation),
- who maintains it and in what capacity,
- an explicit **no-advice disclaimer**,
- the licence position from §3.3,
- a pointer to the live URL.

Keep everything else — the refresh workflow, folder map, caveats and the
"verify before relying on a figure" warnings are all still correct and are
arguably *more* important on a public site than a private one.

### 3.2 Stop redistributing the PDFs

Replace the hosted `Data/` archive with links to the primary sources.

- `Data/` becomes local-only: add a `.gitignore` entry and
  `git rm -r --cached Data/`. The PDFs stay on disk for the local refresh
  workflow; they simply stop being committed.
- The freshness machinery is unaffected. `assets/js/data-manifest.js` is
  currently `{generatedAt: null, files: []}` — it has never been populated, so
  nothing on any page depends on those files being in the repo. Confirmed by
  reading `freshness.js`: it degrades to "unknown" and renders nothing when the
  manifest is empty, which is already today's behaviour.
- Add a **Sources** page (or a section on the DIPN Index) linking each DIPN,
  SOIPN, ordinance and form to its canonical ird.gov.hk / elegislation.gov.hk
  URL. This is strictly better for readers anyway — a link is always current,
  a committed PDF goes stale the moment IRD revises it.
- Repo drops from ~34 MB to roughly 1 MB. Clone and Pages deploy get fast.

**On git history — be honest about what this does and does not achieve.**
`git rm --cached` stops serving the PDFs and removes them from future commits,
but every old commit still contains them and they remain reachable on GitHub.
Two options:

| Option | Effect | Cost |
|---|---|---|
| `git rm --cached` only *(recommended)* | Site stops serving them; history still holds them | Zero risk, five minutes |
| `git filter-repo` + force-push both remotes | Genuinely gone from history | Rewrites every SHA, breaks existing clones, must be done on both `anthonymankaho` and `AnthonyManhk` |

The recommendation is the first. These are public government documents, freely
downloadable from IRD; the goal is to stop *presenting* them as our archive, not
to erase evidence. Escalate to `filter-repo` only if someone raises a formal
objection.

### 3.3 Decide the licence

Two different things need two different answers, and a single `LICENSE` file at
repo root would wrongly imply one covers both:

- **Code** (`scripts/build-combined.py`, `assets/js/*.js`, the CSS) — MIT is the
  obvious default unless there's a reason otherwise.
- **Study content** (the HTML pages' prose, tables and illustrations) — this is
  derived from Module 9 and from IRD's DIPNs. It cannot be MIT-licensed as if it
  were original. State it as: *"Study notes, paraphrased from the sources cited
  inline. Not licensed for redistribution. Cited material remains the property
  of its respective owners."*

Put both statements in `README.md` and in a short `LICENSE` file that
distinguishes them explicitly.

### 3.4 Settle the Module 9 derivation

The existing practice is already the right one — facts paraphrased, never
reproduced verbatim, with the source flagged inline and every stale figure
corrected and shown as corrected. Publishing does not change what the content
*is*, but it does change who can see it. Two concrete actions:

1. Add a visible attribution note, once, on each illustrations page: what the
   source is, that facts are paraphrased not reproduced, and that the figures
   have been independently recomputed against current law.
2. Spot-check the illustrations pages for any passage that reads closer to
   transcription than paraphrase, and rewrite those. This is a reading pass, not
   a rewrite of the pages.

If HKICPA's own terms for Module 9 turn out to prohibit derived study notes
being published, that is a stop condition for §3.4 — not for the whole site.
The DIPN-sourced illustrations and the rules pages stand on their own.

## 4. Architecture / 架構

Nothing is built. GitHub Pages serves the repo root as-is.

```
hktax-studyhub/                     (public, Pages source: master / root)
├── index.html                      ← Pages landing page; already the hub
├── .nojekyll                       ← NEW: disable Jekyll processing
├── robots.txt                      ← NEW: allow all (opposite of MEYERGPR)
├── LICENSE                         ← NEW: code vs content, per §3.3
├── README.md                       ← rewritten per §3.1
├── HK Tax Study Hub - Combined.html   generated; also served
├── combined.html                   ← NEW: clean-URL copy of the above
├── pages/*.html                    17 pages
├── assets/css, assets/js           inlined into the combined file, served here for the multi-file site
├── scripts/build-combined.py       not served in any meaningful sense; harmless
└── Data/                           REMOVED from tracking per §3.2 (stays on disk locally)
```

### Why `.nojekyll`

Without it, Pages runs Jekyll over the repo. Jekyll ignores files and folders
beginning with `_` and can rewrite content in ways that are hard to debug on a
344 KB single-file document. An empty `.nojekyll` at root turns that off. There
is no upside to Jekyll here — nothing in this repo is Markdown-templated.

### Why `combined.html`

The combined file's real name contains spaces, so its URL is
`.../HK%20Tax%20Study%20Hub%20-%20Combined.html` — unpleasant to paste into
Slack or an email. Have `scripts/build-combined.py` write a second copy at
`combined.html` (one extra line in `main()`), giving
`https://anthonymankaho.github.io/hktax-studyhub/combined.html`. Keep the
spaced filename too: that is the one people save as an email attachment, and
its name is what makes it recognisable in a Downloads folder.

### `robots.txt`

```
User-agent: *
Allow: /

Sitemap: https://anthonymankaho.github.io/hktax-studyhub/sitemap.xml
```

A sitemap is optional for 18 pages; add it only if indexing turns out to be
patchy after a few weeks.

### On-site disclaimer

The hub already carries the right caveats in its footer. Add one short block to
`index.html`'s hero, above the fold, stating: study aid only, not professional
advice, verify against the Inland Revenue Ordinance and current IRD guidance
before acting. A reader arriving from a search engine has not read the README.

## 5. The duplicate repo / 重複的 repo

`AnthonyManhk/hktax-studyhub` is a second public copy. The local working copy
pushes to `anthonymankaho` as `origin` and `upstream`, and to `AnthonyManhk` as
`backup`.

**Checked 2026-09-24: the two remotes have not diverged.** Both `origin/master`
and `backup/master` are at `010d867` (2026-08-14). Local `master` is ahead at
`7a5f2ea` (2026-09-23) plus this session's uncommitted work. So there is no
"which tree is newer" problem to resolve — there is only a choice of which one
to keep public.

Two public copies of the same site is still a maintenance trap: only one can be
the canonical URL, and the other will silently drift and eventually serve stale
tax figures to anyone who finds it. Before enabling Pages:

- **Recommended:** make `AnthonyManhk/hktax-studyhub` **private**. It is the
  backup remote, and every other repo on that account is already private — it
  is the odd one out, which is itself a hint that its public status was never
  deliberate. Enable Pages on `anthonymankaho` only, matching the MEYERGPR
  owner choice.
- Alternative: keep both public but enable Pages on one, and put a one-line
  pointer in the other's README.

## 6. Publication procedure / 發布步驟

Run in order. Steps 1–4 are §3; do not skip ahead to 5.

1. Rewrite `README.md` (§3.1).
2. `.gitignore` + `git rm -r --cached Data/`; add the Sources links page (§3.2).
3. Add `LICENSE`; add the licence statement to the README (§3.3).
4. Add attribution notes to the illustrations pages; spot-check for
   transcription (§3.4).
5. Add `.nojekyll`, `robots.txt`, the `combined.html` build output, and the
   hero disclaimer.
6. Rebuild: `python scripts\build-combined.py`. Re-run the Playwright checks.
7. Commit and push to `anthonymankaho/hktax-studyhub` `master`.
8. Settle the duplicate repo (§5).
9. GitHub → repo Settings → Pages → Source: *Deploy from a branch* →
   Branch: `master`, folder `/ (root)` → Save.
10. Wait for the first deploy (usually under two minutes; the Actions tab shows
    a `pages-build-deployment` run).
11. Validate (§7).
12. Only then share the URL.

## 7. Validation / 驗證

On the live URL, in a fresh private window:

1. `https://anthonymankaho.github.io/hktax-studyhub/` loads the hub.
2. Every nav link and every hub card resolves — no 404s. Pages is
   case-sensitive where Windows is not, so a link that works locally can 404
   when deployed. This is the single most likely deployment failure.
   *Checked 2026-09-24: all `href`/`src` references across `index.html` and
   `pages/*.html` currently resolve with exact case — zero problems. Re-run the
   check after any page is added, since Windows will not catch a regression.*
3. `combined.html` loads; card index, tab switching, all three data tables,
   search, dark mode all work. The Playwright suite can be pointed at the live
   URL instead of `file://` for this.
4. `Data/` paths 404 — confirming the PDFs are no longer served.
5. View-source on two pages: the disclaimer is present, no stray
   `noindex` left anywhere.
6. Mobile width — the combined file was verified clean at 400 px locally;
   confirm on a real phone once.
7. `robots.txt` resolves and reads `Allow: /`.

## 8. Rollback / 回復方式

- **Take the site down:** Settings → Pages → Source: *None*. Live within
  minutes; deletes nothing.
- **De-index after takedown:** removing the site leaves search results behind
  for a while. Use Google Search Console's removal tool if it needs to be
  immediate.
- **Revert a bad content push:** `git revert` and push; Pages redeploys.
- **Full retreat:** flip the repo to private. Pages on a private repo requires a
  paid plan, so the site stops serving — which is the desired effect here.

## 9. Open items / 待決事項

- **HKICPA's terms for Module 9** — the one genuine unknown (§3.4). Worth
  checking before step 4, not after.
- **Which remote is canonical** (§5) — needs a look at both trees, not a guess.
- **Whether to keep `scripts/` and `docs/` in the published tree.** Harmless
  (Pages serves them but nothing links to them) and useful for anyone who wants
  to see how the site is built. Default: keep.
- **Analytics.** Not proposed. If the team later wants to know whether anyone
  reads it, that is a separate decision with its own privacy implications.
- **Who fields questions** if a member of the public emails about a tax position
  they read here. The disclaimer should make clear that no one does.
