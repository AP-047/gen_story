# models/story_generator.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class NoirStoryGenerator:
    """Generate a 4-chapter noir story with chained context and simple language."""
    def __init__(self):
        print("📝 Initializing story generator...")
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
        self.model = AutoModelForCausalLM.from_pretrained("gpt2-medium")
        # Ensure pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.tokenizer.eos_token_id
        print("✅ Story generator ready!")

    def generate_chapters(self, prefs):
        name = prefs['detective_name']
        style = prefs['investigation_style']
        atm = prefs['atmosphere']

        chapters = []
        context = ""  # will accumulate previous chapter text

        for idx, title in enumerate(
            ["The Discovery", "First Leads", "The Breakthrough", "Resolution"], start=1
        ):
            # Build prompt with chaining
            base = f"Chapter {idx}: {title}\n"
            if idx == 1:
                prompt = (
                    f"{base}"
                    f"Detective {name} arrives at a crime scene in {atm.lower()}. "
                    f"The victim lies motionless. Using {style.lower()}, the detective begins to work. "
                    f"Write the scene in clear, simple language:"
                )
            else:
                prompt = (
                    f"{base}"
                    f"Last, this happened: {context}\n"
                    f"Continue the story in clear, simple language:"
                )

            text = self._generate_text(prompt)
            clean = text.strip().replace("\n", " ")
            chapters.append((prompt, clean))

            # Update context with this chapter’s text (limit length)
            context = (context + " " + clean)[-800:]

        return chapters

    def _generate_text(self, prompt, max_new_tokens=180):
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=400
        )
        out = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=self.tokenizer.eos_token_id,
            do_sample=True,
            no_repeat_ngram_size=2
        )
        full = self.tokenizer.decode(out[0], skip_special_tokens=True)
        return full[len(prompt):]

# Quick test
if __name__ == "__main__":
    sg = NoirStoryGenerator()
    prefs = {
        'detective_name': 'Detective Kim',
        'investigation_style': 'Intuitive gut feelings',
        'atmosphere': 'smoke-filled jazz clubs'
    }
    chapters = sg.generate_chapters(prefs)
    for n,(_,text) in enumerate(chapters, start=1):
        print(f"\n--- Chapter {n} ---\n{text[:200]}...\n")
