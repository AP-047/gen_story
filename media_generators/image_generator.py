# media_generators/image_generator.py

import os

class NoirImageLoader:
    """Load pre-generated static images for each chapter."""
    def __init__(self):
        print("🖼️ Initializing static image loader...")
        # Map chapter numbers to static image paths
        self.paths = {
            1: "assets/generated_images/chapter_1.png",
            2: "assets/generated_images/chapter_2.png",
            3: "assets/generated_images/chapter_3.png",
            4: "assets/generated_images/chapter_4.png"
        }

    def get_image(self, chapter_number):
        """Return the file path for a chapter image, or None if missing."""
        path = self.paths.get(chapter_number)
        if path and os.path.exists(path):
            return path
        return None
