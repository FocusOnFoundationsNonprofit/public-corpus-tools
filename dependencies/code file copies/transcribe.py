# Library of functions and execution code to transcribe audio files
import os
import sys
import re
import threading
import time
from datetime import datetime, timedelta
import requests
import yt_dlp as youtube_dl
from num2words import num2words
import json
import math
import mutagen  # Import mutagen to handle audio metadata
from wordfreq import top_n_list
# Get the top 3000 English words
common_english_vocab = set(top_n_list('en', 3000))

from config import DEEPGRAM_API_KEY

import warnings  # Set the warnings to use a custom format
from primary.fileops import custom_formatwarning
warnings.formatwarning = custom_formatwarning
# USAGE: warnings.warn(f"Insert warning message here")

# Get the directory name of the current file (transcribe.py) and the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir) # Add the parent directory to sys.path

### YOUTUBE
def download_mp3_from_youtube(url, output_title='downloaded_audio'):
    """ 
    Downloads an audio file from a YouTube URL and saves it as an mp3 file. Uses yt_dlp package.

    :param url: string of the YouTube URL from which to download the audio.
    :param output_title: string of the title to save the downloaded mp3 file as. defaults to 'downloaded_audio'.
    :return: string of the path to the saved mp3 file.
    """
    output_file_path = output_title + '.mp3'
    if os.path.exists(output_file_path):
        user_input = input("Audio file already exists. Enter 'y' or 'yes' to download again and overwrite, or any other key to skip: ").lower()
        if user_input not in ['y', 'yes']:
            print("Skipping download.")
            return output_file_path

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_title,  # note it's not output_path, by default save file as "downloaded_audio.mp3"
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_file_path
def get_youtube_title_length(url):
    """ 
    Retrieves the title and duration of a youtube video in a formatted timestamp. Uses yt_dlp package.

    :param url: string of the youtube url to retrieve information from.
    :return: tuple containing the video title and its duration as a string in a formatted timestamp.
    """
    from primary.fileops import tune_timestamp
    ydl_opts = {
        'quiet': True,
        'skip_download': True,  # We just want the info
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', 'Unknown Title')
        video_duration = info_dict.get('duration', 0)
        # Convert duration from seconds to a time format (H:MM:SS)
        video_length = tune_timestamp(str(timedelta(seconds=video_duration)))
        return video_title, video_length
def download_link_list_to_mp3s(links, audio_inbox_path="data/audio_inbox"):  # NO CALLERS (3-3 RT)
    """
    Downloads a list of youtube links as mp3 files to a specified directory and stores the link-title pairs. Uses yt_dlp package.
    Calls download_mp3_from_youtube

    :param links: list of youtube links to be downloaded.
    :param audio_inbox_path: string of the directory path where the audio files will be saved.
    :return: dictionary mapping each youtube link to its corresponding title.
    """
    link_title_pairs = {}
    for link in links:
        title, length = get_youtube_title_length(link)  # Get title and length
        title = title.rsplit('.', 1)[0]  # Remove file extension from title
        link_title_pairs[link] = title  # Store link-title pair
        download_mp3_from_youtube(link, os.path.join(audio_inbox_path, title))  # Download as MP3
    return link_title_pairs
def download_youtube_subtitles_url(subtitle_url): # DS, cat 1, omit unittests since called by next function
    """
    Downloads and extracts subtitle text from a given YouTube subtitle URL.
    Helper function to that is called from get_youtube_subtitles
    
    :param subtitle_url: string of the url from which subtitles are to be downloaded.
    :return: string of the extracted subtitle text, spaces between segments and stripped of new lines.
    """
    response = requests.get(subtitle_url)
    response.raise_for_status()  # This will raise an exception for HTTP errors
    subtitle_data = response.json()  # Parse JSON data

    # Extract transcript text from the subtitle data
    subtitle_text = ""
    for event in subtitle_data['events']:
        if 'segs' in event:
            for seg in event['segs']:
                if 'utf8' in seg:
                    subtitle_text += seg['utf8'] + " "

    return subtitle_text.replace('\n', ' ').strip()
def get_youtube_subtitles(url):
    """
    Retrieves English subtitles for a given YouTube video URL if available. Uses yt_dlp package.
    
    :param url: string of the youtube video url.
    :return: subtitles as a string if found, otherwise None.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en']  # Specify the language of subtitles you want to download
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        
        # Attempt to get the transcript (subtitles)
        subtitles = info_dict.get('subtitles', {})
        auto_captions = info_dict.get('automatic_captions', {})
        
        # Choose subtitles or automatic captions to return
        transcript_info = subtitles if subtitles else auto_captions
        
        # If there are subtitles or auto captions, download them
        if transcript_info.get('en'):
            subtitles_url = transcript_info['en'][0]['url']  # Get the URL for the first English subtitle track
            return download_youtube_subtitles_url(subtitles_url)
        else:
            print("No English subtitles found.")
            return None
def get_youtube_all(url):
    """
    Retrieves all available information from a YouTube video URL, including title, length, chapters, description, and transcript. Uses yt_dlp package.
    
    :param url: string of the youtube video url.
    :return: dictionary with video details or None if the URL is invalid.
    """
    if not is_valid_youtube_url(url):
        print(f"Invalid YouTube URL: {url}")
        return None
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en']
    }
    
    transcript_text = None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        
        # Extract title, channel, date, and length
        video_title = info_dict.get('title', 'Unknown Title')
        video_channel = info_dict.get('uploader', 'Unknown Channel')
        video_date = info_dict.get('upload_date', 'Unknown Date')
        video_duration = info_dict.get('duration', 0)
        video_length = str(timedelta(seconds=video_duration))
        
        # Extract chapters
        chapters = info_dict.get('chapters', [])
        #print("DEBUG - Chapters:", chapters if chapters else "Chapters is None")
        if chapters:
            formatted_chapters = [{'start_time': str(timedelta(seconds=chap['start_time'])),
                                   'title': chap['title']} for chap in chapters]
        else:
            formatted_chapters = ''
        
        # Extract description
        description = info_dict.get('description', '')
        
        # Extract subtitles
        subtitles = info_dict.get('subtitles', {})
        auto_captions = info_dict.get('automatic_captions', {})
        
        # Choose subtitles or automatic captions to return and assign the source
        if subtitles:
            transcript_info = subtitles
            transcript_source = 'subtitles'
        else:
            transcript_info = auto_captions
            transcript_source = 'auto-captions'
        
        # If there are subtitles or auto captions, download them
        if transcript_info.get('en'):
            subtitles_url = transcript_info['en'][0]['url']  # Get the URL for the first English subtitle track
            transcript_text = download_youtube_subtitles_url(subtitles_url)
            transcript_text = ' '.join(transcript_text.split())  # compress multiple spaces into one
        else:
            print("No English subtitles found.")
        
        print(f"For YouTube video title: {video_title}")
        extracted_features = []
        if formatted_chapters:
            extracted_features.append('chapters')
        if description:
            extracted_features.append('description')
        if transcript_source:
            extracted_features.append(f'transcript from {transcript_source}')
        
        print(f"  extracted the following features: {', '.join(extracted_features)}")
        return {
            'title': video_title,
            'channel': video_channel,
            'date': video_date,
            'length': video_length,
            'chapters': formatted_chapters,
            'description': description,
            'transcript': transcript_text or "No transcript found",
            'transcript source': transcript_source
        }
def is_valid_youtube_url(url):
    """ 
    Determine if a string of url is a valid YouTube URL by attempting to fetch video info using the yt_dlp package.

    :param url: string of url to be validated.
    :return: boolean where true if the url is valid, false otherwise.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            # Try to fetch the video info. If this succeeds, the URL is valid.
            ydl.extract_info(url, download=False)
            return True
        except youtube_dl.utils.DownloadError:
            # If youtube_dl raises a DownloadError, the URL is not valid.
            return False
        except youtube_dl.utils.ExtractorError:
            # If youtube_dl raises an ExtractorError, the URL is not valid.
            return False
        except Exception as e:
            # If any other exception occurs, print the exception and assume the URL is not valid.
            print(f"ERROR in is_valid_youtube_url occurred: {e}")
            return False
def create_youtube_md(url, title_or_path=None):  # unittests 3 APICALL + 1 APIMOCK
    """
    Generates a markdown file containing metadata, chapters, description, and transcript from a YouTube video.

    :param url: string of the url to be processed.
    :param title_or_path: string of the title or path for the markdown file, defaults to None.
    :return: string of the path to the created markdown file.
    """
    from primary.fileops import create_full_path, set_metadata_field
    from primary.fileops import write_metadata_and_content, add_timestamp_links
    
    if not is_valid_youtube_url(url):
        raise ValueError(f"VALUE ERROR - invalid YouTube URL: {url}")

    if title_or_path is None:
        title_or_path, _ = get_youtube_title_length(url)
    
    default_folder = "data/audio_inbox"
    suffix_ext = "_yt.md"
    yt_md_file_path = create_full_path(title_or_path, suffix_ext, default_folder)

    yt_info_dict = get_youtube_all(url)
    yt_content = "## content\n\n"
    if yt_info_dict['chapters']:
        yt_content += "### chapters (youtube)\n\n" + '\n'.join([f"{chap['start_time']} - {chap['title']}" for chap in yt_info_dict['chapters']])
        yt_content += "\n\n"
    yt_content += "### description (youtube)\n\n" + yt_info_dict['description'] + "\n\n"
    yt_content += "### transcript (youtube)\n\n" + yt_info_dict['transcript']

    yt_metadata = "## metadata\n"  # below fields are inserted above
    date_today = datetime.now().strftime("%m-%d-%Y")  # Assign today's date in format MM-DD-YYYY
    yt_metadata = set_metadata_field(yt_metadata, 'last updated', date_today + ' Created')  # Updates last updated
    yt_metadata = set_metadata_field(yt_metadata, 'link', url)
    yt_metadata = set_metadata_field(yt_metadata, 'youtube title', yt_info_dict['title'])
    yt_metadata = set_metadata_field(yt_metadata, 'youtube transcript source', yt_info_dict['transcript source'])
    yt_metadata = set_metadata_field(yt_metadata, 'length', yt_info_dict['length'])
    
    write_metadata_and_content(yt_md_file_path, yt_metadata, yt_content, overwrite='yes')
    add_timestamp_links(yt_md_file_path)
    return yt_md_file_path
def create_youtube_md_from_file_link(md_file_path):
    """
    Creates a YouTube markdown file from a given file path by extracting the YouTube link from the file's metadata.
    
    :param md_file_path: string of the path to the markdown file containing the YouTube link in its metadata.
    :return: string of the path to the created YouTube markdown file.
    """
    from primary.fileops import sub_suffix_in_str, read_metadata_and_content, read_metadata_field_from_file
    suffix_new = '_yt'

    metadata, _ = read_metadata_and_content(md_file_path)
    if metadata is None:
        raise ValueError("VALUE ERROR - metadata is None")

    metadata_result = read_metadata_field_from_file(md_file_path, "link")  # returns a tuple (line num, field val)
    if metadata_result is None or metadata_result[1] is None:
        raise ValueError(f"VALUE ERROR - 'link' metadata field is missing or None in the file: {md_file_path}")
    _, link = metadata_result
    yt_file_path = sub_suffix_in_str(md_file_path, suffix_sub=suffix_new)
    #print(f"DEBUG: before create call {yt_file_path}")
    yt_file_path = create_youtube_md(link, yt_file_path)  # creates and returns the same file_path so the assignment is not needed but do it in case there is a bug and a different file_path is returned
    #print(f"DEBUG: after create call {yt_file_path}")
    return yt_file_path
def extract_feature_from_youtube_md(yt_md_file_path, feature):
    """
    Extracts a specified feature from a YouTube markdown file and returns it as a string.

    :param yt_md_file_path: string of the path to the markdown file from which the feature is to be extracted.
    :param feature: string of the feature to be extracted (e.g., 'chapters', 'description', 'transcript').
    :return: string of the extracted text under the specified feature
    """
    try:
        with open(yt_md_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        feature_section_found = False
        extracted_feature = ""
        feature_heading_pattern = re.compile(r'^#+\s*' + re.escape(feature), re.IGNORECASE)  # Pattern to match any level of markdown heading for the feature

        for line in lines:
            if feature_heading_pattern.match(line) or feature_section_found:
                if line.strip().startswith('#') and feature_section_found:
                    break
                feature_section_found = True
                if not feature_heading_pattern.match(line):  # Do not include the heading line in the extracted feature
                    extracted_feature += line
        if not feature_section_found or extracted_feature == "":
            warnings.warn(f"Feature '{feature}' not found in YouTube markdown file.")
            return None
        else:
            return extracted_feature.strip() + '\n\n'
    except Exception as e:
        raise ValueError(f"Error extracting {feature} from {yt_md_file_path}: {e}")
    
### DEEPGRAM AND JSON
from deepgram import DeepgramClient, PrerecordedOptions

def test_deepgram_client():  # omit unittests
    """
    Tests the Deepgram client initialization with the provided API key and prints a success or failure message.
    Raises ValueError if test fails.
    """
    try:
        test_deepgram_client = DeepgramClient(DEEPGRAM_API_KEY)
        if test_deepgram_client:
            print("Successfully created Deepgram Client and accessed the DeepGram API key.")
        else:
            print("Failed to create the Deepgram Client and/or access the DeepGram API key.")
    except Exception as e:
        raise ValueError(f"VALUE ERROR in test of Deepgram client: {e}")
def get_media_length(file_path_or_url):
    """
    Retrieves the length (duration) of a media file or a YouTube video.
    For a local file, it returns the duration in seconds.
    For a YouTube video, it returns the duration in our tuned timestamp format.

    :param file_path_or_url: Path to a local media file or a URL to a YouTube video.
    :return: length (duration) of the media in seconds (for local files) or in our tuned timestamp format (for YouTube videos).
    """
    from primary.fileops import tune_timestamp

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with open(os.devnull, 'w') as fnull:
            sys.stderr = fnull
            try:
                if is_valid_youtube_url(file_path_or_url):
                    _, video_length = get_youtube_title_length(file_path_or_url)
                    return tune_timestamp(video_length)
                elif os.path.isfile(file_path_or_url):
                    # Use mutagen to get the length of the audio file
                    audio = mutagen.File(file_path_or_url)
                    if audio is not None and hasattr(audio.info, 'length'):
                        return tune_timestamp(str(timedelta(seconds=int(audio.info.length))))
                    else:
                        raise ValueError("Could not determine the length of the audio file.")
                else:
                    raise ValueError("Invalid YouTube URL or file path.")
            except Exception as e:
                raise ValueError(f"An error occurred while retrieving media length: {e}")
            finally:
                sys.stderr = sys.__stderr__
def add_link_to_json(json_file_path, link):
    """ 
    Add a hyperlink to the JSON file under the 'metadata' section.

    :param json_file_path: string, the path to the JSON file to be modified.
    :param link: string, the hyperlink to be added to the JSON file.
    :return: tuple, the path to the modified JSON file and None if successful, or None and an exception if an error occurs.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Check if 'metadata' exists in the JSON
        if 'metadata' in data:
            # Add the 'link' field at the top of the 'metadata'
            data['metadata'] = {'link': link, **data['metadata']}
        else:
            # If 'metadata' does not exist, create it
            data['metadata'] = {'link': link}

        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return json_file_path, None
    except Exception as e:
        print(f"Error processing file {json_file_path}: {e}")
        return None, e
def get_link_from_json(json_file_path):
    """ 
    Retrieve the hyperlink from the 'metadata' section of a JSON file.

    :param json_file_path: string, the path to the JSON file from which the hyperlink is to be retrieved.
    :return: string or None, the hyperlink if found in the JSON file's 'metadata' section, otherwise None.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        link = data.get('metadata', {}).get('link', None)
    except Exception as e:
        print(f"Error extracting link from {json_file_path}: {e}")
        link = None
    return link

# TODO rename to add transcribe_deepgram_sync and propagate including to unittests
def transcribe_deepgram(audio_file_path, model):
    """ 
    Calls the Deepgram API to transcribe the given audio file using the specified Deepgram model.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription, accpets deepgram api call model or our suffix version (see below).
    :return: a dictionary containing the transcription results.
    """
    from primary.fileops import get_current_datetime_humanfriendly, convert_to_epoch_seconds, get_elapsed_seconds, convert_seconds_to_timestamp, convert_timestamp_to_seconds
    MIMETYPES = ['mp3', 'mp4', 'mp2', 'aac', 'wav', 'flac', 'pcm', 'm4a', 'ogg', 'opus', 'webm']  # Supported file types
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    # Check if the file type is supported
    if not any(audio_file_path.endswith(ext) for ext in MIMETYPES):
        raise ValueError(f"File {audio_file_path} does not have a supported MIME type.")

    if model == 'nova-2-general':
        suffix = "_nova2gen"
    elif model == 'nova-2-meeting':
        suffix = "_nova2meet"
    elif model == 'enhanced-meeting':
        suffix = "_enhmeet"
    elif model == 'whisper-medium':
        suffix = "_dgwhspm"
    elif model == 'whisper-large':
        suffix = "_dgwhspl"

    else:
        raise ValueError("Invalid or absent DeepGram model ('nova-2-general' 'nova-2-meeting' 'enhanced-meeting' 'whisper-medium' 'whisper-large').")

    json_file_path = None  # Initialize json_file_path to ensure it has a value
    try:
        print(f"Deepgram transcribing model: {model}  file : {audio_file_path}")
        
        with open(audio_file_path, "rb") as file:
            buffer_data = file.read()

        # Extract the file extension and prepare the correct MIME type
        file_extension = audio_file_path.rsplit('.', 1)[1]
        mimetype = f'audio/{file_extension}'

        payload: FileSource = {
            "buffer": buffer_data,
            "mimetype": mimetype,
        }

        # STEP 2: Configure Deepgram options for audio analysis
        options = {
            "punctuate": True, "diarize": True, "model": model, "intents": True, "sentiment": True,
            "summarize": True, "measurements": True, "smart_format": True, "topics": True
        }

        audio_length = get_media_length(audio_file_path)
        start_time = get_current_datetime_humanfriendly()
        print(f"Start Syncronous Deepgram Transcription at {start_time} for audio length of {audio_length}")
        # STEP 3: Call the transcribe_file method with the text payload and options
        # Use a timeout to prevent the write operation from timing out
        try:
            # Use the Deepgram client to transcribe the audio file
            response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options, timeout=30*60)
            print("Response received successfully.")
            print('\n'.join(str(response).splitlines()[:5]))  # Print only the first five lines of the response JSON
        except Exception as e:
            print(f"An error occurred: {e}")
        
        elapsed_time = get_elapsed_seconds(convert_to_epoch_seconds(start_time))
        transcribe_time_ratio = int(round(elapsed_time / convert_timestamp_to_seconds(audio_length)*100))
        print(f"Elapsed time is {convert_seconds_to_timestamp(elapsed_time)} which is {transcribe_time_ratio}% of the audio length")
        
        # STEP 4: Save the response as a JSON file
        response_json = response.to_json(indent=4)
        json_file_path = audio_file_path.rsplit('.', 1)[0] + suffix + '.json'
        with open(json_file_path, "w") as json_file:
            json_file.write(response_json)
        print(f"Transcription saved to {json_file_path}")
        #audio_duration = get_youtube_title_length(url)
        # TODO fill in code to print elapsed
    except Exception as e:
        print(f"Error during transcription: {e}")
    return json_file_path

def transcribe_deepgram_sdk_prerecorded(audio_file_path, model):
    """
    Calls the Deepgram API to transcribe the given audio file using the specified Deepgram model, utilizing the SDK.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription.
    :return: path to the JSON file containing the transcription results.
    """
    from primary.fileops import get_current_datetime_humanfriendly, convert_to_epoch_seconds, get_elapsed_seconds, convert_seconds_to_timestamp, convert_timestamp_to_seconds

    MIMETYPES = ['mp3', 'mp4', 'mp2', 'aac', 'wav', 'flac', 'pcm', 'm4a', 'ogg', 'opus', 'webm']
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    if not any(audio_file_path.endswith(ext) for ext in MIMETYPES):
        raise ValueError(f"File {audio_file_path} does not have a supported MIME type.")

    model_suffix_map = {
        'nova-2-general': "_nova2gen",
        'nova-2-meeting': "_nova2meet",
        'enhanced-meeting': "_enhmeet",
        'whisper-medium': "_dgwhspm",
        'whisper-large': "_dgwhspl"
    }

    if model not in model_suffix_map:
        raise ValueError("Invalid or absent DeepGram model.")

    suffix = model_suffix_map[model]
    json_file_path = None

    try:
        print(f"Deepgram transcribing model: {model}  file : {audio_file_path}")

        with open(audio_file_path, "rb") as audio:
            source = {'buffer': audio, 'mimetype': f'audio/{audio_file_path.rsplit(".", 1)[1]}'}

        options = PrerecordedOptions(
            model=model,
            punctuate=True,
            diarize=True,
            intents=True,
            sentiment=True,
            summarize=True,
            measurements=True,
            smart_format=True,
            topics=True
        )

        audio_length = get_media_length(audio_file_path)
        start_time = get_current_datetime_humanfriendly()
        print(f"Start Synchronous Deepgram Transcription at {start_time} for audio length of {audio_length}")

        response = deepgram.transcription.sync_prerecorded(source, options)
        print("Response received successfully.")
        print('\n'.join(str(response).splitlines()[:5]))

        elapsed_time = get_elapsed_seconds(convert_to_epoch_seconds(start_time))
        transcribe_time_ratio = int(round(elapsed_time / convert_timestamp_to_seconds(audio_length)*100))
        print(f"Elapsed time is {convert_seconds_to_timestamp(elapsed_time)} which is {transcribe_time_ratio}% of the audio length")

        json_file_path = audio_file_path.rsplit('.', 1)[0] + suffix + '.json'
        with open(json_file_path, "w") as json_file:
            json.dump(response, json_file, indent=4)
        print(f"Transcription saved to {json_file_path}")

    except Exception as e:
        print(f"Error during transcription: {e}")

    return json_file_path


# TODO create APICALL and APIMOCK unittests
# TODO update with options and other stuff from sync version AND FIX THE MODEL PROBLEM!!
# TODO add model to return tuple
def transcribe_deepgram_callback(audio_file_path, model, callback_url):
    """
    Transcribes the given audio file using the specified Deepgram model asynchronously with a callback URL.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription.
    :param callback_url: URL to which Deepgram will send the transcription results.
    :return: Request ID from Deepgram indicating that the file has been accepted for processing.
    """
    from primary.fileops import get_current_datetime_humanfriendly

    # Supported MIME types mapping
    MIMETYPES = {
        'mp3': 'audio/mpeg',
        'mp4': 'audio/mp4',
        'wav': 'audio/wav',
        'flac': 'audio/flac',
        # add other supported formats as necessary
    }

    file_extension = audio_file_path.rsplit('.', 1)[1]
    if file_extension not in MIMETYPES:
        raise ValueError(f"File {audio_file_path} does not have a supported MIME type.")

    mimetype = MIMETYPES[file_extension]

    headers = {
        'Authorization': f'Token {DEEPGRAM_API_KEY}',
        'Content-Type': mimetype
    }

    # Set up the query parameters with the callback URL
    params = {
        'callback': callback_url,
        # 'punctuate': True, # it works if this line is commented out
        # 'diarize': True,  # it works if this line is commented out
        'model': model
    }

    with open(audio_file_path, 'rb') as file:
        audio_data = file.read()

    audio_length = get_media_length(audio_file_path)
    start_time = get_current_datetime_humanfriendly()
    print(f"Start Callback Deepgram Transcription at {start_time} for audio length of {audio_length}")
        
    response = post(
        url='https://api.deepgram.com/v1/listen',
        headers=headers,
        params=params,
        data=audio_data
    )

    # Adjusted to accept both 200 and 202 status codes as successful
    if response.status_code in (200, 202):        
        callback_response = response.json()
        request_id = callback_response.get('request_id', 'NO REQUEST_ID FIELD FOUND IN JSON')
        if request_id == 'NO REQUEST_ID FIELD FOUND IN JSON':
            print(f"Deepgram Callback FAIL - {request_id}")
        else:
            print(f"Deepgram Callback SUCCESS - request_id: {request_id}")
        base_audio_file_name = os.path.splitext(os.path.basename(audio_file_path))[0]
        return (request_id, base_audio_file_name, model)

    else:
        raise Exception(f"Failed to submit audio: {response.text}, Status Code: {response.status_code}")




        # json_data = response.json()
        # with open('tests/test_manual_files/1min youttube/155500a5-83f5-4b56-a4bb-372aa25a29b2.json', 'r') as file:
        #     json_data = json.load(file)

        # request_id = json_data.get('request_id', 'NO REQUEST_ID FIELD FOUND IN JSON')
        # created_timestamp = json_data.get('created', 'NO CREATED FIELD FOUND IN JSON')

        # s3_bucket = 'fofpublic'
        # s3_path = 'deepgram-transcriptions'
        # cur_s3_object_name = f"{request_id}.json"
        # json_data = get_s3_json(s3_bucket, cur_s3_object_name, s3_path)
        # print(f"First characters of received JSON:\n\n{json.dumps(json_data)[:500]}")

        # created_timestamp = json_data.get('metadata', {}).get('created', 'NO CREATED FIELD FOUND IN JSON').replace(':', '').split('.')[0]
        
        # new_s3_object_name = f"{base_audio_file_name}_{created_timestamp}.json"
        # #rename_s3_object(s3_bucket, old_s3_object_name, new_s3_object_name, s3_path=s3_path)
        # return new_s3_object_name
def transcribe_deepgram_callback2(audio_file_path, model, callback_url):
    """
    Transcribes the given audio file using the specified Deepgram model asynchronously with a callback URL.

    :param audio_file_path: path to the audio file to be transcribed.
    :param model: the Deepgram model to use for transcription.
    :param callback_url: URL to which Deepgram will send the transcription results.
    :return: Request ID from Deepgram indicating that the file has been accepted for processing.
    """
    from primary.fileops import get_current_datetime_humanfriendly
    import os

    # Supported MIME types mapping
    MIMETYPES = {
        'mp3': 'audio/mpeg',
        'mp4': 'audio/mp4',
        'wav': 'audio/wav',
        'flac': 'audio/flac',
    }

    file_extension = audio_file_path.rsplit('.', 1)[1]
    if file_extension not in MIMETYPES:
        raise ValueError(f"File {audio_file_path} does not have a supported MIME type.")

    mimetype = MIMETYPES[file_extension]

    headers = {
        'Authorization': f'Token {DEEPGRAM_API_KEY}',
        'Content-Type': mimetype
    }

    # Set up the query parameters with the callback URL
    params = {
        'callback': callback_url,
        #'punctuate': True,
        #'diarize': True,
        'model': model,
    }

    with open(audio_file_path, 'rb') as file:
        audio_data = file.read()

    audio_length = get_media_length(audio_file_path)
    start_time = get_current_datetime_humanfriendly()
    print(f"Start Callback Deepgram Transcription at {start_time} for audio length of {audio_length}")

    try:
        response = post(
            url='https://api.deepgram.com/v1/listen',
            headers=headers,
            params=params,
            data=audio_data,
        )
    except exceptions.SSLError as ssl_err:
        print(f"SSL error: {ssl_err}")
        raise
    except exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")
        raise

    if response.status_code in (200, 202):
        callback_response = response.json()
        request_id = callback_response.get('request_id', 'NO REQUEST_ID FIELD FOUND IN JSON')
        if request_id == 'NO REQUEST_ID FIELD FOUND IN JSON':
            print(f"Deepgram Callback FAIL - {request_id}")
        else:
            print(f"Deepgram Callback SUCCESS - request_id: {request_id}")
        base_audio_file_name = os.path.splitext(os.path.basename(audio_file_path))[0]
        return (request_id, base_audio_file_name, model)
    else:
        raise Exception(f"Failed to submit audio: {response.text}, Status Code: {response.status_code}")
# TODO come back and review this to troubleshoot deepgram whisper transcription
def transcribe_deepgram_OLD_fixhang(file_path, timeout_duration=1*60*60):
    json_file_path = None
    progress_thread = None
    stop_event = threading.Event()
    try:
        if file_path.endswith(MIMETYPE):
            print(f"Starting Deepgram transcription at {get_current_time_str()}")

            # Print the size of the file in MB
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"File size: {file_size_mb:.2f} MB")

            # Start the progress thread with the stop event
            progress_thread = threading.Thread(target=print_progress, args=(timeout_duration, stop_event))
            progress_thread.start()

            with open(file_path, "rb") as f:
                source = {"buffer": f, "mimetype": 'audio/' + MIMETYPE}

                # Start the transcription process
                print(f"Deepgram transcribing file: {file_path}")
                print("Progress: ", end="")

                res = dg.transcription.sync_prerecorded(source, dg_options)

                # Signal the progress thread to stop
                stop_event.set()

                json_file_path = file_path[:-4] + dg_suffix + '.json'
                with open(json_file_path, "w") as transcript:
                    json.dump(res, transcript, indent=4)
                print(f"\nDeepgram transcribe successful on file: {file_path}")
        else:
            print(f"File {file_path} does not end with {MIMETYPE}")
    except Exception as e:
        print(f"Error during transcription: {e}")
    finally:
        # Signal the progress thread to stop and ensure it is stopped
        if progress_thread is not None:
            stop_event.set()
            progress_thread.join(timeout=0)
    return json_file_path
