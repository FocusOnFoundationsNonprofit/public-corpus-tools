# Run tests with python -m unittest discover -s tests

import os
import sys
# Add the parent directory to the Python path so we can import the 'general' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch, Mock, mock_open, MagicMock, call
from termcolor import colored

from general.fileops import *
from general.llm import *

### INITAL HELPER
class TestPrettyPrintFunction(unittest.TestCase):
    def setUp(self):
        # Example setup for messages and tools
        self.messages = [
            {
                "role": "system",
                "content": "\nYou are an expert text analyzer that is trained in identifying questions or implied questions. You will be given dialogue and your role is to return a question that would make sense to ask, or was asked that is best answered by the final text block in the dialogue. You will use your tool to only return exact JSON in the format specified.\n"
            },
            {
                "role": "user",
                "content": "David Deutsch [4:12](https://www.youtube.com/watch?v=SDZ454K_lBY&t=252)\nThe multiverse theory comes about as an explanation of the predictions of our best theory of physics, which is quantum mechanics. Quantum mechanics makes very accurate predictions, the most accurate predictions that any theory of physics has ever made. But if you want to explain why these predictions are so, how these physical events come about, there's no alternative but to postulate that what we see around us is not the whole of reality, that reality is much more varied and has a great multiplicity. This is what we call multiple universes."
            },
            {
                "role": "assistant",
                "content": {
                    "tool_calls": [
                        {
                            "type": "function",
                            "function": {
                                "name": "get_qa",
                                "arguments": '{"question":"What is the basis for the existence of multiple universes according to quantum mechanics?","timestamp":"4:12"}'
                            }
                        }
                    ]
                }
            }
        ]
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "TestFunction",
                    "description": "This is a test function.",
                    "parameters": {
                        "properties": {
                            "param1": {
                                "description": "This is the first parameter."
                            },
                            "param2": {
                                "description": "This is the second parameter."
                            }
                        }
                    }
                }
            }
        ]

    def test_pretty_print_function_with_prompts(self):
        output = pretty_print_function(self.messages, self.tools, print_prompts=True, print_input=True)
        # print(f"DEBUG output[0] = {output[0]}")
        # print(f"DEBUG output[1] = {output[1]}")
        # print(f"DEBUG output[2] = {output[2]}")
        self.assertIn("System Prompt:", output[0])
        self.assertIn("User Input:", output[1])
        self.assertIn("Function Parameters Responses:", output[2])

    def test_pretty_print_function_without_prompts(self):
        output = pretty_print_function(self.messages, self.tools, print_prompts=False, print_input=True)
        self.assertEqual("", output[0])  # No system prompts
        self.assertIn("User Input:", output[1])
        self.assertIn("Function Parameters Responses:", output[2])
    
class TestPrettyPrintFunctionDescriptions(unittest.TestCase):
    def test_pretty_print_function_descriptions(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "TestFunction",
                    "description": "This is a test function.",
                    "parameters": {
                        "properties": {
                            "param1": {
                                "description": "This is the first parameter."
                            },
                            "param2": {
                                "description": "This is the second parameter."
                            }
                        }
                    }
                }
            }
        ]
        print_color = "blue"  # Example color

        # Expected output generation
        expected_output = ""
        for tool in tools:
            if tool["type"] == "function":
                function_name = f"Function Name: {tool['function']['name']}\n"
                function_description = f"Function Description: {tool['function']['description']}\n"
                expected_output += function_name + function_description
                expected_output += "Function Parameter Descriptions:\n\n"
                properties = tool['function']['parameters']['properties']
                for prop, details in properties.items():
                    prop_description = f"  {prop}: {details['description'].strip()}\n"
                    expected_output += prop_description
                #expected_output += '\n'  # Ensure there is a newline after each property description

        # Call the function to test
        output_str = pretty_print_function_descriptions(tools, print_color)
        # print(f"\nDEBUG returned: {repr(output_str)}")
        # print(f"\nDEBUG expected: {repr(expected_output)}")
        
        # Compare the function output with the expected output
        self.assertEqual(output_str.strip(), expected_output.strip())


