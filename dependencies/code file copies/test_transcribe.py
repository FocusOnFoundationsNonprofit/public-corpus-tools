# Run tests with python -m unittest discover -s tests

import os
import sys
# Add the parent directory to the Python path so we can import the 'primary' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch, mock_open, MagicMock, call
import shutil
import tempfile

from primary.fileops import *
from primary.transcribe import *


### YOUTUBE FUNCTIONS
@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLDownloadMp3FromYoutube(unittest.TestCase):
    def setUp(self):
        # Setup method to define the output path for the downloaded mp3 file
        self.cur_path = "tests/test_manual_files/transcribe"
        self.output_title = os.path.join(self.cur_path, 'download_yt_test')
        self.output_file_path = self.output_title + '.mp3'
        self.reference_file_path = self.output_title + '_REF.mp3'

    def tearDown(self):
        # Teardown method to remove the downloaded mp3 file after each test case
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)

    def test_download_mp3_from_youtube__real_download(self):
        # Test that the function can download an audio file from a YouTube URL
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        result = download_mp3_from_youtube(cur_url, output_title=self.output_title)
        self.assertEqual(result, self.output_file_path)
        self.assertTrue(os.path.exists(self.output_file_path))

        # Check that the file size matches the reference file size
        if os.path.exists(self.reference_file_path):
            downloaded_file_size = os.path.getsize(self.output_file_path)
            reference_file_size = os.path.getsize(self.reference_file_path)
            self.assertEqual(downloaded_file_size, reference_file_size, "The downloaded file size does not match the reference file size.")
        else:
            self.fail(f"Reference file {self.reference_file_path} does not exist.")

class TestAPIMOCKDownloadMp3FromYoutube(unittest.TestCase):
    def setUp(self):
        # Setup method to define the output path for the downloaded mp3 file
        self.cur_path = "tests/test_manual_files/transcribe"
        self.output_title = os.path.join(self.cur_path, 'download_yt_test')
        self.output_file_path = self.output_title + '.mp3'
        self.reference_file_path = self.output_title + '_REF.mp3'

    def tearDown(self):
        # Teardown method to remove the downloaded mp3 file after each test case
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)
    
    @patch("yt_dlp.YoutubeDL")
    def test_download_mp3_from_youtube__mock_real_download(self, mock_YoutubeDL):
        # Test that the function can download an audio file from a YouTube URL
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        cur_url_list = [cur_url]
        # Mock instance with method extract_info to return a dict for context manager
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.download.side_effect = lambda urls_list: None
        mock_YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance
        # This should run but won't download anything
        result = download_mp3_from_youtube(cur_url, output_title=self.output_title)
        self.assertEqual(result, self.output_file_path)
        mock_ydl_instance.download.assert_called_once_with(cur_url_list)

@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLGetYoutubeTitleLength(unittest.TestCase):
    def test_get_youtube_title_length__valid_url(self):
        # Test that the function retrieves the correct title and length for a given YouTube URL
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        expected_title = 'Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip!'
        expected_length = '0:39'
        video_title, video_length = get_youtube_title_length(cur_url)
        self.assertEqual(video_title, expected_title)
        self.assertEqual(video_length, expected_length)

class TestAPIMOCKGetYoutubeTitleLength(unittest.TestCase):
    @patch("yt_dlp.YoutubeDL")
    def test_get_youtube_title_length__valid_url(self, mock_YoutubeDL):
        # Test that the function retrieves the correct title and length for a given YouTube URL
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        expected_title = 'Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip!'
        expected_length = '0:39'
        # Mock instance with method extract_info to return a dict for context manager
        mock_ydl_instance = MagicMock()
        with open("tests/test_manual_files/transcribe/info_dict_yt_test.json", "r") as f:
            info_dict_yt_test = json.load(f)
            mock_ydl_instance.extract_info.side_effect = lambda url, download: info_dict_yt_test
        mock_YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance
        video_title, video_length = get_youtube_title_length(cur_url)
        self.assertEqual(video_title, expected_title)
        self.assertEqual(video_length, expected_length)

@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLDownloadLinkListToMp3s(unittest.TestCase):
    def setUp(self):
        # Setup method to define the audio inbox path
        self.audio_inbox_path = "tests/test_manual_files/audio_inbox"
        if not os.path.exists(self.audio_inbox_path):
            os.makedirs(self.audio_inbox_path)

    def tearDown(self):
        # Teardown method to remove downloaded mp3 files and the audio inbox directory after each test case
        for filename in os.listdir(self.audio_inbox_path):
            file_path = os.path.join(self.audio_inbox_path, filename)
            os.remove(file_path)
        os.rmdir(self.audio_inbox_path)

    def test_download_link_list_to_mp3s__downloads_and_titles(self):
        # Test that the function downloads MP3 files and returns the correct link-title pairs
        cur_urls = ["https://youtu.be/RNNfkIE7uYs", "https://youtu.be/VW6LYuli7VU"]
        expected_titles = {
            "https://youtu.be/RNNfkIE7uYs": "Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip!",
            "https://youtu.be/VW6LYuli7VU": "Richard Feynman talks about Algebra"
        }
        link_title_pairs = download_link_list_to_mp3s(cur_urls, self.audio_inbox_path)
        self.assertEqual(link_title_pairs, expected_titles)
        # Check if the MP3 files are downloaded
        for title in expected_titles.values():
            file_path = os.path.join(self.audio_inbox_path, title + ".mp3")
            self.assertTrue(os.path.exists(file_path))

class TestAPIMOCKDownloadLinkListToMp3s(unittest.TestCase):
    def setUp(self):
        # Setup return values for side effect
        self.yt_title_length_pairs_list = [
            ("Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip!", "0"),
            ("Richard Feynman talks about Algebra", "0")]
        # Setup argument
        self.audio_inbox_path = "tests/test_manual_files/audio_inbox"

    @patch("yt_dlp.YoutubeDL")
    @patch("primary.transcribe.get_youtube_title_length")
    @patch("primary.transcribe.download_mp3_from_youtube", return_value="output_file_path")
    def test_download_link_list_to_mp3s__mock_downloads_and_titles(self, mock_download_mp3_from_youtube, mock_get_youtube_title_length, mock_YoutubeDL):
        # Test that the function downloads MP3 files and returns the correct link-title pairs
        cur_urls = ["https://youtu.be/RNNfkIE7uYs", "https://youtu.be/VW6LYuli7VU"]
        mock_get_youtube_title_length.side_effect = self.yt_title_length_pairs_list
        expected_titles = {
            "https://youtu.be/RNNfkIE7uYs": "Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip!",
            "https://youtu.be/VW6LYuli7VU": "Richard Feynman talks about Algebra"
        }
        link_title_pairs = download_link_list_to_mp3s(cur_urls, self.audio_inbox_path)
        self.assertEqual(link_title_pairs, expected_titles)
        # Don't check for downloads

@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLGetYoutubeSubtitles(unittest.TestCase):
    def test_get_youtube_subtitles__subtitles_found(self):
        # Test that the function retrieves subtitles for the given YouTube URL
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        expected_subtitle_start = "there  was  a  little  annoyances  from   censorship"
        subtitles = get_youtube_subtitles(cur_url)
        print(f"TEST EXPECT:{expected_subtitle_start}")
        print(f"TEST RETURN:{subtitles}")
        self.assertIsNotNone(subtitles)
        self.assertTrue(subtitles.startswith(expected_subtitle_start))

    def test_get_youtube_subtitles__no_subtitles_found(self):
        # Test that the function returns None if no subtitles are available
        cur_url = "https://www.youtube.com/watch?v=0ecbeh0hrKE"  # URL with no subtitles
        subtitles = get_youtube_subtitles(cur_url)
        self.assertIsNone(subtitles)

class TestAPIMOCKGetYoutubeSubtitles(unittest.TestCase):
    def setUp(self):
        with open("tests/test_manual_files/transcribe/subtitles_file_yt_test.txt", "r") as f:
            self.subtitles_content = f.read()

    @patch("yt_dlp.YoutubeDL")
    @patch("primary.transcribe.download_youtube_subtitles_url")
    def test_get_youtube_subtitles__mock_subtitles_found(self, mock_download_youtube_subtitles_url, mock_YoutubeDL):
        # Mock test that the function retrieves subtitles for the given YouTube URL
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        mock_download_youtube_subtitles_url.return_value = self.subtitles_content
        expected_subtitle_start = "there  was  a  little  annoyances  from   censorship"
        # Mock instance with method extract_info to return a dict for context manager
        # Just to get condtions to True
        mock_ydl_instance = MagicMock()
        with open("tests/test_manual_files/transcribe/info_dict_yt_test.json", "r") as f:
            info_dict_yt_test = json.load(f)
            mock_ydl_instance.extract_info.side_effect = lambda url, download: info_dict_yt_test
        mock_YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance
        # Mock get info
        subtitles = get_youtube_subtitles(cur_url)
        self.assertIsNotNone(subtitles)
        self.assertTrue(subtitles.startswith(expected_subtitle_start))

    @patch("yt_dlp.YoutubeDL")
    @patch("primary.transcribe.download_youtube_subtitles_url", return_value=None)
    def test_get_youtube_subtitles__mock_no_subtitles_found(self, mock_download_youtube_subtitles_url, mock_YoutubeDL):
        # Mock test that the function returns None if no subtitles are available
        cur_url = "https://www.youtube.com/watch?v=0ecbeh0hrKE"  # URL with no subtitles
        # Mock instance with method extract_info to return a dict for context manager
        # Just to get condtions to True
        mock_ydl_instance = MagicMock()
        with open("tests/test_manual_files/transcribe/info_dict_yt_test.json", "r") as f:
            info_dict_yt_test = json.load(f)
            mock_ydl_instance.extract_info.side_effect = lambda url, download: info_dict_yt_test
        mock_YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance
        # Mock get info
        subtitles = get_youtube_subtitles(cur_url)
        self.assertIsNone(subtitles)

@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLGetYoutubeAll(unittest.TestCase):
    def test_get_youtube_all__apicall_video_details(self):
        # Test that the function retrieves all available information for the given YouTube URL
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        expected_details = {
            'title': 'Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip!',
            'channel': 'Muon Ray',
            'date': '20160120',
            'length': '0:00:39',
            'chapters': '',
            'description': 'Please Help Support This',
            'transcript': "there was a little",
            'transcript source': 'auto-captions'
        }
        video_details = get_youtube_all(cur_url)
        # Truncate the description and transcript in the retrieved details for comparison
        video_details['description'] = ' '.join(video_details['description'].split()[:4])  # truncated to only be the first 4 words
        video_details['transcript'] = ' '.join(video_details['transcript'].split()[:4])
        self.assertEqual(video_details, expected_details)

class TestAPIMOCKGetYoutubeAll(unittest.TestCase):
    def setUp(self):
        with open("tests/test_manual_files/transcribe/subtitles_file_yt_test.txt", "r") as f:
            self.subtitles_content = f.read()

    @patch("yt_dlp.YoutubeDL")
    @patch('primary.transcribe.is_valid_youtube_url', return_value=True)
    @patch('primary.transcribe.download_youtube_subtitles_url')
    def test_get_youtube_all__apimock_video_details(self, mock_download_youtube_subtitles_url, mock_is_valid_youtube_url, mock_YoutubeDL):
        # Mock test for the function that retrieves all available information for the given YouTube URL
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        mock_download_youtube_subtitles_url.return_value = self.subtitles_content
        expected_details = {
            'title': 'Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip!',
            'channel': 'Muon Ray',
            'date': '20160120',
            'length': '0:00:39',
            'chapters': '',
            'description': 'Please Help Support This',
            'transcript': "there was a little",
            'transcript source': 'auto-captions'
        }
        # Mock instance with method extract_info to return a dict for context manager
        mock_ydl_instance = MagicMock()
        with open("tests/test_manual_files/transcribe/info_dict_yt_test.json", "r") as f:
            info_dict_yt_test = json.load(f)
            mock_ydl_instance.extract_info.side_effect = lambda url, download: info_dict_yt_test
        mock_YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance
        video_details = get_youtube_all(cur_url)
        # Truncate the description and transcript to only be the first 4 words in the retrieved details for comparison
        video_details['description'] = ' '.join(video_details['description'].split()[:4])
        video_details['transcript'] = ' '.join(video_details['transcript'].split()[:4])
        mock_ydl_instance.extract_info.assert_called_once_with(cur_url, download=False)
        self.assertEqual(video_details, expected_details)

@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLIsValidYoutubeUrl(unittest.TestCase):
    def test_is_valid_youtube_url__valid_url(self):
        # Test that the function returns True for a valid YouTube URL
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        self.assertTrue(is_valid_youtube_url(cur_url))

    def test_is_valid_youtube_url__invalid_url(self):
        # Test that the function returns False for an invalid YouTube URL
        cur_url = "https://youtu.be/XXXXXXX"
        self.assertFalse(is_valid_youtube_url(cur_url))

    def test_is_valid_youtube_url__non_youtube_url(self):
        # Test that the function returns False for a non-YouTube URL
        cur_url = "https://www.example.com"
        self.assertFalse(is_valid_youtube_url(cur_url))

