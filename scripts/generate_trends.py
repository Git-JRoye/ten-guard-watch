#!/usr/bin/env python3
"""
TenGuard Threat Trends Generator

Aggregates daily news JSON files from news/ directory and produces:
- stats/trends.json (latest aggregated metrics)
- stats/trends-YYYY-MM-DD.json (archived daily snapshot)
- threat-trends/index.html (static dashboard page)

Usage:
    python scripts/generate_trends.py [--days 30] [--sample]
"""

import json
import logging
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Common English stopwords for keyword extraction
STOPWORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
    'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
    'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
    'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them',
    'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over',
    'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work',
    'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
    'give', 'day', 'most', 'us', 'is', 'was', 'are', 'been', 'has', 'had',
    'were', 'said', 'did', 'having', 'may', 'should', 'am', 'being', 'more'
}


def extract_domain(url: str) -> str:
    """Extract domain from URL for source attribution."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        # Remove www. prefix
        domain = re.sub(r'^www\.', '', domain)
        # Clean up common patterns
        domain = domain.split('/')[0]
        return domain or 'unknown'
    except Exception as e:
        logger.warning(f"Failed to parse URL {url}: {e}")
        return 'unknown'


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text using simple tokenization.
    
    Args:
        text: Input text to extract keywords from
        min_length: Minimum word length to consider
        
    Returns:
        List of cleaned keywords
    """
    # Convert to lowercase and extract words
    words = re.findall(r'\b[a-z]+\b', text.lower())
    
    # Filter stopwords and short words
    keywords = [
        word for word in words 
        if word not in STOPWORDS and len(word) >= min_length
    ]
    
    return keywords


def load_news_files(news_dir: Path, days: int = 30) -> List[Dict[str, Any]]:
    """
    Load news JSON files from the specified date range.
    
    Args:
        news_dir: Path to news directory
        days: Number of days to look back
        
    Returns:
        List of all news items from the date range
    """
    all_items = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    logger.info(f"Loading news files from {start_date.date()} to {end_date.date()}")
    
    if not news_dir.exists():
        logger.warning(f"News directory {news_dir} does not exist")
        return all_items
    
    # Iterate through date range
    current_date = start_date
    files_loaded = 0
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        file_path = news_dir / f"{date_str}.json"
        
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Handle different JSON structures
                if isinstance(data, dict) and 'items' in data:
                    items = data['items']
                elif isinstance(data, list):
                    items = data
                else:
                    logger.warning(f"Unexpected JSON structure in {file_path}")
                    items = []
                
                # Add date to each item if not present
                for item in items:
                    if 'date' not in item:
                        item['date'] = date_str
                    all_items.extend([item] if not isinstance(items, list) else [])
                
                all_items.extend(items)
                files_loaded += 1
                logger.debug(f"Loaded {len(items)} items from {file_path}")
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse {file_path}: {e}")
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
        
        current_date += timedelta(days=1)
    
    logger.info(f"Loaded {len(all_items)} total items from {files_loaded} files")
    return all_items


