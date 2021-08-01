import os
import sys
from posixpath import join
from typing import List, Optional
import argparse

# Constants
JPEG_EXT = "JPG"
METADATA_EXT = "xmp"
RAW_EXT = "raf"


class ImageData:
    def __init__(self, jpeg_url: str, metadata_url: str, raw_url: Optional[str] = None):
        self.raw_url = raw_url
        self.jpeg_url = jpeg_url
        self.metadata_url = metadata_url

    def __str__(self) -> str:
        return self.jpeg_url

    def __repr__(self) -> str:
        return self.__str__()

    def sync(self, should_remove_original: bool = False):
        self.sync_jpeg(should_remove_original)
        self.sync_raw(should_remove_original)

    def sync_media(self, media_url: str, metadata_url: str, should_remove_original: bool = False):
        sync_comand = f"exiftool -q \"-{METADATA_EXT}<={metadata_url}\" {media_url}"
        os.system(sync_comand)

        date_sync_command = f"exiftool -q \"-FileCreateDate<DateCreated\" \"-FileModifyDate<DateCreated\"  {media_url}"
        os.system(date_sync_command)

        if should_remove_original:
            remove_command = f"rm -rf {media_url}_original"
            os.system(remove_command)

    def sync_jpeg(self, should_remove_original: bool = False):
        self.sync_media(self.jpeg_url, self.metadata_url,
                        should_remove_original)

    def sync_raw(self, should_remove_original: bool = False):
        if self.raw_url is None:
            return

        self.sync_media(self.raw_url, self.metadata_url,
                        should_remove_original)


class Program:
    def __init__(self, root: str):
        self.root = root

    def confirmation(self, question: str) -> bool:
        ans = input(f"{question} (y/n): ")
        if ans == "y":
            return True
        elif ans == "n":
            return False
        else:
            print(f"> Invalid input! Please try agian.")
            return self.confirmation(question)

    def get_image_data_list(self) -> List[ImageData]:
        dir = self.root
        list: List[ImageData] = []

        for item in os.listdir(dir):
            file_anatomies: List[str] = item.split(".")
            if len(file_anatomies) < 2:
                continue

            item_name = file_anatomies[0]
            item_extension = file_anatomies[1]
            jpeg_url = join(dir, item)

            # make sure the jpeg file exist with the extension
            if (os.path.isfile(jpeg_url) != True) or (item_extension != JPEG_EXT):
                continue

            # make sure the metadata exists with the same file name
            metadata_url = join(dir, f"{item_name}.{METADATA_EXT}")
            if (os.path.isfile(metadata_url) != True):
                continue

            image_data = ImageData(jpeg_url, metadata_url)

            # assign the raw url to the image data if exists
            raw_url = join(dir, f"{item_name}.{RAW_EXT}")
            if os.path.isfile(raw_url):
                image_data.raw_url = raw_url

            # append the image data
            list.append(image_data)

        return list

    def sync_images(self, should_remove_originals: bool = False):
        dir = self.root
        print(f"> Getting images to sync at {dir} ...")
        list = self.get_image_data_list()
        success_count = 0
        print(f"> Found {len(list)} images to sync ...")
        if len(list) == 0:
            return

        confirmed = self.confirmation(
            f"> Are you sure to sync {len(list)} images?")

        if not confirmed:
            print("> Images sync cancelled!")
            return

        for item in list:
            item.sync(should_remove_originals)
            success_count += 1
            progress = float(success_count)/float(len(list)) * 100.0
            formatted_progress = "{:.2f}".format(progress)

            if success_count == len(list):
                print(
                    f"> Syncing images: {formatted_progress}% ({success_count}/{len(list)}) images sync. Done!")
            else:
                print(
                    f"> Syncing images: {formatted_progress}% ({success_count}/{len(list)}) images sync", end="\r")

        print(f"> {success_count}/{len(list)} images successfully sync!")

    def clean_metadata_files(self):
        dir = self.root
        print(f"> Getting image's metadata files to clean at {dir} ...")
        list = self.get_image_data_list()
        success_count = 0
        print(f"> Found {len(list)} images to clean ...")

        if len(list) == 0:
            return

        confirmed = self.confirmation(
            f"> Are you sure to clean {len(list)} image metadata files?")

        if not confirmed:
            print("> Images metadata files cleaning cancelled!")

        for item in list:
            metadata_url = item.metadata_url

            if metadata_url is not None:
                if os.path.isfile(metadata_url):
                    clean_command = f"rm -rf {metadata_url}"
                    os.system(clean_command)

            success_count += 1
            progress = float(success_count)/float(len(list)) * 100.0
            formatted_progress = "{:.2f}".format(progress)

            if success_count == len(list):
                print(
                    f"> Cleaning image's metadata files: {formatted_progress}% ({success_count}/{len(list)}) file cleaned. Done!")
            else:
                print(
                    f"> Cleaning image's metadata files: {formatted_progress}% ({success_count}/{len(list)}) file cleaned", end="\r")

    def clean_originals(self):
        dir = self.root
        print(f"> Getting images to clean at {dir} ...")
        list = self.get_image_data_list()
        success_count = 0
        print(f"> Found {len(list)} images to clean ...")

        if len(list) == 0:
            return

        confirmed = self.confirmation(
            f"> Are you sure to clean {len(list)} image original files?")

        if not confirmed:
            print("> Images original files cleaning cancelled!")

        for item in list:
            original_jpeg_url = item.jpeg_url + "_original"
            original_raw_url = item.raw_url + "_original"

            if os.path.isfile(original_jpeg_url):
                jpeg_clean_command = f"rm -rf {original_jpeg_url}"
                os.system(jpeg_clean_command)

            if os.path.isfile(original_raw_url):
                raw_clean_command = f"rm -rf {original_raw_url}"
                os.system(raw_clean_command)

            success_count += 1
            progress = float(success_count)/float(len(list)) * 100.0
            formatted_progress = "{:.2f}".format(progress)

            if success_count == len(list):
                print(
                    f"> Cleaning original images: {formatted_progress}% ({success_count}/{len(list)}) images cleaned. Done!")
            else:
                print(
                    f"> Cleaning original images: {formatted_progress}% ({success_count}/{len(list)}) images cleaned", end="\r")


def get_should_remove_originals() -> bool:
    ans = input("> Remove originals after new file created? (y/n): ")
    if ans == "y":
        return True
    elif ans == "n":
        return False
    else:
        print(f"> Invalid input! Please try agian.")
        return get_should_remove_originals()


def get_action() -> int:
    ans = input("> Menu: \n\t1. Sync images with its metadata.\n\t2. Remove \"_original\" files.\n\t3. Remove metadata files.\n> Please input action number: ")
    try:
        action = int(ans)
        if action < 1 or action > 3:
            print("> Invalid action! Please try again.")
            return get_action()
        else:
            return action
    except ValueError:
        print("> Invalid action! Please try again.")
        return get_action()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exif Sync Manaager.")

    parser.add_argument(
        "-p", "--path",
        dest="path",
        required=True,
        help="The root directory"
    )

    args = parser.parse_args()

    root = args.path
    program = Program(root=root)
    action = get_action()
    if action == 1:
        should_remove_originals = get_should_remove_originals()
        program.sync_images(should_remove_originals)
    elif action == 2:
        program.clean_originals()
    elif action == 3:
        program.clean_metadata_files()
