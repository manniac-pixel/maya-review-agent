"""
Accessibility & Edge-Case Analyzer module.
Extracts device compatibility, connectivity, accessibility, and edge-case
signals from user reviews using regex pre-extraction followed by LLM analysis
with Philippines-market awareness.
"""

from __future__ import annotations

import json
import logging
import re
from collections import Counter
from pathlib import Path

import pandas as pd

import config
import llm

logger = logging.getLogger(__name__)

# ── Regex patterns for context signal extraction ────────────────────────────

DEVICE_PATTERNS = [
    re.compile(r"\b(samsung|galaxy\s*\w+)\b", re.IGNORECASE),
    re.compile(r"\b(xiaomi|redmi|poco)\b", re.IGNORECASE),
    re.compile(r"\b(oppo|realme|reno)\b", re.IGNORECASE),
    re.compile(r"\b(vivo|iqoo)\b", re.IGNORECASE),
    re.compile(r"\b(huawei|honor)\b", re.IGNORECASE),
    re.compile(r"\b(iphone|ipad)\b", re.IGNORECASE),
    re.compile(r"\b(pixel|google\s+phone)\b", re.IGNORECASE),
    re.compile(r"\b(infinix|tecno|itel)\b", re.IGNORECASE),
    re.compile(r"\b(lenovo|motorola|moto)\b", re.IGNORECASE),
    re.compile(r"\b(cherry\s*mobile|myphone)\b", re.IGNORECASE),
    re.compile(r"\b(android\s+\d+|ios\s+\d+)\b", re.IGNORECASE),
    re.compile(r"\b(old\s+(?:phone|device|model)|low[\s-]?end)\b", re.IGNORECASE),
]

CONNECTIVITY_PATTERNS = [
    re.compile(r"\b(slow\s+(?:internet|connection|data|wifi|network))\b", re.IGNORECASE),
    re.compile(r"\b(no\s+(?:signal|internet|connection|network|wifi))\b", re.IGNORECASE),
    re.compile(r"\b(poor\s+(?:signal|connection|network|coverage))\b", re.IGNORECASE),
    re.compile(r"\b(province|rural|probinsya|barrio|barangay)\b", re.IGNORECASE),
    re.compile(r"\b(mobile\s+data|prepaid|load|data\s+cap)\b", re.IGNORECASE),
    re.compile(r"\b(offline|no\s+wifi|intermittent)\b", re.IGNORECASE),
    re.compile(r"(timeout|timed?\s*out|timing\s+out|connection\s+(?:lost|error|failed))", re.IGNORECASE),
]

ACCESSIBILITY_PATTERNS = [
    re.compile(r"\b(can'?t\s+read|(?:too|very)\s+small|font\s+size|hard\s+to\s+(?:read|see))\b", re.IGNORECASE),
    re.compile(r"\b(tagalog|filipino|bisaya|cebuano|ilokano|english\s+only|language)\b", re.IGNORECASE),
    re.compile(r"\b(senior|elderly|lola|lolo|old\s+(?:age|people|person))\b", re.IGNORECASE),
    re.compile(r"\b(blind|deaf|disability|accessible|screen\s+reader)\b", re.IGNORECASE),
    re.compile(r"\b(confusing|complicated|not?\s+(?:intuitive|clear)|hard\s+to\s+(?:use|understand|navigate))\b", re.IGNORECASE),
    re.compile(r"\b(dark\s+mode|night\s+mode|contrast)\b", re.IGNORECASE),
]

EDGE_CASE_PATTERNS = [
    re.compile(r"(phone\s+(?:was\s+)?(?:stolen|lost)|lost\s+(?:my\s+)?phone)", re.IGNORECASE),
    re.compile(r"(changed?\s+(?:my\s+)?(?:sim|number|phone)|new\s+(?:sim|number|phone|device))", re.IGNORECASE),
    re.compile(r"\b(overseas|abroad|ofw|ofws?|foreign|international|out\s+of\s+(?:the\s+)?country)\b", re.IGNORECASE),
    re.compile(r"\b(dual\s+sim|two\s+(?:sims?|numbers?))\b", re.IGNORECASE),
    re.compile(r"\b((?:expired?|deactivated?)\s+(?:id|account|sim))\b", re.IGNORECASE),
    re.compile(r"\b(minor|underage|under\s+18|student)\b", re.IGNORECASE),
    re.compile(r"\b(multiple\s+accounts?|second\s+account|another\s+account)\b", re.IGNORECASE),
    re.compile(r"\b(name\s+(?:change|mismatch)|married|maiden)\b", re.IGNORECASE),
]


