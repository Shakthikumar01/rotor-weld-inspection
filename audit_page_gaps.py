import pypdf

reader = pypdf.PdfReader('Rotor_Weld_Defect_Inspection_Academic_Report_PSG.pdf')
print(f"Total pages: {len(reader.pages)}")

page_stats = []

for idx, page in enumerate(reader.pages):
    min_y = [999.0]
    max_y = [-999.0]
    
    def visitor(text, cm, tm, fontDict, fontSize):
        if text.strip():
            abs_y = cm[5] + tm[5]
            if abs_y < min_y[0]:
                min_y[0] = abs_y
            if abs_y > max_y[0]:
                max_y[0] = abs_y
            
    page.extract_text(visitor_text=visitor)
    
    # Note: ReportLab canvas page number footer is at y ~ 32
    # So if min_y[0] is around 32, the page number is at 32, but what is the lowest body text/table/figure?
    # Let's inspect elements above y = 45 (excluding footer)
    body_min_y = [999.0]
    def visitor_body(text, cm, tm, fontDict, fontSize):
        if text.strip():
            abs_y = cm[5] + tm[5]
            # Ignore footer page numbers (at y < 45) and header (if any)
            if abs_y > 45:
                if abs_y < body_min_y[0]:
                    body_min_y[0] = abs_y
    page.extract_text(visitor_text=visitor_body)
    
    # Bottom margin is 48 pt. Empty space above bottom margin:
    b_gap = body_min_y[0] - 48.0 if body_min_y[0] != 999.0 else 0.0
    
    first_few = [l.strip() for l in page.extract_text().splitlines() if l.strip()]
    preview = ' // '.join(first_few[:2])[:60] if first_few else 'EMPTY'
    
    page_stats.append((idx + 1, body_min_y[0], b_gap, preview))

print(f"{'Page':<5} | {'Lowest Body Y':<14} | {'Bottom Gap (pt)':<16} | {'Inches':<6} | {'Content Preview'}")
print('-'*100)
large_gaps = []
for p, l_y, gap, prev in page_stats:
    gap_in = gap / 72.0
    flag = ' *** LARGE GAP ***' if gap > 150 else ''
    if gap > 150:
        large_gaps.append((p, gap, gap_in, prev))
    print(f"{p:<5} | {l_y:<14.1f} | {gap:<16.1f} | {gap_in:<6.2f} | {prev}{flag}")

print(f"\nTotal pages with > 150 pt (> 2.1 inches) empty space at bottom: {len(large_gaps)}")
for p, gap, gap_in, prev in large_gaps:
    print(f"Page {p:2d} (gap={gap:5.1f} pt / {gap_in:4.2f} in): {prev}")
