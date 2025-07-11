import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

mood_levels = ["None", "Mild", "Moderate", "Severe"]

def get_choice(prompt, options):
    print(prompt)
    for i, option in enumerate(options, 0):
        print(f"{i}.{option}")
    choice = int(input("Enter choice number: "))
    return options[choice]

today = datetime.now()

data = {
    "Date": today,
    "Depressed Mood": get_choice("Today's most extreme depressed mood:", mood_levels),
    "Elevated Mood": get_choice("Today's most extreme elevated mood:", mood_levels),
    "Irritability": get_choice("Today's most extreme irritability:", mood_levels),
    "Anxiety": get_choice("Today's most extreme anxiety:", mood_levels)
}

filename = "mood_log.csv"

file_exists = False

try:
    with open(filename, 'r'):
        file_exists = True
except FileNotFoundError:
    pass

with open(filename, mode="a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=data.keys())
    if not file_exists:
        writer.writeheader()
    writer.writerow(data)

print("Mood logged successfully for", today)

df = pd.read_csv("mood_log.csv", parse_dates=["Date"])
df.set_index("Date", inplace = True)
df.replace({'None': 0, 'Mild': 1, 'Moderate': 2, 'Severe': 3}, inplace=True)

df.plot.line()
plt.title("Mood Over Time")
plt.ylabel("0 = None, 1 = Mild, 2 = Moderate, 3 = Severe")
plt.legend()
plt.tight_layout()
plt.show()