### SEPARATE BLOCKS FUNCTIONS
class TestGetLineNumbersWithMatch(unittest.TestCase):
    def setUp(self):
        # Setup method to create a temporary test file
        self.test_filename = 'test_file.md'
        self.test_content = """Start
---
This is a test file.
---
It contains multiple lines.
---
Some of which match a given string.
---
"""
        with open(self.test_filename, 'w') as f:
            f.write(self.test_content)

    def tearDown(self):
        # Teardown method to remove the temporary test file
        os.remove(self.test_filename)

    def test_get_line_numbers_with_match__match_found(self):
        # Test case where the match string is found in the file
        match_str = '---'
        expected_line_numbers = [2, 4, 6, 8]
        self.assertEqual(get_line_numbers_with_match(self.test_filename, match_str), expected_line_numbers)

    def test_get_line_numbers_with_match__no_match(self):
        # Test case where the match string is not found in the file
        match_str = 'not found'
        self.assertEqual(get_line_numbers_with_match(self.test_filename, match_str), [])

    def test_get_line_numbers_with_match__file_does_not_exist(self):
        # Test case where the file does not exist
        with self.assertRaises(ValueError):
            get_line_numbers_with_match('nonexistent_file.md', '---')

class TestGetSpeakerSegments(unittest.TestCase):
    def setUp(self):
        # Setup method to create a temporary test file before each test
        self.test_file_name = 'test_speaker_segments.md'
        self.test_header = """## metadata
last updated: 11-19-2023

## content

### transcript

"""
        self.test_segskip = """Charles Bédard  [0:00](https://www.youtube.com/watch?v=CluVy2jICgs&t=0)  SKIPQA
So welcome everyone"""
        self.test_seg0 = """David Deutsch  [1:14](https://www.youtube.com/watch?v=CluVy2jICgs&t=74)
Well, it's no."""
        self.test_seg1 = """Charles Bédard  [1:18](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)
Yeah, yeah, yeah"""
        self.test_seg2 = """David Deutsch  [14:42](https://www.youtube.com/watch?v=CluVy2jICgs&t=882)
Well, I think"""
        self.test_text = self.test_header + self.test_segskip + '\n\n' + self.test_seg0 + '\n\n' + self.test_seg1 + '\n\n' + self.test_seg2 + '\n\n'
        # print(f"DEBUG test text: {self.test_text}")
        with open(self.test_file_name, 'w') as f:
            f.write(self.test_text)

    def tearDown(self):
        # Teardown method to remove the temporary test file after each test
        os.remove(self.test_file_name)

    def test_get_speaker_segments__default_skip_string(self):
        # Test retrieving segments without the skip string
        segments = get_speaker_segments(self.test_file_name)
        expected_segments = [self.test_seg0, self.test_seg1, self.test_seg2]
        self.assertEqual(segments, expected_segments)

    def test_get_speaker_segments__with_different_skip_string(self):
        # Test retrieving segments with a different skip string that is not present
        segments = get_speaker_segments(self.test_file_name, 'NOSUCHSTRING')
        expected_segments = [self.test_segskip, self.test_seg0, self.test_seg1, self.test_seg2]
        self.assertEqual(segments, expected_segments)