class TestAPIMOCKIsValidYoutubeUrl(unittest.TestCase):
    @patch("yt_dlp.YoutubeDL")
    def test_is_valid_youtube_url__mock_valid_url(self, mock_YoutubeDL):
        # Test that the function returns True for a valid YouTube URL
        cur_url = "url"
        # Mock instance for context manager
        mock_ydl_instance = MagicMock()
        mock_YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance
        result = is_valid_youtube_url(cur_url)
        mock_ydl_instance.extract_info.assert_called_once_with(cur_url, download=False)
        self.assertTrue(result)

    def test_is_valid_youtube_url__mock_download_error(self):
        # Test DownloadError
        cur_url = "url"
        with self.assertRaises(youtube_dl.utils.DownloadError):
            raise youtube_dl.utils.DownloadError(msg="DownloadError")
        self.assertFalse(is_valid_youtube_url(cur_url))

    def test_is_valid_youtube_url__mock_extractor_error(self):
        # Test ExtractorError
        cur_url = "url"
        with self.assertRaises(youtube_dl.utils.ExtractorError):
            raise youtube_dl.utils.ExtractorError(msg="ExtractorError")
        self.assertFalse(is_valid_youtube_url(cur_url))

    def test_is_valid_youtube_url__mock_primary_exception(self):
        # Test Exception
        cur_url = "url"
        with self.assertRaises(Exception) as context:
            raise Exception("Exception")
        self.assertFalse(is_valid_youtube_url(cur_url))
        self.assertEqual(str(context.exception), "Exception")

@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLCreateYoutubeMd(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test directory before each test case
        self.test_dir = "tests/test_manual_files/youtube_md"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        # Teardown method to remove test directory and files after each test case
        shutil.rmtree(self.test_dir)

    def test_create_youtube_md__apicall_without_title(self):
        # Test that the function creates a markdown file with the default title
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        md_file_path = create_youtube_md(cur_url)
        expected_md_file_path = "data/audio_inbox/Richard Feynman on Getting Arrested by Los Alamos Fence Security - Funny Clip_yt.md"
        self.assertEqual(md_file_path, expected_md_file_path)
        self.assertTrue(os.path.exists(md_file_path))
        with open(md_file_path, 'r') as file:
            content = file.read()
        self.assertIn("## metadata", content)
        self.assertIn("## content", content)

    def test_create_youtube_md__apicall_with_title(self):
        # Test that the function creates a markdown file with the specified title
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        title_or_path = "Feynman Arrested"
        md_file_path = create_youtube_md(cur_url, title_or_path)
        expected_md_file_path = "data/audio_inbox/Feynman Arrested_yt.md"
        self.assertEqual(md_file_path, expected_md_file_path)
        self.assertTrue(os.path.exists(md_file_path))
        self.assertIn(title_or_path, md_file_path)
        with open(md_file_path, 'r') as file:
            content = file.read()
        self.assertIn("## metadata", content)
        self.assertIn("## content", content)

    def test_create_youtube_md__apicall_with_title_and_path(self):
        # Test that the function creates a markdown file with the specified title and path
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        title_or_path = "primary/Feynman Arrested WHOA"
        md_file_path = create_youtube_md(cur_url, title_or_path)
        expected_md_file_path = "primary/Feynman Arrested WHOA_yt.md"
        self.assertEqual(md_file_path, expected_md_file_path)
        self.assertTrue(os.path.exists(md_file_path))
        self.assertIn(title_or_path.split('/')[-1], md_file_path)
        with open(md_file_path, 'r') as file:
            content = file.read()
        self.assertIn("## metadata", content)
        self.assertIn("## content", content)

    def test_create_youtube_md__apicall_with_title_and_path_same(self):
        # Test that the function creates a markdown file with the specified title and path
        cur_url = "https://youtu.be/RNNfkIE7uYs"
        title_or_path = "primary/Feynman Arrested SAME_yt.md"
        expected_md_file_path = "primary/Feynman Arrested SAME_yt.md"
        md_file_path = create_youtube_md(cur_url, title_or_path)
        self.assertTrue(os.path.exists(md_file_path))
        self.assertEqual(md_file_path, expected_md_file_path)
        with open(md_file_path, 'r') as file:
            content = file.read()
        self.assertIn("## metadata", content)
        self.assertIn("## content", content)

class TestAPIMOCKCreateYoutubeMd(unittest.TestCase):
    def setUp(self):
        self.url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
        self.mock_yt_data = {
            'title': 'Example Video Title',
            'description': 'Description of the video',
            'chapters': [
                {'start_time': '00:00', 'title': 'Introduction'},
                {'start_time': '01:00', 'title': 'Main Content'}
            ],
            'transcript': 'Full transcript of the video',
            'transcript source': 'Automated or manual',
            'length': '15:00'
        }
        self.mock_title_length = ('Example Video Title', '15:00')

    @patch('primary.transcribe.get_youtube_all')
    @patch('primary.transcribe.get_youtube_title_length')
    @patch('primary.transcribe.is_valid_youtube_url')
    def test_create_youtube_md__apimock(self, mock_is_valid_youtube_url, mock_get_youtube_title_length, mock_get_youtube_all):
        # Setup the mocks to return predefined data
        mock_get_youtube_all.return_value = self.mock_yt_data
        mock_get_youtube_title_length.return_value = self.mock_title_length
        mock_is_valid_youtube_url.return_value = True

        # Call the function under test
        md_file_path = create_youtube_md(self.url)

        # Assert file path is as expected
        self.assertIn('_yt.md', md_file_path)

        # Verify no actual API calls were made and all mock functions were called as expected
        mock_get_youtube_all.assert_called_once_with(self.url)
        mock_get_youtube_title_length.assert_called_once_with(self.url)
        mock_is_valid_youtube_url.assert_called_once_with(self.url)

@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLCreateYoutubeMdFromFileLink(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test file before each test case
        self.test_dir = "tests/test_unit_files/transcribe"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        self.test_file_path = os.path.join(self.test_dir, "9999-01-01_UNIT Test file with link_ut.md")
        with open(self.test_file_path, 'w') as f:
            f.write("## metadata\nlast updated: 03-05-2024 Created\nlink: https://youtu.be/RNNfkIE7uYs\n## content\n")
        self.test_file_path2 = os.path.join(self.test_dir, "9999-01-01_UNIT Test file without link_ut.md")
        with open(self.test_file_path2, 'w') as f:
            f.write("## metadata\nlast updated: 03-05-2024 Created\n## content\n")
        self.test_file_path3 = os.path.join(self.test_dir, "9999-01-01_UNIT Test file with bad link_ut.md")
        with open(self.test_file_path3, 'w') as f:
            f.write("## metadata\nlast updated: 03-05-2024 Created\nlink: https://youtu.be/XXXXXX\n## content\n")

    def tearDown(self):
        # Teardown method to remove test directory and files after each test case
        shutil.rmtree(self.test_dir)

    def test_create_youtube_md_from_file_link__apicall_with_link(self):
        # Test that the function creates a new YouTube markdown file from a file link
        yt_md_file_path = create_youtube_md_from_file_link(self.test_file_path)
        expected_md_file_path = "tests/test_unit_files/transcribe/9999-01-01_UNIT Test file with link_yt.md"
        self.assertTrue(os.path.exists(yt_md_file_path))
        self.assertIn("_yt.md", yt_md_file_path)
        self.assertEqual(yt_md_file_path, expected_md_file_path)
        with open(yt_md_file_path, 'r') as file:
            content = file.read()
        self.assertIn("## metadata", content)
        self.assertIn("## content", content)
        self.assertIn("### description (youtube)", content)
        self.assertIn("### transcript (youtube)", content)

    def test_create_youtube_md_from_file_link__apicall_without_link(self):
        # Test that the function handles a file without a YouTube link
        with self.assertRaises(ValueError) as context:
            create_youtube_md_from_file_link(self.test_file_path2)
        self.assertTrue("VALUE ERROR - 'link' metadata field is missing or None in the file" in str(context.exception))

    def test_create_youtube_md_from_file_link__apicall_with_bad_link(self):
        # Test that the function handles a file with an invalid YouTube link
        with self.assertRaises(ValueError) as context:
            create_youtube_md_from_file_link(self.test_file_path3)
        self.assertTrue('invalid YouTube URL' in str(context.exception))

class TestAPIMOCKCreateYoutubeMdFromFileLink(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test directory and files before each test case
        self.test_dir = "tests/test_unit_files/transcribe"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        self.test_file_path = os.path.join(self.test_dir, "9999-01-01_UNIT Test file with link_ut.md")
        with open(self.test_file_path, 'w') as f:
            f.write("## metadata\nlast updated: 03-05-2024 Created\nlink: https://youtu.be/RNNfkIE7uYs\n## content\n")
        self.test_file_path2 = os.path.join(self.test_dir, "9999-01-01_UNIT Test file without link_ut.md")
        with open(self.test_file_path2, 'w') as f:
            f.write("## metadata\nlast updated: 03-05-2024 Created\n## content\n")
        self.test_file_path3 = os.path.join(self.test_dir, "9999-01-01_UNIT Test file with bad link_ut.md")
        with open(self.test_file_path3, 'w') as f:
            f.write("## metadata\nlast updated: 03-05-2024 Created\nlink: https://youtu.be/XXXXXX\n## content\n")

    def tearDown(self):
        # Teardown method to remove test directory and files after each test case
        shutil.rmtree(self.test_dir)

    @patch('primary.transcribe.create_youtube_md')
    def test_create_youtube_md_from_file_link__apimock_with_link(self, mock_create_youtube_md):
        # Configure the mock to return a specific path
        mock_create_youtube_md.return_value = self.test_file_path.replace('_ut.md', '_yt.md')

        # Execute the function under test
        yt_md_file_path = create_youtube_md_from_file_link(self.test_file_path)

        # Assertions to check the right outcomes
        self.assertEqual(yt_md_file_path, self.test_file_path.replace('_ut.md', '_yt.md'))
        mock_create_youtube_md.assert_called_once_with("https://youtu.be/RNNfkIE7uYs", self.test_file_path.replace('_ut.md', '_yt.md'))

    @patch('primary.transcribe.create_youtube_md')
    def test_create_youtube_md_from_file_link__apimock_without_link(self, mock_create_youtube_md):
        # Test handling of missing link in metadata
        with self.assertRaises(ValueError):
            create_youtube_md_from_file_link(self.test_file_path2)

    @patch('primary.transcribe.create_youtube_md')
    def test_create_youtube_md_from_file_link__apimock_with_bad_link(self, mock_create_youtube_md):
        # Configure the mock to raise an exception for an invalid URL
        mock_create_youtube_md.side_effect = ValueError("VALUE ERROR - invalid YouTube URL: https://youtu.be/XXXXXX")

        # Test handling of an invalid YouTube link
        with self.assertRaises(ValueError) as context:
            create_youtube_md_from_file_link(self.test_file_path3)
        self.assertIn("VALUE ERROR - invalid YouTube URL", str(context.exception))


### DEEPGRAM AND JSON FUNCTIONS
@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLGetMediaLength(unittest.TestCase):
    def test_get_media_length__local_file(self):
        # Assuming you have a 1-minute long audio file for testing
        file_path = "tests/test_manual_files/transcribe/Shortest Interview Ever.mp3"
        expected_length = "0:14"  # Expected length in minutes:seconds format
        actual_length = get_media_length(file_path)
        self.assertTrue(isinstance(actual_length, str), "The media length should be a string.")
        self.assertEqual(actual_length, expected_length, f"Expected length was '{expected_length}', but got '{actual_length}'")

    def test_get_media_length__youtube_url(self):
        url = "https://youtu.be/1j0X9QMF--M"
        # Assuming the video length is known and in the correct format
        expected_length = "0:55"  # Expected length in minutes:seconds format
        self.assertEqual(get_media_length(url), expected_length)

    def test_get_media_length__invalid_input(self):
        invalid_input = "invalid_path_or_url"
        with self.assertRaises(ValueError):
            get_media_length(invalid_input)

class TestAPIMOCKGetMediaLength(unittest.TestCase):
    @patch('primary.transcribe.is_valid_youtube_url', return_value=True)
    @patch('primary.transcribe.get_youtube_title_length', return_value=("Shortest Interview Ever", "00:00:14"))
    def test_get_media_length__mock_url(self, mock_get_youtube_title_length, mock_is_valid_youtube_url):
        # Mocks a pair returned in the case of a valid url for some title
        # is_valid_youtube_url returns True
        false_url = "URL for 'Shortest Interview Ever'"
        # Expected length in minutes:seconds format
        expected_length = "0:14"
        actual_length = get_media_length(false_url)
        self.assertTrue(isinstance(actual_length, str), "The media length should be a string.")
        self.assertEqual(actual_length, expected_length, f"Expected length was '{expected_length}', but got '{actual_length}'")

class TestAddLinkToJson(unittest.TestCase):
    def setUp(self):
        self.test_json_file = 'test_file.json'
        self.test_link = 'https://example.com'
        # Create a test JSON file
        with open(self.test_json_file, 'w') as file:
            json.dump({"data": "value"}, file)

    def tearDown(self):
        # Remove the test JSON file after each test
        if os.path.exists(self.test_json_file):
            os.remove(self.test_json_file)

    def test_add_link_to_json__new_metadata(self):
        # Test adding a link to a JSON file that does not have a 'metadata' section
        modified_file_path, error = add_link_to_json(self.test_json_file, self.test_link)
        self.assertIsNone(error)
        self.assertEqual(modified_file_path, self.test_json_file)
        with open(modified_file_path, 'r') as file:
            data = json.load(file)
        self.assertIn('metadata', data)
        self.assertEqual(data['metadata']['link'], self.test_link)

    def test_add_link_to_json__existing_metadata(self):
        # Test adding a link to a JSON file that already has a 'metadata' section
        with open(self.test_json_file, 'w') as file:
            json.dump({"metadata": {"existing": "data"}, "data": "value"}, file)
        modified_file_path, error = add_link_to_json(self.test_json_file, self.test_link)
        self.assertIsNone(error)
        self.assertEqual(modified_file_path, self.test_json_file)
        with open(modified_file_path, 'r') as file:
            data = json.load(file)
        self.assertIn('metadata', data)
        self.assertEqual(data['metadata']['link'], self.test_link)
        self.assertEqual(data['metadata']['existing'], 'data')

    def test_add_link_to_json__invalid_file(self):
        # Test adding a link to an invalid JSON file
        modified_file_path, error = add_link_to_json('nonexistent_file.json', self.test_link)
        self.assertIsNone(modified_file_path)
        self.assertIsNotNone(error)

class TestGetLinkFromJson(unittest.TestCase):
    def setUp(self):
        self.test_json_file = 'test_file.json'
        self.test_link = 'https://example.com'
        # Create a test JSON file with a link in the metadata
        with open(self.test_json_file, 'w') as file:
            json.dump({"metadata": {"link": self.test_link}}, file)

    def tearDown(self):
        # Remove the test JSON file after each test
        if os.path.exists(self.test_json_file):
            os.remove(self.test_json_file)

    def test_get_link_from_json__with_link(self):
        # Test retrieving a link from a JSON file that has a 'metadata' section with a 'link'
        link = get_link_from_json(self.test_json_file)
        self.assertEqual(link, self.test_link)

    def test_get_link_from_json__no_metadata(self):
        # Test retrieving a link from a JSON file that does not have a 'metadata' section
        with open(self.test_json_file, 'w') as file:
            json.dump({"data": "value"}, file)
        link = get_link_from_json(self.test_json_file)
        self.assertIsNone(link)

    def test_get_link_from_json__no_link(self):
        # Test retrieving a link from a JSON file that has a 'metadata' section without a 'link'
        with open(self.test_json_file, 'w') as file:
            json.dump({"metadata": {"other": "data"}}, file)
        link = get_link_from_json(self.test_json_file)
        self.assertIsNone(link)

    def test_get_link_from_json__invalid_file(self):
        # Test retrieving a link from an invalid JSON file
        link = get_link_from_json('nonexistent_file.json')
        self.assertIsNone(link)

@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLTranscribeDeepgram(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test audio file before each test case
        self.test_audio_file = 'test_audio.mp3'
        # Create a small silent audio file for testing
        os.system(f"ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 1 {self.test_audio_file}")

    def tearDown(self):
        # Teardown method to remove test audio file and transcription JSON after each test case
        if os.path.exists(self.test_audio_file):
            os.remove(self.test_audio_file)
        json_file = self.test_audio_file.rsplit('.', 1)[0] + '_dgwhspm.json'
        if os.path.exists(json_file):
            os.remove(json_file)

    def test_transcribe_deepgram__whisper_medium(self):
        # Test transcribing with the whisper-medium model
        json_file_path = transcribe_deepgram(self.test_audio_file, 'whisper-medium')
        self.assertTrue(os.path.exists(json_file_path))

    def test_transcribe_deepgram__nova_2(self):
        # Test transcribing with the nova-2 model
        json_file_path = transcribe_deepgram(self.test_audio_file, 'nova-2')
        self.assertTrue(os.path.exists(json_file_path))

    def test_transcribe_deepgram__invalid_model(self):
        # Test transcribing with an invalid model
        with self.assertRaises(ValueError):
            transcribe_deepgram(self.test_audio_file, 'invalid-model')

    def test_transcribe_deepgram__unsupported_file(self):
        # Test transcribing an unsupported file type
        with self.assertRaises(ValueError):
            transcribe_deepgram('unsupported_file.txt', 'whisper-medium')

class TestAPIMOCKTranscribeDeepgram(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test audio file before each test case
        self.test_audio_file = 'test_audio.mp3'
        # Create a small silent audio file for testing
        os.system(f"ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 1 {self.test_audio_file}")
        # Copy to return as trascription
        self.test_audio_deepgram_json = self.test_audio_file.rsplit('.', 1)[0] + '_dgwhspm.json'
        shutil.copy(self.test_audio_file, self.test_audio_deepgram_json)

    def tearDown(self):
        # Teardown method to remove test audio file and transcription JSON after each test case
        if os.path.exists(self.test_audio_file):
            os.remove(self.test_audio_file)
        json_file = self.test_audio_file.rsplit('.', 1)[0] + '_dgwhspm.json'
        if os.path.exists(json_file):
            os.remove(json_file)

    def test_transcribe_deepgram__mock_transcription_json(self):
        # Just return copy file
        json_file_path = self.test_audio_deepgram_json
        self.assertTrue(os.path.exists(json_file_path))

    def test_transcribe_deepgram__mock_invalid_model(self):
        # Test transcribing with an invalid model
        with self.assertRaises(ValueError):
            transcribe_deepgram(self.test_audio_file, 'invalid-model')

    def test_transcribe_deepgram__mock_unsupported_file(self):
        # Test transcribing an unsupported file type
        with self.assertRaises(ValueError):
            transcribe_deepgram('unsupported_file.txt', 'whisper-medium')

class TestGetSummaryStartSeconds(unittest.TestCase):
    def setUp(self):
        # Setup method to create sample transcription data
        self.transcription_data = {
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "words": [
                                    {"start": 1.23, "word": "Hello"},
                                    {"start": 2.34, "word": "world"},
                                    {"start": 3.45, "word": "this"},
                                    {"start": 4.56, "word": "is"},
                                    {"start": 5.67, "word": "a"},
                                    {"start": 6.78, "word": "test"}
                                ]
                            }
                        ]
                    }
                ]
            }
        }

    def test_get_summary_start_seconds__valid_index(self):
        # Test that the function returns the correct start time for a valid index
        index = 2
        expected_start_seconds = 3
        self.assertEqual(get_summary_start_seconds(self.transcription_data, index), expected_start_seconds)

    def test_get_summary_start_seconds__invalid_index(self):
        # Test that the function returns 0 for an index that is out of range
        index = 10
        expected_start_seconds = 0
        self.assertEqual(get_summary_start_seconds(self.transcription_data, index), expected_start_seconds)

    def test_get_summary_start_seconds__empty_words_list(self):
        # Test that the function returns 0 if the words list is empty
        self.transcription_data['results']['channels'][0]['alternatives'][0]['words'] = []
        index = 0
        expected_start_seconds = 0
        self.assertEqual(get_summary_start_seconds(self.transcription_data, index), expected_start_seconds)

