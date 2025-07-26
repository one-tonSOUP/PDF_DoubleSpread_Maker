import os
import sys
#from pdf2image import convert_from_path
import fitz
import matplotlib.image
import numpy as np
from PIL import Image

class DoubleSpread:
    pages = []
    path = os.getcwd()
    def __init__(self):
        self.pdfPath = input(f"Please provide the filename \t: ")
        print(f"Data received.\nUser provided \t\t: {self.pdfPath}")


    def pdf_to_img(self):
        doc = fitz.open(self.pdfPath)

        # Project folder setup
        project_dir = os.path.dirname(os.path.abspath(__file__))
        img_folder = os.path.join(project_dir, "pdf_pages_output")
        os.makedirs(img_folder, exist_ok=True)

        for i in range(len(doc)):
            page = doc.load_page(i)

            # Enhanced image quality
            zoom_x = 2.0
            zoom_y = 2.0
            mat = fitz.Matrix(zoom_x, zoom_y)
            pix = page.get_pixmap(matrix=mat, dpi=300)

            name = f"Page_{i}.jpg"
            save_path = os.path.join(img_folder, name)
            pix.save(save_path)
            self.pages.append(save_path)

            # Print log . .
            sys.stdout.write(f"\r[single_spread_log] Saved: spread_single_{i}.jpg")
            sys.stdout.flush()

            #print(f"[INFO] Saved {i} pages so far...")

    def get_names(self):
        return self.pages

    def generate_spread_pages(self):
        input_dir = "pdf_pages_output"
        output_dir = "output_spreads"
        os.makedirs(output_dir, exist_ok=True)

        A4_WIDTH, A4_HEIGHT = 3508, 2480  # A4 landscape at 300 DPI

        try:
            single_limit = int(input("\n\nPlease provide the initial number of pages that should be printed as single image spreads: "))
        except ValueError:
            print("[ERROR] Invalid input. Please enter a number.")
            return

        pages = sorted([
            os.path.join(input_dir, fname)
            for fname in os.listdir(input_dir)
            if fname.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])

        i = 0
        total_pages = len(pages)

        while i < total_pages:
            if i < single_limit:
                img = Image.open(pages[i]).convert("RGB")
                img_width, img_height = img.size

                # Create blank canvas with width = 2 * image width, height = image height
                canvas = Image.new("RGB", (img_width * 2, img_height), "white")

                # Create right-side blank image of same size as left image
                blank_right = Image.new("RGB", (img_width, img_height), "white")

                # Paste original image on the left, blank image on the right
                canvas.paste(img, (0, 0))
                canvas.paste(blank_right, (img_width, 0))

                output_path = os.path.join(output_dir, f"spread_single_{i}.jpg")
                canvas.save(output_path)
                # Print log . .
                sys.stdout.write(f"\r[double_spread_log] Saved: spread_double_{i}.jpg")
                sys.stdout.flush()
                i += 1

            else:
                if i + 1 < total_pages:
                    # Pair and merge two images side by side
                    img1 = Image.open(pages[i]).convert("RGB")
                    img2 = Image.open(pages[i+1]).convert("RGB")

                    img1_resized = img1.resize((A4_WIDTH // 2, A4_HEIGHT))
                    img2_resized = img2.resize((A4_WIDTH // 2, A4_HEIGHT))

                    canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
                    canvas.paste(img1_resized, (0, 0))
                    canvas.paste(img2_resized, (A4_WIDTH // 2, 0))
                    canvas.save(os.path.join(output_dir, f"spread_double_{i}_{i+1}.jpg"))
                    # Print log . .
                    sys.stdout.write(f"\r[double_spread_log] Saved: spread_double_{i}_{i+1}.jpg")
                    sys.stdout.flush()
                    i += 2
                else:
                    # Final leftover image
                    img = Image.open(pages[i]).convert("RGB")
                    img_width, img_height = img.size
                    canvas = Image.new("RGB", (img_width * 2, img_height), "white")
                    blank_right = Image.new("RGB", (img_width, img_height), "white")
                    canvas.paste(img, (0, 0))  # Left align without stretching
                    canvas.paste(blank_right, (img_width, 0))
                    canvas.save(os.path.join(output_dir, f"spread_single_last_{i}.jpg"))
                    # Print log . .
                    sys.stdout.write(f"\r[double_spread_log] Saved: spread_double_{i}_{i+1}.jpg")
                    sys.stdout.flush()
                    i += 1


    # 🧪 Example usage:
    # generate_spread_pages("input_pages", "output_spreads", single_limit=4)

    
    """def combine_images(self, image_1, image_2, names):
        image_1 = matplotlib.image.imread(names[0])
        image_2 = matplotlib.image.imread(names[1])

        row1 = np.concatenate((img1, img2), axis=1)
        row2 = np.concatenate((img3, img4), axis=1)
        new_image = np.concatenate((row1, row2))

        # or
        row1 = np.hstack((img1, img2))
        row2 = np.hstack((img3, img4))
        new_image = np.vstack((row1, row2))

        matplotlib.image.imsave('new.png', new_image)
        # START WORKING HERE . .
        return None"""
    
    def create_pdf(self):
        self.pdf_to_img()
        self.generate_spread_pages()
        print("\n\nAll steps completed..!")
        return None


def main():
    obj = DoubleSpread()
    obj.create_pdf()

if __name__ == "__main__":
    main()