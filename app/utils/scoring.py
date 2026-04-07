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