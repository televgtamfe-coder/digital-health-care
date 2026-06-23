# README Premium Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework the public GitHub README into the approved light premium homepage layout while preserving the current body copy and project coverage.

**Architecture:** This implementation only changes markdown composition inside `README.md`. The work will keep all existing prose, regroup the page into the approved five visual bands, refine the opening hierarchy, and add restrained separators and navigation so the same content reads like a premium public profile instead of a technical repository page.

**Tech Stack:** GitHub-flavored Markdown, git, PowerShell verification commands

---

## File Structure

- Modify: `README.md`
  - Recompose the opening block
  - Rebuild top-level section rhythm into the approved premium layout
  - Preserve all existing paragraph text and subsection content
- Reference: `docs/superpowers/specs/2026-06-23-readme-premium-layout-design.md`
  - Source of truth for layout, tone, and preservation constraints

### Task 1: Rebuild the README opening and band structure

**Files:**
- Modify: `README.md`
- Reference: `docs/superpowers/specs/2026-06-23-readme-premium-layout-design.md`

- [ ] **Step 1: Back up the current README structure for quick comparison**

Run:

```powershell
Copy-Item -LiteralPath D:\workflow\output\digital-health-care-profile\README.md -Destination D:\workflow\output\digital-health-care-profile\archives\README-before-premium-layout.md
```

Expected: a copy of the current README exists at `archives/README-before-premium-layout.md`

- [ ] **Step 2: Replace the repository-style opening with the premium opening block**

Rewrite only the opening markdown structure at the top of `README.md` so it follows this shape, while preserving the existing title, summary line, and domain labels:

```md
# Health Strategy & Digital Care

> [existing summary line kept exactly as-is]

`Digital Health` `Women's Health` `Maternal Care` `Internet Healthcare` `Health Service` `AI-Enabled Workflow`

---

## About

[existing 关于我 body copy stays exactly the same]
```

Implementation note: keep the existing Chinese body text intact; only change the surrounding markdown framing and add the horizontal rule.

- [ ] **Step 3: Recompose the top-level sections into the five approved visual bands**

Update `README.md` so the page flows in this exact top-level order:

```md
# Health Strategy & Digital Care
[opening block]

---

## About
[existing 关于我 content]

---

## Long-term Scope
[existing 长期负责的方向 and all existing subsections/content]

---

## Selected Work
[existing 代表性项目与项目面 and all existing subsections/content]

---

## Judgment, Execution, and Methods
[existing sections in this order:
我通常如何判断一个需求
我如何带团队把项目从调研推进到落地
我常用的组织与推进方式
对技术框架和 AI 应用的理解
一些关于商业、组织与长期价值的看法
我常用的知识框架与 skills 结构
从这些项目里沉淀下来的几条稳定判断]

---

## Closing
[existing 结尾 content]
```

Implementation note: use English band headings exactly as above to create the public-homepage feel, but keep all existing Chinese subsection headings and paragraphs under each band.

- [ ] **Step 4: Run a heading scan to verify the new hierarchy is correct**

Run:

```powershell
rg -n "^(#|##|###) " D:\workflow\output\digital-health-care-profile\README.md
```

Expected: the top-level sequence shows `About`, `Long-term Scope`, `Selected Work`, `Judgment, Execution, and Methods`, and `Closing`, with all existing `###` project and scope subsections still present.

- [ ] **Step 5: Commit the structural rewrite**

Run:

```powershell
git -C D:\workflow\output\digital-health-care-profile add README.md archives/README-before-premium-layout.md
git -C D:\workflow\output\digital-health-care-profile commit -m "Restructure README into premium public profile layout"
```

Expected: a commit is created containing only the README layout restructure and the backup archive copy.

### Task 2: Add premium rhythm, restrained navigation, and final polish

**Files:**
- Modify: `README.md`
- Reference: `docs/superpowers/specs/2026-06-23-readme-premium-layout-design.md`

- [ ] **Step 1: Add a compact top navigation block under the opening section**

Insert this navigation block after the opening rule and before `## About`:

```md
<p align="left">
  <a href="#about">About</a> ·
  <a href="#long-term-scope">Long-term Scope</a> ·
  <a href="#selected-work">Selected Work</a> ·
  <a href="#judgment-execution-and-methods">Judgment, Execution, and Methods</a> ·
  <a href="#closing">Closing</a>
</p>
```

Implementation note: keep this as plain HTML text links only. Do not add icons, badges, or button styling.

- [ ] **Step 2: Tighten section presentation with restrained labels and separators only where useful**

Apply the following markdown pattern consistently to each major band in `README.md`:

```md
---

## Selected Work

[section content preserved]
```

And apply the following pattern to the appendices area near `我常用的知识框架与 skills 结构` so the linked companion files feel deliberate rather than tacked on:

```md
- [Methods, Skills & Agents](./METHODS_SKILLS_AND_AGENTS.md)
- [Full Skills & Agents Inventory](./FULL_SKILLS_AND_AGENTS_INVENTORY.md)
```

Implementation note: keep the existing links, but ensure they sit after a short lead-in paragraph and before the following major section break.

- [ ] **Step 3: Verify that body copy and project coverage were preserved**

Run:

```powershell
git -C D:\workflow\output\digital-health-care-profile diff --word-diff -- README.md
```

Expected: the diff shows mostly heading, separator, ordering, and layout changes. Existing paragraphs and project descriptions should remain materially unchanged.

- [ ] **Step 4: Do a final readability pass on the rendered markdown source**

Run:

```powershell
Get-Content -Encoding UTF8 -TotalCount 140 D:\workflow\output\digital-health-care-profile\README.md
```

Expected: the first 140 lines read as a calm public homepage opening with a clean title, summary, navigation, `About`, and the start of `Long-term Scope`.

- [ ] **Step 5: Commit the polish pass**

Run:

```powershell
git -C D:\workflow\output\digital-health-care-profile add README.md
git -C D:\workflow\output\digital-health-care-profile commit -m "Polish README as premium public homepage"
```

Expected: a second commit is created with the navigation and premium rhythm polish.

## Self-Review

- Spec coverage check: this plan covers the premium opening, five-band layout, strong project center, restrained method placement, and content preservation rules from the design spec.
- Placeholder scan: no `TODO`, `TBD`, or implicit follow-up instructions remain.
- Consistency check: the approved band names are used consistently in the markdown structure, nav anchors, and verification steps.

