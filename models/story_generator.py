from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class NoirStoryGenerator:
    def __init__(self):
        print("🔄 Loading AI story model... (this may take a few minutes the first time)")
        
        # Use GPT-2 medium - more reliable for story generation
        self.model_name = "gpt2-medium"
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Set padding token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print("✅ AI model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def generate_noir_story(self, user_preferences, scene_type="opening"):
        """Generate a noir detective story based on user preferences"""
        
        # Create story prompt based on user preferences
        prompt = self.create_story_prompt(user_preferences, scene_type)
        
        # Generate story using AI
        story_text = self.generate_text(prompt)
        
        return story_text
    
    def create_story_prompt(self, preferences, scene_type):
        """Create a compelling prompt for noir story generation"""
        
        investigation_style = preferences.get('investigation_style', 'Methodical evidence analysis')
        atmosphere = preferences.get('atmosphere', 'Rain-soaked city streets')
        detective_name = preferences.get('detective_name', 'Detective Morgan')
        complexity = preferences.get('complexity', 'Simple mystery')
        
        if scene_type == "opening":
            # More detailed prompt for longer stories
            prompt = f"""Detective {detective_name} is a seasoned investigator who specializes in {investigation_style.lower()}. The city is known for its {atmosphere.lower()}, creating the perfect backdrop for mysterious crimes.

The latest case began when a call came in at 11:47 PM. The victim, a prominent art dealer, had been found dead under circumstances that defied explanation. As Detective {detective_name} arrived at the scene, the {atmosphere.lower()} set an ominous mood.

Walking through the crime scene, Detective {detective_name} noticed several peculiar details. The first thing that caught attention was"""
            
        return prompt
    
    def generate_text(self, prompt, max_new_tokens=300, temperature=0.8):
        """Generate longer, more detailed text using the AI model"""
        
        try:
            # Encode the prompt
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=700, truncation=True)
            
            # Generate response with better parameters for longer stories
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=max_new_tokens,  # Generate more tokens
                    temperature=temperature,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    repetition_penalty=1.1,  # Reduce repetition
                    no_repeat_ngram_size=3,  # Avoid repeating 3-word phrases
                    pad_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1
                )
            
            # Decode generated text
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the new part (remove original prompt)
            new_text = generated_text[len(self.tokenizer.decode(inputs[0], skip_special_tokens=True)):].strip()
            
            # Clean up and format the text
            if new_text:
                # Split into sentences and clean them up
                sentences = new_text.split('.')
                clean_sentences = []
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    # Only include substantial sentences (more than 15 characters)
                    if len(sentence) > 15 and not sentence.startswith(('http', 'www', '@')):
                        # Capitalize first letter
                        sentence = sentence[0].upper() + sentence[1:] if sentence else sentence
                        clean_sentences.append(sentence)
                
                # Take first 6-8 sentences for a good story length
                final_sentences = clean_sentences[:8]
                
                if final_sentences:
                    # Join sentences and add proper formatting
                    story = '. '.join(final_sentences) + '.'
                    
                    # Add dramatic ending
                    story += "\n\n*The investigation is just beginning...*"
                    
                    return story
                else:
                    return self.get_fallback_story(user_preferences)
            else:
                return self.get_fallback_story(user_preferences)
            
        except Exception as e:
            print(f"Generation error: {e}")
            return self.get_fallback_story(user_preferences)
    
    def get_fallback_story(self, preferences):
        """Provide a fallback story if AI generation fails"""
        detective_name = preferences.get('detective_name', 'Detective Morgan')
        atmosphere = preferences.get('atmosphere', 'rain-soaked city streets')
        
        return f"""Detective {detective_name} stepped into the dimly lit crime scene, where shadows danced across the walls in the flickering streetlight. The {atmosphere.lower()} created an atmosphere thick with mystery and danger.

The victim lay motionless, but something about the scene didn't add up. There were no signs of forced entry, yet valuable items remained untouched. Detective {detective_name} crouched down to examine the evidence more closely, noting the unusual positioning of objects around the room.

A single photograph on the floor caught the detective's attention - it seemed out of place among the chaos. As {detective_name} picked it up, a chill ran down their spine. This case was about to become much more complicated than initially thought.

The sound of footsteps echoed from the hallway above, but when {detective_name} looked up, no one was there. In this city of secrets, nothing was ever as simple as it appeared.

*The investigation is just beginning...*"""

# Test the generator (optional)
if __name__ == "__main__":
    generator = NoirStoryGenerator()
    
    test_preferences = {
        'detective_name': 'Detective Blake',
        'investigation_style': 'Intuitive gut feelings',
        'atmosphere': 'Smoke-filled jazz clubs',
        'complexity': 'Complex investigation'
    }
    
    story = generator.generate_noir_story(test_preferences)
    print("Generated Story:")
    print(story)
