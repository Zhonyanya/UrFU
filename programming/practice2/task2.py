def check_winners(scores, student_score):
    scores = sorted(scores, reverse=True)
    if student_score in scores[:3]:
        print("Вы в тройке победителей!")
    else:
        print("Вы не попали тройку победителей.")
