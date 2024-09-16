from fileops import *
from llm import *
#from mod_corpus.process_corpus_main_revert import *

if True:
    pass
# if __name__ == "__main__":    
    cur_file_path = "tests/test_manual_files/1900-01-01_Test file for do fileop_prepqa.md"


### PRINT AND TOKEN
def mtest_token_counter():
    pass
#if __name__ == "__main__":
    
    #print(token_counter("This is a test string of arbitrary length. The output should be the number of tokens within this string."))
    # cur_file_path = 'tests/test_manual_files/llm_test_files/split_file_test_files/2023-06-28_Bennett_prepqa.md'
    # print(token_counter(get_heading_from_file(cur_file_path, "### transcript")) / 1000000 * 5)
    cur_str = '''
USER QUESTION: What is the meaning of life?

There is a partial match of your question in David Deutsch's interviews. See his QUOTED QUESTIONS AND ANSWERS below followed by an AI ANSWER that synthesizes these quotes with David Deutsch's philosophy and your exact question.

QUOTED QUESTION 1: What does it mean to know everything?
QUOTED ANSWER 1: When I was a child, I remember being told that in the distant past, a very learned person might hope to understand everything that was understood. Whereas now because of specialization, because so much is known, that's impossible. That one person can only understand a very small fraction of what's known. And I really didn't believe this, I didn't want to believe this. And I envied the ancient scholars who might have aspired to knowing everything that was known at the time. And what I meant by, "knowing everything that was known," or "understanding everything that was understood," is not that they knew in detail everything that happened, that they had lists of things which they remembered. That's very far from what I meant. I meant that they understood all the explanations that were known. And I believe that we are not heading away from an era in which one might understand all the explanations as they're known, but towards it, because we are continually unifying and broadening and deepening our explanations of the world.
QUOTED ANSWER STARS: 5
QUOTED QUESTION SIMILARITY SCORE: 42%

QUOTED QUESTION 2: What is meaning of life, the significance of our existence?
QUOTED ANSWER 2: _Regarding the significance of our existence,_ this has to do with both moral and aesthetic values. What we're trying to do, even though many people try to deny this, they deny that they are seeking, trying to do what is right or trying to create what is actually beautiful and so on. But that is what we're trying to do, and that is the meaning. Religions traditionally thought that the meaning was already known or had been revealed to humans and that what our task is, is to live up to that, to enact it. My view is the other way around, that __the meaning of life is something that we are using creativity to discover, to build. There isn't a perfectly accurate word for what we're doing, but we can't find the meaning of life in the world out there, nor just by pure thought or by reference to an authority. What we have to do is form explanations about what is right and wrong, what is better and worse, what's beautiful and ugly, and hone those theories while also trying to meet them. At any one moment, we will meet them imperfectly, just like scientific theories at any one moment are only an imperfect explanation of what the physical world is like. But through criticism and conjecture and seeking the truth, we can eliminate the errors in what we had previously thought and thereby make progress. And that is trying to find the meaning of life, trying to create the meaning of life is the meaning of life.__ *IN-LINE: So we want to model and articulate reality.* Yes, both moral, aesthetic, as well as abstract and physical reality. Yes, exactly.
QUOTED ANSWER STARS: 4
QUOTED QUESTION SIMILARITY SCORE: 76%
'''
    print(token_counter(cur_str) / 1000000 * 5)
def mtest_cost_llm_on_file():
    pass
#if __name__ == "__main__":
    cur_file_path = 'tests/test_manual_files/llm_test_files/split_file_test_files/2023-06-28_Bennett_prepqa.md'
    print(cost_llm_on_file(cur_file_path, "this is an arbitrary prompt", 'gpt-4-turbo', TOKEN_COST_DICT, group_segments_token_cap, output_tokens_ratio=1)) 

### SPLIT FILES
def mtest_get_line_numbers_with_match():
    pass
#if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/llm_test_files/split_file_qa_test_files/2023-06-28_Bennett_prepqa_blocksREF.md"
    print(get_line_numbers_with_match(cur_file_path, "---"))
def mtest_get_speaker_segments():
    pass
#if __name__ == "__main__":        
    cur_file_path = "data/floodlamp/reg/fda-townhalls/2020-12-09_Virtual Town Hall 36_fixnames.md"
    print(get_speaker_segments(cur_file_path))
def mtest_plot_segment_tokens():  # tests count_segment_tokens also
    pass
