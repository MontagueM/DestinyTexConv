# DestinyTexConv
A Destiny 2 texture converter. Takes an input texture header and converts into an image.

Supports formats DDS, PNG, JPG, BMP, TGA.

## Usage

Change the settings in settings.py to fit.

The unpacker directory should have all the game unpacked to .bin, since otherwise some files may not be found and the program will crash. An unpack of the game can be made using my DestinyUnpacker.

To run, execute convert_texture.py using an interpreter or console. Let me know of any problems either by placing an Issue or contacting me via discord Monteven#9258, the #datamining-discussion channel on RaidSecrets discord, or twitter @monteven.

## Other notes
This program is extremely WIP and has been released in this state so people can have a look and learn about the basics of datamining in the Destiny franchise.

I have some personal ideas of what could be improved, but if you have any other ideas or would like to implement some feel free to pull request or fork.

:black_square_button: Pull from packages instead of requiring a full unpack

:white_check_mark: Support other formats than DDS

:black_square_button: make the program easier to use (executable release/gui?)

:black_square_button: texture plates
