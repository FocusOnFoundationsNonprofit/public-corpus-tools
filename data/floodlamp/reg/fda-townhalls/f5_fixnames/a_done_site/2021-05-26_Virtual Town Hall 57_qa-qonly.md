## metadata
source file: data/floodlamp/reg/fda-townhalls/f5_fixnames/run_auto/2021-05-26_Virtual Town Hall 57_fixnames.md
last updated: 2025-01-03 Created QA Sections
link pdf: https://www.fda.gov/media/149660/download?attachment
link youtube: https://youtu.be/VTWoHUB1_R8
link slides: 
topic: COVID-19


## content

### removed qa blocks



### extract log
#### extract log header
datetime: 2025-01-03 17:27:08 UTC-08:00 America/Los_Angeles
source file prep: primary.llm.add_transcript_section_delimiters for non-FDA speakers
ROUND 1 NAME: Explicit Questions Extraction
- prompt: FCALL_SYSTEM_PROMPT_QA_QONLY_EXPLICIT_1D
- tools: tools_qa_qonly_explicit_1
- provider: openai
- model: gpt-4o-2024-11-20

#### Section 1 of 14
##### Explicit Questions Extraction
QE 1-1: Can an EUA respiratory multiplex kit for COVID, Influenza, and RSV be used as the comparator in a clinical study?
QE 1-2: How should multiple EUA tests be used if chosen as the comparator method?
QE 1-3: Can frozen retrospective samples be used for a 510k clinical validation study if they are retested on a comparative method?
QE 1-4: How should frozen prospective samples be collected to qualify for a clinical validation study?
QE 1-5: Can data from prospective clinical studies outside the US supplement data collected in the US for a 510k or de novo submission?
QE 1-6: What is appropriate for study enrichment when COVID positive cases are decreasing in the US?
QE 1-7: What are suitable enrichment methods to mitigate bias when conducting clinical studies for symptomatic positives?
QE 1-8: What are suitable enrichment methods to mitigate bias when conducting clinical studies for asymptomatic positives?
QE 1-9: Can patients who self-test with a candidate device know their previous test results, and if not, why?
QE 1-10: What precautions should be taken during clinical study enrichment to prevent bias in test results?

##### Implicit Questions Extraction
QI 1-1: What are the FDA's recommendations for using EUA tests as comparator methods for 510k clinical evaluations when 510k-cleared respiratory multiplex kits are unavailable?
QI 1-2: How should developers handle discrepancies between two EUA tests when using them as comparators in clinical studies?
QI 1-3: Is the BioFire assay the only acceptable predicate device currently for 510k submissions involving respiratory panel testing?
QI 1-4: To what extent can retrospective samples be used to supplement low specimen counts in prospective studies?
QI 1-5: How can developers address the use of highly concentrated archived samples that might not reflect actual patient populations?
QI 1-6: What guidelines exist for conducting prospective clinical studies outside the US to supplement US data for 510k or de novo submissions?
QI 1-7: What study designs does the FDA recommend to mitigate bias in prospective clinical studies including enrichment or selection processes?
QI 1-8: Under what conditions are banked samples acceptable for use in clinical validation studies?
QI 1-9: How should blinding of test results be managed to reduce bias during studies where self-testing and previous results are involved?
QI 1-10: What protocols for enrichment are recommended if prevalence is too low to obtain sufficient positive cases for clinical studies?

#### Section 2 of 14
##### Explicit Questions Extraction
QE 2-1: What should be done if a clinical study for a rapid antigen test has collected positive samples but none have CT values over 30, given the FDA's preference for 10 to 20% of positive samples being low positives with a CT over 30?
QE 2-2: Do usability and clinical studies for non-prescription over-the-counter rapid antigen tests need to include considerations for serial testing in their study protocol design?

