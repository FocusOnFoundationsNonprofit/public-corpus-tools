## metadata
last updated: 08-06-2024 Created
link: https://youtu.be/bOnBPGkxUuw
transcript source: deepgram 2-general-nova


## content

### transcript

Speaker 0  [0:00](https://youtu.be/bOnBPGkxUuw&t=0)
If you could talk about hallucinations from your perspectives. The why hallucinations happen from large language models and why and to what degree is that a fundamental flaw of large language models.

Speaker 1  [0:15](https://youtu.be/bOnBPGkxUuw&t=15)
Right. So because of the auto regressive prediction, every time an NLM produces a token or a word, there is some level of probability for that word to take you out of the set of reasonable answers. And if you assume, which is a very strong assumption, that the probability of such error is that those errors are independent across a sequence of tokens being produced. Mhmm. What that means is that every time you produce a token, the probability that you were asked you you stay within the the set of correct answer decreases, and it decreases exponentially.

Speaker 0  [0:54](https://youtu.be/bOnBPGkxUuw&t=54)
So there's a strong, like you said, assumption there that if, there's a nausea probability of making a mistake, which there appears to be, then there's going to be a kind of drift.

Speaker 1  [1:04](https://youtu.be/bOnBPGkxUuw&t=64)
Yep. And that drift is exponential. It's like errors accumulate. Right? So so the probability that an answer would be nonsensical increases exponentially with the number of tokens.

Speaker 0  [1:17](https://youtu.be/bOnBPGkxUuw&t=77)
Is that obvious to you, by the way? Like well, so mathematically speaking, maybe. But, like, isn't there a kind of gravitational pull towards the truth? Because on on average, hopefully, the truth is well represented in the, training set?

Speaker 1  [1:34](https://youtu.be/bOnBPGkxUuw&t=94)
No. It's basically a struggle against the curse of dimensionality. So the way you can correct for this is that you fine tune the system by having it produce answers for all kinds of questions that people might come up with. Mhmm. And people are people, so they a lot of the questions that they have are very similar to each other. So you can probably cover, you know, 80% or whatever of, questions that people will will ask, by, you know, collecting data. And then, and then you fine tune the system to produce good answers for all of those things, and it's probably gonna be able to learn that because it's got a lot of capacity to to learn. But then there is, you know, the enormous set of prompts that you have not covered during training. And that set is enormous. Like, within the set of all possible prompts, the proportion of prompts that have been, used for training is absolutely tiny. It's a it's a tiny, tiny, tiny subset of all possible prompts. And so the system will behave properly on the prompts that has been either trained, pretrained, or fine tuned. But then there is an entire space of things that it cannot possibly have been trained on because it's just the the number is gigantic. So so whatever training the system, has been subject to to produce appropriate answers, you can break it by finding out a prompt that will be outside of the the the set of prompts that's been trained on or things that are similar, and then it will just spew complete nonsense.

Speaker 0  [3:15](https://youtu.be/bOnBPGkxUuw&t=195)
Do you when you say prompt, do you mean that exact prompt, or do you mean a prompt that's, like, in many parts very different than like, is it that easy to ask a question or to say a thing that hasn't been said before on the Internet?

Speaker 1  [3:32](https://youtu.be/bOnBPGkxUuw&t=212)
I mean, people have come up with, things where, like, you you put a essentially a random sequence of characters in the prompt. That's enough to kind of throw the system, into a mode where, you know, it is gonna answer something completely different than it would have answered without this. Mhmm. So that's the way to jailbreak the system, basically. Get it, you know, go outside of its, of its conditioning. Right?

Speaker 0  [3:55](https://youtu.be/bOnBPGkxUuw&t=235)
So that that's a very clear demonstration of it, but, of course, you know, that's, that goes outside of what it's designed to do. Right? If you actually stitch together reasonably grammatical sentences, is that the is it that easy to break it?

Speaker 1  [4:12](https://youtu.be/bOnBPGkxUuw&t=252)
Yeah. Some people have done things like you you you write a sentence in English, right, that has an or you ask a question in English, and it it produces a perfectly fine answer. And then you just substitute a few words by the same word in another language. I I know if a sudden the answer is complete nonsense.

Speaker 0  [4:30](https://youtu.be/bOnBPGkxUuw&t=270)
Yes. So so I guess what I'm saying is, like, which fraction of prompts that humans are likely to generate are going to break the system. So the the part

Speaker 1  [4:41](https://youtu.be/bOnBPGkxUuw&t=281)
of it is that there is a long tail. Yes. This is, an issue that a lot of people have realized, you know, in social networks and stuff like that, which is, there's a very, very long tail of of things that people will ask. And you can fine tune the system for the 80% or whatever of, of the things that most people will will ask. And then this long tail is is so large that you're not gonna be able to function the system for all the conditions. And in the end, the system has a being kind of a giant lookup table, right, essentially, which is not really what you want. You want systems that can reason. Certainly, they can plan. So the type of reasoning that takes place in, LLM is very, very primitive. And the reason you can tell is primitive is because the amount of computation that is spent per token produced is constant. So if you ask a question and that question has an answer in a given number of token, the amount of computation devoted to computing that answer can be exactly estimated. It's like, you know, it's hot it's the the size of the prediction network, you know, with its 36 layers or 92 layers or whatever it is, multiplied by number of tokens. That's it. And so, essentially, it doesn't matter if the question being asked is is simple to answer, complicated to answer, impossible to answer because it's a decidable or something. The amount of computation the system will be able to devote to that to the answer is constant or is number of token produced in the answer. Right? This is not the way we work. The way we reason is that when we're faced with a complex problem or complex question, we spend more time trying to solve it and answer it. Right? Because it's more difficult.

Speaker 0  [6:29](https://youtu.be/bOnBPGkxUuw&t=389)
There's a prediction element. There's a iterative element where you're, like, adjusting your understanding of a thing by going over and over and over. There's a hierarchical element, so on. Does this mean it's a fundamental flaw of LLMs, or does it mean that there's more part to that question?
