import json
import codecs

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
            font-size: 16px;
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
        .header-card h1 { font-family: 'Outfit', sans-serif; font-size: 2.5rem; margin-bottom: 0.5rem; color: #fff; }
        .header-card p { color: var(--accent-orange); font-size: 1.2rem; font-weight: 500; }
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-md);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .card-header h2 { font-size: 1.5rem; color: var(--accent-orange); margin-bottom: 0.5rem; }
        .card-header p.stats { color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border-card); padding-bottom: 1rem; }
        
        .info-block {
            background: rgba(0,0,0,0.2);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border-right: 3px solid var(--accent-blue);
        }
        .info-block h4 { color: var(--accent-blue); margin-bottom: 0.5rem; font-size: 1.1rem; }
        .info-block p { color: var(--text-secondary); font-size: 0.95rem; }
        
        .eats-block { border-right-color: var(--accent-green); }
        .eats-block h4 { color: var(--accent-green); }
        
        .hotel-block { border-right-color: var(--accent-orange); }
        .hotel-block h4 { color: var(--accent-orange); }
        
        .docs-list { list-style: none; display: flex; flex-wrap: wrap; gap: 1rem; }
        .docs-list li a {
            display: inline-block;
            background: rgba(255,255,255,0.05);
            padding: 0.75rem 1.25rem;
            border-radius: 8px;
            color: #fff;
            text-decoration: none;
            border: 1px solid var(--border-card);
            transition: 0.2s;
        }
        .docs-list li a:hover { background: rgba(255,255,255,0.1); border-color: var(--accent-blue); color: var(--accent-blue); }
        
        .btn { display: inline-block; background: var(--accent-blue); color: #fff; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; margin-top: 0.5rem; font-size: 0.9rem; }
        .btn:hover { background: #2563eb; }
    </style>
</head>
<body>
    <div class="dashboard-container">
        
        <header class="header-card">
            <h1>יוון 2026 - Menalon Trail</h1>
            <p>13 באוקטובר - 22 באוקטובר 2026</p>
        </header>

        <div class="card">
            <div class="card-header">
                <h2 style="color: var(--accent-blue);"><i class="fa-solid fa-folder-open"></i> מסמכים שימושיים</h2>
            </div>
            <ul class="docs-list">
                <li><a href="Menalon trail.xlsx" target="_blank"><i class="fa-solid fa-file-excel" style="color:#10b981;"></i> טבלת המסלול (Excel)</a></li>
                <li><a href="כרטיסי טיסה.pdf" target="_blank"><i class="fa-solid fa-plane" style="color:#ef4444;"></i> כרטיסי טיסה</a></li>
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
    date_text = f"{int(date_val)} {month} (יום {row.get('יום בשבוע', '')})"
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
    
    hotel = row.get('מלון', '') or row.get('מלון הזמנה', '')
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
                <h2>יום {day_num} - {date_text} <span style="color:#fff; font-size:1.4rem; display:block; margin-top:0.5rem;">{title_he}</span></h2>
                <p class="stats">{drive_time_html}</p>
            </div>
    '''
    
    if desc or notes:
        desc_text = str(desc or '') + '<br><br>' + str(notes or '')
        html += f'''
            <div class="info-block">
                <h4><i class="fa-solid fa-map-location-dot"></i> פירוט המסלול והערות</h4>
                <p>{desc_text}</p>
            </div>
        '''
        
    if eats:
        html += f'''
            <div class="info-block eats-block">
                <h4><i class="fa-solid fa-utensils"></i> אוכל והצטיידות</h4>
                <p>{eats}</p>
            </div>
        '''
        
    if hotel:
        maps_link = f"https://www.google.com/maps/search/?api=1&query={hotel.replace(' ', '+')}"
        html += f'''
            <div class="info-block hotel-block">
                <h4><i class="fa-solid fa-bed"></i> מקום לינה: {hotel}</h4>
                <p>{hotel_notes}</p>
                <a href="{maps_link}" target="_blank" class="btn"><i class="fa-solid fa-map-pin"></i> נווט למלון ב-Google Maps</a>
            </div>
        '''
        
    html += '</div>\n'

html += """
        </div>
    </div>
</body>
</html>
"""

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)
