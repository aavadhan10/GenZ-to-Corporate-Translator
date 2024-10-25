import streamlit as st
from anthropic import Anthropic
import datetime
import csv
import os
from config import CLAUDE_API_KEY

def init_anthropic_client():
    """Initialize the Anthropic client with API key from config"""
    if not CLAUDE_API_KEY:
        st.error("Anthropic API key not found. Please check your config.py file.")
        st.stop()
    return Anthropic(api_key=CLAUDE_API_KEY)

def log_translation(input_phrase, output_phrase):
    """Log translations to a CSV file"""
    log_file = "translation_log.csv"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Create file with headers if it doesn't exist
        if not os.path.exists(log_file):
            with open(log_file, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Gen Z Phrase", "Corporate Translation"])
        
        # Append the new translation
        with open(log_file, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, input_phrase, output_phrase])
    except Exception as e:
        st.warning(f"Unable to log translation: {str(e)}")

def call_claude(system_prompt, user_input):
    """Call Claude API with the given prompts using the Messages API"""
    try:
        client = init_anthropic_client()
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.content[0].text
    except Exception as e:
        st.error(f"Error calling Claude: {e}")
        return None

def translate_phrase(input_phrase):
    """Translate Gen Z phrase to corporate speak using Claude"""
    system_prompt = "You are a professional translator that specializes in converting casual Gen Z language into formal corporate speak. Provide only the corporate translation without any additional explanation or context. Maintain the core meaning while making it sound professional and workplace-appropriate."
    user_prompt = f"Convert this Gen Z phrase to corporate speak: {input_phrase}"
    
    response = call_claude(system_prompt, user_prompt)
    if response:
        log_translation(input_phrase, response)
        return response
    return "Translation error occurred. Please try again."

# Streamlit UI
st.title("🔄 Gen Z to Corporate Translator by your girl Ankita")
st.write("Convert your casual Gen Z phrases and inhibitions into corporate-appropriate language to avoid workplace drama")

# Example phrases
examples = {
    "no cap": "I assure you this is completely true",
    "this is giving main character energy": "This demonstrates exceptional leadership qualities",
    "are you deadass?": "I require immediate clarification on this matter",
    "that's pretty mid": "This falls short of our expected standards",
    "fr fr": "I wholeheartedly agree with this assessment",
    "slay": "Excellent work on achieving this outcome"
}

# Input section
user_input = st.text_input("Enter your Gen Z phrase:", placeholder="e.g., 'no cap'")

# Example buttons in 3 columns for better layout
st.write("Or try these examples:")
cols = st.columns(3)
for i, (example, _) in enumerate(examples.items()):
    if cols[i % 3].button(example):
        user_input = example

# Translation
if user_input:
    with st.spinner("Translating..."):
        corporate_translation = translate_phrase(user_input)
        
    st.write("### Corporate Translation:")
    st.info(corporate_translation)
    
    # Show example corporate phrases
    if user_input.lower() in examples:
        st.write("### Similar corporate phrases include:")
        st.write(examples[user_input.lower()])

# Footer
st.markdown("---")
st.markdown("*Made with 💼 for the corporate girlies and boys*")
