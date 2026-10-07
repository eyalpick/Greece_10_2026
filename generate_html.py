import json
import re

# Load data
with open(r'C:\Users\Eyal Pick\.gemini\antigravity\brain\4dd4cf76-c8a9-4f41-a9e9-14b74fb877a7\scratch\menalon.json', 'r', encoding='utf-8') as f:
    df = json.load(f)

html = open('index.html', encoding='utf-8').read()

# Find the start of the app container
app_start_idx = html.find('<div id="app">')
if app_start_idx == -1:
    print("Error: Could not find <div id='app'>")
    exit(1)

# Keep everything before <div id="app">
header_html = html[:app_start_idx]

new_html = header_html + '<div id="app" class="dashboard-container">\n'

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
    
    drive_time_html = " | ".join(stats) if stats else "יום התארגנות"
    
    hotel = row.get('מלון', '') or row.get('מלון הזמנה', '')
    hotel_notes = row.get('הערות למלון', '')
    price_euro = row.get('מחיר אירו')
    if hotel_notes is None: hotel_notes = ''
    if price_euro: hotel_notes += f". מחיר: €{price_euro}"
    
    eats = row.get('אוכל במסלול')
    desc = row.get('תיאור')
    notes = row.get('הערות לטיול')
    
    day_html = f'''
        <div class="card day-card">
            <div class="card-header">
                <h2>יום {day_num} <span style="font-size:1.2rem; color:var(--text-muted);">| {date_text}</span></h2>
                <div class="quick-stats">
                    <span>{drive_time_html}</span>
                </div>
            </div>
            
            <div class="card-body">
                <h3 style="color:var(--accent-orange); margin-bottom:1rem; font-size:1.4rem;">{title_he}</h3>
    '''
    
    if desc or notes:
        desc_text = (desc or '') + '<br><br>' + (notes or '')
        day_html += f'''
                <div class="info-block">
                    <h4><i class="fa-solid fa-map-location-dot"></i> פירוט המסלול והערות</h4>
                    <p>{desc_text}</p>
                </div>
        '''
        
    if eats:
        day_html += f'''
                <div class="info-block">
                    <h4><i class="fa-solid fa-utensils"></i> אוכל והצטיידות</h4>
                    <p>{eats}</p>
                </div>
        '''
        
    if hotel:
        maps_link = f"https://www.google.com/maps/search/?api=1&query={hotel.replace(' ', '+')}"
        day_html += f'''
                <div class="info-block">
                    <h4><i class="fa-solid fa-bed"></i> מקום לינה: {hotel}</h4>
                    <p>{hotel_notes}</p>
                    <a href="{maps_link}" target="_blank" class="btn btn-sm btn-outline"><i class="fa-solid fa-map-pin"></i> ניווט למלון</a>
                </div>
        '''
        
    day_html += '''
            </div>
        </div>
    '''
    new_html += day_html

new_html += '</div>\n</body>\n</html>'

# Also remove script tags for itineraryData since it's now statically generated
new_html = re.sub(r'<script.*?</script>', '', new_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
