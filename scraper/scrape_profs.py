from RMPscraper import RMPscraper, save_info
from RMPmodules import get_ratings

import pandas as pd

def scrape_prof(prof_id, headless=True, scroll_iters=5):
    scraper = RMPscraper(
        base=f"https://www.ratemyprofessors.com/professor/{prof_id}", 
        headless=headless
    )
    scraper.find_click(".CCPAModal__StyledCloseButton-sc-10x9kq-2") # Closes cookies popup
    scraper.expand_all(max_iters=scroll_iters)
    page = scraper.source()
    scraper.driver.quit()

    return get_ratings(page, prof_id)
    
def scrape_profs(prof_csv, output, iterations=None, **kwargs):
    proffesors = pd.read_csv(prof_csv, header=0)
    school = proffesors.loc[0, "school"]
    professor_info = []
    i = 0
    SCHEMA = []
    for _, prof in proffesors.iterrows():
        if iterations is not None and i > iterations:
            break
        print(prof)
        if prof["num_ratings"] < 1:
            continue
        try:
            info, SCHEMA = scrape_prof(prof["prof_id"], **kwargs)
            professor_info.extend(info)
            i += 1
        except KeyboardInterrupt as e:
            print(f"Halting...\n{e}")

        except:
            print(f"Error getting professor data {prof}! Skipping for now...")
    
    fname = school+"-profs" if output is None else output
    save_info(professor_info,fname, SCHEMA)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("profCSV", help="The filename of the csv file containing professors and their IDs")
    parser.add_argument("-o", help="The output filename, should not include extension")
    parser.add_argument("-s", default=5, type=int, help="The max number of scroll iterations")
    parser.add_argument("--headless", default=True, help="Whether to run the chromedriver in headless mode")
    parser.add_argument("-i", type=int, help="If set, limit the number of professors to get")
    
    
    args = parser.parse_args()
    
    scrape_profs(args.profCSV, args.i, args.o, headless=args.headless, scroll_iters=args.s)
