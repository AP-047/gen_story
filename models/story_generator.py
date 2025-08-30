# models/story_generator.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class NoirStoryGenerator:
    """Generate a complete noir detective story in 4 chapters."""
    def __init__(self):
        print("📝 Initializing story generator...")
        self.model_name = "gpt2-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        # Ensure pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.tokenizer.eos_token_id
        print("✅ Story generator ready!")

    def generate_complete_noir_story(self, prefs):
        """Generate 4 connected chapters as one story string."""
        name = prefs['detective_name']
        style = prefs['investigation_style']
        atm = prefs['atmosphere']
        
        chapters = []
        prompts = [
            f"Chapter 1: The Discovery\nDetective {name} arrived at the crime scene in {atm.lower()}. The victim, a prominent art dealer, lay dead under mysterious circumstances. Using {style.lower()}, Detective {name} examined the surroundings and noticed",
            f"Chapter 2: First Leads\nDetective {name} followed initial leads through interviews and forensic evidence. The art world secrets revealed motives that pointed to",
            f"Chapter 3: The Breakthrough\nA hidden clue uncovered by Detective {name} shifted the investigation towards a criminal network. In a secret chamber, Detective {name} discovered",
            f"Chapter 4: Resolution\nDetective {name} confronted the culprit in a final showdown. The truth behind the murder was revealed when"
        ]

        for i, prompt in enumerate(prompts, start=1):
            text = self._generate_text(prompt, max_new_tokens=200)
            chapters.append(f"## Chapter {i}\n\n{text.strip()}")
        
        return "\n\n".join(chapters)

    def _generate_text(self, prompt, max_new_tokens=200):
        """Generate a text continuation for a given prompt."""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=400)
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                no_repeat_ngram_size=2
            )
            gen = self.tokenizer.decode(output[0], skip_special_tokens=True)
            # Remove original prompt
            return gen[len(prompt):].strip()
        except Exception as e:
            # Fallback sentence
            return " The investigation continued, revealing deeper secrets that challenged Detective skills."

# Test
if __name__ == "__main__":
    sg = NoirStoryGenerator()
    prefs = {
        'detective_name': 'Detective Morgan',
        'investigation_style': 'Methodical evidence analysis',
        'atmosphere': 'Rain-soaked city streets'
    }
    story = sg.generate_complete_noir_story(prefs)
    print(story)
