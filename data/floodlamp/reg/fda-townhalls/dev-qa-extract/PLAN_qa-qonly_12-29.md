## Project Summary - Third Attempt at Multi-Step Q&A Extraction Pipeline

### Overview
We need to implement a three-round approach to extracting questions from FDA Town Hall transcripts:
1. Extract explicit questions only (Round 1).
2. Extract implicit questions only (Round 2), using the final explicit question set as context.
3. Perform a final coverage check (Round 3) to identify any missed questions.

### Current Functionality
- Code to apply section delimiters based on new non-FDA speakers
- Existing scripts process transcripts section-by-section, outputting full QA blocks.
- We have prompts for extracting and clarifying questions, and for generating QA blocks.
- Code creates QA files with extraction log heading
- Code to create embeddings, calculate similarities, and visualize similarities
- We’ve run two prior extraction attempts; each used multi-prompt calls but encountered redundancy issues.
- Excessive manual review time to remove near-duplicate questions.
- Need to reliably deduplicate through embedding similarity checks.

### Goals
- complete code updates and testing in a few hours including:
    - prompt optimization
    - embedding-based deduplication
    - manual review setup
    - final QA block extraction prompt updated
- manual review process takes 2-3 minutes per transcript

### Desired Improvements
- Automate as much of the deduplication as possible.
- Introduce separate explicit-question and implicit-question extraction rounds.
- Use minimal manual review time (2–3 minutes per transcript).

### Technical Details
- Code resides mostly in a single file primary/llm.py; we have test transcripts and supporting utilities (embedding functions, similarity checking).
- Each transcript is divided into smaller sections. For each round, we run the same transcript data but with different prompts and rules.
- We rely on a similarity threshold to prune near-duplicates; a final threshold-based filter flags borderline cases for quick review.

### Options and Considerations
- We can further refine thresholds or prompt instructions if we see over- or under-aggregation of questions.
- Three calls per transcript section (explicit → implicit → coverage) is acceptable for budget/time constraints.

### Conclusion
This approach should produce a faithful set of clarified questions, enabling a final QA extraction step for each transcript. With all code changes tested and stable, the final extraction can run overnight or within one day of effort.

### Next Steps
- Implement or update the code for three extraction rounds.
- Integrate embedding-based deduplication after each round.
- Perform a coverage check (Round 3) for any remaining/missing questions.
- Conduct a quick manual pass to finalize each transcript’s question list.
- Generate the final QA blocks automatically once question lists are locked in.

## Deliverables Punch List
[x] Implement Round 1 explicit question extraction logic.
[x] Create Round 2 implicit prompts and tools
[x] Update get_questions_from_qa_file to work with ### extract log in addition to qa blocks
[x] Figure out structure for implementing round-by-round processing
[x] Implement Round 2 implicit question extraction with new structure
[x] Use Q similarity code to manually review Q similarity on VTH36, 30, and 20
[SKIP] Implement similarity based removal of duplicate Q, keeping longer one
[SKIP] Implement LLM call to decide on question pairs in similarity score middle zone
[SKIP] Implement optional manual review instead of LLM call and to review LLM call results
[x] Create prompts and tools for full QA block extraction from finalized question list
[x] Implement full QA block extraction function
[x] Run on 36, 30, and 20
[ ] Revisit similarity code for deduplication dev - made Loom!
    [ ] Determine threshold to remove duplicates
    [ ] Implement in code
    [ ] Log what was deleted and sim score info
[SKIP] Compare to previous results with previous approach sections full blocks

[x] Gen Q removal list with Q section-num
[x] do __X formatting__
[x] put print statements in string to write to qa-qonly file

[x] Function to compare two question lists
[x] move removed QA blocks to new '### removed qa blocks' section
[SKIP] Add section number to delimiter @ beginning of each section
[x] Function to rerun QA block fcall with section and question as input
[x] 36 finalized
[x] 30 and 20 finalized
[x] create auto_process_qa_qonly for all 3 rounds plus
    - include moving files to new folders
[x] add_section_delimiters for 0 and 00 and 1 to 10
[ ] run auto_process_qa_qonly on 1-10 (skip 0 and 00 for now)
    - move to another folder to run

[ ] move qa-only related files to new folders



- [x] I need to update the quest to get questions all coded to read from the QA blocks. I want to run both from the QA blocks and from the extract log, then do a comparison to see if any of the clarified questions have changed. I want to include that as a potential third report section. I don't want to expand to do more, but it would be helpful to know. While I'm doing this, I will do the deduplication on the QA block version. I don't need to worry if they've changed, but I want that analysis there so I can look at it.
- [ ] I will do a review of the code today, focusing on the process and what I did for the entire QA. This is for my internal use, so I can remember it and capture some of this information before it leaves my mind. I will go through the whole file before I clean it up and then save an archived version, as I will need to pull that out and update the public repository.


