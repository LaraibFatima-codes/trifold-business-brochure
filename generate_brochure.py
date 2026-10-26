import os
import shutil
import zipfile
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path

# Page Setup: Landscape Letter (11 x 8.5 in) = 792 x 612 pt
PAGE_W, PAGE_H = landscape(LETTER) # 792, 612
PANEL_W = PAGE_W / 3.0 # 264 pt per panel

# Color Palette
C_NAVY = colors.HexColor('#0F172A')       # Primary Dark Navy
C_GOLD = colors.HexColor('#D97706')       # Warm Accent Gold
C_GOLD_LIGHT = colors.HexColor('#FEF3C7') # Soft Gold Background
C_SLATE = colors.HexColor('#334155')      # Secondary Dark Text
C_LIGHT_BG = colors.HexColor('#F8FAFC')   # Light Panel Background
C_WHITE = colors.HexColor('#FFFFFF')      # White
C_BORDER = colors.HexColor('#E2E8F0')     # Subtle Border Lines
C_ACCENT_BLUE = colors.HexColor('#1E293B')# Accent Blue

def draw_fold_lines(c):
    """Draw subtle dashed fold indicators."""
    c.saveState()
    c.setStrokeColor(colors.HexColor('#CBD5E1'))
    c.setLineWidth(0.5)
    c.setDash(3, 3)
    c.line(PANEL_W, 0, PANEL_W, PAGE_H)
    c.line(PANEL_W * 2, 0, PANEL_W * 2, PAGE_H)
    c.restoreState()

