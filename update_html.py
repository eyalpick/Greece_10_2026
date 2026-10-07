import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('לוח בקרה - ספרד & פורטוגל 2026 (Pro Version)', 'לוח בקרה - יוון 2026 - Menalon Trail')
content = content.replace('ספרד & פורטוגל 2026', 'יוון 2026 - Menalon Trail')
content = content.replace('המסע הגדול בחצי האי האיברי | 29/06/2026 - 15/07/2026', 'טרק מנלון והפלופונס | 13/10/2026 - 22/10/2026')
content = content.replace('אירופה / מדריד - ליסבון', 'יוון / אתונה - פלופונס')

# Update the PDFs menu
# The previous project had a specific dropdown structure for PDFs. 
# We'll just replace the inner HTML of that dropdown using regex or string replacement, but it might be easier to just overwrite it.

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
