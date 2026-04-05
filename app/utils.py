# this file serves as the toolbox to put all logic for the routes
# since routes care about web stuff, the utils care about the logic, 
# sent after services has analysed the data to be complete, verifying from db
# then only the data comes to utils for calculation

from datetime import date
from typing import List, Tuple


# checks if the experiences' dates don't overlap, returns True if overlapping
def check_date_overlap(intervals: List[Tuple[date, date|None]]) -> bool:
    intervals.sort(key=lambda x: x[0]) # sort on basis of start time

    for i in range(1, len(intervals)):
        prev_start, prev_end = intervals[i-1]
        curr_start, curr_end = intervals[i]

        if prev_end is None: continue
        if curr_start < prev_end: return True

    return False


# calculate the score for tracking systems, using the resume text and job description text
def calculate_score(resume_text: str, jd_text: str) -> float:
    # matches keywords using a map

    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    if not jd_words: return 0.0

    match_count = 0 # count words that match in both sets
    for word in jd_words:
        if word in resume_words:
            match_count += 1
        
    score = (match_count/len(jd_words)) * 100 # preplanned formula for score
    return round(score,2) # 2 dec places