def get_summary_start_seconds(data, index):
    """ 
    Retrieves the start time in seconds of a word from the transcription data at the given index.

    :param data: dictionary of the transcription data.
    :param index: integer of the index of the word to find the start time for.
    :return: integer of the start time in seconds of the specified word, rounded down to the nearest whole number.
    """
    words_list = data.get('results', {}).get('channels', [])[0].get('alternatives', [])[0].get('words', [])
    if index < len(words_list):
        return math.floor(words_list[index].get('start', 0))
    return 0
def format_feature_segment(feature, segment, data):
    """
    Formats a segment of a feature with a timestamp and additional info.

    :param feature: string, the feature being extracted.
    :param segment: dict, the segment of the feature to be formatted.
    :param data: dict, the JSON data from the Deepgram file.
    :return: string, the formatted segment.
    """
    from primary.fileops import convert_seconds_to_timestamp

    singular_feature_json = feature[:-1]  # Remove the last character to make it singular as found in the JSON
    singular_feature_print = singular_feature_json.capitalize()  # Capitalize the singular form for printing
    segment_text = segment.get('text', '')
    segment_start_index = int(segment.get('start_word', 0))
    segment_start_secs = get_summary_start_seconds(data, segment_start_index)
    segment_timestamp = convert_seconds_to_timestamp(segment_start_secs)
    segment_midline = ""

    if feature.lower() == "summaries":
        singular_feature_json = 'summary'
        singular_feature_print = singular_feature_json.capitalize()
        segment_text = segment.get(singular_feature_json, '')
    elif feature.lower() == "sentiments":
        sentiment = segment.get('sentiment')
        sentiment_score = segment.get('sentiment_score')
        segment_midline = f"{sentiment} - sentiment_score = {sentiment_score:.2f}"
    elif feature.lower() == "topics":
        # Assuming there's only one topic per segment, hence index [0]
        topic_info = segment.get('topics', [{}])[0]
        topic_name = topic_info.get('topic')
        confidence_score = topic_info.get('confidence_score')
        segment_midline = f"{topic_name} - confidence_score = {confidence_score:.2f}"
    elif feature.lower() == "intents":
        # Assuming there's only one intent per segment, hence index [0]
        intent_info = segment.get('intents', [{}])[0]
        intent_name = intent_info.get('intent')
        confidence_score = intent_info.get('confidence_score')
        segment_midline = f"{intent_name} - confidence_score = {confidence_score:.2f}"

    formatted_segment = f"{singular_feature_print}  {segment_timestamp}\n"
    if segment_midline:
        formatted_segment += f"{segment_midline}\n"
    formatted_segment += f"{segment_text}\n\n"

    return formatted_segment