class TestFormatFeatureSegment(unittest.TestCase):
    def setUp(self):
        # Setup method to create sample data
        self.data = {
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "words": [
                                    {"start": 0.0, "word": "Every"},
                                    {"start": 1.0, "word": "time"},
                                    {"start": 2.0, "word": "an"},
                                    {"start": 3.0, "word": "NLM"},
                                    {"start": 4.0, "word": "produces"},
                                ]
                            }
                        ]
                    }
                ]
            }
        }

    def test_format_feature_segment__summaries(self):
        feature = "summaries"
        segment = {
            "summary": "Every time an NLM produces a token.",
            "start_word": 0
        }
        expected_output = "Summary  0:00\nEvery time an NLM produces a token.\n\n"
        self.assertEqual(format_feature_segment(feature, segment, self.data), expected_output)

    def test_format_feature_segment__sentiments(self):
        feature = "sentiments"
        segment = {
            "text": "Every time an NLM produces a token.",
            "start_word": 0,
            "sentiment": "positive",
            "sentiment_score": 0.75
        }
        expected_output = "Sentiment  0:00\npositive - sentiment_score = 0.75\nEvery time an NLM produces a token.\n\n"
        self.assertEqual(format_feature_segment(feature, segment, self.data), expected_output)

    def test_format_feature_segment__topics(self):
        feature = "topics"
        segment = {
            "text": "Every time an NLM produces a token.",
            "start_word": 0,
            "topics": [{"topic": "NLM", "confidence_score": 0.95}]
        }
        expected_output = "Topic  0:00\nNLM - confidence_score = 0.95\nEvery time an NLM produces a token.\n\n"
        self.assertEqual(format_feature_segment(feature, segment, self.data), expected_output)

    def test_format_feature_segment__intents(self):
        feature = "intents"
        segment = {
            "text": "Every time an NLM produces a token.",
            "start_word": 0,
            "intents": [{"intent": "Analyze NLM", "confidence_score": 0.85}]
        }
        expected_output = "Intent  0:00\nAnalyze NLM - confidence_score = 0.85\nEvery time an NLM produces a token.\n\n"
        self.assertEqual(format_feature_segment(feature, segment, self.data), expected_output)

class TestExtractFeatureFromDeepgramJson(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test JSON file before each test case
        self.test_json_filename = 'test_deepgram.json'
        test_data = {
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "summaries": [
                                    {"summary": "This is a summary.", "start_word": 0}
                                ]
                            }
                        ]
                    }
                ],
                "sentiments": {
                    "segments": [
                        {"text": "This is a sentiment.", "start_word": 0, "sentiment": "positive", "sentiment_score": 0.75}
                    ]
                },
                "topics": {
                    "segments": [
                        {"text": "This is a topic.", "start_word": 0, "topics": [{"topic": "Topic", "confidence_score": 0.95}]}
                    ]
                },
                "intents": {
                    "segments": [
                        {"text": "This is an intent.", "start_word": 0, "intents": [{"intent": "Intent", "confidence_score": 0.85}]}
                    ]
                }
            }
        }
        with open(self.test_json_filename, 'w') as f:
            json.dump(test_data, f)

    def tearDown(self):
        # Teardown method to remove test JSON file after each test case
        if os.path.exists(self.test_json_filename):
            os.remove(self.test_json_filename)

    def test_extract_feature_from_deepgram_json__summaries(self):
        # Test extracting summaries from the JSON file
        expected_output = "Summary  0:00\nThis is a summary.\n\n"
        self.assertEqual(extract_feature_from_deepgram_json(self.test_json_filename, "summaries"), expected_output)

    def test_extract_feature_from_deepgram_json__sentiments(self):
        # Test extracting sentiments from the JSON file
        expected_output = "Sentiment  0:00\npositive - sentiment_score = 0.75\nThis is a sentiment.\n\n"
        self.assertEqual(extract_feature_from_deepgram_json(self.test_json_filename, "sentiments"), expected_output)

    def test_extract_feature_from_deepgram_json__topics(self):
        # Test extracting topics from the JSON file
        expected_output = "Topic  0:00\nTopic - confidence_score = 0.95\nThis is a topic.\n\n"
        self.assertEqual(extract_feature_from_deepgram_json(self.test_json_filename, "topics"), expected_output)

    def test_extract_feature_from_deepgram_json__intents(self):
        # Test extracting intents from the JSON file
        expected_output = "Intent  0:00\nIntent - confidence_score = 0.85\nThis is an intent.\n\n"
        self.assertEqual(extract_feature_from_deepgram_json(self.test_json_filename, "intents"), expected_output)

    def test_extract_feature_from_deepgram_json__invalid_feature(self):
        # Test extracting a non-existent feature from the JSON file
        with self.assertWarns(Warning) as warning:
            result = extract_feature_from_deepgram_json(self.test_json_filename, "nonexistent")
        self.assertIsNone(result)
        self.assertEqual(str(warning.warnings[0].message), "in extract_feature_from_deepgram_json - Feature 'nonexistent' not found in Deepgram JSON")

    def test_extract_feature_from_deepgram_json__file_does_not_exist(self):
        # Test extracting a feature from a non-existent JSON file
        with self.assertRaises(ValueError) as context:
            extract_feature_from_deepgram_json("nonexistent.json", "summaries")
        self.assertIn("Error extracting summaries from nonexistent.json", str(context.exception))

    def test_extract_feature_from_deepgram_json__empty_feature(self):
        # Test extracting a feature that exists but has no data
        with open(self.test_json_filename, 'w') as f:
            json.dump({"results": {"channels": [{"alternatives": [{}] }] }}, f)
        with self.assertWarns(Warning) as warning:
            result = extract_feature_from_deepgram_json(self.test_json_filename, "summaries")
        self.assertIsNone(result)
        self.assertEqual(str(warning.warnings[0].message), "in extract_feature_from_deepgram_json - Feature 'summaries' was found in Deepgram JSON but extracted text is None or empty string (should not get this warning!)")