class TestGroupSegmentsSelectSpeaker(unittest.TestCase):
    def setUp(self):
        # Setup test segments
        self.segments = [
            "Charles Bédard  [1:00](https://www.youtube.com/watch?v=CluVy2jICgs&t=0)\nI have questions.",
            "David Deutsch  [1:14](https://www.youtube.com/watch?v=CluVy2jICgs&t=74)\nWell, it's no.",
            "Charles Bédard  [1:18](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nYeah, yeah, yeah",
            "Extra Dude  [1:34](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nHi mom",
            "David Deutsch  [14:42](https://www.youtube.com/watch?v=CluVy2jICgs&t=882)\nWell, I think"
        ]

    def test_group_segments_select_speaker__for_deutsch(self):
        # Test filtering segments for David Deutsch
        returned_segments = group_segments_select_speaker(self.segments, 'David Deutsch')
        expected_segments = [
            "Charles Bédard  [1:00](https://www.youtube.com/watch?v=CluVy2jICgs&t=0)\nI have questions.\n\nDavid Deutsch  [1:14](https://www.youtube.com/watch?v=CluVy2jICgs&t=74)\nWell, it's no.",
            "Charles Bédard  [1:18](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nYeah, yeah, yeah\n\nExtra Dude  [1:34](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nHi mom\n\nDavid Deutsch  [14:42](https://www.youtube.com/watch?v=CluVy2jICgs&t=882)\nWell, I think"
        ]
        self.assertEqual(returned_segments, expected_segments)

    def test_group_segments_select_speaker__for_bedard(self):
        # Test filtering segments for Charles Bédard
        returned_segments = group_segments_select_speaker(self.segments, 'Charles Bédard')
        expected_segments = [
            "Charles Bédard  [1:00](https://www.youtube.com/watch?v=CluVy2jICgs&t=0)\nI have questions.",
            "David Deutsch  [1:14](https://www.youtube.com/watch?v=CluVy2jICgs&t=74)\nWell, it's no.\n\nCharles Bédard  [1:18](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nYeah, yeah, yeah"
        ]
        # print(f"\nDEBUG returned_segments: {repr(returned_segments)}")
        # print(f"\nDEBUG expected_segments: {repr(expected_segments)}")
        self.assertEqual(returned_segments, expected_segments)

class TestGroupSegmentsTokenCap(unittest.TestCase):
    def setUp(self):
        self.segments = [
            "Charles Bédard  [1:00](https://www.youtube.com/watch?v=CluVy2jICgs&t=0)\nThis is a short segment.",  # Assume 5 words = 3.75 tokens
            "David Deutsch  [1:14](https://www.youtube.com/watch?v=CluVy2jICgs&t=74)\nThis segment is a bit longer than the previous one, but still not too long.",  # Assume 14 words = 10.5 tokens
            "Charles Bédard  [1:18](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nThis is another short segment.",  # Assume 5 words = 3.75 tokens
            "Extra Dude  [1:34](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nThis segment is extremely long and definitely exceeds the token cap on its own by having a huge amount of words that no other segment has.",  # Assume 28 words = 21 tokens
            "David Deutsch  [14:42](https://www.youtube.com/watch?v=CluVy2jICgs&t=882)\nFinal short segment to test grouping."  # Assume 7 words = 5.25 tokens
        ]

    def test_group_segments_token_cap__above_all_cap(self):
        # Test grouping segments without any single segment exceeding the token cap
        token_cap = 1000  # above all combined
        returned_segments = group_segments_token_cap(self.segments, token_cap)
        expected_segments = [
            "Charles Bédard  [1:00](https://www.youtube.com/watch?v=CluVy2jICgs&t=0)\nThis is a short segment.\n\nDavid Deutsch  [1:14](https://www.youtube.com/watch?v=CluVy2jICgs&t=74)\nThis segment is a bit longer than the previous one, but still not too long.\n\nCharles Bédard  [1:18](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nThis is another short segment.\n\nExtra Dude  [1:34](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nThis segment is extremely long and definitely exceeds the token cap on its own by having a huge amount of words that no other segment has.\n\nDavid Deutsch  [14:42](https://www.youtube.com/watch?v=CluVy2jICgs&t=882)\nFinal short segment to test grouping."
        ]
        # print(f"\nDEBUG returned_segments: {repr(returned_segments)}")
        # print(f"\nDEBUG expected_segments: {repr(expected_segments)}")
        # self.assertEqual(returned_segments, expected_segments)

    def test_group_segments_token_cap__intermediate_cap(self):
        # Test grouping segments without any single segment exceeding the token cap
        token_cap = 50  # above all combined
        returned_segments = group_segments_token_cap(self.segments, token_cap)
        expected_segments = [
            "Charles Bédard  [1:00](https://www.youtube.com/watch?v=CluVy2jICgs&t=0)\nThis is a short segment.\n\nDavid Deutsch  [1:14](https://www.youtube.com/watch?v=CluVy2jICgs&t=74)\nThis segment is a bit longer than the previous one, but still not too long.\n\nCharles Bédard  [1:18](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nThis is another short segment.\n\nExtra Dude  [1:34](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nThis segment is extremely long and definitely exceeds the token cap on its own by having a huge amount of words that no other segment has.",
            "David Deutsch  [14:42](https://www.youtube.com/watch?v=CluVy2jICgs&t=882)\nFinal short segment to test grouping."
        ]
        # print(f"\nDEBUG returned_segments: {repr(returned_segments)}")
        # print(f"\nDEBUG expected_segments: {repr(expected_segments)}")
        # self.assertEqual(returned_segments, expected_segments)

    def test_group_segments_token_cap__low_cap(self):
        # Test grouping segments without any single segment exceeding the token cap
        token_cap = 20  # above all combined
        returned_segments = group_segments_token_cap(self.segments, token_cap)
        expected_segments = [
            "Charles Bédard  [1:00](https://www.youtube.com/watch?v=CluVy2jICgs&t=0)\nThis is a short segment.\n\nDavid Deutsch  [1:14](https://www.youtube.com/watch?v=CluVy2jICgs&t=74)\nThis segment is a bit longer than the previous one, but still not too long.",
            "Charles Bédard  [1:18](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nThis is another short segment.", 
            "Extra Dude  [1:34](https://www.youtube.com/watch?v=CluVy2jICgs&t=78)\nThis segment is extremely long and definitely exceeds the token cap on its own by having a huge amount of words that no other segment has.",
            "David Deutsch  [14:42](https://www.youtube.com/watch?v=CluVy2jICgs&t=882)\nFinal short segment to test grouping."
        ]
        # print(f"\nDEBUG returned_segments: {repr(returned_segments)}")
        # print(f"\nDEBUG expected_segments: {repr(expected_segments)}")
        # self.assertEqual(returned_segments, expected_segments)

    def test_group_segments_token_cap__empty_segments(self):
        # Test handling of empty segments list
        grouped_segments = group_segments_token_cap([], 100)
        self.assertEqual(grouped_segments, [])

