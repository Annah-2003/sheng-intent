# Human computer interaction rationale

## The interaction problem

Rada's present interface is an assessment demonstration for judges and the team. The handbook requires new-text prediction, a labelled simulated response, results and genuine failures; it does not require a finished assistant service or a formal end-user usability study. The language-access motivation below describes a longer-term direction, not a claim that the current prototype is ready for public everyday use. The interface matches the recorded demonstration.

The team wants useful digital assistance to be approachable without requiring users to learn a fixed English command. Language can be part of the interaction cost: a person may know the task they want completed while the interface expects unfamiliar phrasing. This is the team's design motivation, not a measured finding that all respondents lack access to AI or digital skills.

The first design question is deliberately narrow: can naturally written Kiswahili/Sheng requests be mapped to everyday assistant actions? Rada handles intent recognition only. It does not demonstrate improved employment, talent discovery, technology adoption, time savings or production task completion.

## What we gathered and what it supports

We asked people to express assistant requests in familiar situations involving music, weather, alarms, calendars, lists, news and word meanings. This elicited written language variation for tasks; it was not a formal needs interview or observation of spontaneous assistant use. Participants' wording and the review decisions informed the classification task and exposed ambiguous boundaries.

Code-switching and informal spelling were retained instead of imposing standardised phrases. Some fragments depended on the scenario, and some reviewed labels remain debatable. The collection therefore supports exploring wording diversity and classification errors; it cannot establish community-wide access barriers or satisfaction.

## Design decisions and reasons

| Decision | Interaction reason | Evidence or limitation |
| --- | --- | --- |
| Free-text request instead of a prescribed command | Lets people try their own wording | Scenario collection contains variation; usefulness is not yet user-tested |
| Plain action names | Makes a category understandable without reading code labels | Design rationale; no measured comprehension study |
| One clear prediction followed by a simulated response | Connects recognition to a possible next step without pretending to act | Actual saved classifier; no external action integration |
| Scores in an optional expander | Keeps the first view simple while allowing inspection | Scores are uncalibrated and can be confidently wrong |
| Results and failures visible in the same app | Helps people form realistic expectations | Fixed test, actual errors and small-sample limits are disclosed |
| No response logging or automatic dataset additions | Avoids treating casual demo use as consented new research data | Current code does not persist user entries; hosting logs are outside this claim |

## Evaluation still needed

The rationale also draws on Jakob Nielsen's usability heuristics: familiar action names support a match to users' everyday concepts; visible predictions and simulation labels communicate system status; the on-screen scope reduces the need to remember supported commands; optional score details keep the main task focused. These are design interpretations, not a completed expert heuristic evaluation or evidence of user satisfaction. Reference: [Nielsen Norman Group, 10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/), consulted 12 November 2026.

The completed model test evaluates agreement with reviewed labels, not interface usability. A future user study should ask consenting participants to try representative tasks, explain the output in their own words and identify confusing feedback. Measure completion, misunderstanding, recovery and perceived ease separately from model accuracy. Keep any new study outside the frozen 56-example test and report it as additional evidence.

The recorded demo and teammate checks do not establish accessibility across disabilities, devices or Nairobi communities. Keyboard operation, screen-reader labels, mobile layout and language comprehension remain appropriate checks; do not claim they passed without recorded evidence.

## What is distinctive and what is reused

The value is the combination of original scenario-elicited Sheng/Kiswahili requests, traceable human decisions, a bounded external-data comparison and an assessment interface that makes failures visible. The baseline algorithm and taxonomy are reused from the organiser kit; MASSIVE is upstream data. We do not claim novelty over other teams or that the chosen language alone earns higher marks.