##### Implicit Questions Extraction
QI 2-1: What enrichment strategies does the FDA recommend for obtaining low positive samples with a CT value over 30 for antigen tests?
QI 2-2: How does focusing on patients in the early days of symptoms impact CT values in clinical studies?
QI 2-3: What factors should be considered when choosing patients across the claimed window of sensitivity for antigen test studies?
QI 2-4: If prospectively collecting data on asymptomatic individuals is not required initially for serial testing claims, what are the post-authorization requirements to validate these claims?
QI 2-5: How should test developers demonstrate a PPA of 80% with a lower bound of 70% for symptomatic individuals to support serial testing indications?

#### Section 3 of 14
##### Explicit Questions Extraction
QE 3-1: For online advertisements of EUA-authorized materials, is it acceptable to omit required statements due to space limitations if a link to a webpage with the full list of statements is included in the advertisement?

##### Implicit Questions Extraction
QI 3-1: What should a test developer do if the mandatory statements from the EUA letter of authorization cannot fit within the space provided in an advertisement or promotional material?
QI 3-2: Does the FDA offer exceptions or alternative approaches for including statements when space constraints occur in advertising and promotional materials?
QI 3-3: How should test developers approach the FDA regarding challenges in following the promotional material requirements outlined in EUA letters of authorization?
QI 3-4: What constitutes 'important information' that must always be included in advertising and promotional materials for EUA-authorized tests?

#### Section 4 of 14
##### Explicit Questions Extraction
QE 4-1: What are the FDA's thoughts on the comparator method for a molecular SARS-CoV-2 RT PCR study with asymptomatic claims?
QE 4-2: Does the comparator assay for a molecular SARS-CoV-2 RT PCR study need to have asymptomatic claims?
QE 4-3: Does the comparator assay for a molecular SARS-CoV-2 RT PCR study need to be cleared?
QE 4-4: Is the BioFire RP-2.1 assay an acceptable comparator for a molecular SARS-CoV-2 RT PCR study?
QE 4-5: For the clinical evaluation of a point-of-care or over-the-counter antigen test for an EUA, can some or all of the study be completed outside of the US due to declining positive cases in the US?
QE 4-6: For an antibody test, is a prospective study required for de novo or 510k submissions, or can a retrospective study include some samples from outside the US?
QE 4-7: For an antigen test with de novo or 510k submission claiming use with nasal swabs, can the comparator method be a high-sensitivity RT PCR with nasal swabs, or does it need to be a nasopharyngeal (NP) swab?

##### Implicit Questions Extraction
QI 4-1: What is the recommended comparator method for molecular SARS-CoV-2 tests if no cleared tests exist for asymptomatic claims?
QI 4-2: Should a pre-submission be submitted to discuss the comparator method before starting a 510k study?
QI 4-3: If conducting studies outside the US for a point-of-care antigen test, what criteria must the population meet to be representative of the US?
QI 4-4: Can clinical studies from outside the US supplement, but not replace, US-based prospective data for de novo or 510k submissions?
QI 4-5: What documentation is needed to demonstrate that clinical studies conducted outside the US are relevant to US clinical practice and demographics?
QI 4-6: Can mid-turbinate swabs be used as the comparator for a de novo or 510k submission instead of nasopharyngeal (NP) swabs?
QI 4-7: For saliva sample testing, in what cases would a mid-turbinate swab be an acceptable comparator?

#### Section 5 of 14
##### Explicit Questions Extraction
QE 5-1: What issues were uncovered with saliva as a challenging sample type for antigen tests?
QE 5-2: Does the freeze-thaw process increase sensitivity for antigen tests detecting the N protein, the S protein, or both?

##### Implicit Questions Extraction
QI 5-1: What are the validation challenges specific to using saliva for molecular tests?
QI 5-2: How does variability in saliva sample data impact FDA authorization decisions?
QI 5-3: What steps should be taken to validate performance when using saliva as a specimen type for diagnostics?
QI 5-4: What are FDA recommendations for handling variability in freeze-thaw effects on saliva samples?
QI 5-5: How should frozen saliva sample testing be designed to demonstrate unbiased results for EUA authorization?

