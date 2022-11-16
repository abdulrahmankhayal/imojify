import emoji
from .emoji_dictionaries import *
from PIL import Image
import numpy as np
import os
dir = os.path.dirname(__file__)


class imojify:
    def __init__(self):
        self.uni_code_dirc = unicode_to_dirc
        self.name_dirc = name_to_dirc

    def get_img_path(self, emji):
        """
        return path to emoji image if exist else return empty image

        Parameters
        ----------
        emji : string ; typically an emoji unicode
        """
        if emoji.is_emoji(emji):
            try:
                path = self.uni_code_dirc[emji]
            except BaseException:

                try:
                    path = self.name_dirc[emoji.demojize(
                        emji).lower().replace('-', '_')[1:-1]]
                except BaseException:
                    path = './Images/Empty.png'
            return os.path.join(dir, path)
        else:
            list_im = []
            for emi in emoji.emoji_list(emji):
                list_im.append(self.get_img_path(emi['emoji']))
            if not list_im:
                return os.path.join(dir, './Images/Empty.png')
            imgs = [Image.open(i) for i in list_im]
            # pick the image which is the smallest, and resize the others to
            # match it (can be arbitrary image shape here)
            min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
            imgs_comb = np.hstack([i.resize(min_shape) for i in imgs])

            # save that beautiful picture
            imgs_comb = Image.fromarray(imgs_comb)
            path = os.path.join(dir, f'./Images/{emji}.PNG')
            imgs_comb.save(path)
            return path