ACCESSIBILITY_PROMPT = """\
You are a UX researcher analyzing Maya app reviews with a focus on accessibility, \
device compatibility, and edge cases — especially relevant to the Philippines market \
where many users have budget devices, intermittent connectivity, and may be OFWs \
(Overseas Filipino Workers).

Below are {count} user reviews that contain signals about devices, connectivity, \
accessibility needs, or edge-case scenarios.

Reviews:
{reviews_text}

Return a JSON object with this exact structure:
{{
  "connectivity_issues": [
    {{
      "condition": "specific connectivity scenario (e.g. 'slow mobile data in province areas')",
      "affected_features": ["list of features that fail under this condition"],
      "evidence_count": <number>,
      "recommendation": "specific fix (e.g. 'add offline queue for transfers', 'reduce image payload')"
    }}
  ],
  "device_compatibility": [
    {{
      "device_segment": "device category (e.g. 'budget Android phones (Xiaomi, Realme)', 'older Samsung models')",
      "issues": ["specific issues on these devices"],
      "evidence_count": <number>,
      "recommendation": "specific fix (e.g. 'optimize for 2GB RAM devices', 'reduce APK size')"
    }}
  ],
  "accessibility_gaps": [
    {{
      "issue": "specific accessibility problem (e.g. 'text too small for elderly users')",
      "affected_users": "who is affected (e.g. 'senior citizens', 'non-English speakers')",
      "evidence_count": <number>,
      "recommendation": "specific fix (e.g. 'add font size settings', 'add Tagalog language option')"
    }}
  ],
  "edge_cases": [
    {{
      "scenario": "specific edge case (e.g. 'OFW trying to verify identity from abroad')",
      "current_handling": "how the app currently handles it (or fails to)",
      "evidence_count": <number>,
      "recommendation": "specific fix (e.g. 'allow international phone numbers for OTP')"
    }}
  ],
  "device_distribution": {{
    "top_mentioned_brands": [{{"brand": "Samsung", "mention_count": 15}}, ...],
    "platform_issues_split": {{"android_specific": <count>, "ios_specific": <count>, "both": <count>}}
  }}
}}

Focus on Philippines-specific context: OFW remittance needs, province connectivity, \
budget device prevalence, Tagalog/Filipino language needs. \
Return ONLY valid JSON, no markdown fences or commentary."""