class TestSeparateBlocksSelectSpeakerFfop(unittest.TestCase):
    def setUp(self):
        # Setup method to find the given test file
        self.test_filepath = "tests/test_manual_files/llm_test_files/separate_blocks_test_files/2023-06-28_Bennett_prepqa.md"

    def tearDown(self):
        # Teardown method to remove the QA file after each test case
        blocks_filepath = self.test_filepath.replace('.md', '_blocks.md')
        if os.path.exists(blocks_filepath):
            os.remove(blocks_filepath)

    def test_separate_blocks_select_speaker_ffop(self):
        # Test adding block delimiters after a specific speaker
        speaker = "David Deutsch"
        new_file_path = do_ffop(separate_blocks_select_speaker_ffop, self.test_filepath, speaker, overwrite='no')
        expected_line_numbers = [13, 19, 25, 31, 37, 43, 49, 55, 61, 68, 71, 77, 83, 89, 95, 101, 107, 113, 122, 134, 140, 146, 152, 158]
        self.assertEqual(get_line_numbers_with_match(new_file_path, '---'), expected_line_numbers)

class TestSeparateBlocksEverySpeakerFfop(unittest.TestCase):
    def setUp(self):
        # Setup method to find the given test file
        self.test_filepath = "tests/test_manual_files/llm_test_files/separate_blocks_test_files/2023-06-28_Bennett_prepqa.md"

    def tearDown(self):
        # Teardown method to remove the QA file after each test case
        blocks_filepath = self.test_filepath.replace('.md', '_blocks.md')
        if os.path.exists(blocks_filepath):
            os.remove(blocks_filepath)

    def test_separate_blocks_every_speaker_ffop(self):
        # Test adding block delimiters after a specific speaker
        new_file_path = do_ffop(separate_blocks_every_speaker_ffop, self.test_filepath, overwrite='no')
        expected_line_numbers = [10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91, 94, 97, 100, 103, 106, 109, 112, 115, 118, 121, 124, 127, 130, 133, 136, 139, 142, 145, 148, 151, 154, 157, 160, 163, 166, 169, 172, 175, 178, 181, 184, 187, 190, 193, 196, 199, 202, 206, 209, 212, 215, 218, 221, 224, 227, 230, 233, 236, 239, 242, 245, 248, 251, 254, 257, 260, 263, 266, 269, 272, 275, 278, 281, 284, 287, 290, 293, 296, 299, 302, 305, 308, 311, 314, 317, 320, 323, 326, 329, 332, 335, 338, 341, 344, 347, 350, 353, 356, 359, 362, 365, 368, 371, 374, 377, 380, 383, 386, 389, 392, 395, 398, 401, 404, 407]
        self.assertEqual(get_line_numbers_with_match(new_file_path, '---'), expected_line_numbers)

