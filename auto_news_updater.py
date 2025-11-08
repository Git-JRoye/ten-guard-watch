#!/usr/bin/env python3
"""
Automated News Updater for TenGuard Watch
Updates the tenguardwatch.html file with latest cybersecurity news
"""

import requests
from bs4 import BeautifulSoup
import os
import re
import logging
from datetime import datetime
import time
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_updater.log'),
        logging.StreamHandler()
    ]
)

def fetch_hacker_news():
    """Fetch latest articles from The Hacker News"""
    try:
        url = "https://thehackernews.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        
        for item in soup.find_all("div", class_="body-post clear")[:6]:
            try:
                title = item.find("h2").text.strip()
                link = item.find("a")["href"]
                summary = item.find("div", class_="home-desc").text.strip()
                articles.append({"title": title, "link": link, "summary": summary, "source": "The Hacker News"})
            except Exception as e:
                logging.warning(f"Error parsing Hacker News article: {e}")
                continue
                
        logging.info(f"Successfully fetched {len(articles)} articles from Hacker News")
        return articles
    except Exception as e:
        logging.error(f"Error fetching Hacker News: {e}")
        return []

def fetch_dark_reading():
    """Fetch latest articles from Dark Reading"""
    try:
        url = "https://www.darkreading.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        
        for item in soup.find_all("article")[:5]:
            try:
                title_tag = item.find("h3") or item.find("h2")
                if title_tag:
                    title = title_tag.text.strip()
                    link_tag = title_tag.find("a")
                    if link_tag and link_tag.get("href"):
                        link = url + link_tag["href"] if not link_tag["href"].startswith("http") else link_tag["href"]
                        summary = item.find("p").text.strip() if item.find("p") else ""
                        articles.append({"title": title, "link": link, "summary": summary, "source": "The Hacker News"})
            except Exception as e:
                logging.warning(f"Error parsing Dark Reading article: {e}")
                continue
                
        logging.info(f"Successfully fetched {len(articles)} articles from Dark Reading")
        return articles
    except Exception as e:
        logging.error(f"Error fetching Dark Reading: {e}")
        return []

def fetch_security_week():
    """Fetch latest articles from SecurityWeek"""
    try:
        url = "https://www.securityweek.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        
        # Try multiple selectors to find articles
        selectors_to_try = [
            "section.zox-art-wrap.zoxrel.zox-art-small",
            "div.zox-art-wrap",
            "article",
            "div.post-item"
        ]
        
        items = []
        for selector in selectors_to_try:
            items = soup.select(selector)[:6]  # Get top 6 to allow for deduplication
            if items:
                logging.info(f"Found {len(items)} items using selector: {selector}")
                break
        
        if not items:
            # Fallback: look for any article-like structure
            items = soup.find_all(["article", "div"], class_=lambda x: x and any(word in x.lower() for word in ["post", "article", "news", "item"]))[:6]
        
        for i, item in enumerate(items):
            try:
                logging.info(f"Processing SecurityWeek item {i+1}")
                
                # Find the link first (it's the parent of the heading)
                link_tag = item.find("a")
                if not link_tag:
                    logging.warning(f"No link tag found in item {i+1}")
                    continue
                
                # Find the heading inside the link
                title_tag = link_tag.find(["h1", "h2", "h3", "h4"])
                if not title_tag:
                    logging.warning(f"No title tag found in item {i+1}")
                    continue
                
                title = title_tag.get_text().strip()
                link = link_tag.get("href", "")
                
                # Make sure link absolute
                if link.startswith("/"):
                    link = url + link
                elif not link.startswith("http"):
                    link = url + "/" + link
                
                # Find summary in p.zox-s-graph
                summary = ""
                p_graph = item.find("p", class_="zox-s-graph")
                if p_graph:
                    summary = p_graph.get_text().strip()
                
                if title and link:
                    articles.append({
                        "title": title, 
                        "link": link, 
                        "summary": summary, 
                        "source": "SecurityWeek"
                    })
                    logging.info(f"Added SecurityWeek article: {title[:50]}...")
                    
            except Exception as e:
                logging.warning(f"Skipping SecurityWeek article due to error: {e}")
                continue
                
        logging.info(f"Successfully fetched {len(articles)} articles from SecurityWeek")
        return articles
        
    except Exception as e:
        logging.error(f"Error fetching from SecurityWeek: {e}")
        return []