def _extract_signals(reviews_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Tag reviews with context signals and collect device mentions."""
    signals = []
    device_mentions = Counter()

    for _, row in reviews_df.iterrows():
        text = str(row.get("text", ""))
        if not text.strip():
            continue

        has_device = any(p.search(text) for p in DEVICE_PATTERNS)
        has_connectivity = any(p.search(text) for p in CONNECTIVITY_PATTERNS)
        has_accessibility = any(p.search(text) for p in ACCESSIBILITY_PATTERNS)
        has_edge_case = any(p.search(text) for p in EDGE_CASE_PATTERNS)

        # Collect device brand mentions
        for pattern in DEVICE_PATTERNS:
            for match in pattern.finditer(text):
                brand = match.group(1).strip().lower()
                # Normalize brand names
                brand_map = {
                    "galaxy": "samsung", "redmi": "xiaomi", "poco": "xiaomi",
                    "realme": "oppo/realme", "reno": "oppo/realme",
                    "iqoo": "vivo", "honor": "huawei",
                    "moto": "motorola", "google phone": "google/pixel",
                }
                for prefix, normalized in brand_map.items():
                    if brand.startswith(prefix):
                        brand = normalized
                        break
                device_mentions[brand] += 1

        if has_device or has_connectivity or has_accessibility or has_edge_case:
            signals.append({
                "date": row.get("date"),
                "rating": row.get("rating"),
                "text": text,
                "platform": row.get("platform", "?"),
                "has_device": has_device,
                "has_connectivity": has_connectivity,
                "has_accessibility": has_accessibility,
                "has_edge_case": has_edge_case,
            })

    df = pd.DataFrame(signals) if signals else pd.DataFrame()
    return df, dict(device_mentions.most_common(20))


def _format_signal_reviews(df: pd.DataFrame) -> str:
    """Format signal-tagged reviews for the LLM prompt."""
    lines = []
    for _, row in df.iterrows():
        stars = "*" * int(row["rating"]) if pd.notna(row["rating"]) else "?"
        platform = row.get("platform", "?")
        tags = []
        if row.get("has_device"):
            tags.append("DEVICE")
        if row.get("has_connectivity"):
            tags.append("CONNECTIVITY")
        if row.get("has_accessibility"):
            tags.append("A11Y")
        if row.get("has_edge_case"):
            tags.append("EDGE-CASE")
        tag_str = f" [{', '.join(tags)}]"
        text = str(row["text"]).strip().replace("\n", " ")
        lines.append(f"[{stars}] [{platform}]{tag_str} {text}")
    return "\n".join(lines)


def run(reviews_df: pd.DataFrame, suffix: str = "") -> dict:
    """
    Run accessibility & edge-case analysis. Caches to data/accessibility_analysis{suffix}.json.
    """
    data_dir = config.output_dir()
    output_path = data_dir / f"accessibility_analysis{suffix}.json"
    max_signal_reviews = config.get("accessibility", "max_signal_reviews", 250)

    if output_path.exists():
        logger.info(f"Loading cached accessibility analysis from {output_path}")
        with open(output_path) as f:
            return json.load(f)

    logger.info("Running accessibility analysis: extracting context signals...")
    signal_df, device_mentions = _extract_signals(reviews_df)

    if signal_df.empty:
        logger.warning("No accessibility/edge-case signals found in reviews")
        result = {
            "total_reviews_scanned": len(reviews_df),
            "signal_reviews_found": 0,
            "connectivity_issues": [],
            "device_compatibility": [],
            "accessibility_gaps": [],
            "edge_cases": [],
            "device_distribution": {
                "top_mentioned_brands": [],
                "platform_issues_split": {"android_specific": 0, "ios_specific": 0, "both": 0},
            },
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2, default=str)
        return result

    # Prioritize low-rating reviews
    signal_df = signal_df.sort_values("rating", ascending=True).head(max_signal_reviews)

    logger.info(
        f"Found {len(signal_df)} context signal reviews "
        f"(device: {signal_df['has_device'].sum()}, "
        f"connectivity: {signal_df['has_connectivity'].sum()}, "
        f"accessibility: {signal_df['has_accessibility'].sum()}, "
        f"edge-case: {signal_df['has_edge_case'].sum()})"
    )

    reviews_text = _format_signal_reviews(signal_df)
    prompt = ACCESSIBILITY_PROMPT.format(
        count=len(signal_df),
        reviews_text=reviews_text,
    )

    model = llm.get_model()
    try:
        analysis = llm.call(model, prompt)
    except Exception as e:
        logger.error(f"Accessibility analysis LLM call failed: {e}")
        analysis = {
            "connectivity_issues": [],
            "device_compatibility": [],
            "accessibility_gaps": [],
            "edge_cases": [],
            "device_distribution": {
                "top_mentioned_brands": [],
                "platform_issues_split": {"android_specific": 0, "ios_specific": 0, "both": 0},
            },
        }

    # Enrich device_distribution with regex-extracted data
    if "device_distribution" not in analysis:
        analysis["device_distribution"] = {}
    analysis["device_distribution"]["regex_brand_mentions"] = [
        {"brand": brand, "mention_count": count}
        for brand, count in sorted(device_mentions.items(), key=lambda x: -x[1])
    ]

    result = {
        "total_reviews_scanned": len(reviews_df),
        "signal_reviews_found": len(signal_df),
        "signal_breakdown": {
            "device": int(signal_df["has_device"].sum()),
            "connectivity": int(signal_df["has_connectivity"].sum()),
            "accessibility": int(signal_df["has_accessibility"].sum()),
            "edge_case": int(signal_df["has_edge_case"].sum()),
        },
        **analysis,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    logger.info(f"Saved accessibility analysis to {output_path}")

    return result
