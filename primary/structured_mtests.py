from fileops import *
from primary.structured import *

if True:
    pass
if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/1900-01-01_Test file for do fileop_prepqa.md"

def mtest_count_blocks():
    pass
if __name__ == "__main__":        
    cur_file_path = "data/floodlamp/reg/fda-townhalls/dev/2020-12-09_Virtual Town Hall 36_qa-incremental_7-21_6_25 blocks 1 review.md"
    print(count_blocks(cur_file_path))

def mtest_create_topics_matrix():
    pass
#if __name__ == "__main__":
    cur_folder_paths = ["data/f_c7_done_early", "data/f_c8_qafixed_talks", "data/f_c6_done_after_dq", "data/f_c5_done_after_dq" ]   
    create_topics_matrix(cur_folder_paths)
