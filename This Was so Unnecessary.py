import pdfplumber
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors

pdf_files = ["file1.pdf", "file2.pdf"]

all_totals = []

def extract_last_column_from_pdf(pdf_path):
    totals = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                df = pd.DataFrame(table)

                if df.empty:
                    continue

                last_col = df.iloc[:, -1]

                for val in last_col:
                    try:
                        num = float(val)
                        totals.append(num)
                    except:
                        continue

    return totals

# === Extract data ===
for pdf in pdf_files:
    all_totals.extend(extract_last_column_from_pdf(pdf))

data = np.array(all_totals)

# === Highest & Lowest Marks ===
highest_marks = np.max(data)
lowest_marks = np.min(data)

print(f"Highest Marks: {highest_marks}")
print(f"Lowest Marks: {lowest_marks}")

# === Stats ===
print(f"Average Marks: {np.mean(data):.2f}")

max_score = np.max(data)

# === CGPA FUNCTION (WHOLE NUMBERS) ===
def marks_to_cgpa(mark, max_score):
    if mark < 35:
        return 0  # Fail

    cgpa = 4 + ((mark - 35) / (max_score - 35)) * 6
    return int(round(min(10, max(4, cgpa))))  # whole number clamp

# Convert all
cgpa = np.array([marks_to_cgpa(m, max_score) for m in data])

print(f"Average CGPA: {np.mean(cgpa):.2f}")

# === USER INPUT ===
user_marks = float(input("Enter your marks (out of 50): "))
user_cgpa = marks_to_cgpa(user_marks, max_score)

percentile = (np.sum(data < user_marks) / len(data)) * 100

if user_marks < 35:
    print("Result: FAIL")
else:
    print(f"Your CGPA (rounded): {user_cgpa}")

print(f"You scored higher than {percentile:.2f}% of students")

# === DISCRETE GRAPH WITH ACCURATE COUNT ===

# Fix precision issue by rounding to nearest integer
data_int = np.round(data).astype(int)

marks_range = range(int(min(data_int)), int(max(data_int)) + 1)
freq = [np.sum(data_int == m) for m in marks_range]

plt.figure(figsize=(12, 6))

bars = plt.bar(marks_range, freq, color='skyblue', edgecolor='black')

# Fail cutoff
plt.axvline(35, color='red', linestyle='--', label='Fail Cutoff')

# Your marks
plt.axvline(user_marks, color='blue', linestyle='-', label='Your Marks')

# Labels
plt.title("Exact Marks Distribution (Every Mark Shown)")
plt.xlabel("Marks")
plt.ylabel("Number of Students")

plt.xticks(marks_range)

plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# === HOVER TOOLTIP ===
cursor = mplcursors.cursor(bars, hover=True)

@cursor.connect("add")
def on_add(sel):
    x = sel.target[0]
    y = sel.target[1]
    sel.annotation.set_text(f"Marks: {int(x)}\nStudents: {int(y)}")

plt.tight_layout()
plt.show()