#### Section 6 of 14
##### Explicit Questions Extraction
QE 6-1: Is it a requirement to include validation data for an optional app as part of the initial EUA submission for a point of care molecular diagnostic test system?
QE 6-2: Can the use of an optional app for a point of care molecular diagnostic test system be filed separately from the initial EUA submission?
QE 6-3: Is it necessary to provide validation data for an optional app associated with a point of care molecular diagnostic test system?
QE 6-4: When does the FDA anticipate having a recommended reference material available for antigen tests?

##### Implicit Questions Extraction
QI 6-1: What factors determine whether validation data for an optional app need to be submitted with a point of care molecular diagnostic test system?
QI 6-2: How should developers approach the FDA for discussions about the role of an app in the context of a diagnostic test system?
QI 6-3: What is the process for submitting a pre-EUA for a point of care molecular diagnostic test system with an associated app?
QI 6-4: What are the current challenges in developing reference materials for antigen tests?
QI 6-5: Is the FDA working on or planning to develop reference materials for antigen tests in the future?

#### Section 7 of 14
##### Explicit Questions Extraction
QE 7-1: Is there any expectation that manufacturers of OTC antigen tests include new recent strains of the virus in inclusivity testing?
QE 7-2: Can manufacturers rely on very common strains sourced from Europe for inclusivity testing?
QE 7-3: What are the latest FDA expectations on the quantity of strains and which strains should be used for inclusivity testing?

##### Implicit Questions Extraction
QI 7-1: What methods does the FDA recommend for obtaining relevant protein molecules with variants for testing?
QI 7-2: What specific steps should developers take if their test potentially detects false negatives from variants or mutations above the 5% threshold?
QI 7-3: When and how should developers engage with the FDA to address potential issues with assay performance caused by variants or mutations?
QI 7-4: What are the FDA's expectations regarding developers' plans for ongoing risk assessment of false negatives due to variants and mutations as part of the EUA process?
QI 7-5: What does the FDA require from developers for post-market monitoring of the effects of variants and mutations on test performance?
QI 7-6: How should developers use the recommendations in the EUA templates to ensure compliance with inclusivity testing?

#### Section 8 of 14
##### Explicit Questions Extraction
QE 8-1: Does obtaining over-the-counter designation for an antigen test kit with a mid-turbinate swab require the inclusion of a child safety stopper to prevent over-insertion?
QE 8-2: Is the purpose of the stopper to prevent gross over-insertion, such as being located four centimeters from the tip?
QE 8-3: Does the stopper need to prevent insertion past a specific zone for a two-year-old, such as about 1.5 centimeters or a half inch?
QE 8-4: What is the purpose of the stopper for a mid-turbinate swab in an antigen test kit, and is it required?

##### Implicit Questions Extraction
QI 8-1: What does the FDA consider to be the gray zone between an interior nares swab and a true mid-turbinate swab?
QI 8-2: What steps should test developers take to ensure safety considerations are adequately addressed prior to usability and clinical studies for devices requiring mid-turbinate swabs?
QI 8-3: Does the FDA recommend engaging with them early concerning swab safety issues before conducting usability studies?

#### Section 9 of 14
##### Explicit Questions Extraction
QE 9-1: What is the expectation for fully quantitative serology tests?
QE 9-2: What is the expectation for a fully quantitative neutralizing test?
QE 9-3: Are the validation requirements for fully quantitative tests the same as those listed for semi-quantitative tests?
QE 9-4: Is establishing traceability of the results to the WHO standard required for fully quantitative tests?

##### Implicit Questions Extraction
QI 9-1: What does the FDA consider essential components of a validation study plan for a fully quantitative serology test?
QI 9-2: What additional factors, such as linearity or traceability to international standards, need to be included in the development of fully quantitative tests?
QI 9-3: Where can developers access detailed information about the previously authorized truly quantitative test?
QI 9-4: What should be included in a pre-EUA submission to receive feedback specific to a fully quantitative test?
QI 9-5: How can developers ensure timely responses when submitting questions to the FDA mailbox?
QI 9-6: What steps should be taken if a response from the FDA mailbox is delayed?

