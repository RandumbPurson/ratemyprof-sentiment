# csv (std lib)
# docs: https://docs.python.org/3/library/csv.html
import csv

# beautifulsoup
# docs: https://beautiful-soup-4.readthedocs.io/en/latest/
from bs4 import BeautifulSoup

RATINC_CLS = "Rating__StyledRating-sc-1rhvpxz-1"
RATING_CLS_rating_container = "RatingValues__StyledRatingValues-sc-6dc747-0"
RATING_CLS_num = "CardNumRating__CardNumRatingNumber-sc-17t4b9u-2"
RATING_CLS_comments = "Comments__StyledComments-dzzyvm-0"
RATING_CLS_course = "RatingHeader__StyledClass-sc-1dlkqw1-3"
RATING_CLS_date = "TimeStamp__StyledTimeStamp-sc-9q2r30-0"
RATING_ID_thumbs_up = "thumbs_up"
RATING_ID_thumbs_down = "thumbs_down"
RATING_CLS_helpful_num = "Thumbs__HelpTotalNumber-sc-19shlav-2 lihvHt"

def get_ratings(page_source):
    soup = BeautifulSoup(page_source, features="lxml")
    ratings_list = soup.find(id="ratingsList")
    ratings = []
    for rating in ratings_list.find_all(class_=RATINC_CLS):
        course = rating.find(class_=RATING_CLS_course).contents[-1]
        date = rating.find(class_=RATING_CLS_date).contents[0]
        
        scores = rating.find(class_=RATING_CLS_rating_container)
        quality, difficulty = scores.find_all(class_=RATING_CLS_num)
        quality, difficulty = quality.contents[0], difficulty.contents[0]

        comments = rating.find(class_=RATING_CLS_comments).contents[0]
        thumbs_up = rating.find(id=RATING_ID_thumbs_up).find(class_=RATING_CLS_helpful_num).contents[0]
        thumbs_downs = rating.find(id=RATING_ID_thumbs_down).find(class_=RATING_CLS_helpful_num).contents[0]

        #SCHEMA: course, date, quality, difficulty, comments, thumbs_up, thumbs_down
        ratings.append([course, date, quality, difficulty, comments, thumbs_up, thumbs_downs])
    return ratings    

SCHEMA = ["course", "date", "quality", "difficulty", "comments", "thumbs_up", "thumbs_down"]
def save_ratings(ratings, filename):
    with open(f"{filename}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(SCHEMA)
        writer.writerows(ratings)
