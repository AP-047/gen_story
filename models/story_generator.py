import torch
import random
from transformers import AutoModelForCausalLM, AutoTokenizer

# story generator with templates and fallbacks
class StoryGenerator:
    def __init__(self):
        print("Initializing story generator...")
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
        self.model = AutoModelForCausalLM.from_pretrained("gpt2-medium")
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.tokenizer.eos_token_id
        
        # initialize story templates
        self.setup_story_templates()
        print("Story generator ready.")
    
    # define story structure templates for consistency
    def setup_story_templates(self):
        
        # crime types with specific details
        self.crime_types = [
            {
                "victim": "art dealer",
                "location": "upscale gallery", 
                "weapon": "poison",
                "clue": "forged painting"
            },
            {
                "victim": "jazz club owner",
                "location": "smoky nightclub",
                "weapon": "gunshot", 
                "clue": "hidden recording"
            },
            {
                "victim": "wealthy businessman", 
                "location": "penthouse office",
                "weapon": "stabbing",
                "clue": "secret ledger"
            }
        ]
        
        # suspect types
        self.suspects = [
            {"name": "Elena Martinez", "role": "business partner", "motive": "money"},
            {"name": "Marcus Webb", "role": "rival competitor", "motive": "revenge"}, 
            {"name": "Sarah Chen", "role": "former employee", "motive": "betrayal"}
        ]
        
        # investigation methods
        self.methods = {
            "Methodical evidence analysis": ["examined fingerprints", "studied blood patterns", "analyzed documents"],
            "Intuitive gut feelings": ["sensed something wrong", "followed a hunch", "trusted instincts"],
            "Psychological profiling": ["studied the killer's mind", "analyzed behavior patterns", "understood motives"]
        }
    
    # generate a complete, coherent 4-chapter story
    def generate_chapters(self, prefs):
        
        name = prefs['detective_name'] 
        style = prefs['investigation_style']
        atm = prefs['atmosphere']
        
        # select consistent story elements
        crime = random.choice(self.crime_types)
        suspect = random.choice(self.suspects)
        methods = self.methods[style]
        
        # generate each chapter with templates
        chapters = []
        
        # chapter 1
        ch1 = self.generate_chapter_1(name, atm, crime, methods[0])
        chapters.append(("Chapter 1: The Discovery", ch1))
        
        # chapter 2 
        ch2 = self.generate_chapter_2(name, crime, suspect, methods[1])
        chapters.append(("Chapter 2: First Leads", ch2))
        
        # chapter 3
        ch3 = self.generate_chapter_3(name, crime, suspect, methods[2])
        chapters.append(("Chapter 3: The Breakthrough", ch3))
        
        # chapter 4
        ch4 = self.generate_chapter_4(name, suspect, crime)
        chapters.append(("Chapter 4: Resolution", ch4))
        
        return chapters
    
    def generate_chapter_1(self, detective, atmosphere, crime, method):
        """Generate discovery chapter with guaranteed structure."""
        
        prompt = (
            f"Detective {detective} arrived at the {crime['location']} in {atmosphere.lower()}. "
            f"The victim, a {crime['victim']}, was found dead. The detective {method} and discovered "
            f"that the cause of death was {crime['weapon']}. Write what the detective found in simple words:"
        )
        
        ai_text = self._safe_generate(prompt, max_tokens=100)
        
        # template-based fallback
        if len(ai_text.strip()) < 50:
            ai_text = (
                f"The {crime['location']} was quiet and dark. "
                f"The {crime['victim']} lay on the floor, clearly dead from {crime['weapon']}. "
                f"Detective {detective} noticed something strange about the scene. "
                f"There were signs that this was not a random crime."
            )
        
        # combine template + AI for structure
        full_chapter = (
            f"Detective {detective} walked into the {crime['location']}. "
            f"The atmosphere was tense in the {atmosphere.lower()}. "
            f"The victim, a {crime['victim']}, had been killed by {crime['weapon']}. "
            f"{ai_text.strip()} "
            f"This was clearly the start of a complex case."
        )
        
        return full_chapter
    
    def generate_chapter_2(self, detective, crime, suspect, method):
        """Generate investigation chapter with suspect introduction."""
        
        prompt = (
            f"Detective {detective} began investigating the {crime['victim']} murder case. "
            f"The detective {method} and started interviewing people. "
            f"One person of interest was {suspect['name']}, the victim's {suspect['role']}. "
            f"Write what the detective discovered in simple words:"
        )
        
        ai_text = self._safe_generate(prompt, max_tokens=100)
        
        if len(ai_text.strip()) < 50:
            ai_text = (
                f"{suspect['name']} seemed nervous during questioning. "
                f"There were inconsistencies in the story about the night of the murder. "
                f"The motive appeared to be related to {suspect['motive']}."
            )
        
        full_chapter = (
            f"Detective {detective} spent the next day investigating the case. "
            f"The first person to interview was {suspect['name']}, who worked as the victim's {suspect['role']}. "
            f"{ai_text.strip()} "
            f"Detective {detective} knew that {suspect['motive']} could be a strong motive for murder. "
            f"More investigation was needed to find the truth."
        )
        
        return full_chapter
    
    def generate_chapter_3(self, detective, crime, suspect, method):
        """Generate breakthrough chapter with evidence discovery."""
        
        prompt = (
            f"Detective {detective} found an important clue: {crime['clue']}. "
            f"This evidence connected {suspect['name']} to the crime. "
            f"The detective {method} and realized the truth. "
            f"Write what happened next in simple words:"
        )
        
        ai_text = self._safe_generate(prompt, max_tokens=100)
        
        if len(ai_text.strip()) < 50:
            ai_text = (
                f"The {crime['clue']} had {suspect['name']}'s fingerprints on it. "
                f"This proved that {suspect['name']} was at the crime scene. "
                f"The motive was clearly {suspect['motive']}."
            )
        
        full_chapter = (
            f"The breakthrough came when Detective {detective} found the {crime['clue']}. "
            f"This was the missing piece of evidence that connected everything. "
            f"{ai_text.strip()} "
            f"Now Detective {detective} had enough evidence to confront {suspect['name']}. "
            f"The case was almost solved."
        )
        
        return full_chapter
    
    def generate_chapter_4(self, detective, suspect, crime):
        """Generate resolution chapter with guaranteed ending."""
        
        prompt = (
            f"Detective {detective} confronted {suspect['name']} with the evidence. "
            f"The {crime['clue']} proved {suspect['name']} was the killer. "
            f"Write how the case ended in simple words:"
        )
        
        ai_text = self._safe_generate(prompt, max_tokens=100)
        
        if len(ai_text.strip()) < 50:
            ai_text = (
                f"{suspect['name']} broke down and confessed to the murder. "
                f"The motive was {suspect['motive']}, just as Detective {detective} suspected. "
                f"Justice was served."
            )
        
        full_chapter = (
            f"Detective {detective} called {suspect['name']} to the police station. "
            f"When shown the evidence - the {crime['clue']} - there was no way to deny the truth. "
            f"{ai_text.strip()} "
            f"The case of the murdered {crime['victim']} was now closed. "
            f"Detective {detective} had solved another mystery."
        )
        
        return full_chapter
    
    # generate text with error handling and quality control
    def _safe_generate(self, prompt, max_tokens=100):
        try:
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                truncation=True, 
                max_length=300
            )
            
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=0.6,  # lower for more consistency
                top_p=0.8,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True
            )
            
            full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            new_text = full_text[len(prompt):].strip()
            
            # quality control - ensure minimum length & sensibility
            if len(new_text) > 20 and not any(word in new_text.lower() for word in ['error', 'invalid', '###']):
                return new_text
            else:
                return ""  # will trigger fallback
                
        except Exception as e:
            print(f"Generation error: {e}")
            return ""  # will trigger fallback

# test the generator
if __name__ == "__main__":
    sg = StoryGenerator()
    prefs = {
        'detective_name': 'Detective Jones',
        'investigation_style': 'Methodical evidence analysis', 
        'atmosphere': 'Rain-soaked city streets'
    }
    
    chapters = sg.generate_chapters(prefs)
    for i, (title, text) in enumerate(chapters, 1):
        print(f"\n=== {title} ===")
        print(text)
        print(f"\nTokens: {len(sg.tokenizer.encode(text))}")