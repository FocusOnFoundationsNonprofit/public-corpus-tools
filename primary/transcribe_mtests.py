from fileops import *
from transcribe import *

if True:
    pass
if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/1900-01-01_Test file for do fileop_prepqa.md"
           
### YOUTUBE FUNCTIONS
def mtest_download_mp3_from_youtube():
    cur_url = "https://youtu.be/RNNfkIE7uYs"
    cur_path = "tests/test_manual_files/transcribe"
    print(download_mp3_from_youtube(cur_url, output_title = cur_path + '/download_yt_test'))  # WORKS 3-2 RT
def mtest_get_youtube_title_length():
    cur_url = "https://youtu.be/RNNfkIE7uYs"
    print(get_youtube_title_length(cur_url))  # WORKS 3-3 RT
    # should print ('Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip!', '0:39')
def mtest_download_link_list_to_mp3s():
    cur_urls = ["https://youtu.be/RNNfkIE7uYs", "https://youtu.be/VW6LYuli7VU"]
    print(download_link_list_to_mp3s(cur_urls))  # WORKS 3-3 RT
    # should print {'https://youtu.be/RNNfkIE7uYs': 'Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip!', 'https://youtu.be/VW6LYuli7VU': 'Richard Feynman talks about Algebra'}
def mtest_get_youtube_subtitles():
    cur_url = "https://youtu.be/RNNfkIE7uYs"
    print(get_youtube_subtitles(cur_url))  # WORKS 3-3 RT
    # should print 'there  was  a  little  annoyances  from   censorship ...'
def mtest_get_youtube_all():
    pass
#if __name__ == "__main__":        
    cur_url = "https://youtu.be/RNNfkIE7uYs"  #"https://youtu.be/mNP5w4n9sFU"
    print(get_youtube_all(cur_url))
    # should print {'title': 'Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip!', 'length': '0:00:39', 'chapters': '', 'description': 'Please Help Support This Channel:https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=BLJ283JMTMT7S\nThe famous physicist Richard P. Feynman always loved to test complex systems in the spirit of curiosity and fun and nowhere was this more true than in the security systems of the most complex scientific project in history, the Manhattan Project, where the greatest scientists of the age were gathered to create the first atomic bomb and in the process develop much of the scientific underpinnings of our modern civilization. \n\nFeynman, being Feynman, found that the best way to challenge the rigor of the establishment was with good old-fashioned mischief. He earned fame (or infamy) inside the safes of Los Alamos, cracking them with ease and leaving cryptic messages pretending to be a spy (all while real Soviet spies were inside and really learning the new nuclear secrets!) - hence his seemingly bizarre mischief making was indeed prophetic in many ways. \n\nHere, Richard Feynman talks briefly about how he tested fence security simply by "taking the path of least action" - through the holes in the fence! Funny stuff straight from the legendary man\'s mouth! Enjoy!', 'transcript': "there was a little annoyances from censorship and so forth but and checking in at gates and all kinds of things but there was it was understandable that such a thing had to go in fact most of the complaints was of a security was rather lacks in places there would be big holes in the outside fence the demand could walk through standing up and I used to enjoy going out through the gate coming in through the fence hole and going out through the gate again and then through the fence hole until the poor sergeant at the gate would gradually realize that this guy's come out of place four times without going in once and he kind of arrests me sort of", 'transcript source': 'auto-captions'}
def mtest_is_valid_youtube_url():
    #print(is_valid_youtube_url("https://youtu.be/RNNfkIE7uYs"))  # WORKS True 3-3 RT
    print(is_valid_youtube_url("https://youtu.be/XXXXXXX"))  # expected: False - ERROR: Unsupported URL:
def mtest_create_youtube_md():
    # Make sure to delete all files with this video title in the audio inbox and at any of the specified file paths below.
    cur_url = "https://youtu.be/RNNfkIE7uYs"
    #print(create_youtube_md(cur_url))  # expected: data/audio_inbox/Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip_yt.md
    #print(create_youtube_md(cur_url, title_or_path="Feynman Arrested"))  # expected: data/audio_inbox/Feynman Arrested_yt.md
    #print(create_youtube_md(cur_url, title_or_path="tests/test_manual_files/transcribe/Feynman Arrested WHOA"))  # expected: tests/test_manual_files/transcribe/Feynman Arrested WHOA_yt.md
    cur_file_path = "tests/test_manual_files/transcribe/2099-01-01_Arbitrary_yt.md"
    print(create_youtube_md(cur_url, title_or_path=cur_file_path))  # expected: tests/test_manual_files/transcribe/2099-01-01_Arbitrary_yt.md
