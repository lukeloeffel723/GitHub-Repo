"""
Creates a Google Slides presentation about different types of cars and their benefits.

Requirements:
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

Setup:
    1. Go to https://console.cloud.google.com/
    2. Create a project and enable the Google Slides API
    3. Create OAuth 2.0 credentials and download as 'credentials.json'
    4. Place credentials.json in the same directory as this script
    5. Run the script — it will open a browser for authentication on first run
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/presentations"]

# ---------------------------------------------------------------------------
# Slide content
# ---------------------------------------------------------------------------

SLIDES = [
    {
        "title": "Types of Cars & Their Benefits",
        "subtitle": "A comprehensive guide to choosing the right vehicle for you",
        "layout": "title",
        "bg_color": {"red": 0.08, "green": 0.15, "blue": 0.30},
        "title_color": {"red": 1.0, "green": 1.0, "blue": 1.0},
        "body_color": {"red": 0.75, "green": 0.85, "blue": 1.0},
    },
    {
        "title": "Sedans",
        "body": (
            "• Smooth, comfortable ride for daily commuting\n"
            "• Excellent fuel efficiency — lower running costs\n"
            "• Easy to park in urban environments\n"
            "• Typically lower purchase price vs. SUVs\n"
            "• Wide model variety (compact, mid-size, full-size)\n"
            "• Best for: Commuters, families, budget-conscious drivers"
        ),
        "layout": "body",
        "bg_color": {"red": 0.95, "green": 0.97, "blue": 1.0},
        "title_color": {"red": 0.08, "green": 0.15, "blue": 0.40},
        "body_color": {"red": 0.15, "green": 0.15, "blue": 0.15},
        "accent": {"red": 0.20, "green": 0.40, "blue": 0.80},
    },
    {
        "title": "SUVs (Sport Utility Vehicles)",
        "body": (
            "• Higher seating position with better road visibility\n"
            "• Spacious interior — ideal for families and cargo\n"
            "• Available in AWD/4WD for off-road capability\n"
            "• Towing capacity for trailers and boats\n"
            "• Enhanced safety with larger crumple zones\n"
            "• Best for: Families, adventurers, outdoor enthusiasts"
        ),
        "layout": "body",
        "bg_color": {"red": 0.95, "green": 1.0, "blue": 0.96},
        "title_color": {"red": 0.05, "green": 0.35, "blue": 0.15},
        "body_color": {"red": 0.15, "green": 0.15, "blue": 0.15},
        "accent": {"red": 0.10, "green": 0.55, "blue": 0.25},
    },
    {
        "title": "Pickup Trucks",
        "body": (
            "• High towing and payload capacity\n"
            "• Versatile bed for hauling equipment and materials\n"
            "• Rugged 4WD systems for tough terrain\n"
            "• Durable build for work and commercial use\n"
            "• Modern trucks offer car-like comfort features\n"
            "• Best for: Contractors, farmers, towing, off-road driving"
        ),
        "layout": "body",
        "bg_color": {"red": 1.0, "green": 0.96, "blue": 0.92},
        "title_color": {"red": 0.45, "green": 0.20, "blue": 0.05},
        "body_color": {"red": 0.15, "green": 0.15, "blue": 0.15},
        "accent": {"red": 0.75, "green": 0.35, "blue": 0.05},
    },
    {
        "title": "Electric Vehicles (EVs)",
        "body": (
            "• Zero tailpipe emissions — better for the environment\n"
            "• Very low fuel cost (electricity vs. gasoline)\n"
            "• Minimal maintenance — no oil changes needed\n"
            "• Instant torque for responsive acceleration\n"
            "• Eligible for government tax credits and incentives\n"
            "• Best for: Eco-conscious drivers, city commuters, tech enthusiasts"
        ),
        "layout": "body",
        "bg_color": {"red": 0.92, "green": 1.0, "blue": 0.98},
        "title_color": {"red": 0.02, "green": 0.35, "blue": 0.30},
        "body_color": {"red": 0.15, "green": 0.15, "blue": 0.15},
        "accent": {"red": 0.02, "green": 0.60, "blue": 0.50},
    },
    {
        "title": "Hybrid Vehicles",
        "body": (
            "• Combines gasoline engine with electric motor\n"
            "• Significantly improved fuel economy\n"
            "• Reduced emissions compared to traditional cars\n"
            "• No range anxiety — gas engine as backup\n"
            "• Regenerative braking extends brake life\n"
            "• Best for: Long-distance drivers wanting eco benefits without full EV commitment"
        ),
        "layout": "body",
        "bg_color": {"red": 0.96, "green": 1.0, "blue": 0.93},
        "title_color": {"red": 0.10, "green": 0.38, "blue": 0.08},
        "body_color": {"red": 0.15, "green": 0.15, "blue": 0.15},
        "accent": {"red": 0.25, "green": 0.60, "blue": 0.10},
    },
    {
        "title": "Sports Cars",
        "body": (
            "• High-performance engines for thrilling acceleration\n"
            "• Precise, responsive handling and steering\n"
            "• Aerodynamic design for stability at high speeds\n"
            "• Advanced braking systems (Brembo, carbon-ceramic)\n"
            "• Iconic styling and prestige\n"
            "• Best for: Driving enthusiasts, weekend drivers, motorsport fans"
        ),
        "layout": "body",
        "bg_color": {"red": 1.0, "green": 0.94, "blue": 0.94},
        "title_color": {"red": 0.50, "green": 0.05, "blue": 0.05},
        "body_color": {"red": 0.15, "green": 0.15, "blue": 0.15},
        "accent": {"red": 0.80, "green": 0.10, "blue": 0.10},
    },
    {
        "title": "Minivans",
        "body": (
            "• Maximum passenger capacity (7–8 seats)\n"
            "• Sliding rear doors for safe, easy entry/exit\n"
            "• Flat-folding seats for flexible cargo space\n"
            "• Family-focused features: entertainment screens, USB ports\n"
            "• Smooth, quiet ride for long road trips\n"
            "• Best for: Large families, carpooling, road trip enthusiasts"
        ),
        "layout": "body",
        "bg_color": {"red": 0.97, "green": 0.94, "blue": 1.0},
        "title_color": {"red": 0.28, "green": 0.08, "blue": 0.45},
        "body_color": {"red": 0.15, "green": 0.15, "blue": 0.15},
        "accent": {"red": 0.50, "green": 0.15, "blue": 0.75},
    },
    {
        "title": "Luxury Vehicles",
        "body": (
            "• Premium materials: leather, wood trim, soft-touch surfaces\n"
            "• Advanced driver-assistance systems (ADAS)\n"
            "• Superior noise insulation for a quieter cabin\n"
            "• Cutting-edge infotainment and connectivity\n"
            "• Enhanced ride comfort with adaptive suspension\n"
            "• Best for: Business professionals, comfort seekers, technology enthusiasts"
        ),
        "layout": "body",
        "bg_color": {"red": 0.97, "green": 0.96, "blue": 0.90},
        "title_color": {"red": 0.35, "green": 0.28, "blue": 0.02},
        "body_color": {"red": 0.15, "green": 0.15, "blue": 0.15},
        "accent": {"red": 0.65, "green": 0.50, "blue": 0.05},
    },
    {
        "title": "Summary: Choosing the Right Car",
        "body": (
            "Sedan       →  Efficiency & affordability for daily driving\n"
            "SUV         →  Space, safety & versatility for families\n"
            "Pickup Truck →  Power & utility for work and adventure\n"
            "EV          →  Eco-friendly, low-cost, high-tech driving\n"
            "Hybrid      →  Fuel savings without range anxiety\n"
            "Sports Car  →  Performance & excitement on the road\n"
            "Minivan     →  Comfort & space for large families\n"
            "Luxury      →  Premium comfort, tech & prestige"
        ),
        "layout": "body",
        "bg_color": {"red": 0.08, "green": 0.15, "blue": 0.30},
        "title_color": {"red": 1.0, "green": 0.85, "blue": 0.30},
        "body_color": {"red": 0.90, "green": 0.95, "blue": 1.0},
        "accent": {"red": 1.0, "green": 0.85, "blue": 0.30},
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PT = 12700  # EMUs per point
SLIDE_W = 9144000  # EMU  (720 pt)
SLIDE_H = 5143500  # EMU  (405 pt)


def emu(pt_val: float) -> int:
    return int(pt_val * PT)


def rgb(color: dict) -> dict:
    return {"rgbColor": color}


def solid_fill(color: dict) -> dict:
    return {"solidFill": {"color": rgb(color)}}


def pt_size(pt: float) -> dict:
    return {"magnitude": pt, "unit": "PT"}


def new_text_box(object_id: str, x: float, y: float, w: float, h: float) -> dict:
    """Returns a createShape request for a text box (dimensions in points)."""
    return {
        "createShape": {
            "objectId": object_id,
            "shapeType": "TEXT_BOX",
            "elementProperties": {
                "pageObjectId": "{{SLIDE_ID}}",  # replaced at call time
                "size": {
                    "width": {"magnitude": emu(w), "unit": "EMU"},
                    "height": {"magnitude": emu(h), "unit": "EMU"},
                },
                "transform": {
                    "scaleX": 1,
                    "scaleY": 1,
                    "translateX": emu(x),
                    "translateY": emu(y),
                    "unit": "EMU",
                },
            },
        }
    }


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def get_credentials() -> Credentials:
    creds = None
    token_path = "token.json"
    creds_path = "credentials.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(
                    "credentials.json not found.\n"
                    "Download it from Google Cloud Console → APIs & Services → Credentials."
                )
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return creds


# ---------------------------------------------------------------------------
# Presentation builder
# ---------------------------------------------------------------------------

def build_slide_requests(service, presentation_id: str, slide_data: dict, slide_id: str) -> list:
    """Returns a list of batchUpdate requests to populate one slide."""
    requests = []
    layout = slide_data.get("layout", "body")
    bg = slide_data["bg_color"]

    # Background
    requests.append({
        "updatePageProperties": {
            "objectId": slide_id,
            "pageProperties": {
                "pageBackgroundFill": solid_fill(bg)
            },
            "fields": "pageBackgroundFill",
        }
    })

    if layout == "title":
        # ── Title slide ──────────────────────────────────────────────────────
        title_id = f"{slide_id}_title"
        subtitle_id = f"{slide_id}_subtitle"

        # Title box — centered, large
        requests.append({
            "createShape": {
                "objectId": title_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "width": {"magnitude": emu(620), "unit": "EMU"},
                        "height": {"magnitude": emu(100), "unit": "EMU"},
                    },
                    "transform": {
                        "scaleX": 1, "scaleY": 1,
                        "translateX": emu(50), "translateY": emu(120),
                        "unit": "EMU",
                    },
                },
            }
        })
        requests.append({
            "insertText": {"objectId": title_id, "text": slide_data["title"]}
        })
        requests.append({
            "updateTextStyle": {
                "objectId": title_id,
                "style": {
                    "bold": True,
                    "fontSize": pt_size(40),
                    "foregroundColor": solid_fill(slide_data["title_color"]),
                    "fontFamily": "Google Sans",
                },
                "fields": "bold,fontSize,foregroundColor,fontFamily",
            }
        })
        requests.append({
            "updateParagraphStyle": {
                "objectId": title_id,
                "style": {"alignment": "CENTER"},
                "fields": "alignment",
            }
        })

        # Subtitle box
        requests.append({
            "createShape": {
                "objectId": subtitle_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "width": {"magnitude": emu(580), "unit": "EMU"},
                        "height": {"magnitude": emu(60), "unit": "EMU"},
                    },
                    "transform": {
                        "scaleX": 1, "scaleY": 1,
                        "translateX": emu(70), "translateY": emu(240),
                        "unit": "EMU",
                    },
                },
            }
        })
        requests.append({
            "insertText": {"objectId": subtitle_id, "text": slide_data["subtitle"]}
        })
        requests.append({
            "updateTextStyle": {
                "objectId": subtitle_id,
                "style": {
                    "fontSize": pt_size(20),
                    "foregroundColor": solid_fill(slide_data["body_color"]),
                    "fontFamily": "Google Sans",
                },
                "fields": "fontSize,foregroundColor,fontFamily",
            }
        })
        requests.append({
            "updateParagraphStyle": {
                "objectId": subtitle_id,
                "style": {"alignment": "CENTER"},
                "fields": "alignment",
            }
        })

    else:
        # ── Content slide ────────────────────────────────────────────────────
        title_id = f"{slide_id}_title"
        body_id = f"{slide_id}_body"
        accent_bar_id = f"{slide_id}_accent"

        # Accent bar (left edge)
        accent_color = slide_data.get("accent", {"red": 0.2, "green": 0.4, "blue": 0.8})
        requests.append({
            "createShape": {
                "objectId": accent_bar_id,
                "shapeType": "RECTANGLE",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "width": {"magnitude": emu(8), "unit": "EMU"},
                        "height": {"magnitude": emu(300), "unit": "EMU"},
                    },
                    "transform": {
                        "scaleX": 1, "scaleY": 1,
                        "translateX": emu(36), "translateY": emu(52),
                        "unit": "EMU",
                    },
                },
            }
        })
        requests.append({
            "updateShapeProperties": {
                "objectId": accent_bar_id,
                "shapeProperties": {
                    "shapeBackgroundFill": solid_fill(accent_color),
                    "outline": {"outlineFill": solid_fill(accent_color)},
                },
                "fields": "shapeBackgroundFill,outline",
            }
        })

        # Title
        requests.append({
            "createShape": {
                "objectId": title_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "width": {"magnitude": emu(600), "unit": "EMU"},
                        "height": {"magnitude": emu(55), "unit": "EMU"},
                    },
                    "transform": {
                        "scaleX": 1, "scaleY": 1,
                        "translateX": emu(58), "translateY": emu(44),
                        "unit": "EMU",
                    },
                },
            }
        })
        requests.append({
            "insertText": {"objectId": title_id, "text": slide_data["title"]}
        })
        requests.append({
            "updateTextStyle": {
                "objectId": title_id,
                "style": {
                    "bold": True,
                    "fontSize": pt_size(28),
                    "foregroundColor": solid_fill(slide_data["title_color"]),
                    "fontFamily": "Google Sans",
                },
                "fields": "bold,fontSize,foregroundColor,fontFamily",
            }
        })

        # Body
        requests.append({
            "createShape": {
                "objectId": body_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "width": {"magnitude": emu(600), "unit": "EMU"},
                        "height": {"magnitude": emu(240), "unit": "EMU"},
                    },
                    "transform": {
                        "scaleX": 1, "scaleY": 1,
                        "translateX": emu(58), "translateY": emu(108),
                        "unit": "EMU",
                    },
                },
            }
        })
        requests.append({
            "insertText": {"objectId": body_id, "text": slide_data["body"]}
        })
        requests.append({
            "updateTextStyle": {
                "objectId": body_id,
                "style": {
                    "fontSize": pt_size(16),
                    "foregroundColor": solid_fill(slide_data["body_color"]),
                    "fontFamily": "Google Sans",
                },
                "fields": "fontSize,foregroundColor,fontFamily",
            }
        })

    return requests


def create_presentation() -> str:
    creds = get_credentials()
    service = build("slides", "v1", credentials=creds)

    # Create blank presentation
    presentation = service.presentations().create(
        body={"title": "Types of Cars & Their Benefits"}
    ).execute()
    presentation_id = presentation["presentationId"]
    print(f"Created presentation: https://docs.google.com/presentation/d/{presentation_id}/edit")

    # The API auto-creates one blank slide; get its ID
    existing_slide_id = presentation["slides"][0]["objectId"]

    all_requests = []

    # Build all slide-creation requests first (except first slide which exists)
    slide_ids = []
    for i, slide_data in enumerate(SLIDES):
        if i == 0:
            slide_id = existing_slide_id
        else:
            slide_id = f"slide_{i}"
            all_requests.append({
                "createSlide": {
                    "objectId": slide_id,
                    "insertionIndex": i,
                    "slideLayoutReference": {"predefinedLayout": "BLANK"},
                }
            })
        slide_ids.append(slide_id)

    # Execute slide creation first
    if all_requests:
        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": all_requests}
        ).execute()

    # Now populate each slide individually (avoids object-id conflicts)
    for slide_id, slide_data in zip(slide_ids, SLIDES):
        content_requests = build_slide_requests(service, presentation_id, slide_data, slide_id)
        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": content_requests}
        ).execute()
        print(f"  ✓ Slide added: {slide_data['title']}")

    print(f"\nDone! Open your presentation:")
    print(f"  https://docs.google.com/presentation/d/{presentation_id}/edit")
    return presentation_id


if __name__ == "__main__":
    create_presentation()
