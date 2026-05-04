import json
import logging
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlayWrightTimeoutError

class HockeyScraper:
    URL = "https://www.scrapethissite.com/pages"
    TEAM = "New York Rangers"

    def __init__(self, headless=True):
        self.headless = headless
        self.output_dir = Path("output")
        self.screeshot_dir = self.output_dir / "screenshots"
        self.output_file = self.output_dir / "results.json"
        self._setup_logging()

    def _setup_logging(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=self.output_dir / f"hockeyscraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
            level = logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        self.logger = logging.getLogger("Scraper")

    def _screenshot(self, page, name):
        try:
            self.screeshot_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = self.screeshot_dir / f"{ts}_{name}.png"
            page.screenshot(path=str(path), full_page=True)
            self.logger.info(f"Screenshot: {path} ")
        except Exception as e:
            self.logger.warning(f"Screenshot failed : {e} ")

    def _step(self, page, name, func):
        try:
            self.logger.info(f"Step : {name}")
            result = func()
            self._screenshot(page, name)
            return result
        except PlayWrightTimeoutError:
            self.logger.error(f"Timeout at step : {name}")
            self._screenshot(page, f"ERROR_{name}")
            raise
        except Exception as e:
            self.logger.error("Error at step {name} : {e}")
            self._screenshot(page, f"ERROR_{name}")
            raise
    
    def extract_data(self, page):

        totals = {
            "wins" : 0,
            "losses" : 0,
            "goals_scored" : 0,
            "goals_against" : 0
        }

        yearly_data = {}
        page_number = 1

        while True:
            self.logger.info(f"Processing Page: {page_number}")
            rows = page.locator("table tbody tr.team")
            if rows.count() == 0:
                raise Exception("No rows found")
            for i in range(rows.count()):
                row = rows.nth(i)
                name = row.locator("td.name").inner_text().strip()
                if self.TEAM.lower() not in name.lower():
                    continue
                try:
                    year = int(row.locator("td.year").inner_text())
                    wins = int(row.locator("td.wins").inner_text())
                    losses = int(row.locator("td.losses").inner_text())
                    goals_for = int(row.locator("td.gf").inner_text())
                    goals_against = int(row.locator("td.ga").inner_text())
                except Exception:
                    self.logger.warning("Skipping row due to parsing issue")
                    continue
                yearly_data[year] = {
                    "year" : year,
                    "wins" : wins,
                    "losses" : losses,
                    "goals_scored" : goals_for,
                    "goals_against" : goals_against
                    }
                totals['wins'] += wins
                totals['losses'] += losses
                totals['goals_scored'] += goals_for
                totals['goals_against'] += goals_against
            
            self._screenshot(page, f"page_{page_number}")
            next_btn = page.locator("li.next:not(.disabled) a")

            if next_btn.count() > 0:
                next_btn.click()
                page.wait_for_selector("table tbody tr")
                page_number += 1
            else:
                break
        yearly_list = sorted(yearly_data.values(), key= lambda x : x["year"])
        return totals, yearly_list
    
    def run(self):
        result = {
            'team' : self.TEAM,
            'totals' : {},
            'yearly_performance' : [],
            'status' : "failed",
            'error' : None,
            'scraped_at' : datetime.now().isoformat()
            }
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()

            try:
                self._step(page, "01_home", lambda: page.goto(self.URL))
                page.wait_for_load_state("networkidle")

                self._step(page, "02_hockey_page", lambda: page.get_by_role("link", name="Hockey Teams: Forms,").click())
                page.wait_for_load_state("networkidle")

                def search():
                    page.get_by_role("textbox", name="Search for Teams:").fill(self.TEAM)
                    page.get_by_role("button", name="Search").click()
                    page.wait_for_selector("table tbody tr", timeout=10000)

                self._step(page, "03_search", search)

                totals, yearly = self._step(page, "04_extract", lambda : self.extract_data(page))
                result["totals"] = totals
                result["yearly_performance"] = yearly
                result["status"] = "success"
            
            except Exception as e:
                self.logger.error(f"Scraper failed : {e}")
                result["error"] = str(e)

            finally:
                browser.close()

        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, "w") as f:
            json.dump(result, f, indent = 4)

        self.logger.info(f"Final Output : {result}")
        return result
    
if __name__ == "__main__":
    scraper = HockeyScraper(headless=True)
    output = scraper.run()
    print(json.dumps(output, indent=4))