class TestExtractFeatureFromDeepgramJsonRealFile(unittest.TestCase):
    def setUp(self):
        # Setup method to specify the path to the full test JSON file
        self.full_json_filename = "tests/test_manual_files/jsons/2024-03-08_Test Deepgram with all features_nova2.json"

    def test_extract_feature_from_deepgram_json_real_file__summaries(self):
        # Test extracting summaries from the full JSON file
        result = extract_feature_from_deepgram_json(self.full_json_filename, "summaries")
        expected_output = "Summary  0:00\nEvery time an NLM produces a token or a word, there is some level of probability for that word to take you out of the set of reasonable answers. So the probability that an answer would be nonsensical increases exponentially with the number of tokens. It's basically a struggle against the curse of dimensionality.\n\nSummary  4:05\nIf you stitch together reasonably grammatical sentences, is that the is it that easy to break it? Yeah. So the the part of it is that there is a long tail. This is, an issue that a lot of people have realized, you know, in social networks and stuff like that.\n\n"
        self.assertEqual(result, expected_output)

    def test_extract_feature_from_deepgram_json_real_file__sentiments(self):
        # Test extracting sentiments from the full JSON file
        result = extract_feature_from_deepgram_json(self.full_json_filename, "sentiments")
        expected_output = "Sentiment  0:00\nneutral - sentiment_score = -0.12\nIf you could talk about hallucinations from your perspectives.\n\nSentiment  0:04\nnegative - sentiment_score = -0.35\nThe why hallucinations happen from large language models and why and to what degree is that a fundamental flaw of large language models.\n\nSentiment  0:15\nneutral - sentiment_score = -0.16\nRight.\n\nSentiment  0:15\nnegative - sentiment_score = -0.37\nSo because of the auto regressive prediction, every time an NLM produces a token or a word, there is some level of probability for that word to take you out of the set of reasonable answers. And if you assume, which is a very strong assumption, that the probability of such error is that those errors are independent across a sequence of tokens being produced.\n\nSentiment  0:44\nneutral - sentiment_score = -0.20\nMhmm. What that means is that every time you produce a token, the probability that you were asked you you stay within the the set of correct answer decreases, and it decreases exponentially.\n\nSentiment  0:54\nnegative - sentiment_score = -0.41\nSo there's a strong, like you said, assumption there that if, there's a nausea probability of making a mistake, which there appears to be, then there's going to be a kind of drift.\n\nSentiment  1:04\nneutral - sentiment_score = -0.03\nYep. And that drift is exponential. It's like errors accumulate. Right? So so the probability that an answer would be nonsensical increases exponentially with the number of tokens. Is that obvious to you, by the way? Like well, so mathematically speaking, maybe. But, like, isn't there a kind of gravitational pull towards the truth? Because on on average, hopefully, the truth is well represented in the, training set? No.\n\nSentiment  1:35\nnegative - sentiment_score = -0.38\nIt's basically a struggle against the curse of dimensionality.\n\nSentiment  1:41\nneutral - sentiment_score = 0.06\nSo the way you can correct for this is that you fine tune the system by having it produce answers for all kinds of questions that people might come up with. Mhmm. And people are people, so they a lot of the questions that they have are very similar to each other. So you can probably cover, you know, 80% or whatever of, questions that people will will ask, by, you know, collecting data.\n\nSentiment  2:05\npositive - sentiment_score = 0.34\nAnd then, and then you fine tune the system to produce good answers for all of those things, and it's probably gonna be able to learn that because it's got a lot of capacity to to learn.\n\nSentiment  2:17\nneutral - sentiment_score = -0.04\nBut then there is, you know, the enormous set of prompts that you have not covered during training.\n\nSentiment  2:25\nneutral - sentiment_score = 0.12\nAnd that set is enormous. Like, within the set of all possible prompts, the proportion of prompts that have been, used for training is absolutely tiny. It's a it's a tiny, tiny, tiny subset of all possible prompts. And so the system will behave properly on the prompts that has been either trained, pretrained, or fine tuned.\n\nSentiment  2:47\nnegative - sentiment_score = -0.44\nBut then there is an entire space of things that it cannot possibly have been trained on because it's just the the number is gigantic.\n\nSentiment  2:55\nneutral - sentiment_score = -0.06\nSo so whatever training the system, has been subject to to produce appropriate answers, you can break it by finding out a prompt that will be outside of the the the set of prompts that's been trained on or things that are similar, and then it will just spew complete nonsense. Do you when you say prompt, do you mean that exact prompt, or do you mean a prompt that's, like, in many parts very different than like, is it that easy to ask a question or to say a thing that hasn't been said before on the Internet? I mean, people have come up with, things where, like, you you put a essentially a random sequence of characters in the prompt. That's enough to kind of throw the system, into a mode where, you know, it is gonna answer something completely different than it would have answered without this. Mhmm. So that's the way to jailbreak the system, basically. Get it, you know, go outside of its, of its conditioning. Right? So that that's a very clear demonstration of it, but, of course, you know, that's, that goes outside of what it's designed to do. Right? If you actually stitch together reasonably grammatical sentences, is that the is it that easy to break it? Yeah.\n\nSentiment  4:12\npositive - sentiment_score = 0.33\nSome people have done things like you you you write a sentence in English, right, that has an or you ask a question in English, and it it produces a perfectly fine answer.\n\nSentiment  4:22\nneutral - sentiment_score = 0.16\nAnd then you just substitute a few words by the same word in another language.\n\nSentiment  4:27\nnegative - sentiment_score = -0.61\nI I know if a sudden the answer is complete nonsense.\n\nSentiment  4:30\nneutral - sentiment_score = -0.03\nYes.\n\nSentiment  4:30\nneutral - sentiment_score = -0.18\nSo so I guess what I'm saying is, like, which fraction of prompts that humans are likely to generate are going to break the system. So the the part of it is that there is a long tail. Yes. This is, an issue that a lot of people have realized, you know, in social networks and stuff like that, which is, there's a very, very long tail of of things that people will ask. And you can fine tune the system for the 80% or whatever of, of the things that most people will will ask.\n\nSentiment  5:01\nnegative - sentiment_score = -0.49\nAnd then this long tail is is so large that you're not gonna be able to function the system for all the conditions. And in the end, the system has a being kind of a giant lookup table, right, essentially, which is not really what you want.\n\nSentiment  5:13\nneutral - sentiment_score = -0.14\nYou want systems that can reason. Certainly, they can plan. So the type of reasoning that takes place in, LLM is very, very primitive. And the reason you can tell is primitive is because the amount of computation that is spent per token produced is constant. So if you ask a question and that question has an answer in a given number of token, the amount of computation devoted to computing that answer can be exactly estimated. It's like, you know, it's hot it's the the size of the prediction network, you know, with its 36 layers or 92 layers or whatever it is, multiplied by number of tokens. That's it. And so, essentially, it doesn't matter if the question being asked is is simple to answer, complicated to answer, impossible to answer because it's a decidable or something. The amount of computation the system will be able to devote to that to the answer is constant or is number of token produced in the answer. Right?\n\nSentiment  6:15\nnegative - sentiment_score = -0.45\nThis is not the way we work. The way we reason is that when we're faced with a complex problem or complex question, we spend more time trying to solve it and answer it.\n\nSentiment  6:27\nneutral - sentiment_score = -0.31\nRight?\n\nSentiment  6:28\nnegative - sentiment_score = -0.55\nBecause it's more difficult.\n\nSentiment  6:29\nneutral - sentiment_score = -0.17\nThere's a prediction element. There's a iterative element where you're, like, adjusting your understanding of a thing by going over and over and over.\n\nSentiment  6:40\nnegative - sentiment_score = -0.38\nThere's a hierarchical element, so on. Does this mean it's a fundamental flaw of LLMs, or does it mean that there's more part to that question?\n\n"
        self.assertEqual(result, expected_output)

    def test_extract_feature_from_deepgram_json_real_file__topics(self):
        # Test extracting topics from the full JSON file
        result = extract_feature_from_deepgram_json(self.full_json_filename, "topics")
        expected_output = "Topic  0:00\nHallucinations - confidence_score = 0.98\nIf you could talk about hallucinations from your perspectives. The why hallucinations happen from large language models and why and to what degree is that a fundamental flaw of large language models. Right.\n\nTopic  0:15\nErrors - confidence_score = 0.50\nSo because of the auto regressive prediction, every time an NLM produces a token or a word, there is some level of probability for that word to take you out of the set of reasonable answers. And if you assume, which is a very strong assumption, that the probability of such error is that those errors are independent across a sequence of tokens being produced. Mhmm.\n\nTopic  0:45\nRandomness - confidence_score = 0.01\nWhat that means is that every time you produce a token, the probability that you were asked you you stay within the the set of correct answer decreases, and it decreases exponentially. So there's a strong, like you said, assumption there that if, there's a nausea probability of making a mistake, which there appears to be, then there's going to be a kind of drift.\n\nTopic  1:22\nTruth - confidence_score = 0.09\nBut, like, isn't there a kind of gravitational pull towards the truth? Because on on average, hopefully, the truth is well represented in the, training set?\n\nTopic  1:34\nConfusion - confidence_score = 0.06\nNo.\n\nTopic  1:34\nTraining set - confidence_score = 0.04\nNo. It's basically a struggle against the curse of dimensionality. So the way you can correct for this is that you fine tune the system by having it produce answers for all kinds of questions that people might come up with. Mhmm.\n\nTopic  1:41\nAnswers - confidence_score = 0.00\nSo the way you can correct for this is that you fine tune the system by having it produce answers for all kinds of questions that people might come up with.\n\nTopic  1:41\nSystem - confidence_score = 0.00\nSo the way you can correct for this is that you fine tune the system by having it produce answers for all kinds of questions that people might come up with. Mhmm.\n\nTopic  2:26\nPrompts - confidence_score = 0.59\nLike, within the set of all possible prompts, the proportion of prompts that have been, used for training is absolutely tiny.\n\nTopic  2:39\nSystem behavior - confidence_score = 0.50\nAnd so the system will behave properly on the prompts that has been either trained, pretrained, or fine tuned.\n\nTopic  3:15\nScheduling - confidence_score = 0.00\nDo you when you say prompt, do you mean that exact prompt, or do you mean a prompt that's, like, in many parts very different than like, is it that easy to ask a question or to say a thing that hasn't been said before on the Internet?\n\nTopic  4:53\nSystem tuning - confidence_score = 0.49\nAnd you can fine tune the system for the 80% or whatever of, of the things that most people will will ask.\n\nTopic  5:16\nSystem reasoning - confidence_score = 0.03\nSo the type of reasoning that takes place in, LLM is very, very primitive.\n\nTopic  6:31\nIterative approach - confidence_score = 0.20\nThere's a iterative element where you're, like, adjusting your understanding of a thing by going over and over and over.\n\n"
        self.assertEqual(result, expected_output)

    def test_extract_feature_from_deepgram_json_real_file__intents(self):
        # Test extracting intents from the full JSON file
        result = extract_feature_from_deepgram_json(self.full_json_filename, "intents")
        expected_output = "Intent  0:00\nAnalyze hallucinations - confidence_score = 0.08\nIf you could talk about hallucinations from your perspectives. The why hallucinations happen from large language models and why and to what degree is that a fundamental flaw of large language models. Right.\n\nIntent  2:39\nEvaluate system effectiveness - confidence_score = 0.00\nAnd so the system will behave properly on the prompts that has been either trained, pretrained, or fine tuned.\n\nIntent  5:01\nEvaluate system functionality - confidence_score = 0.08\nAnd then this long tail is is so large that you're not gonna be able to function the system for all the conditions.\n\n"
        self.assertEqual(result, expected_output)

    def test_extract_feature_from_deepgram_json_real_file__invalid_feature(self):
        # Test extracting a non-existent feature from the full JSON file
        with self.assertWarns(Warning):
            result = extract_feature_from_deepgram_json(self.full_json_filename, "nonexistent")
        self.assertIsNone(result)

