# Run tests with python -m unittest discover -s tests

import os
import sys
# Add the parent directory to the Python path so we can import the 'general' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tempfile
import unittest
from unittest.mock import patch, mock_open, MagicMock, call
import calendar

from general.fileops import *

print_get_timestamp_flag = False

### INITIAL FUNCTIONS CALLED BY FLEX FILE OP AND FOLDER FUNCTIONS
class TestVerbosePrint(unittest.TestCase):  # mocks print
    @patch('builtins.print')
    def test_verbose_print__prints_single_correctly(self, mock_print):
        # Test that verbose_print prints the correct messages when verbose is True
        verbose_print(True, "Test single message")
        mock_print.assert_called_once_with("Test single message")

    @patch('builtins.print')
    def test_verbose_print__prints_multiple_correctly(self, mock_print):
        # Test that verbose_print prints the correct messages when verbose is True
        verbose_print(True, "Test message", "with multiple arguments")
        mock_print.assert_called_once_with("Test message", "with multiple arguments")

    @patch("builtins.print")
    def test_verbose_print__verbose_true_prints_messages(self, mock_print):
        verbose = True
        messages = ("This", "is", "a", "test.")
        verbose_print(verbose, *messages)
        
        # Verify that print was called with the messages when verbose is True
        mock_print.assert_called_once_with(*messages)

    @patch("builtins.print")
    def test_verbose_print__verbose_false_does_not_print(self, mock_print):
        verbose = False
        messages = ("This", "is", "a", "test.")
        verbose_print(verbose, *messages)
        
        # Verify that print was not called when verbose is False
        mock_print.assert_not_called()

class TestCheckFileExists(unittest.TestCase):  # no mock
    def test_check_file_exists__file_exists(self):
        # Create a temporary file
        with tempfile.NamedTemporaryFile() as temp_file:
            file_path = temp_file.name
            operation_name = "Test Operation"
            # Test should pass without raising an exception
            try:
                check_file_exists(file_path, operation_name)
            except ValueError:
                self.fail("check_file_exists raised ValueError unexpectedly!")

    def test_check_file_exists__file_does_not_exist_raises_value_error(self):
        file_path = "/path/to/nonexistent_file.txt"
        operation_name = "Test Operation"
        # Test should raise a ValueError
        with self.assertRaises(ValueError) as context:
            check_file_exists(file_path, operation_name)
        
        expected_error_message = f"VALUE ERROR in {operation_name}: input file does not exist for {file_path}"
        self.assertEqual(str(context.exception), expected_error_message)

class TestMOCKCheckFileExists(unittest.TestCase):  # mocks isfile
    @patch('os.path.isfile', return_value=True)
    def test_check_file_exists__file_exists(self, mock_isfile):
        file_path = "/path/to/existing_file.txt"
        operation_name = "Test Operation"
        # Test should pass without raising an exception
        try:
            check_file_exists(file_path, operation_name)
        except ValueError:
            self.fail("check_file_exists raised ValueError unexpectedly!")

    @patch('os.path.isfile', return_value=False)
    def test_check_file_exists__file_does_not_exist_raises_value_error(self, mock_isfile):
        file_path = "/path/to/nonexistent_file.txt"
        operation_name = "Test Operation"
        # Test should raise a ValueError
        with self.assertRaises(ValueError) as context:
            check_file_exists(file_path, operation_name)
        expected_error_message = f"VALUE ERROR in {operation_name}: input file does not exist for {file_path}"
        self.assertEqual(str(context.exception), expected_error_message)

class TestGetSuffix(unittest.TestCase):  # no mock
    def test_get_suffix__with_single_period(self):
        self.assertEqual(get_suffix("filename_v1.txt", "_"), "_v1")

    def test_get_suffix__with_no_period(self):
        self.assertEqual(get_suffix("filename_v1", "_"), "_v1")

    def test_get_suffix__with_multiple_periods(self):
        with self.assertRaises(ValueError):
            get_suffix("filename_v1.backup.txt", "_")

    def test_get_suffix__with_no_delimiter(self):
        self.assertIsNone(get_suffix("filename.txt", "_"))

    def test_get_suffix__with_space_in_suffix(self):
        self.assertIsNone(get_suffix("filename_v 1.txt", "_"))

    def test_get_suffix__with_no_extension(self):
        self.assertEqual(get_suffix("filename_v1", "_"), "_v1")

    def test_get_suffix__with_period_in_path(self):
        self.assertEqual(get_suffix("path.to/filename_v1.txt", "_"), "_v1")

    def test_get_suffix__with_multiple_delimiters(self):
        self.assertEqual(get_suffix("filename__v1.txt", "_"), "_v1")

    def test_get_suffix__with_delimiter_at_end(self):
        self.assertEqual(get_suffix("filename_.txt", "_"), "_")

    def test_get_suffix__with_period_and_space_in_suffix(self):
        with self.assertRaises(ValueError):
            get_suffix("data/test file string with a extra .period_vrb.md", "_")

    def test_get_suffix__with_space_in_filename(self):
        self.assertIsNone(get_suffix("data/test file string_with space.md", "_"))

    def test_get_suffix__with_suffix_containing_dash(self):
        self.assertEqual(get_suffix("data/test file string_vrb-dq.md", "_"), "_vrb-dq")

    def test_get_suffix__with_suffix_containing_at_symbol(self):
        with self.assertRaises(ValueError):
            get_suffix("data/2024-03-02_test file string_vrb@dq.md", "_")

    def test_get_suffix__with_date_in_filename(self):
        self.assertIsNone(get_suffix("data/2024-03-02_test.md", "_"))

    def test_get_suffix__with_underscore_at_end_of_filename(self):
        self.assertEqual(get_suffix("tests/test file string_", "_"), "_")

class TestSubSuffixInString(unittest.TestCase):  # need further testing of different delimters
    def test_sub_suffix_in_str__existing_suffix(self):
        # Test replacing existing suffix
        self.assertEqual(sub_suffix_in_str("0_document file_v1.txt", "_v2"), "0_document file_v2.txt")

    def test_sub_suffix_in_str__no_existing_suffix(self):
        # Test replacing suffix when there is no existing suffix
        self.assertEqual(sub_suffix_in_str("0_document file.txt", "_v2"), "0_document file_v2.txt")

    def test_sub_suffix_in_str__no_extension(self):
        # Test with no extension
        self.assertEqual(sub_suffix_in_str("0_document file", "_v2"), "0_document file_v2")

    def test_sub_suffix_in_str__no_suffix_no_extension(self):
        # Test with no suffix and no extension, using a delimiter
        self.assertEqual(sub_suffix_in_str("0_document file", "_v2", delimiter="-"), "0_document file_v2")

    def test_sub_suffix_in_str__same_suffix(self):
        # Test with the same suffix as the substitution
        self.assertEqual(sub_suffix_in_str("2099-01-01_Test file_same.md", "_same", delimiter="_"), "2099-01-01_Test file_same.md")

class TestAddSuffixInString(unittest.TestCase):  # no mock
    def test_add_suffix_in_str__with_extension(self):
        # Test adding suffix to file with extension
        self.assertEqual(add_suffix_in_str("document.txt", "_new"), "document_new.txt")

    def test_add_suffix_in_str__no_extension(self):
        # Test adding suffix to file without extension
        self.assertEqual(add_suffix_in_str("document", "_new"), "document_new")

    def test_add_suffix_in_str__different_delimiter(self):
        # Test adding suffix with different delimiter
        self.assertEqual(add_suffix_in_str("document.txt", "-new"), "document-new.txt")

    def test_add_suffix_in_str__same_suffix_present(self):
        # Test adding a suffix that is already present in the file name
        self.assertEqual(add_suffix_in_str("2099-01-01_Test file_same.md", "_same"), "2099-01-01_Test file_same_same.md")

class TestRemoveAllSuffixesInStr(unittest.TestCase):
    def test_remove_all_suffixes_in_str__multiple_suffixes(self):
        file_str = "2024-03-12_Title with a space_suf1_suf2.md"
        expected_result = "2024-03-12_Title with a space.md"
        self.assertEqual(remove_all_suffixes_in_str(file_str), expected_result)

    def test_remove_all_suffixes_in_str__single_suffix(self):
        file_str = "filename_suffix.txt"
        expected_result = "filename.txt"
        self.assertEqual(remove_all_suffixes_in_str(file_str), expected_result)

    def test_remove_all_suffixes_in_str__no_suffix(self):
        file_str = "filename.txt"
        expected_result = "filename.txt"
        self.assertEqual(remove_all_suffixes_in_str(file_str), expected_result)

    def test_remove_all_suffixes_in_str__custom_delimiter(self):
        file_str = "filename-suffix1-suffix2.txt"
        expected_result = "filename.txt"
        self.assertEqual(remove_all_suffixes_in_str(file_str, delimiter="-"), expected_result)


class TestMOCKHandleOverwritePrompt(unittest.TestCase):  # mocks rename, remove, input and user functions verbose, check_file_exists
    @patch('os.rename')
    @patch('os.remove')
    @patch('general.fileops.verbose_print')
    @patch('general.fileops.check_file_exists')
    @patch('builtins.input', side_effect=['y'])
    def testmock_handle_overwrite_prompt__overwrite_yes(self, mock_input, mock_check, mock_verbose_print, mock_remove, mock_rename):
        file_path = "/path/to/original_file.txt"
        file_path_opfunc = "/path/to/new_file.txt"

        result = handle_overwrite_prompt(file_path, file_path_opfunc)

        self.assertEqual(result, file_path)
        mock_check.assert_any_call(file_path, "handle_overwrite_prompt - original file")
        mock_check.assert_any_call(file_path_opfunc, "handle_overwrite_prompt - new file")
        mock_remove.assert_called_once_with(file_path)
        mock_rename.assert_called_once_with(file_path_opfunc, file_path)
        mock_verbose_print.assert_called_once_with(True, "File operation with overwrite=prompt+yes - overwrite original file.")

    @patch('os.rename')
    @patch('os.remove')
    @patch('general.fileops.verbose_print')
    @patch('general.fileops.check_file_exists')
    @patch('builtins.input', side_effect=['n'])
    def testmock_handle_overwrite_prompt__overwrite_no(self, mock_input, mock_check, mock_verbose_print, mock_remove, mock_rename):
        file_path = "/path/to/original_file.txt"
        file_path_opfunc = "/path/to/new_file.txt"

        result = handle_overwrite_prompt(file_path, file_path_opfunc)

        self.assertEqual(result, file_path_opfunc)
        mock_check.assert_any_call(file_path, "handle_overwrite_prompt - original file")
        mock_check.assert_any_call(file_path_opfunc, "handle_overwrite_prompt - new file")
        mock_remove.assert_not_called()
        mock_rename.assert_not_called()
        mock_verbose_print.assert_called_once_with(True, "File operation with overwrite=prompt+no - keep original file and new file.")

    @patch('os.path.basename', return_value="original_file.txt")
    @patch('general.fileops.sub_suffix_in_str', return_value="/path/to/original_file_newsuffix.txt")
    @patch('general.fileops.get_suffix', return_value="_newsuffix")
    @patch('os.rename')
    @patch('general.fileops.verbose_print')
    @patch('general.fileops.check_file_exists')
    @patch('builtins.input', side_effect=['s'])
    def testmock_handle_overwrite_prompt__overwrite_sub(self, mock_input, mock_check, mock_verbose_print, mock_rename, mock_get_suffix, mock_sub_suffix_in_str, mock_basename):
        file_path = "/path/to/original_file.txt"
        file_path_opfunc = "/path/to/original_file_newsuffix.txt"
        expected_substituted_path = "/path/to/original_file_newsuffix.txt"

        result = handle_overwrite_prompt(file_path, file_path_opfunc)

        self.assertEqual(result, expected_substituted_path)
        mock_check.assert_any_call(file_path, "handle_overwrite_prompt - original file")
        mock_check.assert_any_call(file_path_opfunc, "handle_overwrite_prompt - new file")
        mock_rename.assert_called_once_with(file_path_opfunc, expected_substituted_path)
        mock_verbose_print.assert_called_once_with(True, "File operation with overwrite=prompt+sub - keep original file and new file with substituted suffix.")

    @patch('os.rename')
    @patch('os.remove')
    @patch('general.fileops.verbose_print')
    @patch('general.fileops.check_file_exists')
    @patch('builtins.input', side_effect=['invalid', 'y'])
    def testmock_handle_overwrite_prompt__invalid_input_then_overwrite(self, mock_input, mock_check, mock_verbose_print, mock_remove, mock_rename):
        file_path = "/path/to/original_file.txt"
        file_path_opfunc = "/path/to/new_file.txt"

        result = handle_overwrite_prompt(file_path, file_path_opfunc)

        self.assertEqual(result, file_path)
        mock_check.assert_any_call(file_path, "handle_overwrite_prompt - original file")
        mock_check.assert_any_call(file_path_opfunc, "handle_overwrite_prompt - new file")
        mock_remove.assert_called_once_with(file_path)
        mock_rename.assert_called_once_with(file_path_opfunc, file_path)
        mock_verbose_print.assert_called_once_with(True, "File operation with overwrite=prompt+yes - overwrite original file.")