class TestSeparateBlocksTokenCapFfop(unittest.TestCase):
    def setUp(self):
        # Setup method to find the given test file
        self.test_filepath = "tests/test_manual_files/llm_test_files/separate_blocks_test_files/2023-06-28_Bennett_prepqa.md"

    def tearDown(self):
        # Teardown method to remove the QA file after each test case
        blocks_filepath = self.test_filepath.replace('.md', '_blocks.md')
        if os.path.exists(blocks_filepath):
            os.remove(blocks_filepath)

    def test_separate_blocks_token_cap_ffop(self):
        # Test adding block delimiters after a specific speaker
        new_file_path = do_ffop(separate_blocks_token_cap_ffop, self.test_filepath, token_cap=1000, overwrite='no')
        expected_line_numbers = [13, 25, 40, 58, 80, 104, 140]
        self.assertEqual(get_line_numbers_with_match(new_file_path, '---'), expected_line_numbers)


### LLM SIMPLE CALL FUNCTIONS
class TestProcessBlockWithLLM(unittest.TestCase):
    @patch('general.llm.openai_chat_completion_request')
    def test_process_block_with_llm__successful_response(self, mock_chat_completion):
        # Simulate a successful API response
        mock_chat_completion.return_value.json.return_value = {
            "choices": [{"message": {"content": "Processed text block"}}]
        }
        mock_chat_completion.return_value.status_code = 200

        block = "Original text block"
        prompt = "Please summarize this text."
        expected_response = "Processed text block"
        response = process_block_with_llm(block, prompt)

        self.assertEqual(response, expected_response)

    @patch('general.llm.openai_chat_completion_request')
    def test_process_block_with_llm__no_choices(self, mock_chat_completion):
        # Simulate a response with no 'choices'
        mock_chat_completion.return_value.json.return_value = {}
        mock_chat_completion.return_value.status_code = 200

        block = "Original text block"
        prompt = "Please summarize this text."
        response = process_block_with_llm(block, prompt)

        self.assertIsNone(response)

    @patch('general.llm.openai_chat_completion_request')
    def test_process_block_with_llm__failed_request(self, mock_chat_completion):
        # Simulate a failed request
        mock_chat_completion.return_value.status_code = 400
        mock_chat_completion.return_value.text = "Bad Request"

        block = "Original text block"
        prompt = "Please summarize this text."
        response = process_block_with_llm(block, prompt)

        self.assertIsNone(response)

