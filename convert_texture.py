import texlib
import pkg_db
import gf
import settings

if __name__ == '__main__':
    ##########################
    #   DO NOT TOUCH BELOW   #
    ##########################
    pkg_db.start_db_connection('3_1_0_1.db')
    afi = {x[0]: dict(zip(['Reference', 'FileType'], x[1:])) for x in
                     pkg_db.get_entries_from_table('Everything', 'FileName, Reference, FileType')}
    other_types = ['tga', 'png', 'jpg', 'bmp']

    # Input control
    if len(settings.header_file_name) != 9 and '-' not in settings.header_file_name:
        raise Exception('Header file name incorrect')
    if settings.header_file_name not in afi.keys():
        raise KeyError('Header file not a texture header')

    if 'dds' == settings.texture_format.lower():
        file_type = 'dds'
    elif settings.texture_format.lower() in other_types:
        file_type = settings.texture_format.lower()
    else:
        raise Exception('Unknown file format given.')

    with open(settings.header_list_name) as f:
        content = [i.strip() for i in f.readlines()]

    # Getting texture
    for header_file_name in content:
        uid = gf.get_hash_from_file(header_file_name)
        texture = texlib.TextureHeader(uid=uid, afi=afi)
        if file_type == 'dds':
            texlib.tex2dds(texture, f'{settings.output_directory}/{texture.name}.dds')
        else:
            texlib.tex2other(texture, f'{settings.output_directory}/{texture.name}.dds', file_type)
