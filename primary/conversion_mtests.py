from fileops import *
from conversion import *

if True:
    pass
if __name__ == "__main__":        
    cur_file_path = "tests/test_manual_files/1900-01-01_Test file for do fileop_prepqa.md"


### LLAMAINDEX
# WIP - NOT WORKING YET see py file
def mtest_convert_llamaindex_gdocs_to_md(gdoc_id_list):
    pass
#if __name__ == "__main__": 
    cur_gdoc_id_list = ['19yTV3UUkOQrfbqOPcL5hhBw9eJyc_5ra5Uz_tKQcs24']
    convert_llamaindex_gdocs_to_md(cur_gdoc_id_list)


### PANDOC
def mtest_convert_file_to_md_pandoc():
    pass
#if __name__ == "__main__": 
    #cur_file_path = 'tests/test_manual_files/file_conversion/2021-05-18_Instructions for Use - FloodLAMP QuickColor COVID-19 Test v1.1.docx'
    cur_file_path = 'data/floodlamp_fda/subs/2021-05-18_Pre-EUA Sub - FloodLAMP Proposed Pooling and Asymptomatic Screening Study.docx'
    print(convert_file_to_md_pandoc(cur_file_path))