def fetch_bleepingcomputer():
    """Fetch latest articles from BleepingComputer"""
    try:
        url = "https://www.bleepingcomputer.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        
        # Based on screenshot: articles are in ul#bc-home-news-main-wrap > li
        # Title is in h4.bc_latest_news_text > a
        items = soup.select("ul#bc-home-news-main-wrap li")[:15]  # Get more to filter
        
        if not items:
            # Fallback: try alternative selectors
            items = soup.select("li.bc_latest_news_item, li.article-item, article, div.bc_latest_news_text")[:15]
        
        logging.info(f"Found {len(items)} potential items from BleepingComputer")
        
        for i, item in enumerate(items):
            try:
                title = None
                link = None
                summary = ""
                
                # Method 1: Find h4 with class bc_latest_news_text (from screenshot)
                h4_tag = item.find("h4", class_="bc_latest_news_text")
                if h4_tag:
                    link_tag = h4_tag.find("a", href=True)
                    if link_tag:
                        title = link_tag.get_text().strip()
                        link = link_tag.get("href")
                
                # Method 2: If no h4 found, try finding any h4 with a link
                if not title or not link:
                    h4_tag = item.find("h4")
                    if h4_tag:
                        link_tag = h4_tag.find("a", href=True)
                        if link_tag:
                            title = link_tag.get_text().strip()
                            link = link_tag.get("href")
                
                # Method 3: Try finding any link with a substantial title
                if not title or not link:
                    link_tag = item.find("a", href=True)
                    if link_tag:
                        potential_title = link_tag.get_text().strip()
                        # Only use if it looks like a title (not too short, not too long)
                        if len(potential_title) > 20 and len(potential_title) < 200:
                            title = potential_title
                            link = link_tag.get("href")
                
                if link:
                    # Make sure link is absolute
                    if link.startswith("/"):
                        link = url.rstrip("/") + link
                    elif not link.startswith("http"):
                        link = url + link
                    
                    # Find summary/excerpt
                    # Look for summary in the item
                    summary_elem = item.find("p", class_=lambda x: x and ("excerpt" in str(x).lower() or "summary" in str(x).lower()))
                    if not summary_elem:
                        summary_elem = item.find("div", class_=lambda x: x and ("excerpt" in str(x).lower() or "summary" in str(x).lower()))
                    if summary_elem:
                        summary = summary_elem.get_text().strip()
                    else:
                        # Try first paragraph
                        p_tag = item.find("p")
                        if p_tag:
                            summary = p_tag.get_text().strip()
                            if len(summary) > 300:
                                summary = summary[:300] + "..."
                    
                    if title and link:
                        articles.append({
                            "title": title,
                            "link": link,
                            "summary": summary,
                            "source": "BleepingComputer"
                        })
                        logging.info(f"Added BleepingComputer article: {title[:50]}...")
                        
                        # Stop after getting 6 articles (will be deduplicated later)
                        if len(articles) >= 6:
                            break
                else:
                    logging.debug(f"No link found in BleepingComputer item {i+1}")
                    
            except Exception as e:
                logging.warning(f"Skipping BleepingComputer article due to error: {e}")
                continue
                
        logging.info(f"Successfully fetched {len(articles)} articles from BleepingComputer")
        return articles
        
    except Exception as e:
        logging.error(f"Error fetching from BleepingComputer: {e}")
        return []

