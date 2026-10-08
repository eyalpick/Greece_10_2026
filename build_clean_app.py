import json
import codecs
import re
from guide_text import GUIDE_TEXT

# Updated static weather based on Gemini's 08/10 forecast
MANUAL_WEATHER = {
    13: {
        "summary": "שמש ברובה, יבש ונוח",
        "temp": "ביום 19°C | בלילה 9°C",
        "rain": "1% (יבש)",
        "focus": ""
    },
    14: {
        "summary": "שמש ברובה, תנאים נוחים ויציבים",
        "temp": "ביום 19°C | בלילה 9°C",
        "rain": "0% (יבש לחלוטין)",
        "focus": "תנאים אידיאליים לירידה לקניון לוסיוס (Lousios Gorge) ולמעבר בין המנזרים ללא חשש מסלעים רטובים."
    },
    15: {
        "summary": "שילוב של שמש ועננות, ייתכן ממטר מקומי קל אחה\"צ",
        "temp": "18°C ביום, 9°C בלילה (ברכס הגבוה כ-13°C–14°C עם רוח ערה)",
        "rain": "49%",
        "focus": "מומלץ לצאת מוקדם כדי לעבור את מעבר ההרים (זיוגוביסטי) לפני שעות הצהריים."
    },
    16: {
        "summary": "מעונן עם גשם בחלק ניכר משעות היום",
        "temp": "ביום 18°C | בלילה 8°C",
        "rain": "60%",
        "focus": "יום גשום המצריך מעיל גשם, כיסוי לתרמיל והליכה זהירה במדרונות חלקים."
    },
    17: {
        "summary": "התבהרות מהירה, שמש ועננות חלקית, יציב ויבש",
        "temp": "ביום 17°C | בלילה 8°C",
        "rain": "1% (יבש לחלוטין)",
        "focus": ""
    },
    18: {
        "summary": "מעונן ברובו עם פרקי שמש, סיכוי נמוך לטפטוף",
        "temp": "ביום 18°C | בלילה 9°C",
        "rain": "25%",
        "focus": ""
    }
}

parts = re.split(r'\n(?=יום \d+ \|)', GUIDE_TEXT.strip())
day_texts = {}
for p in parts:
    p = p.strip()
    if p.startswith('יום '):
        num = int(re.search(r'יום (\d+)', p).group(1))
        lines = p.split('\n')
        content = '<br>'.join(lines[1:]).strip()
        day_texts[num] = content

with open(r'C:\Users\Eyal Pick\.gemini\antigravity\brain\4dd4cf76-c8a9-4f41-a9e9-14b74fb877a7\scratch\menalon.json', 'r', encoding='utf-8') as f:
    df = json.load(f)

html = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>לוח בקרה - יוון 2026 - Menalon Trail</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
        :root {
            --bg-main: #0b0f19;
            --bg-card: rgba(30, 41, 59, 0.45);
            --border-card: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --accent-orange: #f97316;
            --accent-blue: #3b82f6;
            --accent-red: #ef4444;
            --accent-green: #10b981;
            --font-body: 'Inter', sans-serif;
            --radius-lg: 16px;
            --radius-md: 12px;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg-main);
            color: var(--text-primary);
            font-family: var(--font-body);
            min-height: 100vh;
            line-height: 1.6;
            padding-bottom: 3rem;
            font-size: 19px;
        }
        .dashboard-container { max-width: 1200px; margin: 0 auto; padding: 2rem 1.5rem; }
        .header-card {
            background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(30, 41, 59, 0.45) 100%);
            border: 1px solid var(--accent-orange);
            border-radius: var(--radius-lg);
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 0 20px 2px rgba(249, 115, 22, 0.15);
        }
        .header-card h1 { font-family: 'Outfit', sans-serif; font-size: 2.8rem; margin-bottom: 0.5rem; color: #fff; }
        .header-card p { color: var(--accent-orange); font-size: 1.3rem; font-weight: 500; }
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-md);
            padding: 1.5rem;
            margin-bottom: 2rem;
        }
        .card-header h2 { font-size: 1.7rem; color: var(--accent-orange); margin-bottom: 0.5rem; }
        .card-header p.stats { color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border-card); padding-bottom: 1rem; }
        
        .info-block {
            background: rgba(0,0,0,0.2);
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.25rem;
            border-right: 4px solid var(--accent-blue);
        }
        .info-block h4 { color: var(--accent-blue); margin-bottom: 0.75rem; font-size: 1.3rem; }
        .info-block p { color: var(--text-primary); font-size: 1.1rem; line-height: 1.8; }
        
        .weather-block { border-right-color: #a855f7; }
        .weather-block h4 { color: #a855f7; }
        
        .eats-block { border-right-color: var(--accent-green); }
        .eats-block h4 { color: var(--accent-green); }
        
        .hotel-block { border-right-color: var(--accent-orange); }
        .hotel-block h4 { color: var(--accent-orange); }
        
        .docs-list { list-style: none; display: flex; flex-wrap: wrap; gap: 1rem; }
        .docs-list li a {
            display: inline-block;
            background: rgba(255,255,255,0.05);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            color: #fff;
            text-decoration: none;
            border: 1px solid var(--border-card);
            transition: 0.2s;
            font-size: 1.1rem;
        }
        .docs-list li a:hover { background: rgba(255,255,255,0.1); border-color: var(--accent-blue); color: var(--accent-blue); }
        
        @media (max-width: 768px) {
            .dashboard-container { padding: 0.5rem 0.25rem; }
            .header-card { padding: 1.25rem 0.5rem; border-radius: 8px; margin-bottom: 1rem; }
            .header-card h1 { font-size: 1.9rem; }
            .card { padding: 1rem 0.75rem; border-radius: 8px; margin-bottom: 1.5rem; }
            .card-header h2 { font-size: 1.4rem; }
            .info-block { padding: 1rem 0.75rem; }
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        
        <header class="header-card">
            <h1>יוון 2026 - Menalon Trail</h1>
            <p>13 באוקטובר - 22 באוקטובר 2026</p>
            <div style="margin-top:1.5rem;">
                <p style="font-size:1.1rem; color:var(--text-muted);"><i class="fa-solid fa-cloud-sun" style="color:#a855f7;"></i> תחזית מזג אוויר מסונכרנת מול ספארק-ג'ימני (עודכן: 08/10)</p>
            </div>
        </header>

        <div class="card">
            <div class="card-header">
                <h2 style="color: var(--accent-blue);"><i class="fa-solid fa-folder-open"></i> מסמכים שימושיים</h2>
            </div>
            <ul class="docs-list">
                <li><a href="menalon_trail_guide_v2.pdf" target="_blank"><i class="fa-solid fa-book" style="color:#3b82f6;"></i> מדריך שביל מנלון</a></li>
                <li><a href="Mainalon_In_Search_of_Arcadia_-_Matt_Stanley.pdf" target="_blank"><i class="fa-solid fa-book-open" style="color:#f97316;"></i> ספר Arcadia</a></li>
            </ul>
        </div>
        
        <div id="days-container">
"""

month = "באוקטובר"

for i, row in enumerate(df):
    date_val = row.get("תאריך")
    if date_val is None: continue
    
    day_num = i + 1
    date_int = int(date_val)
    date_text = f"{date_int} {month} (יום {row.get('יום בשבוע', '')})"
    title_he = row.get("מסלול", "יום התארגנות")
    if not title_he: title_he = "יום התארגנות"
    
    km = row.get('ק"מ')
    time_est = row.get('זמן משוער')
    elev_up = row.get('עלייה מצטברת')
    elev_down = row.get('ירידה מצטברת')
    
    stats = []
    if km: stats.append(f'<i class="fa-solid fa-person-walking"></i> {km} ק"מ')
    if time_est: stats.append(f'<i class="fa-solid fa-clock"></i> {time_est}')
    if elev_up: stats.append(f'<i class="fa-solid fa-arrow-trend-up"></i> {elev_up}')
    if elev_down: stats.append(f'<i class="fa-solid fa-arrow-trend-down"></i> {elev_down}')
    
    drive_time_html = " | ".join(stats) if stats else "יום התארגנות / נסיעות"
    
    hotel = row.get('מלון הזמנה', '')
    if not hotel: hotel = row.get('מלון', '')
        
    hotel_notes = row.get('הערות למלון', '')
    price_euro = row.get('מחיר אירו')
    if hotel_notes is None: hotel_notes = ''
    if price_euro: hotel_notes += f". מחיר: €{price_euro}"
    
    eats = row.get('אוכל במסלול')
    desc = row.get('תיאור')
    notes = row.get('הערות לטיול')
    
    html += f'''
        <div class="card">
            <div class="card-header">
                <h2>יום {day_num} - {date_text} <span style="color:#fff; font-size:1.6rem; display:block; margin-top:0.5rem;">{title_he}</span></h2>
                <p class="stats">{drive_time_html}</p>
            </div>
    '''
    
    # Static weather block from Gemini
    w_data = MANUAL_WEATHER.get(date_int)
    if w_data:
        focus_html = f'<div class="weather-focus" style="margin-top:10px; padding:10px; background:rgba(168, 85, 247, 0.2); border-radius:6px;"><strong>דגש יומי והמלצות:</strong> {w_data["focus"]}</div>' if w_data.get("focus") else ''
        
        html += f'''
            <div class="info-block weather-block">
                <h4><i class="fa-solid fa-cloud-sun"></i> תחזית מזג אוויר</h4>
                <div style="font-size:1.1rem;">
                    <p class="w-summary"><strong>מזג אוויר:</strong> {w_data["summary"]}</p>
                    <p class="w-temp"><strong>טמפרטורות:</strong> {w_data["temp"]}</p>
                    <p class="w-rain"><strong>סיכוי למשקעים:</strong> {w_data["rain"]}</p>
                    {focus_html}
                </div>
            </div>
        '''

    if eats:
        html += f'''
            <div class="info-block eats-block">
                <h4><i class="fa-solid fa-utensils"></i> הצטיידות ומזון במסלול</h4>
                <p>{eats}</p>
            </div>
        '''

    pdf_info = day_texts.get(day_num - 1, "")
    
    if desc or notes or pdf_info:
        desc_text = str(desc or '')
        if notes: desc_text += '<br><br><strong>הערות לטיול:</strong> ' + str(notes)
        if pdf_info: desc_text += '<br><br><div style="background:rgba(59, 130, 246, 0.15); padding: 15px; border-radius: 8px; border-right: 3px solid #3b82f6; margin-top:10px;"><h4 style="color:#3b82f6; margin-bottom:10px; font-size: 1.15rem;"><i class="fa-solid fa-book"></i> מדריך מנלון (פירוט מהמסמך):</h4>' + pdf_info + '</div>'
        
        html += f'''
            <div class="info-block">
                <h4><i class="fa-solid fa-map-location-dot"></i> פירוט המסלול</h4>
                <p>{desc_text}</p>
            </div>
        '''
        
    if hotel:
        maps_link = f"https://www.google.com/maps/search/?api=1&query={hotel.replace(' ', '+')}"
        html += f'''
            <div class="info-block hotel-block">
                <h4><i class="fa-solid fa-bed"></i> מקום לינה: {hotel}</h4>
                <p>{hotel_notes}</p>
                <a href="{maps_link}" target="_blank" class="btn"><i class="fa-solid fa-map-pin"></i> נווט ל-{hotel} ב-Google Maps</a>
            </div>
        '''
        
    html += '</div>\n'

html += """
        </div>
    </div>
    
    <script>
        // JS Weather engine disabled to prevent overriding accurate Gemini/AccuWeather forecasts.
        // localStorage is cleared to reset state.
        window.addEventListener('DOMContentLoaded', () => {
            localStorage.removeItem('menalon_weather');
            localStorage.removeItem('menalon_weather_time');
        });
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