class TestProcessFileBlocks(unittest.TestCase):
    test_file_path = 'test_file_blocks.md'

    @classmethod
    def setUpClass(cls):
        # Prepare a test file
        with open(cls.test_file_path, 'w') as f:
            f.write("## Header\n---\nBlock 1 content\n---\nBlock 2 content")

    @classmethod
    def tearDownClass(cls):
        # Cleanup test file
        os.remove(cls.test_file_path)

    @patch('general.llm.process_block_with_llm', return_value="Processed content")
    @patch('general.fileops.write_header_and_content_ffop', return_value='path/to/updated_file_summarized.md')
    def test_process_file_blocks__replace_mode(self, mock_write, mock_process):
        updated_file_path = process_file_blocks(self.test_file_path, "Please summarize this block.", 'replace', False, '_summarized')
        mock_write.assert_called_once()
        self.assertIn('_summarized', updated_file_path)

    @patch('general.llm.process_block_with_llm', side_effect=lambda block, _: "Processed " + block)
    @patch('general.fileops.write_header_and_content_ffop', return_value='path/to/updated_file_appended.md')
    def test_process_file_blocks__append_mode(self, mock_write, mock_process):
        new_file_path = process_file_blocks(self.test_file_path, "Please summarize this block.", 'append', False, '_appended')
        args, _ = mock_write.call_args
        self.assertTrue(mock_write.called)
        expected_file_path = 'path/to/updated_file_appended.md'
        self.assertEqual(new_file_path, expected_file_path)
        mock_process.assert_called()
        # This assumes your function joins processed blocks with "\n\n" or the original BLOCK_DELIMITER if retain_delimiters=True
        expected_content = "Block 1 content\nProcessed Block 1 content\n\nBlock 2 content\nProcessed Block 2 content"
        # Adjust as necessary if your function implementation details differ
        actual_content = args[2]  # Assuming the 'content' argument is the third positional argument
        self.assertIn(expected_content, actual_content)

    @patch('general.llm.process_block_with_llm', side_effect=lambda block, _: "Processed " + block)
    @patch('general.fileops.write_header_and_content_ffop', return_value='path/to/updated_file_delimiters.md')
    def test_process_file_blocks__retain_delimiters(self, mock_write, mock_process):
        new_file_path = process_file_blocks(self.test_file_path, "Please summarize this block.", 'replace', True, '_delimiters')
        args, _ = mock_write.call_args
        self.assertTrue(mock_write.called)
        expected_file_path = 'path/to/updated_file_delimiters.md'
        self.assertEqual(new_file_path, expected_file_path)
        mock_process.assert_called()
        # This assumes your function joins processed blocks with the original BLOCK_DELIMITER
        expected_content = "## Header\n---\nProcessed Block 1 content\n---\nProcessed Block 2 content"
        # Adjust as necessary if your function implementation details differ
        actual_content = args[2]  # Assuming the 'content' argument is the third positional argument
        self.assertIn(expected_content, actual_content)

class TestScallReplaceFFop(unittest.TestCase):
    test_file_path = 'test_scall_replace_ffop.md'

    @classmethod
    def setUpClass(cls):
        # Prepare a test file with known content
        with open(cls.test_file_path, 'w') as f:
            f.write("## Header\n---\nBlock 1 content\n---\nBlock 2 content")

    @classmethod
    def tearDownClass(cls):
        # Cleanup test file
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)
    
    @patch('general.llm.process_block_with_llm', return_value="Processed content")
    @patch('general.fileops.write_header_and_content_ffop', return_value='path/to/updated_file_scall-replace.md')
    def test_scall_replace_ffop__replace_mode_without_delimiters(self, mock_write, mock_process):
        updated_file_path = scall_replace_ffop(self.test_file_path, "Please summarize this block.", retain_delimiters=False)
        mock_write.assert_called_once()
        self.assertTrue(updated_file_path.endswith('_scall-replace.md'))

    @patch('general.llm.process_block_with_llm', return_value="Processed content")
    @patch('general.fileops.write_header_and_content_ffop', return_value='path/to/updated_file_scall-replace_delimiters.md')
    def test_scall_replace_ffop__replace_mode_with_delimiters(self, mock_write, mock_process):
        updated_file_path = scall_replace_ffop(self.test_file_path, "Please summarize this block.", retain_delimiters=True)
        mock_write.assert_called_once()
        self.assertTrue(updated_file_path.endswith('_scall-replace_delimiters.md'))

