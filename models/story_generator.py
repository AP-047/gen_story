from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time

class NoirStoryGenerator:
    def __init__(self):
        print("🔄 Loading AI story model... (this may take a few minutes the first time)")
        
        self.model_name = "gpt2-medium"
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print("✅ AI model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def generate_complete_noir_story(self, user_preferences):
        """Generate a complete long-form noir story in connected chapters"""
        
        print("🔄 Generating your complete noir story...")
        
        # Story structure: 4 chapters for ~10 minutes
        chapters = [
            {"title": "The Discovery", "focus": "crime scene investigation"},
            {"title": "First Leads", "focus": "evidence analysis and initial suspects"},
            {"title": "The Breakthrough", "focus": "key discovery and plot twist"},
            {"title": "Resolution", "focus": "solving the case and conclusion"}
        ]
        
        story_parts = []
        story_context = ""
        
        for i, chapter in enumerate(chapters):
            print(f"📝 Writing Chapter {i+1}: {chapter['title']}...")
            
            # Generate each chapter with growing context
            chapter_text = self.generate_story_chapter(
                user_preferences, 
                chapter, 
                story_context,
                chapter_number=i+1,
                total_chapters=len(chapters)
            )
            
            story_parts.append(f"## Chapter {i+1}: {chapter['title']}\n\n{chapter_text}")
            
            # Update context for next chapter (sliding window approach)
            story_context = self.update_story_context(story_context, chapter_text, max_context_length=400)
            
            # Small delay between chapters
            time.sleep(1)
        
        # Combine all chapters
        complete_story = "\n\n---\n\n".join(story_parts)
        
        # Add atmospheric ending
        complete_story += "\n\n---\n\n*Case closed. But in this city, there's always another mystery waiting in the shadows...*"
        
        print("✅ Complete story generated!")
        return complete_story
    
    def generate_story_chapter(self, preferences, chapter_info, previous_context, chapter_number, total_chapters):
        """Generate a single chapter with proper context"""
        
        detective_name = preferences.get('detective_name', 'Detective Morgan')
        investigation_style = preferences.get('investigation_style', 'Methodical evidence analysis')
        atmosphere = preferences.get('atmosphere', 'Rain-soaked city streets')
        
        # Create chapter-specific prompt
        if chapter_number == 1:
            prompt = f"""Detective {detective_name} specializes in {investigation_style.lower()}. The city's {atmosphere.lower()} create the perfect backdrop for mysterious crimes.

A call came in at 11:47 PM. A prominent art dealer had been found dead under mysterious circumstances. As Detective {detective_name} arrived at the crime scene, the atmosphere was thick with tension.

Chapter 1: The Discovery

Detective {detective_name} stepped through the doorway, immediately noticing"""
        
        else:
            prompt = f"""Detective {detective_name} continues the investigation. Previous events: {previous_context}

Chapter {chapter_number}: {chapter_info['title']}
Focus: {chapter_info['focus']}

As the investigation deepens, Detective {detective_name}"""
        
        # Generate longer chapter text
        chapter_text = self.generate_text(prompt, max_new_tokens=400, temperature=0.8)
        
        # Clean and format the chapter
        return self.format_chapter_text(chapter_text, chapter_info['title'])
    
    def update_story_context(self, current_context, new_chapter, max_context_length=400):
        """Update story context using sliding window approach"""
        
        # Extract key information from new chapter for context
        key_sentences = new_chapter.split('.')[:3]  # Take first 3 sentences
        new_context = '. '.join([s.strip() for s in key_sentences if len(s.strip()) > 10]) + '.'
        
        # Combine with previous context
        combined_context = f"{current_context} {new_context}".strip()
        
        # Keep context within token limits using sliding window
        words = combined_context.split()
        if len(words) > max_context_length:
            # Keep the most recent context
            combined_context = ' '.join(words[-max_context_length:])
        
        return combined_context
    
    def format_chapter_text(self, raw_text, chapter_title):
        """Format and clean chapter text"""
        
        if not raw_text or len(raw_text.strip()) < 50:
            return f"The investigation continues as Detective {self.preferences.get('detective_name', 'Morgan')} follows new leads in this complex case..."
        
        # Split into sentences and clean
        sentences = raw_text.split('.')
        clean_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 15 and not sentence.startswith(('http', 'www', '@', 'Chapter')):
                # Capitalize first letter
                if sentence:
                    sentence = sentence.upper() + sentence[1:]
                    clean_sentences.append(sentence)
        
        # Ensure good chapter length (aim for 6-10 sentences per chapter)
        final_sentences = clean_sentences[:10]  
        
        if len(final_sentences) >= 3:
            formatted_text = '. '.join(final_sentences) + '.'
        else:
            # Fallback for short chapters
            formatted_text = self.get_fallback_chapter(chapter_title)
        
        return formatted_text
    
    def get_fallback_chapter(self, chapter_title):
        """Provide fallback content if generation fails"""
        
        fallbacks = {
            "The Discovery": """The crime scene was unlike anything Detective Morgan had encountered before. The victim lay in the center of an upscale gallery, surrounded by priceless artwork that remained mysteriously untouched. Blood spatter patterns suggested a struggle, yet there were no signs of forced entry. The security system had been disabled from the inside, pointing to someone with intimate knowledge of the building. Detective Morgan crouched down to examine a peculiar detail - a single white chess piece placed deliberately next to the victim's hand. This wasn't a random act of violence; it was a message. The killer wanted to play a game, and Detective Morgan was now an unwilling participant in this deadly puzzle.""",
            
            "First Leads": """The investigation led Detective Morgan through the victim's complex web of relationships. Gallery owner Marcus Rivera had been involved in several questionable art deals over the past year. His business partner, Elena Vasquez, had recently discovered discrepancies in their financial records. Meanwhile, art critic Jonathan Hayes had published a scathing review just days before the murder, questioning the authenticity of several pieces in Rivera's collection. Each interview revealed new motives and deeper secrets. The white chess piece found at the scene was traced to an exclusive set sold at auction three months prior. Detective Morgan realized that this case would require more than standard investigative techniques - it demanded an understanding of the art world's hidden darkness.""",
            
            "The Breakthrough": """A breakthrough came from an unexpected source. The gallery's cleaning lady, Maria Santos, had witnessed something crucial but feared speaking up due to her immigration status. Detective Morgan assured her protection and learned about a secret room behind the main gallery wall. Inside, they discovered forged paintings worth millions and detailed records of an international art forgery ring. The white chess piece wasn't just a calling card - it was a symbol used by a sophisticated criminal organization. Rivera hadn't been just a victim; he had been a key player who tried to leave the game. The real killer was someone much more dangerous than initially suspected, someone who viewed murder as just another move on their criminal chessboard.""",
            
            "Resolution": """The final confrontation took place in the same gallery where it all began. Detective Morgan had discovered that the mastermind was Elena Vasquez, Rivera's trusted partner, who had been orchestrating the forgery operation from the beginning. Rivera's attempt to expose her had signed his death warrant. The chess piece was her signature, left at the scene of every elimination. As police surrounded the building, Elena made one last desperate move, attempting to destroy evidence that would implicate her international network. But Detective Morgan had anticipated this, having already secured copies of all crucial documents. The case closed with Elena's arrest, but the investigation had revealed a vast criminal enterprise that would take years to fully unravel. In this city of shadows, one mystery's end was often another's beginning."""
        }
        
        return fallbacks.get(chapter_title, "The investigation continues with new discoveries that bring Detective Morgan closer to the truth...")
    
    def generate_text(self, prompt, max_new_tokens=400, temperature=0.8):
        """Generate text with optimized parameters for story continuity"""
        
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=600, truncation=True)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_k=50,
                    top_p=0.95,
                    repetition_penalty=1.15,  # Higher penalty to avoid repetition
                    no_repeat_ngram_size=3,
                    pad_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1,
                    do_sample=True
                )
            
            generated_text = self.tokenizer.decode(outputs, skip_special_tokens=True)
            new_text = generated_text[len(self.tokenizer.decode(inputs, skip_special_tokens=True)):].strip()
            
            return new_text
            
        except Exception as e:
            print(f"Generation error: {e}")
            return "The investigation reveals new clues that bring the detective closer to solving this complex case."

# Test the generator
if __name__ == "__main__":
    generator = NoirStoryGenerator()
    
    test_preferences = {
        'detective_name': 'Detective Blake',
        'investigation_style': 'Intuitive gut feelings',
        'atmosphere': 'Smoke-filled jazz clubs'
    }
    
    complete_story = generator.generate_complete_noir_story(test_preferences)
    
    # Count tokens to verify length
    tokens = generator.tokenizer.encode(complete_story)
    print(f"\n📊 Story Statistics:")
    print(f"Total tokens: {len(tokens)}")
    print(f"Estimated reading time: {len(tokens)/4:.1f} minutes")
    print(f"Word count: ~{len(complete_story.split())}")