class TestHandleOverwritePrompt(unittest.TestCase):  # mocks rename, remove, input
    def setUp(self):
        # Create temporary files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, "Test file_orig.txt")
        self.file_path_opfunc = os.path.join(self.temp_dir.name, "Test file_orig_new.txt")
        with open(self.file_path, 'w') as f:
            f.write("Original file content")
        with open(self.file_path_opfunc, 'w') as f:
            f.write("Modified file content")

    def tearDown(self):
        # Clean up temporary files
        self.temp_dir.cleanup()

    @patch('os.rename')
    @patch('os.remove')
    @patch('builtins.input', side_effect=['y'])
    def test_handle_overwrite_prompt__overwrite_yes(self, mock_input, mock_remove, mock_rename):
        result = handle_overwrite_prompt(self.file_path, self.file_path_opfunc)
        self.assertEqual(result, self.file_path)
        mock_remove.assert_called_once_with(self.file_path)
        mock_rename.assert_called_once_with(self.file_path_opfunc, self.file_path)

    @patch('os.rename')
    @patch('os.remove')
    @patch('builtins.input', side_effect=['n'])
    def test_handle_overwrite_prompt__overwrite_no(self, mock_input, mock_remove, mock_rename):
        result = handle_overwrite_prompt(self.file_path, self.file_path_opfunc)
        self.assertEqual(result, self.file_path_opfunc)
        mock_remove.assert_not_called()
        mock_rename.assert_not_called()

    @patch('os.rename')
    @patch('builtins.input', side_effect=['s'])
    def test_handle_overwrite_prompt__overwrite_sub(self, mock_input, mock_rename):
        expected_substituted_path = os.path.join(self.temp_dir.name, "Test file_new.txt")
        result = handle_overwrite_prompt(self.file_path, self.file_path_opfunc)
        self.assertEqual(result, expected_substituted_path)
        mock_rename.assert_called_once_with(self.file_path_opfunc, expected_substituted_path)

    @patch('os.rename')
    @patch('os.remove')
    @patch('builtins.input', side_effect=['invalid', 'y'])
    def test_handle_overwrite_prompt__invalid_input_then_overwrite(self, mock_input, mock_remove, mock_rename):
        result = handle_overwrite_prompt(self.file_path, self.file_path_opfunc)
        self.assertEqual(result, self.file_path)
        mock_remove.assert_called_once_with(self.file_path)
        mock_rename.assert_called_once_with(self.file_path_opfunc, self.file_path)

class TestCheckAndWarnFileOverwrite(unittest.TestCase):  # mocks isfile
    @patch('os.path.isfile', return_value=True)
    def test_check_and_warn_file_overwrite__file_exists(self, mock_isfile):
        file_path = "/path/to/existing_file.txt"
        with self.assertWarns(Warning) as warning:
            check_and_warn_file_overwrite(file_path)
        self.assertIn("overwriting a file that already exists", str(warning.warning))

    @patch('os.path.isfile', return_value=False)
    def test_check_and_warn_file_overwrite__file_does_not_exist(self, mock_isfile):
        file_path = "/path/to/non_existing_file.txt"
        with self.assertRaises(AssertionError):
            with self.assertWarns(Warning):
                check_and_warn_file_overwrite(file_path)

class TestAddTextAboveFfop(unittest.TestCase):  # no mock (except warning)
    def setUp(self):
        # Setup method to create a test file before each test case
        self.test_filename = 'test_file.txt'
        self.add_text = 'First line'
        with open(self.test_filename, 'w') as f:
            f.write('Second line\nThird line')

    def tearDown(self):
        # Teardown method to remove test files after each test case
        os.remove(self.test_filename)
        new_filename = self.test_filename.replace('.txt', '_addtextabove.txt')
        if os.path.exists(new_filename):
            os.remove(new_filename)

    def test_add_text_above_ffop__file_is_created_with_add_text(self):
        # Test that a new file is created with the specified add_text
        new_filename = add_text_above_ffop(self.test_filename, self.add_text)
        self.assertTrue(os.path.exists(new_filename))
        with open(new_filename, 'r') as f:
            content = f.readlines()
        self.assertEqual(content[0].strip(), self.add_text)

    def test_add_text_above_ffop__rest_of_content_is_unchanged(self):
        # Test that the rest of the content in the new file is unchanged
        new_filename = add_text_above_ffop(self.test_filename, self.add_text)
        with open(new_filename, 'r') as f:
            content = f.readlines()
        with open(self.test_filename, 'r') as original:
            original_content = original.readlines()
        self.assertEqual(content[1:], original_content)

    # decided not to raise ValueError and to just overwrite file and print WARNING to console, see 1-5 Cursor history and entry in Coding Log gdoc
    @patch('warnings.warn')
    def test_add_text_above_ffop__warning_raised_if_file_exists(self, mock_warn):
        # Test that a warning is raised if the new file already exists
        new_filename = add_text_above_ffop(self.test_filename, self.add_text)
        # Create the file again to trigger the warning
        add_text_above_ffop(self.test_filename, self.add_text)
        mock_warn.assert_called()
### FLEX FILE OP AND FOLDER FUNCTIONS
class TestDoFfop(unittest.TestCase):
    def setUp(self):
        self.filename = "test_orig.md"
        self.new_filename = "test_orig_addtextabove.md"
        self.add_text = "HERE"
        self.original_content = "Original content of the file."
        self.mock_file_content = self.add_text + '\n' + self.original_content

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.new_filename):
            os.remove(self.new_filename)

    def test_do_ffop__add_text_above_ffop_overwrite_no(self):
        with open(self.filename, 'w') as f:
            f.write(self.original_content)
        do_ffop(add_text_above_ffop, self.filename, self.add_text, overwrite="no", verbose=False)
        self.assertTrue(os.path.exists(self.new_filename))
        with open(self.new_filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.mock_file_content)

    def test_do_ffop__add_text_above_ffop_overwrite_no_sub(self):
        with open(self.filename, 'w') as f:
            f.write(self.original_content)
        new_filename_sub = self.filename.replace('_orig.md', '_addtextabove.md')
        do_ffop(add_text_above_ffop, self.filename, self.add_text, overwrite="no-sub", verbose=False)
        self.assertTrue(os.path.exists(new_filename_sub))
        with open(new_filename_sub, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.mock_file_content)

    def test_do_ffop__add_text_above_ffop_overwrite_replace(self):
        with open(self.filename, 'w') as f:
            f.write(self.original_content)
        result = do_ffop(add_text_above_ffop, self.filename, self.add_text, overwrite="replace", verbose=False)
        self.assertTrue(os.path.exists(self.new_filename))  # Check if the new file exists
        self.assertFalse(os.path.exists(self.filename))  # Check if the original file has been deleted
        with open(self.new_filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.mock_file_content)  # Check if the content is correct
        self.assertEqual(result, self.new_filename)  # Check if the function returns the correct new file path

    def test_do_ffop__add_text_above_ffop_overwrite_replace_sub(self):
        with open(self.filename, 'w') as f:
            f.write(self.original_content)
        new_filename_sub = self.filename.replace('_orig.md', '_addtextabove.md')
        do_ffop(add_text_above_ffop, self.filename, self.add_text, overwrite="replace-sub", verbose=False)
        self.assertTrue(os.path.exists(new_filename_sub))
        with open(new_filename_sub, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.mock_file_content)

    def test_do_ffop__add_text_above_ffop_overwrite_yes(self):
        with open(self.filename, 'w') as f:
            f.write(self.original_content)
        do_ffop(add_text_above_ffop, self.filename, self.add_text, overwrite="yes", verbose=False)
        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.mock_file_content)

    @patch('builtins.input', side_effect=['y'])
    def test_do_ffop__add_text_above_ffop_overwrite_prompt_yes(self, mock_input):
        with open(self.filename, 'w') as f:
            f.write(self.original_content)
        do_ffop(add_text_above_ffop, self.filename, self.add_text, overwrite="prompt", verbose=False)
        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.mock_file_content)

    @patch('builtins.input', side_effect=['n'])
    def test_do_ffop__add_text_above_ffop_overwrite_prompt_no(self, mock_input):
        with open(self.filename, 'w') as f:
            f.write(self.original_content)
        do_ffop(add_text_above_ffop, self.filename, self.add_text, overwrite="prompt", verbose=False)
        self.assertTrue(os.path.exists(self.new_filename))
        with open(self.new_filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.mock_file_content)

    @patch('builtins.input', side_effect=['s'])
    def test_do_ffop__add_text_above_ffop_overwrite_prompt_sub(self, mock_input):
        with open(self.filename, 'w') as f:
            f.write(self.original_content)
        new_filename_sub = self.filename.replace('_orig.md', '_addtextabove.md')
        do_ffop(add_text_above_ffop, self.filename, self.add_text, overwrite="prompt", verbose=False)
        self.assertTrue(os.path.exists(new_filename_sub))
        with open(new_filename_sub, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.mock_file_content)

    def test_add_text_above_ffop_functionality(self):
        with open(self.filename, 'w') as f:
            f.write(self.original_content)
        result = add_text_above_ffop(self.filename, self.add_text)
        self.assertTrue(os.path.exists(result))
        with open(result, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.mock_file_content)

    def test_do_ffop__error_propagation(self):
        # Create a mock ffop_func that raises an Exception
        ffop_func = MagicMock(side_effect=Exception("Test exception"))
        # Ensure the input file exists
        with open(self.filename, 'w') as f:
            f.write("Dummy content.")
        # Call do_ffop with the mock ffop_func
        with self.assertRaises(Exception) as context:
            do_ffop(ffop_func, self.filename, overwrite="yes", verbose=False)
        # Check that the exception message is as expected
        self.assertEqual(str(context.exception), "Test exception")

    def test_do_ffop__file_does_not_exist(self):
        with self.assertRaises(ValueError) as context:
            do_ffop(add_text_above_ffop, self.filename, self.add_text, overwrite="yes", verbose=False)
        self.assertIn('input file does not exist for test_orig.md', str(context.exception))

    def test_do_ffop__invalid_overwrite_argument(self):
        # Ensure the input file exists
        with open(self.filename, 'w') as f:
            f.write("Dummy content.")

        # Test do_ffop with an invalid overwrite argument, expecting a ValueError
        with self.assertRaises(ValueError) as context:
            do_ffop(add_text_above_ffop, self.filename, self.add_text, overwrite="x", verbose=False)
        self.assertIn("VALUE ERROR in do_ffop: invalid overwrite argument: 'x'. Valid options are: no, no-sub, replace, replace-sub, yes, prompt", str(context.exception))

