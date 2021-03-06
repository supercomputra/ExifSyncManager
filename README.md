# ExifSyncManager

Script for syncing image's metadata files using exiftool. This script will embed any information on your image's metadata file to the original image's file. The creation date and modification date of the file will be set as same as the image taken date based on the information specified in the metadata.

## Prerequisite

This script using exiftool to update media's metadata files. Please install [exiftool](https://exiftool.org) on your machine before get started.

## Get Started

In the project directory, run the script using command below:

```
python3 main.py --path YOUR_DIRECTORY_PATH
```

**By default, this script accept media with extension .JPG, metadata with .xmp extension, and RAW file with .raf extension. For other extension options please modify constans defined on the top of main.py. Please check [exiftool](https://exiftool.org) for the supported format.**

```
optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  The root directory
```

<img width="780" alt="Screen Shot 2021-08-02 at 01 21 50" src="https://user-images.githubusercontent.com/17508929/127781405-001b8ef5-6d33-4b0e-90cd-2bcc7ca44f01.png">


## Features

### Images sync

This feature will sync metadata file with its media file. The metadata and its media file should be named identical (e.g. DSCF00001.JPG and DSCF00001.xmp)

### Remove the original files

The script will produce new file after sync and rename original file with suffix (e.g. DSCF00001.JPG_original). This feature will remove all originals.

### Remove the metadata files

This feature will remove all metadata.
