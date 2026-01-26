#!/usr/bin/env python3
"""
AIMC Framework v2.3 - Matrix-Layer Hybrid Visualization
========================================================
Uses Google Gemini API (Nanobanana) with ASCII Blueprint approach.

Theoretical Foundations:
- Nelson & Narens (1990): Dual-level metacognition model
- Efklides (2008): Three metacognitive dimensions
- Salomon (1993): Effects OF vs WITH technology

Setup:
    pip install google-genai
    export GOOGLE_API_KEY="your-api-key"

Author: Research Coordinator v3.1 (21-Conceptual-Framework-Visualizer)
"""

import os
from pathlib import Path

# Check for API key
API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("❌ GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
    print("   설정 방법: export GOOGLE_API_KEY='your-api-key'")
    print("   API 키 획득: https://aistudio.google.com/apikey")
    exit(1)

try:
    from google import genai
except ImportError:
    print("❌ google-genai 패키지가 설치되지 않았습니다.")
    print("   설치 방법: pip install google-genai")
    exit(1)

# =============================================================================
# ASCII BLUEPRINT (Structure Constraint)
# =============================================================================

ASCII_BLUEPRINT = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                        AIMC Framework v2.3                                   │
│         (Nelson & Narens + Efklides Theoretical Integration)                 │
└──────────────────────────────────────────────────────────────────────────────┘

                      Efklides' Metacognitive Dimensions
            ┌─────────────────┬─────────────────┬─────────────────┐
            │   KNOWLEDGE     │   EXPERIENCES   │     SKILLS      │
            │   (What)        │   (Feel)        │     (How)       │
┌───────────┼─────────────────┼─────────────────┼─────────────────┤
│           │                 │                 │                 │
│   L3      │  Task &         │  Transfer       │  Autonomous     │
│ AUTONOMOUS│  Strategy       │  JOL/FOK        │  Planning &     │
│           │  Knowledge      │  Calibration    │  Monitoring     │
│           │                 │                 │                 │
├───────────┼─────────────────┼─────────────────┼─────────────────┤
│           │                 │                 │                 │
│   L2      │  AI Capability  │  AI Calibration │  AI Selection   │
│ META-AI   │  & Limitation   │  Accuracy       │  & Evaluation   │
│ AWARENESS │  Knowledge      │  (New Construct)│  Skills         │
│           │                 │                 │                 │
├───────────┼─────────────────┼─────────────────┼─────────────────┤
│           │                 │                 │                 │
│   L1      │  Expanded       │  Supported      │  Guided         │
│ SUPPORTED │  Object-Level   │  FOD/JOL        │  Monitoring     │
│           │  Knowledge      │  (AI-enhanced)  │  & Control      │
│           │                 │                 │                 │
└───────────┴─────────────────┴─────────────────┴─────────────────┘
                                    ▲
                                    │
            ┌───────────────────────┴───────────────────────┐
            │         DISTRIBUTED METACOGNITION             │
            │       (Human-AI System Boundary)              │
            │    Based on Clark & Chalmers (1998)           │
            └───────────────────────────────────────────────┘

Arrows indicating progression:
- L1 → L2: Reflection (understanding AI's role)
- L2 → L3: Internalization (skills transfer to AI-absent contexts)
"""

# =============================================================================
# NANOBANANA PROMPT (Creative Rendering)
# =============================================================================

AIMC_PROMPT = f"""
Create a professional academic diagram for the "AI-Integrated Metacognition (AIMC) Framework v2.3".

## ASCII BLUEPRINT (Follow This Structure Exactly):
{ASCII_BLUEPRINT}

## Theoretical Foundation to Visualize:
1. **Nelson & Narens (1990)**: Dual-level model where meta-level monitors object-level
2. **Efklides (2008)**: Three metacognitive dimensions - Knowledge, Experiences, Skills
3. **Three AIMC Levels**:
   - L1 (Supported): AI-scaffolded metacognition
   - L2 (Meta-AI Awareness): Understanding AI capabilities
   - L3 (Autonomous): Skills that transfer to AI-absent contexts

## Visual Requirements:
- Create a 3x3 matrix grid with clear cell boundaries
- Row headers on the left: L3 (top), L2 (middle), L1 (bottom)
- Column headers on top: Knowledge, Experiences, Skills
- Use a professional blue gradient color scheme:
  - L3 cells: Light blue (#7BA3CC)
  - L2 cells: Medium blue (#4A7CB8)
  - L1 cells: Dark blue (#2B5797)
  - Headers: Navy (#1A365D)
- Include the "Distributed Metacognition" zone at the bottom as a separate element
- Add subtle arrows showing L1→L2→L3 progression on the left side

## Title and Labels:
- Main title at top: "AI-Integrated Metacognition (AIMC) Framework"
- Subtitle: "Integration of Nelson & Narens (1990) and Efklides (2008)"
- Each cell should contain its label text clearly
- Source citation at bottom: "Adapted from Nelson & Narens (1990), Efklides (2008)"

## Style:
- Clean, minimalist academic style suitable for journal publication (Educational Psychology Review)
- Professional, publication-ready quality
- No decorative elements, pure academic visualization
- High contrast for readability
- Sans-serif fonts (Arial or Helvetica)
- White background

Generate a high-resolution image (2048x1536 pixels).
"""

# =============================================================================
# GENERATION FUNCTIONS
# =============================================================================

def generate_aimc_image(client, model="gemini-2.0-flash-exp", prompt=AIMC_PROMPT):
    """Generate AIMC Framework image using Gemini API."""

    print(f"🎨 Generating image with {model}...")
    print(f"   Prompt length: {len(prompt)} characters")

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_modalities": ["TEXT", "IMAGE"],
        }
    )

    # Extract image from response
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data is not None:
            return part

    # If no image, check for text response
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'text'):
            print(f"   Response text: {part.text[:200]}...")

    return None


def save_image(image_part, output_path):
    """Save generated image to file."""
    if image_part is None:
        print("❌ No image generated")
        return False

    # Get image data
    image_data = image_part.inline_data.data
    mime_type = image_part.inline_data.mime_type

    # Determine extension
    ext = ".png" if "png" in mime_type else ".jpg"
    output_path = Path(output_path).with_suffix(ext)

    # Save
    with open(output_path, "wb") as f:
        f.write(image_data)

    print(f"✅ Saved: {output_path}")
    print(f"   Size: {len(image_data) / 1024:.1f} KB")
    return True


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main execution."""

    output_dir = Path(__file__).parent

    # Initialize client
    print("🔌 Connecting to Gemini API...")
    client = genai.Client(api_key=API_KEY)

    # Models to try (best quality first)
    models_to_try = [
        "gemini-3-pro-image-preview",    # Nano Banana Pro - best text rendering
        "gemini-2.5-flash-image",         # Nano Banana - fast
        "gemini-2.0-flash-exp",           # Experimental fallback
    ]

    # Try generation with available model
    image_part = None
    used_model = None

    for model in models_to_try:
        try:
            print(f"\n🎨 Trying {model}...")
            image_part = generate_aimc_image(client, model=model)
            if image_part:
                used_model = model
                break
        except Exception as e:
            print(f"   ⚠️ {model} failed: {str(e)[:100]}")
            continue

    if image_part is None:
        print("\n❌ All models failed to generate image.")
        print("   Please check your API key and model availability.")
        return

    # Save image
    output_path = output_dir / "AIMC_Framework_v2.3_Matrix.png"
    save_image(image_part, output_path)

    print(f"\n✅ Generation complete with {used_model}")
    print(f"   Output: {output_path}")


if __name__ == "__main__":
    main()
