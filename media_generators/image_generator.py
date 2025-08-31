import os

# load pre-generated static images for each chapter
class ImageLoader:
    def __init__(self):
        print("Initializing static image loader...")
        # map chapter numbers to static image paths
        self.paths = {
            1: "assets/generated_images/chapter_1.png",
            2: "assets/generated_images/chapter_2.png",
            3: "assets/generated_images/chapter_3.png",
            4: "assets/generated_images/chapter_4.png"
        }

    # return the file path for a chapter image or none if missing
    def get_image(self, chapter_number):
        path = self.paths.get(chapter_number)
        if path and os.path.exists(path):
            return path
        return None