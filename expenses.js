const WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxKwpk_Mfz8zTYQeewIBJWtKqJW0yHHLBI759Jnq1TpvdBoeoT0g3MA1BwNL7mDBClG/exec";
const PARTICIPANTS = ["איל", "שי", "יעקב"];
let expenses = [];
let eurToIlsRate = 4.05; // Fallback rate

async function initExpensesApp() {
    renderAppShell();
    await fetchExchangeRate();
    await fetchExpenses();
}

async function fetchExchangeRate() {
    try {
        const cached = localStorage.getItem('eur_to_ils_rate');
        const cachedTime = localStorage.getItem('eur_to_ils_time');
        const now = new Date().getTime();
        
        // Cache exchange rate for 24 hours
        if (cached && cachedTime && (now - parseInt(cachedTime)) < 24 * 60 * 60 * 1000) {
            eurToIlsRate = parseFloat(cached);
            return;
        }
        
        const res = await fetch("https://api.exchangerate-api.com/v4/latest/EUR");
        const data = await res.json();
        eurToIlsRate = data.rates.ILS;
        
        localStorage.setItem('eur_to_ils_rate', eurToIlsRate);
        localStorage.setItem('eur_to_ils_time', now);
    } catch (e) {
        console.warn("Could not fetch rate, using fallback");
    }
}

async function fetchExpenses() {
    document.getElementById('expenses-status').innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> טוען נתונים...';
    try {
        const res = await fetch(WEB_APP_URL);
        expenses = await res.json();
        renderExpenses();
    } catch (e) {
        document.getElementById('expenses-status').innerHTML = '<i class="fa-solid fa-triangle-exclamation" style="color:var(--accent-red);"></i> שגיאה בטעינת נתונים';
    }
}

