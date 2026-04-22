def calculate_matching_score(profile_a, profile_b):
    fields = ['cleanliness', 'noise_tolerance', 'sleep_schedule', 
              'guest_frequency', 'religion', 'study_habits',
              'smoking_preference']

    matching_score = sum(
        1 for field in fields 
        if getattr(profile_a, field) == getattr(profile_b, field)
    )
    return round(matching_score / len(fields) * 100, 2)