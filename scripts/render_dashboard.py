#!/usr/bin/env python3
"""
Render the threat trends dashboard HTML from template and metrics.

Usage:
    python scripts/render_dashboard.py
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def render_dashboard():
    """Render the dashboard HTML from template and trends data."""
    repo_root = Path(__file__).parent.parent
    stats_dir = repo_root / 'stats'
    templates_dir = repo_root / 'templates'
    output_dir = repo_root / 'threat-trends'
    
    # Load trends data
    trends_path = stats_dir / 'trends.json'
    if not trends_path.exists():
        logger.error(f"Trends file not found: {trends_path}")
        logger.info("Run 'python scripts/generate_trends.py' first")
        return False
    
    with open(trends_path, 'r', encoding='utf-8') as f:
        metrics = json.load(f)
    
    # Prepare template data
    kpis = metrics.get('kpis', {})
    has_data = kpis.get('total_30_days', 0) > 0
    
    # Format last update
    last_update = kpis.get('last_update', '')
    try:
        dt = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
        last_update_formatted = dt.strftime('%B %d, %Y at %I:%M %p UTC')
    except:
        last_update_formatted = 'Unknown'
    
    # Prepare chart data
    tag_counts_30 = metrics.get('tag_counts', {}).get('30_days', {})
    tag_labels = list(tag_counts_30.keys())[:10]
    tag_values = [tag_counts_30[tag] for tag in tag_labels]
    
    urgency_counts_30 = metrics.get('urgency_counts', {}).get('30_days', {})
    urgency_values = [
        urgency_counts_30.get('High', 0),
        urgency_counts_30.get('Medium', 0),
        urgency_counts_30.get('Low', 0)
    ]
    
    # Determine top urgency
    if urgency_values[0] >= max(urgency_values):
        top_urgency = 'High'
        urgency_color = '#dc3545'  # Red
    elif urgency_values[1] >= max(urgency_values):
        top_urgency = 'Medium'
        urgency_color = '#ffc107'  # Yellow
    else:
        top_urgency = 'Low'
        urgency_color = '#10b981'  # Green (site theme)
    
    daily_counts = metrics.get('daily_counts', [])
    daily_labels = [item['date'] for item in daily_counts[-30:]]
    daily_values = [item['count'] for item in daily_counts[-30:]]
    
    top_keywords = metrics.get('top_keywords', {})
    keyword_labels = list(top_keywords.keys())[:10]
    keyword_values = [top_keywords[kw] for kw in keyword_labels]
    
    top_sources = list(metrics.get('top_sources', {}).items())[:10]
    top_keywords_list = list(top_keywords.items())[:15]
    
    # Get webhook URL from environment or use placeholder
    webhook_url = os.environ.get('WEBHOOK_URL', 'https://hooks.zapier.com/hooks/catch/YOUR_WEBHOOK_ID/')
    
    # Setup Jinja2
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    template = env.get_template('threat_trends.j2')
    
    # Render template
    html = template.render(
        has_data=has_data,
        kpis=kpis,
        last_update=last_update,
        last_update_formatted=last_update_formatted,
        top_urgency=top_urgency,
        urgency_color=urgency_color,
        tag_labels=tag_labels,
        tag_values=tag_values,
        urgency_values=urgency_values,
        daily_labels=daily_labels,
        daily_values=daily_values,
        keyword_labels=keyword_labels,
        keyword_values=keyword_values,
        top_articles=metrics.get('top_articles', []),
        top_sources=top_sources,
        top_keywords_list=top_keywords_list,
        webhook_url=webhook_url
    )
    
    # Write output
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / 'index.html'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"Dashboard rendered successfully: {output_path}")
    return True


if __name__ == '__main__':
    success = render_dashboard()
    exit(0 if success else 1)

