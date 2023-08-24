import numpy as np
from PIL import Image, ImageColor
from ui import BACKGROUND_COLOR, FONT_COLOR


class ImageConverter:
    def __init__(self):
        self.image = None
        self.background = (255, 255, 255)
        self.foreground = (0, 0, 0)

    def set_background_color(self, color):
        self.background = ImageColor.getrgb(color)

    def set_foreground_color(self, color):
        self.foreground = ImageColor.getrgb(color)

    def convert(self, original_file, target_file):
        self.open_image(original_file)
        img_array = np.array(self.image)
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                if np.all(img_array[i, j, :] > [230, 230, 230]):
                    img_array[i, j, :] = self.background
                elif np.all(img_array[i, j, :] < [60, 60, 60]):
                    img_array[i, j, :] = self.foreground
        self.save(img_array, target_file)

    def open_image(self, file_path: str):
        try:
            self.image = Image.open(file_path)
        except FileNotFoundError as e:
            print(f'File: {file_path} does not exist')
            print(e)

    @staticmethod
    def save(image_array, file_path):
        new_image = Image.fromarray(image_array)
        new_image.save(file_path)


converter = ImageConverter()
converter.set_background_color(BACKGROUND_COLOR)
converter.set_foreground_color(FONT_COLOR)
converter.convert('images/original/cross.jpg', 'images/converted/cross.png')
converter.convert('images/original/grid.jpg', 'images/converted/grid.png')
converter.convert('images/original/o.jpg', 'images/converted/o.png')
