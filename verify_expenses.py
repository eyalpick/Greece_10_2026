import urllib.request
import json
import math
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# 1. Fetch Rates (Simulating once a day fetch)
try:
    url = "https://api.exchangerate-api.com/v4/latest/EUR"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    eur_to_ils = data['rates']['ILS']
except Exception as e:
    # Fallback rate if offline
    eur_to_ils = 4.05

print("--- שער חליפין (נמשך פעם ביום) ---")
print(f"1 אירו = {eur_to_ils} שקלים\n")

# 2. Simulate Expenses
participants = ["אייל", "דני", "יוסי"]
expenses = [
    {"date": "2026-10-08", "description": "ארוחת ערב בטברנה", "payer": "אייל", "amount": 100, "currency": "EUR"},
    {"date": "2026-10-09", "description": "תדלוק רכב", "payer": "דני", "amount": 150, "currency": "ILS"}
]

print("--- רשימת הוצאות ---")
balances = {p: 0 for p in participants}

for exp in expenses:
    # Convert to ILS
    amount_in_ils = exp["amount"]
    if exp["currency"] == "EUR":
        amount_in_ils *= eur_to_ils
    
    share = amount_in_ils / len(participants)
    
    print(f"תאריך: {exp['date']} | תיאור: {exp['description']} | שולם ע\"י: {exp['payer']} | מקור: {exp['amount']} {exp['currency']} | בשקלים: {amount_in_ils:.2f} ILS")
    
    # Update balances
    for p in participants:
        if p == exp["payer"]:
            balances[p] += (amount_in_ils - share)
        else:
            balances[p] -= share

print("\n--- יתרות ביניים --- (מינוס = חייב כסף, פלוס = חייבים לו)")
for p, bal in balances.items():
    print(f"{p}: {bal:.2f} ILS")

print("\n--- אלגוריתם סגירת חובות (Settlement) ---")
debtors = []
creditors = []
for p, bal in balances.items():
    if bal < -0.01:
        debtors.append([p, -bal])
    elif bal > 0.01:
        creditors.append([p, bal])

debtors.sort(key=lambda x: x[1], reverse=True)
creditors.sort(key=lambda x: x[1], reverse=True)

i, j = 0, 0
while i < len(debtors) and j < len(creditors):
    debtor, debt_amount = debtors[i]
    creditor, credit_amount = creditors[j]
    
    settle_amount = min(debt_amount, credit_amount)
    print(f"> {debtor} מעביר ל{creditor} סכום של {settle_amount:.2f} ILS")
    
    debtors[i][1] -= settle_amount
    creditors[j][1] -= settle_amount
    
    if debtors[i][1] < 0.01: i += 1
    if creditors[j][1] < 0.01: j += 1
