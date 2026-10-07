import pandas as pd
import json
import math

df = pd.read_excel('Menalon trail.xlsx')

itinerary = []
month = "באוקטובר"

for i, row in df.iterrows():
    date_val = row.get("תאריך", None)
    if pd.isna(date_val):
        continue
        
    date_text = f"{int(date_val)} {month} (יום {row.get('יום בשבוע', '')})"
    
    title_he = row.get("מסלול", "")
    if pd.isna(title_he):
        title_he = "יום התארגנות / נסיעות"
        
    km = row.get('ק"מ', None)
    time_est = row.get('זמן משוער', None)
    elev_up = row.get('עלייה מצטברת', None)
    elev_down = row.get('ירידה מצטברת', None)
    
    stats = []
    if not pd.isna(km): stats.append(f"{km} ק\"מ")
    if not pd.isna(time_est): stats.append(f"זמן: {time_est}")
    if not pd.isna(elev_up): stats.append(f"עלייה: {elev_up}")
    if not pd.isna(elev_down): stats.append(f"ירידה: {elev_down}")
    
    drive_time = " | ".join(stats)
    
    hotel_name_he = row.get('מלון הזמנה', '')
    hotel_name_en = row.get('מלון', '')
    
    hotel_notes = row.get('הערות למלון', '')
    price_euro = row.get('מחיר אירו', None)
    price_ils = row.get('מחיר ₪', None)
    if pd.isna(hotel_name_he): hotel_name_he = ""
    if pd.isna(hotel_name_en): hotel_name_en = ""
    if pd.isna(hotel_notes): hotel_notes = ""
    
    hotel_desc = hotel_notes
    if not pd.isna(price_euro):
        hotel_desc += f". מחיר: €{price_euro}"
    if not pd.isna(price_ils):
        hotel_desc += f" (₪{price_ils})"
        
    eats = row.get('אוכל במסלול', '')
    if pd.isna(eats): eats = ""
    
    desc = row.get('תיאור', '')
    if pd.isna(desc): desc = ""
    notes = row.get('הערות לטיול', '')
    if pd.isna(notes): notes = ""
    
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
        "weatherText": "15°C / 8°C", # Placeholder for mountains
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
