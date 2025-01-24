METADATA
last updated: 12-27-24 by BA fixed
primary file: Resulting Decision (Single Triplicate Re-run) Flow Chart v1.2_PUB.pdf
conversion: claude
notes:


CONTENT

Resulting decision chart (single triplicate re-run) Flow Chart v1.2

```mermaid
flowchart LR
    Start[Initial Test] --> Neg{Negative}
    Start --> Inc{Inconclusive}
    Start --> Pos{Positive}
    Neg --> NegResult[Negative]
    
    Inc --> ReRun1[Re-run
    triplicate]
    ReRun1 --> Pos2{2+ Positives} --> PosResult[Positive]
    ReRun1 --> Neg3{3
    Negatives} --> NegResult
    ReRun1 --> Other1{Other} --> IncResult[Inconclusive]

    Pos --> ReRun2[Re-run
    triplicate]
    ReRun2 --> Neg4{3
    Negatives} --> NegResult
    ReRun2 --> PosOrOne{2+Positives or
    1/1/1} --> PosResult[Positive]
    ReRun2 --> Other2{Other} --> IncResult[Inconclusive]
    
```