import re

html = open('index.html', encoding='utf-8').read()

pdf_section = """
        <!-- PDF Documents Section -->
        <div class="card" style="margin-top: 2rem;">
            <div class="card-header">
                <h2><i class="fa-solid fa-file-pdf" style="color: var(--accent-red);"></i> מסמכים שימושיים</h2>
            </div>
            <div class="card-body">
                <ul style="list-style: none; padding: 0; line-height: 2;">
                    <li><a href="Menalon trail.xlsx" target="_blank" style="color: var(--accent-blue); text-decoration: none;"><i class="fa-solid fa-file-excel"></i> טבלת המסלול (Excel)</a></li>
                    <li><a href="כרטיסי טיסה.pdf" target="_blank" style="color: var(--accent-blue); text-decoration: none;"><i class="fa-solid fa-plane-departure"></i> כרטיסי טיסה</a></li>
                    <li><a href="menalon_trail_guide_v2.pdf" target="_blank" style="color: var(--accent-blue); text-decoration: none;"><i class="fa-solid fa-book"></i> מדריך שביל מנלון V2</a></li>
                    <li><a href="Mainalon_In_Search_of_Arcadia_-_Matt_Stanley.pdf" target="_blank" style="color: var(--accent-blue); text-decoration: none;"><i class="fa-solid fa-book-open"></i> ספר: Mainalon In Search of Arcadia</a></li>
                </ul>
            </div>
        </div>
"""

# Insert it before <div id="app">
html = html.replace('<div id="app">', pdf_section + '\n        <div id="app">')

# Also, I should check if docxData.js is referenced and remove it since we don't have it for Greece
html = re.sub(r'<script src="docxData.js"></script>\s*', '', html)
html = re.sub(r'<script src="injectData.js"></script>\s*', '<script src="itineraryData.js"></script>\n<script src="injectData.js"></script>\n', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
