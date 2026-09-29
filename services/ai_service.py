import json
from flask import current_app

SYSTEM_PROMPT='''You are a cautious personal-finance assistant inside a budgeting application. Use only the supplied user data. Do not invent transactions or income. Give educational, practical suggestions, not regulated financial advice. Do not recommend specific financial products, securities, loans, or tax strategies. Return valid JSON with keys: summary (string), recommendations (array of strings), warnings (array of strings), budget (object with category names mapped to numeric monthly amounts).'''

def _fallback(data):
    income=float(data.get("income",0)); expenses=float(data.get("expenses",0)); net=income-expenses; recs=[]; warnings=[]
    if income<=0: warnings.append("No income is recorded for this month.")
    if expenses>income and income>0: warnings.append("Recorded spending is above recorded income."); recs.append("Review the largest expense categories and identify non-essential spending to reduce.")
    elif income>0:
        recs.append("Try to create a small automatic savings target before increasing discretionary spending." if net/income*100<10 else "Maintain the current savings habit and review the largest spending category monthly.")
    for item in data.get("category_breakdown",[])[:3]: recs.append(f"Review {item['name']} spending because it is among the highest categories this month.")
    return {"summary":f"Monthly income is ₹{income:,.2f}, expenses are ₹{expenses:,.2f}, and net cash flow is ₹{net:,.2f}.","recommendations":recs[:6],"warnings":warnings,"budget":{}}

def generate_advice(data):
    if current_app.config.get("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client=OpenAI(api_key=current_app.config["OPENAI_API_KEY"]); response=client.chat.completions.create(model=current_app.config["OPENAI_MODEL"],temperature=0.2,response_format={"type":"json_object"},messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":json.dumps(data,default=str)}]); return json.loads(response.choices[0].message.content)
        except Exception: pass
    if current_app.config.get("GEMINI_API_KEY"):
        try:
            from google import genai
            client=genai.Client(api_key=current_app.config["GEMINI_API_KEY"]); response=client.models.generate_content(model=current_app.config["GEMINI_MODEL"],contents=SYSTEM_PROMPT+"\nUSER DATA:\n"+json.dumps(data,default=str),config={"response_mime_type":"application/json"}); return json.loads(response.text)
        except Exception: pass
    return _fallback(data)
