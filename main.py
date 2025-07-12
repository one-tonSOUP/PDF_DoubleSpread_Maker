import os
from pdf2image import convert_from_path
import matplotlib.image
import numpy as np

class DoubleSpread:
    pages = []
    path = os.getdir()
    def __init__(self):
        self.pdfPath = input(f"Please provide the filename \t: ")
        print(f"Data received.\nUser provided \t\t: {self.pdfPath}")

    def pdf_to_img(self, pdf):
        images = convert_from_path('example.pdf')       # WORK HERE . .
        os.mkdir(self.path + "data")
        os.chdir(self.path + "data")
        for i in range(len(images)):
            name = 'Page_'+ str(i) +'.jpg'
            images[i].save(name, 'JPEG')
            self.pages.append(name)
    
    def get_names(self):
        return self.pages
    
    def combine_images(self, image_1, image_2, names[]):
        # START WORKING HERE . .
        return None
    
    def create_pdf(self, data):
        return None


def main():
    obj = DoubleSpread()

if __name__ == "__main__":
    main()