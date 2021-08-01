# ExifSyncManager
Sync image's metadata files using exiftool.

## Prerequisite
This script using exiftool to update media's metadata files. Please install [exiftool](https://exiftool.org) on your machine before get started.

## Get Started
In the project directory, run the script using command below:
```
python3 main.py YOUR_DIRECTORY_PATH
```
By default, this script accept media with extension .JPG, metadata with .xmp extension, and RAW file with .raf extension. For other extension please modify constans defined on the top of main.py. Please check [exiftool](https://exiftool.org) for supported format.

## Features
### Images sync
This feature will sync metadata file with its media file. The metadata and its media file should be named identical (e.g. DSCF00001.JPG and DSCF00001.xmp)

### Remove the original files
The script will produce new file after sync and rename original file with suffix (e.g. DSCF00001.JPG_original). This feature will remove all originals.

### Remove the metada files
This feature will remove all metadata.
