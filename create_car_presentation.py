"""
Creates car_types_presentation.pptx using python-pptx.

Install: pip install python-pptx
Run:     python create_car_presentation.py

Then import the .pptx into Google Slides:
  slides.google.com → File → Import slides  (or drag into Drive)
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

DARK_BLUE   = RGBColor(0x14, 0x27, 0x4E)   # title / closing bg
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
GOLD        = RGBColor(0xFF, 0xD7, 0x00)
LIGHT_GREY  = RGBColor(0xF4, 0xF6, 0xF9)   # content slide bg

# Per-slide accent colours (title bar strip)
ACCENTS = {
    "Sedans":                    RGBColor(0x33, 0x66, 0xCC),
    "SUVs":                      RGBColor(0x1E, 0x8A, 0x44),
    "Pickup Trucks":             RGBColor(0xBF, 0x5A, 0x0E),
    "Electric Vehicles (EVs)":   RGBColor(0x00, 0x99, 0x88),
    "Hybrid Vehicles":           RGBColor(0x4C, 0xAF, 0x1A),
    "Sports Cars":               RGBColor(0xCC, 0x1A, 0x1A),
    "Minivans":                  RGBColor(0x7B, 0x2F, 0xBE),
    "Luxury Vehicles":           RGBColor(0xA0, 0x7C, 0x10),
    "Summary":                   GOLD,
}

# ---------------------------------------------------------------------------
# Slide content
# ---------------------------------------------------------------------------

CONTENT_SLIDES = [
    {
        "title": "Sedans",
        "bullets": [
            "Smooth, comfortable ride for daily commuting",
            "Excellent fuel efficiency — lower running costs",
            "Easy to park in urban environments",
            "Typically lower purchase price vs. SUVs",
            "Wide model variety: compact, mid-size, full-size",
            "Best for: commuters, families, budget-conscious drivers",
        ],
    },
    {
        "title": "SUVs",
        "bullets": [
            "Higher seating position with better road visibility",
            "Spacious interior — ideal for families and cargo",
            "Available in AWD/4WD for off-road capability",
            "Strong towing capacity for trailers and boats",
            "Enhanced safety with larger crumple zones",
            "Best for: families, adventurers, outdoor enthusiasts",
        ],
    },
    {
        "title": "Pickup Trucks",
        "bullets": [
            "High towing and payload capacity",
            "Versatile bed for hauling equipment and materials",
            "Rugged 4WD systems for tough terrain",
            "Durable build suited for work and commercial use",
            "Modern trucks offer car-like comfort and tech features",
            "Best for: contractors, farmers, towing, off-road driving",
        ],
    },
    {
        "title": "Electric Vehicles (EVs)",
        "bullets": [
            "Zero tailpipe emissions — better for the environment",
            "Very low fuel cost (electricity vs. gasoline)",
            "Minimal maintenance — no oil changes needed",
            "Instant torque for responsive acceleration",
            "Eligible for government tax credits and incentives",
            "Best for: eco-conscious drivers, city commuters, tech enthusiasts",
        ],
    },
    {
        "title": "Hybrid Vehicles",
        "bullets": [
            "Combines a gasoline engine with an electric motor",
            "Significantly improved fuel economy",
            "Reduced emissions compared to traditional cars",
            "No range anxiety — gas engine acts as backup",
            "Regenerative braking extends brake life",
            "Best for: long-distance drivers wanting eco benefits without full EV commitment",
        ],
    },
    {
        "title": "Sports Cars",
        "bullets": [
            "High-performance engines for thrilling acceleration",
            "Precise, responsive handling and steering",
            "Aerodynamic design for stability at high speeds",
            "Advanced braking systems (Brembo, carbon-ceramic)",
            "Iconic styling and prestige",
            "Best for: driving enthusiasts, weekend drivers, motorsport fans",
        ],
    },
    {
        "title": "Minivans",
        "bullets": [
            "Maximum passenger capacity (7–8 seats)",
            "Sliding rear doors for safe, easy entry and exit",
            "Flat-folding seats for flexible cargo space",
            "Family-focused features: entertainment screens, USB ports",
            "Smooth, quiet ride for long road trips",
            "Best for: large families, carpooling, road trip enthusiasts",
        ],
    },
    {
        "title": "Luxury Vehicles",
        "bullets": [
            "Premium materials: leather, wood trim, soft-touch surfaces",
            "Advanced driver-assistance systems (ADAS)",
            "Superior noise insulation for a quieter cabin",
            "Cutting-edge infotainment and connectivity",
            "Enhanced ride comfort with adaptive suspension",
            "Best for: business professionals, comfort seekers, technology enthusiasts",
        ],
    },
]

SUMMARY_ROWS = [
    ("Sedan",         "Efficiency & affordability for daily driving"),
    ("SUV",           "Space, safety & versatility for families"),
    ("Pickup Truck",  "Power & utility for work and adventure"),
    ("EV",            "Eco-friendly, low-cost, high-tech driving"),
    ("Hybrid",        "Fuel savings without range anxiety"),
    ("Sports Car",    "Performance & excitement on the road"),
    ("Minivan",       "Comfort & space for large families"),
    ("Luxury",        "Premium comfort, technology & prestige"),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def set_bg(slide, colour: RGBColor):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = colour


def add_textbox(slide, text, left, top, width, height,
                font_size, bold=False, colour=WHITE, align=PP_ALIGN.LEFT, wrap=True):
    txb = slide.shapes.add_textbox(left, top, width, height)
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = colour
    run.font.name = "Calibri"
    return txb


def add_rect(slide, colour: RGBColor, left, top, width, height):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = colour
    shape.line.fill.background()   # no border
    return shape


# ---------------------------------------------------------------------------
# Slide builders
# ---------------------------------------------------------------------------

W = Inches(10)
H = Inches(7.5)


def build_title_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    set_bg(slide, DARK_BLUE)

    # Decorative gold bar
    add_rect(slide, GOLD, Inches(0), Inches(3.1), W, Inches(0.08))

    # Main title
    add_textbox(
        slide, "Types of Cars & Their Benefits",
        Inches(0.6), Inches(1.6), Inches(8.8), Inches(1.3),
        font_size=44, bold=True, colour=WHITE, align=PP_ALIGN.CENTER,
    )

    # Subtitle
    add_textbox(
        slide, "A guide to choosing the right vehicle for you",
        Inches(0.6), Inches(3.3), Inches(8.8), Inches(0.8),
        font_size=22, bold=False, colour=GOLD, align=PP_ALIGN.CENTER,
    )


def build_content_slide(prs, title: str, bullets: list):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, LIGHT_GREY)

    accent = ACCENTS.get(title, DARK_BLUE)

    # Top accent bar
    add_rect(slide, accent, Inches(0), Inches(0), W, Inches(1.1))

    # Title text on bar
    add_textbox(
        slide, title,
        Inches(0.4), Inches(0.12), Inches(9.2), Inches(0.85),
        font_size=32, bold=True, colour=WHITE,
    )

    # Bullet points
    txb = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(9.0), Inches(5.8))
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True

    for i, bullet in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = f"  •  {bullet}"
        run.font.size = Pt(19)
        run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
        run.font.name = "Calibri"

        # Bold "Best for:" label
        if bullet.startswith("Best for:"):
            run.font.bold = True
            run.font.color.rgb = accent


def build_summary_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, DARK_BLUE)

    # Gold top bar
    add_rect(slide, GOLD, Inches(0), Inches(0), W, Inches(1.1))
    add_textbox(
        slide, "Summary: Choosing the Right Car",
        Inches(0.4), Inches(0.12), Inches(9.2), Inches(0.85),
        font_size=30, bold=True, colour=DARK_BLUE,
    )

    # Two-column table layout
    col1_x = Inches(0.5)
    col2_x = Inches(5.2)
    row_h   = Inches(0.66)
    start_y = Inches(1.3)

    for i, (car_type, benefit) in enumerate(SUMMARY_ROWS):
        y = start_y + i * row_h

        # Alternating row highlight
        if i % 2 == 0:
            add_rect(slide, RGBColor(0x1E, 0x35, 0x5E), Inches(0.3), y - Inches(0.04),
                     Inches(9.4), row_h)

        add_textbox(
            slide, car_type,
            col1_x, y, Inches(4.4), row_h,
            font_size=17, bold=True, colour=GOLD,
        )
        add_textbox(
            slide, benefit,
            col2_x, y, Inches(4.6), row_h,
            font_size=17, bold=False, colour=WHITE,
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    prs = Presentation()
    prs.slide_width  = W
    prs.slide_height = H

    build_title_slide(prs)

    for slide_data in CONTENT_SLIDES:
        build_content_slide(prs, slide_data["title"], slide_data["bullets"])

    build_summary_slide(prs)

    output = "car_types_presentation.pptx"
    prs.save(output)
    print(f"Saved: {output}")
    print()
    print("To open in Google Slides:")
    print("  1. Go to slides.google.com")
    print("  2. Click File → Import slides  (or drag the file into Drive)")


if __name__ == "__main__":
    main()
