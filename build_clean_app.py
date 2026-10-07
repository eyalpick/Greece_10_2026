import json
import codecs
import re
from guide_text import GUIDE_TEXT

MANUAL_WEATHER = {
    13: {
        "summary": "שמש ברובה, יבש",
        "temp": "ביום 19°C | בלילה 9°C",
        "rain": "1% (יבש)",
        "focus": ""
    },
    14: {
        "summary": "שמש ברובה, תנאים נוחים ויבשים",
        "temp": "ביום 19°C | בלילה 9°C",
        "rain": "0% (יבש לחלוטין)",
        "focus": "תנאים מצוינים ויבשים לחציית קניון לוסיוס (Lousios Gorge) והגעה למנזרים."
    },
    15: {
        "summary": "שילוב של שמש ועננות, ייתכן ממטר מקומי קל אחה\"צ",
        "temp": "בכפרים 18°C ביום, 9°C בלילה (ברכס הגבוה כ-13°C–14°C עם רוח ערה)",
        "rain": "49%",
        "focus": "מומלץ לצאת מוקדם כדי לעבור את הרכס הגבוה לפני שעות אחר הצהריים."
    },
    16: {
        "summary": "מעונן עם גשם בחלק ניכר משעות היום",
        "temp": "ביום 18°C | בלילה 8°C",
        "rain": "60%",
        "focus": "יום גשום המצריך מעיל גשם, כיסוי לתרמיל והליכה זהירה במדרונות חלקים."
    },
    17: {
        "summary": "התבהרות מהירה, שמש ועננות חלקית, יציב",
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
        
        .btn { display: inline-block; background: var(--accent-blue); color: #fff; padding: 0.75rem 1.25rem; border-radius: 6px; text-decoration: none; margin-top: 0.5rem; font-size: 1.05rem; cursor: pointer; border: none; font-family: 'Inter', sans-serif;}
        .btn:hover { background: #2563eb; }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }

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
                <button id="weather-update-btn" class="btn" style="background: #a855f7;" onclick="fetchSmartWeather()">
                    <i class="fa-solid fa-cloud-sun"></i> עדכן תחזית חכמה עכשיו
                </button>
                <p style="font-size:0.9rem; color:var(--text-muted); margin-top:0.5rem;">מושך נתונים עדכניים ובונה המלצות יציאה חכמות (לא צורך חבילת גלישה)</p>
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
    function getSmartFocus(dayNum, w) {
        let focus = [];
        
        if (w.rainProb >= 50 || w.rainSum > 3) {
            focus.push("יום גשום! חובה להצטייד במעיל גשם וכיסוי לתרמיל.");
        } else if (w.rainProb >= 20) {
            focus.push("ייתכן ממטר מקומי. כדאי להחזיק ציוד גשם נגיש.");
        }
        
        if (w.rainProb >= 30 || w.rainSum > 1) {
            focus.push("מומלץ ליציאה מוקדמת כדי להימנע מממטרי אחר הצהריים.");
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
        if (dayNum === 2 && w.rainProb >= 20) {
            focus.push("<br>⚠️ <strong>דגש בטיחות למקטע:</strong> סלעים ומדרגות חלקות בקניון לוסיוס (Lousios) בעת רטיבות! נדרשת הליכה זהירה מאוד.");
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
                el.querySelector('.w-rain').innerHTML = `<strong>סיכוי למשקעים:</strong> ${w.rainProb}%`;
                
                const focusEl = el.querySelector('.weather-focus');
                focusEl.style.display = 'block';
                focusEl.innerHTML = `<strong>דגש יומי והמלצות:</strong> ${focusText}`;
                
                // Add timestamp if available
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
                    tsEl.innerHTML = `<i class="fa-solid fa-clock-rotate-left"></i> עודכן לאחרונה: ${d.toLocaleDateString('he-IL')} בשעה ${d.toLocaleTimeString('he-IL', {hour: '2-digit', minute:'2-digit'})}`;
                }
            }
        });
    }

    async function fetchSmartWeather() {
        const btn = document.getElementById('weather-update-btn');
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> סורק מקורות מטאורולוגיים...';
        btn.disabled = true;

        try {
            // Using elevation=1000 for Arcadia mountains to get accurate cold/wind models
            const response = await fetch("https://api.open-meteo.com/v1/forecast?latitude=37.595&longitude=22.04&elevation=1000&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max&timezone=auto&forecast_days=16");
            const data = await response.json();
            
            const weatherMap = {};
            for(let i=0; i<data.daily.time.length; i++) {
                const dateStr = data.daily.time[i]; 
                const d = new Date(dateStr);
                const day = d.getDate();
                const month = d.getMonth() + 1;
                
                const maxT = Math.round(data.daily.temperature_2m_max[i]);
                const minT = Math.round(data.daily.temperature_2m_min[i]);
                const rainProb = data.daily.precipitation_probability_max[i];
                const rainSum = data.daily.precipitation_sum[i];
                const wind = data.daily.wind_speed_10m_max[i];
                const code = data.daily.weather_code[i];
                
                let summary = "שמשי ויבש, תנאים נוחים";
                if(code >= 1 && code <= 3) summary = "עננות חלקית, שילוב של שמש ועננים";
                if(code >= 45 && code <= 48) summary = "ערפילי (בעיקר בבוקר)";
                if(code >= 51 && code <= 67) summary = "מעונן עם גשם קל עד בינוני";
                if(code >= 80 && code <= 82) summary = "גשם שוטף / ממטרים חזקים";
                if(code >= 95) summary = "סופות רעמים וגשם";
                
                weatherMap[`${day}.${month}`] = { maxT, minT, rainProb, rainSum, wind, summary };
            }

            // Save to localStorage
            const now = new Date().getTime();
            localStorage.setItem('menalon_weather', JSON.stringify(weatherMap));
            localStorage.setItem('menalon_weather_time', now);
            
            renderWeather(weatherMap, now);

            btn.innerHTML = '<i class="fa-solid fa-check"></i> התחזית וההמלצות עודכנו בהצלחה!';
            setTimeout(() => {
                btn.innerHTML = '<i class="fa-solid fa-cloud-sun"></i> עדכן תחזית חכמה עכשיו';
                btn.disabled = false;
            }, 4000);

        } catch (e) {
            console.error(e);
            btn.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> שגיאת חיבור';
            setTimeout(() => {
                btn.innerHTML = '<i class="fa-solid fa-cloud-sun"></i> עדכן תחזית חכמה עכשיו';
                btn.disabled = false;
            }, 4000);
        }
    }

    // Load saved weather on startup
    window.addEventListener('DOMContentLoaded', () => {
        const savedWeather = localStorage.getItem('menalon_weather');
        const savedTime = localStorage.getItem('menalon_weather_time');
        if (savedWeather) {
            try {
                renderWeather(JSON.parse(savedWeather), parseInt(savedTime));
            } catch(e) {}
        }
    });
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
