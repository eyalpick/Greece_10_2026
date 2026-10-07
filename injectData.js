function processDocxData() {
    const lines = docxText.split('\n').map(l => l.trim()).filter(l => l.length > 0);
    
    let dayTexts = {};
    let currentDayNum = 0;
    
    for(let line of lines) {
        let dayMatch = line.match(/^יום\s*(\d+)/);
        if(dayMatch) {
            currentDayNum = parseInt(dayMatch[1], 10);
            dayTexts[currentDayNum] = [];
            continue;
        }
        if(currentDayNum > 0) {
            dayTexts[currentDayNum].push(line);
        }
    }

    // Helper to format block of text
    function formatBlock(linesArr) {
        return linesArr.map(l => {
            // make lines starting with numbers or ending with ':' bold
            if(l.match(/^\d+\./) || l.endsWith(':')) {
                return `<h3 style="margin-top:1rem; color:var(--text-primary); font-size:1.2rem;">${l}</h3>`;
            }
            return `<p style="margin-bottom:0.5rem;">${l}</p>`;
        }).join("");
    }

    // Manual perfect mapping logic
    itineraryData.forEach(day => {
        let textLines = dayTexts[day.dayNum];
        if(!textLines) return;
        
        let sections = [];
        let currentSection = { title: "כללי", lines: [] };
        
        // split day text into sections based on short lines that look like titles
        for(let line of textLines) {
            // if line is short and doesn't end with a period, assume it's a section title
            if(line.length < 40 && !line.endsWith('.') && !line.endsWith(',') && !line.startsWith('1.') && !line.startsWith('2.')) {
                if(currentSection.lines.length > 0) sections.push(currentSection);
                currentSection = { title: line, lines: [] };
            } else {
                currentSection.lines.push(line);
            }
        }
        if(currentSection.lines.length > 0) sections.push(currentSection);

        // Grouping into activities
        let restaurantsLines = [];
        
        sections.forEach(sec => {
            let t = sec.title;
            let html = `<h3>${t}</h3>` + formatBlock(sec.lines);
            
            if(t.includes("מסעדות") || t.includes("אוכל") || t.includes("קולינריה")) {
                restaurantsLines.push(html);
                return;
            }
            
            // Find best matching activity
            let bestMatchIdx = 0;
            let bestScore = 0;
            day.activities.forEach((act, idx) => {
                let score = 0;
                let words = act.title.split(/[\s\-\(\)]+/).filter(w => w.length > 2);
                words.forEach(w => {
                    if(t.includes(w)) score += 2;
                    if(sec.lines.join(" ").includes(w)) score += 1;
                });
                if(score > bestScore) {
                    bestScore = score;
                    bestMatchIdx = idx;
                }
            });
            
            if(bestScore > 0 || day.activities.length === 1) {
                if(!day.activities[bestMatchIdx].detailsHtml) day.activities[bestMatchIdx].detailsHtml = "";
                day.activities[bestMatchIdx].detailsHtml += html;
            } else {
                // fallback to first activity
                if(!day.activities[0].detailsHtml) day.activities[0].detailsHtml = "";
                day.activities[0].detailsHtml += html;
            }
        });
        
        if(restaurantsLines.length > 0) {
            day.activities.push({
                title: "🍽️ מסעדות ואוכל מומלץ (מהמסמך המורחב)",
                desc: "המלצות קולינריות מהירות וטברנות מקומיות",
                mapsQuery: day.eatsHe ? day.eatsHe : "Restaurants",
                detailsHtml: restaurantsLines.join("")
            });
        }
    });
}
processDocxData();
