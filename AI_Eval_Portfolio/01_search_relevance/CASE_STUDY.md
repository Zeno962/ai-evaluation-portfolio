# Case study · Search relevance under incomplete evidence

## Problem

Keyword overlap hides failures of task, location, timing and intent. The evaluation needs to distinguish useful partial matches from superficially related results while preserving uncertainty about unseen pages.

## Design and evidence

Eight fictional queries each have four results: device instructions, a university portal, local inventory, opening hours, an ambiguous term, CSV handling, venue access and repair instructions. The 32 judgments use an explicit 0–3 scale, written intent, confidence and review flags. All four grades are intentionally represented within each group.

## Decisions that matter

**Same-day pickup (S03-2 vs S03-3).** Abuja inventory with an unknown pickup date is useful but incomplete (2). A Lagos-only listing contradicts the location requirement (1), even though its price is attractive.

**Ambiguous referent (S05-2).** A vehicle-performance result earns 2 for a plausible secondary interpretation of “jaguar speed.” It becomes 3 if the user confirms car intent. Its original grade remains tied to the animal-first interpretation.

**Verification versus relevance (S07-1).** The venue snippet explicitly states quiet seating and step-free access, so metadata relevance is 3. The access claim still needs verification; a grade is not a venue safety certification.

## Findings and limits

[Analysis](ANALYSIS.md) reports grade coverage and ranking calculations. Baseline ranks are authored to illustrate displacement of useful results; they are not observed retrieval outputs. Their metrics cannot establish search-engine quality. No pages were opened and no second rater or production traffic was sampled.

The practical outcome is a reviewable decision boundary: unknown constraints, violated constraints and secondary interpretations receive different treatment, with the evidence needed to resolve uncertainty recorded explicitly.