async function addExpense(e) {
    e.preventDefault();
    const btn = document.getElementById('add-expense-btn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> שומר...';
    
    const dateStr = document.getElementById('exp-date').value;
    const desc = document.getElementById('exp-desc').value;
    const amount = parseFloat(document.getElementById('exp-amount').value);
    const currency = document.getElementById('exp-currency').value;
    const payer = document.getElementById('exp-payer').value;
    
    const sharedBy = [];
    PARTICIPANTS.forEach(p => {
        if(document.getElementById(`exp-share-${p}`).checked) {
            sharedBy.push(p);
        }
    });
    
    if (sharedBy.length === 0) {
        alert("חובה לבחור לפחות משתתף אחד שמתחלק בהוצאה");
        btn.disabled = false;
        btn.innerHTML = 'הוסף הוצאה';
        return;
    }
    
    let amountILS = amount;
    if (currency === 'EUR') amountILS = amount * eurToIlsRate;
    
    const expenseData = {
        date: dateStr,
        description: desc,
        amount: amount,
        currency: currency,
        payer: payer,
        amountILS: amountILS,
        sharedBy: sharedBy
    };
    
    try {
        await fetch(WEB_APP_URL, {
            method: 'POST',
            body: JSON.stringify(expenseData),
            mode: 'no-cors' // Prevent CORS blocked response issue on Google Apps Script redirect
        });
        
        // Optimistically update the UI without waiting for another GET
        expenses.push(expenseData);
        renderExpenses();
        
        // Reset form, but keep the selected date
        document.getElementById('add-expense-form').reset();
        document.getElementById('exp-date').value = dateStr;
        checkYaakovStatus();
        document.getElementById('add-expense-section').style.display = 'none';
        
    } catch(err) {
        alert("שגיאה בשמירת ההוצאה: " + err.message);
    }
    
    btn.disabled = false;
    btn.innerHTML = 'הוסף הוצאה';
}

function renderAppShell() {
    const container = document.getElementById('expenses-app');
    if (!container) return;
    
    container.innerHTML = `
        <div class="card" style="border-color: var(--accent-green); box-shadow: 0 0 15px rgba(16, 185, 129, 0.1);">
            <div class="card-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: none; margin-bottom: 0;">
                <h2 style="color: var(--accent-green); margin-bottom: 0; font-size: 1.6rem;"><i class="fa-solid fa-wallet"></i> התחשבנות כספית</h2>
                <div id="expenses-status" style="font-size: 0.9rem; color: var(--text-muted);">ממתין...</div>
            </div>
            
            <div style="margin-top: 1rem;">
                <button class="btn" style="background: var(--accent-green); width: 100%; margin-bottom: 0.5rem; font-weight: bold; font-size: 1.15rem;" onclick="document.getElementById('add-expense-section').style.display='block'">+ הוסף הוצאה חדשה</button>
            </div>
            
            <div id="add-expense-section" style="display: none; background: rgba(0,0,0,0.3); padding: 1.25rem; border-radius: 12px; margin: 1.5rem 0; border: 1px solid var(--accent-green);">
                <form id="add-expense-form" onsubmit="addExpense(event)">
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; color: var(--text-secondary);">תאריך ההוצאה:</label>
                        <input type="date" id="exp-date" required style="width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #444; background: #1a1a24; color: white; font-family: inherit; font-size: 1rem;" onchange="checkYaakovStatus()">
                    </div>
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; color: var(--text-secondary);">על מה ההוצאה?</label>
                        <input type="text" id="exp-desc" required placeholder="לדוגמה: ארוחת צהריים בוויטינה, דלק..." style="width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #444; background: #1a1a24; color: white; font-family: inherit; font-size: 1rem;">
                    </div>
                    <div style="display: flex; gap: 15px; margin-bottom: 15px;">
                        <div style="flex: 1.5;">
                            <label style="display: block; margin-bottom: 5px; color: var(--text-secondary);">סכום:</label>
                            <input type="number" id="exp-amount" step="0.01" required style="width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #444; background: #1a1a24; color: white; font-family: inherit; font-size: 1rem;">
                        </div>
                        <div style="flex: 1;">
                            <label style="display: block; margin-bottom: 5px; color: var(--text-secondary);">מטבע:</label>
                            <select id="exp-currency" style="width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #444; background: #1a1a24; color: white; font-family: inherit; font-size: 1rem;">
                                <option value="EUR">אירו (€)</option>
                                <option value="ILS">שקל (₪)</option>
                            </select>
                        </div>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; color: var(--text-secondary);">מי שילם בפועל?</label>
                        <select id="exp-payer" style="width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #444; background: #1a1a24; color: white; font-family: inherit; font-size: 1rem;">
                            ${PARTICIPANTS.map(p => `<option value="${p}">${p}</option>`).join('')}
                        </select>
                    </div>
                    <div style="margin-bottom: 20px; background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                        <label style="display: block; margin-bottom: 8px; color: var(--text-secondary);">מתחלק בין:</label>
                        <div style="display: flex; gap: 20px;" id="share-checkboxes">
                            ${PARTICIPANTS.map(p => `
                                <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 1.1rem;">
                                    <input type="checkbox" id="exp-share-${p}" value="${p}" checked style="width: 20px; height: 20px; accent-color: var(--accent-green);"> ${p}
                                </label>
                            `).join('')}
                        </div>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button type="submit" id="add-expense-btn" class="btn" style="flex: 2; background: var(--accent-green); font-size: 1.1rem; padding: 12px;">שמור הוצאה</button>
                        <button type="button" class="btn" style="flex: 1; background: #475569; font-size: 1.1rem; padding: 12px;" onclick="document.getElementById('add-expense-section').style.display='none'">ביטול</button>
                    </div>
                </form>
            </div>
            
            <div id="expenses-summary"></div>
            
            <div style="margin-top: 1.5rem; max-height: 400px; overflow-y: auto; border: 1px solid var(--border-card); border-radius: 8px;">
                <table style="width: 100%; text-align: right; border-collapse: collapse; font-size: 1rem;">
                    <thead>
                        <tr style="background: rgba(255,255,255,0.08);">
                            <th style="padding: 12px 10px; border-bottom: 1px solid var(--border-card);">תאריך</th>
                            <th style="padding: 12px 10px; border-bottom: 1px solid var(--border-card);">פרטים</th>
                            <th style="padding: 12px 10px; border-bottom: 1px solid var(--border-card);">סכום</th>
                        </tr>
                    </thead>
                    <tbody id="expenses-log-body">
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    // Default to today
    const tzoffset = (new Date()).getTimezoneOffset() * 60000; 
    const localISOTime = (new Date(Date.now() - tzoffset)).toISOString().slice(0, 10);
    document.getElementById('exp-date').value = localISOTime;
    checkYaakovStatus();
}

function checkYaakovStatus() {
    const dStr = document.getElementById('exp-date').value;
    if(!dStr) return;
    const d = new Date(dStr);
    const cbYaakov = document.getElementById('exp-share-יעקב');
    if (cbYaakov) {
        // Yaakov is active 14.10.2026 - 19.10.2026
        const isYaakovDate = (d >= new Date('2026-10-14') && d <= new Date('2026-10-19'));
        cbYaakov.checked = isYaakovDate;
    }
}

function renderExpenses() {
    document.getElementById('expenses-status').innerHTML = '<i class="fa-solid fa-check" style="color:var(--accent-green);"></i> מעודכן';
    
    const tbody = document.getElementById('expenses-log-body');
    tbody.innerHTML = '';
    
    if (expenses.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 20px; color: var(--text-muted);">אין הוצאות בינתיים</td></tr>';
    } else {
        const displayExp = [...expenses].reverse();
        displayExp.forEach(ex => {
            const sym = ex.currency === 'EUR' ? '€' : '₪';
            const amtStr = `<span dir="ltr">${ex.amount.toFixed(1)} ${sym}</span>`;
            const dObj = new Date(ex.date);
            const dStr = `${dObj.getDate().toString().padStart(2, '0')}/${(dObj.getMonth()+1).toString().padStart(2, '0')}`;
            
            // Format sharedBy safely
            let sharedStr = "";
            if (Array.isArray(ex.sharedBy)) {
                sharedStr = ex.sharedBy.join(', ');
            } else if (typeof ex.sharedBy === 'string') {
                sharedStr = ex.sharedBy.split(',').join(', ');
            }
            
            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 12px 10px; color: var(--text-muted); width: 25%;">${dStr}</td>
                    <td style="padding: 12px 10px;">
                        <strong>${ex.description}</strong><br>
                        <span style="font-size:0.8rem; color:#888;">שילם: <span style="color:var(--accent-orange);">${ex.payer}</span> | חולקים: ${sharedStr}</span>
                    </td>
                    <td style="padding: 12px 10px; font-weight: bold; width: 25%;">${amtStr}</td>
                </tr>
            `;
        });
    }
    
    calculateAndRenderSettlement();
}