#### Section 10 of 14
##### Explicit Questions Extraction
QE 10-1: Is the NCI still conducting validations, or is the independent validation process still in effect?
QE 10-2: Has the backlog of submissions at NCI been cleared, and have the reports been issued?
QE 10-3: Are validations being conducted at a different lab other than NCI?

##### Implicit Questions Extraction

#### Section 11 of 14
##### Explicit Questions Extraction
QE 11-1: Can you include vaccinated individuals in an antigen clinical evaluation study?
QE 11-2: Can the data for vaccinated and unvaccinated individuals be analyzed separately, without necessarily doubling the sample size?

##### Implicit Questions Extraction
QI 11-1: How might lower viral loads in vaccinated individuals affect antigen test performance?
QI 11-2: Is there any existing research or data on antigen test performance in vaccinated individuals?
QI 11-3: Should vaccinated individuals' antigen test data be analyzed separately from unvaccinated individuals in the Instructions for Use (IFU)?
QI 11-4: Does the FDA require specific reporting formats for antigen test performance in vaccinated populations?
QI 11-5: Does symptomatic follow-up infection in vaccinated individuals differ significantly from primary or natural infection in terms of testing impact?

#### Section 12 of 14
##### Explicit Questions Extraction
QE 12-1: Are there any other institutions besides NCI that might perform vaccine antibody testing?
QE 12-2: Do you have any plans for establishing a center to verify and validate tests for neutralizing and protective antibodies?
QE 12-3: Is vaccination considered a diagnostic test requiring approval the way it is done?
QE 12-4: Can you confirm that NCI had a discussion with CBER regarding vaccines and diagnostics?
QE 12-5: Is vaccine testing still a responsibility of the CBER team at FDA?

##### Implicit Questions Extraction
QI 12-1: What are the FDA's recommendations for using serology tests to evaluate immunity or protection in vaccinated individuals?
QI 12-2: Will the FDA design a blinded panel for evaluating quantitative assays for neutralizing and non-neutralizing antibodies?
QI 12-3: Is there a timeline or conditions under which the FDA might establish a program for assessing quantitative antibody assays?
QI 12-4: What non-quantitative serology assay approaches might still be considered for future FDA review?
QI 12-5: Which types of COVID-19 serology assays are reviewed by the CBER team versus other FDA teams?

#### Section 13 of 14
##### Explicit Questions Extraction
QE 13-1: How is the review flow of pre-EUAs progressing?
QE 13-2: Is the FDA still heavily backed up, or will they address the pre-EUA submission soon?

##### Implicit Questions Extraction
QI 13-1: What is the process for ensuring that a submitted pre-EUA is reviewed and not overlooked?
QI 13-2: Should a reader submission always include a candidate test for evaluation?
QI 13-3: Why is it necessary to validate readers across multiple devices and software versions?
QI 13-4: What are the specific validation requirements for Smartphone-based reader applications?
QI 13-5: If a reader demonstrates variable performance across different models, how should developers address this issue to meet FDA standards?
QI 13-6: Is there an alternative process for evaluating readers not tied to a candidate test?
QI 13-7: Will the FDA continue to provide forums for developers to ask questions about IVD development after the COVID-19 pandemic?

#### Section 14 of 14
##### Explicit Questions Extraction
QE 14-1: Do you foresee a series of new tests or other ones in the pipeline that would be vaccine-specific, i.e., detecting specific antibodies to the Pfizer, Moderna, or Johnson vaccines?
QE 14-2: Would vaccine-specific tests need to be labeled to be matched with their vaccines?