#if __name__ == "__main__":        
    cur_file_path = "data/floodlamp/reg/fda-townhalls/2020-12-09_Virtual Town Hall 36_fixnames.md"
    print(plot_segment_tokens(cur_file_path))
def mtest_split_file_select_speaker():
    pass
#if __name__ == "__main__":  
    cur_file_path = "tests/test_manual_files/llm_test_files/split_file_test_files/2023-06-28_Bennett_prepqa.md"
    new_file_path = split_file_select_speaker(cur_file_path, speaker="David Deutsch")
    line_numbers = get_line_numbers_with_match(new_file_path, "---")
    print(line_numbers)
    print(line_numbers == [14, 20, 26, 32, 38, 44, 50, 56, 62, 69, 72, 78, 84, 90, 96, 102, 108, 114, 123, 135, 141, 147, 153, 159])
def mtest_split_file_every_speaker():
    pass
#if __name__ == "__main__":        
    #cur_file_path = "tests/test_manual_files/llm_test_files/scall_test_files/1900-01-01_scall test file.md"
    cur_file_path = "tests/test_manual_files/llm_test_files/split_file_test_files/2023-06-28_Bennett_prepqa.md"
    new_file_path = split_file_every_speaker(cur_file_path)
    line_numbers = get_line_numbers_with_match(new_file_path, "---")
    print(line_numbers)
    print(line_numbers == [11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 89, 92, 95, 98, 101, 104, 107, 110, 113, 116, 119, 122, 125, 128, 131, 134, 137, 140, 143, 146, 149, 152, 155, 158, 161, 164, 167, 170, 173, 176, 179, 182, 185, 188, 191, 194, 197, 200, 203, 207, 210, 213, 216, 219, 222, 225, 228, 231, 234, 237, 240, 243, 246, 249, 252, 255, 258, 261, 264, 267, 270, 273, 276, 279, 282, 285, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324, 327, 330, 333, 336, 339, 342, 345, 348, 351, 354, 357, 360, 363, 366, 369, 372, 375, 378, 381, 384, 387, 390, 393, 396, 399, 402, 405, 408])
def mtest_split_file_token_cap():
    pass
#if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/llm_test_files/split_file_test_files/2023-06-28_Bennett_prepqa.md"
    new_file_path = split_file_token_cap(cur_file_path, token_cap=1000)
    line_numbers = get_line_numbers_with_match(new_file_path, "---")
    print(line_numbers)
    print(line_numbers == [14, 26, 41, 59, 81, 105, 141])
    
### OPENAI LLM
def mtest_test_openai_chat():
    pass
#if __name__ == "__main__":
    test_openai_chat()
def mtest_scall_replace_ffop():
    pass
#if __name__ == "__main__":
    cur_blocks_file_path = "tests/test_manual_files/llm_test_files/scall_test_files/1900-01-01_scall test file_blocks.md"
    MY_PROMPT = "turn the text into 2 lines that rhyme"
    print(scall_replace(cur_blocks_file_path, MY_PROMPT, suffix_new='_scall-replace-poem', retain_delimiters=True))
def mtest_scall_append_ffop():
    pass
#if __name__ == "__main__":
    cur_file_path = "tests/test_manual_files/llm_test_files/scall_test_files/1900-01-01_scall test file_blocks.md"
    MY_PROMPT = "make a onery redneck response to this as a single sentence in all caps"
    print(scall_append(cur_file_path, MY_PROMPT, suffix_new='_scall-append-redneck', retain_delimiters=True))

### ANTHROPIC LLM
def mtest_anthropic_chat_completion_request():
    pass
#if __name__ == "__main__":
    # Test case 1: Basic request with system message and user message
    system_message = "You are a helpful assistant."
    user_message = "What is the capital of France?"
    messages = [
        {"role": "user", "content": user_message}
    ]
    
    response = anthropic_chat_completion_request(messages=messages, system=system_message)
    print("Test case 1 response:", response)
    
    # Test case 2: Request with different model and temperature
    custom_model = "claude-3-opus-20240229"
    custom_temp = 0.9
    custom_message = "Tell me a joke about programming."
    
    response = anthropic_chat_completion_request(
        model=custom_model,
        messages=[{"role": "user", "content": custom_message}],
        temperature=custom_temp
    )
    print(f"Test case 2 response (model: {custom_model}, temp: {custom_temp}):", response)
    
    # Test case 3: Error handling (no messages provided)
    #print("**** Test case 3 (error handling) - Expect error! ***")
    try:
        anthropic_chat_completion_request()
    except TypeError as e:
        print("Test case 3 (error handling) - Expected error:", str(e))
