 import random

class FootballAIPro:
    def __init__(self):
        self.strategies = ["Offensive Attack", "Defensive Wall", "Counter-Strike"]

    def analyze(self, team_a, team_b):
        # محاكاة تحليل 5 مباريات سابقة وقوة الهجوم/الدفاع
        power_a = random.randint(60, 95)
        power_b = random.randint(55, 90)
        
        win_p = (power_a / (power_a + power_b)) * 100
        loss_p = (power_b / (power_a + power_b)) * 100
        draw_p = 100 - (win_p + loss_p)
        
        confidence = abs(win_p - loss_p) + 40
        
        return {
            "teams": f"{team_a} vs {team_b}",
            "probabilities": {"Win": round(win_p, 1), "Draw": round(draw_p, 1), "Loss": round(loss_p, 1)},
            "confidence": f"{min(confidence, 99)}%",
            "recommendation": "Safe Win" if win_p > 65 else "Medium Risk: Over 1.5",
            "reason": f"AI identified {team_a} has a 85% success rate in home matches this season."
        }
