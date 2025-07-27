import os
import sys
import fitz
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
        project_dir = os.path.dirname(os.path.abspath(__file__))
        img_folder = os.path.join(project_dir, "pdf_pages_output")
        os.makedirs(img_folder, exist_ok=True)

        for i in range(len(doc)):
            page = doc.load_page(i)
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

    def get_names(self):
        return self.pages

    def generate_spread_pages(self):
        input_dir = "pdf_pages_output"
        output_dir = "output_spreads"
        os.makedirs(output_dir, exist_ok=True)

        A4_WIDTH, A4_HEIGHT = 3508, 2480

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
        spread_counter = 0

        while i < total_pages:
            if i < single_limit:
                img = Image.open(pages[i]).convert("RGB")
                img_width, img_height = img.size
                canvas = Image.new("RGB", (img_width * 2, img_height), "white")
                blank_right = Image.new("RGB", (img_width, img_height), "white")
                canvas.paste(img, (0, 0))
                canvas.paste(blank_right, (img_width, 0))

                output_path = os.path.join(output_dir, f"spread_{spread_counter:03}.jpg")
                canvas.save(output_path)
                sys.stdout.write(f"\r[double_spread_log] Saved: spread_{spread_counter:03}.jpg")
                sys.stdout.flush()
                spread_counter += 1
                i += 1

            else:
                if i + 1 < total_pages:
                    img1 = Image.open(pages[i]).convert("RGB")
                    img2 = Image.open(pages[i + 1]).convert("RGB")

                    img1_resized = img1.resize((A4_WIDTH // 2, A4_HEIGHT))
                    img2_resized = img2.resize((A4_WIDTH // 2, A4_HEIGHT))
                    canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
                    canvas.paste(img1_resized, (0, 0))
                    canvas.paste(img2_resized, (A4_WIDTH // 2, 0))

                    output_path = os.path.join(output_dir, f"spread_{spread_counter:03}.jpg")
                    canvas.save(output_path)
                    sys.stdout.write(f"\r[double_spread_log] Saved: spread_{spread_counter:03}.jpg")
                    sys.stdout.flush()
                    spread_counter += 1
                    i += 2
                else:
                    img = Image.open(pages[i]).convert("RGB")
                    img_width, img_height = img.size
                    canvas = Image.new("RGB", (img_width * 2, img_height), "white")
                    blank_right = Image.new("RGB", (img_width, img_height), "white")
                    canvas.paste(img, (0, 0))
                    canvas.paste(blank_right, (img_width, 0))

                    output_path = os.path.join(output_dir, f"spread_{spread_counter:03}.jpg")
                    canvas.save(output_path)
                    sys.stdout.write(f"\r[double_spread_log] Saved: spread_{spread_counter:03}.jpg")
                    sys.stdout.flush()
                    spread_counter += 1
                    i += 1

    
    def create_spread_pdf(self):
        input_dir = "output_spreads"
        orientation = input("\n\nChoose orientation - Landscape [L] or Portrait [P]: ").strip().upper()
        output_pdf_path = self.pdfPath[:-4] + "_"  + orientation + "_" + "final.pdf"

        if orientation not in ("L", "P"):
            print("[ERROR] Invalid input. Use 'L' or 'P'.")
            return

        image_filenames = sorted([
            fname for fname in os.listdir(input_dir)
            if fname.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])

        images = [
            Image.open(os.path.join(input_dir, fname)).convert("RGB")
            for fname in image_filenames
        ]

        processed_images = []

        for img in images:
            if orientation == "P":
                img = img.rotate(-90, expand=True)
            processed_images.append(img)

        if processed_images:
            processed_images[0].save(
                output_pdf_path,
                save_all=True,
                append_images=processed_images[1:]
            )
            print(f"\nPDF generated: {output_pdf_path}")
        else:
            print("\nNo images found to include in PDF.")

    
    def create_pdf(self):
        user_response = input("\n\nPress Y to follow all the steps, N to skip to creating PDF from the merged generated images : ")
        if(user_response == 'Y'):
            self.pdf_to_img()
            self.generate_spread_pages()
            self.create_spread_pdf()
            print("\n\nAll steps completed..!")
        elif(user_response == 'N'):
            self.create_spread_pdf()
            print("\n\nAll steps completed..!")
        else:
            print("\n\033[1mInvalid input!\033[0m\nPlease note the input must be in \033[1mY/N\033[0m.")
            exit()
        return None


def main():
    obj = DoubleSpread()
    obj.create_pdf()

if __name__ == "__main__":
    main()