##### Implicit Questions Extraction
QI 14-1: What clinical study data does the FDA prioritize for demonstrating immunity and protection from vaccines or natural infections?
QI 14-2: What are the recommended procedures for linking study assays to the International WHO standard?
QI 14-3: Could developers update their tests to use standardized antibody levels without conducting new outcome studies?
QI 14-4: Would the FDA consider using a bank of immune plasma serum for test validation or post-market authorization?
QI 14-5: Are there plans to standardize antibody cut points that can be universally applied across different tests and vaccines?
QI 14-6: What steps should developers take to ensure their serology tests produce accurate and useful results that align with FDA expectations?

### qa


#### 1. Guidance on Validation and Study Design for SARS-CoV-2 Tests

QA Block 1-1
CLARIFIED QUESTION: Can an EUA respiratory multiplex kit for COVID, Influenza, and RSV be used as the comparator in a clinical study?
CLARIFIED ANSWER: An EUA respiratory multiplex kit can be used as a comparator in a clinical study, though FDA recommends using a 510k-cleared comparator if possible. If using EUA tests, FDA suggests employing multiple EUA tests in an algorithm (e.g., using two tests and a third as a tiebreaker in case of disagreement). Submitting a presubmission to discuss the proposed comparator method is also recommended.
VERBATIM QUESTION: Can an EUA respiratory multiplex kit for COVID, Influenza, and RSV be used as the comparator in a clinical study?
VERBATIM ANSWER: Generally we do recommend that the respiratory multiplex comparator methods are 510k cleared. But we do know that that's, that maybe challenging at the moment, so you could also consider using an EUA-authorized, highly sensitive RT PCR assay as your comparator method for your clinical evaluation. But we do note that the EUA tests are validated with a different level of evidence than a 510k tests, a cleared test. So, we would probably recommend that you use multiple EUA tests in an algorithm to determine positive and negative comparator test results. For example, you could use two EUA tests per sample of the comparator and if there's disagreement between those, use a third tiebreaker test. And as we've mentioned here on this call before, we do recommend that if you're pursing 510k pathway, that you submit a presubmission to discuss your proposed comparator method.
SPEAKER QUESTION: NOT APPLICABLE
SPEAKER ANSWER: Toby Lowe (FDA IVD Assoc Director)
TOPICS: EUA respiratory multiplex kit usage, 510k pathway, Clinical study comparators
REVIEW FLAG: False

QA Block 1-2
CLARIFIED QUESTION: How should multiple EUA tests be used if chosen as the comparator method?
CLARIFIED ANSWER: The FDA recommends using multiple EUA tests in an algorithm to determine positive and negative comparator test results. For instance, two EUA tests can be used per sample, with a third tiebreaker test if there's disagreement between the results.
VERBATIM QUESTION: How should multiple EUA tests be used if chosen as the comparator method?
VERBATIM ANSWER: But we do note that the EUA tests are validated with a different level of evidence than a 510k tests, a cleared test. So, we would probably recommend that you use multiple EUA tests in an algorithm to determine positive and negative comparator test results. For example, you could use two EUA tests per sample of the comparator and if there's disagreement between those, use a third tiebreaker test.
SPEAKER QUESTION: NOT APPLICABLE
SPEAKER ANSWER: Toby Lowe (FDA IVD Assoc Director)
TOPICS: EUA tests, Comparator methods, COVID-19 diagnostics
REVIEW FLAG: False

