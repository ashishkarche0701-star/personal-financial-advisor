from flask import Blueprint, jsonify, request, Response
from flask_login import login_required, current_user
from services.finance_service import monthly_summary
from services.ai_service import generate_advice

api_bp=Blueprint("api",__name__)

@api_bp.get("/summary")
@login_required
def summary():
    data=monthly_summary(current_user.id,request.args.get("month")); data["income"]=float(data["income"]); data["expenses"]=float(data["expenses"]); data["net"]=float(data["net"]); data["budget_total"]=float(data["budget_total"])
    for item in data["category_breakdown"]: item["amount"]=float(item["amount"])
    return jsonify(data)

@api_bp.post("/ai/advice")
@login_required
def ai_advice():
    data=monthly_summary(current_user.id); payload={"month":data["month"],"income":float(data["income"]),"expenses":float(data["expenses"]),"net":float(data["net"]),"savings_rate":data["savings_rate"],"budget_total":float(data["budget_total"]),"category_breakdown":[{"name":x["name"],"amount":float(x["amount"])} for x in data["category_breakdown"]]}; return jsonify(generate_advice(payload))

@api_bp.get("/report.csv")
@login_required
def report_csv():
    data=monthly_summary(current_user.id); lines=["Category,Amount"]
    for row in data["category_breakdown"]:
        safe_name=str(row["name"]).replace('"','""'); lines.append(f'"{safe_name}",{row["amount"]}')
    return Response("\n".join(lines),mimetype="text/csv",headers={"Content-Disposition":f'attachment; filename="finance-{data["month"]}.csv"'})