def fetch_cybersecurity_news():
    """Fetch from Cybersecurity News as backup source"""
    try:
        url = "https://cybersecuritynews.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        
        for item in soup.find_all("article")[:3]:  # Get fewer articles as backup
            try:
                title_tag = item.find("h2") or item.find("h3")
                if title_tag:
                    title = title_tag.text.strip()
                    link_tag = title_tag.find("a")
                    if link_tag and link_tag.get("href"):
                        link = link_tag["href"] if link_tag["href"].startswith("http") else url + link_tag["href"]
                        summary = item.find("p").text.strip() if item.find("p") else ""
                        articles.append({"title": title, "link": link, "summary": summary, "source": "Cybersecurity News"})
            except Exception as e:
                logging.warning(f"Error parsing Cybersecurity News article: {e}")
                continue
                
        logging.info(f"Successfully fetched {len(articles)} articles from Cybersecurity News")
        return articles
    except Exception as e:
        logging.error(f"Error fetching Cybersecurity News: {e}")
        return []

def normalize_title(title):
    """Normalize title for comparison by removing special chars and converting to lowercase"""
    if not title:
        return ""
    # Convert to lowercase
    normalized = title.lower()
    # Remove special characters and extra spaces
    normalized = re.sub(r'[^\w\s]', '', normalized)
    # Remove extra spaces
    normalized = ' '.join(normalized.split())
    return normalized

def are_titles_similar(title1, title2, threshold=0.7):
    """
    Check if two titles are similar (same story from different sources)
    Uses normalized title comparison and word overlap
    """
    if not title1 or not title2:
        return False
    
    norm1 = normalize_title(title1)
    norm2 = normalize_title(title2)
    
    # Exact match after normalization
    if norm1 == norm2:
        return True
    
    # Check if one title contains the other (for cases like "Article Title" vs "Article Title - Updated")
    if len(norm1) > 20 and len(norm2) > 20:
        if norm1 in norm2 or norm2 in norm1:
            return True
    
    # Word-based similarity check
    words1 = set(norm1.split())
    words2 = set(norm2.split())
    
    # Remove common stopwords for better comparison
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
    words1 = words1 - stopwords
    words2 = words2 - stopwords
    
    if not words1 or not words2:
        return False
    
    # Calculate Jaccard similarity (intersection over union)
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    if union == 0:
        return False
    
    similarity = intersection / union
    
    # Also check if significant words overlap
    significant_words1 = {w for w in words1 if len(w) > 4}  # Words longer than 4 chars
    significant_words2 = {w for w in words2 if len(w) > 4}
    
    if significant_words1 and significant_words2:
        significant_overlap = len(significant_words1 & significant_words2) / len(significant_words1 | significant_words2)
        if significant_overlap >= threshold:
            return True
    
    return similarity >= threshold

def deduplicate_articles(articles):
    """
    Remove duplicate articles across different sources.
    If two articles have similar titles, keep the first one encountered.
    """
    if not articles:
        return articles
    
    unique_articles = []
    seen_titles = []
    
    for article in articles:
        title = article.get("title", "")
        is_duplicate = False
        
        # Check against all previously seen titles
        for seen_title in seen_titles:
            if are_titles_similar(title, seen_title):
                logging.info(f"Skipping duplicate article: '{title[:60]}...' (similar to: '{seen_title[:60]}...')")
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_articles.append(article)
            seen_titles.append(title)
    
    removed_count = len(articles) - len(unique_articles)
    if removed_count > 0:
        logging.info(f"Removed {removed_count} duplicate article(s). Kept {len(unique_articles)} unique articles.")
    
    return unique_articles