class TestGetFilesInFolder(unittest.TestCase):  # no mock (except input)
    def setUp(self):
        # Create a temporary directory with files and a subfolder
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file1 = os.path.join(self.temp_dir.name, "file1.txt")
        self.file2 = os.path.join(self.temp_dir.name, "file2_prepqa.txt")
        self.subfolder = os.path.join(self.temp_dir.name, "subfolder")
        self.subfolder_file = os.path.join(self.subfolder, "file3.txt")
        os.mkdir(self.subfolder)
        with open(self.file1, 'w') as f:
            f.write("File 1 content")
        with open(self.file2, 'w') as f:
            f.write("File 2 content")
        with open(self.subfolder_file, 'w') as f:
            f.write("Subfolder file content")

    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_get_files_in_folder__all_files(self):
        result = get_files_in_folder(self.temp_dir.name)
        self.assertEqual(set(result), {self.file1, self.file2})

    def test_get_files_in_folder__suffix_include(self):
        result = get_files_in_folder(self.temp_dir.name, suffix_include="_prepqa")
        self.assertEqual(result, [self.file2])

    def test_get_files_in_folder__suffix_exclude(self):
        result = get_files_in_folder(self.temp_dir.name, suffix_exclude="_prepqa")
        self.assertEqual(result, [self.file1])

    def test_get_files_in_folder__include_subfolders(self):
        result = get_files_in_folder(self.temp_dir.name, include_subfolders=True)
        self.assertEqual(set(result), {self.file1, self.file2, self.subfolder_file})

    def test_get_files_in_folder__suffix_include_and_subfolders(self):
        result = get_files_in_folder(self.temp_dir.name, suffix_include="_prepqa", include_subfolders=True)
        self.assertEqual(result, [self.file2])

    def test_get_files_in_folder__nonexistent_folder(self):
        with self.assertRaises(ValueError):
            get_files_in_folder(os.path.join(self.temp_dir.name, "nonexistent_folder"))

    def test_get_files_in_folder__both_suffix_include_and_exclude(self):
        with self.assertRaises(ValueError):
            get_files_in_folder(self.temp_dir.name, suffix_include="_qatest", suffix_exclude="_prepqa")