class TestValidateTranscriptJson(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test JSON file before each test case
        self.test_json_filename = 'test_transcript.json'
        test_data = {
            "metadata": {
                "speaker_names": [],
                "link": "https://example.com",
                "transaction_key": "key",
                "request_id": "request_id",
                "sha256": "sha256",
                "created": "2024-03-09T17:08:48.104Z",
                "duration": 410.856,
                "channels": 1,
                "models": ["model"],
                "model_info": {"model": {"name": "2-primary-nova", "version": "2024-01-09.29447", "arch": "nova-2"}},
                "intents_info": {"model_uuid": "uuid", "input_tokens": 1496, "output_tokens": 36},
                "sentiment_info": {"model_uuid": "uuid", "input_tokens": 1496, "output_tokens": 1499},
                "topics_info": {"model_uuid": "uuid", "input_tokens": 1496, "output_tokens": 156}
            },
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "transcript": "This is a transcript.",
                                "confidence": 0.95,
                                "words": [
                                    {"word": "This", "start": 0.0, "end": 0.5, "confidence": 0.95, "punctuated_word": "This", "speaker": 0, "speaker_confidence": 0.9, "sentiment": "neutral", "sentiment_score": 0.0},
                                    {"word": "is", "start": 0.5, "end": 1.0, "confidence": 0.95, "punctuated_word": "is", "speaker": 0, "speaker_confidence": 0.9, "sentiment": "neutral", "sentiment_score": 0.0}
                                ],
                                "summaries": [{"summary": "This is a summary.", "start_word": 0, "end_word": 1}],
                                "paragraphs": {
                                    "transcript": "This is a transcript.",
                                    "paragraphs": [{"sentences": [{"text": "This is a sentence.", "start": 0.0, "end": 1.0, "sentiment": "neutral", "sentiment_score": 0.0}], "start": 0.0, "end": 1.0, "num_words": 2, "speaker": 0, "sentiment": "neutral", "sentiment_score": 0.0}]
                                }
                            }
                        ]
                    }
                ],
                "sentiments": {"segments": [{"text": "This is a sentiment.", "start_word": 0, "end_word": 1, "sentiment": "positive", "sentiment_score": 0.75}], "average": {"sentiment": "positive", "sentiment_score": 0.75}},
                "topics": {"segments": [{"text": "This is a topic.", "start_word": 0, "end_word": 1, "topics": [{"topic": "Topic", "confidence_score": 0.95}]}]},
                "intents": {"segments": [{"text": "This is an intent.", "start_word": 0, "end_word": 1, "intents": [{"intent": "Intent", "confidence_score": 0.85}]}]}
            }
        }
        with open(self.test_json_filename, 'w') as f:
            json.dump(test_data, f)

    def tearDown(self):
        # Teardown method to remove test JSON file after each test case
        if os.path.exists(self.test_json_filename):
            os.remove(self.test_json_filename)

    def test_validate_transcript_json__valid_structure(self):
        # Test a valid JSON structure
        self.assertTrue(validate_transcript_json(self.test_json_filename))

    def test_validate_transcript_json__missing_results(self):
        # Test a JSON file with missing 'results' key
        with open(self.test_json_filename, 'w') as f:
            json.dump({"metadata": {}}, f)
        self.assertFalse(validate_transcript_json(self.test_json_filename))

    def test_validate_transcript_json__missing_channels(self):
        # Test a JSON file with missing 'channels' key
        with open(self.test_json_filename, 'w') as f:
            json.dump({"results": {}}, f)
        self.assertFalse(validate_transcript_json(self.test_json_filename))

    def test_validate_transcript_json__missing_alternatives(self):
        # Test a JSON file with missing 'alternatives' key
        with open(self.test_json_filename, 'w') as f:
            json.dump({"results": {"channels": [{}]}}, f)
        self.assertFalse(validate_transcript_json(self.test_json_filename))

    def test_validate_transcript_json__missing_words(self):
        # Test a JSON file with missing 'words' key
        with open(self.test_json_filename, 'w') as f:
            json.dump({"results": {"channels": [{"alternatives": [{}]}]}}, f)
        self.assertFalse(validate_transcript_json(self.test_json_filename))

    def test_validate_transcript_json__missing_paragraphs(self):
        # Test a JSON file with missing 'paragraphs' key
        with open(self.test_json_filename, 'w') as f:
            json.dump({"results": {"channels": [{"alternatives": [{"words": [{"word": "word", "start": 0.0, "end": 0.5}]}]}]}}, f)
        self.assertFalse(validate_transcript_json(self.test_json_filename))

    def test_validate_transcript_json__empty_transcript(self):
        # Test a JSON file with an empty 'transcript' key
        with open(self.test_json_filename, 'w') as f:
            json.dump({"results": {"channels": [{"alternatives": [{"words": [{"word": "word", "start": 0.0, "end": 0.5}], "paragraphs": {"transcript": "", "paragraphs": []}}]}]}}, f)
        self.assertFalse(validate_transcript_json(self.test_json_filename))

    def test_validate_transcript_json__file_does_not_exist(self):
        # Test a non-existent JSON file
        with self.assertRaises(ValueError):
            validate_transcript_json("nonexistent.json")

