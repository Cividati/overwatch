# Overwatch Scripts

Python scripts for Overwatch stats scraping and automation:

- `program.py`, `team-scrap.py`, `easy_team_scrap.py`, `open-division.py` — scrape team/player data from Overwatch pages using BeautifulSoup/Selenium (results saved to JSON, e.g. `data.json`).
- `auto-lucio.py` — toy automation script that presses Shift every 0.2s to alternate Lúcio's speed/heal aura.
- `testes/` — scratch tests.

## Run

```bash
pip install selenium beautifulsoup4 requests
python <script>.py
```

## Tech stack

Python · BeautifulSoup · Selenium