def compute_metrics(items: List[Dict[str, Any]], days_7: List[Dict[str, Any]], 
                    days_30: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute all metrics from news items.
    
    Args:
        items: All items (for top articles)
        days_7: Items from last 7 days
        days_30: Items from last 30 days
        
    Returns:
        Dictionary containing all computed metrics
    """
    logger.info("Computing metrics...")
    
    # Tag counts
    tag_counts_7 = Counter()
    tag_counts_30 = Counter()
    
    for item in days_7:
        tags = item.get('tags', [])
        if isinstance(tags, list):
            tag_counts_7.update(tags)
    
    for item in days_30:
        tags = item.get('tags', [])
        if isinstance(tags, list):
            tag_counts_30.update(tags)
    
    # Urgency counts
    urgency_counts_7 = Counter()
    urgency_counts_30 = Counter()
    
    for item in days_7:
        urgency = item.get('urgency', 'Medium')
        urgency_counts_7[urgency] += 1
    
    for item in days_30:
        urgency = item.get('urgency', 'Medium')
        urgency_counts_30[urgency] += 1
    
    # Source counts (from link domain)
    source_counts = Counter()
    for item in days_30:
        source = item.get('source')
        if not source:
            link = item.get('link', '')
            source = extract_domain(link)
        source_counts[source] += 1
    
    # Keyword extraction
    all_text = []
    for item in days_30:
        title = item.get('title', '')
        summary = item.get('summary', '')
        all_text.append(f"{title} {summary}")
    
    keyword_counter = Counter()
    for text in all_text:
        keywords = extract_keywords(text)
        keyword_counter.update(keywords)
    
    # Daily counts (last 30 days)
    daily_counts = defaultdict(int)
    for item in days_30:
        date = item.get('date', '')
        if date:
            daily_counts[date] += 1
    
    # Sort daily counts by date
    sorted_daily = sorted(daily_counts.items())
    
    # Top articles (by urgency then recency)
    urgency_priority = {'High': 3, 'Medium': 2, 'Low': 1}
    sorted_items = sorted(
        items,
        key=lambda x: (
            urgency_priority.get(x.get('urgency', 'Medium'), 2),
            x.get('date', '')
        ),
        reverse=True
    )
    top_articles = sorted_items[:10]
    
    metrics = {
        'tag_counts': {
            '7_days': dict(tag_counts_7.most_common(20)),
            '30_days': dict(tag_counts_30.most_common(20))
        },
        'urgency_counts': {
            '7_days': dict(urgency_counts_7),
            '30_days': dict(urgency_counts_30)
        },
        'top_sources': dict(source_counts.most_common(10)),
        'top_keywords': dict(keyword_counter.most_common(20)),
        'daily_counts': [{'date': date, 'count': count} for date, count in sorted_daily],
        'top_articles': [
            {
                'title': item.get('title', 'Untitled'),
                'link': item.get('link', '#'),
                'summary': item.get('summary', '')[:200],
                'urgency': item.get('urgency', 'Medium'),
                'date': item.get('date', ''),
                'tags': item.get('tags', [])
            }
            for item in top_articles
        ],
        'kpis': {
            'total_7_days': len(days_7),
            'total_30_days': len(days_30),
            'top_tag': tag_counts_30.most_common(1)[0][0] if tag_counts_30 else 'N/A',
            'last_update': datetime.now().isoformat()
        }
    }
    
    logger.info("Metrics computation complete")
    return metrics


def save_metrics(metrics: Dict[str, Any], stats_dir: Path) -> None:
    """
    Save metrics to JSON files.
    
    Args:
        metrics: Computed metrics dictionary
        stats_dir: Path to stats directory
    """
    stats_dir.mkdir(parents=True, exist_ok=True)
    
    # Save current trends
    trends_path = stats_dir / 'trends.json'
    with open(trends_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved trends to {trends_path}")
    
    # Save archived snapshot
    date_str = datetime.now().strftime('%Y-%m-%d')
    archive_path = stats_dir / f'trends-{date_str}.json'
    with open(archive_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved archived trends to {archive_path}")


def generate_sample_data(stats_dir: Path) -> None:
    """Generate sample trends.json for preview purposes."""
    sample_metrics = {
        'tag_counts': {
            '7_days': {'malware': 15, 'ransomware': 12, 'phishing': 10, 'vulnerability': 8},
            '30_days': {'malware': 45, 'ransomware': 38, 'phishing': 35, 'vulnerability': 30}
        },
        'urgency_counts': {
            '7_days': {'High': 8, 'Medium': 12, 'Low': 5},
            '30_days': {'High': 25, 'Medium': 40, 'Low': 15}
        },
        'top_sources': {
            'thehackernews.com': 30,
            'securityweek.com': 25,
            'bleepingcomputer.com': 20
        },
        'top_keywords': {
            'vulnerability': 45, 'attack': 40, 'security': 38, 'data': 35,
            'breach': 30, 'malware': 28, 'ransomware': 25, 'exploit': 22
        },
        'daily_counts': [
            {'date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'), 'count': 3 + (i % 5)}
            for i in range(30, -1, -1)
        ],
        'top_articles': [
            {
                'title': 'Critical Windows Vulnerability Exploited in Wild',
                'link': 'https://example.com/article1',
                'summary': 'A critical vulnerability in Windows is being actively exploited...',
                'urgency': 'High',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'tags': ['vulnerability', 'windows', 'exploit']
            }
        ],
        'kpis': {
            'total_7_days': 25,
            'total_30_days': 80,
            'top_tag': 'malware',
            'last_update': datetime.now().isoformat()
        }
    }
    
    stats_dir.mkdir(parents=True, exist_ok=True)
    sample_path = stats_dir / 'sample-trends.json'
    with open(sample_path, 'w', encoding='utf-8') as f:
        json.dump(sample_metrics, f, indent=2, ensure_ascii=False)
    logger.info(f"Generated sample data at {sample_path}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Generate TenGuard Threat Trends')
    parser.add_argument('--days', type=int, default=30, 
                       help='Number of days to analyze (default: 30)')
    parser.add_argument('--sample', action='store_true',
                       help='Generate sample data for preview')
    args = parser.parse_args()
    
    # Setup paths
    repo_root = Path(__file__).parent.parent
    news_dir = repo_root / 'news'
    stats_dir = repo_root / 'stats'
    
    logger.info("=== TenGuard Threat Trends Generator ===")
    logger.info(f"Repository root: {repo_root}")
    logger.info(f"Days to analyze: {args.days}")
    
    if args.sample:
        logger.info("Generating sample data...")
        generate_sample_data(stats_dir)
        logger.info("Sample data generation complete")
        return
    
    # Load news items
    all_items = load_news_files(news_dir, days=args.days)
    
    if not all_items:
        logger.warning("No news items found. Generating empty metrics.")
        metrics = {
            'tag_counts': {'7_days': {}, '30_days': {}},
            'urgency_counts': {'7_days': {}, '30_days': {}},
            'top_sources': {},
            'top_keywords': {},
            'daily_counts': [],
            'top_articles': [],
            'kpis': {
                'total_7_days': 0,
                'total_30_days': 0,
                'top_tag': 'N/A',
                'last_update': datetime.now().isoformat()
            }
        }
        save_metrics(metrics, stats_dir)
        return
    
    # Filter items by time periods
    now = datetime.now()
    date_7_days_ago = (now - timedelta(days=7)).strftime('%Y-%m-%d')
    date_30_days_ago = (now - timedelta(days=30)).strftime('%Y-%m-%d')
    
    items_7_days = [item for item in all_items if item.get('date', '') >= date_7_days_ago]
    items_30_days = [item for item in all_items if item.get('date', '') >= date_30_days_ago]
    
    # Compute metrics
    metrics = compute_metrics(all_items, items_7_days, items_30_days)
    
    # Save metrics
    save_metrics(metrics, stats_dir)
    
    logger.info("=== Trends generation complete ===")


if __name__ == '__main__':
    main()