## OLD Punch List
2. [ ] Implement Round 2 implicit question extraction logic with explicit Qs as context.
3. [ ] Implement Round 3 final coverage check logic.
4. [ ] Update and integrate similarity-based deduplication and culling steps.
5. [ ] Conduct test runs on a small sample (3–5 transcripts) to confirm correctness.
6. [ ] Execute the pipeline on the entire corpus and perform minimal manual review.
7. [ ] Finalize QA block extraction once question sets are complete.

## Deliverables Tasks and Details

### 1. [ ] Implement Round 1 Explicit Question Extraction Logic
#### [x] Task: Update Prompt for Explicit Extraction
[x] Create or update the system/user prompt to target only explicitly asked questions (e.g., question marks, “I’d like to ask…”).
    - Do not do speaker identification
    - Clarify that no implied or “assumed” questions should be included here.
[x] Update 2 functions to call this Round 1 prompt per section.
    - Ensure newly added or updated function processes each transcript section individually.

#### [SKIP] Task: Integrate Post-Round Deduplication
[ ] Use the existing embedding model to compare newly extracted Round 1 questions.
    - Apply a high-similarity threshold to remove near-duplicate explicit questions.
    - Generate a final list of “explicit questions” per section.
[ ] Output or store these deduplicated explicit questions for subsequent rounds.
    - Confirm they are saved in a stable format or data structure.

### 2. [ ] Implement Round 2 Implicit Question Extraction Logic
#### [ ] Task: Prompt for Implicit Extraction
[ ] Subtask 1.1
    [ ] Write or refine a prompt to “over-extract” any potential implied questions.
    - Exclude all obvious explicit forms that Round 1 already covered.
    - Clarify that speaker roles can be “IMPLIED” if the question arises from an FDA statement, etc.
[ ] Subtask 1.2
    [ ] Pass in the final Round 1 question list as context, so Round 2 doesn’t repeat them.
    - Use the explicit question set to instruct the model: “Do not re-include these.”

#### [ ] Task: Integrate Post-Round 2 Deduplication
[ ] Subtask 2.1
    [ ] Use the same embedding-based method to prune near-duplicates among implicit questions.
[ ] Subtask 2.2
    [ ] Merge the Round 1 explicit questions with the Round 2 implicit questions into a single combined question list for each transcript section.
    - Mark each question as “explicit” or “implicit” for reference.

### 3. [ ] Implement Round 3 Final Coverage Check Logic
#### [ ] Task: Final Coverage Prompt
[ ] Subtask 1.1
    [ ] Write a “final coverage check” prompt that references the combined question list (explicit + implicit).
    - Instruct the model: “Are we missing any questions on important topics in this section?”
[ ] Subtask 1.2
    [ ] If new questions are found, have the model specify if they’re explicit or implicit and deduplicate them similarly.

#### [ ] Task: Summarize or Store Final Question List
[ ] Subtask 2.1
    [ ] Produce a consolidated final question list per transcript section.
    [ ] Label each question with speaker name or “IMPLIED” if appropriate.
[ ] Subtask 2.2
    [ ] Save or display the final list in a stable JSON or CSV structure for quick manual review.

### 4. [ ] Update and Integrate Similarity-Based Deduplication and Culling Steps
#### [ ] Task: Threshold Tuning
[ ] Subtask 1.1
    [ ] Adjust the similarity threshold for auto-removal of duplicates.
    - Decide whether to keep borderline duplicates for manual review or auto-merge.
[ ] Subtask 1.2
    [ ] Provide a “middle zone” manual review option if time permits.

#### [ ] Task: Implementation Check
[ ] Subtask 2.1
    [ ] Confirm that each round’s deduplication script or function is invoked at the correct time.
    - Round 1 dedup, Round 2 dedup, Round 3 dedup if new Qs appear.

### 5. [ ] Conduct Test Runs on a Small Sample of Transcripts
#### [ ] Task: Dry Run with 3–5 Files
[ ] Subtask 1.1
    [ ] Execute Round 1 → Round 2 → Round 3 pipeline on 3–5 transcripts.
    - Evaluate output question sets.
[ ] Subtask 1.2
    [ ] Check performance, look for missed or duplicated questions.

#### [ ] Task: Adjust if Needed
[ ] Subtask 2.1
    [ ] Refine thresholds or prompt instructions if we see oversights or repeated questions.
[ ] Subtask 2.2
    [ ] Re-run test to confirm improvements.

### 6. [ ] Execute the Pipeline on Entire Corpus with Minimal Manual Review
[ ] Task: Run Full Extraction
    - Initiate the pipeline for all ~100 transcripts.
    - Let the code run overnight if needed.
[ ] Task: Brief Manual Screening
    - Spend 2–3 minutes reviewing questionable items flagged by the deduplication step.
    - Resolve borderline duplicates or combine them if needed.

### 7. [ ] Finalize QA Block Extraction
[ ] Task: Execute Final QA Generation
    - Use the final question set per transcript section to call your existing QA extraction function (verbatim question, verbatim answer, etc.).
    - Ensure speaker info aligns correctly.
[ ] Task: Validate and Store QA Blocks
    - Confirm that QA blocks map accurately to transcript text.
    - Output everything to the final data files (JSON, CSV, or your chosen format).