class TestScallAppendFfop(unittest.TestCase):
    test_file_path = 'test_file_blocks_add.md'

    @classmethod
    def setUpClass(cls):
        # Prepare a test file
        with open(cls.test_file_path, 'w') as f:
            f.write("## Header\n---\nBlock 1 content\n---\nBlock 2 content")

    @classmethod
    def tearDownClass(cls):
        # Cleanup test file
        os.remove(cls.test_file_path)

    @patch('general.llm.process_block_with_llm', side_effect=lambda block, _: "Processed " + block)
    @patch('general.fileops.write_header_and_content_ffop', return_value='path/to/updated_file_scall-add.md')
    def test_scall_append_ffop__append_mode(self, mock_write, mock_process):
        new_file_path = scall_append_ffop(self.test_file_path, "Please summarize this block.", False, '_scall-add')
        args, _ = mock_write.call_args
        self.assertTrue(mock_write.called)
        expected_file_path = 'path/to/updated_file_scall-add.md'
        self.assertEqual(new_file_path, expected_file_path)
        mock_process.assert_called()
        expected_content = "## Header\nProcessed ## Header\n\nBlock 1 content\nProcessed Block 1 content\n\nBlock 2 content\nProcessed Block 2 content"
        actual_content = args[2]  # Assuming the 'content' argument is the third positional argument
        self.assertIn(expected_content, actual_content)

    @patch('general.llm.process_block_with_llm', side_effect=lambda block, _: "Processed " + block)
    @patch('general.fileops.write_header_and_content_ffop', return_value='path/to/updated_file_scall-delimiters.md')
    def test_scall_append_ffop__retain_delimiters(self, mock_write, mock_process):
        new_file_path = scall_append_ffop(self.test_file_path, "Please summarize this block.", True, '_scall-delimiters')
        args, _ = mock_write.call_args
        self.assertTrue(mock_write.called)
        expected_file_path = 'path/to/updated_file_scall-delimiters.md'
        self.assertEqual(new_file_path, expected_file_path)
        mock_process.assert_called()
        expected_content = "## Header\nProcessed ## Header\n---\nBlock 1 content\nProcessed Block 1 content\n---\nBlock 2 content\nProcessed Block 2 content"
        actual_content = args[2]  # Assuming the 'content' argument is the third positional argument
        self.assertIn(expected_content, actual_content)


### LLM FUNCTION CALLING FUNCTIONS
class TestOpenAiFunctionCall(unittest.TestCase):
    @patch('general.llm.openai_chat_completion_request')
    def test_openai_function_call__successful_response(self, mock_chat_completion_request):
        # Create a mock response object
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': "This is the simulated assistant's message based on the prompt and content."
            }]
        }
        
        mock_chat_completion_request.return_value = mock_response

        # Assuming openai_function_call is correctly implemented
        assistant_message = openai_function_call("System prompt", "User content", [])

        # Assert that the response is as expected
        expected_message = "This is the simulated assistant's message based on the prompt and content."
        self.assertEqual(assistant_message, expected_message)



### LLM APPLICATION FUNCTIONS
#### QA
@unittest.skip("Temporarily disabled for faster test runs")
class TestCreateQa(unittest.TestCase):
    def setUp(self):
        # Setup method to find the given test file
        self.test_filepath = "tests/test_manual_files/llm_test_files/create_qa_test_files/1900-01-01_Test file for do qa_prepqa.md"
        self.ref_filepath = "tests/test_manual_files/llm_test_files/create_qa_test_files/1900-01-01_Test file for do qa_prepqa_qaREF.md"

    def tearDown(self):
        # Teardown method to remove the QA file after each test case
        qa_filepath = self.test_filepath.replace('.md', '_qa.md')
        if os.path.exists(qa_filepath):
            os.remove(qa_filepath)

    def test_create_qa_file(self):
        # Test creating QA from the markdown file
        qa_filepath = create_qa_file(self.test_filepath, "David Deutsch")
        self.assertTrue(os.path.exists(qa_filepath))

        with open(qa_filepath, 'r') as qa_file, open(self.ref_filepath, 'r') as ref_file:
            qa_lines = qa_file.readlines()
            ref_lines = ref_file.readlines()
            self.assertEqual(len(qa_lines), len(ref_lines))

            for qa_line, ref_line in zip(qa_lines, ref_lines):
                # Skip comparison for lines that start with 'last updated:' or 'QUESTION'
                if qa_line.startswith('last updated:') or qa_line.startswith('QUESTION'):
                    continue
                self.assertEqual(qa_line, ref_line)

#### COPYEDIT

# AssertionError: 'Returned' != 'Expected'

if __name__ == '__main__':
    unittest.main()