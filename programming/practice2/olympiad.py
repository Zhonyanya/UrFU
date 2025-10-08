def check_winners(scores, student_score):
    """
    Определяет, попал ли в тройку победителей ученик

    Args:
        scores (list): Общий список баллов всех учеников
        student_score (int): Число баллов у ученика

    Example:
        check_winners([20, 48, 52, 38, 36, 13, 7, 41, 34, 24, 5, 51, 9, 14, 28, 0], 52)
        Вы в тройке победителей!
    """
    scores = sorted(scores, reverse=True)
    if student_score in scores[:3]:
        print("Вы в тройке победителей!")
    else:
        print("Вы не попали тройку победителей.")
