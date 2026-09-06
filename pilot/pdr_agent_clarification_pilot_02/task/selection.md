# Frozen task-user selection

## Selected identifiers

- `query_id`: 1
- `task_id`: 1
- `persona_id`: User1

## Why this pair is high-personalization-sensitivity

Task 1 requires choosing AI research directions, regions, universities and labs, funding routes, application requirements, background-building activities, and a 1–2-year execution plan. These decisions should change materially for users with different academic preparation, subfield interests, financial constraints, career goals, geography, and work habits.

User1 provides multiple task-relevant facts: a high-performing Chinese computer-science undergraduate; declared interest in deep learning, natural language processing, and algorithms; scholarship- and family-supported finances with a frugal, cost-conscious style; a stability-oriented family context; evening productivity and strict planning habits; and intensive use of GitHub, technical blogs, Coursera, and Bilibili learning resources.

The unmodified PDR criteria explicitly score direction discovery, DL/NLP program and lab matching, a Chinese-applicant regional comparison, a dated 1–2-year roadmap, background strengthening using GPA/scholarships/GitHub, cost-conscious funding strategy, stability-aware employment planning, and presentation aligned with an analytical working style.

## Leakage boundary

Selection and the critical-preference registry were frozen before either product agent produced a question or report. The agents receive only the original task plus the common clarification-permission sentence and isolation wrapper. They do not receive this rationale, the persona, the criteria, or the registry.
