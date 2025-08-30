from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import os

class NoirImageGenerator:
    def __init__(self):
        print("🎨 Initializing image generator...")
        
        # Theme configurations - easily changeable
        self.themes = {
            "film_noir": {
                "style": "film noir, black and white, dramatic lighting, high contrast, shadows",
                "negative": "color, bright, cartoon, anime, low quality"
            },
            "ghibli": {
                "style": "Studio Ghibli style, anime, hand-drawn, detailed, beautiful landscape",
                "negative": "photorealistic, dark, horror, low quality"
            },
            "cyberpunk": {
                "style": "cyberpunk, neon lights, futuristic city, rain, dark atmosphere",
                "negative": "bright, natural, countryside, low quality"
            },
            "comic_book": {
                "style": "comic book style, graphic novel, bold lines, cel shading",
                "negative": "photorealistic, blurry, low quality"
            }
        }
        
        # Set current theme (easy to change)
        self.current_theme = "film_noir"
        
        # Initialize model - using smaller, CPU-friendly version
        self.pipe = None
        self.setup_model()
    
    def setup_model(self):
        """Setup Stable Diffusion with CPU-friendly settings"""
        try:
            # Use smaller model for robustness
            model_id = "runwayml/stable-diffusion-v1-5"
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                safety_checker=None,  # Disable for speed
                requires_safety_checker=False
            )
            
            # CPU or GPU setup
            if torch.cuda.is_available():
                self.pipe = self.pipe.to("cuda")
                print("✅ Image generator loaded (GPU)")
            else:
                print("⚠️ Using CPU for images (will be slower)")
            
        except Exception as e:
            print(f"⚠️ Image generation not available: {e}")
            self.pipe = None
    
    def change_theme(self, theme_name):
        """Change the visual theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            print(f"🎨 Theme changed to: {theme_name}")
        else:
            print(f"⚠️ Theme '{theme_name}' not found")
    
    def generate_scene_image(self, scene_description, chapter_number=1):
        """Generate an image for a story scene"""
        
        if not self.pipe:
            return self.create_fallback_image(chapter_number)
        
        try:
            # Get current theme settings
            theme = self.themes[self.current_theme]
            
            # Create full prompt with theme
            full_prompt = f"{scene_description}, {theme['style']}"
            
            # Generate image
            print(f"🎨 Generating {self.current_theme} style image...")
            
            image = self.pipe(
                prompt=full_prompt,
                negative_prompt=theme['negative'],
                num_inference_steps=20,  # Reduced for speed
                guidance_scale=7.5,
                width=512,
                height=512
            ).images[0]
            
            # Save image
            image_path = self.save_image(image, chapter_number)
            print(f"✅ Image saved: {image_path}")
            
            return image_path
            
        except Exception as e:
            print(f"⚠️ Image generation failed: {e}")
            return self.create_fallback_image(chapter_number)
    
    def save_image(self, image, chapter_number):
        """Save generated image"""
        os.makedirs("assets/generated_images", exist_ok=True)
        
        filename = f"chapter_{chapter_number}_{self.current_theme}.png"
        filepath = os.path.join("assets/generated_images", filename)
        
        image.save(filepath)
        return filepath
    
    def create_fallback_image(self, chapter_number):
        """Create a simple fallback image if AI generation fails"""
        try:
            # Create a simple colored rectangle as fallback
            img = Image.new('RGB', (512, 512), color=(30, 30, 30))  # Dark grey
            
            filepath = f"assets/generated_images/fallback_chapter_{chapter_number}.png"
            os.makedirs("assets/generated_images", exist_ok=True)
            img.save(filepath)
            
            return filepath
            
        except Exception:
            return None

# Test the generator
if __name__ == "__main__":
    generator = NoirImageGenerator()
    
    # Test different themes
    themes_to_test = ["film_noir", "ghibli", "cyberpunk"]
    
    for theme in themes_to_test:
        generator.change_theme(theme)
        image_path = generator.generate_scene_image(
            "Detective standing in a dark alley investigating a crime scene",
            chapter_number=1
        )
        print(f"Generated: {image_path}")