class TestDoFfopOnFolder(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with files and a subfolder
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file1 = os.path.join(self.temp_dir.name, "file1.txt")
        self.file2 = os.path.join(self.temp_dir.name, "file2_prepqa.txt")
        self.subfolder = os.path.join(self.temp_dir.name, "subfolder")
        self.subfolder_file = os.path.join(self.subfolder, "file3.txt")
        os.mkdir(self.subfolder)
        with open(self.file1, 'w') as f:
            f.write("File 1 content")
        with open(self.file2, 'w') as f:
            f.write("File 2 content")
        with open(self.subfolder_file, 'w') as f:
            f.write("Subfolder file content")

        # Diagnostic printing
        print("Temporary directory contents:")
        for root, dirs, files in os.walk(self.temp_dir.name):
            print(f"Root: {root}")
            print(f"Directories: {dirs}")
            print(f"Files: {files}")

    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_do_ffop_on_folder__overwrite_no(self):
        do_ffop_on_folder(add_text_above_ffop, self.temp_dir.name, "HERE")
        new_file1 = os.path.splitext(self.file1)[0] + "_addtextabove.txt"
        new_file2 = os.path.splitext(self.file2)[0] + "_addtextabove.txt"
        with open(new_file1, 'r') as f:
            self.assertEqual(f.readline().strip(), "HERE")
        with open(new_file2, 'r') as f:
            self.assertEqual(f.readline().strip(), "HERE")

    def test_do_ffop_on_folder__overwrite_yes(self):
        do_ffop_on_folder(add_text_above_ffop, self.temp_dir.name, "HERE", overwrite="yes")
        # The original files should be replaced with new files with the added text
        with open(self.file1, 'r') as f:
            self.assertEqual(f.readline().strip(), "HERE")
        with open(self.file2, 'r') as f:
            self.assertEqual(f.readline().strip(), "HERE")

    def test_do_ffop_on_folder__suffix_include(self):
        do_ffop_on_folder(add_text_above_ffop, self.temp_dir.name, "HERE", suffix_include='_prepqa')
        new_file2 = os.path.splitext(self.file2)[0] + "_addtextabove.txt"
        with open(self.file1, 'r') as f:
            self.assertNotEqual(f.readline().strip(), "HERE")
        with open(new_file2, 'r') as f:
            self.assertEqual(f.readline().strip(), "HERE")

    def test_do_ffop_on_folder__suffix_exclude(self):
        do_ffop_on_folder(add_text_above_ffop, self.temp_dir.name, "HERE", suffix_exclude='_prepqa')
        new_file1 = os.path.splitext(self.file1)[0] + "_addtextabove.txt"
        with open(new_file1, 'r') as f:
            self.assertEqual(f.readline().strip(), "HERE")
        with open(self.file2, 'r') as f:
            self.assertNotEqual(f.readline().strip(), "HERE")

    def test_do_ffop_on_folder__both_suffix_include_and_exclude(self):
        with self.assertRaises(ValueError):
            do_ffop_on_folder(add_text_above_ffop, self.temp_dir.name, "HERE", suffix_include='_prepqa', suffix_exclude='_prepqa')

    def test_do_ffop_on_folder__include_subfolders(self):
        do_ffop_on_folder(add_text_above_ffop, self.temp_dir.name, "HERE", include_subfolders=True)
        new_subfolder_file = os.path.splitext(self.subfolder_file)[0] + "_addtextabove.txt"
        with open(new_subfolder_file, 'r') as f:
            self.assertEqual(f.readline().strip(), "HERE")

    def test_do_ffop_on_folder__processed_files_count_subfolder_false(self):
        processed_files_count = do_ffop_on_folder(add_text_above_ffop, self.temp_dir.name, "HERE", include_subfolders=False)
        self.assertEqual(processed_files_count, 2)  # Expecting 2 files to be processed, excluding subfolder

    def test_do_ffop_on_folder__processed_files_count_subfolder_true(self):
        processed_files_count = do_ffop_on_folder(add_text_above_ffop, self.temp_dir.name, "HERE", include_subfolders=True)
        self.assertEqual(processed_files_count, 3)  # Expecting 3 files to be processed, including subfolder

    def test_do_ffop_on_folder__processed_files_count_include(self):
        processed_files_count = do_ffop_on_folder(add_text_above_ffop, self.temp_dir.name, "HERE", suffix_include='_prepqa')
        self.assertEqual(processed_files_count, 1)  # Expecting 1 file to be processed with the suffix

    def test_do_ffop_on_folder__processed_files_count_exclude(self):
        processed_files_count = do_ffop_on_folder(add_text_above_ffop, self.temp_dir.name, "HERE", suffix_exclude='_prepqa')
        self.assertEqual(processed_files_count, 1)  # Expecting 1 file to be processed without the suffix

def mock_function(file_path, *args, **kwargs):
    return f"Processed {os.path.basename(file_path)}"
class TestAnyFuncOnFolder(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with files and a subfolder
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file1 = os.path.join(self.temp_dir.name, "file1.txt")
        self.file2 = os.path.join(self.temp_dir.name, "file2_prepqa.txt")
        self.subfolder = os.path.join(self.temp_dir.name, "subfolder")
        self.subfolder_file = os.path.join(self.subfolder, "file3.txt")
        os.mkdir(self.subfolder)
        with open(self.file1, 'w') as f:
            f.write("File 1 content")
        with open(self.file2, 'w') as f:
            f.write("File 2 content")
        with open(self.subfolder_file, 'w') as f:
            f.write("Subfolder file content")

    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_any_func_on_folder__no_suffix(self):
        results = any_func_on_folder(mock_function, self.temp_dir.name)
        expected_results = {
            self.file1: "Processed file1.txt",
            self.file2: "Processed file2_prepqa.txt"
        }
        self.assertEqual(results, expected_results)

    def test_any_func_on_folder__suffix_include(self):
        results = any_func_on_folder(mock_function, self.temp_dir.name, suffix_include='_prepqa')
        expected_results = {
            self.file2: "Processed file2_prepqa.txt"
        }
        self.assertEqual(results, expected_results)

    def test_any_func_on_folder__suffix_exclude(self):
        results = any_func_on_folder(mock_function, self.temp_dir.name, suffix_exclude='_prepqa')
        expected_results = {
            self.file1: "Processed file1.txt"
        }
        self.assertEqual(results, expected_results)

    def test_any_func_on_folder__include_subfolders(self):
        results = any_func_on_folder(mock_function, self.temp_dir.name, include_subfolders=True)
        expected_results = {
            self.file1: "Processed file1.txt",
            self.file2: "Processed file2_prepqa.txt",
            self.subfolder_file: "Processed file3.txt"
        }
        self.assertEqual(results, expected_results)

    def test_any_func_on_folder__suffix_include_and_exclude(self):
        with self.assertRaises(ValueError):
            any_func_on_folder(mock_function, self.temp_dir.name, suffix_include='_prepqa', suffix_exclude='_prepqa')


### TIME AND TIMESTAMP SUPPORT FUNCTIONS
class TestConvertSecondsToTimestamp(unittest.TestCase):
    def test_convert_seconds_to_timestamp__returns_correct_format_for_hours_minutes_seconds(self):
        # Testing for a time that includes hours, minutes, and seconds
        self.assertEqual(convert_seconds_to_timestamp(3665), "1:01:05")

    def test_convert_seconds_to_timestamp__returns_correct_format_for_minutes_seconds(self):
        # Testing for a time that includes minutes and seconds but no hours
        self.assertEqual(convert_seconds_to_timestamp(65), "1:05")

    def test_convert_seconds_to_timestamp__returns_correct_format_for_seconds_only(self):
        # Testing for a time that includes seconds only
        self.assertEqual(convert_seconds_to_timestamp(45), "0:45")

    def test_convert_seconds_to_timestamp__edge_case_of_zero_seconds(self):
        # Edge case: Exactly 0 seconds
        self.assertEqual(convert_seconds_to_timestamp(0), "0:00")

    def test_convert_seconds_to_timestamp__edge_case_of_exactly_one_hour(self):
        # Edge case: Exactly one hour
        self.assertEqual(convert_seconds_to_timestamp(3600), "1:00:00")

    def test_convert_seconds_to_timestamp__edge_case_of_exactly_one_minute(self):
        # Edge case: Exactly one minute
        self.assertEqual(convert_seconds_to_timestamp(60), "1:00")

    def test_convert_seconds_to_timestamp__value_error_raised_for_negative_input(self):
        # Testing for ValueError on negative input (invalid input scenario)
        with self.assertRaises(ValueError):
            convert_seconds_to_timestamp(-1)

    def test_convert_seconds_to_timestamp__value_error_raised_for_non_integer_input(self):
        # Testing for ValueError on non-integer input
        with self.assertRaises(TypeError):
            convert_seconds_to_timestamp("a string")

class TestConvertTimestampToSeconds(unittest.TestCase):
    def test_convert_timestamp_to_seconds__correct_conversion_hh_mm_ss(self):
        # Testing correct conversion from hh:mm:ss to total seconds
        self.assertEqual(convert_timestamp_to_seconds("01:02:03"), 3723)

    def test_convert_timestamp_to_seconds__correct_conversion_mm_ss(self):
        # Testing correct conversion from mm:ss to total seconds
        self.assertEqual(convert_timestamp_to_seconds("02:03"), 123)

    def test_convert_timestamp_to_seconds__non_string_input_raises_type_error(self):
        # Testing that non-string input raises TypeError
        with self.assertRaises(TypeError):
            convert_timestamp_to_seconds(123)

    def test_convert_timestamp_to_seconds__invalid_format_raises_value_error(self):
        # Testing that an invalid format raises ValueError
        with self.assertRaises(ValueError):
            convert_timestamp_to_seconds("01:02:03:04")

    def test_convert_timestamp_to_seconds__non_numeric_characters_raise_value_error(self):
        # Testing that non-numeric characters in the input raise ValueError
        with self.assertRaises(ValueError):
            convert_timestamp_to_seconds("01:xx:03")

    def test_convert_timestamp_to_seconds__out_of_range_hours_raises_value_error(self):
        # Testing that hours out of valid range raise ValueError
        with self.assertRaises(ValueError):
            convert_timestamp_to_seconds("100:00:00")

    def test_convert_timestamp_to_seconds__out_of_range_minutes_raises_value_error(self):
        # Testing that minutes out of valid range raise ValueError
        with self.assertRaises(ValueError):
            convert_timestamp_to_seconds("00:60:00")

    def test_convert_timestamp_to_seconds__out_of_range_seconds_raises_value_error(self):
        # Testing that seconds out of valid range raise ValueError
        with self.assertRaises(ValueError):
            convert_timestamp_to_seconds("00:00:60")

class TestChangeTimestamp(unittest.TestCase):
    def test_change_timestamp__increases_timestamp_correctly(self):
        # Test increasing a timestamp successfully
        self.assertEqual(change_timestamp("01:01:01", 3661), "2:02:02")

    def test_change_timestamp__decreases_timestamp_correctly(self):
        # Test decreasing a timestamp successfully
        self.assertEqual(change_timestamp("02:02:02", -3661), "1:01:01")

    def test_change_timestamp__handles_zero_delta_seconds(self):
        # Test that timestamp remains unchanged with delta_seconds = 0
        self.assertEqual(change_timestamp("01:00:00", 0), "1:00:00")

    def test_change_timestamp__none_input_raises_value_error(self):
        # Test that None timestamp input raises ValueError
        with self.assertRaises(ValueError):
            change_timestamp(None, 60)

    def test_change_timestamp__negative_raises_value_error(self):
        # Test that negative modified seconds raises ValueError
        with self.assertRaises(ValueError):
            change_timestamp("00:00:01", -2)

    def test_change_timestamp__large_positive_delta_rolls_over_days(self):
        # Test a large delta that rolls over multiple days
        # Assuming the output format is always "hh:mm:ss" even for values exceeding 24 hours
        self.assertEqual(change_timestamp("00:00:00", 86400 + 3661), "25:01:01")

class TestTuneTimestamp(unittest.TestCase):
    def test_tune_timestamp__correct_format_conversion(self):
        # Test that the timestamp is correctly "tuned" or normalized
        self.assertEqual(tune_timestamp("01:02:03"), "1:02:03")

    def test_tune_timestamp__handles_leading_zeros(self):
        # Test that leading zeros are handled correctly, assuming they are removed in the tuning process
        self.assertEqual(tune_timestamp("01:00:00"), "1:00:00")

    def test_tune_timestamp__handles_none_input(self):
        # Test that None input is handled by returning None
        self.assertIsNone(tune_timestamp(None))

    def test_tune_timestamp__input_output_equality_for_valid_timestamps(self):
        # Test that valid timestamps are returned unchanged, assuming the tuning process does not alter already correct timestamps
        self.assertEqual(tune_timestamp("12:34:56"), "12:34:56")

    def test_tune_timestamp__adjusts_minute_and_second_format(self):
        # Test that minutes and seconds are always returned with two digits, assuming this is part of the tuning
        self.assertEqual(tune_timestamp("0:2:9"), "2:09")

class TestGetTimestamp(unittest.TestCase):

    def test_get_timestamp__with_valid_timestamp(self):
        line = "David Deutsch  [3:18](https://www.youtube.com/dummylink&t=198)  SKIPQA"
        expected_timestamp = "3:18"
        expected_index = 15
        if print_get_timestamp_flag:
            print_chars_with_indices(line,25)
        timestamp, index = get_timestamp(line, print_line=print_get_timestamp_flag)
        self.assertEqual(timestamp, expected_timestamp)
        self.assertEqual(index, expected_index)

    def test_get_timestamp__with_invalid_timestamp(self):
        line = "Bob McBobbin  99:99:99 should not be accepted."
        with self.assertRaises(ValueError):
            get_timestamp(line)

    def test_get_timestamp__with_timestamp_without_hours(self):
        line = "Quick example [12:34] with no hours."
        expected_timestamp = "12:34"
        expected_index = 14
        if print_get_timestamp_flag:
            print_chars_with_indices(line,25)
        timestamp, index = get_timestamp(line, print_line=print_get_timestamp_flag)
        self.assertEqual(timestamp, expected_timestamp)
        self.assertEqual(index, expected_index)

    def test_get_timestamp__with_line_with_excessive_words_around_timestamp(self):
        line = "This is a line with a lot of words before the timestamp [1:23:45] and also a lot of words after the timestamp."
        expected_timestamp = None
        expected_index = None
        if print_get_timestamp_flag:
            print_chars_with_indices(line,60)
        timestamp, index = get_timestamp(line, print_line=print_get_timestamp_flag)
        self.assertEqual(timestamp, expected_timestamp)
        self.assertEqual(index, expected_index)

    def test_get_timestamp__with_line_with_no_timestamp(self):
        line = "This line does not contain a timestamp at all."
        expected_timestamp = None
        expected_index = None
        if print_get_timestamp_flag:
            print_chars_with_indices(line,25)
        timestamp, index = get_timestamp(line, print_line=print_get_timestamp_flag)
        self.assertEqual(timestamp, expected_timestamp)
        self.assertEqual(index, expected_index)

    def test_get_timestamp__with_line_with_timestamp_and_no_link(self):
        line = "Here is a timestamp 2:34 without a link."
        expected_timestamp = "2:34"
        expected_index = 20
        if print_get_timestamp_flag:
            print_chars_with_indices(line,25)
        timestamp, index = get_timestamp(line, print_line=print_get_timestamp_flag)
        self.assertEqual(timestamp, expected_timestamp)
        self.assertEqual(index, expected_index)

    def test_get_timestamp__with_line_with_timestamp_and_link(self):
        line = "Timestamp with link [5:27](https://www.example.com) should be found."
        expected_timestamp = "5:27"
        expected_index = 20
        if print_get_timestamp_flag:
            print_chars_with_indices(line,25)
        timestamp, index = get_timestamp(line, print_line=print_get_timestamp_flag)
        self.assertEqual(timestamp, expected_timestamp)
        self.assertEqual(index, expected_index)

class TestGetCurrentTime(unittest.TestCase):
    def test_get_current_time__default_timezone(self):
        result = get_current_time()
        expected_timezones = ['PST', 'PDT']  # Pacific Standard Time or Pacific Daylight Time
        self.assertTrue(any(tz in result for tz in expected_timezones))

    def test_get_current_time__specific_timezone(self):
        result = get_current_time(timezone='UTC')
        expected_timezone = 'UTC'
        self.assertIn(expected_timezone, result)

    def test_get_current_time__format(self):
        result = get_current_time()
        try:
            datetime.strptime(result, '%Y-%m-%d %H:%M:%S %Z')
            format_valid = True
        except ValueError:
            format_valid = False
        self.assertTrue(format_valid)

class TestConvertToEpochSeconds(unittest.TestCase):
    def test_convert_to_epoch_seconds__full_datetime(self):
        result = convert_to_epoch_seconds("2024-03-07 06:52:18", timezone='UTC')
        expected = time.mktime(time.strptime("2024-03-07 06:52:18", "%Y-%m-%d %H:%M:%S"))
        expected -= time.timezone  # Adjust for local timezone
        self.assertEqual(result, expected)

    def test_convert_to_epoch_seconds__only_time(self):
        # Get the current date in UTC timezone
        current_date_utc = datetime.now(pytz.timezone('UTC')).strftime("%Y-%m-%d")
        # Test conversion of only time (HH:MM:SS) to epoch seconds
        result = convert_to_epoch_seconds("06:52:18", timezone='UTC')
        # Expected epoch seconds for the current date with the given time in UTC timezone
        # Adjust for the UTC timezone explicitly instead of using local timezone
        expected = calendar.timegm(time.strptime(f"{current_date_utc} 06:52:18", "%Y-%m-%d %H:%M:%S"))
        self.assertAlmostEqual(result, expected, delta=60)  # Allowing a 1-minute margin for potential delay

    def test_convert_to_epoch_seconds__12_hour_clock(self):
        result = convert_to_epoch_seconds("2024-03-07 06:52:18AM", timezone='UTC')
        expected = time.mktime(time.strptime("2024-03-07 06:52:18", "%Y-%m-%d %H:%M:%S"))
        expected -= time.timezone  # Adjust for local timezone
        self.assertEqual(result, expected)

    def test_convert_to_epoch_seconds__only_time_12_hour_clock(self):
        current_date = datetime.now(pytz.timezone('UTC')).strftime("%Y-%m-%d")
        result = convert_to_epoch_seconds(f"{current_date} 06:52:18AM", timezone='UTC')
        expected = time.mktime(time.strptime(f"{current_date} 06:52:18AM", "%Y-%m-%d %I:%M:%S%p"))
        expected = pytz.timezone('UTC').localize(datetime.fromtimestamp(expected)).timestamp()
        self.assertAlmostEqual(result, expected, delta=60)  # Allowing a 1-minute margin for potential delay

    def test_convert_to_epoch_seconds__with_invalid_format(self):
        with self.assertRaises(ValueError):
            convert_to_epoch_seconds("invalid format", timezone='UTC')

class TestGetElapsedSeconds(unittest.TestCase):
    def test_get_elapsed_seconds__valid(self):
        start_time = time.time() - 90  # 1.5 minutes ago
        elapsed_time = get_elapsed_seconds(start_time)
        self.assertEqual(elapsed_time, 90)

    def test_get_elapsed_time__invalid_input(self):
        start_time = "invalid input"
        with self.assertRaises(TypeError):
            get_elapsed_seconds(start_time)


### READ FUNCTIONS
class TestReadCompleteTextFromFile(unittest.TestCase):
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="File content")
    def test_read_complete_text_from_file__returns_file_content(self, mock_file, mock_exists):
        file_path = "/path/to/file.txt"
        self.assertEqual(read_complete_text_from_file(file_path), "File content")

    @patch('os.path.exists', return_value=False)
    def test_read_complete_text_from_file__raises_value_error_for_nonexistent_path(self, mock_exists):
        file_path = "/nonexistent/path/to/file.txt"
        with self.assertRaises(ValueError):
            read_complete_text_from_file(file_path)

class TestSplitHeaderAndContent(unittest.TestCase):
    def test_split_header_and_content__with_delimiter(self):
        # Test with a delimiter present in the text
        text = "Header info\n## content\nContent starts here\n\n\n"
        delimiter = "## content"
        expected_header = "Header info\n## content\n\n"
        expected_content = "Content starts here\n\n\n"
        header, content = split_header_and_content(text, delimiter)
        self.assertEqual(header, expected_header)
        self.assertEqual(content, expected_content)

    def test_split_header_and_content__without_delimiter(self):
        # Test without a delimiter present in the text
        text = "No delimiter here\nContent continues"
        delimiter = "## content"
        expected_header = ""
        expected_content = text  # Entire text should be treated as content
        header, content = split_header_and_content(text, delimiter)
        self.assertEqual(header, expected_header)
        self.assertEqual(content, expected_content)

    def test_split_header_and_content__empty_text(self):
        # Test with an empty string
        text = ""
        delimiter = "## content"
        expected_header = ""
        expected_content = ""
        header, content = split_header_and_content(text, delimiter)
        self.assertEqual(header, expected_header)
        self.assertEqual(content, expected_content)

    def test_split_header_and_content__delimiter_at_start(self):
        # Test with the delimiter at the very start of the text
        text = "## content\nNo Header info\nContent starts here"
        delimiter = "## content"
        expected_header = "## content\n\n"
        expected_content = "No Header info\nContent starts here"
        header, content = split_header_and_content(text, delimiter)
        self.assertEqual(header, expected_header)
        self.assertEqual(content, expected_content)

    def test_split_header_and_content__delimiter_at_end(self):
        # Test with the delimiter at the very end of the text
        text = "Header info\nNo content w delimiter at end\n## content"
        delimiter = "## content"
        expected_header = "Header info\nNo content w delimiter at end\n## content\n\n"
        expected_content = ""
        header, content = split_header_and_content(text, delimiter)
        self.assertEqual(header, expected_header)
        self.assertEqual(content, expected_content)

class TestReadHeaderAndContentFromFile(unittest.TestCase):
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Header information\n## content\nActual content starts here")
    def test_read_header_and_content_from_file__with_delimiter(self, mock_file, mock_exists):
        file_path = "/path/to/file.txt"
        header, content = read_header_and_content_from_file(file_path)
        expected_header = "Header information\n## content\n\n"
        expected_content = "Actual content starts here"
        self.assertEqual(header, expected_header)
        self.assertEqual(content, expected_content)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="No delimiter here, just content")
    def test_read_header_and_content_from_file__without_delimiter(self, mock_file, mock_exists):
        file_path = "/path/to/file.txt"
        header, content = read_header_and_content_from_file(file_path, delimiter="## content")
        expected_header = ""
        expected_content = "No delimiter here, just content"
        self.assertEqual(header, expected_header)
        self.assertEqual(content, expected_content)

    @patch('os.path.exists', return_value=False)
    def test_read_header_and_content_from_file__file_does_not_exist(self, mock_exists):
        file_path = "/nonexistent/path/to/file.txt"
        with self.assertRaises(ValueError):
            read_header_and_content_from_file(file_path)

