import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

# =====================================
# LOAD FILE
# =====================================

file_path = "Updated_sem3 (1).xlsx"
df = pd.read_excel(file_path, header=4)

df.columns = df.columns.astype(str).str.strip()
df = df[df["Student Name"].notna()]
df["SGPA"] = pd.to_numeric(df["SGPA"], errors="coerce")

# =====================================
# CREATE PDF
# =====================================

pdf_file = "Semester_Result_Analysis_Report.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4)
elements = []
styles = getSampleStyleSheet()

# Title
title = styles["Heading1"]
title.alignment = TA_CENTER
elements.append(Paragraph("Semester Result Analysis Report", title))
elements.append(Spacer(1, 0.3 * inch))

# =====================================
# SUBJECT TOPPERS
# =====================================

elements.append(Paragraph("<b>SUBJECT TOPPERS</b>", styles["Heading2"]))
elements.append(Spacer(1, 0.2 * inch))

columns = df.columns.tolist()

for i in range(len(columns)):
    col = columns[i]

    if any(code in col for code in ["CE", "OE", "MD", "NC", "EE", "VE"]):
        try:
            ext_col = columns[i+1]
            int_col = columns[i+3]

            ext = pd.to_numeric(df[ext_col], errors="coerce")
            internal = pd.to_numeric(df[int_col], errors="coerce")

            total = ext.fillna(0) + internal.fillna(0)

            max_marks = total.max()
            toppers = df.loc[total == max_marks, "Student Name"]

            elements.append(Paragraph(f"<b>Subject:</b> {col}", styles["Normal"]))
            elements.append(Paragraph(f"Highest Marks: {int(max_marks)}", styles["Normal"]))
            elements.append(Paragraph(f"Topper(s): {', '.join(toppers)}", styles["Normal"]))
            elements.append(Spacer(1, 0.2 * inch))

        except:
            continue

# =====================================
# TOP 5 TOPPERS
# =====================================

elements.append(Paragraph("<b>TOP 5 OVERALL TOPPERS</b>", styles["Heading2"]))
elements.append(Spacer(1, 0.2 * inch))

top5 = df.sort_values(by="SGPA", ascending=False).head(5)

for _, row in top5.iterrows():
    elements.append(Paragraph(
        f"{row['Student Name']}  -  SGPA: {round(row['SGPA'],2)}",
        styles["Normal"]
    ))

elements.append(Spacer(1, 0.3 * inch))

# =====================================
# RESULT SUMMARY
# =====================================

elements.append(Paragraph("<b>RESULT SUMMARY</b>", styles["Heading2"]))
elements.append(Spacer(1, 0.2 * inch))

total_students = len(df)
passed_students = len(df[df["Overall Pass/Fail"].str.upper() == "PASS"])
failed_students = len(df[df["Overall Pass/Fail"].str.upper() == "FAIL"])

elements.append(Paragraph(f"Total Students Appeared : {total_students}", styles["Normal"]))
elements.append(Paragraph(f"Total Students Passed   : {passed_students}", styles["Normal"]))
elements.append(Paragraph(f"Total Students Failed   : {failed_students}", styles["Normal"]))
elements.append(Spacer(1, 0.3 * inch))

# =====================================
# SGPA CLASSIFICATION
# =====================================

elements.append(Paragraph("<b>SGPA CLASSIFICATION</b>", styles["Heading2"]))
elements.append(Spacer(1, 0.2 * inch))

elements.append(Paragraph(
    f"First Class With Distinction (>=8.0): {len(df[df['SGPA'] >= 8.0])}",
    styles["Normal"]
))
elements.append(Paragraph(
    f"First Class (7.0 - 7.99): {len(df[(df['SGPA'] >= 7.0) & (df['SGPA'] < 8.0)])}",
    styles["Normal"]
))
elements.append(Paragraph(
    f"Higher Second Class (6.0 - 6.99): {len(df[(df['SGPA'] >= 6.0) & (df['SGPA'] < 7.0)])}",
    styles["Normal"]
))
elements.append(Paragraph(
    f"Second Class (5.0 - 5.99): {len(df[(df['SGPA'] >= 5.0) & (df['SGPA'] < 6.0)])}",
    styles["Normal"]
))
elements.append(Paragraph(
    f"Pass Class (4.0 - 4.99): {len(df[(df['SGPA'] >= 4.0) & (df['SGPA'] < 5.0)])}",
    styles["Normal"]
))

elements.append(Spacer(1, 0.3 * inch))

# =====================================
# BACKLOG CALCULATION
# =====================================

df["Backlog_Count"] = 0

for i in range(len(columns)):
    col = columns[i]

    if any(code in col for code in ["CE", "OE", "MD", "NC", "EE", "VE"]):
        try:
            ext_col = columns[i+1]
            int_col = columns[i+3]

            ext = pd.to_numeric(df[ext_col], errors="coerce")
            internal = pd.to_numeric(df[int_col], errors="coerce")

            total = ext + internal
            valid_students = total.notna()

            if valid_students.sum() == 0:
                continue

            max_total = total[valid_students].max()

            if max_total > 50:
                backlog_condition = (total < 40) & valid_students
            else:
                backlog_condition = (total < 20) & valid_students

            df["Backlog_Count"] += backlog_condition.astype(int)

        except:
            continue

elements.append(Paragraph("<b>BACKLOG DISTRIBUTION</b>", styles["Heading2"]))
elements.append(Spacer(1, 0.2 * inch))

elements.append(Paragraph(f"One Backlog: {len(df[df['Backlog_Count'] == 1])}", styles["Normal"]))
elements.append(Paragraph(f"Two Backlogs: {len(df[df['Backlog_Count'] == 2])}", styles["Normal"]))
elements.append(Paragraph(f"Three Backlogs: {len(df[df['Backlog_Count'] == 3])}", styles["Normal"]))
elements.append(Paragraph(f"Four Backlogs: {len(df[df['Backlog_Count'] == 4])}", styles["Normal"]))
elements.append(Paragraph(f"More than Four Backlogs: {len(df[df['Backlog_Count'] > 4])}", styles["Normal"]))

# =====================================
# BUILD PDF
# =====================================

doc.build(elements)

print("PDF Generated Successfully:", pdf_file)
