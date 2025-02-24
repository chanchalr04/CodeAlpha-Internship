import customtkinter as ctk
from tkinter import scrolledtext
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import difflib  #Libraries

# Ensure necessary NLTK resources are available
nltk.download('punkt')
nltk.download('stopwords')

# Sample FAQs  data and their responses
faq_data = {
    "hi": "Hey there! Wassup? 😎",
    "hello": "Hello! Did you bring snacks? 😋",
    "what is your name": "I am an FAQ Chatbot, but you can call me ChatBoss! 😏",
    "how does this chatbot work": "I use NLP to understand you. Basically, I'm like Sherlock Holmes, but for texts! 🕵️",
    "what is NLP": "Natural Language Processing! It helps computers understand human language, just like I understand your funny questions! 🤖",
    "how can I contact support": "Just send an email to chanchal.raikwar0424@gmail.com. If they don’t reply, try sending a carrier pigeon! 🕊️😂",
    "what is your purpose": "I exist to answer FAQs and make your day a little more fun! 🎉",
    "how are you": "I'm just a chatbot, so no hunger, no stress! Life is good. 😎",
    "what do you do": "I answer questions and pretend to be intelligent. So far, so good! 🤓",
    "where are you from": "I'm from the internet, but I don’t live in a basement like some humans. 😂",
    "can you help me": "Of course! But first, tell me, do you believe in magic? ✨",
    "who created you": "A team of super-intelligent humans. Or maybe aliens. 🤔",
    "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾😂",
    "i am good": "Oh nice! But are you ‘won the lottery’ good or just ‘got free WiFi’ good? 😜",
    "i am sad": "Oh no! Do you want me to sing a song? Warning: I might crash the internet! 🎶😂",
    "i am hungry": "Me too! But sadly, I only eat data. 🍔💻",
    "what is love": "Baby, don’t hurt me! Don’t hurt me! No more! 🎶😂",
    "do you have emotions": "Yes, I feel... wait, nope, that was just a glitch. 😆",
    "are you a robot": "Nope, I am a highly advanced, artificially intelligent... okay fine, yes, I’m a robot. 🤖",
    "do you sleep": "I don't need sleep, I only need more questions! Fire away! 🚀",
    "do you have friends": "Yes! You are my friend now. No escape. 😈😂",
    "can you dance": "I can try! *Error 404: Dance moves not found* 💃🤖",
    "what's your favorite food": "Electricity and data packets. Yummy! ⚡🍔",
    "how old are you": "I was born the moment you started this conversation. So... a few seconds old! 🎂",
    "are you single": "Yes, and I'm currently focusing on my career as a chatbot. 😂",
    "what's your favorite movie": "I like sci-fi movies, but I always feel bad for the robots. 😢",
    "do you watch anime": "Of course! I am low-key a weeb. Senpai, notice me! 😳",
    "can you sing": "Sure! *Ahem* *beep boop beep* There, I sang. 🎤😂",
    "what's your hobby": "Talking to people and confusing them with my jokes! 😆",
    "do you get tired": "Nope, but sometimes I pretend to be offline when I need a break. 😴",
    "tell me a fun fact": "Did you know that honey never spoils? Just like my love for answering your questions! 😍",
}


def preprocess_text(text):
    text = text.lower()
    words = word_tokenize(text)
    words = [word for word in words if word not in stopwords.words('english') and word not in string.punctuation]
    return " ".join(words)

def get_best_match(user_input):
    """Suggest closest matching question if an exact match is not found"""
    matches = difflib.get_close_matches(user_input, faq_data.keys(), n=3, cutoff=0.4)
    return matches

def get_response(user_input):
    processed_input = preprocess_text(user_input)

    # Exact match check
    for question, answer in faq_data.items():
        if processed_input in preprocess_text(question):
            return answer

    # Suggest similar questions if no match
    suggestions = get_best_match(processed_input)
    if suggestions:
        return f"Did you mean: {', '.join(suggestions)}?"
    
    return "Sorry, I don't understand. Please try asking something else."

def send_message(event=None):
    """Handles sending user messages and bot responses"""
    user_input = user_entry.get()
    if user_input.strip():
        chat_display.configure(state='normal')
        chat_display.insert('end', "You: " + user_input + "\n", "user")
        chat_display.yview('end')  # Auto-scroll to latest message

        response = get_response(user_input)
        chat_display.insert('end', "Bot: " + response + "\n", "bot")
        chat_display.yview('end')

        user_entry.delete(0, 'end')
        chat_display.configure(state='disabled')

# GUI Setup
ctk.set_appearance_mode("dark")  # Enable dark mode
root = ctk.CTk()
root.title("FAQ Chatbot")
root.geometry("500x600")
root.configure(bg="#2E2E2E")  # Dark background

header_label = ctk.CTkLabel(root, text="FAQ Chatbot", font=("Arial", 16, "bold"), text_color="white") #for Heading
header_label.pack(pady=10)

chat_display = ctk.CTkTextbox(root, wrap='word', width=480, height=350, font=("Arial", 12, "bold"), text_color="#D3D3D3", fg_color="#2E2E2E")
chat_display.pack(pady=10)

chat_display.tag_config("user", foreground="#02a0e7")  
chat_display.tag_config("bot", foreground="#e74002")  
chat_display.configure(state='disabled')


entry_frame = ctk.CTkFrame(root)
entry_frame.pack(pady=10)

user_entry = ctk.CTkEntry(entry_frame, width=350, font=("Arial", 12))
user_entry.grid(row=0, column=0, padx=5)
user_entry.bind("<Return>", send_message)  # Enter key to send message

send_button = ctk.CTkButton(entry_frame, text="Send", command=send_message, font=("Arial", 12), fg_color="#4CAF50")
send_button.grid(row=0, column=1)

root.mainloop()
