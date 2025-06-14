import json
from datetime import datetime
import os

class User:
    def __init__(self, name):
        self.name = name
        self.mood_history = {}  # Dictionary to store Mood Entries {date: (description, mood, score)}

    def add_entry(self, date, description, mood, score):
        self.mood_history[date] = (description, mood, score)

    def get_history(self):
        return self.mood_history

# Analyze Mood based on keywords and return Mood Label and Score:
def analyze_mood(description):
    description = description.lower()
    positive_keywords = ["happy", "great", "awesome", "good", "excited"]
    neutral_keywords = ["okay", "fine", "normal", "meh"]
    negative_keywords = ["sad", "tired", "bad", "angry", "depressed"]

    score = 2  # Default to neutral
    mood = "Neutral"

    if any(keyword in description for keyword in positive_keywords):
        score = 3
        mood = "Happy"
    elif any(keyword in description for keyword in negative_keywords):
        score = 1
        mood = "Sad"

    return mood, score

# Suggest an Activity based on the Mood:
def suggest_activity(mood):
    activities = {
        "Happy": "Go for a walk and enjoy the day!",
        "Neutral": "Try reading a book or watching a movie.",
        "Sad": "Listen to some uplifting music or call a friend."
    }
    return activities.get(mood, "Take some time to relax.")

# Save Mood history to a JSON file:
def save_journal(user, filename="journal.json"):
    try:
        with open(filename, 'w') as file:
            json.dump({user.name: user.mood_history}, file)
        print("Journal saved successfully!")
    except Exception as e:
        print(f"Error saving Journal: {e}")

# Load Mood history from a JSON file:
def load_journal(filename="journal.json"):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
                return data
        return None
    except Exception as e:
        print(f"Error loading Journal: {e}")
        return None

# Export Mood history to a Text file:
def export_to_txt(user, filename="journal_export.txt"):
    try:
        with open(filename, 'w') as file:
            file.write(f"{user.name}'s Mood Journal\n")
            file.write("=" * 30 + "\n")
            for date, (description, mood, score) in user.mood_history.items():
                file.write(f"Date: {date}\nDescription: {description}\nMood: {mood} (Score: {score})\n\n")
        print("Journal exported to", filename)
    except Exception as e:
        print(f"Error exporting Journal: {e}")

# Calculate and display a weekly Mood Summary:
def weekly_summary(user):
    if not user.mood_history:
        print("No entries to summarize.")
        return

    scores = [score for _, (_, _, score) in user.mood_history.items()]
    avg_score = sum(scores) / len(scores)
    
    if avg_score > 2.5:
        summary = "Mostly Happy"
    elif avg_score > 1.5:
        summary = "Mostly Neutral"
    else:
        summary = "Mostly Sad"
    
    print(f"Weekly Mood Summary: {summary} (Average Score: {avg_score:.2f})")

# Find and display the most common Mood:
def most_common_mood(user):
    if not user.mood_history:
        print("No entries to analyze.")
        return
    
    moods = [mood for _, (_, mood, _) in user.mood_history.items()]
    common_mood = max(set(moods), key=moods.count)
    print(f"Most Common Mood: {common_mood}")

# Load existing Journal or create a new user:
def main():
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty. Using default name 'User'.")
        name = "User"
    
    user = User(name)
    journal_data = load_journal()
    if journal_data and name in journal_data:
        user.mood_history = journal_data[name]
        print(f"Welcome back, {name}! Loaded your Journal.")

    while True:
        print("\nMood Journal Menu:")
        print("1. Log a new entry")
        print("2. View Mood history")
        print("3. View weekly Summary")
        print("4. View most common Mood")
        print("5. Export Journal to Text file")
        print("6. Save and exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            try:
                date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                if not date:
                    date = datetime.now().strftime("%Y-%m-%d")
                else:
                    datetime.strptime(date, "%Y-%m-%d")  # Validate date format
                
                description = input("How are you feeling today? ").strip()
                if not description:
                    print("Description cannot be empty.")
                    continue
                
                mood, score = analyze_mood(description)
                user.add_entry(date, description, mood, score)
                print(f"Entry logged: Mood = {mood}, Score = {score}")
                print("Suggestion:", suggest_activity(mood))
            
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        elif choice == "2":
            if not user.mood_history:
                print("No entries found.")
            else:
                print(f"\n{name}'s Mood History:")
                for date, (description, mood, score) in user.mood_history.items():
                    print(f"Date: {date}, Description: {description}, Mood: {mood} (Score: {score})")
        
        elif choice == "3":
            weekly_summary(user)
        
        elif choice == "4":
            most_common_mood(user)
        
        elif choice == "5":
            export_to_txt(user)
        
        elif choice == "6":
            save_journal(user)
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()