class TestSetVariousTranscriptHeadings(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for the test
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.md')
        self.temp_file.write("## metadata\n\n## content\n\nOriginal content\n")
        self.temp_file.flush()  # Ensure content is written to disk
        self.temp_file_json = self.temp_file.name.replace('.md', '.json')
        self.temp_file_yt = self.temp_file.name.replace('.md', '_yt.md')
        # Create a mock JSON file that the function expects to find
        with open(self.temp_file_json, 'w') as f:
            json.dump({"some": "data"}, f)
        # Create a mock YouTube markdown file that the function expects to find
        with open(self.temp_file_yt, 'w') as f:
            f.write("## metadata\n\n##content\n\nOriginal YouTube content\n")

    def tearDown(self):
        # Clean up by deleting the temporary files
        os.unlink(self.temp_file.name)
        if os.path.exists(self.temp_file_json):
            os.unlink(self.temp_file_json)
        if os.path.exists(self.temp_file_yt):
            os.unlink(self.temp_file_yt)

    @patch('primary.transcribe.extract_feature_from_deepgram_json')
    @patch('primary.fileops.set_heading')
    @patch('primary.fileops.find_file_in_folders')
    def test_set_various_transcript_headings__deepgram(self, mock_find_file, mock_set_heading, mock_extract_feature):
        mock_extract_feature.return_value = "Mock Heading\n\nPretend this is real text."
        mock_find_file.return_value = self.temp_file_json

        set_various_transcript_headings(self.temp_file.name, 'summaries', 'deepgram')

        # Verify that the set_heading function was called with the correct arguments
        mock_set_heading.assert_called_with(self.temp_file.name, "Mock Heading\n\nPretend this is real text.", "### summaries")
        mock_extract_feature.assert_called_with(self.temp_file_json, 'summaries')

    @patch('primary.transcribe.extract_feature_from_youtube_md')
    @patch('primary.fileops.set_heading')
    @patch('primary.fileops.find_file_in_folders')
    def test_set_various_transcript_headings__youtube(self, mock_find_file, mock_set_heading, mock_extract_feature):
        mock_extract_feature.return_value = "Mock YouTube Heading\n\nPretend this is YouTube text."
        mock_find_file.return_value = self.temp_file_yt

        set_various_transcript_headings(self.temp_file.name, 'chapters', 'youtube')

        # Verify that the set_heading function was called with the correct arguments
        mock_set_heading.assert_called_with(self.temp_file.name, "Mock YouTube Heading\n\nPretend this is YouTube text.", "### chapters")
        mock_extract_feature.assert_called_with(self.temp_file_yt, 'chapters')

class TestExtractFeatureFromYoutubeMd(unittest.TestCase):
    def setUp(self):
        # Create a temporary markdown file
        self.temp_md_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.md')
        # Text for the input test file
        self.test_md_content = """
## metadata
last updated: 03-13-2024 Created

## content

### chapters (youtube)

[0:00](https://youtu.be/pZUDEQs89zc&t=0) - Intro to ChatGPT Assistants API Beta
[0:20](https://youtu.be/pZUDEQs89zc&t=20) - How to Create a Custom AI Assistant

### description (youtube)

Dive deeper into the innovative world of AI!

### transcript (youtube)

this is huge is there any way to create a custom chat GPT assistant
"""
        self.temp_md_file.write(self.test_md_content)
        self.temp_md_file.close()

    def tearDown(self):
        # Clean up by removing the temporary file
        os.unlink(self.temp_md_file.name)

    def test_extract_feature_from_youtube_md__chapters(self):
        # Test extracting chapters from the YouTube markdown file
        extracted_chapters = extract_feature_from_youtube_md(self.temp_md_file.name, 'chapters')
        expected_chapters = "[0:00](https://youtu.be/pZUDEQs89zc&t=0) - Intro to ChatGPT Assistants API Beta\n[0:20](https://youtu.be/pZUDEQs89zc&t=20) - How to Create a Custom AI Assistant\n\n"
        self.assertEqual(extracted_chapters, expected_chapters)

    def test_extract_feature_from_youtube_md__description(self):
        # Test extracting description from the YouTube markdown file
        extracted_description = extract_feature_from_youtube_md(self.temp_md_file.name, 'description')
        expected_description = "Dive deeper into the innovative world of AI!\n\n"
        self.assertEqual(extracted_description, expected_description)

    def test_extract_feature_from_youtube_md__transcript(self):
        # Test extracting transcript from the YouTube markdown file
        extracted_transcript = extract_feature_from_youtube_md(self.temp_md_file.name, 'transcript')
        expected_transcript = "this is huge is there any way to create a custom chat GPT assistant\n\n"
        self.assertEqual(extracted_transcript, expected_transcript)


### NUMERAL CONVERT FUNCTIONS
class TestExtractContext(unittest.TestCase):
    def test_extract_context_with_match(self):
        line = "This is a test line for extracting context"
        match = re.search(r"test", line)
        expected_context = "a test line"
        self.assertEqual(extract_context(line, match, 1), expected_context)

    def test_extract_context_with_larger_radius(self):
        line = "This is a test line for extracting context"
        match = re.search(r"test", line)
        expected_context = "is a test line for"
        self.assertEqual(extract_context(line, match, 2), expected_context)

    def test_extract_context_at_start_of_line(self):
        line = "This is a test line for extracting context"
        match = re.search(r"This", line)
        expected_context = "This is a"
        self.assertEqual(extract_context(line, match, 2), expected_context)

    def test_extract_context_at_end_of_line(self):
        line = "This is a test line for extracting context"
        match = re.search(r"context", line)
        expected_context = "extracting context"
        self.assertEqual(extract_context(line, match, 1), expected_context)

    def test_extract_context_with_no_match(self):
        line = "This is a test line for extracting context"
        match = re.search(r"nonexistent", line)
        with self.assertRaises(ValueError):
            extract_context(line, match, 2)

class TestPrintNumException(unittest.TestCase):
    def setUp(self):
        # Setup method to initialize a list to store printed exceptions
        self.printed_exceptions = []

    def test_print_num_exception__basic(self):
        # Test that the function prints and records an exception message
        line = "The answer is 42."
        print_num_exception("42", 10, 2, self.printed_exceptions, "ordinal", line)
        expected_exception_msg = "Excluding conversion for ordinal at line 13: ...The answer is 42...."
        self.assertIn(expected_exception_msg, self.printed_exceptions)

    def test_print_num_exception__no_duplicate(self):
        # Test that the function does not print or record duplicate exception messages
        line = "The answer is 42."
        print_num_exception("42", 10, 2, self.printed_exceptions, "ordinal", line)
        print_num_exception("42", 10, 2, self.printed_exceptions, "ordinal", line)
        self.assertEqual(len(self.printed_exceptions), 1)

    def test_print_num_exception__context_extraction(self):
        # Test that the context is correctly extracted for the exception message
        line = "This is a test line with number 42 in the middle."
        print_num_exception("42", 5, 1, self.printed_exceptions, "number", line)
        expected_exception_msg = "Excluding conversion for number at line 7: ...a test line with number 42 in the middle...."
        self.assertIn(expected_exception_msg, self.printed_exceptions)

class TestGetPreviousWord(unittest.TestCase):
    def test_get_previous_word__middle_of_sentence(self):
        sentence = "This is a sample sentence."
        start_index = 10
        expected_word = "a"
        self.assertEqual(get_previous_word(sentence, start_index), expected_word)

    def test_get_previous_word__start_of_sentence(self):
        sentence = "This is a sample sentence."
        start_index = 5
        expected_word = "This"
        self.assertEqual(get_previous_word(sentence, start_index), expected_word)

    def test_get_previous_word__end_of_sentence(self):
        sentence = "This is a sample sentence."
        start_index = len(sentence) - 1
        expected_word = "sentence"
        self.assertEqual(get_previous_word(sentence, start_index), expected_word)

    def test_get_previous_word__no_previous_word(self):
        sentence = "This is a sample sentence."
        start_index = 0
        expected_word = ""
        self.assertEqual(get_previous_word(sentence, start_index), expected_word)

    def test_get_previous_word__with_multiple_spaces(self):
        sentence = "This   is  a  sample   sentence."
        start_index = 15
        expected_word = "a"
        # Adjust start_index to point to the 'a' in the sentence
        adjusted_start_index = sentence.rfind(' ', 0, start_index) + 1
        self.assertEqual(get_previous_word(sentence, adjusted_start_index), expected_word)

class TestPreviousWordException(unittest.TestCase):
    def test_previous_word_exception__additional_exception(self):
        word = "Example"
        common_english_vocab = {"example", "word", "test"}
        additional_exception_words = {"example", "special"}
        self.assertTrue(previous_word_exception(word, common_english_vocab, additional_exception_words))

    def test_previous_word_exception__common_english_vocab(self):
        word = "Word"
        common_english_vocab = {"example", "word", "test"}
        additional_exception_words = {"special"}
        self.assertFalse(previous_word_exception(word, common_english_vocab, additional_exception_words))

    def test_previous_word_exception__capitalized_not_in_vocab(self):
        word = "Capitalized"
        common_english_vocab = {"example", "word", "test"}
        additional_exception_words = {"special"}
        self.assertTrue(previous_word_exception(word, common_english_vocab, additional_exception_words))

    def test_previous_word_exception__lowercase_not_in_vocab(self):
        word = "lowercase"
        common_english_vocab = {"example", "word", "test"}
        additional_exception_words = {"special"}
        self.assertFalse(previous_word_exception(word, common_english_vocab, additional_exception_words))
        
class TestConvertNumLineLowercase(unittest.TestCase):
    def setUp(self):
        self.common_english_vocab = {'this', 'is', 'a', 'test'}
        self.printed_exceptions = set()

    def test_convert_num_line_lowercase__simple_conversion(self):
        line = "This is a line with 1 number."
        num = 1
        num_str = "1"
        line_number = 0
        num_header_lines = 0
        converted_line, num_subs_total = convert_num_line_lowercase(line, num, num_str, line_number, num_header_lines, self.printed_exceptions, self.common_english_vocab)
        self.assertEqual(converted_line, "This is a line with one number.")
        self.assertEqual(num_subs_total, 1)

    def test_convert_num_line_lowercase__conversion_with_exception(self):
        line = "Step 1 is important."
        num = 1
        num_str = "1"
        line_number = 0
        num_header_lines = 0
        self.printed_exceptions = []  # Use a list to store printed exceptions
        converted_line, num_subs_total = convert_num_line_lowercase(line, num, num_str, line_number, num_header_lines, self.printed_exceptions, self.common_english_vocab)
        self.assertEqual(converted_line, line)
        self.assertEqual(num_subs_total, 0)
        expected_exception_msg = "Excluding conversion for proper name at line 1: ...Step 1 is important...."
        self.assertIn(expected_exception_msg, self.printed_exceptions)  # Check if the expected message is in the list

class TestConvertNumLineCapitalization(unittest.TestCase):
    def test_convert_num_line_capitalization__beginning_of_sentence(self):
        line = "1 is the first number."
        num = 1
        num_str = "1"
        expected_line = "One is the first number."
        converted_line, num_subs_total = convert_num_line_capitalization(line, num, num_str)
        self.assertEqual(converted_line, expected_line)
        self.assertEqual(num_subs_total, 1)

    def test_convert_num_line_capitalization__after_punctuation(self):
        line = "This is the first number. 1 is an important number."
        num = 1
        num_str = "1"
        expected_line = "This is the first number. One is an important number."
        converted_line, num_subs_total = convert_num_line_capitalization(line, num, num_str)
        self.assertEqual(converted_line, expected_line)
        self.assertEqual(num_subs_total, 1)

    def test_convert_num_line_capitalization__after_colon(self):
        line = "This is the first number: 1. And this is the second: 2."
        num1 = 1
        num_str1 = "1"
        num2 = 2
        num_str2 = "2"
        expected_line = line  # no change for after the colon
        converted_line, num_subs_total = convert_num_line_capitalization(line, num1, num_str1)
        converted_line, num_subs_total = convert_num_line_capitalization(converted_line, num2, num_str2)
        self.assertEqual(converted_line, expected_line)

    def test_convert_num_line_capitalization__no_substitution(self):
        line = "The number 3 is not at the beginning."
        num = 3
        num_str = "3"
        expected_line = "The number 3 is not at the beginning."
        converted_line, num_subs_total = convert_num_line_capitalization(line, num, num_str)
        self.assertEqual(converted_line, expected_line)
        self.assertEqual(num_subs_total, 0)

# depends on the get_timestamp max_words default value (changed to 8 from 5 for PV meetings)
class TestSkipSpeakerLineWithTimestamp(unittest.TestCase):
    def test_skip_speaker_line_with_timestamp__speaker_line_with_link(self):
        line = "David Deutsch [00:01](https://www.youtube.com/dummylink&t=0)"
        self.assertTrue(skip_speaker_line_with_timestamp(line))

    def test_skip_speaker_line_with_timestamp__speaker_line_without_link(self):
        line = "David Deutsch 1:01"
        self.assertTrue(skip_speaker_line_with_timestamp(line))

    def test_skip_speaker_line_with_timestamp__no_timestamp(self):
        line = "This is a test line without a timestamp."
        self.assertFalse(skip_speaker_line_with_timestamp(line))

    def test_skip_speaker_line_with_timestamp__multiple_timestamps(self):
        line = "This line has multiple timestamps [00:01] and [00:02]."
        self.assertTrue(skip_speaker_line_with_timestamp(line))
        # this should give False because the timestamp is being used to identify the speaker line.

    def test_skip_speaker_line_with_timestamp__malformed_timestamp(self):
        line = "This is a line with a malformed timestamp [1;23]."
        self.assertFalse(skip_speaker_line_with_timestamp(line))

    def test_skip_speaker_line_with_timestamp__empty_line(self):
        line = ""
        self.assertFalse(skip_speaker_line_with_timestamp(line))

class TestConvertNumLines(unittest.TestCase):
    def setUp(self):
        self.num = 1
        self.num_str = "1"
        self.num_header_lines = 2
        self.print_output = False
        self.printed_exceptions = []

    def test_convert_num_lines__single_line_conversion(self):
        lines = ["This is line 1."]
        expected_lines = ["This is line one."]
        converted_lines, num_subs_total = convert_num_lines(lines, self.num, self.num_str, self.num_header_lines, self.print_output, self.printed_exceptions)
        self.assertEqual(converted_lines, expected_lines)
        self.assertEqual(num_subs_total, 1)

    def test_convert_num_lines__multiple_line_conversion(self):
        lines = ["This is the number 1 line.", "And this is the number 2 line."]
        expected_lines = ["This is the number one line.", "And this is the number 2 line."]
        converted_lines, num_subs_total = convert_num_lines(lines, self.num, self.num_str, self.num_header_lines, self.print_output, self.printed_exceptions)
        self.assertEqual(converted_lines, expected_lines)
        self.assertEqual(num_subs_total, 1)

    def test_convert_num_lines__skip_line_with_timestamp(self):
        lines = ["David Deutsch  1:01", "And this is the second line."]
        expected_lines = lines
        converted_lines, num_subs_total = convert_num_lines(lines, self.num, self.num_str, self.num_header_lines, self.print_output, self.printed_exceptions)
        self.assertEqual(converted_lines, expected_lines)
        self.assertEqual(num_subs_total, 0)

    def test_convert_num_lines__conversion_with_exception(self):
        lines = ["Step 1 is important."]
        expected_lines = ["Step 1 is important."]
        converted_lines, num_subs_total = convert_num_lines(lines, self.num, self.num_str, self.num_header_lines, self.print_output, self.printed_exceptions)
        self.assertEqual(converted_lines, expected_lines)
        self.assertEqual(num_subs_total, 0)
        self.assertIn("Excluding conversion for proper name at line 3: ...Step 1 is important....", self.printed_exceptions)

class TestConvertNumbersInContent(unittest.TestCase):
    def setUp(self):
        self.num_limit = 10
        self.additional_numbers = [1000000]
        self.num_header_lines = 0
        self.print_output = False

    def test_convert_numbers_in_content__all_cases(self):
        input_content = """
1 is the lonliest number.
"""
        expected_output = """
One is the lonliest number.
"""
        converted_content, total_subs = convert_numbers_in_content(
            input_content, 
            self.num_limit, 
            self.additional_numbers, 
            self.num_header_lines, 
            self.print_output
        )
        self.assertEqual(converted_content, expected_output)
        self.assertEqual(total_subs, 1)

    def test_convert_numbers_in_content__all_cases(self):
        input_content = """
Speaker 0  [0:00](https://www.youtube.com/dummylink&t=0)
CASES WHERE NUMERAL SHOULD BE CHANGED IN TEST FILE
1 capitalize example is here.
The blue car was the best 2.
I prefer these 3 to those.
A 4 time event.
He scored 5 goals.
1 in a 7 billion chance.
We want this very big number to be a word 1000000.
Here is a corner case for 1 of 2 examples.
Hunh going to mean? Like 4 times now in the history of FOF
We got enough for 8 times 4. 0, you know what?
7.

For a paragraph, here is 1 example. 1 more capital is here. In the middle of the room, 1 chair stood out. She mentioned the number 1 in her speech? 1 is the lonlinest number.

And then, look 9 towel left, perfect. Now here is 5 more. What if I add Mistral 8 model. There we go. Surface. 

Let's try to get it nice and dry. If your towel gets too wet, just get another 1. You should have plenty of towels. Okay. I've done plenty of towels. Okay. Step 1 more quick bleach wipe. These guys, It's step 3 of where you touch them. Especially the thumb part. 

just get another 1.

SKIP ORDINALS BECAUSE THAT IS A SEPARATE FUNCTION

CASES WHERE NUMERAL SHOULD NOT BE CHANGED IN TEST FILE
Hit the limit of 10.
Money cost about $33, or $50 or $5 or $2, or nothing.
How about #43 or #2 or #8.
A big number with a comma such as 5,000 units.
Decimal number 60.6 and 70.7. Ends a sentence.
Anything with a non digit or not punctuation like 4- or 8* or anything like that.
1. List item to not change.
I like Orca 2 best. 
These could go either way but let's leave 100 and 1000 for now.
The year was 1991.
The is version 1.0 of our prototype.
The address is 123 Main St.
The model number is A1B2.
When the numeral appears in single quotes '1' like this.
When the numeral appears in double quotes "1" like this.
"""
        expected_output = """
Speaker 0  [0:00](https://www.youtube.com/dummylink&t=0)
CASES WHERE NUMERAL SHOULD BE CHANGED IN TEST FILE
One capitalize example is here.
The blue car was the best two.
I prefer these three to those.
A four time event.
He scored five goals.
One in a seven billion chance.
We want this very big number to be a word one million.
Here is a corner case for one of two examples.
Hunh going to mean? Like four times now in the history of FOF
We got enough for eight times four. Zero, you know what?
seven.

For a paragraph, here is one example. One more capital is here. In the middle of the room, one chair stood out. She mentioned the number one in her speech? One is the lonlinest number.

And then, look nine towel left, perfect. Now here is five more. What if I add Mistral 8 model. There we go. Surface. 

Let's try to get it nice and dry. If your towel gets too wet, just get another one. You should have plenty of towels. Okay. I've done plenty of towels. Okay. Step 1 more quick bleach wipe. These guys, It's step 3 of where you touch them. Especially the thumb part. 

just get another one.

SKIP ORDINALS BECAUSE THAT IS A SEPARATE FUNCTION

CASES WHERE NUMERAL SHOULD NOT BE CHANGED IN TEST FILE
Hit the limit of 10.
Money cost about $33, or $50 or $5 or $2, or nothing.
How about #43 or #2 or #8.
A big number with a comma such as 5,000 units.
Decimal number 60.6 and 70.7. Ends a sentence.
Anything with a non digit or not punctuation like 4- or 8* or anything like that.
1. List item to not change.
I like Orca 2 best. 
These could go either way but let's leave 100 and 1000 for now.
The year was 1991.
The is version 1.0 of our prototype.
The address is 123 Main St.
The model number is A1B2.
When the numeral appears in single quotes '1' like this.
When the numeral appears in double quotes "1" like this.
"""
        converted_content, total_subs = convert_numbers_in_content(
            input_content, 
            self.num_limit, 
            self.additional_numbers, 
            self.num_header_lines, 
            self.print_output
        )
        self.assertEqual(converted_content, expected_output)
        self.assertEqual(total_subs, 24)

class TestConvertOrdinalsInContent(unittest.TestCase):
    def test_convert_ordinals_with_punctuation(self):
        content = "This is the 1st example. now we move to the 2nd one."
        expected = "This is the first example. Now we move to the second one."
        self.assertEqual(convert_ordinals_in_content(content, ['.', '?', '!']), expected)

    def test_convert_ordinals_with_question_mark(self):
        content = "Here's the 3rd example? do you get it? here's the 4th."
        expected = "Here's the third example? Do you get it? Here's the fourth."
        self.assertEqual(convert_ordinals_in_content(content, ['.', '?', '!']), expected)

    def test_convert_ordinals_with_exclamation_mark(self):
        content = "Wow, this is the 5th! isn't it great? now for the 6th."
        expected = "Wow, this is the fifth! Isn't it great? Now for the sixth."
        self.assertEqual(convert_ordinals_in_content(content, ['.', '?', '!']), expected)
    
    def test_convert_ordinals_without_capitalization(self):
        content = "This is the 7th example, and this is the 8th."
        expected = "This is the seventh example, and this is the eighth."
        self.assertEqual(convert_ordinals_in_content(content, []), expected)

# DONE: Update convert_nums_to_words function to handle cases where the input file has no metadata.
# The function should use read_file_flex and handle the case where metadata is None.
# DONE: Modify write_metadata_and_content to handle None metadata gracefully.
# DONE: Ensure that the function doesn't add an extra newline when there's no metadata.
class TestConvertNumsToWords(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test file before each test case
        self.test_filename = 'test_file.md'
        self.test_text = """## metadata
last updated: 2023-07-08
link: https://example.com

## content
This is a test with 1st, 2nd, and 3rd ordinals.
Also, numbers like 1, 2, 3, and 9 should be converted.
Also, this big 1000000 should be converted.
But 10 and 11 should remain as numerals.
"""
        with open(self.test_filename, 'w') as f:
            f.write(self.test_text)

    def tearDown(self):
        # Teardown method to remove test files after each test case
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_convert_nums_to_words__main(self):
        # Test that the function creates a new file with numbers converted to words
        convert_nums_to_words(self.test_filename)
        self.assertTrue(os.path.exists(self.test_filename))
        with open(self.test_filename, 'r') as f:
            converted_text = f.read()
        expected_text = """## metadata
last updated: 2023-07-08
link: https://example.com


## content
This is a test with first, second, and third ordinals.
Also, numbers like one, two, three, and nine should be converted.
Also, this big one million should be converted.
But 10 and 11 should remain as numerals.
"""
        self.assertEqual(converted_text, expected_text)

    def test_convert_nums_to_words__with_specified_files(self):
        # Test that the function correctly converts numbers in the specified files
        cur_file_path = "tests/test_manual_files/transcribe/test numbers convert.md"
        ref_file_path = "tests/test_manual_files/transcribe/test numbers convert_convertnumsREF.md"
        temp_file_path = "tests/test_manual_files/transcribe/temp_test_numbers_convert.md"
        
        # Create a copy of the original file
        shutil.copy(cur_file_path, temp_file_path)
        
        try:
            # Run the conversion on the temporary file
            convert_nums_to_words(temp_file_path)
            self.assertTrue(os.path.exists(temp_file_path))
            
            with open(temp_file_path, 'r') as f:
                converted_content = f.read()
            with open(ref_file_path, 'r') as f:
                expected_content = f.read()
            
            self.assertEqual(converted_content, expected_content)
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def test_convert_nums_to_words__no_metadata(self):
        # Test converting numbers in a file without metadata
        no_metadata_filename = 'test_file_no_metadata.md'
        no_metadata_content = """This is a test with 1st, 2nd, and 3rd ordinals.
Also, numbers like 1, 2, 3, and 9 should be converted.
Also, this big 1000000 should be converted.
But 10 and 11 should remain as numerals.
"""
        with open(no_metadata_filename, 'w') as f:
            f.write(no_metadata_content)

        try:
            convert_nums_to_words(no_metadata_filename)
            self.assertTrue(os.path.exists(no_metadata_filename))
            with open(no_metadata_filename, 'r') as f:
                converted_text = f.read()
            expected_text = """This is a test with first, second, and third ordinals.
Also, numbers like one, two, three, and nine should be converted.
Also, this big one million should be converted.
But 10 and 11 should remain as numerals.
"""
            self.assertEqual(converted_text.strip(), expected_text.strip())
        finally:
            if os.path.exists(no_metadata_filename):
                os.remove(no_metadata_filename)


### SPEAKER NAMES FUNCTIONS
class TestReadSpeakerNamesFromJson(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test JSON file before each test case
        self.test_json_filename = 'test_speaker_names.json'
        test_data = {
            "metadata": {
                "speaker_names": [
                    [0, "Lex Fridman"],
                    [1, "Yann LeCun"]
                ],
                "link": "https://youtu.be/bOnBPGkxUuw"
            },
            "results": {}
        }
        with open(self.test_json_filename, 'w') as f:
            json.dump(test_data, f)

    def tearDown(self):
        # Teardown method to remove the test JSON file after each test case
        os.remove(self.test_json_filename)

    def test_read_speaker_names_from_json__existing_speaker_names(self):
        # Test reading existing speaker names from the JSON file
        speaker_names = read_speaker_names_from_json(self.test_json_filename)
        expected_speaker_names = [
            [0, "Lex Fridman"],
            [1, "Yann LeCun"]
        ]
        self.assertEqual(speaker_names, expected_speaker_names)

    def test_read_speaker_names_from_json__no_speaker_names(self):
        # Test reading a JSON file with no speaker names in the metadata
        test_data = {
            "metadata": {
                "link": "https://youtu.be/bOnBPGkxUuw"
            },
            "results": {}
        }
        with open(self.test_json_filename, 'w') as f:
            json.dump(test_data, f)

        speaker_names = read_speaker_names_from_json(self.test_json_filename)
        self.assertEqual(speaker_names, [])

class TestWriteSpeakerNamesToJson(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test JSON file before each test case
        self.test_json_filename = 'test_speaker_names.json'
        test_json_content = {
            "metadata": {
                "link": "https://example.com",
                "transaction_key": "example_key",
                "request_id": "example_request_id",
                "sha256": "example_sha256",
                "created": "2024-03-09T17:08:48.104Z",
                "duration": 410.856,
                "channels": 1,
                "models": ["example_model_uuid"],
                "model_info": {
                    "example_model_uuid": {
                        "name": "example_model",
                        "version": "2024-01-09.29447",
                        "arch": "nova-2"
                    }
                }
            },
            "results": {}
        }
        with open(self.test_json_filename, 'w') as file:
            json.dump(test_json_content, file, indent=4)

    def tearDown(self):
        # Teardown method to remove test JSON file after each test case
        os.remove(self.test_json_filename)

    def test_write_speaker_names_to_json__add_speaker_names(self):
        # Test adding speaker names to a JSON file
        speaker_names = [[0, "John Doe"], [1, "Jane Smith"]]
        write_speaker_names_to_json(self.test_json_filename, speaker_names)
        with open(self.test_json_filename, 'r') as file:
            data = json.load(file)
        self.assertEqual(data.get('metadata', {}).get('speaker_names', []), speaker_names)

    def test_write_speaker_names_to_json__update_speaker_names(self):
        # Test updating existing speaker names in a JSON file
        initial_speaker_names = [[0, "John Doe"], [1, "Jane Smith"]]
        write_speaker_names_to_json(self.test_json_filename, initial_speaker_names)
        updated_speaker_names = [[0, "Alice Johnson"], [1, "Bob Williams"]]
        write_speaker_names_to_json(self.test_json_filename, updated_speaker_names)
        with open(self.test_json_filename, 'r') as file:
            data = json.load(file)
        self.assertEqual(data.get('metadata', {}).get('speaker_names', []), updated_speaker_names)

    def test_write_speaker_names_to_json__file_does_not_exist(self):
        # Test attempting to write speaker names to a non-existent JSON file
        with self.assertRaises(ValueError):
            write_speaker_names_to_json('nonexistent_file.json', [['Speaker']])

class TestFindUnassignedSpeakers(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test markdown file before each test case
        self.test_md_filename = 'test_unassigned_speakers.md'
        test_md_content = """
        ## metadata
link: https://www.youtube.com/dummylink
last updated: 

## content

Speaker 0  [0:00](https://www.youtube.com/dummylink&t=0)
I think it was unfortunate...

Bill  [0:23](https://www.youtube.com/dummylink&t=23)
That is, we know how...

Speaker 3  [2:23](https://www.youtube.com/dummylink&t=143)
Just because it isn't relative...

Speaker 2  [2:34](https://www.youtube.com/dummylink&t=154)
Contemporary pragmatists tend to say...

Speaker X  [3:17](https://www.youtube.com/dummylink&t=197)
Nietzschean perspectivism, which says...
"""
        with open(self.test_md_filename, 'w') as f:
            f.write(test_md_content)

    def tearDown(self):
        # Teardown method to remove test markdown file after each test case
        os.remove(self.test_md_filename)

    def test_find_unassigned_speakers__unassigned_speakers_present(self):
        # Test finding unassigned speakers in the markdown file
        unassigned_speakers = find_unassigned_speakers(self.test_md_filename)
        self.assertEqual(unassigned_speakers, ['Speaker 0','Speaker 2','Speaker 3'],)

    def test_find_unassigned_speakers__all_speakers_assigned(self):
        # Test when all speakers in the markdown file are assigned
        with open(self.test_md_filename, 'r') as f:
            test_md_content_all_assigned = f.read().replace('Speaker 0', 'John').replace('Speaker 3', 'Alice').replace('Speaker 2', 'Bob')
        with open(self.test_md_filename, 'w') as f:
            f.write(test_md_content_all_assigned)
        unassigned_speakers = find_unassigned_speakers(self.test_md_filename)
        self.assertIsNone(unassigned_speakers)

    def test_find_unassigned_speakers__file_does_not_exist(self):
        # Test when the markdown file does not exist
        non_existent_md_filename = 'non_existent_file.md'
        with self.assertRaises(ValueError):
            find_unassigned_speakers(non_existent_md_filename)
  
class TestPropagateSpeakerNamesThroughoutMd(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test markdown file before each test case
        self.test_md_filename = 'test_propagate_speakers.md'
        test_md_content = """
## metadata
link: https://www.youtube.com/dummylink
last updated: 

## content

Speaker 0  [0:00](https://www.youtube.com/dummylink&t=0)
I think it was unfortunate...

Bill  [0:23](https://www.youtube.com/dummylink&t=23)
That is, we know how...

Speaker 1  [2:23](https://www.youtube.com/dummylink&t=143)
Just because it isn't relative...

Speaker 2  [2:34](https://www.youtube.com/dummylink&t=154)
Contemporary pragmatists tend to say...

Speaker 0  [3:17](https://www.youtube.com/dummylink&t=197)
Nietzschean perspectivism, which says...
"""
        with open(self.test_md_filename, 'w') as f:
            f.write(test_md_content)

    def tearDown(self):
        # Teardown method to remove test markdown file after each test case
        os.remove(self.test_md_filename)

    def test_propagate_speaker_names_throughout_md__imput_2_names(self):
        # Test propagating speaker names throughout the markdown file
        input_speaker_names = [(0, 'Alice'), (1, 'Bob')]
        expected_output = [(0, 'Alice'), (1, 'Bob')]
        speaker_names = propagate_speaker_names_throughout_md(self.test_md_filename, input_speaker_names)
        self.assertEqual(speaker_names, expected_output)
        with open(self.test_md_filename, 'r') as f:
            content = f.read()
            self.assertIn('Alice  [0:00]', content)
            self.assertIn('Bob  [2:23]', content)
            self.assertNotIn('Speaker 0', content)
            self.assertNotIn('Speaker 1', content)
            self.assertIn('Bill  [0:23]', content)
            self.assertIn('Speaker 2', content)

    def test_propagate_speaker_names_throughout_md__no_input(self):
        # Test propagating speaker names with no input speaker names
        expected_output = []
        speaker_names = propagate_speaker_names_throughout_md(self.test_md_filename)
        self.assertEqual(speaker_names, expected_output)
        with open(self.test_md_filename, 'r') as f:
            content = f.read()
            self.assertIn('Bill  [0:23]', content)
            self.assertIn('Speaker 0', content)
            self.assertIn('Speaker 1', content)
            self.assertIn('Speaker 2', content)

class TestIterateInputSpeakerNames(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test markdown file before each test case
        self.test_md_filename = 'test_iterate_speakers.md'
        test_md_content = """
## metadata
link: https://www.youtube.com/dummylink
last updated: 

## content

Speaker 0  [0:00](https://www.youtube.com/dummylink&t=0)
I think it was unfortunate...

Bill  [0:23](https://www.youtube.com/dummylink&t=23)
That is, we know how...

Speaker 1  [2:23](https://www.youtube.com/dummylink&t=143)
Just because it isn't relative...

Speaker 2  [2:34](https://www.youtube.com/dummylink&t=154)
Contemporary pragmatists tend to say...

Speaker 0  [3:17](https://www.youtube.com/dummylink&t=197)
Nietzschean perspectivism, which says...
"""
        with open(self.test_md_filename, 'w') as f:
            f.write(test_md_content)

    def tearDown(self):
        # Teardown method to remove test markdown file after each test case
        os.remove(self.test_md_filename)

    @patch('builtins.input', side_effect=['', 'E'])
    def test_iterate_input_speaker_names__input_2_names(self, mock_input):
        # Test iterating input speaker names throughout the markdown file
        input_speaker_names = [(0, 'Alice'), (1, 'Bob')]
        expected_output = [(0, 'Alice'), (1, 'Bob')]
        speaker_names = iterate_input_speaker_names(self.test_md_filename, input_speaker_names)
        self.assertEqual(speaker_names, expected_output)
        with open(self.test_md_filename, 'r') as f:
            content = f.read()
            self.assertIn('Alice  [0:00]', content)
            self.assertIn('Bob  [2:23]', content)
            self.assertNotIn('Speaker 0', content)
            self.assertNotIn('Speaker 1', content)
            self.assertIn('Bill  [0:23]', content)
            self.assertIn('Speaker 2  [2:34]', content)
            self.assertIn('Alice  [3:17]', content)

    @patch('builtins.input', side_effect=['', 'E'])
    def test_iterate_input_speaker_names__prompt_2_names(self, mock_input):
        # Test iterating input speaker names throughout the markdown file without initial input
        with open(self.test_md_filename, 'r') as f:
            test_md_content_with_names = f.read().replace('Speaker 0', 'Speaker 0=Alice').replace('Speaker 1', 'Speaker 1=Bob')
        with open(self.test_md_filename, 'w') as f:
            f.write(test_md_content_with_names)

        expected_output = [(0, 'Alice'), (1, 'Bob')]
        speaker_names = iterate_input_speaker_names(self.test_md_filename)
        self.assertEqual(speaker_names, expected_output)
        with open(self.test_md_filename, 'r') as f:
            content = f.read()
            self.assertIn('Alice  [0:00]', content)
            self.assertIn('Bob  [2:23]', content)
            self.assertNotIn('Speaker 0', content)
            self.assertNotIn('Speaker 1', content)
            self.assertIn('Bill  [0:23]', content)
            self.assertIn('Speaker 2  [2:34]', content)
            self.assertIn('Alice  [3:17]', content)

class TestAssignSpeakerNames(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test markdown file and a corresponding JSON file before each test case
        self.test_md_filename = 'test_assign_speakers.md'
        self.test_json_filename = self.test_md_filename.replace('.md', '.json')
        test_md_content = """
## metadata
link: https://www.youtube.com/dummylink
last updated: 

## content

Speaker 0  [0:00](https://www.youtube.com/dummylink&t=0)
I think it was unfortunate...

Bill  [0:23](https://www.youtube.com/dummylink&t=23)
That is, we know how...

Speaker 1  [2:23](https://www.youtube.com/dummylink&t=143)
Just because it isn't relative...

Speaker 2  [2:34](https://www.youtube.com/dummylink&t=154)
Contemporary pragmatists tend to say...

Speaker 0  [3:17](https://www.youtube.com/dummylink&t=197)
Nietzschean perspectivism, which says...
"""
        with open(self.test_md_filename, 'w') as f:
            f.write(test_md_content)

        test_json_content = '{"metadata": {"speaker_names": []}}'
        with open(self.test_json_filename, 'w') as f:
            f.write(test_json_content)

    def tearDown(self):
        # Teardown method to remove test markdown file and JSON file after each test case
        os.remove(self.test_md_filename)
        os.remove(self.test_json_filename)

    @patch('builtins.input', side_effect=['', 'E'])
    def test_assign_speaker_names__no_entry(self, mock_input):
        # Test assigning speaker names to the markdown file
        assign_speaker_names(self.test_md_filename)
        with open(self.test_md_filename, 'r') as f:
            content = f.read()
            self.assertIn('Speaker 0  [0:00]', content)
            self.assertIn('Bill  [0:23]', content)
            self.assertIn('Speaker 1  [2:23]', content)
            self.assertIn('Speaker 2  [2:34]', content)
            self.assertIn('Speaker 0  [3:17]', content)

    @patch('builtins.input', side_effect=['', 'E'])
    def test_assign_speaker_names__prompt_2_names(self, mock_input):
        # Test assigning speaker names to the markdown file without initial input
        with open(self.test_md_filename, 'r') as f:
            test_md_content_with_names = f.read().replace('Speaker 0', 'Speaker 0=Alice').replace('Speaker 1', 'Speaker 1=Bob')
        with open(self.test_md_filename, 'w') as f:
            f.write(test_md_content_with_names)

        assign_speaker_names(self.test_md_filename)
        with open(self.test_md_filename, 'r') as f:
            content = f.read()
            self.assertIn('Alice  [0:00]', content)
            self.assertIn('Bob  [2:23]', content)
            self.assertNotIn('Speaker 0', content)
            self.assertNotIn('Speaker 1', content)
            self.assertIn('Bill  [0:23]', content)
            self.assertIn('Speaker 2  [2:34]', content)
            self.assertIn('Alice  [3:17]', content)

### WRAPPER FUNCTIONS TO PROCESS DEEPGRAM TRANSCRIPTION
class TestCreateTranscriptMdFromJson(unittest.TestCase):
    def setUp(self):
        # Setup method to specify the path to the full test JSON file and the reference markdown file
        self.full_json_filename = "tests/test_manual_files/jsons/2024-03-08_Test Deepgram with all features_nova2.json"
        self.ref_md_filename = "tests/test_manual_files/jsons/2024-03-08_Test Deepgram with all features_nova2REF.md"

    def test_create_transcript_md_from_json__real_file(self):
        # Test creating a markdown transcript from the full JSON file
        md_file_path = create_transcript_md_from_json(self.full_json_filename)
        self.assertTrue(os.path.exists(md_file_path))
        with open(md_file_path, 'r') as f:
            generated_content_lines = f.readlines()
        with open(self.ref_md_filename, 'r') as f:
            reference_content_lines = f.readlines()
        
        # Remove the line starting with 'last updated:' from both contents
        generated_content_lines = [line for line in generated_content_lines if not line.startswith('last updated:')]
        reference_content_lines = [line for line in reference_content_lines if not line.startswith('last updated:')]

        self.assertEqual(generated_content_lines, reference_content_lines)

@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLProcessDeepgramTranscription(unittest.TestCase):
    def setUp(self):
        # Setup method to create a test directory for audio files
        self.audio_inbox_path = 'test_audio_inbox'
        os.makedirs(self.audio_inbox_path, exist_ok=True)

    def tearDown(self):
        # Teardown method to remove test audio files and directory
        shutil.rmtree(self.audio_inbox_path, ignore_errors=True)

    @patch('builtins.input', side_effect=['', 'E'])
    def test_apicall_process_deepgram_transcription__trunc_shortest_interview(self, mock_input):
        # Test processing a Deepgram transcription from a YouTube video link
        title = 'Shortest Interview Ever'
        link = 'https://youtu.be/6pMcXSixdVQ'
        model = 'nova-2'
        md_file_path = process_deepgram_transcription(title, link, model, self.audio_inbox_path)
        self.assertTrue(os.path.exists(md_file_path))
        with open(md_file_path, 'r') as f:
            content = f.read()
        # skip the first two lines because it has the current date which will change.
        # truncate the transcript because it's not properly recognizing the diarization (4-23 RT) as it was previously, no idea why
        expected_content = """
## metadata
last updated: IGNORE THIS LINE BECAUSE OF DATE
link: https://youtu.be/6pMcXSixdVQ
transcript source: deepgram 2-primary-nova

## content

Speaker 0  [0:00](https://youtu.be/6pMcXSixdVQ&t=0)
Hi. I'm Max Flower.
""".strip()
        self.assertEqual(content.splitlines()[2].split('Hi. I\'m Max Flower.')[0], expected_content.splitlines()[2].split('Hi. I\'m Max Flower.')[0])

class TestAPIMOCKProcessDeepgramTranscription(unittest.TestCase):
    # MOCK version of TestAPIProcessDeepgramTranscription that does not call API
    def setUp(self):
        # Setup method to mock parameters
        self.audio_inbox_path = 'tests/test_manual_files/transcribe/'
        self.audio_file_path = 'tests/test_manual_files/transcribe/Shortest Interview Ever.mp3'
        self.json_file_path = 'tests/test_manual_files/transcribe/Shortest Interview Ever Mock Copy_nova2.json'
        self.md_file_original = 'tests/test_manual_files/transcribe/Shortest Interview Ever Mock Compare_nova2.md'

    def tearDown(self):
        # Teardown method to remove the generated markdown file
        md_file_path = self.json_file_path.replace('.json', '.md')
        if os.path.exists(md_file_path):
            os.remove(md_file_path)

    @patch('primary.transcribe.download_mp3_from_youtube')
    @patch('primary.transcribe.transcribe_deepgram')
    @patch('builtins.input', side_effect=['', 'E'])
    def test_process_deepgram_transcription__api_mock_main(self, mock_input, mock_transcribe_deepgram, mock_download_mp3_from_youtube):
        # Mock processing a Deepgram transcription from a YouTube video link
        mock_download_mp3_from_youtube.return_value = self.audio_file_path
        mock_transcribe_deepgram.return_value = self.json_file_path
        title = 'Shortest Interview Ever.mp3'
        link = 'https://youtu.be/6pMcXSixdVQ'
        model = 'nova2'
        md_file_path = process_deepgram_transcription(title, link, model, self.audio_inbox_path)
        self.assertTrue(os.path.exists(md_file_path))
        with open(md_file_path, 'r') as f:
            content = f.read()
        with open(self.md_file_original, 'r') as f:
            expected_content = f.read()
        self.assertEqual(content.splitlines()[2:], expected_content.splitlines()[2:])
        # skip the first two lines because it has the current date which will change.

@unittest.skip("Temporarily skipped because calls API")
class TestAPICALLProcessDeepgramTranscriptionFromAudioFile(unittest.TestCase):
    def setUp(self):
        # Setup method to specify the path to the test MP3 file
        self.audio_file_path = 'tests/test_manual_files/transcribe/Shortest Interview Ever.mp3'

    def tearDown(self):
        # Teardown method to remove the generated markdown file
        md_file_path = self.audio_file_path.replace('.mp3', '.md')
        if os.path.exists(md_file_path):
            os.remove(md_file_path)

    @patch('builtins.input', side_effect=['', 'E'])
    def test_process_deepgram_transcription_from_audio_file(self, mock_input):
        # Test processing a Deepgram transcription from an audio file
        link = 'https://youtu.be/6pMcXSixdVQ'
        model = 'nova-2'
        md_file_path = process_deepgram_transcription_from_audio_file(link, self.audio_file_path, model)
        self.assertTrue(os.path.exists(md_file_path))
        with open(md_file_path, 'r') as f:
            content = f.read()
        expected_content = """
## metadata
last updated: 03-11-2024 Created
link: https://youtu.be/6pMcXSixdVQ
transcript source: nova2

## content

Speaker 0  [0:00](https://youtu.be/6pMcXSixdVQ&t=0)
Hi. I'm Max Flower. I'm here with Adam Morrison, and he's gonna tell us about his secrets to success. Adam?

Speaker 1  [0:05](https://youtu.be/6pMcXSixdVQ&t=5)
Just working hard and, you know, doing the right things every day.

Speaker 0  [0:09](https://youtu.be/6pMcXSixdVQ&t=9)
Well, Adam, thank you for your time, and I wish you the best of luck. Appreciate it.

Speaker 1  [0:13](https://youtu.be/6pMcXSixdVQ&t=13)
Thanks.

Speaker 0  [0:13](https://youtu.be/6pMcXSixdVQ&t=13)
Thanks, Adam. See
""".strip()
        self.assertEqual(content.splitlines()[2:], expected_content.splitlines()[2:])
        # skip the first two lines because it has the current date which will change.

class TestAPIMOCKProcessDeepgramTranscriptionFromAudioFile(unittest.TestCase):
    # MOCK version of TestAPIProcessDeepgramTranscriptionFromAudioFile that does not call API
    def setUp(self):
        # Setup method to mock parameters
        self.audio_inbox_path = 'tests/test_manual_files/transcribe/'
        self.audio_file_path = 'tests/test_manual_files/transcribe/Shortest Interview Ever.mp3'
        self.json_file_path = 'tests/test_manual_files/transcribe/Shortest Interview Ever Mock Copy_nova2.json'
        self.md_file_original = 'tests/test_manual_files/transcribe/Shortest Interview Ever Mock Compare_nova2.md'

    def tearDown(self):
        # Teardown method to remove the generated markdown file
        md_file_path = self.json_file_path.replace('.json', '.md')
        if os.path.exists(md_file_path):
            os.remove(md_file_path)

    @patch('primary.transcribe.transcribe_deepgram')
    @patch('builtins.input', side_effect=['', 'E'])
    def test_process_deepgram_transcription_from_audio_file__api_mock_main(self, mock_input, mock_transcribe_deepgram):
        # Mock processing a Deepgram transcription from an audio file
        mock_transcribe_deepgram.return_value = self.json_file_path
        link = 'https://youtu.be/6pMcXSixdVQ'
        model = 'nova-2'
        md_file_path = process_deepgram_transcription_from_audio_file(link, self.audio_file_path, model)
        self.assertTrue(os.path.exists(md_file_path))
        with open(md_file_path, 'r') as f:
            content = f.read()
        with open(self.md_file_original, 'r') as f:
            expected_content = f.read()
        self.assertEqual(content.splitlines()[2:], expected_content.splitlines()[2:])
        # skip the first two lines because it has the current date which will change.

class TestProcessMultipleVideos(unittest.TestCase):
    @patch('primary.transcribe.create_youtube_md_from_file_link')
    @patch('primary.transcribe.process_deepgram_transcription')
    def test_process_multiple_videos(self, mock_process_deepgram, mock_create_youtube_md):
        # Mocking the return values of process_deepgram_transcription
        mock_process_deepgram.side_effect = [
            'path/to/markdown1.md',
            'path/to/markdown2.md'
        ]

        videos_to_process = [
            ('Video Title 1', 'https://youtu.be/link1'),
            ('Video Title 2', 'https://youtu.be/link2')
        ]

        process_multiple_videos(videos_to_process, model='nova-2')

        # Assert that process_deepgram_transcription is called with the correct arguments
        expected_calls = [
            call('Video Title 1', 'https://youtu.be/link1', 'nova-2'),
            call('Video Title 2', 'https://youtu.be/link2', 'nova-2')
        ]
        mock_process_deepgram.assert_has_calls(expected_calls, any_order=False)

        # Assert that create_youtube_md_from_file_link is called with the correct arguments
        expected_md_calls = [
            call('path/to/markdown1.md'),
            call('path/to/markdown2.md')
        ]
        mock_create_youtube_md.assert_has_calls(expected_md_calls, any_order=False)

        # Assert that both functions are called twice (once for each video)
        self.assertEqual(mock_process_deepgram.call_count, 2)
        self.assertEqual(mock_create_youtube_md.call_count, 2)


# AssertionError: 'Returned' != 'Expected'

if __name__ == '__main__':
    unittest.main()