import os
import csv
import calendar
from datetime import date, timedelta
import matplotlib.pyplot as plt

FILE = "mood_data.csv"
FIELDS = ["date", "sleep", "depressed", "elevated", "irritable", "anxiety"]
SYMPTOMS = ["depressed", "elevated", "irritable", "anxiety"]
LEVELS = ["none", "mild", "moderate", "severe"]

def load_data():
    
    data = {}
    if not os.path.exists(FILE):
        return data
    
    with open(FILE, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            d = row["date"]

            data[d] = {
                "sleep": float(row["sleep"]),
                "depressed": int(row["depressed"]),
                "elevated": int(row["elevated"]),
                "irritable": int(row["irritable"]),
                "anxiety": int(row["anxiety"]),
            }

    return data

def save_data(data):
    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()

        for dstr, entry in sorted(data.items()):
            row = {"date": dstr, **entry}
            writer.writerow(row)

def ask_level(label):
    while True:
        txt = input(f"{label} (none/mild/moderate/severe): ").strip()
        if txt in LEVELS:
            return LEVELS.index(txt)
        print("Please choose one of:", ", ".join(LEVELS))

def log_today(data):

    print("\n=== Log Today ===")
    today = date.today()
    print(f"\n--- Logging for {today} ---")

    while True:

        # sleep
        try:
            sleep = float(input("Last night’s sleep (hours): ").lower())
            break
        except ValueError:
            print("↳ please enter a number like 7.5")

    entry = {"sleep": sleep}

        # symptoms
    for s in SYMPTOMS:
        entry[s] = ask_level(f"Most extreme {s} mood")
    data[today.isoformat()] = entry
    save_data(data)
    print("✓ Entry saved!\n")

def calendar_view(data):
    today = date.today()
    year, month = today.year, today.month
    cal = calendar.monthcalendar(year, month)
    print("\n", calendar.month_name[month], year)
    print("Su Mo Tu We Th Fr Sa")

    for week in cal:
        line = ""
        for day in week:
            if day == 0:
                line += "   "
            else:
                dstr = f"{year:04d}-{month:02d}-{day:02d}"
                mark = "●" if dstr in data else " "
                line += f"{day:02d}{mark} "
        print(line.rstrip())
    print() 


def last_30_days_plot(data):

    today = date.today()
    start = today - timedelta(days=29)

    dates, sleep_vals = [], []
    rows = {s: [] for s in SYMPTOMS}

    for i in range(30):

        d = start + timedelta(days=i)
        dstr = d.isoformat()
        dates.append(d)
        entry = data.get(dstr)

        sleep_vals.append(entry["sleep"] if entry else 0)
        for s in SYMPTOMS:
            rows[s].append(entry[s] if entry else None)

    fig = plt.figure(figsize=(9, 6))
    ax1 = fig.add_subplot(211)
    ax1.bar(dates, sleep_vals)
    ax1.set_title("Sleep (hrs)")
    ax1.set_ylabel("Hours")
    ax1.set_xticks([])

    ax2 = fig.add_subplot(212)
    y_pos = {s: i for i, s in enumerate(SYMPTOMS)}
    for s in SYMPTOMS:
        sizes = [(val + 1) * 30 if val is not None else 0 for val in rows[s]]
        ax2.scatter(dates, [y_pos[s]] * 30, s=sizes, label=s.capitalize())
    ax2.set_yticks(list(y_pos.values()), [s.capitalize() for s in SYMPTOMS])
    ax2.set_xlabel("Date")
    ax2.set_xlim(min(dates), max(dates))
    ax2.set_title("Mood Levels (Dot Size = Intensity)")
    plt.tight_layout()
    plt.show()

def main():
    data = load_data()
    while True:
        print("=== Mini Mood Tracker (CSV) ===")
        print("1) Log today")
        print("2) Show calendar")
        print("3) Plot last 30 days")
        print("4) Quit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            log_today(data)
        elif choice == "2":
            calendar_view(data)
        elif choice == "3":
            last_30_days_plot(data)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("↳ please choose 1–4\n")


if __name__ == "__main__":
    main()

