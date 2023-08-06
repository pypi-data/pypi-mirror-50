# -*- coding: utf-8 -*-
"""rhinopics class.

This module contains functions to rename pictures.
"""
from datetime import datetime
import os
import pathlib
from typing import Sequence, Union
import exifread


class Rhinopics:
    """
    Rhinopics class.

    Class to handle the renaming of pictures.
    """

    TAGS_DATE = {'EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'EXIF DateTime'}
    IMG_EXTS = {'.jpg', '.JPG', '.JPEG', '.png', '.PNG'}

    def __init__(self, directory: pathlib.PosixPath, keyword: str, backup: bool,
                 tags: Union[Sequence, None] = None,
                 img_exts: Union[Sequence, None] = None):
        self.directory = directory
        self.keyword = keyword
        self.backup = backup
        self.tags = tags or Rhinopics.TAGS_DATE
        self.img_exts = img_exts or Rhinopics.IMG_EXTS
        self.counter = 1

    def rename(self):
        """
        Rename the pictures of the directory.

        Pictures are renamed with the given keyword and the date of the picture.
        """
        paths = self.directory.glob('*')
        img_paths = [p for p in paths if p.suffix in self.img_exts]
        img_paths_sorted = sorted(img_paths, key=os.path.getmtime)
        nb_digits = len(str(len(img_paths_sorted)))

        for path in img_paths_sorted:
            date = self.get_date(path)
            new_name = (f'{self.keyword}_{date}_{str(self.counter).rjust(nb_digits, "0")}'
                        f'{path.suffix}')
            new_path = path.with_name(new_name)
            if not new_path.exists():
                if self.backup:
                    with new_path.open(mode='xb') as fid:
                        fid.write(path.read_bytes())
                    print(f'Copying {path} to {new_path}.')
                else:
                    path.replace(new_path)
                    print(f'Renaming {path} to {new_path}.')
                self.counter += 1
            else:
                print(f'Path {new_path} already exists.')

        print(f'Done. {self.counter-1} pictures were renamed!')

    def get_date(self, path: pathlib.PosixPath) -> str:
        """
        Retrieve the date of a picture.

        Parameters
        ----------
        path: pathlib.PosixPath
            Path containing the pictures to rename.

        Returns
        -------
        str
            Date as a string in the following format: %Y%m%d.
            If date is not found, return 'NoDateFound'.
        """
        with path.open(mode='rb') as fid:
            tags_read = exifread.process_file(fid)

            for tag in self.tags:
                if tag in tags_read.keys():
                    date = datetime.strptime(str(tags_read[tag]),
                                             '%Y:%m:%d %H:%M:%S').strftime('%Y%m%d')
                    return date

        return 'NoDateFound'