def mtest_simple_anthropic_chat_completion_request():
    pass
#if __name__ == "__main__":
    MY_PROMPT = "give me a corny Dad joke"
    print(simple_anthropic_chat_completion_request(MY_PROMPT))

### LLM PROCESSING
def mtest_create_simple_llm_file():
    pass
#if __name__ == "__main__":
    cur_file_path = "tests/test_manual_files/llm_test_files/scall_test_files/1900-01-01_scall test file.md"
    #MY_PROMPT = "turn the text into a short corny Dad joke"
    #print(create_simple_llm_file(cur_file_path, MY_PROMPT, "_dadjoke", "replace", split_file_every_speaker_ffop))
    MY_PROMPT = "reply with what a California valley girl would say about this"
    print(create_simple_llm_file(cur_file_path, MY_PROMPT, "_create-simple-llm-file-replace-valleygirl", "replace", split_file_every_speaker))

#### COPYEDIT
# TODO needs updating to change to replacement for ffop function
def mtest_create_copyedit_file():
    pass
#if __name__ == "__main__":
    cur_file_path = "tests/test_manual_files/llm_test_files/scall_test_files/1900-01-01_scall test file_test.md"
    #cur_file_path = "tests/test_manual_files/llm_test_files/split_file_test_files/2023-06-28_Bennett_prepqa.md"
    #create_copyedit_file(cur_file_path, split_file_select_speaker_ffop, PROMPT_COPYEDIT, speaker="David Deutsch")
    create_copyedit_file(cur_file_path, split_file_every_speaker_ffop, PROMPT_COPYEDIT)
    #create_copyedit_file(cur_file_path, split_file_token_cap_ffop, PROMPT_COPYEDIT, token_cap=1000)

#### TRANSITIONS
def mtest_mod_blocks_file_with_adjacent_words():
    pass
#if __name__ == "__main__":
    # copy the file "1900-01-01_scall test file_blocksREF.md" and rename as just _blocks, then when this mtest works use that _blocks file with the next mtest
    cur_file_path = "tests/test_manual_files/llm_test_files/scall_test_files/1900-01-01_scall test file_blocks.md" 
    mod_blocks_file_with_adjacent_words(cur_file_path, 5)
def mtest_scall_replace_adjacent_words():
    pass
#if __name__ == "__main__":
    # use the modified _blocks file from the above mtest
    cur_file_path = "tests/test_manual_files/llm_test_files/scall_test_files/1900-01-01_scall test file_blocks.md"
    print(scall_replace_adjacent_words(cur_file_path, PROMPT_TRANSITIONS, 10, overwrite="no-sub"))
def mtest_create_transitions_file():
    pass
#if __name__ == "__main__":
    cur_file_path = "tests/test_manual_files/llm_test_files/scall_test_files/1900-01-01_scall test file for transitions_test.md"
    print(create_transitions_file(cur_file_path, split_file_every_speaker, PROMPT_TRANSITIONS))

#### QA
def mtest_create_qa_file_select_speaker(): 
    pass
#if __name__ == "__main__":
    cur_file_path = "tests/test_manual_files/llm_test_files/create_qa_test_files/1900-01-01_Test file for do qa_prepqa.md"
    print(create_qa_file_select_speaker(cur_file_path, "David Deutsch", FCALL_PROMPT_QA_DIALOGUE_FROMANSWER))
def mtest_create_qa_file_incremental():
    pass
#if __name__ == "__main__":
    cur_file_path = "data/floodlamp/reg/fda-townhalls/dev/2020-12-09_Virtual Town Hall 36_manual-edits.md"
    create_qa_file_from_transcript_incremental(cur_file_path, FCALL_SYSTEM_PROMPT_QA_INCREMENTAL_TRANSCTIPRT_FDA_TOWNHALLS)
def mtest_run_automated_evaluation():
    pass
#if __name__ == "__main__":
    transcript_file = "data/floodlamp/reg/fda-townhalls/dev/2020-12-09_Virtual Town Hall 36_manual-edits.md"
    qa_file = "data/floodlamp/reg/fda-townhalls/dev/2020-12-09_Virtual Town Hall 36_qa-incremental.md"
    run_automated_evaluation(transcript_file, qa_file)
    
    # pos_start = 3977
    # pos_end = pos_start + 100
    # transcript = get_heading(transcript_file, "### transcript")
    # transcript = transcript.lstrip('### transcript').rstrip('\n').lstrip('\n*')
    # print(transcript[pos_start:pos_end])