def extract_feature_from_deepgram_json(json_file_path, feature):
    """
    Extract a specific feature section from a Deepgram JSON file and return it as a string.

    :param json_file_path: string of the path to the JSON file from which the feature is to be extracted.
    :param feature: string of the feature of the section to be extracted.
    :return: string of the extracted text under the specified feature, preceded by the feature itself (no pound signs) and a blank line.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        extracted_text = ''
        if feature == "summaries":
            summaries = data.get('results', {}).get('channels', [])[0].get('alternatives', [])[0].get(feature, [])
            #print(f"DEBUG summaries {summaries}")
            for summary in summaries:
                extracted_text += format_feature_segment(feature, summary, data)
        elif feature in ["sentiments", "topics", "intents"]:
            segments = data.get('results', {}).get(feature, {}).get('segments', [])
            #print(f"DEBUG {feature} {segments}")
            for segment in segments:
                extracted_text += format_feature_segment(feature, segment, data)
        else:
            warnings.warn(f"in extract_feature_from_deepgram_json - Feature '{feature}' not found in Deepgram JSON")
            return None

        if extracted_text:
            return f"{extracted_text.strip()}\n\n"
        else:
            warnings.warn(f"in extract_feature_from_deepgram_json - Feature '{feature}' was found in Deepgram JSON but extracted text is None or empty string (should not get this warning!)")
            return None
    except Exception as e:
        raise ValueError(f"Error extracting {feature} from {json_file_path}: {e}")
def validate_transcript_json(json_file_path):
    """
    Validates the structure of a JSON file to ensure it contains specific keys and types.

    :param json_file_path: string of the path to the JSON file to be validated.
    :return: boolean, True if the JSON structure is as expected, False otherwise.
    """
    if not os.path.exists(json_file_path):
        raise ValueError(f"The file path does not exist for {json_file_path}.")
    
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Access the nested structure with checks for KeyError and TypeError
        results = data.get("results")
        if results is None:
            raise KeyError("results key not found")

        channels = results.get("channels")
        if not isinstance(channels, list) or not channels:
            raise TypeError("channels is not a non-empty list")

        alternatives = channels[0].get("alternatives")
        if not isinstance(alternatives, list) or not alternatives:
            raise TypeError("alternatives is not a non-empty list")

        words_data = alternatives[0].get("words")
        if not isinstance(words_data, list) or len(words_data) <= 1:
            raise ValueError("The list of words is empty or has only one word.")

        paragraphs_data = alternatives[0].get("paragraphs")
        if paragraphs_data is None:
            raise KeyError("paragraphs key not found")

        transcript = paragraphs_data.get("transcript", "").strip()
        if not transcript:
            raise ValueError("The transcript in paragraphs is empty.")

        paragraphs_list = paragraphs_data.get("paragraphs")
        if not isinstance(paragraphs_list, list) or not paragraphs_list:
            raise ValueError("There are no paragraphs in paragraphs.")

    except (KeyError, TypeError, ValueError) as e:
        print(f"Error occurred with file {json_file_path}: {str(e)}")
        return False

    return True
def set_various_transcript_headings(file_path, feature, source):
    """
    Sets the transcript heading in a file based on the extracted feature from a specified source.

    :param file_path: string of the path to the file where the heading is to be set.
    :param feature: string of the feature to extract and use as the heading.
    :param source: string of the source from which to extract the feature ('deepgram' or 'youtube').
    :return: None.
    """
    from primary.fileops import set_heading, add_suffix_in_str, remove_all_suffixes_in_str, find_file_in_folders  # seems to be needed for unittest, see Claude thread

    folder_paths = ["data/f_c9_done_json_yt_host"]     
    if source == "deepgram":
        dg_json_file_path = file_path.replace('.md', '.json')
        if not os.path.isfile(dg_json_file_path):
            dg_json_file_path = find_file_in_folders(dg_json_file_path, folder_paths)
            if dg_json_file_path is None:
                raise ValueError(f"No companion deepgram json file found for {file_path}")
        extracted_feature_text = extract_feature_from_deepgram_json(dg_json_file_path, feature)
    elif source == "youtube":
        yt_md_file_path = add_suffix_in_str(remove_all_suffixes_in_str(file_path), "_yt")
        if not os.path.isfile(yt_md_file_path):
            yt_md_file_path = find_file_in_folders(yt_md_file_path, folder_paths)
            if yt_md_file_path is None:
                raise ValueError(f"No companion youtube md file found for {file_path}")
        extracted_feature_text = extract_feature_from_youtube_md(yt_md_file_path, feature)
    else:
        raise ValueError("source invalid")
    if extracted_feature_text is None:
        return

    set_heading(file_path, extracted_feature_text, "### " + feature)

### NUMERAL CONVERT
def extract_context(line, match, context_radius):
    """ 
    Extracts a context window around a regex match within a string of text.

    :param line: string of text containing the match.
    :param match: regex match object containing the start and end positions of the match within the line.
    :param context_radius: integer specifying the number of words around the match to include in the context window.
    :return: string of text representing the context window around the match.
    """
 
    if match is None:
        raise ValueError("Match not found")

    # Define the number of words around the match to include in the context
    words = line.split()
    match_word_index = None

    # Find the index of the word that contains the match
    for index, word in enumerate(words):
        if match.start() >= line.find(word) and match.end() <= line.find(word) + len(word):
            match_word_index = index
            break

    if match_word_index is None:
        raise ValueError("Match not found within the words of the line")

    # Calculate the start and end indices for the context window
    context_start = max(match_word_index - context_radius, 0)
    context_end = min(match_word_index + context_radius + 1, len(words))

    # Extract the context window from the line
    context_window = ' '.join(words[context_start:context_end])
    return context_window
def print_num_exception(match_str, line_number, num_metadata_lines, printed_exceptions, exception_type, line):
    """ 
    Prints a message for numbers that are excluded from conversion and records the message.

    :param match_str: the string that matches the number to be excluded from conversion.
    :param line_number: the current line number in the file being processed.
    :param num_metadata_lines: the number of metadata lines in the file to adjust the actual line number.
    :param printed_exceptions: a list of exception messages that have already been printed.
    :param exception_type: the type of exception to be printed.
    :param line: the current line of text being processed.
    :return: None, but updates the printed_exceptions list with the new exception message if it hasn't been printed before.
    """
    match = re.search(re.escape(match_str), line)
    if match:
        exception_msg = f"Excluding conversion for {exception_type} at line {line_number+1+num_metadata_lines}: ...{extract_context(line, match, 5)}..."
        if exception_msg not in printed_exceptions:
            print(exception_msg)
            printed_exceptions.append(exception_msg)
    # DEBUG CODE to check if certain words are in english_vocab
    # debug_words = ["Like", "And", "Orca", "Shirley", "FTGSTKLOMNB"]
    # for word in debug_words:
    #     print(f"Is '{word}' in common_english_vocab? {'yes' if word.lower() in common_english_vocab else 'no'}")
def get_previous_word(substring, start_index):
    """ 
    Finds the word in a string that precedes the given start index.

    :param substring: the string from which to extract the previous word.
    :param start_index: the index in the string to start searching backward from.
    :return: the word found before the start index, or an empty string if no word is found.
    """
    # Find the last non-space character before the start_index
    word_end = start_index
    while word_end > 0 and substring[word_end-1].isspace():
        word_end -= 1
    # Find the start of the word
    word_start = word_end
    while word_start > 0 and not substring[word_start-1].isspace():
        word_start -= 1
    # Return the word found, if any
    return substring[word_start:word_end] if word_start != word_end else ""
def previous_word_exception(word, common_english_vocab, additional_exception_words):
    """ 
    Determines if a word is an exception based on its presence in additional exceptions or English vocabulary.

    :param word: the word to check for exception status.
    :param common_english_vocab: a set of common English words to compare against.
    :param additional_exception_words: a set of words that are always considered exceptions.
    :return: True if the word is an exception, False otherwise.
    """
    if word.lower() in additional_exception_words:
        #print(f"DEBUG: '{word}' before the number is in the additional exception list.")
        return True
    if word.istitle() and word.lower() not in common_english_vocab:
        #print(f"DEBUG: Capitalized '{word}' before the number is not in common English vocabulary.")
        return True
    return False
def convert_num_line_lowercase(line, num, num_str, line_number, num_metadata_lines, printed_exceptions, common_english_vocab):
    """ 
    Converts numbers in a line of text to their lowercase word equivalents, skipping exceptions.

    :param line: The line of text in which to convert numbers.
    :param num: The numerical value to convert to words.
    :param num_str: The string representation of the number to find in the line.
    :param line_number: The current line number in the text being processed.
    :param num_metadata_lines: The number of metadata lines in the text before the content.
    :param printed_exceptions: A set to record exceptions that have been printed.
    :param common_english_vocab: A set of common English vocabulary words.
    :return: A tuple containing the modified line and the total number of substitutions made.
    """
    num_subs_total = 0
    current_index = 0
    additional_exception_words = ["step"]
    while current_index < len(line):
        if line[current_index].isdigit():
            # Check if the digit is adjacent to any characters that are not digits or allowed punctuation
            if (current_index > 0 and not line[current_index-1] in '0123456789.,?! \n') or \
               (current_index < len(line) - 1 and not line[current_index+1] in '0123456789.,?! \n'):
                # Search forward until a space or a new line is found
                while current_index < len(line) and not line[current_index] in ' \n':
                    current_index += 1
                continue
            # Skip conversion if the digit is part of a decimal number (e.g., "1.0")
            if current_index < len(line) - 1 and not line[current_index+1].isdigit() and \
               current_index + 2 < len(line) and line[current_index+2].isdigit():
                current_index += 3  # Skip past the decimal point and the following digit(s)
                while current_index < len(line) and (line[current_index].isdigit() or line[current_index].isspace() or line[current_index] in '.,!?'):
                    current_index += 1
                continue
            # Check if the character directly before the number is a period, then skip conversion
            if current_index > 0 and line[current_index-1] == '.':
                    current_index += 2  # Skip past the period and the decimal point
                    while current_index < len(line) and line[current_index].isdigit():
                        current_index += 1
                    continue
            # Skip conversion if the number starts the line or is preceded only by whitespace and followed by a period and a space
            if (current_index == 0 or (current_index > 0 and line[:current_index].isspace())) and \
               (current_index + 1 < len(line) and line[current_index+1] == '.' and \
                (current_index + 2 < len(line) and line[current_index+2] == ' ')):
                current_index += 3  # Skip past the period and the space
                continue
            end_index = current_index + 1
            while end_index < len(line) and line[end_index].isdigit():
                end_index += 1
            number_str = line[current_index:end_index]
            if number_str == num_str:
                previous_word = get_previous_word(line, current_index)
                if not previous_word_exception(previous_word, common_english_vocab, additional_exception_words):
                    new_line, num_subs = re.subn(r'\b' + re.escape(num_str) + r'\b', num2words(num), line[current_index:], 1)
                    num_subs_total += num_subs
                    line = line[:current_index] + new_line
                    current_index = end_index
                else:
                    print_num_exception(line[current_index:end_index], line_number, num_metadata_lines, printed_exceptions, "proper name", line)
            current_index = end_index
        else:
            current_index += 1
    return line, num_subs_total
    # old comment - need to fix $3zero - found in FloodLAMP_Demo13_Plate_v1.md 'It cost about $30, but super helpful.'
def convert_num_line_capitalization(line, num, num_str):
    """ 
    Capitalize the numeral word at the beginning of a sentence or after punctuation.

    :param line: the line of text in which to perform capitalization.
    :param num: the numerical value to convert to words.
    :param num_str: the string representation of the number to find in the line.
    :return: a tuple containing the modified line and the total number of substitutions made.
    """
    num_subs_total = 0
    for punctuation in ['.', '?', '!']:
        # Include comma in the lookahead assertion
        pattern = r'(^|[' + re.escape(punctuation) + r']\s)' + re.escape(num_str) + r'(?=[\s,]|$)'
        new_line, num_subs = re.subn(pattern, lambda match: match.group(1) + num2words(num).capitalize(), line)
        num_subs_total += num_subs
        if num_subs > 0:
            line = new_line
    return line, num_subs_total
def skip_speaker_line_with_timestamp(line):
    """ 
    Determine if a line contains a single timestamp with max_words before the timestamp less that get_timestamp default val (8) and is therefore a speaker line to skip.

    :param line: The line of text to be checked for a timestamp.
    :return: boolean where True if a timestamp is found, otherwise False.
    """
    from primary.fileops import get_timestamp
    timestamp_result = get_timestamp(line)
    return timestamp_result and any(value is not None for value in timestamp_result)
def convert_num_lines(lines, num, num_str, num_metadata_lines, verbose, printed_exceptions):
    """ 
    Converts numbers in lines of text to their word equivalents, handles capitalization, and skips lines with timestamps.
    Takes both num and num_str as separate parameters to provide flexibility in how the function is called.
    This design allows the caller to specify the string representation of the number 1 that should be searched for within the text lines,
    which may not always be a straightforward string conversion of num.
    For example, num could be an integer, but num_str could be a formatted string that represents the number
    in a specific way within the text (e.g., "001" instead of "1", or "1st" for the ordinal form).
    
    :param lines: list of text lines to process.
    :param num: the numerical value to convert to words.
    :param num_str: the string representation of the number to find in the lines.
    :param num_metadata_lines: the number of metadata lines in the document to adjust line numbering for output.
    :param verbose: boolean indicating whether to print the conversion output.
    :param printed_exceptions: list to record any exceptions encountered during processing.
    :return: tuple containing the list of processed lines and the total number of substitutions made.
    """
    num_subs_total = 0
    for i, line in enumerate(lines):
        if skip_speaker_line_with_timestamp(line):
            continue  # Skip lines with timestamps
        line, num_subs = convert_num_line_capitalization(line, num, num_str)
        num_subs_total += num_subs
        if num_subs > 0 and verbose:
            print(f"  convert in line {i+1+num_metadata_lines} the number: {num}")
        line, num_subs = convert_num_line_lowercase(line, num, num_str, i, num_metadata_lines, printed_exceptions, common_english_vocab)
        num_subs_total += num_subs
        lines[i] = line  # Update the line in lines
    return lines, num_subs_total
def convert_numbers_in_content(content, num_limit, additional_numbers, num_metadata_lines, print_output):
    """ 
    Converts numerical values in text content to their word equivalents, excluding lines with timestamps.

    :param content: string containing the text content to be processed.
    :param num_limit: integer representing the upper limit for numbers to convert.
    :param additional_numbers: list of additional numbers to be converted outside the standard range.
    :param num_metadata_lines: integer representing the number of metadata lines in the content.
    :param print_output: boolean indicating whether to print the conversion output.
    :return: tuple containing the converted content as a string and the total number of substitutions made.
    """
    lines = content.split('\n')  # Break the content into lines
    num_subs_total = 0  # Initialize counter for the number of conversions
    printed_exceptions = []  # Initialize a list to keep track of printed exceptions
    for num in list(range(num_limit)) + additional_numbers:  # Loop over all numbers from 0 to 9 and additional numbers
        num_str = str(num)  # Convert the number to a string
        lines, num_subs = convert_num_lines(lines, num, num_str, num_metadata_lines, print_output, printed_exceptions)
        num_subs_total += num_subs
        #print(f"Convert number {num} with conversions: {num_subs}")
    return '\n'.join(lines), num_subs_total
def convert_ordinals_in_content(content, punct_capitalization):
    """ 
    Converts ordinal numbers in a string of text to their word equivalents and capitalizes words following specified punctuation.

    :param content: string of text containing ordinal numbers and punctuation.
    :param punct_capitalization: list of punctuation characters after which the following word should be capitalized.
    :return: string of text with ordinal numbers converted and words capitalized as specified.
    """

    ordinal_map = {
        '1st': 'first', '2nd': 'second', '3rd': 'third', '4th': 'fourth',
        '5th': 'fifth', '6th': 'sixth', '7th': 'seventh', '8th': 'eighth',
        '9th': 'ninth'
    }
    converted_content = content
    for ordinal, word in ordinal_map.items():
        converted_content = re.sub(r'\b' + re.escape(ordinal) + r'\b', word, converted_content)
    # Capitalize where necessary
    for punctuation in punct_capitalization:
        pattern = r'(^|[' + re.escape(punctuation) + r']\s)(\w)'
        converted_content = re.sub(pattern, lambda match: match.group(1) + match.group(2).upper(), converted_content)
    return converted_content
    # DONE fill in code to change "1st" to "first", "2nd" to "second", etc. up to "9th"
    # DONE fill in code to capilatize when needed as is done in @convert_nums_to_words
def convert_nums_to_words(file_path, verbose=False):
    """
    Converts numerals in the content of a file to their corresponding words, appends a specified suffix to the filename, and creates a new file with the converted content.

    :param file_path: string of the path to the original file.
    :param verbose: boolean for printing verbose messages. Defaults to False.
    :return: string of the path to the newly created file with the converted content.
    """
    from primary.fileops import read_file_flex, write_metadata_and_content, verbose_print

    num_limit = 10  # number up to which will be converted plus any additional numbers
    additional_numbers = [1000000, 1000000000, 1000000000000]
    metadata, content = read_file_flex(file_path)
    
    # Handle case where metadata is None (no metadata in file)
    num_metadata_lines = 0 if metadata is None else len(metadata.splitlines())
    
    content = convert_ordinals_in_content(content, ['.', '?', '!'])
    converted_content, num_subs_total = convert_numbers_in_content(content, num_limit, additional_numbers, num_metadata_lines, verbose)

    verbose_print(verbose, "Review and fix manually: addresses")
    verbose_print(verbose, f"END convert_nums_to_words - Conversion Count: {num_subs_total}\n")
    write_metadata_and_content(file_path, metadata, converted_content, overwrite='yes')
    return file_path  # Return the path of the modified file

### SPEAKER NAMES
def read_speaker_names_from_json(json_file_path):
    """ 
    Reads speaker names from a JSON file's metadata, which have been inserted by us and are not in the raw deepgram json files.

    :param json_file_path: string of the path to the JSON file.
    :return: list of speaker names if they exist, otherwise an empty list.
    """ 
    if not os.path.exists(json_file_path):
        raise ValueError(f"The file path does not exist for {json_file_path}.")
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Return the speaker_names if they exist in the metadata
    return data.get('metadata', {}).get('speaker_names', [])
def write_speaker_names_to_json(json_file_path, speaker_names, verbose=False):
    """ 
    Writes speaker names to a JSON file's metadata. Overwrites file.

    :param json_file_path: string of the path to the JSON file.
    :param speaker_names: list of strings containing speaker names.
    :return: None.
    """ 
    from primary.fileops import verbose_print

    if not os.path.exists(json_file_path):
        raise ValueError(f"The file path does not exist for {json_file_path}.")
    # Read the existing JSON file's content
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Initialize a flag to check if speaker_names have been updated
    speaker_names_updated = False

    # Check if 'metadata' exists and if 'speaker_names' is present
    if 'metadata' in data and 'speaker_names' in data['metadata']:
        # If the new speaker_names are different from the existing ones, update them
        if data['metadata']['speaker_names'] != speaker_names:
            data['metadata']['speaker_names'] = speaker_names
            speaker_names_updated = True
    else:
        # If 'metadata' does not exist or 'speaker_names' is not present, create 'metadata' with speaker_names
        data.setdefault('metadata', {}).update({'speaker_names': speaker_names})
        speaker_names_updated = True

    # Write the modified data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    # Print a statement to the console if the speaker_names have been updated
    if speaker_names_updated:
        verbose_print(verbose, f"Speaker names in the JSON have been updated.")
    else:
        verbose_print(verbose, f"Speaker names in the JSON are unchanged.")
def find_unassigned_speakers(md_file_path, verbose=False):
    """ 
    Identifies speakers in the markdown file who do not have assigned names.
    This is determined by if the line has a valid timestamp and then looking for 'Speaker X' before the timestamp.

    :param md_file_path: string of the path to the markdown file.
    :return: list of strings of unassigned speaker names, or None if all speakers are assigned.
    """
    from primary.fileops import verbose_print, get_timestamp
    
    if not os.path.exists(md_file_path):
        raise ValueError(f"The file path does not exist for {md_file_path}.")

    unassigned_speaker_numbers = []
    with open(md_file_path, 'r') as md_file:
        for line in md_file:
            timestamp_index = get_timestamp(line)
            if timestamp_index:
                # Search for unnamed speaker pattern before the timestamp
                match = re.search(r"Speaker\s+(\d+)", line[:timestamp_index[1]])
                if match:
                    speaker_number = int(match.group(1))
                    if speaker_number not in unassigned_speaker_numbers:
                        unassigned_speaker_numbers.append(speaker_number)

    # Sort the list of unassigned speaker numbers
    unassigned_speaker_numbers.sort()

    # Convert the sorted list of numbers to the required string format
    unassigned_speakers = [f"Speaker {number}" for number in unassigned_speaker_numbers]

    num_unassigned = len(unassigned_speakers)
    if num_unassigned > 0:
        verbose_print(verbose, f"From find_unassigned_speakers - Number of speakers not assigned names: {num_unassigned}. Speaker names: {' '.join(unassigned_speakers)}")
        return unassigned_speakers
    else:
        verbose_print(verbose, f"From find_unassigned_speakers - All speakers have been assigned names.")
        return None
    # DONE fill in code to find all speakers without names assigned ('Speaker X') using code similar to @propagate_speaker_names_throughout_md
    # DONE fill in code to print the number of speakers not assigned followed by the specific speaker numbers, as a single print line
    # DONE return a list of the unassigned speaker numbers or NONE
# TODO think this is done but double check - change to propagate the speaker assignment backwards as well as forwards in the Markdown file.
def propagate_speaker_names_throughout_md(md_file_path, input_speaker_names=None):
    """
    Propagates speaker names throughout a markdown file based on provided input names or existing assignments.

    :param md_file_path: string of the path to the markdown file.
    :param input_speaker_names: list of tuples with speaker numbers and names, if available.
    :return: list of tuples with speaker numbers and names after propagation.
    """
    from primary.fileops import get_timestamp

    # Initialize speaker names list based on input
    speaker_names = input_speaker_names.copy() if input_speaker_names else []

    # Read the content of the markdown file
    with open(md_file_path, 'r') as file:
        content = file.readlines()

    updated_content = []
    for i, line in enumerate(content):
        # Extract timestamp index from the line
        _, index = get_timestamp(line, max_words=10)
        if index is not None:
            # Search for speaker name assignment before the timestamp
            match = re.search(r"Speaker\s+(\d+)\s*=\s*(.+)", line[:index])
            if match:
                speaker_num, name = match.groups()
                speaker_num = int(speaker_num)  # Ensure speaker number is an integer
                name = name.strip()
                # Add new speaker name if not already in the list
                if (speaker_num, name) not in speaker_names:
                    speaker_names.append((speaker_num, name))
                # Update the line with the speaker name and timestamp
                line = f"{name}  {line[index:].lstrip()}"
            else:
                # Replace speaker placeholders with names throughout the document
                for spkr_num, spkr_name in speaker_names:
                    line = re.sub(rf"\bSpeaker {spkr_num}\b\s*", f"{spkr_name}  ", line)

        updated_content.append(line)

    # After the forward pass, perform a backward pass to propagate names to earlier mentions
    for i in range(len(updated_content) - 1, -1, -1):
        line = updated_content[i]
        _, index = get_timestamp(line, max_words=10)
        if index is not None:
            for spkr_num, spkr_name in speaker_names:
                line = re.sub(rf"\bSpeaker {spkr_num}\b\s*", f"{spkr_name}  ", line)
            updated_content[i] = line    

    # Write the updated content back to the markdown file
    with open(md_file_path, 'w') as file:
        file.writelines(updated_content)

    # Sort the speaker names by speaker number for consistency
    speaker_names.sort(key=lambda x: x[0])
    return speaker_names
def iterate_input_speaker_names(md_file_path, input_speaker_names=None):
    """
    Iterates over input speaker names and updates the markdown file until the user decides to exit.

    :param md_file_path: string of the path to the markdown file.
    :param input_speaker_names: list of tuples with speaker numbers and names, if available.
    :return: list of tuples with speaker numbers and names after all iterations.
    """
    if not os.path.exists(md_file_path):
        raise ValueError(f"The file path does not exist for {md_file_path}.")

    overall_speaker_names = input_speaker_names.copy() if input_speaker_names else []

    while True:
        current_speaker_names = propagate_speaker_names_throughout_md(md_file_path, overall_speaker_names)
        
        for speaker_name in current_speaker_names:
            if speaker_name not in overall_speaker_names:
                overall_speaker_names.append(speaker_name)
        
        overall_speaker_names.sort(key=lambda x: x[0])
        
        if not overall_speaker_names:
            print("No Speaker Names")
        else:
            print("Current speaker_names:")
            for num, name in overall_speaker_names:
                print(f"Speaker {num}: {name}")
        
        continue_prompt = input("\nASSIGN SPEAKER NAMES NOW - hit enter to continue or E/exit to exit: ").strip().lower()
        if continue_prompt == '':
            continue
        elif continue_prompt in ['e', 'exit']:
            unassigned_speakers = find_unassigned_speakers(md_file_path)
            if unassigned_speakers:
                print("Unassigned speakers:")
                for spkr in unassigned_speakers:
                    print(f"  {spkr}")
            else:
                print("All speakers have been assigned.")
            print("\nAssigned speaker names:")
            for num, name in overall_speaker_names:
                print(f"  Speaker {num}: {name}")
            return overall_speaker_names
        else:
            print("Invalid input. Please either hit enter to continue or type 'E'/'Exit' to exit.")
def assign_speaker_names(md_file_path):
    """
    Assigns speaker names to markdown file by reading from a corresponding JSON file, updating, and writing back to the json if changed.
    Prompts the user iteratively through assigning the names.
    
    :param md_file_path: string of the path to the markdown file.
    :return: None
    """
    json_file_path = md_file_path.replace('.md', '.json')
    try:
        with open(json_file_path, 'r') as file:
            # Check if there is a corresponding JSON file
            speaker_names = read_speaker_names_from_json(json_file_path)
    except FileNotFoundError:
        # If the JSON file does not exist, start with an empty list
        speaker_names = []

    # Iterate over speaker_names and update them
    updated_speaker_names = iterate_input_speaker_names(md_file_path, speaker_names)

    # Check if the updated speaker_names are different from the original ones
    if updated_speaker_names != speaker_names:
        # Write the updated speaker_names back to the JSON file
        write_speaker_names_to_json(json_file_path, updated_speaker_names)

### TRANSCRIBE WRAPPER
def create_transcript_md_from_json(json_file_path, combine_segs=True):
    """
    Creates a markdown transcript from a JSON file containing Deepgram transcription data.
    If combine_segs is True, combines consecutive segments from the same speaker.

    :param json_file_path: string of the path to the json file containing transcription data.
    :param combine_segs: boolean indicating whether to combine consecutive segments from the same speaker.
    :return: string of the path to the created markdown file or None if the json file is not valid.
    """
    from primary.fileops import create_initial_metadata, convert_seconds_to_timestamp, set_metadata_field
    from primary.fileops import write_metadata_and_content, add_timestamp_links
    
    md_file_path = json_file_path[:-5] + ".md"
    link = get_link_from_json(json_file_path)
    lines = []

    if not validate_transcript_json(json_file_path):
        return None

    with open(json_file_path, "r") as file:
        data = json.load(file)
        model_name = data["metadata"]["model_info"][list(data["metadata"]["model_info"].keys())[0]]["name"]
        paragraph_data = data["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"]

        # Initialize current paragraph information
        curr_speaker = None
        curr_timestamp = None
        curr_transcript = ""

        for para in paragraph_data:
            speaker_id = str(para['speaker'])  # Keep speaker_id as string
            speaker = f'Speaker {speaker_id}'

            start_timestamp = convert_seconds_to_timestamp(para['start'])

            # Extract sentences from paragraph and join them
            sentences = para.get('sentences', [])
            transcript = ' '.join(sentence.get('text', '') for sentence in sentences)

            if combine_segs and speaker == curr_speaker:
                # If combine_segs is True and the speaker is the same as the previous paragraph, continue accumulating the transcript
                curr_transcript += " " + transcript
            else:
                # If it's a new speaker, write the accumulated transcript to lines, then reset curr_speaker, curr_timestamp, and curr_transcript
                if curr_transcript:
                    # Add speaker, timestamp and transcript to lines
                    lines.extend([curr_speaker + '  ' + curr_timestamp, curr_transcript, ''])
                curr_speaker = speaker
                curr_timestamp = start_timestamp
                curr_transcript = transcript

        # Write the last paragraph to lines
        if curr_transcript:
            lines.extend([curr_speaker + '  ' + curr_timestamp, curr_transcript, ''])

    content = "## content\n\n### transcript\n\n" + "\n".join(lines)
    print(f"DEBUG - content: {content}")
    metadata = create_initial_metadata()
    date_today = datetime.now().strftime("%m-%d-%Y") # Assign today's date in format MM-DD-YYY
    metadata = set_metadata_field(metadata, 'last updated', date_today + ' Created')  
    metadata = set_metadata_field(metadata, 'link', link)
    metadata = set_metadata_field(metadata, 'transcript source', 'deepgram '+model_name)
    
    write_metadata_and_content(md_file_path, metadata, content, overwrite='yes')
    convert_nums_to_words(md_file_path)
    add_timestamp_links(md_file_path)
    return md_file_path
def process_deepgram_transcription(title, link, model, audio_inbox_path="data/audio_inbox"):  # unittests 1 TEMP SKIPPED
    """
    Processes a Deepgram transcription from a YouTube video link by downloading the audio, transcribing it, and creating a markdown transcript.

    :param title: the title of the video used to name the downloaded audio file.
    :param link: the YouTube link to the video to be transcribed.
    :param model: the Deepgram model used for transcription.
    :param audio_inbox_path: the directory path where the audio file will be downloaded.
    :return: the path to the created markdown file or None if transcription fails.
    """
    # Download the audio file
    audio_file_path = download_mp3_from_youtube(link, f"{audio_inbox_path}/{title}")
    
    # Transcribe the downloaded audio file
    json_file_path = transcribe_deepgram(audio_file_path, model)
    if json_file_path is None:
        print("transcription failed or the file type is incorrect.")
        return None
    print(json_file_path)

    # Add the YouTube link to the transcription JSON
    add_link_to_json(json_file_path, link)

    # Create a markdown transcript from the JSON file and process it
    md_file_path = create_transcript_md_from_json(json_file_path)
    
    # Assign speaker names to the markdown transcript
    assign_speaker_names(md_file_path)
    
    return md_file_path
def process_deepgram_transcription_from_audio_file(audio_file_path, link, model):  # unittests 1 TEMP SKIPPED
    """ 
    Transcribes an audio file using the Deepgram service, adds the YouTube link to the transcription, creates a markdown transcript, and assigns speaker names.

    :param audio_file_path: string of the path to the audio file to be transcribed.
    :param link: string of the youtube link to be added to the transcription json.
    :param model: string of the deepgram model to be used for transcription.
    :return: string of the path to the markdown file with the completed transcription or None if transcription fails.
    """
    # Transcribe the downloaded audio file
    json_file_path = transcribe_deepgram(audio_file_path, model)
    if json_file_path is None:
        raise ValueError("Transcription failed or the file type is incorrect.")
    # Add the YouTube link to the transcription JSON
    add_link_to_json(json_file_path, link)

    # Create a markdown transcript from the JSON file and process it
    md_file_path = create_transcript_md_from_json(json_file_path)

    # Assign speaker names to the markdown transcript
    assign_speaker_names(md_file_path)

    return md_file_path
def process_multiple_videos(videos_to_process, model='nova-2-general', bool_youtube=True):  # unittests 1 MOCK
    """
    Processes multiple videos by transcribing them and creating YouTube markdown files if bool_youtube is True.

    :param videos_to_process: list of tuples containing the title and link of each video to be processed.
    :param model: string of the deepgram model to be used for transcription. Defaults to 'enhmeet' (deepgram enhanced-meeting) model.
    :param bool_youtube: boolean indicating whether to create YouTube markdown files. Defaults to True.
    :return: None
    """
    for title, link in videos_to_process:
        try:                                             
            cur_md = process_deepgram_transcription(title, link, model)
            if bool_youtube:
                create_youtube_md_from_file_link(cur_md)
        except ValueError as e:
            print(f"Error processing video {title}: {e}")


