## metadata
source file: data/floodlamp/reg/fda-townhalls/dev-qa-extract/VTH 36 just2_trans.md
last updated: 2024-12-30 Created QA Sections
link pdf: https://www.fda.gov/media/144566/download?attachment
link youtube: https://youtu.be/VNrwrH0N0dY
link slides: 
topic: COVID-19
notes: delete and combine unimportant segments


## content


### extract log
#### extract log header
datetime: 2024-12-30 13:29:33 UTC-08:00 America/Los_Angeles
source file prep: primary.llm.add_transcript_section_delimiters for non-FDA speakers
ROUND 1 NAME: Explicit Questions Extraction
- prompt: FCALL_SYSTEM_PROMPT_QA_QONLY_EXPLICIT_1D
- tools: tools_qa_qonly_explicit_1
- provider: openai
- model: gpt-4o-2024-11-20

#### Section 1 of 2
##### Explicit Questions Extraction

##### Implicit Questions Extraction
QI 1-1: What are the specific caveats related to the FDA's authorizations for pooling in asymptomatic screening?
QI 1-2: If a pooling scheme is not authorized for asymptomatic screening, what guidelines should developers follow for off-label use?
QI 1-3: What are the requirements for obtaining authorization for a home collection kit that detects both SARS-CoV-2 and flu?
QI 1-4: What specific conditions need to be met for panel testing to be supported by the FDA?
QI 1-5: What are the FDA's highest priorities for developers in terms of point-of-care tests, home collection kits, panels, and high-throughput systems?
QI 1-6: What are the limitations on using authorized tests for only symptomatic patients?
QI 1-7: How does the FDA define its recommendations for asymptomatic screenings using pooling methods?

#### Section 2 of 2
##### Explicit Questions Extraction
QE 2-1: What is the process for establishing a primer set for LAMP and consolidating a general letter of reference for multiple test developers?
QE 2-2: What requirements are involved in the inclusivity in silico analysis, in silico cross-reactivity, and wet cross-reactivity for LAMP tests?
QE 2-3: If we get authorization for a test with a specific license or activation buffer and another test developer uses a different purification but the same primer set and LAMP master mix, do they need to repeat the interfering substances study?
QE 2-4: If a test developer is granted a general right of reference to our authorized test, will they need to get their own EUA to control designations?
QE 2-5: Does granting a right of reference allow test developers to independently control EUA designations while referencing another developer’s core test data?

##### Implicit Questions Extraction
QI 2-1: What are the specific conditions or scenarios under which a test developer would need to perform additional validations if using the same primer set and LAMP master mix?
QI 2-2: What data or criteria would the FDA evaluate if a test developer introduces changes to components like activation buffers or purifications?
QI 2-3: How does the FDA define the scope of 'synergy' in validation requirements when multiple developers cross-reference each other's assays?
QI 2-4: What commitments are required from a test developer to the FDA when designating labs under their EUA authorization?
QI 2-5: How does a test developer determine the extent to which they can limit or open the rights provided under a right of reference for their EUA submission?
