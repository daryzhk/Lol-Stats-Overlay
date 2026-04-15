import os
import sys
from flask import Flask, render_template, jsonify
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def resource_path(relative_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)

app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static"),
)
#КД для Смолдера
Q_BASE = [5.5, 5.0, 4.5, 4.0, 3.5]
E_BASE = [24.0, 22.0, 20.0, 18.0, 16.0]
def skills_cd(base_cd: float, ability_haste:float):
    return base_cd * 100 / (100 + ability_haste)

def get_data():
    try:
        response = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False, timeout=1.5)
        data = response.json()
        stats = data["championStats"]
        attack_range = float(stats['attackRange'])
        armor_penetration = float(stats['armorPenetrationPercent'])
        armor_penetration_percent_value = (1 - armor_penetration)*100
        armor_penetration_percent = f"{armor_penetration_percent_value:.1f}%"
        damage_value = float(stats['attackDamage'])
        damage = f"{damage_value:.1f}"
        attack_speed = f"{float(stats['attackSpeed']):.2f}"
        crit_chance = f"{float(stats['critChance'])* 100}%"
        crit_damage_value = float(stats['critDamage'])
        crit_damage = f"{crit_damage_value:.1f}%"
        lifesteal = f"{float(stats['lifeSteal'])* 100:.0f}%"
        if crit_damage_value > 10:
            crit_damage_value = crit_damage_value / 100.0
        all_damage_value = damage_value * crit_damage_value
        all_damage = f"{all_damage_value:.1f}"
        #Q/E
        Q_lvl = int(data["abilities"]["Q"]["abilityLevel"])
        E_lvl = int(data["abilities"]["E"]["abilityLevel"])
        #подсчёт кулдауна
        cooldown = float(data["championStats"]["abilityHaste"])
        cdr_value = (cooldown / (100 + cooldown) * 100) if cooldown > 0 else 0
        cdr = f"{cdr_value:.1f}%"
        Q_CD = skills_cd(Q_BASE[Q_lvl-1],cooldown) if Q_lvl > 0 else None
        E_CD = skills_cd(E_BASE[E_lvl-1],cooldown) if E_lvl > 0 else None
        Q_txt = f"{Q_CD:.2f} sec" if Q_CD is not None else "нужно вкачать скилл"
        E_txt = f"{E_CD:.2f} sec" if E_CD is not None else "нужно вкачать скилл"
        return{
            "attack_range":attack_range,
            "armor_penetration_percent":armor_penetration_percent,
            "damage":damage,
            "attack_speed":attack_speed,
            "crit_chance":crit_chance,
            "crit_damage":crit_damage,
            "lifesteal":lifesteal,
            "all_damage":all_damage,
            "q": Q_txt,
            "e": E_txt,
            "cdr": cdr
        }
    
    except Exception:
        return{
            "attack_range":"—",
            "armor_penetration_percent":"—",
            "damage":"—",
            "attack_speed":"—",
            "crit_chance":"—",
            "crit_damage":"—",
            "lifesteal":"—",
            "all_damage":"—",
            "q": "—",
            "e": "—",
            "cdr": "—"
        }

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/data")
def data_route():
    return jsonify(get_data())
if __name__ == "__main__":
    app.run(debug=True)