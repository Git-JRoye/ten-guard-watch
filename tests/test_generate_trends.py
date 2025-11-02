"""
Unit tests for generate_trends.py

Run with: pytest tests/test_generate_trends.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from generate_trends import (
    extract_domain,
    extract_keywords,
    load_news_files,
    compute_metrics,
    STOPWORDS
)


class TestExtractDomain:
    """Test domain extraction from URLs."""
    
    def test_extract_domain_standard_url(self):
        """Test extraction from standard HTTPS URL."""
        url = "https://www.securityweek.com/article/test"
        assert extract_domain(url) == "securityweek.com"
    
    def test_extract_domain_with_www(self):
        """Test that www. prefix is removed."""
        url = "https://www.thehackernews.com/2025/article"
        assert extract_domain(url) == "thehackernews.com"
    
    def test_extract_domain_http(self):
        """Test HTTP URL."""
        url = "http://example.com/path"
        assert extract_domain(url) == "example.com"
    
    def test_extract_domain_invalid(self):
        """Test handling of invalid URL."""
        url = "not-a-valid-url"
        result = extract_domain(url)
        assert result in ["not-a-valid-url", "unknown"]


class TestExtractKeywords:
    """Test keyword extraction."""
    
    def test_extract_keywords_basic(self):
        """Test basic keyword extraction."""
        text = "Critical vulnerability in Windows Server allows remote code execution"
        keywords = extract_keywords(text)
        
        assert "critical" in keywords
        assert "vulnerability" in keywords
        assert "windows" in keywords
        assert "server" in keywords
        
        # Stopwords should be filtered
        assert "in" not in keywords
        assert "the" not in keywords
    
    def test_extract_keywords_case_insensitive(self):
        """Test that extraction is case-insensitive."""
        text = "MALWARE Attack Targets USERS"
        keywords = extract_keywords(text)
        
        assert "malware" in keywords
        assert "attack" in keywords
        assert "targets" in keywords
        assert "users" in keywords
    
    def test_extract_keywords_min_length(self):
        """Test minimum length filtering."""
        text = "A big SQL injection in web app"
        keywords = extract_keywords(text, min_length=3)
        
        assert "sql" in keywords
        assert "injection" in keywords
        assert "web" in keywords
        assert "app" in keywords
        
        # Short words filtered
        keywords_min4 = extract_keywords(text, min_length=4)
        assert "sql" not in keywords_min4
        assert "web" not in keywords_min4
        assert "app" not in keywords_min4
    
    def test_extract_keywords_stopwords(self):
        """Test that stopwords are properly filtered."""
        text = "The vulnerability was found in the system and it allows remote access"
        keywords = extract_keywords(text)
        
        # Stopwords should not be present
        for stopword in ["the", "was", "in", "and", "it"]:
            assert stopword not in keywords
        
        # Real keywords should be present
        assert "vulnerability" in keywords
        assert "found" in keywords
        assert "system" in keywords


class TestLoadNewsFiles:
    """Test loading news JSON files."""
    
    @pytest.fixture
    def sample_news_dir(self, tmp_path):
        """Create temporary news directory with sample files."""
        news_dir = tmp_path / "news"
        news_dir.mkdir()
        
        # Create sample news files
        for i in range(5):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            data = {
                "date": date,
                "items": [
                    {
                        "title": f"Test Article {i}",
                        "link": "https://example.com/article",
                        "summary": "Test summary",
                        "tags": ["test", "malware"],
                        "urgency": "High" if i < 2 else "Medium"
                    }
                ]
            }
            
            file_path = news_dir / f"{date}.json"
            with open(file_path, 'w') as f:
                json.dump(data, f)
        
        return news_dir
    
    def test_load_news_files_basic(self, sample_news_dir):
        """Test basic file loading."""
        items = load_news_files(sample_news_dir, days=5)
        
        assert len(items) == 5
        assert all('title' in item for item in items)
        assert all('link' in item for item in items)
    
    def test_load_news_files_date_range(self, sample_news_dir):
        """Test loading with specific date range."""
        items = load_news_files(sample_news_dir, days=3)
        
        # Should load only last 3 days
        assert len(items) <= 3
    
    def test_load_news_files_nonexistent_dir(self, tmp_path):
        """Test handling of nonexistent directory."""
        fake_dir = tmp_path / "nonexistent"
        items = load_news_files(fake_dir, days=7)
        
        assert items == []
    
    def test_load_news_files_malformed_json(self, tmp_path):
        """Test handling of malformed JSON."""
        news_dir = tmp_path / "news"
        news_dir.mkdir()
        
        # Create malformed JSON file
        date = datetime.now().strftime('%Y-%m-%d')
        file_path = news_dir / f"{date}.json"
        with open(file_path, 'w') as f:
            f.write("{ invalid json }")
        
        items = load_news_files(news_dir, days=1)
        
        # Should handle gracefully and return empty list
        assert items == []


class TestComputeMetrics:
    """Test metrics computation."""
    
    @pytest.fixture
    def sample_items(self):
        """Create sample news items for testing."""
        base_date = datetime.now()
        
        items = []
        for i in range(30):
            date = (base_date - timedelta(days=i)).strftime('%Y-%m-%d')
            urgency = "High" if i < 10 else ("Medium" if i < 20 else "Low")
            
            items.append({
                "title": f"Test Article {i}",
                "link": f"https://example.com/article{i}",
                "summary": "Critical vulnerability malware attack security breach",
                "tags": ["malware", "vulnerability"] if i % 2 == 0 else ["phishing"],
                "urgency": urgency,
                "date": date
            })
        
        return items
    
    def test_compute_metrics_tag_counts(self, sample_items):
        """Test tag counting."""
        items_7 = [item for item in sample_items if item['date'] >= (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')]
        items_30 = sample_items
        
        metrics = compute_metrics(sample_items, items_7, items_30)
        
        assert 'tag_counts' in metrics
        assert '7_days' in metrics['tag_counts']
        assert '30_days' in metrics['tag_counts']
        
        # Check that tags are counted
        tags_30 = metrics['tag_counts']['30_days']
        assert 'malware' in tags_30 or 'phishing' in tags_30
    
    def test_compute_metrics_urgency_counts(self, sample_items):
        """Test urgency counting."""
        items_7 = sample_items[:7]
        items_30 = sample_items
        
        metrics = compute_metrics(sample_items, items_7, items_30)
        
        assert 'urgency_counts' in metrics
        urgency_30 = metrics['urgency_counts']['30_days']
        
        assert 'High' in urgency_30
        assert 'Medium' in urgency_30
        assert 'Low' in urgency_30
        
        # Check counts
        total = sum(urgency_30.values())
        assert total == len(items_30)
    
    def test_compute_metrics_keywords(self, sample_items):
        """Test keyword extraction in metrics."""
        items_7 = sample_items[:7]
        items_30 = sample_items
        
        metrics = compute_metrics(sample_items, items_7, items_30)
        
        assert 'top_keywords' in metrics
        keywords = metrics['top_keywords']
        
        # Should extract keywords from titles and summaries
        assert len(keywords) > 0
        assert 'vulnerability' in keywords or 'malware' in keywords
    
    def test_compute_metrics_top_articles(self, sample_items):
        """Test top articles selection."""
        items_7 = sample_items[:7]
        items_30 = sample_items
        
        metrics = compute_metrics(sample_items, items_7, items_30)
        
        assert 'top_articles' in metrics
        top_articles = metrics['top_articles']
        
        assert len(top_articles) <= 10
        
        # High urgency articles should be prioritized
        if len(top_articles) > 0:
            first_article = top_articles[0]
            assert 'title' in first_article
            assert 'urgency' in first_article
    
    def test_compute_metrics_kpis(self, sample_items):
        """Test KPI computation."""
        items_7 = sample_items[:7]
        items_30 = sample_items
        
        metrics = compute_metrics(sample_items, items_7, items_30)
        
        assert 'kpis' in metrics
        kpis = metrics['kpis']
        
        assert 'total_7_days' in kpis
        assert 'total_30_days' in kpis
        assert 'top_tag' in kpis
        assert 'last_update' in kpis
        
        assert kpis['total_7_days'] == len(items_7)
        assert kpis['total_30_days'] == len(items_30)
    
    def test_compute_metrics_empty_input(self):
        """Test handling of empty input."""
        metrics = compute_metrics([], [], [])
        
        assert metrics['kpis']['total_7_days'] == 0
        assert metrics['kpis']['total_30_days'] == 0
        assert len(metrics['top_articles']) == 0
    
    def test_compute_metrics_missing_fields(self):
        """Test handling of items with missing fields."""
        items = [
            {"title": "Test"},  # Missing other fields
            {"link": "https://example.com"},  # Missing title
            {}  # Empty item
        ]
        
        # Should not crash
        metrics = compute_metrics(items, items, items)
        
        assert 'kpis' in metrics
        assert metrics['kpis']['total_30_days'] == len(items)


class TestIntegration:
    """Integration tests for the full pipeline."""
    
    def test_full_pipeline(self, tmp_path):
        """Test the complete pipeline from files to metrics."""
        # Create news directory with sample data
        news_dir = tmp_path / "news"
        news_dir.mkdir()
        
        date = datetime.now().strftime('%Y-%m-%d')
        data = {
            "date": date,
            "items": [
                {
                    "title": "Critical Vulnerability in Windows",
                    "link": "https://www.securityweek.com/article",
                    "summary": "A critical vulnerability allows remote code execution",
                    "tags": ["vulnerability", "windows", "critical"],
                    "urgency": "High"
                },
                {
                    "title": "Phishing Campaign Targets Users",
                    "link": "https://thehackernews.com/phishing",
                    "summary": "New phishing campaign discovered targeting email users",
                    "tags": ["phishing", "email"],
                    "urgency": "Medium"
                }
            ]
        }
        
        file_path = news_dir / f"{date}.json"
        with open(file_path, 'w') as f:
            json.dump(data, f)
        
        # Load and process
        items = load_news_files(news_dir, days=1)
        assert len(items) == 2
        
        metrics = compute_metrics(items, items, items)
        
        # Verify metrics
        assert metrics['kpis']['total_30_days'] == 2
        assert len(metrics['top_articles']) == 2
        assert 'vulnerability' in metrics['top_keywords']
        assert 'phishing' in metrics['tag_counts']['30_days']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

