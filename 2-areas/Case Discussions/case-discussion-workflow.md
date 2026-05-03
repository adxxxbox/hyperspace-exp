---
title: Case Discussion Workflow
created: 2026-04-13
---

# Case Discussion Workflow

## A. When a clinical case is given:

### 1. Folder Creation
- Create folder: `yyyy-mm-dd-procedure`
- Date = date of discussion
- Procedure = short descriptor of the surgery/procedure

### 2. Files (in order)

**a-case-summary-and-analysis.md**
Patient case, diagnoses, current condition. Concise but don't compromise understanding.

**b-anesthesia-concerns.md**
ALL anesthesia concerns relevant to managing the case safely.

**c-anesthesia-mx.md**
Anesthesia management plan, focusing on intraop. Practical and bedside-useful. Precise doses (mg/kg and actual doses for the patient), equipment sizes, specific numbers.

**d-emergencies.md**
Potential emergencies ordered from most important/likely to least. Include recognition, immediate management steps, and drug doses.

**e-preparation.md**
Detailed preparation guide: all meds (with doses), equipment (with sizes), checks, and communications needed before the case.

### 3. References
- Always search `anesthesia-refs-md` folder for knowledge first
- Cite exact file name and heading from resources used

### 4. Chat Summary
- Post a concise summary of all files in the chat after generating them

---

## B. When a question is asked:

### 1. Research
- Search `anesthesia-refs-md` folder for relevant information
- Every piece of information must have a precise citation: **exact file name + exact heading** from refs-md

### 2. Output File
- Save to: `Case Discussions/questions-answered/`
- File name: `yyyy-mm-dd-question-topic.md`
- Contents:
  - **Question** — formalized version of the question asked
  - **Answer** — with inline citations for every claim (file name + heading)
  - **References** — list of all sources used at the end

### 3. Chat Summary
- Also provide a concise answer in chat
