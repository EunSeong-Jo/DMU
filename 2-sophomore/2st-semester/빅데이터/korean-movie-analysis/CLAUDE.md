# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Korean Movie Success Analysis Project** - A big data project analyzing success factors of Korean movies from 2019-2024 using KOBIS API and Naver Movie data.

**Target**: 300 movies + 15,000 reviews
**Current Status**: Data collection code complete (Phase 1), ready for execution
**Tech Stack**: Python 3.8+, pandas, scikit-learn, selenium, KoNLPy

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Testing
```bash
cd src
python test_collection.py

# Test options:
# 1 - Test KOBIS API connection
# 2 - Test Naver crawler
# 3 - Run small-scale collection test
```

### Data Collection
```bash
cd src

# KOBIS boxoffice data (30min-1hr)
python kobis_collector.py

# Naver ratings and reviews (2-3hrs)
python naver_collector.py
```

### Configuration
API keys and settings in `.env` file (copy from `.env.example`):
```bash
KOBIS_API_KEY=your_key_here
START_DATE=2019-01-01
END_DATE=2024-12-31
MAX_MOVIES=300
DELAY_SECONDS=2
MAX_RETRIES=3
```

## Code Architecture

### Data Collection Layer (`src/`)

**KOBISCollector** (`kobis_collector.py`)
- Two-stage API workflow: Daily boxoffice → Movie details
- Auto-merges data: `kobis_boxoffice.csv` + `kobis_movie_details.csv` → `kobis_merged.csv`
- Rate limiting: Configurable delay between API calls (default: 1.0s)
- Error handling: Retry logic with exponential backoff

**NaverMovieCollector** (`naver_collector.py`)
- Three-step process: Search movie code → Get ratings → Scrape reviews
- Selenium-based: Chrome WebDriver with automatic driver management (webdriver-manager)
- Anti-bot measures: Random delays (1.5-3.5s), User-Agent headers
- Headless mode: Configurable for debugging (set `headless=False`)

### Data Flow Architecture
```
KOBIS API → kobis_boxoffice.csv → merge → kobis_merged.csv
                                 ↗
KOBIS API → kobis_movie_details.csv

Naver Search → Movie Code → Ratings Page → naver_ratings.csv
                         → Reviews Page → naver_reviews.csv (Selenium)
```

### Key Design Patterns

1. **Session Management**: Both collectors use `requests.Session()` for connection pooling
2. **Progress Tracking**: tqdm progress bars for long-running operations
3. **Graceful Degradation**: Continue on individual failures, log errors, save partial results
4. **Data Validation**: Type hints, optional returns, explicit error states

## Project Structure

```
korean-movie-analysis/
├── src/                    # Source code
│   ├── kobis_collector.py      # KOBIS API client
│   ├── naver_collector.py      # Naver crawler
│   └── test_collection.py      # Test suite
├── data/                   # Data storage (gitignored)
│   ├── raw/                   # Original collected data
│   ├── processed/             # Preprocessed data
│   └── final/                 # Analysis-ready data
├── notebooks/              # Jupyter notebooks (future)
├── visualizations/         # Generated plots (future)
├── models/                 # Trained models (future)
└── reports/               # Final reports (future)
```

## Development Guidelines

### API Usage
- **KOBIS**: Official Korean Film Council API requiring free key from https://www.kobis.or.kr/kobisopenapi
- **Rate Limits**: KOBIS has no strict limit but use delays (1-2s) for courtesy
- **Naver**: No official API - web scraping with respectful delays (2-3s minimum)

### Selenium Best Practices
- Driver lifecycle: Call `setup_driver()` before collection, `close_driver()` after
- Explicit waits: Use `WebDriverWait` with `expected_conditions` for dynamic content
- Error recovery: Reinitialize driver on WebDriverException
- Chrome options: Configured with `--disable-blink-features=AutomationControlled` to avoid detection

### Data Collection Strategy
1. Collect KOBIS data first (authoritative movie list)
2. Use KOBIS movie titles to search Naver
3. Collect ~50 reviews per movie (configurable)
4. Save incrementally to prevent data loss

### Error Handling Philosophy
- **API errors**: Log and retry with backoff (max 3 attempts)
- **Parsing errors**: Skip problematic items, continue collection
- **Network errors**: Save progress, allow manual resume
- **Validation errors**: Strict type checking at boundaries

## Common Tasks

### Adding a New Data Source
1. Create new collector class in `src/`
2. Implement similar interface: `__init__`, collection methods, error handling
3. Add test case in `test_collection.py`
4. Update `requirements.txt` if new dependencies needed

### Debugging Collection Issues
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test with small sample
collector = NaverMovieCollector(delay=3.0, headless=False)
# Watch browser behavior in non-headless mode
```

### Handling Partial Collection Failures
- Check logs: Collection scripts log all errors with timestamps
- Resume from checkpoint: Load existing CSV, skip collected movies
- Verify data integrity: Use test scripts to validate collected data

## Project Phases (5-week plan)

- **Week 1**: Data collection (current phase)
- **Week 2**: Data preprocessing → Create `preprocessing.py`
- **Week 3**: EDA and statistical analysis → Jupyter notebooks
- **Week 4**: Machine learning modeling → Random Forest + Logistic Regression
- **Week 5**: Report writing and visualization

## Research Hypotheses

- H1: Summer/winter releases have 30%+ higher audience vs spring/fall
- H2: Action/SF genres have 2x success rate vs drama/melodrama
- H3: Movies rated 8.0+ have 5x higher success rate vs 7.0-
- H4: 70%+ positive reviews correlate with 80%+ success probability

Success threshold: 3 million+ cumulative audience

## Important Notes

### Character Encoding
- All files use UTF-8 encoding
- Movie titles contain Korean characters (한글)
- Proper encoding critical for Naver search queries

### Chrome Driver Management
- Uses `webdriver-manager` for automatic ChromeDriver installation
- Updates driver automatically on version mismatch
- Fallback: Manual driver installation in PATH if webdriver-manager fails

### Git Workflow
- `.gitignore` excludes: `venv/`, `data/`, `.env`, `__pycache__/`
- Include: Source code, documentation, requirements
- Current branch: `dongyang`, main branch: `main`

### Academic Context
- Course: Big Data Programming (빅데이터응용프로그래밍)
- Institution: Dongyang Mirae University (DMU)
- Deliverable: Final report (20 pages) + presentation + public GitHub repo