QA Block 1-3
CLARIFIED QUESTION: Can frozen retrospective samples be used for a 510k clinical validation study if they are retested on a comparative method?
CLARIFIED ANSWER: Frozen retrospective samples are not recommended for primary use in 510k clinical validation studies due to potential bias, but they may supplement a study if prospective samples are insufficient. Prospective studies should primarily occur in the US, with non-US data used as a supplement if needed.
VERBATIM QUESTION: Can frozen retrospective samples be used for a 510k clinical validation study if they are retested on a comparative method?
VERBATIM ANSWER: Generally we do recommend that clinical studies include prospectively fresh and frozen samples to preserve analyte prevalence. Retrospective samples are considered to be selected and archived samples that are previously frozen usually based on a previous positive result. So, since that approach is more than minimally biased since the prevalence is generally not preserved, that's not, not our recommended method. Typically, the, or often the archived samples are also very high concentration so they would not be near the LOD of the assay and may not be reflective of the actual patient population. So, we do agree that sponsors can supplement with retrospective samples but usually only after conducting a prospective study which yielded too few samples to demonstrate adequate performance. In terms of US versus outside the US, we recommend that sponsors conduct their prospective clinical studies primarily in the US to support a 510k or de novo. Data from outside the US prospective clinical studies can also be submitted to supplement the US data, especially in cases where there's difficulty getting enough specimens in the US due to low prevalence with a heavily vaccinated population.
SPEAKER QUESTION: NOT APPLICABLE
SPEAKER ANSWER: Toby Lowe (FDA IVD Assoc Director)
TOPICS: Frozen retrospective samples, Clinical validation, 510k requirements
REVIEW FLAG: False

QA Block 1-4
CLARIFIED QUESTION: How should frozen prospective samples be collected to qualify for a clinical validation study?
CLARIFIED ANSWER: The FDA recommends including prospectively fresh and frozen samples to preserve analyte prevalence. Retrospective samples should only be used to supplement prospective ones if necessary and are not preferred due to bias. Prospective samples should mainly be collected within the US, although data from outside the US can supplement if specimen collection is challenging.
VERBATIM QUESTION: How should frozen prospective samples be collected to qualify for a clinical validation study?
VERBATIM ANSWER: So, generally we do recommend that clinical studies include prospectively fresh and frozen samples to preserve analyte prevalence. Retrospective samples are considered to be selected and archived samples that are previously frozen usually based on a previous positive result. So, since that approach is more than minimally biased since the prevalence is generally not preserved, that's not, not our recommended method. Typically, the, or often the archived samples are also very high concentration so they would not be near the LOD of the assay and may not be reflective of the actual patient population. So, we do agree that sponsors can supplement with retrospective samples but usually only after conducting a prospective study which yielded too few samples to demonstrate adequate performance. In terms of US versus outside the US, we recommend that sponsors conduct their prospective clinical studies primarily in the US to support a 510k or de novo. Data from outside the US prospective clinical studies can also be submitted to supplement the US data, especially in cases where there's difficulty getting enough specimens in the US due to low prevalence with a heavily vaccinated population.
SPEAKER QUESTION: NOT APPLICABLE
SPEAKER ANSWER: Toby Lowe (FDA IVD Assoc Director)
TOPICS: frozen prospective samples, clinical validation studies, sample collection guidelines
REVIEW FLAG: False

QA Block 1-5
CLARIFIED QUESTION: Can data from prospective clinical studies outside the US supplement data collected in the US for a 510k or de novo submission?
CLARIFIED ANSWER: The FDA recommends conducting prospective clinical studies primarily in the US for 510k or de novo submissions. However, data from outside the US can supplement US data, particularly when there are challenges in obtaining enough specimens in the US due to low prevalence or high vaccination rates.
VERBATIM QUESTION: Can data from prospective clinical studies outside the US supplement data collected in the US for a 510k or de novo submission?
VERBATIM ANSWER: In terms of US versus outside the US, we recommend that sponsors conduct their prospective clinical studies primarily in the US to support a 510k or de novo. Data from outside the US prospective clinical studies can also be submitted to supplement the US data, especially in cases where there's difficulty getting enough specimens in the US due to low prevalence with a heavily vaccinated population.
SPEAKER QUESTION: NOT APPLICABLE
SPEAKER ANSWER: Toby Lowe (FDA IVD Assoc Director)
TOPICS: US and non-US data for 510k, de novo submissions, specimen collection challenges
REVIEW FLAG: False
