##########################
#   CHANGE VALUES HERE   #
##########################

"""
unpacked_directory : this must be the directory where the packages are unpacked to. The folder should include the pkg
                     folder names such as sr_sandbox_0105/ or investment_globals_client_0173/, not any .bins

output_directory : the folder where the images will all go. They will not be separated per pkg, just put there

header_file_name : the name of the texture header. names can be obtained by reading the database file provided with an
                   SQLite DB reader such as "DB Browser (SQLite)"; my code in pkg_db.py; or custom databases.
                   the name must be in the format 'ABCD-1234' where string length == 9 and there's a "-" in the string
                   otherwise it will fial.

texture_format : supports dds, png, jpg, tga, bmp
"""

unpacked_directory = 'C:/UnpackDirectory/Right/Here/Not/Bins/'
output_directory = 'C:/MyOutput/Folder/'
header_list_name = 'headers.txt'
texture_format = 'DDS'