function calculateAndRenderSettlement() {
    const balances = {};
    PARTICIPANTS.forEach(p => balances[p] = 0);
    
    expenses.forEach(ex => {
        const amt = parseFloat(ex.amountILS);
        
        let sharedArr = [];
        if (Array.isArray(ex.sharedBy)) sharedArr = ex.sharedBy;
        else if (typeof ex.sharedBy === 'string') sharedArr = ex.sharedBy.split(',').map(s=>s.trim()).filter(s=>s);
        
        const numSharers = sharedArr.length;
        if (numSharers === 0) return;
        
        const share = amt / numSharers;
        if (balances[ex.payer] !== undefined) balances[ex.payer] += amt;
        
        sharedArr.forEach(p => {
            if (balances[p] !== undefined) balances[p] -= share;
        });
    });
    
    const debtors = [];
    const creditors = [];
    PARTICIPANTS.forEach(p => {
        const bal = balances[p];
        if (bal < -0.01) debtors.push({p: p, b: -bal});
        else if (bal > 0.01) creditors.push({p: p, b: bal});
    });
    
    debtors.sort((a,b) => b.b - a.b);
    creditors.sort((a,b) => b.b - a.b);
    
    let settlements = [];
    let i=0, j=0;
    while(i < debtors.length && j < creditors.length) {
        const amt = Math.min(debtors[i].b, creditors[j].b);
        settlements.push(`💸 <strong>${debtors[i].p}</strong> מעביר ל<strong>${creditors[j].p}</strong>: <span dir="ltr">${amt.toFixed(0)} ₪</span>`);
        debtors[i].b -= amt;
        creditors[j].b -= amt;
        if (debtors[i].b < 0.01) i++;
        if (creditors[j].b < 0.01) j++;
    }
    
    let summaryHtml = `
        <div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px; margin-top: 15px; border: 1px solid rgba(255,255,255,0.05);">
            <h4 style="margin-bottom: 15px; color: var(--text-primary); border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px;"><i class="fa-solid fa-scale-balanced"></i> מצב החשבון (בשקלים)</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
    `;
    
    PARTICIPANTS.forEach(p => {
        const bal = balances[p] || 0;
        const color = bal >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';
        const dir = bal >= 0 ? '+' : '';
        summaryHtml += `<div style="flex: 1; min-width: 80px; text-align: center; background: rgba(255,255,255,0.05); padding: 12px 5px; border-radius: 8px;">
            <div style="font-size: 1rem; color: var(--text-secondary); margin-bottom: 5px;">${p}</div>
            <div style="color: ${color}; font-weight: bold; font-size: 1.2rem; direction: ltr;">${dir}${bal.toFixed(0)} ₪</div>
        </div>`;
    });
    summaryHtml += `</div>`;
    
    if (settlements.length > 0) {
        summaryHtml += `<h4 style="margin-bottom: 10px; color: var(--text-primary);">איך מתחשבנים?</h4><ul style="list-style: none; padding: 0; margin: 0;">`;
        settlements.forEach(s => {
            summaryHtml += `<li style="margin-bottom: 8px; padding: 12px; background: rgba(59, 130, 246, 0.15); border-radius: 6px; border-right: 4px solid var(--accent-blue); font-size: 1.05rem;">${s}</li>`;
        });
        summaryHtml += `</ul>`;
    } else {
        if(expenses.length > 0) summaryHtml += `<div style="text-align: center; color: var(--accent-green); font-size: 1.1rem; padding: 10px;"><i class="fa-solid fa-check-circle"></i> כל החשבונות מאוזנים!</div>`;
    }
    
    summaryHtml += `</div>`;
    document.getElementById('expenses-summary').innerHTML = summaryHtml;
}

window.addEventListener('DOMContentLoaded', initExpensesApp);