def create_backup(html_file):
    """Create a backup of the current HTML file"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{html_file}.backup_{timestamp}"
        with open(html_file, "r", encoding="utf-8") as original:
            with open(backup_file, "w", encoding="utf-8") as backup:
                backup.write(original.read())
        logging.info(f"Backup created: {backup_file}")
        return backup_file
    except Exception as e:
        logging.error(f"Error creating backup: {e}")
        return None

def extract_tags_and_urgency(article):
    """Extract tags and urgency from article title and summary"""
    title = article["title"].lower()
    summary = article.get("summary", "").lower()
    text = title + " " + summary
    
    # Extract tags based on keywords
    tags = []
    tag_keywords = {
        "vulnerability": ["vulnerability", "cve", "exploit", "patch"],
        "malware": ["malware", "trojan", "virus", "backdoor"],
        "phishing": ["phishing", "smishing", "social engineering"],
        "ransomware": ["ransomware", "encryption", "decrypt"],
        "breach": ["breach", "leak", "data exposure", "compromised"],
        "apt": ["apt", "nation-state", "espionage", "government"],
        "attack": ["attack", "campaign", "targeting"],
        "critical": ["critical", "zero-day", "actively exploited"]
    }
    
    for tag, keywords in tag_keywords.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)
    
    # Determine urgency
    urgency = "Low"
    if any(kw in text for kw in ["critical", "zero-day", "actively exploited", "emergency"]):
        urgency = "High"
    elif any(kw in text for kw in ["exploit", "breach", "ransomware", "attack"]):
        urgency = "Medium"
    
    return tags, urgency

def generate_slug(title):
    """Generate a URL-friendly slug from title"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:50]  # Limit length

def save_articles_to_json(articles):
    """Save articles to JSON file for trends dashboard"""
    try:
        # Create news directory if it doesn't exist
        news_dir = "news"
        os.makedirs(news_dir, exist_ok=True)
        
        # Get today's date
        date_str = datetime.now().strftime("%Y-%m-%d")
        json_file = os.path.join(news_dir, f"{date_str}.json")
        
        # Prepare items for JSON
        items = []
        for article in articles:
            tags, urgency = extract_tags_and_urgency(article)
            item = {
                "title": article["title"],
                "link": article["link"],
                "summary": article.get("summary", ""),
                "tags": tags if tags else ["cybersecurity"],
                "urgency": urgency,
                "slug": generate_slug(article["title"]),
                "source": article.get("source", "Unknown"),
                "date": date_str
            }
            items.append(item)
        
        # Save to JSON
        data = {
            "date": date_str,
            "items": items
        }
        
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Saved {len(items)} articles to {json_file}")
        return True
    except Exception as e:
        logging.error(f"Error saving articles to JSON: {e}")
        return False

def generate_professional_summary(article):
    """Generate a professional Security Weekly-style summary"""
    title = article["title"]
    summary = article["summary"]
    source = article["source"]
    
    # Create a concise, professional summary
    if len(summary) > 200:
        summary = summary[:200] + "..."
    
    # Determine impact based on keywords
    impact_keywords = {
        "critical": "Critical vulnerability requiring immediate attention and patching.",
        "exploit": "Active exploitation observed in the wild, requiring immediate defensive measures.",
        "breach": "Data breach affecting organizations and requiring incident response procedures.",
        "malware": "Malicious software campaign targeting users and organizations.",
        "phishing": "Social engineering campaign targeting users with fraudulent communications.",
        "ransomware": "Ransomware attack campaign targeting organizations for financial gain.",
        "vulnerability": "Security vulnerability affecting systems and requiring patching.",
        "threat": "Emerging threat affecting cybersecurity landscape and requiring awareness.",
        "attack": "Cyber attack campaign targeting organizations and individuals.",
        "hack": "Unauthorized access campaign targeting systems and data."
    }
    
    # Find matching impact keywords
    impact = "Cybersecurity development requiring attention and monitoring."
    for keyword, impact_text in impact_keywords.items():
        if keyword.lower() in title.lower() or keyword.lower() in summary.lower():
            impact = impact_text
            break
    
    return {
        "summary": summary,
        "impact": impact
    }

