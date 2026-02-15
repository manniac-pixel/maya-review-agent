
import logging
from pathlib import Path
import json
import pandas as pd
import config
from rich.logging import RichHandler
from dotenv import load_dotenv
import os

load_dotenv()

# Setup simple logging
logging.basicConfig(
    level="INFO",
    handlers=[RichHandler(show_time=True, show_path=False)]
)
logger = logging.getLogger("manual_gen")

# Import modules
import visualizations
import insights_generator
import competitor_analysis
import llm

def main():
    logger.info("Starting manual report generation...")
    
    # 1. Load Data
    d = config.output_dir()
    
    # Reviews
    reviews_df = pd.read_csv(d / "raw_reviews.csv")
    if (d / "gcash_reviews.csv").exists():
        gcash_df = pd.read_csv(d / "gcash_reviews.csv")
        logger.info(f"Loaded {len(gcash_df)} GCash reviews")
    else:
        logger.warning("GCash reviews not found!")
        gcash_df = None

    # Cached Analyses
    with open(d / "temporal_analysis.json") as f:
        temporal_data = json.load(f)
    with open(d / "comprehensive_analysis.json") as f:
        comprehensive_data = json.load(f)
    
    # Funnel (Mock or Real)
    if (d / "funnel_analysis.json").exists():
        with open(d / "funnel_analysis.json") as f:
            funnel_data = json.load(f)
    else:
        funnel_data = {}
        
    # Accessibility (Mock or Real)
    if (d / "accessibility_analysis.json").exists():
        with open(d / "accessibility_analysis.json") as f:
            accessibility_data = json.load(f)
    else:
        accessibility_data = {}

    # 2. Competitor Analysis (Run if missing)
    comp_path = d / "competitor_comparison.json"
    if comp_path.exists():
        with open(comp_path) as f:
            comparison = json.load(f)
        logger.info("Loaded cached competitor comparison")
    else:
        if gcash_df is not None:
            logger.info("Running competitor analysis...")
            comparison = competitor_analysis.run(reviews_df, gcash_df)
        else:
            comparison = None

    # 3. Insights (Load Cached)
    insights_path = d / "final_insights.json"
    if insights_path.exists():
        with open(insights_path) as f:
            insights = json.load(f)
        logger.info("Loaded cached insights")
    else:
        logger.warning("final_insights.json missing! Cannot generate report without it.")
        return

    # 4. Generate Charts (Force regeneration including Funnel)
    logger.info("Regenerating charts...")
    chart_paths = visualizations.generate_all_charts(
        insights,
        temporal_data,
        comprehensive_data,
        funnel_data=funnel_data,
        reviews_df=reviews_df,
        suffix=""
    )

    # Inject funnel data into insights for markdown generation
    if funnel_data:
        insights["_funnel_highlights"] = funnel_data

    # 5. Generate Markdown
    logger.info("Regenerating Markdown report...")
    md_report = insights_generator._generate_markdown(
        insights,
        chart_paths=chart_paths,
        comparison=comparison,
        journey_map=None # Skip loading journey map for now or load if exists
    )
    
    with open(d / "maya_insights_report.md", "w") as f:
        f.write(md_report)
    logger.info(f"Saved report to {d / 'maya_insights_report.md'}")

if __name__ == "__main__":
    main()
