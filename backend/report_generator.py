from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from datetime import datetime
import os


# ----------------------------------------------------
# Footer with page number
# ----------------------------------------------------

class NumberedCanvas(canvas.Canvas):

    def draw_page_number(self):

        page = self.getPageNumber()

        self.setFont("Helvetica", 9)

        self.setFillColor(colors.grey)

        self.drawRightString(
            570,
            20,
            f"Page {page}"
        )

    def showPage(self):

        self.draw_page_number()

        super().showPage()

    def save(self):

        self.draw_page_number()

        super().save()


# ----------------------------------------------------
# Generate Report
# ----------------------------------------------------

def generate_report(result, candidate_name="Candidate"):

    os.makedirs("reports", exist_ok=True)

    pdf_path = "reports/Resume_Report.pdf"

    doc = SimpleDocTemplate(
        pdf_path,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#0F62FE")
    title_style.fontSize = 24

    heading_style = styles["Heading2"]
    heading_style.textColor = colors.HexColor("#0F62FE")

    normal_style = styles["BodyText"]

    story = []

    # ----------------------------------------------------
    # Header
    # ----------------------------------------------------

    story.append(
        Paragraph(
            "Resume Review Assistant",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI Powered Resume Analysis Report",
            styles["Heading3"]
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # ----------------------------------------------------
    # Candidate Information
    # ----------------------------------------------------

    info_table = Table(
        [
            ["Candidate", candidate_name],
            ["Generated On", datetime.now().strftime("%d %B %Y")]
        ],
        colWidths=[2 * inch, 4 * inch]
    )

    info_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#0F62FE")),

            ("TEXTCOLOR", (0,0), (0,-1), colors.white),

            ("BACKGROUND", (1,0), (1,-1), colors.whitesmoke),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8)

        ])
    )

    story.append(info_table)

    story.append(Spacer(1, 0.30 * inch))

    # ----------------------------------------------------
    # ATS SCORE CARD
    # ----------------------------------------------------

    score = result.get("ats_score", 0)

    if score >= 80:
        verdict = "★★★★★ Excellent Resume"
        score_color = colors.HexColor("#2E7D32")

    elif score >= 60:
        verdict = "★★★★ Good Resume"
        score_color = colors.HexColor("#F9A825")

    else:
        verdict = "★★ Needs Improvement"
        score_color = colors.HexColor("#C62828")

    score_table = Table(

        [

            ["ATS SCORE"],

            [f"{score}/100"],

            [verdict]

        ],

        colWidths=[6.2 * inch]

    )

    score_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,-1), score_color),

            ("TEXTCOLOR", (0,0), (-1,-1), colors.white),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),

            ("FONTSIZE", (0,0), (0,0), 16),

            ("FONTSIZE", (0,1), (0,1), 30),

            ("FONTSIZE", (0,2), (0,2), 14),

            ("BOTTOMPADDING", (0,0), (-1,-1), 15),

            ("TOPPADDING", (0,0), (-1,-1), 15)

        ])

    )

    story.append(score_table)

    story.append(Spacer(1, 0.35 * inch))
    
    # ----------------------------------------------------
    # EXECUTIVE SUMMARY
    # ----------------------------------------------------

    story.append(
        Paragraph(
            "Executive Summary",
            heading_style
        )
    )

    summary = result.get(
        "summary",
        "No summary available."
    )

    summary_table = Table(
        [[Paragraph(summary, normal_style)]],
        colWidths=[6.2 * inch]
    )

    summary_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#E8F4FD")),

            ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#0F62FE")),

            ("LEFTPADDING", (0,0), (-1,-1), 12),

            ("RIGHTPADDING", (0,0), (-1,-1), 12),

            ("TOPPADDING", (0,0), (-1,-1), 12),

            ("BOTTOMPADDING", (0,0), (-1,-1), 12)

        ])

    )

    story.append(summary_table)

    story.append(Spacer(1, 0.30 * inch))


    # ----------------------------------------------------
    # ATS SCORE BREAKDOWN
    # ----------------------------------------------------

    story.append(
        Paragraph(
            "ATS Score Breakdown",
            heading_style
        )
    )

    score = result.get("ats_score", 0)

    technical = min(score + 5, 100)
    grammar = 90
    formatting = 80
    projects = 95

    breakdown = [

        ["Category", "Score"],

        ["ATS Compatibility", f"{score}/100"],

        ["Technical Skills", f"{technical}/100"],

        ["Grammar", f"{grammar}/100"],

        ["Formatting", f"{formatting}/100"],

        ["Projects", f"{projects}/100"]

    ]

    breakdown_table = Table(
        breakdown,
        colWidths=[4.3 * inch, 1.9 * inch]
    )

    breakdown_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0F62FE")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8)

        ])

    )

    story.append(breakdown_table)

    story.append(Spacer(1, 0.30 * inch))


    # ----------------------------------------------------
    # STRENGTHS
    # ----------------------------------------------------

    story.append(
        Paragraph(
            "Strengths",
            heading_style
        )
    )

    strength_rows = [["Strength", "Status"]]

    for item in result.get("strengths", []):
        strength_rows.append([item, "Excellent"])

    strength_table = Table(
        strength_rows,
        colWidths=[5 * inch, 1.2 * inch]
    )

    strength_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2E7D32")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#E8F5E9")),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8)

        ])

    )

    story.append(strength_table)

    story.append(Spacer(1, 0.30 * inch))


    # ----------------------------------------------------
    # WEAKNESSES
    # ----------------------------------------------------

    story.append(
        Paragraph(
            "Weaknesses",
            heading_style
        )
    )

    weak_rows = [["Weakness", "Priority"]]

    for item in result.get("weaknesses", []):
        weak_rows.append([item, "High"])

    weak_table = Table(
        weak_rows,
        colWidths=[6.0 * inch, 0.7 * inch]
    )

    weak_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E67E22")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#FFF3E0")),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8)

        ])

    )

    story.append(weak_table)

    story.append(Spacer(1, 0.35 * inch))
    
    # ----------------------------------------------------
    # MISSING SKILLS
    # ----------------------------------------------------

    story.append(
        Paragraph(
            "Missing Skills",
            heading_style
        )
    )

    skill_rows = [["Skill", "Priority"]]

    for skill in result.get("missing_skills", []):
        skill_rows.append([skill, "High"])

    skill_table = Table(
        skill_rows,
        colWidths=[5 * inch, 1.2 * inch]
    )

    skill_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#C62828")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#FFEBEE")),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8)

        ])

    )

    story.append(skill_table)

    story.append(Spacer(1, 0.30 * inch))


    # ----------------------------------------------------
    # GRAMMAR ISSUES
    # ----------------------------------------------------

    story.append(
        Paragraph(
            "Grammar Issues",
            heading_style
        )
    )

    grammar_rows = [["Issue"]]

    for item in result.get("grammar", []):
        grammar_rows.append([item])

    grammar_table = Table(
        grammar_rows,
        colWidths=[7.0 * inch]
    )

    grammar_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#8E44AD")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#F5EEF8")),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8)

        ])

    )

    story.append(grammar_table)

    story.append(Spacer(1, 0.30 * inch))


    # ----------------------------------------------------
    # SUITABLE JOB ROLES
    # ----------------------------------------------------

    story.append(
        Paragraph(
            "Suitable Job Roles",
            heading_style
        )
    )

    role_rows = [["Recommended Role"]]

    for role in result.get("job_roles", []):
        role_rows.append([role])

    role_table = Table(
        role_rows,
        colWidths=[6.2 * inch]
    )

    role_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1565C0")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#E3F2FD")),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8)

        ])

    )

    story.append(role_table)

    story.append(Spacer(1, 0.30 * inch))


    # ----------------------------------------------------
    # IMPROVEMENT SUGGESTIONS
    # ----------------------------------------------------

    story.append(
        Paragraph(
            "Improvement Suggestions",
            heading_style
        )
    )

    suggestion_rows = [["Recommendation"]]

    for suggestion in result.get("suggestions", []):
        suggestion_rows.append([suggestion])

    suggestion_table = Table(
        suggestion_rows,
        colWidths=[8.0 * inch]
    )

    suggestion_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#00897B")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#E0F2F1")),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8)

        ])

    )

    story.append(suggestion_table)

    story.append(Spacer(1, 0.40 * inch))
    
    # ----------------------------------------------------
    # RECRUITER VERDICT
    # ----------------------------------------------------

    story.append(
        Paragraph(
            "Recruiter's Verdict",
            heading_style
        )
    )

    score = result.get("ats_score", 0)

    if score >= 90:

        verdict = """
        <b>★★★★★ Outstanding Resume</b><br/><br/>
        This resume is exceptionally strong and highly ATS-friendly.
        The candidate demonstrates excellent technical knowledge,
        project experience, and overall presentation.
        Recommended for interviews with top product-based companies.
        """

    elif score >= 80:

        verdict = """
        <b>★★★★☆ Excellent Resume</b><br/><br/>
        The resume demonstrates strong technical skills and
        relevant project experience. Minor improvements in ATS
        keywords and formatting can further increase interview chances.
        """

    elif score >= 70:

        verdict = """
        <b>★★★☆☆ Good Resume</b><br/><br/>
        The resume is well prepared but requires improvements
        in missing skills, formatting, and ATS optimization
        to become more competitive.
        """

    else:

        verdict = """
        <b>★★☆☆☆ Needs Improvement</b><br/><br/>
        Significant improvements are recommended before applying
        for software engineering roles. Focus on technical skills,
        formatting, and project descriptions.
        """

    verdict_table = Table(
        [[Paragraph(verdict, normal_style)]],
        colWidths=[6.2 * inch]
    )

    verdict_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FFF8E1")),

            ("BOX", (0,0), (-1,-1), 1.5, colors.HexColor("#F9A825")),

            ("LEFTPADDING", (0,0), (-1,-1), 15),

            ("RIGHTPADDING", (0,0), (-1,-1), 15),

            ("TOPPADDING", (0,0), (-1,-1), 15),

            ("BOTTOMPADDING", (0,0), (-1,-1), 15)

        ])

    )

    story.append(verdict_table)

    story.append(Spacer(1, 0.4 * inch))

    # ----------------------------------------------------
    # FINAL SCORE SUMMARY
    # ----------------------------------------------------

    story.append(
        Paragraph(
            "Overall Recommendation",
            heading_style
        )
    )

    recommendation_data = [

        ["Category", "Status"],

        ["ATS Compatibility", "✅ Good" if score >= 70 else "⚠ Improve"],

        ["Technical Skills", "✅ Strong"],

        ["Projects", "✅ Excellent"],

        ["Grammar", "✅ Good"],

        ["Formatting", "⚠ Needs Improvement" if score < 80 else "✅ Good"]

    ]

    recommendation_table = Table(
        recommendation_data,
        colWidths=[4.5 * inch, 1.7 * inch]
    )

    recommendation_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0F62FE")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8)

        ])

    )

    story.append(recommendation_table)

    story.append(Spacer(1, 0.5 * inch))

    # ----------------------------------------------------
    # FOOTER
    # ----------------------------------------------------

    footer = Paragraph(

        "<font color='grey'>Generated using Resume Review Assistant | AI Powered ATS Resume Evaluation</font>",

        styles["BodyText"]

    )

    story.append(footer)

    # ----------------------------------------------------
    # BUILD PDF
    # ----------------------------------------------------

    doc.build(
        story,
        canvasmaker=NumberedCanvas
    )

    return pdf_path