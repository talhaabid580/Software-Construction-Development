def employee_bonus_eligibility(is_active, experience, performance_rating, attendance, has_disciplinary_action):
    
    if (is_active and experience >= 12 and performance_rating >= 4
            and attendance >= 90 and not has_disciplinary_action):
        return True
    return False


print(employee_bonus_eligibility(True, 24, 4.5, 95, False))   
print(employee_bonus_eligibility(True, 6, 5, 98, False))     
print(employee_bonus_eligibility(False, 36, 5, 100, False))  
print(employee_bonus_eligibility(True, 24, 5, 100, True))    
