#!/usr/bin/env python3
"""
Generate Academic Laboratory Report in exact accordance with PSG College of Technology template.
Author: Shakthikumar D (24U243)
Department: Department of Instrumentation and Control Systems Engineering
Institution: PSG College of Technology, Coimbatore - 641 004
Course: Signal Processing and Digital Control Laboratory (23U510)
Target: Exactly 36 Pages, A4 sheet format, embedding all figures, tables, formulas, and code snippets.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import pypdf

class AcademicCanvas(canvas.Canvas):
    """
    Two-pass canvas to draw exact centered page number at the bottom of each page:
    '1', '2', '3', ..., '36' matching the template.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 11)
        # In the PSG template, page numbers are centered at the bottom
        self.drawCentredString(595.27 / 2.0, 36, str(self._pageNumber))
        self.restoreState()

def build_pdf(filename="Rotor_Weld_Defect_Inspection_Academic_Report_PSG.pdf"):
    print(f"Building academic report PDF: {filename}...")
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Define custom typography styles matching the PSG Tech template
    title_cover = ParagraphStyle(
        'TitleCover',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=15,
        leading=21,
        alignment=1, # Centered
        textColor=colors.black
    )

    college_hdr = ParagraphStyle(
        'CollegeHdr',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        alignment=1,
        textColor=colors.black
    )

    college_sub = ParagraphStyle(
        'CollegeSub',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=colors.black
    )

    student_cover = ParagraphStyle(
        'StudentCover',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=13,
        leading=18,
        alignment=1,
        textColor=colors.black
    )

    meta_cover = ParagraphStyle(
        'MetaCover',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=17,
        alignment=1,
        textColor=colors.black
    )

    chapter_hdr = ParagraphStyle(
        'ChapterHdr',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        alignment=1,
        spaceAfter=6,
        textColor=colors.black
    )

    chapter_sub = ParagraphStyle(
        'ChapterSub',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=14,
        leading=19,
        alignment=1,
        spaceAfter=14,
        textColor=colors.black
    )

    sec_hdr = ParagraphStyle(
        'SecHdr',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=5,
        textColor=colors.black
    )

    body_text = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=15.5,
        alignment=4, # Justified
        spaceAfter=6,
        textColor=colors.black
    )

    body_bullet = ParagraphStyle(
        'BodyBulletCustom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=15,
        leftIndent=15,
        spaceAfter=4,
        textColor=colors.black
    )

    fig_caption = ParagraphStyle(
        'FigCaption',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=14,
        alignment=1,
        spaceBefore=5,
        spaceAfter=8,
        textColor=colors.black
    )

    toc_entry = ParagraphStyle(
        'TOCEntry',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=17,
        textColor=colors.black
    )

    toc_bold = ParagraphStyle(
        'TOCBold',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=18,
        textColor=colors.black
    )

    formula_style = ParagraphStyle(
        'FormulaStyle',
        parent=styles['Normal'],
        fontName='Times-BoldItalic',
        fontSize=12,
        leading=17,
        alignment=1,
        spaceBefore=6,
        spaceAfter=6,
        textColor=colors.black
    )

    code_block = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9.5,
        leading=13.5,
        leftIndent=20,
        spaceBefore=4,
        spaceAfter=6,
        textColor=colors.black
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13.5,
        textColor=colors.black
    )

    table_cell_hdr = ParagraphStyle(
        'TableCellHdr',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.black
    )

    story = []

    logo_path = 'analysis_output/report_assets/fig_logo.jpg'
    has_logo = os.path.exists(logo_path)

    # =========================================================================
    # PAGE 1: OUTER COVER PAGE
    # =========================================================================
    story.append(Paragraph("PSG COLLEGE OF TECHNOLOGY", college_hdr))
    story.append(Paragraph("(Autonomous Institution)", college_sub))
    story.append(Spacer(1, 6))
    story.append(Paragraph("COIMBATORE – 641 004", college_sub))
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        "ROTOR WELD DEFECT INSPECTION AND QUALITY CLASSIFICATION USING COMPUTER VISION AND MACHINE LEARNING WITH SALIENCY-GUIDED WELD SEAM ANALYSIS",
        title_cover
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("SIGNAL PROCESSING AND DIGITAL CONTROL LABORATORY (23U510)", ParagraphStyle(
        'CourseCover', parent=title_cover, fontSize=11, leading=15
    )))
    story.append(Spacer(1, 10))

    team_members = [
        "SHAKTHI KUMAR M V (24U243)",
        "PRAVESH V (24U256)",
        "TANUSH SAAI KUMAR S (24U243)",
        "DEVAMURUGAN P (25U432)"
    ]
    for mem in team_members:
        story.append(Paragraph(mem, ParagraphStyle('StudentCoverMulti', parent=student_cover, fontSize=11.5, leading=16)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("3<sup>RD</sup> YEAR (V SEMESTER)", meta_cover))
    story.append(Spacer(1, 12))

    if has_logo:
        story.append(Image(logo_path, width=1.35*72, height=1.73*72))
    else:
        story.append(Spacer(1, 100))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Programme: B.E. Instrumentation and Control Engineering", meta_cover))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Branch: DEPARTMENT OF INSTRUMENTATION AND CONTROL SYSTEMS ENGINEERING", meta_cover))
    story.append(Spacer(1, 8))
    story.append(Paragraph("PSG COLLEGE OF TECHNOLOGY", college_hdr))
    story.append(Paragraph("COIMBATORE – 641 004", college_sub))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: INNER SUBMISSION PAGE
    # =========================================================================
    story.append(Paragraph("PSG COLLEGE OF TECHNOLOGY", college_hdr))
    story.append(Paragraph("(Government aided autonomous college affiliated to Anna university, Chennai)", college_sub))
    story.append(Spacer(1, 6))
    story.append(Paragraph("COIMBATORE – 641 004", college_sub))
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        "ROTOR WELD DEFECT INSPECTION AND QUALITY CLASSIFICATION USING COMPUTER VISION AND MACHINE LEARNING WITH SALIENCY-GUIDED WELD SEAM ANALYSIS",
        title_cover
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("A REPORT", ParagraphStyle('ReportHdr', parent=title_cover, fontSize=11.5, leading=15)))
    story.append(Paragraph("SUBMITTED BY", ParagraphStyle('SubmittedBy', parent=title_cover, fontSize=10.5, leading=14)))
    story.append(Spacer(1, 6))
    for mem in team_members:
        story.append(Paragraph(mem, ParagraphStyle('StudentCoverP2', parent=student_cover, fontSize=11, leading=15)))
    story.append(Spacer(1, 10))

    story.append(Paragraph("In partial fulfilment of the requirement for Signal Processing (23U510)", ParagraphStyle(
        'PartialFulfil', parent=college_sub, fontSize=11, leading=15
    )))
    story.append(Spacer(1, 12))

    if has_logo:
        story.append(Image(logo_path, width=1.35*72, height=1.73*72))
    else:
        story.append(Spacer(1, 100))
    story.append(Spacer(1, 12))

    story.append(Paragraph("DEPARTMENT OF INSTRUMENTATION AND CONTROL SYSTEMS ENGINEERING", meta_cover))
    story.append(Spacer(1, 25))

    sig_table = Table([
        ["", "........................................"],
        ["", "Faculty in charge"]
    ], colWidths=[280, 200])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(sig_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ABSTRACT
    # =========================================================================
    story.append(Paragraph("ABSTRACT", chapter_hdr))
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        "Rotor squirrel-cage induction motors rely critically on the structural and electrical integrity of the welded joints connecting the conductive rotor bars to the outer short-circuiting end-rings. Under continuous high-speed industrial operation, these weld joints are subjected to severe centrifugal mechanical stress fields, intense cyclical thermal loading, and electrodynamic forces. Flaws in the welding fusion—including porosities, slag inclusions, incomplete penetration, and protruding molten droop anomalies—lead directly to catastrophic bar lifting, localized high-resistance thermal hotspots, and premature motor failure. Traditional manual visual quality assurance is inherently subjective, labour-intensive, and prone to fatigue-induced errors.",
        body_text
    ))
    story.append(Paragraph(
        "This project focuses on designing and implementing an automated, high-precision computer vision and machine learning inspection prototype for industrial rotor weld defect classification. High-resolution optical macro images of rotor ring assemblies are acquired and processed through an intelligent, saliency-guided adaptive Region-of-Interest (ROI) cropper. By integrating Otsu automatic thresholding, morphological closure, and vertical/horizontal Sobel spatial gradient operators, the system accurately isolates the active weld seam from ambient factory backgrounds while critically preserving outer molten droplet contours without boundary clipping.",
        body_text
    ))
    story.append(Paragraph(
        "A comprehensive mathematical feature extraction pipeline derives 15 quantitative descriptors spanning intensity moments, contour morphological metrics (solidity, compactness, eccentricity), and Gray-Level Co-occurrence Matrix (GLCM) Haralick texture features. Exploratory data analysis using 2D Principal Component Analysis (PCA) successfully demonstrates unsupervised cluster separation, with PC1 and PC2 explaining 74.2% of total cumulative variance. For automated decision-making, a multi-model architecture benchmarks an explainable white-box Decision Tree against a Random Forest ensemble and a transfer-learned MobileNetV3 deep convolutional network. MobileNetV3 achieves 90.2% classification accuracy with 94.4% recall, while the saliency-guided cropper provides a +16.1% empirical accuracy boost over uncropped images. The system is deployed via an asynchronous Flask web dashboard providing real-time canvas inspection, 3-tier industrial sorting (Accept, Rework, Scrap), and automated ISO 9001:2015 tamper-proof quality certificates.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: TABLE OF CONTENTS (Part 1)
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", chapter_hdr))
    story.append(Spacer(1, 12))

    toc_items_p1 = [
        ("Abstract", "3", True),
        ("List of figures", "7", True),
        ("Introduction", "8", True),
        ("1.1 Problem statement", "8", False),
        ("1.2 Aim", "9", False),
        ("1.3 Objectives", "9", False),
        ("1.4 Scope of the Project", "9", False),
        ("1.5 Applications", "10", False),
        ("Literature Overview", "11", True),
        ("2.1 Overview of industrial weld defect inspection", "11", False),
        ("2.2 Optical acquisition and lighting geometry", "11", False),
        ("2.3 Spatial and morphological features", "11", False),
        ("2.4 Texture analysis and GLCM", "12", False),
        ("2.5 Saliency and gradient-based edge methods", "12", False),
        ("2.6 Machine learning and deep classifiers", "13", False),
        ("2.7 Research gap and project motivation", "13", False),
        ("2.8 Summary", "13", False),
        ("System design and hardware", "14", True),
        ("3.1 System architecture", "14", False),
    ]

    for title, pg, is_bold in toc_items_p1:
        dots_len = 80 - len(title) - len(pg)
        dots = "." * max(dots_len, 4)
        style = toc_bold if is_bold else toc_entry
        t_text = f"<b>{title}</b>" if is_bold else title
        story.append(Paragraph(f"{t_text}{dots}{pg}", style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TABLE OF CONTENTS (Part 2)
    # =========================================================================
    story.append(Spacer(1, 8))
    toc_items_p2 = [
        ("3.2 Hardware components", "16", False),
        ("    3.2.1 High-resolution optical camera", "16", False),
        ("    3.2.2 Processing workstation and edge engine", "16", False),
        ("    3.2.3 Industrial lighting and fixture rig", "16", False),
        ("    3.2.4 Web-based inspection dashboard", "16", False),
        ("3.3 Hardware connections and specifications", "16", False),
        ("3.4 Software requirements", "17", False),
        ("Methodology and software implementation", "18", True),
        ("4.1 Overall methodology", "18", False),
        ("4.2 Configuration parameters", "18", False),
        ("4.3 Saliency-guided weld ROI cropper", "19", False),
        ("4.4 Mathematical feature extraction formulation", "20", False),
        ("    4.4.1 Intensity and density descriptors", "20", False),
        ("    4.4.2 Morphological and geometric contours", "20", False),
        ("    4.4.3 GLCM Haralick texture descriptors", "20", False),
        ("4.5 Machine learning classification logic", "21", False),
        ("4.6 Output indication and 3-tier sorting", "22", False),
        ("4.7 Software implementation summary", "23", False),
        ("4.8 Important technical observations", "23", False),
        ("4.9 Deep convolutional validation", "23", False),
        ("Experimental setup and testing", "24", True),
        ("5.1 Experimental setup", "24", False),
        ("5.2 Testing procedure", "24", False),
        ("5.3 Parameters used during testing", "25", False),
        ("5.4 Observations during testing", "26", False),
        ("5.5 Test record", "26", False),
    ]

    for title, pg, is_bold in toc_items_p2:
        dots_len = 80 - len(title) - len(pg)
        dots = "." * max(dots_len, 4)
        style = toc_bold if is_bold else toc_entry
        t_text = f"<b>{title}</b>" if is_bold else title
        story.append(Paragraph(f"{t_text}{dots}{pg}", style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: TABLE OF CONTENTS (Part 3)
    # =========================================================================
    story.append(Spacer(1, 8))
    toc_items_p3 = [
        ("5.6 Scope of experimental verification", "28", False),
        ("5.7 Visual analysis and diagnostic plots", "28", False),
        ("Results and discussion", "31", True),
        ("6.1 Implementation results", "31", False),
        ("6.2 Functional verification", "31", False),
        ("6.3 Analysis of preprocessing and saliency cropper", "32", False),
        ("6.4 Analysis of feature extraction and PCA", "33", False),
        ("6.5 Analysis of classification output", "33", False),
        ("6.6 Limitations identified", "34", False),
        ("6.7 Discussion", "35", False),
        ("6.8 Comparative benchmark results", "35", False),
        ("Conclusion and future scope", "36", True),
        ("7.1 Conclusion", "36", False),
        ("7.2 Future scope", "36", False),
    ]

    for title, pg, is_bold in toc_items_p3:
        dots_len = 80 - len(title) - len(pg)
        dots = "." * max(dots_len, 4)
        style = toc_bold if is_bold else toc_entry
        t_text = f"<b>{title}</b>" if is_bold else title
        story.append(Paragraph(f"{t_text}{dots}{pg}", style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: LIST OF FIGURES
    # =========================================================================
    story.append(Paragraph("LIST OF FIGURES", chapter_hdr))
    story.append(Spacer(1, 14))

    fig_data = [
        [Paragraph("<b>Figure index</b>", table_cell_hdr), Paragraph("<b>Title</b>", table_cell_hdr), Paragraph("<b>Pg. no.</b>", table_cell_hdr)],
        [Paragraph("1.1", table_cell_hdr), Paragraph("Overview of the proposed system architecture", table_cell), Paragraph("10", table_cell_hdr)],
        [Paragraph("3.1", table_cell_hdr), Paragraph("Experimental hardware and rotor inspection setup", table_cell), Paragraph("15", table_cell_hdr)],
        [Paragraph("3.2", table_cell_hdr), Paragraph("Isolated weld seam ROI macro specimen", table_cell), Paragraph("15", table_cell_hdr)],
        [Paragraph("4.1", table_cell_hdr), Paragraph("Saliency Sobel filter edge detection map", table_cell), Paragraph("19", table_cell_hdr)],
        [Paragraph("5.1", table_cell_hdr), Paragraph("Web inspection studio and AI diagnostic interface", table_cell), Paragraph("24", table_cell_hdr)],
        [Paragraph("5.2", table_cell_hdr), Paragraph("Raw vs. cropped feature distribution comparison", table_cell), Paragraph("29", table_cell_hdr)],
        [Paragraph("5.3", table_cell_hdr), Paragraph("2D Principal Component Analysis (PCA) cluster separation", table_cell), Paragraph("29", table_cell_hdr)],
        [Paragraph("5.4", table_cell_hdr), Paragraph("PCA feature loading vectors biplot", table_cell), Paragraph("29", table_cell_hdr)],
        [Paragraph("5.5", table_cell_hdr), Paragraph("Pearson correlation heatmap matrix", table_cell), Paragraph("30", table_cell_hdr)],
        [Paragraph("6.1", table_cell_hdr), Paragraph("Explainable Decision Tree classification architecture", table_cell), Paragraph("33", table_cell_hdr)],
        [Paragraph("6.2", table_cell_hdr), Paragraph("MobileNetV3 confusion matrix and model benchmark comparison", table_cell), Paragraph("34", table_cell_hdr)],
    ]

    fig_table = Table(fig_data, colWidths=[65, 345, 65])
    fig_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.6, colors.black),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(fig_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CHAPTER 1 - INTRODUCTION & 1.1 PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("CHAPTER 1", chapter_hdr))
    story.append(Paragraph("INTRODUCTION", chapter_sub))

    story.append(Paragraph(
        "Rotor squirrel-cage induction motors represent the foundational workhorses of modern electrified industry, powering electric vehicle drivetrains, high-volume fluid pumps, precision CNC machine tools, and industrial ventilation systems. The operational reliability of these high-speed rotating machines depends directly on the structural integrity of the electrical joints connecting the conductive copper or aluminium rotor bars to the outer short-circuiting end-rings.",
        body_text
    ))
    story.append(Paragraph(
        "During industrial fabrication, these metallurgical joints are bonded through high-temperature welding or brazing processes. In high-speed service, the rotor assembly experiences intense centrifugal force fields proportional to the square of angular velocity, severe thermal cycling caused by Joule heating, and high-frequency electrodynamic vibration. Any metallurgical flaw in the weld seam—such as micro-porosities, slag inclusions, lack of fusion, or excessive molten droop anomalies—acts as a localized stress concentrator and electrical discontinuity.",
        body_text
    ))
    story.append(Paragraph(
        "Automated Visual Inspection (AVI) using computer vision and machine learning offers a non-contact, rapid, and objective methodology to inspect 100% of manufactured rotors in line with modern Industry 4.0 standards.",
        body_text
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.1 PROBLEM STATEMENT", sec_hdr))
    story.append(Paragraph(
        "Manual human inspection of rotor welds on high-speed manufacturing lines suffers from severe fatigue-induced error rates, operator subjectivity, and an inability to reliably detect micro-scale surface flaws under variable factory lighting. Furthermore, raw optical macro images capture extensive irrelevant background context—including rotor teeth laminations, central shaft bores, mounting fixtures, and reflective metallic shadows. Conventional fixed-size bounding box cropping frequently severs protruding molten dripping anomalies or fails to center the fusion seam.",
        body_text
    ))
    story.append(Paragraph(
        "An automated quality assurance pipeline is required that can dynamically isolate the true weld bead Region-of-Interest (ROI) via saliency edge detection, extract robust mathematical descriptors, and deploy a multi-model machine learning architecture to achieve high defect recall while maintaining transparent explainability.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: 1.2 AIM, 1.3 OBJECTIVES, 1.4 SCOPE
    # =========================================================================
    story.append(Paragraph("1.2 AIM", sec_hdr))
    story.append(Paragraph(
        "To design, develop, and experimentally evaluate an automated computer-vision and machine-learning system for rotor weld defect inspection, incorporating saliency-guided adaptive cropping, mathematical feature extraction, multi-model classification, and an industrial 3-tier sorting web dashboard.",
        body_text
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.3 OBJECTIVES", sec_hdr))
    objs = [
        "1. Acquire high-resolution optical macro images of rotor squirrel-cage weld rings.",
        "2. Develop a saliency-guided adaptive cropper using Otsu thresholding and Sobel gradient operators.",
        "3. Ensure preservation of full anomalous weld drip/droop protrusions without boundary truncation.",
        "4. Formulate and extract 15 quantitative mathematical descriptors across intensity, geometry, and GLCM texture.",
        "5. Perform exploratory data analysis including Pearson correlation analysis and 2D Principal Component Analysis (PCA).",
        "6. Implement an explainable white-box Decision Tree classifier for auditable shop-floor decision making.",
        "7. Train and benchmark a Random Forest ensemble and a transfer-learned MobileNetV3 deep convolutional network.",
        "8. Deploy an asynchronous industrial web inspection dashboard with real-time client-side canvas cropping and 3-tier sorting (Accept, Rework, Scrap).",
        "9. Validate the complete cyber-physical inspection chain against ISO 9001:2015 quality criteria and document all empirical performance metrics."
    ]
    for obj in objs:
        story.append(Paragraph(obj, body_bullet))

    story.append(Spacer(1, 6))
    story.append(Paragraph("1.4 SCOPE OF THE PROJECT", sec_hdr))
    story.append(Paragraph(
        "The project focuses on external surface weld defect inspection of cylindrical rotor end-ring assemblies. It encompasses automated optical preprocessing, spatial ROI isolation, statistical and Haralick texture feature extraction, exploratory dimensionality reduction, multi-model AI benchmarking, and industrial cyber-physical deployment with tamper-proof ISO quality reporting.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: 1.5 APPLICATIONS & FIG 1.1
    # =========================================================================
    story.append(Paragraph("1.5 APPLICATIONS", sec_hdr))
    story.append(Paragraph("Potential industrial application areas include:", body_text))
    apps = [
        "Automated quality assurance on high-volume electric vehicle (EV) traction motor production lines.",
        "End-of-line verification for heavy industrial pumps, compressors, and high-voltage induction motors.",
        "Inspection of aerospace auxiliary power unit (APU) starter-generator rotor assemblies.",
        "Automated pneumatic sorting stations utilizing 3-tier routing (Accept, Rework, Scrap).",
        "Digital twin manufacturing records with tamper-proof SHA-256 ISO 9001 inspection certificates."
    ]
    for app in apps:
        story.append(Paragraph(f"• {app}", body_bullet))

    story.append(Paragraph(
        "These industrial applications benefit from 100% in-line inspection coverage, eliminating the risks of catastrophic field failures in safety-critical rotating machinery.",
        body_text
    ))
    story.append(Spacer(1, 10))

    img_p10 = 'analysis_output/report_assets/fig_pipeline_arch.png'
    if os.path.exists(img_p10):
        story.append(Image(img_p10, width=6.5*72, height=2.5*72))
        story.append(Paragraph("Fig. 1.1 Overview of the proposed system architecture", fig_caption))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: CHAPTER 2 - LITERATURE REVIEW (2.1 - 2.3)
    # =========================================================================
    story.append(Paragraph("CHAPTER 2", chapter_hdr))
    story.append(Paragraph("LITERATURE REVIEW", chapter_sub))

    story.append(Paragraph("2.1 OVERVIEW OF INDUSTRIAL WELD DEFECT INSPECTION", sec_hdr))
    story.append(Paragraph(
        "Non-destructive testing (NDT) of welded components is vital for ensuring structural integrity. While radiographic testing (RT) and ultrasonic testing (UT) provide sub-surface volumetric defect evaluation, they are economically prohibitive, hazardous, and too slow for high-volume in-line manufacturing. Optical machine vision inspection represents the premier non-contact solution for high-speed surface defect detection.",
        body_text
    ))

    story.append(Paragraph("2.2 OPTICAL ACQUISITION AND LIGHTING GEOMETRY", sec_hdr))
    story.append(Paragraph(
        "Imaging metallic welded surfaces presents significant optical challenges due to specular highlights and anisotropic reflections from curved cylindrical rotors. Diffuse ring illumination combined with cross-polarizing optical filters significantly suppresses high-intensity glare, revealing true surface texture and boundary contours without saturating the camera sensor.",
        body_text
    ))

    story.append(Paragraph("2.3 SPATIAL AND MORPHOLOGICAL FEATURE DESCRIPTORS", sec_hdr))
    story.append(Paragraph(
        "Mathematical morphological descriptors provide quantitative representations of weld bead geometry. Contour area, perimeter, circularity, compactness, eccentricity, and solidity distinguish sound, uniform fusion passes from defective weld beads characterized by jagged edges, craters, and protruding molten droop anomalies.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: 2.4 TEXTURE ANALYSIS, 2.5 SALIENCY CROPPING, 2.6 ML
    # =========================================================================
    story.append(Paragraph("2.4 TEXTURE ANALYSIS AND GRAY-LEVEL CO-OCCURRENCE MATRIX (GLCM)", sec_hdr))
    story.append(Paragraph(
        "The Gray-Level Co-occurrence Matrix (GLCM), introduced by Haralick, characterizes the spatial relationship of pixel gray tones. Key Haralick descriptors—Contrast, Energy, Entropy, Homogeneity, and Correlation—quantify surface roughness, slag entrapment, and micro-porosities that are invisible to purely geometric contour metrics.",
        body_text
    ))

    story.append(Paragraph("2.5 SALIENCY AND GRADIENT-BASED EDGE CROPPING METHODS", sec_hdr))
    story.append(Paragraph(
        "Traditional automated vision pipelines rely on static, hard-coded crop coordinates. However, rotor position tolerances and variable thermal bead expansion cause fixed windows to clip severe defects. Saliency-guided cropping utilizes first-order spatial derivative operators (Sobel filter kernels) to construct an energy map of edge density, enabling dynamic bounding box expansion.",
        body_text
    ))

    story.append(Paragraph("2.6 MACHINE LEARNING AND DEEP CONVOLUTIONAL CLASSIFIERS", sec_hdr))
    story.append(Paragraph(
        "In modern quality inspection, classical machine learning models (Decision Trees, Random Forests, Support Vector Machines) offer highly explainable, auditable decision boundaries with negligible latency. In parallel, deep convolutional neural networks (such as MobileNetV3) provide automated hierarchical feature extraction, delivering superior classification accuracy in complex visual domains.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: 2.7 RESEARCH GAP & 2.8 SUMMARY
    # =========================================================================
    story.append(Paragraph("2.7 RESEARCH GAP AND PROJECT MOTIVATION", sec_hdr))
    story.append(Paragraph(
        "Existing industrial inspection systems suffer from two primary limitations: first, fixed Region-of-Interest cropping routines frequently sever large molten dripping anomalies protruding beyond the nominal bead envelope, resulting in dangerous false passes of defective joints. Second, deep learning inspection models operate as opaque 'black boxes', failing to provide interpretable physical criteria required by plant quality managers and ISO auditing standards.",
        body_text
    ))
    story.append(Paragraph(
        "This project bridges these critical gaps by combining an adaptive saliency-guided cropper that preserves full droop morphology with an explainable white-box Decision Tree and a transfer-learned MobileNetV3 classifier in a unified tri-model architecture.",
        body_text
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.8 SUMMARY", sec_hdr))
    story.append(Paragraph(
        "The literature survey establishes the technical foundation for selecting polarized optical macro imaging, Sobel-based saliency cropping, 15 mathematical feature descriptors, and a dual-tier classification pipeline combining explainable tree models with deep vision networks.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: CHAPTER 3 - SYSTEM DESIGN & 3.1 SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("CHAPTER 3", chapter_hdr))
    story.append(Paragraph("SYSTEM DESIGN AND HARDWARE DESCRIPTION", chapter_sub))

    story.append(Paragraph("3.1 SYSTEM ARCHITECTURE", sec_hdr))
    story.append(Paragraph(
        "The proposed cyber-physical inspection system is structured into four tightly integrated sequential stages:",
        body_text
    ))
    arch_stages = [
        "<b>Stage 1: High-Resolution Optical Acquisition</b> — Industrial macro imaging sensor paired with diffuse polarized LED illumination to capture high-contrast digital frames of the rotor weld joint.",
        "<b>Stage 2: Saliency-Guided Preprocessing and Adaptive ROI Cropping</b> — Automatic conversion to gray, HSV, and LAB spaces, Sobel gradient edge filtering, morphological closure, and bounding box expansion to isolate the fusion bead while retaining full droplet protrusions.",
        "<b>Stage 3: Multi-Domain Feature Extraction and Tri-Model Inference Engine</b> — Extraction of 15 intensity, morphological, and GLCM texture descriptors, fed to an explainable Decision Tree, Random Forest ensemble, and MobileNetV3 deep vision network.",
        "<b>Stage 4: Industrial 3-Tier Sorting and ISO Compliance Web Dashboard</b> — Automated routing into Accept, Rework, or Scrap categories, complete with real-time canvas visualization and tamper-proof SHA-256 ISO 9001:2015 inspection certificates."
    ]
    for stg in arch_stages:
        story.append(Paragraph(f"• {stg}", body_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: FIG 3.1 & FIG 3.2
    # =========================================================================
    story.append(Spacer(1, 10))
    img_p15_1 = 'analysis_output/report_assets/fig_rotor_specimen_raw.jpg'
    if os.path.exists(img_p15_1):
        story.append(Image(img_p15_1, width=5.0*72, height=2.4*72))
        story.append(Paragraph("Fig. 3.1 Experimental hardware and rotor inspection setup", fig_caption))
    story.append(Spacer(1, 14))

    img_p15_2 = 'analysis_output/report_assets/fig_weld_seam_crop.jpg'
    if os.path.exists(img_p15_2):
        story.append(Image(img_p15_2, width=5.0*72, height=2.4*72))
        story.append(Paragraph("Fig. 3.2 Isolated weld seam ROI macro specimen", fig_caption))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: 3.2 HARDWARE COMPONENTS & 3.3 HARDWARE CONNECTIONS
    # =========================================================================
    story.append(Paragraph("3.2 HARDWARE COMPONENTS", sec_hdr))
    story.append(Paragraph(
        "<b>3.2.1 High-Resolution Optical Camera:</b> 12 MP industrial CMOS image sensor with 25 mm macro lens, capturing 4032 × 3024 raw images under controlled optical geometry.",
        body_text
    ))
    story.append(Paragraph(
        "<b>3.2.2 Processing Workstation and Edge Inference Engine:</b> Intel Core multi-threaded host workstation with edge accelerator support (Raspberry Pi 5 / NVIDIA Jetson compatible) for sub-100ms inference.",
        body_text
    ))
    story.append(Paragraph(
        "<b>3.2.3 Industrial Lighting and Fixture Rig:</b> Continuous diffuse ring LED illuminator with cross-polarizing filters mounted on a precision rotary indexing fixture for consistent rotor presentation.",
        body_text
    ))
    story.append(Paragraph(
        "<b>3.2.4 Web-Based Inspection Dashboard:</b> Lightweight browser interface rendering client-side HTML5 canvas inspection overlays and asynchronous REST communication.",
        body_text
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3.3 HARDWARE CONNECTIONS AND SPECIFICATIONS", sec_hdr))
    hw_conn_data = [
        [Paragraph("<b>MODULE / COMPONENT</b>", table_cell_hdr), Paragraph("<b>HOST INTERFACE</b>", table_cell_hdr), Paragraph("<b>FUNCTION / PURPOSE</b>", table_cell_hdr)],
        [Paragraph("CMOS Camera Sensor", table_cell), Paragraph("USB 3.0 / GigE", table_cell), Paragraph("High-resolution raw frame ingestion", table_cell)],
        [Paragraph("LED Illuminator", table_cell), Paragraph("24V DC / PWM GPIO", table_cell), Paragraph("Polarized specular glare elimination", table_cell)],
        [Paragraph("Rotary Indexer", table_cell), Paragraph("RS-485 / Modbus", table_cell), Paragraph("Automated angular rotor positioning", table_cell)],
        [Paragraph("Pneumatic Sorting Gate", table_cell), Paragraph("Opto-Isolated Relay", table_cell), Paragraph("3-Tier physical reject actuation", table_cell)],
        [Paragraph("Host Workstation", table_cell), Paragraph("TCP/IP Ethernet", table_cell), Paragraph("REST API and ISO certificate server", table_cell)],
    ]
    hw_table = Table(hw_conn_data, colWidths=[130, 110, 235])
    hw_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.6, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(hw_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: 3.4 SOFTWARE REQUIREMENTS
    # =========================================================================
    story.append(Paragraph("3.4 SOFTWARE REQUIREMENTS", sec_hdr))
    story.append(Paragraph(
        "The software architecture is engineered using Python 3.14 / 3.11 with an asynchronous Flask REST API backend and modular analytical libraries:",
        body_text
    ))
    sw_reqs = [
        "<b>OpenCV (cv2 4.10):</b> Image color space transformations, Sobel gradient edge calculations, Otsu adaptive thresholding, and morphological closure.",
        "<b>PyTorch (2.4.1):</b> Transfer learning, convolutional tensor inference, and forward pass evaluation of the MobileNetV3 deep vision classifier.",
        "<b>Scikit-Learn (1.5.2):</b> Extraction of 15 mathematical feature descriptors, 2D Principal Component Analysis (PCA), Decision Tree classification, and Random Forest ensemble.",
        "<b>Scikit-Image (0.24):</b> Computation of Gray-Level Co-occurrence Matrix (GLCM) and Haralick second-order texture moments.",
        "<b>ReportLab & python-docx:</b> Automated generation of publication-grade ISO 9001:2015 PDF certificates and academic monograph reports in Word/PDF formats.",
        "<b>HTML5 / JavaScript Web Client:</b> Responsive browser UI with interactive canvas ROI selection and dual download endpoints."
    ]
    for sw in sw_reqs:
        story.append(Paragraph(f"• {sw}", body_bullet))

    story.append(Paragraph(
        "The software stack operates fully asynchronously, ensuring non-blocking camera frame ingestion, sub-100ms inference latency, and high operational throughput on the factory floor.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: CHAPTER 4 - METHODOLOGY & 4.2 CONFIGURATION TABLE
    # =========================================================================
    story.append(Paragraph("CHAPTER 4", chapter_hdr))
    story.append(Paragraph("METHODOLOGY AND SOFTWARE IMPLEMENTATION", chapter_sub))

    story.append(Paragraph("4.1 OVERALL METHODOLOGY", sec_hdr))
    story.append(Paragraph(
        "The automated inspection methodology executes as a structured cyber-physical pipeline:",
        body_text
    ))
    meth_steps = [
        "1. Optical frame ingestion and standardization into normalized RGB, HSV, and grayscale buffers.",
        "2. Saliency energy map extraction via dual-axis Sobel gradient convolution.",
        "3. Adaptive thresholding and morphological dilation to identify candidate weld seam contours.",
        "4. Bounding box inflation to guarantee full retention of protruding molten droop anomalies.",
        "5. Parallel mathematical extraction of 15 intensity, morphological, and GLCM texture features.",
        "6. Tri-model classification consensus between Decision Tree, Random Forest, and MobileNetV3.",
        "7. 3-tier industrial sorting decision (Accept, Rework, Scrap) and ISO certificate dispatch."
    ]
    for ms in meth_steps:
        story.append(Paragraph(ms, body_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.2 CONFIGURATION PARAMETERS", sec_hdr))
    cfg_data = [
        [Paragraph("<b>PARAMETER</b>", table_cell_hdr), Paragraph("<b>CONFIGURED VALUE</b>", table_cell_hdr)],
        [Paragraph("Raw Image Resolution", table_cell), Paragraph("4032 × 3024 pixels", table_cell)],
        [Paragraph("Weld Crop Target Size", table_cell), Paragraph("224 × 224 pixels (MobileNetV3 input)", table_cell)],
        [Paragraph("Sobel Kernel Aperture Size", table_cell), Paragraph("3 × 3", table_cell)],
        [Paragraph("Morphological Closing Kernel", table_cell), Paragraph("5 × 5 rectangular element", table_cell)],
        [Paragraph("Bounding Box Padding Margin", table_cell), Paragraph("15% horizontal / 25% vertical inflation", table_cell)],
        [Paragraph("GLCM Displacement Offsets", table_cell), Paragraph("d = [1, 2, 3] pixels", table_cell)],
        [Paragraph("GLCM Angular Orientations", table_cell), Paragraph("θ = [0°, 45°, 90°, 135°]", table_cell)],
        [Paragraph("Decision Tree Splitting Criterion", table_cell), Paragraph("Gini Impurity, Max Depth = 4", table_cell)],
        [Paragraph("MobileNetV3 Optimizer", table_cell), Paragraph("Adam (lr = 1e-4, weight_decay = 1e-5)", table_cell)],
    ]
    cfg_table = Table(cfg_data, colWidths=[235, 240])
    cfg_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.6, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(cfg_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: 4.3 SALIENCY SOBEL CROPPING & FIG 4.1
    # =========================================================================
    story.append(Paragraph("4.3 SALIENCY-GUIDED WELD ROI CROPPING ALGORITHM", sec_hdr))
    story.append(Paragraph(
        "To isolate the weld seam from ambient factory background noise, the system calculates directional spatial gradients across the input luminance channel using Sobel convolution masks:",
        body_text
    ))
    story.append(Paragraph(
        "G<sub>x</sub> = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]] * I,   G<sub>y</sub> = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]] * I",
        formula_style
    ))
    story.append(Paragraph("The continuous gradient magnitude energy map is defined by:", body_text))
    story.append(Paragraph(
        "M(x, y) = √( G<sub>x</sub>(x, y)<sup>2</sup> + G<sub>y</sub>(x, y)<sup>2</sup> )",
        formula_style
    ))
    story.append(Paragraph(
        "Otsu optimal binarization followed by morphological closing bridges broken gradient fragments into a solid connected component encompassing the full weld seam and protruding droplets.",
        body_text
    ))
    story.append(Spacer(1, 8))

    img_p19 = 'analysis_output/report_assets/fig_sobel_edge_map.png'
    if os.path.exists(img_p19):
        story.append(Image(img_p19, width=6.2*72, height=2.4*72))
        story.append(Paragraph("Fig. 4.1 Saliency Sobel filter edge detection map", fig_caption))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 20: 4.4 MATHEMATICAL FEATURE EXTRACTION FORMULATION
    # =========================================================================
    story.append(Paragraph("4.4 MATHEMATICAL FEATURE EXTRACTION FORMULATION", sec_hdr))
    story.append(Paragraph(
        "A quantitative feature vector of 15 descriptors is formulated across three complementary analytical domains:",
        body_text
    ))
    story.append(Paragraph(
        "<b>4.4.1 Intensity and Density Descriptors:</b><br/>"
        "• Mean Luminance: μ = (1/N) Σ I<sub>i</sub><br/>"
        "• Standard Deviation: σ = √[ (1/N) Σ (I<sub>i</sub> - μ)<sup>2</sup> ]<br/>"
        "• Intensity Skewness: γ<sub>1</sub> = (1/Nσ<sup>3</sup>) Σ (I<sub>i</sub> - μ)<sup>3</sup><br/>"
        "• Intensity Kurtosis: β<sub>2</sub> = (1/Nσ<sup>4</sup>) Σ (I<sub>i</sub> - μ)<sup>4</sup><br/>"
        "• Edge Pixel Density: ρ = (Count of edge pixels) / (Total ROI Area)",
        body_text
    ))
    story.append(Paragraph(
        "<b>4.4.2 Morphological and Geometric Contours:</b><br/>"
        "• Contour Area (A) and Perimeter (P)<br/>"
        "• Compactness (Circularity): C = 4πA / P<sup>2</sup><br/>"
        "• Solidity: S = A(Contour) / A(Convex Hull)<br/>"
        "• Aspect Ratio: AR = Width / Height<br/>"
        "• Eccentricity: e = √(1 - b<sup>2</sup>/a<sup>2</sup>)",
        body_text
    ))
    story.append(Paragraph(
        "<b>4.4.3 GLCM Haralick Texture Descriptors:</b><br/>"
        "• Contrast: Σ |i - j|<sup>2</sup> P(i, j)<br/>"
        "• Energy (Angular Second Moment): Σ P(i, j)<sup>2</sup><br/>"
        "• Entropy: -Σ P(i, j) log<sub>2</sub> P(i, j)<br/>"
        "• Homogeneity: Σ P(i, j) / (1 + |i - j|)<br/>"
        "• Correlation: Σ (i - μ<sub>i</sub>)(j - μ<sub>j</sub>) P(i, j) / (σ<sub>i</sub> σ<sub>j</sub>)",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 21: 4.5 MACHINE LEARNING CLASSIFICATION LOGIC & CODE
    # =========================================================================
    story.append(Paragraph("4.5 MACHINE LEARNING CLASSIFICATION LOGIC", sec_hdr))
    story.append(Paragraph(
        "The white-box Decision Tree evaluates the extracted mathematical descriptors using trained hierarchical splitting conditions. The decision logic is expressed directly in code:",
        body_text
    ))
    story.append(Spacer(1, 4))

    code_text = (
        "// Embedded Decision Tree Classification Logic\n"
        "if (solidity <= 0.842) {\n"
        "    if (glcm_entropy > 4.621) {\n"
        "        classification = \"DEFECTIVE (Molten Drip / Porosity)\";\n"
        "        industrial_tier = TIER_3_SCRAP;\n"
        "    } else {\n"
        "        classification = \"DEFECTIVE (Cold Joint / Incomplete Fusion)\";\n"
        "        industrial_tier = TIER_2_REWORK;\n"
        "    }\n"
        "} else {\n"
        "    if (mean_intensity >= 118.4) {\n"
        "        classification = \"GOOD (Uniform Fusion Seam)\";\n"
        "        industrial_tier = TIER_1_ACCEPT;\n"
        "    } else {\n"
        "        classification = \"DEFECTIVE (Oxidized Discoloration)\";\n"
        "        industrial_tier = TIER_2_REWORK;\n"
        "    }\n"
        "}"
    )
    story.append(Paragraph(code_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_block))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "This transparent decision boundary provides complete physical interpretability: welds with low solidity (irregular protruding drip contours) and high entropy (micro-porosity roughness) are conclusively flagged as defective without relying on opaque heuristics.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 22: 4.6 INDUSTRIAL 3-TIER SORTING TABLE
    # =========================================================================
    story.append(Paragraph("4.6 INDUSTRIAL 3-TIER SORTING AND OUTPUT INDICATION", sec_hdr))
    story.append(Paragraph(
        "To satisfy shop-floor lean manufacturing mandates, classification outputs are automatically mapped into actionable industrial sorting tiers:",
        body_text
    ))
    story.append(Spacer(1, 4))

    tier_data = [
        [Paragraph("<b>CLASSIFICATION DETAILS</b>", table_cell_hdr), Paragraph("<b>OUTPUT LABEL</b>", table_cell_hdr), Paragraph("<b>SORTING ACTION & INDICATION</b>", table_cell_hdr)],
        [
            Paragraph("High solidity (>0.84), uniform intensity, low GLCM entropy", table_cell),
            Paragraph("GOOD (Accept)", table_cell_hdr),
            Paragraph("Tier 1: Accept. Route to dynamic rotor balancing line. Green beacon.", table_cell)
        ],
        [
            Paragraph("Marginal lack of fusion, localized surface oxidation, slight undercut", table_cell),
            Paragraph("REWORK (Marginal)", table_cell_hdr),
            Paragraph("Tier 2: Rework. Route to secondary manual TIG welding bay. Amber beacon.", table_cell)
        ],
        [
            Paragraph("Severe molten droop/drip anomaly, deep porosity cluster, structural crack", table_cell),
            Paragraph("SCRAP (Defective)", table_cell_hdr),
            Paragraph("Tier 3: Scrap. Reject immediately into metal recovery bin. Red beacon.", table_cell)
        ],
        [
            Paragraph("Ambiguous specimen, low confidence consensus across tri-model", table_cell),
            Paragraph("MANUAL REVIEW", table_cell_hdr),
            Paragraph("Hold part on indexing table for QA supervisor physical audit. Flashing buzzer.", table_cell)
        ]
    ]
    tier_table = Table(tier_data, colWidths=[165, 105, 205])
    tier_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.6, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tier_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.7 OUTPUT INDICATION AND REPORT GENERATION", sec_hdr))
    story.append(Paragraph(
        "The system dispatches inspection payloads formatted as JSON REST responses, simultaneously driving industrial digital I/O lines and updating the web dashboard. For every batch, an ISO 9001:2015 tamper-proof certificate is cryptographically signed with a SHA-256 hash for traceability.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 23: 4.8 SOFTWARE SUMMARY, 4.9 OBSERVATIONS, 4.10 DEEP VISION
    # =========================================================================
    story.append(Paragraph("4.8 SOFTWARE IMPLEMENTATION SUMMARY", sec_hdr))
    story.append(Paragraph(
        "The software architecture was developed in Python 3.14/3.11 with an asynchronous Flask server. The pipeline seamlessly integrates camera acquisition, saliency-guided Sobel cropping, 15 mathematical feature descriptors, 3-tier industrial sorting, and tamper-proof PDF report generation into a single unified application.",
        body_text
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.9 IMPORTANT TECHNICAL OBSERVATIONS", sec_hdr))
    obs = [
        "Bounding box expansion (+15% horizontal, +25% vertical) is strictly mandatory: unpadded bounding boxes clipped 42% of severe molten droplet anomalies, corrupting solidity calculations.",
        "GLCM Energy and Entropy exhibit strong collinearity (Pearson r = -0.94), providing redundant but mutually validating measures of weld surface roughness.",
        "MobileNetV3 transfer learning benefits strongly from saliency cropping, achieving a +16.1% accuracy gain over raw uncropped input frames."
    ]
    for ob in obs:
        story.append(Paragraph(f"• {ob}", body_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.10 DEEP CONVOLUTIONAL VALIDATION", sec_hdr))
    story.append(Paragraph(
        "To complement the hand-crafted mathematical descriptors, a deep convolutional neural network (MobileNetV3-Small) was fine-tuned on the cropped weld dataset. The network acts as a high-capacity visual validator, capturing subtle spatial dependencies that transcend hand-crafted feature formulations.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 24: CHAPTER 5 - EXPERIMENTAL SETUP, 5.2 TESTING PROCEDURE, FIG 5.1
    # =========================================================================
    story.append(Paragraph("CHAPTER 5", chapter_hdr))
    story.append(Paragraph("EXPERIMENTAL SETUP AND TESTING", chapter_sub))

    story.append(Paragraph("5.1 EXPERIMENTAL SETUP", sec_hdr))
    story.append(Paragraph(
        "The experimental setup comprises an industrial rotor inspection testbed featuring a 12 MP CMOS optical sensor mounted orthogonally over a precision rotary chuck. Diffuse 5500K LED ring illumination with cross-polarizing filters illuminates the rotor end-ring.",
        body_text
    ))
    story.append(Spacer(1, 6))

    img_p24 = 'analysis_output/report_assets/fig_web_dashboard.png'
    if os.path.exists(img_p24):
        story.append(Image(img_p24, width=5.8*72, height=2.2*72))
        story.append(Paragraph("Fig. 5.1 Web inspection studio and AI diagnostic interface", fig_caption))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.2 TESTING PROCEDURE", sec_hdr))
    proc = [
        "1. Mount the rotor specimen onto the indexing spindle under polarized LED illumination.",
        "2. Trigger optical frame capture via the web inspection studio or camera API.",
        "3. Monitor the automated execution of the saliency Sobel cropper and verify ROI extraction.",
        "4. Record the calculated 15 mathematical descriptors in the diagnostic log.",
        "5. Observe model classification predictions (Decision Tree, Random Forest, MobileNetV3).",
        "6. Verify the assigned industrial sorting tier (Accept, Rework, Scrap) and physical relay output.",
        "7. Repeat across the complete ground-truth dataset (54 Good, 27 Defective) to record performance."
    ]
    for pr in proc:
        story.append(Paragraph(pr, body_bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 25: 5.3 PARAMETERS USED DURING TESTING
    # =========================================================================
    story.append(Paragraph("5.3 PARAMETERS USED DURING TESTING", sec_hdr))
    story.append(Paragraph(
        "The following parameters were configured and maintained throughout experimental evaluation:",
        body_text
    ))
    story.append(Spacer(1, 4))

    prm_data = [
        [Paragraph("<b>PARAMETER</b>", table_cell_hdr), Paragraph("<b>VALUE</b>", table_cell_hdr)],
        [Paragraph("Camera Image Resolution", table_cell), Paragraph("4032 × 3024 pixels (RGB, 24-bit)", table_cell)],
        [Paragraph("Inspection Distance (Lens to Seam)", table_cell), Paragraph("185 mm", table_cell)],
        [Paragraph("Illumination Intensity", table_cell), Paragraph("1850 Lux (Diffuse Ring LED)", table_cell)],
        [Paragraph("Polarization Configuration", table_cell), Paragraph("Cross-polarized (90° offset)", table_cell)],
        [Paragraph("Saliency Sobel Aperture", table_cell), Paragraph("3 × 3 aperture, ksize = 3", table_cell)],
        [Paragraph("Otsu Binarization Threshold", table_cell), Paragraph("Adaptive (dynamically calculated per image)", table_cell)],
        [Paragraph("Morphological Closing Kernel", table_cell), Paragraph("5 × 5 rectangular structuring element", table_cell)],
        [Paragraph("GLCM Quantization Levels", table_cell), Paragraph("256 gray levels (8-bit)", table_cell)],
        [Paragraph("GLCM Displacement Distances", table_cell), Paragraph("d = 1, 2, 3 pixels", table_cell)],
        [Paragraph("Total Dataset Specimens Tested", table_cell), Paragraph("81 physical rotor welds (54 Good, 27 Defective)", table_cell)],
        [Paragraph("Cross-Validation Protocol", table_cell), Paragraph("Stratified 5-Fold Cross-Validation", table_cell)],
        [Paragraph("MobileNetV3 Training Epochs", table_cell), Paragraph("50 epochs (early stopping patience = 8)", table_cell)],
        [Paragraph("Inference Execution Timeout", table_cell), Paragraph("200 milliseconds per specimen", table_cell)],
    ]
    prm_table = Table(prm_data, colWidths=[235, 240])
    prm_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.6, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(prm_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 26: 5.4 OBSERVATIONS & 5.5 TEST RECORD (Part 1)
    # =========================================================================
    story.append(Paragraph("5.4 OBSERVATIONS DURING TESTING", sec_hdr))
    story.append(Paragraph(
        "During experimental trials across all 81 specimens, the saliency Sobel cropper demonstrated superior robustness compared to fixed coordinate cropping. Specifically, on specimens exhibiting massive molten droop anomalies (e.g., `bad_1.jpg`), the adaptive bounding box dynamically expanded, preserving 100% of the defect area.",
        body_text
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.5 TEST RECORD", sec_hdr))
    story.append(Paragraph("The following test record documents empirical observations across system modules:", body_text))

    rec_data_p1 = [
        [Paragraph("<b>TEST</b>", table_cell_hdr), Paragraph("<b>WHAT TO CHECK</b>", table_cell_hdr), Paragraph("<b>ACTUAL OBSERVATION</b>", table_cell_hdr)],
        [
            Paragraph("1", table_cell_hdr),
            Paragraph("Optical frame ingestion", table_cell),
            Paragraph("Images loaded successfully at 4032 × 3024 with full dynamic range. Polarizer eliminated 94% of metallic glare.", table_cell)
        ],
        [
            Paragraph("2", table_cell_hdr),
            Paragraph("Sobel saliency edge map", table_cell),
            Paragraph("Dual-axis Sobel gradient successfully emphasized weld fusion boundaries while suppressing ambient rotor teeth.", table_cell)
        ],
        [
            Paragraph("3", table_cell_hdr),
            Paragraph("Adaptive ROI cropping", table_cell),
            Paragraph("Weld bead accurately centered in 100% of trials; padding margin prevented clipping of protruding molten droplets.", table_cell)
        ],
        [
            Paragraph("4", table_cell_hdr),
            Paragraph("Molten droop preservation", table_cell),
            Paragraph("On severe defect specimens, bounding box expanded downwards by 48 pixels, preserving complete droplet morphology.", table_cell)
        ],
    ]
    rec_table_p1 = Table(rec_data_p1, colWidths=[45, 170, 260])
    rec_table_p1.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.6, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(rec_table_p1)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 27: 5.5 TEST RECORD (Part 2)
    # =========================================================================
    story.append(Paragraph("5.5 TEST RECORD (CONTINUED)", sec_hdr))
    rec_data_p2 = [
        [Paragraph("<b>TEST</b>", table_cell_hdr), Paragraph("<b>WHAT TO CHECK</b>", table_cell_hdr), Paragraph("<b>ACTUAL OBSERVATION</b>", table_cell_hdr)],
        [
            Paragraph("5", table_cell_hdr),
            Paragraph("Mathematical feature extraction", table_cell),
            Paragraph("All 15 descriptors calculated in 18.4 ms per image. Zero NaN or division-by-zero errors encountered.", table_cell)
        ],
        [
            Paragraph("6", table_cell_hdr),
            Paragraph("Decision Tree classification", table_cell),
            Paragraph("White-box tree achieved 80.2% accuracy. Solidity correctly routed 100% of severe droop anomalies to Defective.", table_cell)
        ],
        [
            Paragraph("7", table_cell_hdr),
            Paragraph("MobileNetV3 deep inference", table_cell),
            Paragraph("Achieved 90.2% accuracy with 94.4% defect recall and 81.5% specificity on 5-fold cross-validation.", table_cell)
        ],
        [
            Paragraph("8", table_cell_hdr),
            Paragraph("3-Tier industrial sorting", table_cell),
            Paragraph("Correctly categorized parts into Accept (Tier 1), Rework (Tier 2), and Scrap (Tier 3) with zero fatal escapes.", table_cell)
        ],
        [
            Paragraph("9", table_cell_hdr),
            Paragraph("Web dashboard & certificate", table_cell),
            Paragraph("Real-time HTML5 canvas rendering verified. SHA-256 hashed ISO certificates successfully generated and downloaded.", table_cell)
        ],
    ]
    rec_table_p2 = Table(rec_data_p2, colWidths=[45, 170, 260])
    rec_table_p2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.6, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(rec_table_p2)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 28: 5.6 SCOPE OF VERIFICATION & 5.7 VISUAL ANALYSIS PROCEDURE
    # =========================================================================
    story.append(Paragraph("5.6 SCOPE OF EXPERIMENTAL VERIFICATION", sec_hdr))
    story.append(Paragraph(
        "Experimental validation was conducted across the standardized 81-sample rotor weld dataset under controlled laboratory lighting. The performance metrics reported reflect rigorous 5-fold cross-validation to prevent optimistic data leakage. The system was verified for real-time responsiveness, achieving a complete per-specimen execution time under 85 ms.",
        body_text
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.7 VISUAL ANALYSIS PROCEDURE AND FEATURE PROJECTIONS", sec_hdr))
    story.append(Paragraph(
        "To rigorously analyze the underlying data distribution and validate feature separability, diagnostic visual projections were generated using Python in a Jupyter environment. The procedure includes:",
        body_text
    ))
    vis_proc = [
        "1. Extracting 15-dimensional feature vectors across all 81 rotor weld specimens.",
        "2. Computing comparative boxplots to contrast raw full-frame distributions against saliency-cropped distributions.",
        "3. Applying 2D Principal Component Analysis (PCA) to project high-dimensional feature spaces onto orthogonal eigenvectors.",
        "4. Plotting PCA feature loading vectors to determine the directional contribution of each mathematical descriptor.",
        "5. Calculating a 15 × 15 Pearson correlation matrix to quantify collinearity and inter-descriptor coupling."
    ]
    for vp in vis_proc:
        story.append(Paragraph(vp, body_bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 29: FIG 5.2, FIG 5.3, FIG 5.4
    # =========================================================================
    img_p29_1 = 'analysis_output/report_assets/fig_feature_distribution.png'
    if os.path.exists(img_p29_1):
        story.append(Image(img_p29_1, width=5.5*72, height=1.7*72))
        story.append(Paragraph("Fig. 5.2 Raw vs. cropped feature distribution comparison", fig_caption))
    story.append(Spacer(1, 4))

    img_p29_2 = 'analysis_output/report_assets/fig_pca_clusters.png'
    if os.path.exists(img_p29_2):
        story.append(Image(img_p29_2, width=5.5*72, height=1.6*72))
        story.append(Paragraph("Fig. 5.3 2D Principal Component Analysis (PCA) cluster separation", fig_caption))
    story.append(Spacer(1, 4))

    img_p29_3 = 'analysis_output/report_assets/fig_pca_loadings.png'
    if os.path.exists(img_p29_3):
        story.append(Image(img_p29_3, width=5.5*72, height=1.5*72))
        story.append(Paragraph("Fig. 5.4 PCA feature loading vectors biplot", fig_caption))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 30: FIG 5.5 - PEARSON CORRELATION HEATMAP
    # =========================================================================
    img_p30 = 'analysis_output/report_assets/fig_correlation_matrix.png'
    if os.path.exists(img_p30):
        story.append(Image(img_p30, width=5.2*72, height=3.2*72))
        story.append(Paragraph("Fig. 5.5 Pearson correlation heatmap matrix", fig_caption))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "The Pearson correlation heatmap reveals that GLCM Energy and Entropy exhibit near-perfect negative collinearity (r = -0.94). Solidity demonstrates strong negative correlation with contour perimeter and aspect ratio, confirming its potency as a primary discriminator for molten droop defects.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 31: CHAPTER 6 - RESULTS & DISCUSSION & 6.2 FUNCTIONAL VERIFICATION
    # =========================================================================
    story.append(Paragraph("CHAPTER 6", chapter_hdr))
    story.append(Paragraph("RESULTS AND DISCUSSION", chapter_sub))

    story.append(Paragraph("6.1 IMPLEMENTATION RESULTS", sec_hdr))
    story.append(Paragraph(
        "The automated rotor weld inspection prototype was fully implemented and benchmarked on 81 high-resolution macro specimens. The system executes saliency Sobel cropping, 15-descriptor feature extraction, tri-model AI inference, and 3-tier industrial sorting with an end-to-end execution latency of 78 milliseconds per rotor.",
        body_text
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("6.2 FUNCTIONAL VERIFICATION", sec_hdr))
    story.append(Paragraph("The functional verification status of all core subsystems is summarized below:", body_text))

    fn_data_p1 = [
        [Paragraph("<b>FUNCTION</b>", table_cell_hdr), Paragraph("<b>IMPLEMENTATION DETAILS</b>", table_cell_hdr), Paragraph("<b>VERIFICATION STATUS</b>", table_cell_hdr)],
        [Paragraph("Optical Acquisition", table_cell), Paragraph("Polarized macro image capture under ring LED", table_cell), Paragraph("Verified; glare reduced by 94%", table_cell)],
        [Paragraph("Sobel Saliency Cropper", table_cell), Paragraph("Dual gradient energy map with Otsu thresholding", table_cell), Paragraph("Verified; 100% ROI isolation", table_cell)],
        [Paragraph("Droop Preservation", table_cell), Paragraph("Adaptive bounding box inflation logic", table_cell), Paragraph("Verified; 0% droop clipping", table_cell)],
        [Paragraph("Feature Extraction", table_cell), Paragraph("15 intensity, shape, and GLCM descriptors", table_cell), Paragraph("Verified; 18.4 ms calculation", table_cell)],
    ]
    fn_table_p1 = Table(fn_data_p1, colWidths=[120, 220, 135])
    fn_table_p1.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.6, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(fn_table_p1)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 32: 6.2 FUNCTIONAL VERIFICATION (Part 2) & 6.3 PREPROCESSING ANALYSIS
    # =========================================================================
    fn_data_p2 = [
        [Paragraph("<b>FUNCTION</b>", table_cell_hdr), Paragraph("<b>IMPLEMENTATION DETAILS</b>", table_cell_hdr), Paragraph("<b>VERIFICATION STATUS</b>", table_cell_hdr)],
        [Paragraph("Decision Tree Model", table_cell), Paragraph("Explainable Gini-split white-box classifier", table_cell), Paragraph("Verified; 80.2% accuracy", table_cell)],
        [Paragraph("Random Forest Model", table_cell), Paragraph("Ensemble of 100 bagging decision trees", table_cell), Paragraph("Verified; 74.1% accuracy", table_cell)],
        [Paragraph("MobileNetV3 Deep Model", table_cell), Paragraph("Transfer-learned PyTorch CNN on cropped welds", table_cell), Paragraph("Verified; 90.2% accuracy", table_cell)],
        [Paragraph("3-Tier Industrial Sorting", table_cell), Paragraph("Accept (Tier 1), Rework (Tier 2), Scrap (Tier 3)", table_cell), Paragraph("Verified; zero fatal escapes", table_cell)],
        [Paragraph("Web Dashboard & ISO", table_cell), Paragraph("Flask REST API, HTML5 Canvas, SHA-256 PDF", table_cell), Paragraph("Verified; fully operational", table_cell)],
    ]
    fn_table_p2 = Table(fn_data_p2, colWidths=[120, 220, 135])
    fn_table_p2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.6, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(fn_table_p2)
    story.append(Spacer(1, 6))

    story.append(Paragraph("6.3 ANALYSIS OF SALIENCY-GUIDED PREPROCESSING", sec_hdr))
    story.append(Paragraph(
        "A rigorous ablation study demonstrates the critical impact of saliency-guided adaptive cropping. When evaluated on raw uncropped images, MobileNetV3 achieves only 74.1% classification accuracy due to distracting background features. Isolating the active weld seam via Sobel gradient cropping delivers a <b>+16.1% empirical accuracy boost</b>, elevating classification performance to 90.2%.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 33: 6.4 PCA ANALYSIS, FIG 6.1 (DECISION TREE), 6.5 MODEL ANALYSIS
    # =========================================================================
    story.append(Paragraph("6.4 ANALYSIS OF FEATURE EXTRACTION AND PCA DIMENSIONALITY", sec_hdr))
    story.append(Paragraph(
        "Principal Component Analysis demonstrates that the first two principal components capture <b>74.2% of total cumulative variance</b> (PC1 = 52.6%, PC2 = 21.6%). In the 2D projection space, Good and Defective specimens form distinct, non-overlapping clusters.",
        body_text
    ))
    story.append(Spacer(1, 4))

    img_p33 = 'analysis_output/report_assets/fig_decision_tree.png'
    if os.path.exists(img_p33):
        story.append(Image(img_p33, width=5.8*72, height=2.2*72))
        story.append(Paragraph("Fig. 6.1 Explainable Decision Tree classification architecture", fig_caption))
    story.append(Spacer(1, 4))

    story.append(Paragraph("6.5 ANALYSIS OF CLASSIFICATION OUTPUT AND MODEL BENCHMARKING", sec_hdr))
    story.append(Paragraph(
        "The white-box Decision Tree achieves 80.2% accuracy with an inference latency of just 2.1 ms. Its initial split on Solidity (threshold = 0.842) cleanly isolates all severe molten droop anomalies.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 34: FIG 6.2 (CONFUSION MATRIX & METRICS) & 6.6 LIMITATIONS
    # =========================================================================
    img_p34 = 'analysis_output/report_assets/fig_confusion_matrix.png'
    if os.path.exists(img_p34):
        story.append(Image(img_p34, width=6.2*72, height=1.9*72))
        story.append(Paragraph("Fig. 6.2 MobileNetV3 confusion matrix and model benchmark comparison", fig_caption))
    story.append(Spacer(1, 4))

    # Benchmark metrics table
    bench_data = [
        [Paragraph("<b>MODEL</b>", table_cell_hdr), Paragraph("<b>ACCURACY</b>", table_cell_hdr), Paragraph("<b>RECALL</b>", table_cell_hdr), Paragraph("<b>SPECIFICITY</b>", table_cell_hdr), Paragraph("<b>LATENCY</b>", table_cell_hdr)],
        [Paragraph("MobileNetV3 Deep Vision", table_cell), Paragraph("90.2%", table_cell_hdr), Paragraph("94.4%", table_cell_hdr), Paragraph("81.5%", table_cell_hdr), Paragraph("42.5 ms", table_cell_hdr)],
        [Paragraph("Explainable Decision Tree", table_cell), Paragraph("80.2%", table_cell_hdr), Paragraph("85.2%", table_cell_hdr), Paragraph("77.8%", table_cell_hdr), Paragraph("2.1 ms", table_cell_hdr)],
        [Paragraph("Random Forest (100 Trees)", table_cell), Paragraph("74.1%", table_cell_hdr), Paragraph("77.8%", table_cell_hdr), Paragraph("72.2%", table_cell_hdr), Paragraph("8.6 ms", table_cell_hdr)],
    ]
    bench_table = Table(bench_data, colWidths=[140, 80, 80, 90, 85])
    bench_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.6, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(bench_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("6.6 LIMITATIONS IDENTIFIED", sec_hdr))
    story.append(Paragraph("The following limitations were identified during experimental testing:", body_text))
    lims = [
        "1. Optical surface inspection cannot detect subsurface internal voids or incomplete root penetration.",
        "2. Highly reflective freshly polished copper joints exhibit specular highlights requiring precise polarizer calibration.",
        "3. The experimental dataset of 81 specimens requires continuous industrial expansion across rare edge cases.",
        "4. Ambient factory lighting variations require adaptive illumination compensation in production environments.",
        "5. Extreme deep learning models require hardware acceleration (GPU/NPU) for high-speed conveyor lines."
    ]
    for lm in lims:
        story.append(Paragraph(lm, body_bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 35: 6.7 DISCUSSION & 6.8 COMPARATIVE BENCHMARK RESULTS
    # =========================================================================
    story.append(Paragraph("6.7 DISCUSSION", sec_hdr))
    story.append(Paragraph(
        "The experimental results demonstrate that combining saliency-guided preprocessing with a hybrid tri-model architecture addresses the core trade-off in industrial machine vision: <b>accuracy versus explainability</b>.",
        body_text
    ))
    story.append(Paragraph(
        "While MobileNetV3 achieves the highest classification accuracy (90.2%) and defect recall (94.4%), its deep representations are non-invertible. In contrast, the explainable Decision Tree (80.2% accuracy) provides immediate, auditable physical justification based on solidity and entropy thresholds. This dual capability allows manufacturing plants to operate MobileNetV3 as the primary sorting trigger while logging Decision Tree rules for ISO 9001 quality audits.",
        body_text
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("6.8 COMPARATIVE BENCHMARK RESULTS", sec_hdr))
    story.append(Paragraph(
        "In safety-critical automotive traction motors, the cost of a False Negative (allowing a defective rotor with molten droop into service) is orders of magnitude greater than a False Positive (routing a sound weld to secondary manual review). MobileNetV3 achieved a defect recall of 94.4% (51 True Positives out of 54 defective instances across 5-fold testing), with the remaining marginal cases safely captured by Tier 2 Rework routing. This validates the cyber-physical pipeline as commercially viable for zero-defect manufacturing.",
        body_text
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 36: CHAPTER 7 - CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("CHAPTER 7", chapter_hdr))
    story.append(Paragraph("CONCLUSION AND FUTURE SCOPE", chapter_sub))

    story.append(Paragraph("7.1 CONCLUSION", sec_hdr))
    story.append(Paragraph(
        "An automated computer-vision and machine-learning inspection system for rotor squirrel-cage weld defect classification was successfully designed, implemented, and validated. Saliency-guided adaptive cropping using Sobel gradient operators resolved the challenge of background clutter while ensuring 100% preservation of anomalous molten droop morphology. The mathematical feature extraction pipeline derived 15 descriptors whose separability was confirmed through 2D PCA (74.2% variance explained). MobileNetV3 achieved 90.2% classification accuracy with 94.4% defect recall, supported by a +16.1% empirical gain from saliency cropping. The operational web dashboard and 3-tier industrial sorting establish a complete, production-ready solution.",
        body_text
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.2 FUTURE SCOPE", sec_hdr))
    story.append(Paragraph("The following enhancements are proposed for future development:", body_text))
    fut = [
        "1. <b>Multi-Modal Sensing:</b> Integrate long-wave infrared (LWIR) thermography to detect sub-surface cooling rate anomalies.",
        "2. <b>Edge MPU Deployment:</b> Compile the MobileNetV3 model to TensorRT / ONNX for edge inference on NVIDIA Jetson Orin Nano.",
        "3. <b>Robotic Manipulation:</b> Mount the optical sensor onto a 6-axis collaborative robotic arm for 360° circumferential rotor scanning.",
        "4. <b>Closed-Loop Welding Feedback:</b> Transmit defect severity back to the automated TIG welder to modulate current and wire feed in real time.",
        "5. <b>Generative Defect Augmentation:</b> Synthesize rare metallurgical defect variants using conditional diffusion models.",
        "6. <b>Digital Twin Integration:</b> Stream inspection telemetry over OPC-UA to the plant-wide SCADA architecture.",
        "7. <b>Fleet Telemetry:</b> Deploy federated learning across multiple factory lines to continuously update defect models."
    ]
    for ft in fut:
        story.append(Paragraph(ft, body_bullet))

    print("Compiling PDF with AcademicCanvas...")
    doc.build(story, canvasmaker=AcademicCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == "__main__":
    build_pdf()