def mtest_create_youtube_md_from_file_link():
    pass
#if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/jsons/2024-03-08_Test Deepgram with all features_nova2.md"
    print(create_youtube_md_from_file_link(cur_file_path))  # expected: same file_path with suffix replaced with _yt
def mtest_extract_feature_from_youtube_md():
    pass
#if __name__ == "__main__":        
    cur_file_path = "data/p_Mervin Praison/2023-11-06_Mervin Praison - OpenAI Assistants plus Python_yt.md"
    print(extract_feature_from_youtube_md(cur_file_path, "chapters"))  # expected: same file_path with suffix replaced with _yt

### DEEPGRAM AND JSON FUNCTIONS
def mtest_test_deepgram_client():
    pass
#if __name__ == "__main__":        
    test_deepgram_client()
def mtest_get_media_length():
    pass
#if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/1min youttube/1 Minute TED Talk.mp3"
    cur_url = "https://youtu.be/1j0X9QMF--M"
    print(get_media_length(cur_file_path))
    print(get_media_length(cur_url))
def mtest_transcribe_deepgram():
    pass
if __name__ == "__main__":        
    cur_audio_file_path = "tests/test_manual_files/1min youttube/1 Minute TED Talk.mp3"
    #transcribe_deepgram(cur_audio_file_path, model='whisper-medium')
    transcribe_deepgram(cur_audio_file_path, model='nova-2-general')
def mtest_transcribe_deepgram_with_callback():
    pass
#if __name__ == "__main__":        
    cur_audio_file_path = "tests/test_manual_files/1min youttube/1 Minute TED Talk.mp3"
    cur_callback_url = "https://lsehufc3n2.execute-api.us-west-2.amazonaws.com/api/transcription"
    print(transcribe_deepgram_callback(cur_audio_file_path, "enhanced-meeting", cur_callback_url))
def mtest_extract_feature_from_deepgram_json():
    pass
#if __name__ == "__main__":        
    cur_json_file_path = "tests/test_manual_files/jsons/2024-03-08_Test Deepgram with all features_nova2.json"
    #print(extract_feature_from_deepgram_json(cur_json_file_path, "summaries"))
    # print(repr(extract_feature_from_deepgram_json(cur_json_file_path, "sentiments")))
    # print(extract_feature_from_deepgram_json(cur_json_file_path, "topics"))
    # print(extract_feature_from_deepgram_json(cur_json_file_path, "intents"))
    print(repr(extract_feature_from_deepgram_json(cur_json_file_path, "intents")))    
def mtest_validate_transcript_json():
    cur_json_file_path = "tests/test_manual_files/jsons/2024-03-08_Test Deepgram with all features_nova2.json"
    print(validate_transcript_json(cur_json_file_path))
def mtest_set_various_transcript_headings_ffop():  # NOT TESTED AFTER REMOVING FFOP
    pass
#if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/jsons/2024-03-08_Test Deepgram with all features_nova2.md"
    set_various_transcript_headings(cur_file_path, "intents", "deepgram")
    #set_various_transcript_headings(cur_file_path, "description", "youtube")
    #cur_file_path = "data/p_Mervin Praison/2023-11-06_Mervin Praison - OpenAI Assistants plus Python_dgwhspm.md"
    #set_various_transcript_headings_ffop(cur_file_path, "chapters", "youtube")
    #set_various_transcript_headings_ffop(cur_file_path, "summaries", "deepgram")
    # expected: UserWarning when feature not present
    
def mtest_add_dg_summaries_to_md():
    pass
#if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/1min youttube/1 Minute TED Talk_dgwhspm_nosummaries.md" 

### NUMERAL CONVERT FUNCTIONS
def mtest_convert_ordinals_in_content():
    content = "This is the 1st example. now we move to the 2nd one."
    print(convert_ordinals_in_content(content, ['.', '?', '!']))
      # expected: "This is the first example. Now we move to the second one."
    content = "Here's the 3rd example? do you get it? here's the 4th."
    print(convert_ordinals_in_content(content, ['.', '?', '!'])) 
      # expected: "Here's the third example? Do you get it? Here's the fourth."
    content = "Wow, this is the 5th! isn't it great? now for the 6th."
    print(convert_ordinals_in_content(content, ['.', '?', '!']))
      # expected: "Wow, this is the fifth! Isn't it great? now for the sixth."
