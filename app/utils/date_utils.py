from datetime import date
from typing import List, Tuple

# checks if the experiences' dates don't overlap, returns True if overlapping
def check_date_overlap(intervals: List[Tuple[date, date|None]]) -> bool:
    intervals.sort(key=lambda x: x[0]) # sort on basis of start time

    for i in range(1, len(intervals)):
        prev_start, prev_end = intervals[i-1]
        curr_start, curr_end = intervals[i]

        if prev_end is not None and prev_start > prev_end: return True # schmea checks this already (for safety)
        if curr_end is not None and curr_start > curr_end: return True

        if prev_end is None: continue
        if curr_start < prev_end: return True

    return False