class TestReadMetadataFieldFromFile(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with a file containing metadata
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, "test_file.md")
        with open(self.file_path, 'w') as f:
            f.write('## metadata\nTitle: Test Title\nAuthor: Test Author\n## content\nMain content')

    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_read_metadata_field_from_file__existing_field(self):
        # Test reading an existing metadata field
        field_line, field_value = read_metadata_field_from_file(self.file_path, 'Title')
        self.assertEqual(field_line, 2)
        self.assertEqual(field_value, 'Test Title')

    def test_read_metadata_field_from_file__non_existing_field(self):
        # Test reading a non-existing metadata field
        result = read_metadata_field_from_file(self.file_path, 'Nonexistent')
        self.assertIsNone(result)

    def test_read_metadata_field_from_file__multiple_fields(self):
        # Test reading multiple metadata fields
        _, title_value = read_metadata_field_from_file(self.file_path, 'Title')
        _, author_value = read_metadata_field_from_file(self.file_path, 'Author')
        self.assertEqual(title_value, 'Test Title')
        self.assertEqual(author_value, 'Test Author')


### WRITE FUNCTIONS
class TestWriteCompleteTextFfop(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test file before each test case
        self.test_filename = 'test_file.txt'
        self.complete_text = 'Complete text content'
        with open(self.test_filename, 'w') as f:
            f.write('Original content')

    def tearDown(self):
        # Teardown method to remove test files after each test case
        os.remove(self.test_filename)
        new_filename = self.test_filename.replace('.txt', '_writecompletetext.txt')
        if os.path.exists(new_filename):
            os.remove(new_filename)

    def test_write_complete_text_ffop__file_is_created_with_complete_text(self):
        # Test that a new file is created with the specified complete_text
        new_filename = write_complete_text_ffop(self.test_filename, self.complete_text)
        self.assertTrue(os.path.exists(new_filename))
        with open(new_filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.complete_text)

    def test_write_complete_text_ffop__original_file_is_unchanged(self):
        # Test that the original file remains unchanged
        write_complete_text_ffop(self.test_filename, self.complete_text)
        with open(self.test_filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'Original content')

    @patch('warnings.warn')
    def test_write_complete_text_ffop__warning_raised_if_file_exists(self, mock_warn):
        # Test that a warning is raised if the new file already exists
        write_complete_text_ffop(self.test_filename, self.complete_text)
        # Create the file again to trigger the warning
        write_complete_text_ffop(self.test_filename, self.complete_text)
        mock_warn.assert_called_once()
        
class TestWriteHeaderAndContentFfop(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test file before each test case
        self.test_filename = 'test_file.md'
        self.header = '## Header\n\n'
        self.content = 'Content line 1\nContent line 2\n'
        with open(self.test_filename, 'w') as f:
            f.write(self.header + self.content)

    def tearDown(self):
        # Teardown method to remove test files after each test case
        os.remove(self.test_filename)
        new_filename = self.test_filename.replace('.md', '_writeheaderandcontent.md')
        if os.path.exists(new_filename):
            os.remove(new_filename)

    def test_write_header_and_content_ffop__file_is_created_with_header_and_content(self):
        # Test that a new file is created with the specified header and content
        new_filename = write_header_and_content_ffop(self.test_filename, self.header, self.content)
        self.assertTrue(os.path.exists(new_filename))
        with open(new_filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.header + self.content)

    def test_write_header_and_content_ffop__original_file_is_unchanged(self):
        # Test that the original file remains unchanged
        write_header_and_content_ffop(self.test_filename, self.header, self.content)
        with open(self.test_filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.header + self.content)

    @patch('warnings.warn')
    def test_write_header_and_content_ffop__warning_raised_if_file_exists(self, mock_warn):
        # Test that a warning is raised if the new file already exists
        new_filename = write_header_and_content_ffop(self.test_filename, self.header, self.content)
        # Create the file again to trigger the warning
        write_header_and_content_ffop(self.test_filename, self.header, self.content)
        mock_warn.assert_called_once()


### TIMESTAMP LINKS FILE FUNCTIONS
class TestRemoveTimestampLinksFromContent(unittest.TestCase):
    def test_remove_timestamp_links_from_content__with_links(self):
        original_content = "John  [1:00](Link 1)\nBill  [2:00](Link 2)\nNormal text\n"
        expected_content = "John  1:00\nBill  2:00\nNormal text\n"
        processed_content = remove_timestamp_links_from_content(original_content)
        self.assertEqual(processed_content, expected_content)

    def test_remove_timestamp_links_from_content__with_links_text_after(self):
        original_content = "John  [1:00](Link 1)  AFTER\nBill  [2:00](Link 2)\nNormal text\n"
        expected_content = "John  1:00  AFTER\nBill  2:00\nNormal text\n"
        processed_content = remove_timestamp_links_from_content(original_content)
        self.assertEqual(processed_content, expected_content)

    def test_remove_timestamp_links_from_content__no_links(self):
        original_content = "No links here\nJust normal text\n"
        expected_content = "No links here\nJust normal text\n"
        processed_content = remove_timestamp_links_from_content(original_content)
        self.assertEqual(processed_content, expected_content)

    def test_remove_timestamp_links_from_content__empty_content(self):
        original_content = ""
        expected_content = "\n"  # Function adds an extra newline
        processed_content = remove_timestamp_links_from_content(original_content)
        self.assertEqual(processed_content, expected_content)

class TestRemoveTimestampLinksFfop(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test file before each test case
        self.test_filename = 'test_file.md'
        with open(self.test_filename, 'w') as f:
            f.write('## content\nJohn  [1:00](Link 1)\nBill  [2:00](Link 2)\nNormal text\n')

    def tearDown(self):
        # Teardown method to remove test files after each test case
        os.remove(self.test_filename)
        new_filename = self.test_filename.replace('.md', '_removetimestamplinks.md')
        if os.path.exists(new_filename):
            os.remove(new_filename)

    def test_remove_timestamp_links_ffop__file_is_created_without_timestamp_links(self):
        # Test that a new file is created without timestamp links
        new_filename = remove_timestamp_links_ffop(self.test_filename)
        self.assertTrue(os.path.exists(new_filename))
        with open(new_filename, 'r') as f:
            content = f.read()
        self.assertIn('John  1:00\nBill  2:00\nNormal text\n', content)

    def test_remove_timestamp_links_ffop__header_is_preserved(self):
        # Test that the header in the new file is preserved
        new_filename = remove_timestamp_links_ffop(self.test_filename)
        with open(new_filename, 'r') as f:
            content = f.read()
        self.assertTrue(content.startswith('## content\n'))

class TestGenerateTimestampLink(unittest.TestCase):
    def test_generate_timestamp_link__youtube(self):
        base_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        timestamp = "1:00"
        expected_link = "[1:00](https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=60)"
        self.assertEqual(generate_timestamp_link(base_link, timestamp), expected_link)

    def test_generate_timestamp_link__vimeo(self):
        base_link = "https://vimeo.com/123456789"
        timestamp = "1:00"
        expected_link = "[1:00](https://vimeo.com/123456789?ts=60000)"
        self.assertEqual(generate_timestamp_link(base_link, timestamp), expected_link)

    def test_generate_timestamp_link__spotify(self):
        base_link = "https://open.spotify.com/track/abcde12345"
        timestamp = "1:00"
        expected_link = "[1:00](https://open.spotify.com/track/abcde12345&t=60)"
        self.assertEqual(generate_timestamp_link(base_link, timestamp), expected_link)

    def test_generate_timestamp_link__unknown_domain(self):
        base_link = "https://unknown.com/video/abc"
        timestamp = "1:00"
        expected_link = "[1:00](https://unknown.com/video/abc&t=60)"
        self.assertEqual(generate_timestamp_link(base_link, timestamp), expected_link)

class TestAddTimestampLinksToContent(unittest.TestCase):
    def test_add_timestamp_links_to_content__with_timestamps_youtube_watch(self):
        base_link = "https://www.youtube.com/watch?v=2BLo2SdmjLI"
        original_content = "John  1:00\nBill  2:00\nNormal text\n"
        expected_content = "John  [1:00](https://www.youtube.com/watch?v=2BLo2SdmjLI&t=60)\nBill  [2:00](https://www.youtube.com/watch?v=2BLo2SdmjLI&t=120)\nNormal text\n"
        processed_content = add_timestamp_links_to_content(original_content, base_link)
        self.assertEqual(processed_content, expected_content)

    def test_add_timestamp_links_to_content__with_timestamps_youtube_dotbe(self):
        base_link = "https://youtu.be/vYNLahd6fds"
        original_content = "John  1:00\nBill  2:00\nNormal text\n"
        expected_content = "John  [1:00](https://youtu.be/vYNLahd6fds&t=60)\nBill  [2:00](https://youtu.be/vYNLahd6fds&t=120)\nNormal text\n"
        processed_content = add_timestamp_links_to_content(original_content, base_link)
        self.assertEqual(processed_content, expected_content)

    def test_add_timestamp_links_to_content__with_timestamps_spotify(self):
        base_link = "https://open.spotify.com/episode/2YJea3yl6k0ORFbJAwuELg?si=KfB2VaOiRyy64XFmxn3YHQ"
        original_content = "John  1:00\nBill  2:00\nNormal text\n"
        expected_content = "John  [1:00](https://open.spotify.com/episode/2YJea3yl6k0ORFbJAwuELg?si=KfB2VaOiRyy64XFmxn3YHQ&t=60)\nBill  [2:00](https://open.spotify.com/episode/2YJea3yl6k0ORFbJAwuELg?si=KfB2VaOiRyy64XFmxn3YHQ&t=120)\nNormal text\n"
        processed_content = add_timestamp_links_to_content(original_content, base_link)
        self.assertEqual(processed_content, expected_content)

    def test_add_timestamp_links_to_content__with_timestamps_vimeo(self):
        base_link = "https://vimeo.com/668273372/14ec57a5d7"
        original_content = "John  1:00\nBill  2:00\nNormal text\n"
        expected_content = "John  [1:00](https://vimeo.com/668273372/14ec57a5d7?ts=60000)\nBill  [2:00](https://vimeo.com/668273372/14ec57a5d7?ts=120000)\nNormal text\n"
        processed_content = add_timestamp_links_to_content(original_content, base_link)
        self.assertEqual(processed_content, expected_content)
 
    def test_add_timestamp_links_to_content__with_timestamps_text_after(self):
        base_link = "https://www.youtube.com/watch?v=2BLo2SdmjLI"
        original_content = "John  1:00 AFTER\nBill  2:00\nNormal text\n"
        expected_content = "John  [1:00](https://www.youtube.com/watch?v=2BLo2SdmjLI&t=60) AFTER\nBill  [2:00](https://www.youtube.com/watch?v=2BLo2SdmjLI&t=120)\nNormal text\n"
        processed_content = add_timestamp_links_to_content(original_content, base_link)
        self.assertEqual(processed_content, expected_content)

    def test_add_timestamp_links_to_content__no_timestamps(self):
        base_link = "https://youtube.com/video"
        original_content = "No timestamps here\nJust normal text\n"
        expected_content = "No timestamps here\nJust normal text\n"
        processed_content = add_timestamp_links_to_content(original_content, base_link)
        self.assertEqual(processed_content, expected_content)

    def test_add_timestamp_links_to_content__empty_content(self):
        base_link = "https://example.com/video"
        original_content = ""
        expected_content = "\n"  # Function adds an extra newline
        processed_content = add_timestamp_links_to_content(original_content, base_link)
        self.assertEqual(processed_content, expected_content)

class TestAddTimestampLinksFfop(unittest.TestCase):
    def setUp(self):
        # Setup method to create test files before each test case
        self.test_filename = 'test_file.md'
        with open(self.test_filename, 'w') as f:
            f.write('## metadata\nlink: https://example.com/video\n\n## content\n\nJohn  1:00\nHi There.\\nnBill  2:00\nI like turtles.\n\n')

        # Create a file that already has timestamp links
        self.test_filename_with_links = 'test_file_with_links.md'
        with open(self.test_filename_with_links, 'w') as f:
            f.write('## metadata\nlink: https://example.com/video\n\n## content\n\nJohn  [1:00](https://example.com/video&t=60)\nHi There.\n\nBill  [2:00](https://example.com/video&t=120)\nI like turtules.\n\n')

    def tearDown(self):
        # Teardown method to remove test files after each test case
        os.remove(self.test_filename)
        new_filename = self.test_filename.replace('.md', '_addtimestamplinks.md')
        if os.path.exists(new_filename):
            os.remove(new_filename)

        # Remove the file with timestamp links
        os.remove(self.test_filename_with_links)
        new_filename_with_links = self.test_filename_with_links.replace('.md', '_addtimestamplinks.md')
        if os.path.exists(new_filename_with_links):
            os.remove(new_filename_with_links)

    def test_add_timestamp_links_ffop__file_is_created_with_timestamp_links(self):
        # Test that a new file is created with timestamp links
        new_filename = add_timestamp_links_ffop(self.test_filename)
        self.assertTrue(os.path.exists(new_filename))
        with open(new_filename, 'r') as f:
            content = f.read()
        self.assertIn('John  [1:00](https://example.com/video&t=60)', content)
        self.assertIn('Bill  [2:00](https://example.com/video&t=120)', content)

    def test_add_timestamp_links_ffop__header_is_preserved(self):
        # Test that the header in the new file is preserved
        new_filename = add_timestamp_links_ffop(self.test_filename)
        with open(new_filename, 'r') as f:
            content = f.read()
        self.assertTrue(content.startswith('## metadata\nlink: https://example.com/video\n\n## content\n\n'))

    def test_add_timestamp_links_ffop__links_preserved_when_already_present(self):
        # Test that adding timestamp links to a file that already has them results in the same content
        new_filename = add_timestamp_links_ffop(self.test_filename_with_links)
        self.assertTrue(os.path.exists(new_filename))
        with open(new_filename, 'r') as f:
            content = f.read()
        with open(self.test_filename_with_links, 'r') as original_file:
            original_content = original_file.read()
        self.assertEqual(content, original_content)


### CONTENT PROCESSING
class TestFindAndReplaceInContentFfop(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test file before each test case
        self.test_filename = 'test_file.md'
        with open(self.test_filename, 'w') as f:
            f.write('## content\n\nJohn  1:00\nBill  2:00\nNormal text\n')

    def tearDown(self):
        # Teardown method to remove test files after each test case
        os.remove(self.test_filename)
        new_filename = self.test_filename.replace('.md', '_findandreplace.md')
        if os.path.exists(new_filename):
            os.remove(new_filename)

    def test_find_and_replace_in_content_ffop__replacements_made(self):
        # Test that replacements are made in the content
        find_str = "1:00"
        replace_str = "1:30"
        new_filename = find_and_replace_in_content_ffop(self.test_filename, find_str, replace_str)
        self.assertTrue(os.path.exists(new_filename))
        with open(new_filename, 'r') as f:
            content = f.read()
        self.assertIn('John  1:30', content)
        self.assertNotIn(find_str, content)

    def test_find_and_replace_in_content_ffop__no_replacements_made(self):
        # Test that a new file is created even if no replacements are made
        find_str = "nonexistent"
        replace_str = "replacement"
        new_filename = find_and_replace_in_content_ffop(self.test_filename, find_str, replace_str)
        self.assertTrue(os.path.exists(new_filename))  # A new file should be created
        with open(new_filename, 'r') as f:
            content = f.read()
        with open(self.test_filename, 'r') as original:
            original_content = original.read()
        self.assertEqual(content, original_content)  # The content should be unchanged


    def test_find_and_replace_in_content_ffop__header_is_preserved(self):
        # Test that the header in the new file is preserved
        find_str = "1:00"
        replace_str = "1:30"
        new_filename = find_and_replace_in_content_ffop(self.test_filename, find_str, replace_str)
        with open(new_filename, 'r') as f:
            content = f.read()
        self.assertTrue(content.startswith('## content\n'))

class TestGetTextBetweenDelimiters(unittest.TestCase):
    def setUp(self):
        # Suppress warnings in the test output
        warnings.simplefilter("ignore")

    def test_get_text_between_delimiters__start_and_end(self):
        # Test extraction of text between start and end delimiters
        full_text = "Start here: This is the text. End here."
        delimiter_start = "Start here:"
        delimiter_end = "End here."
        expected_text = "Start here: This is the text.\n"
        self.assertEqual(get_text_between_delimiters(full_text, delimiter_start, delimiter_end), expected_text)

    def test_get_text_between_delimiters__start_only(self):
        # Test extraction of text from start delimiter to end of text
        full_text = "Start here: This is the text."
        delimiter_start = "Start here:"
        expected_text = "Start here: This is the text.\n"
        self.assertEqual(get_text_between_delimiters(full_text, delimiter_start), expected_text)

    def test_get_text_between_delimiters__missing_start_delimiter(self):
        # Test when start delimiter is not found in the text
        full_text = "This is the text."
        delimiter_start = "Start here:"
        self.assertIsNone(get_text_between_delimiters(full_text, delimiter_start))

    def test_get_text_between_delimiters__missing_end_delimiter(self):
        # Test when end delimiter is not found in the text
        full_text = "Start here: This is the text."
        delimiter_start = "Start here:"
        delimiter_end = "End here."
        expected_text = "Start here: This is the text.\n"
        self.assertEqual(get_text_between_delimiters(full_text, delimiter_start, delimiter_end), expected_text)

    def test_get_text_between_delimiters__empty_text(self):
        # Test when the full_text is empty
        full_text = ""
        delimiter_start = "Start here:"
        self.assertIsNone(get_text_between_delimiters(full_text, delimiter_start))

class TestGetHeadingFromFile(unittest.TestCase):
    def setUp(self):
        # Create a temporary test file
        self.test_filename = "test_heading_file.md"
        test_content = """
## Apple
This is the first heading's content.

## Banana
This is the second heading's content.

### Subheading under Banana
This is a subheading under the second heading.

## Coconut
This is the third heading's content.
"""
        with open(self.test_filename, 'w') as f:
            f.write(test_content)

    def tearDown(self):
        # Remove the temporary test file
        os.remove(self.test_filename)

    def test_get_heading_from_file__valid_heading(self):
        # Test extraction of valid heading
        expected_content = "## Apple\nThis is the first heading's content.\n"
        self.assertEqual(get_heading_from_file(self.test_filename, "## Apple"), expected_content)

    def test_get_heading_from_file__subheading(self):
        # Test extraction of subheading
        expected_content = "### Subheading under Banana\nThis is a subheading under the second heading.\n"
        self.assertEqual(get_heading_from_file(self.test_filename, "### Subheading under Banana"), expected_content)

    def test_get_heading_from_file__double_heading_with_subheading(self):
        # Test extraction of heading with its subheading
        expected_content = """## Banana
This is the second heading's content.

### Subheading under Banana
This is a subheading under the second heading.
"""
        self.assertEqual(get_heading_from_file(self.test_filename, "## Banana"), expected_content)

    def test_get_heading_from_file__invalid_heading(self):
        # Test extraction of non-existent heading
        self.assertIsNone(get_heading_from_file(self.test_filename, "## Dragonfruit"))

    def test_get_heading_from_file__empty_file(self):
        # Test extraction from an empty file
        empty_filename = "empty_file.md"
        with open(empty_filename, 'w') as f:
            f.write("")
        self.assertIsNone(get_heading_from_file(empty_filename, "## Apple"))
        os.remove(empty_filename)

class TestSetHeadingTextFfop(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test file before each test case
        self.test_filename = 'test_heading_file.md'
        test_content = """
## content

## Heading 1
This is the first heading's content.

## Heading 2
This is the second heading's content.

### Subheading 2.1
This is a subheading under heading 2.
"""
        with open(self.test_filename, 'w') as f:
            f.write(test_content)

    def tearDown(self):
        # Teardown method to remove test files after each test case
        os.remove(self.test_filename)
        new_filename = self.test_filename.replace('.md', '_setheading.md')
        if os.path.exists(new_filename):
            os.remove(new_filename)

    def test_set_heading_text_ffop__replace_heading(self):
        # Test replacing the text of an existing heading
        new_text = "## Heading 1\nNew content for heading 1.\n"
        new_filename = set_heading_ffop(self.test_filename, new_text, "## Heading 1")
        self.assertTrue(os.path.exists(new_filename))
        content = read_complete_text_from_file(new_filename)
        self.assertIn(new_text, content)
        self.assertNotIn("This is the first heading's content.", content)

    def test_set_heading_text_ffop__add_heading(self):
        # Test adding a new heading and its text
        new_text = "## New Heading\nContent for the new heading.\n"
        new_filename = set_heading_ffop(self.test_filename, new_text, "## New Heading")
        self.assertTrue(os.path.exists(new_filename))
        content = read_complete_text_from_file(new_filename)
        self.assertIn(new_text, content)

    def test_set_heading_text_ffop__remove_heading(self):
        # Test removing the text of an existing heading
        new_filename = set_heading_ffop(self.test_filename, "", "## Heading 2")
        self.assertTrue(os.path.exists(new_filename))
        content = read_complete_text_from_file(new_filename)
        self.assertNotIn("## Heading 2", content)
        self.assertNotIn("This is the second heading's content.", content)

    def test_set_heading_text_ffop__value_error_for_nonexistent_heading(self):
        # Test that a ValueError is raised when trying to replace a non-existent heading
        with self.assertRaises(ValueError):
            do_ffop(set_heading_ffop, self.test_filename, "", "### notfound", overwrite="no")

class TestDeleteHeadingFfop(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test file before each test case
        self.test_filename = 'test_heading_file.md'
        test_content = """
## content

## Heading 1
This is the first heading's content.

## Heading 2
This is the second heading's content.

### Subheading 2.1
This is a subheading under heading 2.
"""
        with open(self.test_filename, 'w') as f:
            f.write(test_content.lstrip())

    def tearDown(self):
        # Teardown method to remove test files after each test case
        os.remove(self.test_filename)
        new_filename = self.test_filename.replace('.md', '_deleteheading.md')
        if os.path.exists(new_filename):
            os.remove(new_filename)

    def test_delete_heading_ffop__delete_existing_heading(self):
        # Test deleting an existing heading and its text
        new_filename = delete_heading_ffop(self.test_filename, "## Heading 1")
        self.assertTrue(os.path.exists(new_filename))
        content = read_complete_text_from_file(new_filename)
        self.assertNotIn("## Heading 1", content)
        self.assertNotIn("This is the first heading's content.", content)

    def test_delete_heading_ffop__delete_nonexistent_heading(self):
        # Test deleting a nonexistent heading (should not modify the file)
        original_content = read_complete_text_from_file(self.test_filename)
        new_filename = delete_heading_ffop(self.test_filename, "## Nonexistent Heading")
        self.assertTrue(os.path.exists(new_filename))
        content = read_complete_text_from_file(new_filename)
        self.assertEqual(original_content, content)

    @patch('warnings.warn')
    def test_delete_heading_ffop__warning_raised_if_file_exists(self, mock_warn):
        # Test that a warning is raised if the new file already exists
        # Create the file that would be generated by delete_heading_ffop to trigger the warning
        new_filename = self.test_filename.replace('.md', '_deleteheading.md')
        with open(new_filename, 'w') as f:
            f.write("Dummy content to simulate existing file.")
        delete_heading_ffop(self.test_filename, "## Heading 1")
        mock_warn.assert_called_once()


### COMBINE AND CSV


### JSON PROCESSING
class TestPrettyPrintJsonStructure(unittest.TestCase):
    def setUp(self):
        # Create a temporary JSON file
        self.temp_json_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json')
        self.test_json_data = {
            "key1": "value1",
            "key2": ["list_item1", "list_item2"],
            "key3": {
                "subkey1": "subvalue1"
            }
        }
        json.dump(self.test_json_data, self.temp_json_file)
        self.temp_json_file.close()

    def tearDown(self):
        # Clean up by removing the temporary file and its '.pretty' counterpart
        os.unlink(self.temp_json_file.name)
        if os.path.exists(self.temp_json_file.name + '.pretty'):
            os.unlink(self.temp_json_file.name + '.pretty')

    def test_pretty_printjson_structure__with_save(self):
        # Test that the output is correctly saved to a '.pretty' file
        pretty_print_json_structure(self.temp_json_file.name, level_limit=2, save_to_file=True)
        pretty_file_path = self.temp_json_file.name + '.pretty'
        self.assertTrue(os.path.exists(pretty_file_path))

    def test_pretty_print_json_structure__level_limit(self):
        # Test the level limit functionality by inspecting the saved file content
        # (This test assumes that examining the saved file's content can indirectly verify the level limit functionality)
        pretty_print_json_structure(self.temp_json_file.name, level_limit=1, save_to_file=True)
        pretty_file_path = self.temp_json_file.name + '.pretty'
        with open(pretty_file_path, 'r') as pretty_file:
            contents = pretty_file.readlines()
            # Verify that contents respect the level limit (exact verification depends on function's output format)
            self.assertTrue(any("key3" in line for line in contents))
            # This checks if 'key3' is present but does not verify deeper structures beyond the level limit

    def test_pretty_print_json_structure__without_save(self):
        # Test that the output is not saved to a file when save_to_file is False
        pretty_print_json_structure(self.temp_json_file.name, level_limit=2, save_to_file=False)
        pretty_file_path = self.temp_json_file.name + '.pretty'
        self.assertFalse(os.path.exists(pretty_file_path))

    def test_pretty_print_json_structure__no_level_limit(self):
        # Test that all levels are printed when level_limit is None
        pretty_print_json_structure(self.temp_json_file.name, level_limit=None, save_to_file=True)
        pretty_file_path = self.temp_json_file.name + '.pretty'
        with open(pretty_file_path, 'r') as pretty_file:
            contents = pretty_file.read()
            # Verify that all levels are printed (exact verification depends on function's output format)
            self.assertIn("subkey1", contents)

    def test_pretty_print_json_structure__with_nonexistent_file(self):
        # Test that a warning is raised when the file does not exist
        non_existent_file_path = "non_existent_file.json"
        with self.assertWarns(Warning):
            pretty_print_json_structure(non_existent_file_path, level_limit=2, save_to_file=True)

    def test_pretty_print_json_structure__save_to_file_false(self):
        # Test pretty printing JSON structure without saving to file
        json_file_path = self.temp_json_file.name
        pretty_print_json_structure(json_file_path, level_limit=2, save_to_file=False)

        output_file_path = json_file_path + '.pretty'
        self.assertFalse(os.path.exists(output_file_path), "Output file should not exist when save_to_file is False.")

    def test_pretty_print_json_structure__non_existent_file(self):
        # Test handling of non-existent JSON file
        non_existent_file_path = 'non_existent_file.json'
        with self.assertWarns(Warning) as warning:
            pretty_print_json_structure(non_existent_file_path)
        self.assertIn("does not exist", str(warning.warning.args[0]), "Warning should mention the non-existent file.")

    def test_pretty_print_json_structure__no_level_limit(self):
        # Test printing JSON structure without a level limit
        json_file_path = self.temp_json_file.name
        pretty_print_json_structure(json_file_path, level_limit=None, save_to_file=False)

        # Verifying the function runs without error and the precise output check is done through inspection

    def test_pretty_print_json_structure__specific_level_limit(self):
        # Test printing JSON structure with a specific level limit
        json_file_path = self.temp_json_file.name
        pretty_print_json_structure(json_file_path, level_limit=1, save_to_file=False)

        # This test ensures that the function correctly limits the printing depth
        # Precise output verification is manual due to the nature of console output

    def test_pretty_print_json_structure__empty_json(self):
        # Test handling of an empty JSON file
        empty_json_file_path = tempfile.mkstemp(suffix='.json')[1]
        with open(empty_json_file_path, 'w') as file:
            json.dump({}, file)

### MORE METADATA AND HEADER FUNCTIONS
class TestSetMetadataField(unittest.TestCase):
    def test_set_metadata_field__add_new_field(self):
        header = "## metadata\n\n## content\n\n"
        field = "length"
        value = "4:30"
        expected_header = "## metadata\nlength: 4:30\n\n## content\n\n"
        updated_header = set_metadata_field(header, field, value)
        self.assertEqual(updated_header, expected_header)

    def test_set_metadata_field__update_existing_field(self):
        header = "## metadata\nlast updated: old_value\n\n## content\n\n"
        field = "last updated"
        value = "11-19-2023 by Susan"
        expected_header = "## metadata\nlast updated: 11-19-2023 by Susan\n\n## content\n\n"
        updated_header = set_metadata_field(header, field, value)
        self.assertEqual(updated_header, expected_header)

    def test_set_metadata_field__add_two_fields(self):
        header = "## metadata\nlast updated: old_value\n\n## content\n\n"
        field1 = "last updated"
        value1 = "11-19-2023 by Susan"
        field2 = "link"
        value2 = "dummy"
        expected_header = "## metadata\nlast updated: 11-19-2023 by Susan\nlink: dummy\n\n## content\n\n"
        updated_header = set_metadata_field(header, field1, value1)
        updated_header = set_metadata_field(updated_header, field2, value2)
        self.assertEqual(updated_header, expected_header)

    def test_set_metadata_field__add_field_when_no_blank_line_at_header_end(self):
        header = "## metadata\n## content"
        field = "new_field"
        value = "new_value"
        expected_header = "## metadata\nnew_field: new_value\n## content"
        updated_header = set_metadata_field(header, field, value)
        self.assertEqual(updated_header, expected_header)

class TestRemoveMetadataField(unittest.TestCase):
    def test_remove_metadata_field__existing_field(self):
        header = "## metadata\nlength: 4:30\nlast updated: 11-19-2023 by Susan\n\n## content\n\n"
        field = "length"
        expected_header = "## metadata\nlast updated: 11-19-2023 by Susan\n\n## content\n\n"
        updated_header = remove_metadata_field(header, field)
        self.assertEqual(updated_header, expected_header)

    def test_remove_metadata_field__nonexistent_field(self):
        header = "## metadata\nlength: 4:30\n\n## content\n\n"
        field = "nonexistent"
        expected_header = "## metadata\nlength: 4:30\n\n## content\n\n"
        updated_header = remove_metadata_field(header, field)
        self.assertEqual(updated_header, expected_header)

    def test_remove_metadata_field__multiple_fields(self):
        header = "## metadata\nlength: 4:30\nlast updated: 11-19-2023 by Susan\n\n## content\n\n"
        field = "last updated"
        expected_header = "## metadata\nlength: 4:30\n\n## content\n\n"
        updated_header = remove_metadata_field(header, field)
        self.assertEqual(updated_header, expected_header)

class TestSetLastUpdated(unittest.TestCase):
    def test_set_last_updated__add_new_field(self):
        header = "## metadata\n\n## content\n\n"
        new_value = "by John"
        date_today = datetime.now().strftime("%m-%d-%Y")
        expected_header = f"## metadata\nlast updated: {date_today} by John\n\n## content\n\n"
        updated_header = set_last_updated(header, new_value)
        self.assertEqual(updated_header, expected_header)

    def test_set_last_updated__update_existing_field(self):
        header = "## metadata\nlast updated: old_value\n\n## content\n\n"
        new_value = "by Susan"
        date_today = datetime.now().strftime("%m-%d-%Y")
        expected_header = f"## metadata\nlast updated: {date_today} by Susan\n\n## content\n\n"
        updated_header = set_last_updated(header, new_value)
        self.assertEqual(updated_header, expected_header)

    def test_set_last_updated__use_today_false(self):
        header = "## metadata\nlast updated: old_value\n\n## content\n\n"
        new_value = "11-19-2023 by Susan"
        expected_header = "## metadata\nlast updated: 11-19-2023 by Susan\n\n## content\n\n"
        updated_header = set_last_updated(header, new_value, use_today=False)
        self.assertEqual(updated_header, expected_header)

### MISC FILE FUNCTIONS
class TestDeleteFile(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test file before each test case
        self.test_filename = 'test_file.txt'
        with open(self.test_filename, 'w') as f:
            f.write('Test content')

    def tearDown(self):
        # Teardown method to remove test file if it still exists after a test case
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_delete_file__file_deleted_successfully(self):
        # Test that a file is successfully deleted
        result = delete_file(self.test_filename)
        self.assertTrue(result)
        self.assertFalse(os.path.exists(self.test_filename))

    def test_delete_file__file_does_not_exist(self):
        # Test that the function handles the case where the file does not exist
        os.remove(self.test_filename)  # Delete the file to simulate the file not existing
        result = delete_file(self.test_filename)
        self.assertIsInstance(result, OSError)

class TestDeleteFilesWithSuffix(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test directory with files before each test case
        self.temp_dir = 'test_folder'
        os.mkdir(self.temp_dir)
        self.file1 = os.path.join(self.temp_dir, 'file1.txt')
        self.file2 = os.path.join(self.temp_dir, 'file2_suffix.txt')
        with open(self.file1, 'w') as f:
            f.write('File 1 content')
        with open(self.file2, 'w') as f:
            f.write('File 2 content')

    def tearDown(self):
        # Teardown method to remove test directory and files after each test case
        if os.path.exists(self.file1):
            os.remove(self.file1)
        if os.path.exists(self.file2):
            os.remove(self.file2)
        os.rmdir(self.temp_dir)

    def test_delete_files_with_suffix__files_deleted(self):
        # Test that files with the specified suffix are deleted from the folder
        suffix_include = '_suffix'
        deleted_files = delete_files_with_suffix(self.temp_dir, suffix_include)
        self.assertTrue(os.path.exists(self.file1))
        self.assertFalse(os.path.exists(self.file2))
        self.assertIn(self.file2, deleted_files)

    def test_delete_files_with_suffix__no_files_deleted(self):
        # Test that no files are deleted if no files match the specified suffix
        suffix_include = '_nonexistent_suffix.txt'
        deleted_files = delete_files_with_suffix(self.temp_dir, suffix_include)
        self.assertTrue(os.path.exists(self.file1))
        self.assertTrue(os.path.exists(self.file2))
        self.assertEqual(len(deleted_files), 0)

class TestTuneTitle(unittest.TestCase):
    def test_tune_title__alphanumeric(self):
        self.assertEqual(tune_title('Title123'), 'Title123')

    def test_tune_title__spaces(self):
        self.assertEqual(tune_title('Title With Spaces'), 'Title With Spaces')

    def test_tune_title__allowed_special_characters(self):
        self.assertEqual(tune_title('Title-With-Dashes(And)Parentheses.Period'), 'Title-With-Dashes(And)Parentheses.Period')

    def test_tune_title__disallowed_special_characters(self):
        self.assertEqual(tune_title('Title!@#$%^&*+=With{}[]Special|\\:;"\'<>,?/Characters'), 'TitleWithSpecialCharacters')

    def test_tune_title__mix_allowed_disallowed_characters(self):
        self.assertEqual(tune_title('Title-123(With)Special_Characters!@#'), 'Title-123(With)Special_Characters')

    def test_tune_title__leading_trailing_special_characters(self):
        self.assertEqual(tune_title('!Title@'), 'Title')

    def test_tune_title__only_special_characters(self):
        self.assertEqual(tune_title('!@#$%^&*'), '')  # exclude parantheses because they are allowed

    def test_tune_title__path_separators(self):
        self.assertEqual(tune_title('Title/With\\Path|Separators:'), 'TitleWithPathSeparators')

    def test_tune_title__unicode_characters(self):
        self.assertEqual(tune_title('Título Con Caracteres Españolesñá'), 'Título Con Caracteres Españolesñá')

class TestCreateFullPath(unittest.TestCase):
    def test_create_full_path__empty_title_or_path(self):
        self.assertEqual(create_full_path('', '_xyz.md', 'data/audio_inbox'), 'data/audio_inbox/_xyz.md')

    def test_create_full_path__default_folder_only(self):
        self.assertEqual(create_full_path('Lost Lecture', '_xyz.md', 'data/audio_inbox'), 'data/audio_inbox/Lost Lecture_xyz.md')

    def test_create_full_path__with_existing_extension(self):
        self.assertEqual(create_full_path('Lost Lecture_blah.txt', '_xyz.md', 'data/audio_inbox'), 'data/audio_inbox/Lost Lecture_blah_xyz.md')

    def test_create_full_path__absolute_path(self):
        self.assertEqual(create_full_path('/absolute/path/Lost Lecture', '_xyz.md', 'data/audio_inbox'), '/absolute/path/Lost Lecture_xyz.md')

    def test_create_full_path__relative_path(self):
        self.assertEqual(create_full_path('relative/path/Lost Lecture', '_xyz.md', 'data/audio_inbox'), 'relative/path/Lost Lecture_xyz.md')

    def test_create_full_path__path_with_special_characters(self):
        # exclude underscore and parantheses because these are allowed in filenames
        self.assertEqual(create_full_path('Special!@#$%^&*+= Lecture', '_xyz.md', 'data/audio_inbox'), 'data/audio_inbox/Special Lecture_xyz.md')

    def test_create_full_path__path_with_spaces(self):
        self.assertEqual(create_full_path('Lost Lecture With Spaces', '_xyz.md', 'data/audio_inbox'), 'data/audio_inbox/Lost Lecture With Spaces_xyz.md')

    def test_create_full_path__path_with_dot_in_directory_name(self):
        self.assertEqual(create_full_path('data.audio.inbox/Lost Lecture', '_xyz.md', 'data/audio_inbox'), 'data.audio.inbox/Lost Lecture_xyz.md')

    def test_create_full_path__path_with_existing_extension(self):
        # Test creating a full path with an existing extension in the file title or path
        self.assertEqual(create_full_path('tests/2099-01-01_Test file with link.md', '_xyz.md'), 'tests/2099-01-01_Test file with link_xyz.md')

    def test_create_full_path__invalid_directory(self):
        # Test creating a full path with an invalid directory in the file title or path
        with self.assertRaises(ValueError):
            create_full_path('2099-01-01_Test file with link.md', '_xyz.md')

class TestFindFileInFolders(unittest.TestCase):
    def setUp(self):
        # Setup temporary folders and a file for the test
        self.temp_folder1 = tempfile.mkdtemp()
        self.temp_folder2 = tempfile.mkdtemp()
        self.file_name = "testfile.txt"
        self.file_path = os.path.join(self.temp_folder1, self.file_name)
        with open(self.file_path, 'w') as f:
            f.write('Test content')

    def tearDown(self):
        # Clean up by removing temporary folders
        shutil.rmtree(self.temp_folder1)
        shutil.rmtree(self.temp_folder2)

    def test_file_found_in_folder(self):
        # Test finding the file in the folders
        found_path = find_file_in_folders(self.file_name, [self.temp_folder1, self.temp_folder2])
        self.assertEqual(found_path, self.file_path)

    def test_file_not_found_in_folder(self):
        # Test not finding the file when it's not in the folders
        found_path = find_file_in_folders("nonexistent.txt", [self.temp_folder1, self.temp_folder2])
        self.assertIsNone(found_path)

    def test_file_already_exists(self):
        # Test the warning when the file already exists at the given path
        with self.assertWarns(Warning):
            found_path = find_file_in_folders(self.file_path, [self.temp_folder1, self.temp_folder2])
        self.assertEqual(found_path, self.file_path)

class TestCopyFileAndAppendSuffix(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test file before each test case
        self.test_filename = 'test_file.txt'
        with open(self.test_filename, 'w') as f:
            f.write('Test content')

    def tearDown(self):
        # Teardown method to remove test files after each test case
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
        new_filename = self.test_filename.replace('.txt', '_backup.txt')
        if os.path.exists(new_filename):
            os.remove(new_filename)

    def test_copy_file_and_append_suffix__file_copied(self):
        # Test that a new file is created with the specified suffix
        new_filename = copy_file_and_append_suffix(self.test_filename, '_backup')
        self.assertTrue(os.path.exists(new_filename))
        with open(new_filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'Test content')

    def test_copy_file_and_append_suffix__file_does_not_exist(self):
        # Test that an error is raised if the original file does not exist
        with self.assertRaises(ValueError):
            copy_file_and_append_suffix('nonexistent_file.txt', '_backup')




# AssertionError: 'Returned' != 'Expected'

if __name__ == '__main__':
    unittest.main()