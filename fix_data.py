import json

# Read the good json
with open(r'C:\Users\Eyal Pick\.gemini\antigravity\brain\4dd4cf76-c8a9-4f41-a9e9-14b74fb877a7\scratch\menalon.json', 'r', encoding='utf-8') as f:
    df = json.load(f)

itinerary = []
month = "באוקטובר"

for i, row in enumerate(df):
    date_val = row.get("תאריך", None)
    if date_val is None:
        continue
        
    date_text = f"{int(date_val)} {month} (יום {row.get('יום בשבוע', '')})"
    
    title_he = row.get("מסלול", "")
    if not title_he:
        title_he = "יום התארגנות / נסיעות"
        
    km = row.get('ק"מ', None)
    time_est = row.get('זמן משוער', None)
    elev_up = row.get('עלייה מצטברת', None)
    elev_down = row.get('ירידה מצטברת', None)
    
    stats = []
    if km: stats.append(f"{km} ק\"מ")
    if time_est: stats.append(f"זמן: {time_est}")
    if elev_up: stats.append(f"עלייה: {elev_up}")
    if elev_down: stats.append(f"ירידה: {elev_down}")
    
    drive_time = " | ".join(stats)
    
    hotel_name_he = row.get('מלון הזמנה', '')
    hotel_name_en = row.get('מלון', '')
    if hotel_name_he is None: hotel_name_he = ""
    if hotel_name_en is None: hotel_name_en = ""
    
    hotel_notes = row.get('הערות למלון', '')
    if hotel_notes is None: hotel_notes = ""
    
    price_euro = row.get('מחיר אירו', None)
    price_ils = row.get('מחיר ₪', None)
    
    hotel_desc = hotel_notes
    if price_euro:
        hotel_desc += f". מחיר: €{price_euro}"
    if price_ils:
        hotel_desc += f" (₪{price_ils})"
        
    eats = row.get('אוכל במסלול', '')
    if eats is None: eats = ""
    
    desc = row.get('תיאור', '')
    if desc is None: desc = ""
    notes = row.get('הערות לטיול', '')
    if notes is None: notes = ""
    
    activities = []
    if desc or notes:
        activities.append({
            "title": "פירוט המסלול והערות",
            "desc": f"{desc}<br><br>{notes}"
        })
        
    lodging = None
    if hotel_name_he or hotel_name_en:
        lodging = {
            "nameHe": hotel_name_he if hotel_name_he else hotel_name_en,
            "nameEn": hotel_name_en,
            "desc": hotel_desc.strip(),
            "bookingUrl": "",
            "mapsUrl": f"https://www.google.com/maps/search/?api=1&query={hotel_name_en.replace(' ', '+')}" if hotel_name_en else ""
        }
    
    day_obj = {
        "dayNum": i + 1,
        "dateText": date_text,
        "titleHe": title_he,
        "titleEn": title_he,
        "driveTime": drive_time,
        "weatherText": "15°C / 8°C",
        "lodging": lodging,
        "eatsHe": "אוכל והצטיידות",
        "eatsDesc": eats,
        "activities": activities
    }
    
    itinerary.append(day_obj)

# Write to JS file
js_content = "const itineraryData = " + json.dumps(itinerary, ensure_ascii=False, indent=4) + ";"
with open('itineraryData.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
