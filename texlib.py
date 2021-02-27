from dataclasses import dataclass, fields, field
import numpy as np
import gf
import binascii
from typing import List
import settings
import os


class File:
    def __init__(self, uid):
        self.uid = uid
        self.name = gf.get_file_from_hash(self.uid)
        self.fb = None
        self.pkg_name = None

    def get_file_from_uid(self):
        self.name = gf.get_file_from_hash(self.uid)
        return self.pkg_name

    def get_uid_from_file(self):
        self.uid = gf.get_hash_from_file(self.name)
        return self.pkg_name

    def get_pkg_name(self):
        self.pkg_name = gf.get_pkg_name(self.name)
        return self.pkg_name

    def get_fb(self):
        if not self.pkg_name:
            self.get_pkg_name()
        if not self.pkg_name:
            raise FileNotFoundError(f'Missing package for file {self.name}. Please extract the package with that ID, or ideally extract the full game.')
        self.fb = open(f'{settings.unpacked_directory}/{self.pkg_name}/{self.name}.bin', 'rb').read()
        return self.fb


class Header(File):
    def __init__(self, uid, afi):
        super().__init__(uid)
        self.ref_file = File(afi[self.name]['Reference'])

    def get_header(self):
        raise Exception(f'Header not defined for file {self.uid}.')


class TextureHeader(Header):
    def __init__(self, uid, afi):
        super(TextureHeader, self).__init__(uid, afi)
        self.get_fb()
        self.data_file = File(uid=afi[gf.get_file_from_hash(uid)]['Reference'])
        self.data_file.get_fb()
        self.texture_format = None
        self.width = None
        self.height = None
        self.array_size = None
        self.large_hash = None
        self.get_header()

    def get_header(self):
        self.texture_format = gf.get_uint16(self.fb, 4)
        self.width = gf.get_uint16(self.fb, 0x22)
        self.height = gf.get_uint16(self.fb, 0x24)
        self.array_size = gf.get_uint16(self.fb, 0x28)
        self.large_hash = self.fb[0x3C:0x3C+4].hex()


@dataclass
class ImageHeader:
    TargetSize: np.uint32 = np.uint32(0)  # 0
    TextureFormat: np.uint32 = np.uint32(0)  # 4
    Field8: np.uint32 = np.uint32(0)  # 8
    FieldC:  np.uint32 = np.uint32(0)  # C
    Field10: np.uint32 = np.uint32(0)  # 10
    Field14: np.uint32 = np.uint32(0)  # 14
    Field18: np.uint32 = np.uint32(0)  # 18
    Field1C: np.uint32 = np.uint32(0)  # 1C
    Cafe: np.uint16 = np.uint16(0)  # 20  0xCAFE
    Width: np.uint16 = np.uint16(0)  # 22
    Height: np.uint16 = np.uint16(0)  # 24
    Field26: np.uint16 = np.uint16(0)
    TA: np.uint16 = np.uint16(0)  # 28
    Field2A: np.uint16 = np.uint16(0)
    Field2C: np.uint32 = np.uint32(0)
    Field30: np.uint32 = np.uint32(0)
    Field34: np.uint32 = np.uint32(0)
    Field38: np.uint32 = np.uint32(0)
    LargeTextureHash: np.uint32 = np.uint32(0)  # 3C


@dataclass
class DX10Header:
    MagicNumber: np.uint32 = np.uint32(0)
    dwSize: np.uint32 = np.uint32(0)
    dwFlags: np.uint32 = np.uint32(0)
    dwHeight: np.uint32 = np.uint32(0)
    dwWidth: np.uint32 = np.uint32(0)
    dwPitchOrLinearSize: np.uint32 = np.uint32(0)
    dwDepth: np.uint32 = np.uint32(0)
    dwMipMapCount: np.uint32 = np.uint32(0)
    dwReserved1: List[np.uint32] = field(default_factory=list)  # size 11, [11]
    dwPFSize: np.uint32 = np.uint32(0)
    dwPFFlags: np.uint32 = np.uint32(0)
    dwPFFourCC: np.uint32 = np.uint32(0)
    dwPFRGBBitCount: np.uint32 = np.uint32(0)
    dwPFRBitMask: np.uint32 = np.uint32(0)
    dwPFGBitMask: np.uint32 = np.uint32(0)
    dwPFBBitMask: np.uint32 = np.uint32(0)
    dwPFABitMask: np.uint32 = np.uint32(0)
    dwCaps: np.uint32 = np.uint32(0)
    dwCaps2: np.uint32 = np.uint32(0)
    dwCaps3: np.uint32 = np.uint32(0)
    dwCaps4: np.uint32 = np.uint32(0)
    dwReserved2: np.uint32 = np.uint32(0)
    dxgiFormat: np.uint32 = np.uint32(0)
    resourceDimension: np.uint32 = np.uint32(0)
    miscFlag: np.uint32 = np.uint32(0)
    arraySize: np.uint32 = np.uint32(0)
    miscFlags2: np.uint32 = np.uint32(0)