# PAGE 1: OUTSIDE SPREAD
# Panel 1 (x: 0-264): Inside Flap (Fold-In)
# Panel 2 (x: 264-528): Back Cover
# Panel 3 (x: 528-792): Front Cover
def draw_page1_outside(c):
    # Backgrounds
    c.setFillColor(C_LIGHT_BG)
    c.rect(0, 0, PANEL_W, PAGE_H, fill=1, stroke=0)
    
    c.setFillColor(C_NAVY)
    c.rect(PANEL_W, 0, PANEL_W, PAGE_H, fill=1, stroke=0)
    
    c.setFillColor(C_WHITE)
    c.rect(PANEL_W * 2, 0, PANEL_W, PAGE_H, fill=1, stroke=0)
    
    # Top Gold Header Bar across Outside
    c.setFillColor(C_GOLD)
    c.rect(0, PAGE_H - 12, PAGE_W, 12, fill=1, stroke=0)

    # PANEL 1: INSIDE FLAP
    p1_x = 0
    c.setFillColor(C_NAVY)
    c.rect(p1_x + 16, PAGE_H - 60, PANEL_W - 32, 36, fill=1, stroke=0)
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(p1_x + PANEL_W/2, PAGE_H - 44, "WHY CHOOSE APEX")
    
    c.setFillColor(C_SLATE)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(p1_x + PANEL_W/2, PAGE_H - 80, "Excellence in Premium Real Estate")
    
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(1.5)
    c.line(p1_x + 40, PAGE_H - 92, p1_x + PANEL_W - 40, PAGE_H - 92)

    stats = [
        ("15+ Years", "Industry Leadership & Track Record"),
        ("99%", "Client Satisfaction & Retention Rate"),
        ("500+", "Premium Properties Represented")
    ]
    card_y = PAGE_H - 120
    for val, desc in stats:
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1)
        c.roundRect(p1_x + 20, card_y - 42, PANEL_W - 40, 50, 6, fill=1, stroke=1)
        
        c.setFillColor(C_GOLD)
        c.roundRect(p1_x + 20, card_y - 42, 6, 50, 3, fill=1, stroke=0)
        
        c.setFillColor(C_NAVY)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(p1_x + 36, card_y - 18, val)
        
        c.setFillColor(C_SLATE)
        c.setFont("Helvetica", 9)
        c.drawString(p1_x + 36, card_y - 32, desc)
        card_y -= 62

    c.setFillColor(C_NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(p1_x + 24, card_y - 10, "Our Key Pillars:")
    
    pillars = [
        "Personalized Portfolio Curation",
        "Exclusive Property Listings",
        "Comprehensive Market Advisory",
        "Bespoke Marketing Solutions"
    ]
    py = card_y - 30
    for p in pillars:
        c.setFillColor(C_GOLD)
        c.circle(p1_x + 30, py + 3, 3, fill=1, stroke=0)
        c.setFillColor(C_SLATE)
        c.setFont("Helvetica", 9.5)
        c.drawString(p1_x + 40, py, p)
        py -= 20

    c.setFillColor(C_GOLD_LIGHT)
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(1)
    c.roundRect(p1_x + 20, 24, PANEL_W - 40, 40, 6, fill=1, stroke=1)
    c.setFillColor(C_NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(p1_x + PANEL_W/2, 48, "CERTIFIED REAL ESTATE ADVISORS")
    c.setFont("Helvetica", 8.5)
    c.setFillColor(C_SLATE)
    c.drawCentredString(p1_x + PANEL_W/2, 32, "Top Industry Standards Nationwide")

    # PANEL 2: BACK COVER
    p2_x = PANEL_W
    c.setFillColor(C_GOLD)
    c.circle(p2_x + PANEL_W/2, PAGE_H - 70, 36, fill=1, stroke=0)
    c.setFillColor(C_NAVY)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(p2_x + PANEL_W/2, PAGE_H - 76, "A")
    
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(p2_x + PANEL_W/2, PAGE_H - 125, "APEX REAL ESTATE")
    c.setFillColor(C_GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(p2_x + PANEL_W/2, PAGE_H - 140, "PREMIUM PROPERTIES & ADVISORY")
    
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(1)
    c.line(p2_x + 50, PAGE_H - 155, p2_x + PANEL_W - 50, PAGE_H - 155)

    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(p2_x + PANEL_W/2, PAGE_H - 185, "CONNECT WITH US")

    info_items = [
        ("HEADQUARTERS", "123 Business Plaza, Suite 500\nMetropolis, NY 10001"),
        ("CONTACT DIRECT", "+1 (800) 555-0199\ninfo@example.com"),
        ("WEBSITE", "www.example.com\n@ApexProperties")
    ]
    iy = PAGE_H - 225
    for title, text in info_items:
        c.setFillColor(C_GOLD)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(p2_x + PANEL_W/2, iy, title)
        c.setFillColor(colors.HexColor('#CBD5E1'))
        c.setFont("Helvetica", 9)
        lines = text.split('\n')
        c.drawCentredString(p2_x + PANEL_W/2, iy - 14, lines[0])
        if len(lines) > 1:
            c.drawCentredString(p2_x + PANEL_W/2, iy - 26, lines[1])
        iy -= 52

    # QR Code Box Placeholder
    c.setFillColor(C_ACCENT_BLUE)
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(1)
    c.roundRect(p2_x + PANEL_W/2 - 40, iy - 20, 80, 80, 6, fill=1, stroke=1)
    
    c.setFillColor(C_WHITE)
    c.rect(p2_x + PANEL_W/2 - 30, iy - 10, 60, 60, fill=1, stroke=0)
    c.setFillColor(C_NAVY)
    c.rect(p2_x + PANEL_W/2 - 25, iy - 5, 20, 20, fill=1, stroke=0)
    c.rect(p2_x + PANEL_W/2 + 5, iy - 5, 20, 20, fill=1, stroke=0)
    c.rect(p2_x + PANEL_W/2 - 25, iy + 25, 20, 20, fill=1, stroke=0)
    c.rect(p2_x + PANEL_W/2 - 5, iy + 10, 10, 10, fill=1, stroke=0)

    c.setFillColor(colors.HexColor('#94A3B8'))
    c.setFont("Helvetica", 8)
    c.drawCentredString(p2_x + PANEL_W/2, iy - 32, "Scan for Virtual Portfolio")

    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor('#64748B'))
    c.drawCentredString(p2_x + PANEL_W/2, 35, "@ApexProperties • #ApexLiving")
    c.drawCentredString(p2_x + PANEL_W/2, 22, "© 2026 Apex Real Estate Group. All Rights Reserved.")

    # PANEL 3: FRONT COVER
    p3_x = PANEL_W * 2
    
    path = c.beginPath()
    path.moveTo(p3_x, PAGE_H)
    path.lineTo(p3_x + PANEL_W, PAGE_H)
    path.lineTo(p3_x + PANEL_W, PAGE_H - 240)
    path.lineTo(p3_x, PAGE_H - 280)
    path.close()
    c.setFillColor(C_NAVY)
    c.drawPath(path, fill=1, stroke=0)

    path_gold = c.beginPath()
    path_gold.moveTo(p3_x, PAGE_H - 280)
    path_gold.lineTo(p3_x + PANEL_W, PAGE_H - 240)
    path_gold.lineTo(p3_x + PANEL_W, PAGE_H - 248)
    path_gold.lineTo(p3_x, PAGE_H - 288)
    path_gold.close()
    c.setFillColor(C_GOLD)
    c.drawPath(path_gold, fill=1, stroke=0)

    c.setFillColor(C_GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(p3_x + 24, PAGE_H - 50, "PREMIUM REAL ESTATE")
    
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(p3_x + 24, PAGE_H - 85, "ELEVATING")
    c.drawString(p3_x + 24, PAGE_H - 112, "MODERN")
    c.setFillColor(C_GOLD)
    c.drawString(p3_x + 24, PAGE_H - 139, "LIVING.")

    c.setFillColor(colors.HexColor('#E2E8F0'))
    c.setFont("Helvetica", 10)
    c.drawString(p3_x + 24, PAGE_H - 175, "Bespoke Residences &")
    c.drawString(p3_x + 24, PAGE_H - 189, "Strategic Property Advisory")

    frame_y = PAGE_H - 430
    c.setFillColor(C_LIGHT_BG)
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(1.5)
    c.roundRect(p3_x + 20, frame_y, PANEL_W - 40, 120, 8, fill=1, stroke=1)
    
    c.setFillColor(C_GOLD_LIGHT)
    c.rect(p3_x + 28, frame_y + 8, PANEL_W - 56, 104, fill=1, stroke=0)
    
    c.setStrokeColor(C_NAVY)
    c.setLineWidth(2)
    c.line(p3_x + 50, frame_y + 30, p3_x + 132, frame_y + 85)
    c.line(p3_x + 132, frame_y + 85, p3_x + 214, frame_y + 30)
    c.line(p3_x + 65, frame_y + 30, p3_x + 65, frame_y + 70)
    c.line(p3_x + 199, frame_y + 30, p3_x + 199, frame_y + 70)
    c.line(p3_x + 50, frame_y + 30, p3_x + 214, frame_y + 30)
    c.setFillColor(C_NAVY)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(p3_x + PANEL_W/2, frame_y + 15, "ARCHITECTURAL EXCELLENCE")

    c.setFillColor(C_NAVY)
    c.roundRect(p3_x + 20, 40, PANEL_W - 40, 50, 6, fill=1, stroke=0)
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(p3_x + PANEL_W/2, 68, "EXPLORE OUR COLLECTION")
    c.setFont("Helvetica", 9)
    c.setFillColor(C_GOLD)
    c.drawCentredString(p3_x + PANEL_W/2, 52, "www.example.com  →")

    draw_fold_lines(c)

# PAGE 2: INSIDE SPREAD
def draw_page2_inside(c):
    c.setFillColor(C_WHITE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setFillColor(C_NAVY)
    c.rect(0, PAGE_H - 48, PAGE_W, 48, fill=1, stroke=0)
    c.setFillColor(C_GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(24, PAGE_H - 20, "THE APEX EXPERIENCE")
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(24, PAGE_H - 38, "COMPREHENSIVE REAL ESTATE SERVICES")
    c.setFillColor(C_GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(PAGE_W - 24, PAGE_H - 30, "PROPERTY PORTFOLIO")

    c.setFillColor(C_GOLD)
    c.rect(0, PAGE_H - 52, PAGE_W, 4, fill=1, stroke=0)

    # PANEL 1: OUR SERVICES
    p1_x = 0
    c.setFillColor(C_NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(p1_x + 20, PAGE_H - 80, "OUR CORE SERVICES")
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(2)
    c.line(p1_x + 20, PAGE_H - 86, p1_x + 100, PAGE_H - 86)

    services = [
        ("Residential Buying & Sales", 
         "Tailored acquisition and marketing strategies for premium homes and estates."),
        ("Luxury Property Leasing", 
         "Connecting distinguished tenants with high-value residences and leasing solutions."),
        ("Commercial Advisory", 
         "Data-driven portfolio evaluation, asset expansion, and strategic positioning."),
        ("Property Management", 
         "Turnkey estate management, maintenance oversight, and operational care.")
    ]

    sy = PAGE_H - 115
    for stitle, sdesc in services:
        c.setFillColor(C_LIGHT_BG)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1)
        c.roundRect(p1_x + 16, sy - 85, PANEL_W - 32, 92, 6, fill=1, stroke=1)

        c.setFillColor(C_NAVY)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(p1_x + 28, sy - 18, stitle)

        c.setStrokeColor(C_GOLD)
        c.setLineWidth(1)
        c.line(p1_x + 28, sy - 24, p1_x + 80, sy - 24)

        c.setFillColor(C_SLATE)
        c.setFont("Helvetica", 8.5)
        
        words = sdesc.split(' ')
        line1, line2, line3 = "", "", ""
        for w in words:
            if len(line1 + " " + w) < 32:
                line1 += (" " if line1 else "") + w
            elif len(line2 + " " + w) < 32:
                line2 += (" " if line2 else "") + w
            else:
                line3 += (" " if line3 else "") + w
        
        c.drawString(p1_x + 28, sy - 42, line1)
        if line2:
            c.drawString(p1_x + 28, sy - 54, line2)
        if line3:
            c.drawString(p1_x + 28, sy - 66, line3)

        sy -= 110

    # PANEL 2: FEATURED LISTINGS
    p2_x = PANEL_W
    c.setFillColor(C_NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(p2_x + 20, PAGE_H - 80, "FEATURED LISTINGS")
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(2)
    c.line(p2_x + 20, PAGE_H - 86, p2_x + 100, PAGE_H - 86)

    listings = [
        ("THE SKYLINE PENTHOUSE", "$2,850,000", "4 Beds • 4.5 Baths • 4,200 sq ft", "Full floor, panoramic city skyline views."),
        ("COASTAL PALM VILLA", "$3,200,000", "5 Beds • 6 Baths • 5,500 sq ft", "Direct oceanfront access with private pool."),
        ("HILLSIDE MODERN ESTATE", "$1,900,000", "3 Beds • 3.5 Baths • 3,200 sq ft", "Architectural glass design with hillside view.")
    ]

    ly = PAGE_H - 115
    for ltitle, lprice, lspecs, ldesc in listings:
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1)
        c.roundRect(p2_x + 16, ly - 110, PANEL_W - 32, 120, 6, fill=1, stroke=1)

        c.setFillColor(C_NAVY)
        c.roundRect(p2_x + 16, ly - 35, PANEL_W - 32, 45, 6, fill=1, stroke=0)
        c.setFillColor(C_GOLD)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(p2_x + 26, ly - 18, ltitle)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(p2_x + PANEL_W - 26, ly - 18, lprice)

        c.setFillColor(C_GOLD_LIGHT)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(p2_x + 26, ly - 30, "AVAILABLE NOW • PRIVATE VIEWINGS")

        c.setFillColor(C_NAVY)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(p2_x + 26, ly - 54, lspecs)

        c.setFillColor(C_SLATE)
        c.setFont("Helvetica", 8.5)
        c.drawString(p2_x + 26, ly - 70, ldesc)

        c.setFillColor(C_LIGHT_BG)
        c.setStrokeColor(C_GOLD)
        c.roundRect(p2_x + 26, ly - 98, 120, 18, 4, fill=1, stroke=1)
        c.setFillColor(C_NAVY)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(p2_x + 34, ly - 90, "VIEW VIRTUAL TOUR →")

        ly -= 150

    # PANEL 3: PROCESS & TESTIMONIAL
    p3_x = PANEL_W * 2
    c.setFillColor(C_NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(p3_x + 20, PAGE_H - 80, "THE APEX PROCESS")
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(2)
    c.line(p3_x + 20, PAGE_H - 86, p3_x + 100, PAGE_H - 86)

    steps = [
        ("1. DISCOVERY & VISION", "Consultation to define property goals, location criteria, and investment targets."),
        ("2. CURATED SELECTION", "Accessing curated inventory and arranging private, confidential viewings."),
        ("3. SEAMLESS CLOSING", "End-to-end support for negotiation, advisory, and successful closing.")
    ]

    sty = PAGE_H - 115
    for stitle, sdesc in steps:
        c.setFillColor(C_LIGHT_BG)
        c.setStrokeColor(C_BORDER)
        c.roundRect(p3_x + 16, sty - 60, PANEL_W - 32, 68, 6, fill=1, stroke=1)

        c.setFillColor(C_GOLD)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(p3_x + 26, sty - 18, stitle)

        c.setFillColor(C_SLATE)
        c.setFont("Helvetica", 8.5)
        words = sdesc.split(' ')
        l1, l2 = "", ""
        for w in words:
            if len(l1 + " " + w) < 32:
                l1 += (" " if l1 else "") + w
            else:
                l2 += (" " if l2 else "") + w
        c.drawString(p3_x + 26, sty - 36, l1)
        if l2:
            c.drawString(p3_x + 26, sty - 48, l2)

        sty -= 82

    # Client Testimonial Box
    c.setFillColor(C_NAVY)
    c.roundRect(p3_x + 16, 40, PANEL_W - 32, 130, 8, fill=1, stroke=0)

    c.setFillColor(C_GOLD)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(p3_x + 28, 135, "“")

    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(p3_x + 42, 140, "Apex transformed our property search.")
    c.drawString(p3_x + 28, 126, "Their professionalism, market insight, and focus")
    c.drawString(p3_x + 28, 114, "on client priorities were second to none.")

    c.setStrokeColor(C_GOLD)
    c.setLineWidth(1)
    c.line(p3_x + 28, 98, p3_x + 100, 98)

    c.setFillColor(C_GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(p3_x + 28, 82, "CLIENT TESTIMONIAL")
    c.setFillColor(colors.HexColor('#94A3B8'))
    c.setFont("Helvetica", 8)
    c.drawString(p3_x + 28, 68, "Homeowners • Metropolis")

    draw_fold_lines(c)

def main():
    scratch_dir = "/workspace/scratch"
    out_dir = "/workspace/out"
    os.makedirs(scratch_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    pdf_filename = "apex_real_estate_trifold_brochure.pdf"
    scratch_pdf_path = os.path.join(scratch_dir, pdf_filename)
    out_pdf_path = os.path.join(out_dir, pdf_filename)

    c = canvas.Canvas(scratch_pdf_path, pagesize=landscape(LETTER))
    c.setTitle("Apex Real Estate - Trifold Brochure")

    draw_page1_outside(c)
    c.showPage()

    draw_page2_inside(c)
    c.showPage()

    c.save()
    print(f"Generated PDF at {scratch_pdf_path}")

    images = convert_from_path(scratch_pdf_path, dpi=150)
    png_paths = []
    for i, img in enumerate(images):
        png_name = f"trifold_brochure_page{i+1}.png"
        scratch_png = os.path.join(scratch_dir, png_name)
        img.save(scratch_png, 'PNG')
        png_paths.append(scratch_png)
        shutil.copy(scratch_png, os.path.join(out_dir, png_name))
        print(f"Saved preview image {png_name}")

    shutil.copy(scratch_pdf_path, out_pdf_path)

    readme_path = os.path.join(scratch_dir, "README.md")
    readme_content = """# Internship Task Submission: Business Trifold Brochure

## Overview
This package provides a professional 6-panel **Trifold Brochure** designed for **Apex Real Estate Group**.

### Files Included
1. `apex_real_estate_trifold_brochure.pdf` - High-resolution print-ready 2-page landscape PDF.
2. `trifold_brochure_page1.png` - Outside spread (Flap, Back Cover, Front Cover).
3. `trifold_brochure_page2.png` - Inside spread (Services, Listings, Process).
4. `generate_brochure.py` - Python source code using ReportLab for vector rendering.
5. `README.md` - Technical notes and submission documentation.

---

## Design System
- **Dimensions**: 11" x 8.5" Landscape (3 equal 3.66" panels).
- **Colors**: Deep Navy (`#0F172A`), Gold (`#D97706`), Slate Gray (`#334155`), Off-White (`#F8FAFC`).
- **Structure**:
  - Panel 1 (Inside Flap): Stats & Why Choose Us
  - Panel 2 (Back Cover): Contact Info & QR Code
  - Panel 3 (Front Cover): Hero Banner & Brand Tagline
  - Panel 4-6 (Inside Spread): Services, Featured Listings, Process & Testimonial
"""
    with open(readme_path, "w") as f:
        f.write(readme_content)

    zip_name = "apex_real_estate_trifold_package.zip"
    scratch_zip = os.path.join(scratch_dir, zip_name)
    out_zip = os.path.join(out_dir, zip_name)

    with zipfile.ZipFile(scratch_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(scratch_pdf_path, arcname="apex_real_estate_trifold_brochure.pdf")
        zipf.write(png_paths[0], arcname="trifold_brochure_page1.png")
        zipf.write(png_paths[1], arcname="trifold_brochure_page2.png")
        zipf.write(os.path.join(scratch_dir, "generate_brochure.py"), arcname="generate_brochure.py")
        zipf.write(readme_path, arcname="README.md")

    shutil.copy(scratch_zip, out_zip)
    print(f"Created ZIP package at {out_zip}")

if __name__ == "__main__":
    main()
