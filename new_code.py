import pandas as pd
import numpy as np

# =====================================
# LOAD FILE (IMPORTANT: header=4)
# =====================================

file_path = "Updated_sem3 (1).xlsx"

df = pd.read_excel(file_path, header=4)   # ✅ FIXED

df.columns = df.columns.astype(str).str.strip()

print("Columns Loaded:\n", df.columns.tolist())

# =====================================
# BASIC CLEANING
# =====================================

# Remove empty rows
df = df[df["Student Name"].notna()]

# Convert SGPA
df["SGPA"] = pd.to_numeric(df["SGPA"], errors="coerce")

print("\n======================================")
print("RESULT ANALYSIS")
print("======================================\n")

# =====================================
# SUBJECT TOPPERS
# =====================================

print("========== SUBJECT TOPPERS ==========\n")

columns = df.columns.tolist()
subject_fail_columns = []

for i in range(len(columns)):

    col = columns[i]

    # Subject columns contain subject codes like CE124...
    if "CE" in col or "OE" in col or "MD" in col or "NC" in col:

        try:
            ext_col = columns[i+1]
            int_col = columns[i+3]
            result_col = columns[i+5]   # Result column in your layout

            ext = pd.to_numeric(df[ext_col], errors="coerce")
            internal = pd.to_numeric(df[int_col], errors="coerce")

            df["TOTAL_TEMP"] = ext.fillna(0) + internal.fillna(0)

            max_marks = df["TOTAL_TEMP"].max()

            toppers = df.loc[df["TOTAL_TEMP"] == max_marks, "Student Name"]

            print(f"Subject: {col}")
            print(f"Highest Marks: {max_marks}")
            print("Topper(s):", ", ".join(toppers))
            print("-----------------------------------")

            subject_fail_columns.append(result_col)

        except:
            continue


# =====================================
# TOP 5 TOPPERS
# =====================================

print("\n========== TOP 5 TOPPERS ==========\n")

top5 = df.sort_values(by="SGPA", ascending=False).head(5)
print(top5[["Student Name", "SGPA"]])


# =====================================
# RESULT SUMMARY
# =====================================

print("\n========== RESULT SUMMARY ==========\n")

total_students = len(df)
passed_students = len(df[df["Overall Pass/Fail"].str.upper() == "PASS"])
failed_students = len(df[df["Overall Pass/Fail"].str.upper() == "FAIL"])

print("Total Students Appeared :", total_students)
print("Total Students Passed   :", passed_students)
print("Total Students Failed   :", failed_students)


# =====================================
# SGPA CLASSIFICATION
# =====================================

print("\n========== SGPA CLASSIFICATION ==========\n")

print("First Class With Distinction (>=8.0):", len(df[df["SGPA"] >= 8.0]))
print("First Class (>=7.0):", len(df[(df["SGPA"] >= 7.0) & (df["SGPA"] < 8.0)]))
print("Higher Second Class (>=6.0):", len(df[(df["SGPA"] >= 6.0) & (df["SGPA"] < 7.0)]))
print("Second Class (>=5.0):", len(df[(df["SGPA"] >= 5.0) & (df["SGPA"] < 6.0)]))
print("Pass Class (>=4.0):", len(df[(df["SGPA"] >= 4.0) & (df["SGPA"] < 5.0)]))


# =====================================
# BACKLOG ANALYSIS
# =====================================

# =====================================
# BACKLOG ANALYSIS (FINAL VERSION)
# =====================================

print("\n========== BACKLOG ANALYSIS ==========\n")

df["Backlog_Count"] = 0

columns = df.columns.tolist()

for i in range(len(columns)):

    col = columns[i]

    # Detect subject column (contains subject code)
    if any(code in col for code in ["CE", "OE", "MD", "NC", "EE", "VE"]):

        try:
            ext_col = columns[i+1]
            int_col = columns[i+3]

            ext = pd.to_numeric(df[ext_col], errors="coerce")
            internal = pd.to_numeric(df[int_col], errors="coerce")

            total = ext + internal

            # 🔹 Ignore students where both marks are blank
            valid_students = total.notna()

            if valid_students.sum() == 0:
                continue

            max_total = total[valid_students].max()

            if max_total > 50:
                # Out of 100 subject
                backlog_condition = (total < 40) & valid_students
            else:
                # Out of 50 subject
                backlog_condition = (total < 20) & valid_students

            df["Backlog_Count"] += backlog_condition.astype(int)

        except:
            continue


# Backlog Distribution
print("One Backlog:", len(df[df["Backlog_Count"] == 1]))
print("Two Backlog:", len(df[df["Backlog_Count"] == 2]))
print("Three Backlog:", len(df[df["Backlog_Count"] == 3]))
print("Four Backlog:", len(df[df["Backlog_Count"] == 4]))
print("More than Four Backlog:", len(df[df["Backlog_Count"] > 4]))
