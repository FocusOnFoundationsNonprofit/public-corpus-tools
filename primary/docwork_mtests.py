from fileops import *
from docwork import *

if True:
    pass
if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/1900-01-01_Test file for do fileop_prepqa.md"

### COMMON DOCWORK
def mtest_validate_transcript():
    pass
#if __name__ == "__main__":
    cur_file_path = "tests/test_manual_files/docwork_tests/town_hall_tests/2020-10-14_Virtual Town Hall 30_cleaned.md"
    #print(validate_transcript(cur_file_path, verbose=True))
    print(apply_to_folder(validate_transcript, 'tests/test_manual_files/docwork_tests/town_hall_tests/', verbose=True))
def mtest_extract_transcript_data():
    pass
#if __name__ == "__main__":
    cur_file_path = "tests/test_manual_files/misc/3099-01-01_Test file with headings.md"
    print(extract_transcript_data(cur_file_path)) 
def mtest_create_speaker_triples(file_path):
    pass
#if __name__ == "__main__":        
    #cur_file_path = "data/floodlamp_fda/townhalls/f4_md_cleaned/2022-06-15_Virtual Town Hall 87_cleaned.md"
    cur_file_path = "data/pv/2024_meetings/epc/2024-04-04_PV-EPC_pub.md"
    print(create_speaker_triples(cur_file_path))
def mtest_extract_proper_names():
    pass
#if __name__ == "__main__":        
    print(extract_proper_names("Alice and Bob went to New York. They met with Charlie and discussed."))
def mtest_create_proper_names_triples(file_path):
    pass
#if __name__ == "__main__":        
    #cur_file_path = "data/floodlamp_fda/townhalls/f4_md_cleaned/2022-06-15_Virtual Town Hall 87_cleaned.md"
    cur_file_path = "data/pv/meetings_epc/2024-03-07_PV-EPC_spfixBA.md"
    custom_proper_names_files = ['data/pv/cspell_dictionary_pv.txt','data/pv/compound_proper_names.txt']
    #print(create_proper_names_triples(cur_file_path, custom_proper_names_files, True))
    print_proper_names(cur_file_path, custom_proper_names_files, True, True) 
def mtest_create_speaker_matrix():
    pass
#if __name__ == "__main__":        
    #create_speaker_matrix('data/floodlamp_fda/townhalls/f4_md_cleaned_manualedits','_cleaned', 'matrix_names_fdatownhalls.csv')
    create_speaker_matrix('data/pv/2024_meetings/epc/f2_speaker_fix_done','_spfixWIP', 'matrix_names.csv')

### FDA TOWNHALLS
def mtest_clean_fda_townhalls():
    pass
#if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/docwork_tests/town_hall_tests/clean_tests/2020-10-14_Virtual Town Hall 30.md"
    #cur_file_path = "data/floodlamp_fda/townhalls/f3_md_metadata/2022-06-15_Virtual Town Hall 87.md"
    clean_fda_townhall(cur_file_path)
def mtest_run_clean_on_townhalls():
    pass
#if __name__ == "__main__": 
    source_folder = "data/floodlamp_fda/townhalls/f3_md_metadata"
    destination_folder = "data/floodlamp_fda/townhalls/f4_md_cleaned"
    run_clean_on_townhalls(source_folder, destination_folder)
