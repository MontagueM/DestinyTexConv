import texlib
import pkg_db
import gf
import settings
import os

if __name__ == '__main__':
    ##########################
    #   DO NOT TOUCH BELOW   #
    ##########################
    pkg_db.start_db_connection('3_1_0_1.db')
    afi = {x[0]: dict(zip(['Reference', 'FileType'], x[1:])) for x in
                     pkg_db.get_entries_from_table('Everything', 'FileName, Reference, FileType')}
    other_types = ['tga', 'png', 'jpg', 'bmp']

    # Input control
    if 'dds' == settings.texture_format.lower():
        file_type = 'dds'
    elif settings.texture_format.lower() in other_types:
        file_type = settings.texture_format.lower()
    else:
        raise Exception('Unknown file format given.')

    if not os.path.exists(settings.header_list_file):
        raise FileNotFoundError('Given header list file is not valid.')
    with open(settings.header_list_file) as f:
        headers = [i.strip() for i in f.readlines()]

    # Getting texture
    for header_file_name in headers:
        if len(header_file_name) != 9 or '-' not in header_file_name:
            raise Exception('Header file name incorrect')
        if header_file_name not in afi.keys():
            raise KeyError('Header file not a texture header')
    
        uid = gf.get_hash_from_file(header_file_name)
        texture = texlib.TextureHeader(uid=uid, afi=afi)
        if file_type == 'dds':
            texlib.tex2dds(texture, f'{settings.output_directory}/{texture.name}.dds')
        else:
            texlib.tex2other(texture, f'{settings.output_directory}/{texture.name}.dds', file_type)