def update_html():
    """Update the HTML file with latest articles"""
    html_file = "tenguardwatch.html"
    
    if not os.path.exists(html_file):
        logging.error(f"Error: {html_file} not found.")
        return False
    
    try:
        # Create backup before updating
        backup_file = create_backup(html_file)
        
        # Read current content
        with open(html_file, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Fetch articles (fetching 6 from each source = 18 total)
        # This allows deduplication to create variable daily counts for better trend visualization
        logging.info("Fetching latest articles...")
        articles = fetch_hacker_news() + fetch_security_week() + fetch_bleepingcomputer()
        
        # Remove Dark Reading since we updated the disclaimer
        # articles = fetch_hacker_news() + fetch_dark_reading() + fetch_security_week()
        
        # Remove duplicate articles across sources
        # After deduplication, we'll have a variable number (typically 8-15 unique articles)
        # This creates meaningful trends in the daily activity chart
        logging.info(f"Checking for duplicates among {len(articles)} articles...")
        articles = deduplicate_articles(articles)
        
        # If we don't have enough articles after deduplication, try backup source
        if len(articles) < 5:
            logging.info("Not enough articles after deduplication, trying backup source...")
            backup_articles = fetch_cybersecurity_news()
            # Deduplicate backup articles too
            all_articles = articles + backup_articles
            articles = deduplicate_articles(all_articles)
        
        if not articles:
            logging.error("No articles fetched. Aborting update.")
            return False
        
        # Generate ticker items
        ticker_items = "".join([f'<div class="ticker-item">{article["title"]}</div>' for article in articles])
        
        # Generate professional service cards with Security Weekly format
        service_cards = ""
        for article in articles:
            professional = generate_professional_summary(article)
            service_cards += f'''
            <div class="service-card" data-aos="fade-up">
                <h3>{article["title"]}</h3>
                <p><strong>Summary:</strong> {professional["summary"]}</p>
                <p><strong>Impact:</strong> {professional["impact"]}</p>
                <p>Source: {article["source"]} - <a href="{article["link"]}" target="_blank">Read Full Article</a></p>
                <a href="{article["link"]}" target="_blank" class="button-link">Read Full Article</a>
            </div>'''
        
        # Update ticker section
        content = re.sub(
            r'<section class="ticker-section">.*?</section>',
            f'<section class="ticker-section">'
            f'<div class="news-ticker"><div class="ticker-wrapper">{ticker_items}</div></div>'
            f'</section>',
            content,
            flags=re.DOTALL
        )
        
        # Update cyber news section with updated disclaimer
        content = re.sub(
            r'<section class="cyber-news" data-aos="fade-up">.*?</section>',
            f'<section class="cyber-news" data-aos="fade-up">'
            f'<h1>Daily Cyber News</h1>'
            f'<p>Stay informed with the latest trends and developments in cybersecurity.</p>'
            f'<p class="disclaimer">Disclaimer: TenGuard Watch provides curated summaries of articles from trusted sources like The Hacker News, SecurityWeek, and BleepingComputer. For full content, visit the original publication by following the provided links.</p>'
            f'{service_cards}'
            f'</section>',
            content,
            flags=re.DOTALL
        )
        
        # Write updated content
        with open(html_file, "w", encoding="utf-8") as file:
            file.write(content)
        
        # Save articles to JSON for trends dashboard
        save_articles_to_json(articles)
        
        # Save update metadata
        update_info = {
            "last_update": datetime.now().isoformat(),
            "articles_count": len(articles),
            "backup_file": backup_file
        }
        
        with open("update_info.json", "w") as f:
            json.dump(update_info, f, indent=2)
        
        logging.info(f"Successfully updated {html_file} with {len(articles)} articles using professional Security Weekly format.")
        return True
        
    except Exception as e:
        logging.error(f"Error updating HTML: {e}")
        return False

def main():
    """Main function"""
    logging.info("Starting automated news update...")
    
    start_time = time.time()
    success = update_html()
    end_time = time.time()
    
    if success:
        logging.info(f"Update completed successfully in {end_time - start_time:.2f} seconds")
    else:
        logging.error("Update failed. Check logs for details.")
    
    return success

if __name__ == "__main__":
    main()
