import json
import codecs
import re
import urllib.parse
from guide_text import GUIDE_TEXT

# Default static fallback
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

with open('itineraryData.js', 'r', encoding='utf-8') as f:
    js_content = f.read()
json_str = js_content[js_content.find('['):js_content.rfind(']')+1]
df = json.loads(json_str)

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
        
        /* Accordion Day Card Styles */
        .day-card {
            padding: 0 !important;
            margin-bottom: 1.25rem !important;
            overflow: hidden;
            border: 1px solid var(--border-card);
            border-radius: var(--radius-md);
            transition: border-color 0.25s, box-shadow 0.25s;
        }
        .day-card.active {
            border-color: rgba(249, 115, 22, 0.5);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        .day-card .card-header {
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.25rem 1.5rem;
            background: rgba(255, 255, 255, 0.02);
            transition: background 0.2s ease;
            -webkit-tap-highlight-color: rgba(249, 115, 22, 0.25);
            touch-action: manipulation;
            outline: none;
        }
        .day-card .card-header * {
            pointer-events: none;
        }
        .day-card .card-header:hover {
            background: rgba(255, 255, 255, 0.05);
        }
        .header-title-group {
            flex: 1;
        }
        .day-card .card-header h2 {
            font-size: 1.5rem;
            color: var(--accent-orange);
            margin-bottom: 0.35rem;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.5rem;
        }
        .day-subtitle {
            color: #fff;
            font-size: 1.35rem;
            font-weight: 600;
        }
        .day-card .card-header p.stats {
            color: var(--text-secondary);
            font-size: 1.05rem;
            margin-bottom: 0;
            padding-bottom: 0;
            border-bottom: none;
        }
        .toggle-icon {
            font-size: 1.4rem;
            color: var(--accent-orange);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-right: 1rem;
            flex-shrink: 0;
        }
        .day-card.active .toggle-icon {
            transform: rotate(180deg);
        }
        .day-card .card-body {
            display: none;
            padding: 1.25rem 1.5rem 1.5rem 1.5rem;
            border-top: 1px solid var(--border-card);
            animation: fadeIn 0.2s ease-in-out;
        }
        .day-card.active .card-body {
            display: block;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-4px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .accordion-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
            flex-wrap: wrap;
            gap: 0.75rem;
            padding: 0 0.25rem;
        }
        .toggle-all-btn {
            background: rgba(255, 255, 255, 0.06);
            color: var(--text-primary);
            border: 1px solid var(--border-card);
            padding: 0.6rem 1.25rem;
            border-radius: 8px;
            font-size: 1.05rem;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: inherit;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        .toggle-all-btn:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: var(--accent-orange);
            color: var(--accent-orange);
        }
        .today-badge {
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
            border: 1px solid #10b981;
            font-size: 0.85rem;
            padding: 0.2rem 0.65rem;
            border-radius: 12px;
            font-weight: 600;
        }
        
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
        
        .btn { display: inline-block; background: var(--accent-blue); color: #fff; padding: 0.75rem 1.25rem; border-radius: 6px; text-decoration: none; margin-top: 0.5rem; font-size: 1.05rem; cursor: pointer; border: none; font-family: 'Inter', sans-serif;}
        .btn:hover { background: #2563eb; }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }

        @media (max-width: 768px) {
            .dashboard-container { padding: 0.5rem 0.25rem; }
            .header-card { padding: 1.25rem 0.5rem; border-radius: 8px; margin-bottom: 1rem; }
            .header-card h1 { font-size: 1.9rem; }
            .card { padding: 1rem 0.75rem; border-radius: 8px; margin-bottom: 1.5rem; }
            .day-card .card-header {
                padding: 1rem 0.75rem !important;
                touch-action: manipulation !important;
                cursor: pointer !important;
                -webkit-tap-highlight-color: rgba(249, 115, 22, 0.25) !important;
            }
            .day-card .card-header * {
                pointer-events: none !important;
            }
            .day-card .card-header h2 { font-size: 1.25rem; }
            .day-subtitle { font-size: 1.15rem; }
            .day-card .card-body { padding: 1rem 0.75rem; }
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
                <button id="weather-update-btn" class="btn" style="background: #a855f7;" onclick="fetchSmartWeather()">
                    <i class="fa-solid fa-cloud-sun"></i> עדכן תחזית חי בזמן אמת
                </button>
                <p style="font-size:0.9rem; color:var(--text-muted); margin-top:0.5rem;">שואב נתונים ממודל לוויין (Open-Meteo) ומייצר אזהרות אוטומטיות למסלול (שומר מצב גם ללא רשת)</p>
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
        
        <div id="expenses-app"></div>

        <div class="accordion-controls">
            <div style="color: var(--text-muted); font-size: 1.05rem;">
                <i class="fa-solid fa-list-check"></i> ימי המסלול (לחץ על יום לפתיחה/סגירה):
            </div>
            <button id="toggle-all-btn" class="toggle-all-btn" onclick="toggleAllDays()">
                <i class="fa-solid fa-angles-down"></i> פתח את כל הימים
            </button>
        </div>
        
        <div id="days-container">
"""

for day in df:
    day_num = day.get("dayNum")
    date_text = day.get("dateText", "")
    title_he = day.get("titleHe", "יום התארגנות")
    
    date_int_match = re.search(r'\d+', date_text)
    date_int = int(date_int_match.group()) if date_int_match else 0
    
    drive_time_html = day.get("driveTime") or "יום התארגנות / נסיעות"
    
    hotel_info = day.get("lodging")
    hotel = ""
    hotel_en = ""
    hotel_notes = ""
    hotel_maps = ""
    if hotel_info:
        hotel = hotel_info.get("nameHe", "")
        hotel_en = hotel_info.get("nameEn", "")
        hotel_notes = hotel_info.get("desc", "")
        hotel_maps = hotel_info.get("mapsUrl", "")
    
    eats = day.get("eatsDesc", "")
    activities = day.get("activities", [])
    
    html += f'''
        <div class="card day-card" id="day-card-{day_num}" data-day-date="{date_int}.10" data-day-num="{day_num}">
            <div class="card-header" role="button" tabindex="0" id="header-{day_num}">
                <div class="header-title-group">
                    <h2>
                        <span>יום {day_num} - {date_text}</span>
                        <span class="day-subtitle">{title_he}</span>
                    </h2>
                    <p class="stats">{drive_time_html}</p>
                </div>
                <i class="fa-solid fa-chevron-down toggle-icon" id="toggle-icon-{day_num}"></i>
            </div>
            <div class="card-body">
    '''
    
    w_data = MANUAL_WEATHER.get(date_int)
    if w_data:
        focus_html = f'<div class="weather-focus" style="margin-top:10px; padding:10px; background:rgba(168, 85, 247, 0.2); border-radius:6px;"><strong>דגש יומי והמלצות:</strong> {w_data["focus"]}</div>' if w_data.get("focus") else '<div class="weather-focus" style="margin-top:10px; padding:10px; background:rgba(168, 85, 247, 0.2); border-radius:6px; display:none;"></div>'
        
        html += f'''
            <div class="info-block weather-block weather-widget" data-date="{date_int}.10" data-daynum="{day_num}">
                <h4><i class="fa-solid fa-cloud-sun"></i> תחזית מזג אוויר</h4>
                <div style="font-size:1.1rem;">
                    <p class="w-summary"><strong>מזג אוויר:</strong> {w_data["summary"]}</p>
                    <p class="w-temp"><strong>טמפרטורות:</strong> {w_data["temp"]}</p>
                    <p class="w-rain"><strong>סיכוי למשקעים:</strong> {w_data["rain"]}</p>
                    {focus_html}
                </div>
            </div>
        '''
    else:
        html += f'''
            <div class="info-block weather-block weather-widget" data-date="{date_int}.10" data-daynum="{day_num}">
                <h4><i class="fa-solid fa-cloud-sun"></i> תחזית מזג אוויר</h4>
                <div style="font-size:1.1rem;">
                    <p class="w-summary">אין מידע זמין כרגע.</p>
                    <p class="w-temp"></p>
                    <p class="w-rain"></p>
                    <div class="weather-focus" style="margin-top:10px; padding:10px; background:rgba(168, 85, 247, 0.2); border-radius:6px; display:none;"></div>
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
    desc_text = ""
    for act in activities:
        desc_text += f"<strong>{act.get('title','')}</strong><br>{act.get('desc','')}<br><br>"
    
    if pdf_info:
        desc_text += '<div style="background:rgba(59, 130, 246, 0.15); padding: 15px; border-radius: 8px; border-right: 3px solid #3b82f6; margin-top:10px;"><h4 style="color:#3b82f6; margin-bottom:10px; font-size: 1.15rem;"><i class="fa-solid fa-book"></i> מדריך מנלון (פירוט מהמסמך):</h4>' + pdf_info + '</div>'
        
    if desc_text:
        html += f'''
            <div class="info-block">
                <h4><i class="fa-solid fa-map-location-dot"></i> פירוט המסלול</h4>
                <p>{desc_text}</p>
            </div>
        '''
        
    if hotel:
        query_val = hotel_en if hotel_en else hotel
        maps_link = hotel_maps if hotel_maps else f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(query_val)}"
        html += f'''
            <div class="info-block hotel-block">
                <h4><i class="fa-solid fa-bed"></i> מקום לינה: {hotel}</h4>
                <p>{hotel_notes}</p>
                <a href="{maps_link}" target="_blank" class="btn"><i class="fa-solid fa-map-pin"></i> נווט ל-{hotel} ב-Google Maps</a>
            </div>
        '''
        
    html += '''
            </div>
        </div>
    '''

html += """
        </div>
    </div>
    
    <script>
    function toggleCard(dayNum, event) {
        if (event) {
            event.stopPropagation();
        }
        const card = document.getElementById('day-card-' + dayNum);
        if (card) {
            card.classList.toggle('active');
        }
        updateToggleAllBtn();
    }

    function setupAccordionEvents() {
        document.querySelectorAll('.day-card .card-header').forEach(header => {
            // Direct click listener
            header.addEventListener('click', function(e) {
                e.stopPropagation();
                const card = this.closest('.day-card');
                if (card) {
                    card.classList.toggle('active');
                    updateToggleAllBtn();
                }
            });

            // Mobile touch tap detection
            let touchStartY = 0;
            let touchStartX = 0;
            header.addEventListener('touchstart', function(e) {
                touchStartY = e.touches[0].clientY;
                touchStartX = e.touches[0].clientX;
            }, { passive: true });

            header.addEventListener('touchend', function(e) {
                const touchEndY = e.changedTouches[0].clientY;
                const touchEndX = e.changedTouches[0].clientX;
                if (Math.abs(touchEndY - touchStartY) < 14 && Math.abs(touchEndX - touchStartX) < 14) {
                    e.preventDefault();
                    const card = this.closest('.day-card');
                    if (card) {
                        card.classList.toggle('active');
                        updateToggleAllBtn();
                    }
                }
            });
        });
    }

    function toggleAllDays() {
        const cards = document.querySelectorAll('.day-card');
        const anyClosed = Array.from(cards).some(c => !c.classList.contains('active'));
        cards.forEach(c => {
            if (anyClosed) {
                c.classList.add('active');
            } else {
                c.classList.remove('active');
            }
        });
        updateToggleAllBtn();
    }

    function updateToggleAllBtn() {
        const cards = document.querySelectorAll('.day-card');
        const btn = document.getElementById('toggle-all-btn');
        if (!btn || cards.length === 0) return;
        const allActive = Array.from(cards).every(c => c.classList.contains('active'));
        if (allActive) {
            btn.innerHTML = '<i class="fa-solid fa-angles-up"></i> סגור את כל הימים';
        } else {
            btn.innerHTML = '<i class="fa-solid fa-angles-down"></i> פתח את כל הימים';
        }
    }

    function autoOpenToday() {
        const today = new Date();
        const day = today.getDate();
        const month = today.getMonth() + 1; // 10 = Oct
        const todayKey = day + '.10';
        
        let targetCard = null;
        if (month === 10 && day >= 13 && day <= 22) {
            targetCard = document.querySelector('.day-card[data-day-date="' + todayKey + '"]');
        }
        
        if (targetCard) {
            targetCard.classList.add('active');
            const h2 = targetCard.querySelector('.header-title-group h2');
            if (h2) {
                const badge = document.createElement('span');
                badge.className = 'today-badge';
                badge.innerHTML = '<i class="fa-solid fa-location-dot"></i> היום';
                h2.prepend(badge);
            }
            setTimeout(() => {
                targetCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 300);
        } else {
            // Before or after trip, open Day 1 by default so the screen is not completely closed
            const firstCard = document.querySelector('.day-card');
            if (firstCard) {
                firstCard.classList.add('active');
            }
        }
        updateToggleAllBtn();
    }

    function getSmartFocus(dayNum, w) {
        let focus = [];
        const dayRain = Math.round(((w.morningSum || 0) + (w.noonSum || 0)) * 10) / 10;
        const isNightOnlyRain = (w.nightSum >= 1.0 && dayRain < 0.5);
        
        if (isNightOnlyRain) {
            focus.push("🌙 הגשם צפוי בלילה בלבד. שעות ההליכה צפויות להיות יבשות ונוחות.");
        } else if (dayRain > 4 && (w.morningProb > 60 || w.noonProb > 60)) {
            focus.push("☔ יום גשום בשעות ההליכה! חובה לקחת מעיל גשם אטום וכיסוי לתיק.");
        } else if (dayRain >= 1.5) {
            focus.push('🌦️ ייתכנו ממטרים פזורים בשעות ההליכה. כדאי להשאיר ציוד גשם נגיש בראש התרמיל.');
        } else if (dayRain >= 0.5) {
            focus.push("☁️ ייתכן טפטוף חולף קל במהלך היום. הליכה רגילה עם שכבות.");
        }
        
        if (w.wind > 35) {
            focus.push("רוחות חזקות צפויות ברכסים. מומלץ להצטייד במעיל רוח.");
        }
        if (w.maxT < 14) {
            focus.push("תנאים קרים מהרגיל. מומלץ לבוש חם בשיטת הבצל.");
        } else if (w.maxT >= 25) {
            focus.push("יום חם. להקפיד על שתייה מרובה וקרם הגנה.");
        }

        // Trail specific rules based on day_num
        // dayNum 2 = 14.10 (Stemnitsa -> Dimitsana)
        if (dayNum === 2) {
            if (isNightOnlyRain || dayRain >= 0.5) {
                focus.push("<br>⚠️ <strong>דגש בטיחות למקטע:</strong> סלעים ומדרגות בקניון לוסיוס (Lousios) עלולים להיות רטובים וחלקים! נדרשת הליכה זהירה עם מקלות הליכה.");
            }
        }
        // dayNum 3 = 15.10 (Dimitsana/Zygovisti -> Elati)
        if (dayNum === 3 && (w.wind > 20 || w.maxT < 15)) {
            focus.push("<br>⚠️ <strong>דגש בטיחות למקטע:</strong> צפוי קור ורוחות במעברי הרכס הגבוהים (זיוגוביסטי - 1,550 מ'). חובה להצטייד במגן רוח וחימום לפני החצייה.");
        }

        if (focus.length === 0) {
            focus.push("תנאים מצוינים ויבשים להליכה. מזג אוויר אידיאלי למסלול.");
        }
        return focus.join(" ");
    }

    function renderWeather(weatherData, lastUpdated) {
        document.querySelectorAll('.weather-widget').forEach(el => {
            const dateAttr = el.getAttribute('data-date');
            const dayNum = parseInt(el.getAttribute('data-daynum'));
            
            if(weatherData[dateAttr]) {
                const w = weatherData[dateAttr];
                const focusText = getSmartFocus(dayNum, w);
                
                el.querySelector('.w-summary').innerHTML = `<strong>מזג אוויר:</strong> ${w.summary}`;
                el.querySelector('.w-temp').innerHTML = `<strong>טמפרטורות:</strong> ביום ${w.maxT}°C | בלילה ${w.minT}°C`;
                
                const dayRain = Math.round(((w.morningSum || 0) + (w.noonSum || 0)) * 10) / 10;
                const hasNightRain = (w.nightSum && w.nightSum >= 0.5);

                const mornText = (w.morningSum && w.morningSum >= 0.5) ? `${w.morningProb}% (${w.morningSum} מ"מ)` : (w.morningProb > 20 ? `${w.morningProb}% (יבש/טפטוף זניח)` : `0% (יבש)`);
                const noonText = (w.noonSum && w.noonSum >= 0.5) ? `${w.noonProb}% (${w.noonSum} מ"מ)` : (w.noonProb > 20 ? `${w.noonProb}% (יבש/טפטוף זניח)` : `0% (יבש)`);

                let subParts = [];
                subParts.push(`בוקר (06-12): ${mornText}`);
                subParts.push(`צהריים (12-18): ${noonText}`);
                if (hasNightRain) {
                    subParts.push(`לילה (00-06): ${w.nightSum} מ"מ`);
                }

                const subStr = `<br><span style="font-size:0.9rem; color:var(--text-muted);">${subParts.join(' | ')}</span>`;
                let rainDisplay = '';

                if (dayRain === 0 && !hasNightRain) {
                    rainDisplay = `<strong>סיכוי למשקעים:</strong> 0% <span style="font-size:0.9rem; color:var(--accent-green); font-weight:500;">(יבש לחלוטין)</span>${subStr}`;
                } else if (dayRain === 0 && hasNightRain) {
                    rainDisplay = `<strong>סיכוי למשקעים:</strong> יבש בהליכה <span style="font-size:0.9rem; color:var(--accent-green); font-weight:500;">(גשם בלילה בלבד: ${w.nightSum} מ"מ)</span>${subStr}`;
                } else {
                    rainDisplay = `<strong>סיכוי למשקעים:</strong> ${w.rainProb}% (${w.rainSum} מ"מ סה"כ)${subStr}`;
                }
                el.querySelector('.w-rain').innerHTML = rainDisplay;
                
                const focusEl = el.querySelector('.weather-focus');
                focusEl.style.display = 'block';
                focusEl.innerHTML = `<strong>דגש יומי והמלצות:</strong> ${focusText}`;
                
                if (lastUpdated) {
                    let tsEl = el.querySelector('.w-timestamp');
                    if (!tsEl) {
                        tsEl = document.createElement('div');
                        tsEl.className = 'w-timestamp';
                        tsEl.style.fontSize = '0.85rem';
                        tsEl.style.color = 'var(--text-muted)';
                        tsEl.style.marginTop = '8px';
                        el.appendChild(tsEl);
                    }
                    const d = new Date(lastUpdated);
                    tsEl.innerHTML = `<i class="fa-solid fa-clock-rotate-left"></i> עודכן לאחרונה מהלוויין (Open-Meteo): ${d.toLocaleDateString('he-IL')} בשעה ${d.toLocaleTimeString('he-IL', {hour: '2-digit', minute:'2-digit'})}`;
                }
            }
        });
    }

    async function fetchSmartWeather() {
        const btn = document.getElementById('weather-update-btn');
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> סורק מקורות מטאורולוגיים...';
        btn.disabled = true;

        try {
            const response = await fetch("https://api.open-meteo.com/v1/forecast?latitude=37.595&longitude=22.04&elevation=1000&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max&hourly=precipitation_probability,precipitation&timezone=auto&forecast_days=16");
            const data = await response.json();
            
            const weatherMap = {};
            for(let i=0; i<data.daily.time.length; i++) {
                const dateStr = data.daily.time[i]; 
                const d = new Date(dateStr);
                const day = d.getDate();
                const month = d.getMonth() + 1;
                
                const maxT = Math.round(data.daily.temperature_2m_max[i]);
                const minT = Math.round(data.daily.temperature_2m_min[i]);
                let rawRainProb = data.daily.precipitation_probability_max[i] || 0;
                let rainSum = Math.round((data.daily.precipitation_sum[i] || 0) * 10) / 10;
                const wind = data.daily.wind_speed_10m_max[i];
                const code = data.daily.weather_code[i];
                
                // Calibration rule: Ignore drizzles and humidity under 1.0 mm
                let rainProb = (rainSum >= 1.0) ? rawRainProb : 0;
                
                let morningProb = 0; let morningSum = 0;
                let noonProb = 0; let noonSum = 0;
                let nightProb = 0; let nightSum = 0;
                
                if (data.hourly) {
                    for(let h=0; h<data.hourly.time.length; h++) {
                        const hTime = data.hourly.time[h];
                        if (hTime.startsWith(dateStr)) {
                            const hour = parseInt(hTime.substring(11, 13));
                            const hProb = data.hourly.precipitation_probability[h] || 0;
                            const hSum = data.hourly.precipitation[h] || 0;
                            
                            if (hour >= 0 && hour <= 5) {
                                nightProb = Math.max(nightProb, hProb);
                                nightSum += hSum;
                            } else if (hour >= 6 && hour <= 11) {
                                morningProb = Math.max(morningProb, hProb);
                                morningSum += hSum;
                            } else if (hour >= 12 && hour <= 17) {
                                noonProb = Math.max(noonProb, hProb);
                                noonSum += hSum;
                            }
                        }
                    }
                    nightSum = Math.round(nightSum * 10) / 10;
                    morningSum = Math.round(morningSum * 10) / 10;
                    noonSum = Math.round(noonSum * 10) / 10;
                }

                let summary = "שמשי ויבש, תנאים נוחים";
                if(code >= 1 && code <= 3) summary = "עננות חלקית, שילוב של שמש ועננים";
                if(code >= 45 && code <= 48) summary = "ערפילי (בעיקר בבוקר)";
                
                const dayRain = Math.round((morningSum + noonSum) * 10) / 10;
                
                if (dayRain >= 1.0) {
                    if (dayRain > 4 && (morningProb > 60 || noonProb > 60)) {
                        summary = "גשם משמעותי / רציף בשעות ההליכה";
                    } else {
                        summary = "גשם מקומי / ממטרים פזורים בשעות ההליכה";
                    }
                } else if (nightSum >= 1.0) {
                    summary = "יבש בשעות ההליכה (גשם בלילה בלבד)";
                } else if (code >= 51 || dayRain > 0) {
                    summary = "מעונן / יבש (ייתכן טפטוף חולף שאינו מורגש)";
                }
                
                weatherMap[`${day}.${month}`] = { maxT, minT, rainProb, rainSum, wind, summary, morningProb, morningSum, noonProb, noonSum, nightProb, nightSum };
            }

            const now = new Date().getTime();
            localStorage.setItem('menalon_weather', JSON.stringify(weatherMap));
            localStorage.setItem('menalon_weather_time', now);
            
            renderWeather(weatherMap, now);

            btn.innerHTML = '<i class="fa-solid fa-check"></i> התחזית וההמלצות עודכנו בהצלחה!';
            setTimeout(() => {
                btn.innerHTML = '<i class="fa-solid fa-cloud-sun"></i> עדכן תחזית חי בזמן אמת';
                btn.disabled = false;
            }, 4000);

        } catch (e) {
            console.error(e);
            btn.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> שגיאת חיבור';
            setTimeout(() => {
                btn.innerHTML = '<i class="fa-solid fa-cloud-sun"></i> עדכן תחזית חי בזמן אמת';
                btn.disabled = false;
            }, 4000);
        }
    }

    // Load saved weather on startup & auto-open today & setup mobile events
    window.addEventListener('DOMContentLoaded', () => {
        setupAccordionEvents();
        autoOpenToday();
        
        const savedWeather = localStorage.getItem('menalon_weather');
        const savedTime = localStorage.getItem('menalon_weather_time');
        if (savedWeather) {
            try {
                renderWeather(JSON.parse(savedWeather), parseInt(savedTime));
            } catch(e) {}
        }
    });
    </script>
    <script src="expenses.js?v=4"></script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