def mtest_extract_context():
    line = "apple banana coconut donut egg fig sample alex betty carl dan eliot fern."
    print(extract_context(line, re.search("sample", line), 3))  # expected: "donut egg fig sample alex betty carl"
    print(extract_context(line, re.search("sample", line), 4))  # expected: "coconut donut egg fig sample alex betty carl dan"
    print(extract_context(line, re.search("banana", line), 4))  # expected: "coconut donut egg fig sample alex betty carl dan"
    #print(extract_context(line, re.search("absent", line), 4))  # expected ValueError: Match not found
def mtest_convert_nums_to_words():   # NOT TESTED AFTER REMOVING FFOP
    pass
#if __name__ == "__main__":        
    #cur_file_path = "tests/test_manual_files/1900-01-01_Test file for do fileop_prepqa.md"
    cur_file_path = "tests/test_manual_files/transcribe/test numbers convert.md"
    ref_file_path = "tests/test_manual_files/transcribe/test numbers convert_convertnumsREF.md"
    new_file_path = convert_nums_to_words(cur_file_path, overwrite='no', verbose=True)
    compare_files_text(ref_file_path, new_file_path)
    new2_file_path = copy_file_and_append_suffix(cur_file_path, suffix_new='_convertnums2')
    convert_nums_to_words(new2_file_path, verbose=True)
    compare_files_text(ref_file_path, new2_file_path)
    # cur_file_path = "data/training_old1-20_md/FloodLAMP_Demo13_Plate_v1.md"
    # print(convert_nums_to_words(cur_file_path, overwrite='no')

### SPEAKER NAMES FUNCTIONS
def mtest_find_unassigned_speakers():
    cur_md_file_path = 'tests/test_manual_files/transcribe/2000-01-01_Test file for assign speaker names_dgwhspm.md'
    print(find_unassigned_speakers(cur_md_file_path, verbose=True))
def mtest_propagate_speaker_names_throughout_md():
    pass
#if __name__ == "__main__":        
    cur_md_file_path = 'tests/test_manual_files/transcribe/2000-01-01_Test file for assign speaker names_dgwhspm.md'
    cur_input_speaker_names = [(0, 'Alice'), (1, 'Bob')]
    print(propagate_speaker_names_throughout_md(cur_md_file_path, cur_input_speaker_names))
def mtest_iterate_input_speaker_names():
    pass
#if __name__ == "__main__":        
    cur_md_file_path = 'tests/test_manual_files/transcribe/2000-01-01_Test file for assign speaker names_dgwhspm.md'
    print(iterate_input_speaker_names(cur_md_file_path))
def mtest_assign_speaker_names():
    pass
#if __name__ == "__main__":        
    cur_md_file_path = 'tests/test_manual_files/transcribe/2000-01-01_Test file for assign speaker names_dgwhspm.md'
    assign_speaker_names(cur_md_file_path)

### WRAPPER FUNCTIONS TO PROCESS DEEPGRAM TRANSCRIPTION
def mtest_create_transcript_md_from_json():
    pass
#if __name__ == "__main__":        
    cur_json = 'tests/test_manual_files/jsons/2024-03-08_Test Deepgram with all features_nova2.json'
    #cur_json = 'tests/test_manual_files/1min youttube/1 Minute TED Talk_dgwhspm.json'
    print(create_transcript_md_from_json(cur_json))
def mtest_process_deepgram_transcription():
    pass
#if __name__ == "__main__":        
    test_deepgram_client()
    # cur_title = 'Shortest Interview Ever'  # this is not creating multiple speaker segments 4-23 RT
    # cur_link = 'https://youtu.be/6pMcXSixdVQ'
    # print(process_deepgram_transcription(cur_title, cur_link, model='nova-2'))
    cur_title = 'Closer to Truth - for test'
    cur_link = 'https://www.youtube.com/watch?v=mNP5w4n9sFU'
    print(process_deepgram_transcription(cur_title, cur_link, model='nova-2'))
def mtest_process_deepgram_transcription_from_audio_file():
    pass
#if __name__ == "__main__":        
    test_deepgram_client()
    cur_audio_file_path = 'tests/test_manual_files/transcribe/Shortest Interview Ever.mp3'
    cur_link = 'https://youtu.be/6pMcXSixdVQ'
    print(process_deepgram_transcription_from_audio_file(cur_audio_file_path, cur_link, model='nova-2'))
def mtest_process_multiple_videos():
    pass
#if __name__ == "__main__":        
    videos_to_process = [  #  (title, link)
        ("2023-11-10_Lex Clip - Elon Musk on the existence of a soul", "https://youtu.be/1_wT3NEGT6s"),
        ("Feynman - There are No Miracle People", "https://youtu.be/IIDLcaQVMqw"),
    ] 
    process_multiple_videos(videos_to_process)  # default set to audio_inbox