@dataclass
class DDSHeader:
    MagicNumber: np.uint32 = np.uint32(0)
    dwSize: np.uint32 = np.uint32(0)
    dwFlags: np.uint32 = np.uint32(0)
    dwHeight: np.uint32 = np.uint32(0)
    dwWidth: np.uint32 = np.uint32(0)
    dwPitchOrLinearSize: np.uint32 = np.uint32(0)
    dwDepth: np.uint32 = np.uint32(0)
    dwMipMapCount: np.uint32 = np.uint32(0)
    dwReserved1: List[np.uint32] = field(default_factory=list)  # size 11, [11]
    dwPFSize: np.uint32 = np.uint32(0)
    dwPFFlags: np.uint32 = np.uint32(0)
    dwPFFourCC: np.uint32 = np.uint32(0)
    dwPFRGBBitCount: np.uint32 = np.uint32(0)
    dwPFRBitMask: np.uint32 = np.uint32(0)
    dwPFGBitMask: np.uint32 = np.uint32(0)
    dwPFBBitMask: np.uint32 = np.uint32(0)
    dwPFABitMask: np.uint32 = np.uint32(0)
    dwCaps: np.uint32 = np.uint32(0)
    dwCaps2: np.uint32 = np.uint32(0)
    dwCaps3: np.uint32 = np.uint32(0)
    dwCaps4: np.uint32 = np.uint32(0)
    dwReserved2: np.uint32 = np.uint32(0)


def get_header(file_hex):
    img_header = ImageHeader()
    for f in fields(img_header):
        if f.type == np.uint32:
            flipped = "".join(gf.get_flipped_hex(file_hex, 8))
            value = np.uint32(int(flipped, 16))
            setattr(img_header, f.name, value)
            file_hex = file_hex[8:]
        elif f.type == np.uint16:
            flipped = "".join(gf.get_flipped_hex(file_hex, 4))
            value = np.uint16(int(flipped, 16))
            setattr(img_header, f.name, value)
            file_hex = file_hex[4:]
    return img_header


def tex2dds(tex, full_save_path):
    """
    DDS will only be used for maps so we don't need to return an image object that can be manipulated
    """
    if tex.large_hash != 'ffffffff':
        tex.data_file = File(uid=tex.large_hash)
        tex.data_file.get_fb()
    write_texture(tex, full_save_path)


with open('dxgi.format') as f:
    DXGI_FORMAT = f.readlines()


def write_texture(tex, full_save_path):
    form = DXGI_FORMAT[tex.texture_format]
    if '_BC' in form:
        dds_header = DX10Header()  # 0x0
    else:
        dds_header = DDSHeader()  # 0x0

    dds_header.MagicNumber = int('20534444', 16)  # 0x4
    dds_header.dwSize = 124  # 0x8
    dds_header.dwFlags = (0x1 + 0x2 + 0x4 + 0x1000) + 0x8
    dds_header.dwHeight = tex.height  # 0xC
    dds_header.dwWidth = tex.width  # 0x10
    dds_header.dwDepth = 0
    dds_header.dwMipMapCount = 0
    dds_header.dwReserved1 = [0]*11
    dds_header.dwPFSize = 32
    dds_header.dwPFRGBBitCount = 0
    dds_header.dwPFRGBBitCount = 32
    dds_header.dwPFRBitMask = 0xFF  # RGBA so FF first, but this is endian flipped
    dds_header.dwPFGBitMask = 0xFF00
    dds_header.dwPFBBitMask = 0xFF0000
    dds_header.dwPFABitMask = 0xFF000000
    dds_header.dwCaps = 0x1000
    dds_header.dwCaps2 = 0
    dds_header.dwCaps3 = 0
    dds_header.dwCaps4 = 0
    dds_header.dwReserved2 = 0
    if '_BC' in form:
        dds_header.dwPFFlags = 0x1 + 0x4  # contains alpha data + contains compressed RGB data
        dds_header.dwPFFourCC = int.from_bytes(b'\x44\x58\x31\x30', byteorder='little')
        dds_header.dxgiFormat = tex.texture_format
        dds_header.resourceDimension = 3  # DDS_DIMENSION_TEXTURE2D
        if tex.array_size % 6 == 0:
            # Compressed cubemap
            dds_header.miscFlag = 4
            dds_header.arraySize = int(tex.array_size / 6)
        else:
            # Compressed BCn
            dds_header.miscFlag = 0
            dds_header.arraySize = 1
    else:
        # Uncompressed
        dds_header.dwPFFlags = 0x1 + 0x40  # contains alpha data + contains uncompressed RGB data
        dds_header.dwPFFourCC = 0
        dds_header.miscFlag = 0
        dds_header.arraySize = 1
        dds_header.miscFlags2 = 0x1

    write_file(dds_header, tex, full_save_path)


def write_file(header, tex, full_save_path):
    with open(full_save_path, 'wb') as b:
        for f in fields(header):
            if f.type == np.uint32:
                flipped = "".join(gf.get_flipped_hex(gf.fill_hex_with_zeros(hex(np.uint32(getattr(header, f.name)))[2:], 8), 8))
            elif f.type == List[np.uint32]:
                flipped = ''
                for val in getattr(header, f.name):
                    flipped += "".join(
                        gf.get_flipped_hex(gf.fill_hex_with_zeros(hex(np.uint32(val))[2:], 8), 8))
            else:
                print(f'ERROR {f.type}')
                return
            b.write(binascii.unhexlify(flipped))
        b.write(tex.data_file.fb)


def tex2other(tex, full_save_path, other):
    tex2dds(tex, full_save_path)
    os.system(f'texconv.exe "{full_save_path}" -y -ft {other} -f {DXGI_FORMAT[tex.texture_format][12:]}')
    os.remove(full_save_path)