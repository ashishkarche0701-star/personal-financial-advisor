from datetime import date
from decimal import Decimal
from sqlalchemy import func
from models import Income, Expense, ExpenseCategory, Budget, SavingsGoal

def month_range(month=None):
    month=month or date.today().strftime("%Y-%m"); year,mon=map(int,month.split("-")); start=date(year,mon,1); end=date(year+1,1,1) if mon==12 else date(year,mon+1,1); return start,end

def monthly_summary(user_id,month=None):
    start,end=month_range(month)
    income=Income.query.filter(Income.user_id==user_id,Income.received_on>=start,Income.received_on<end).with_entities(func.coalesce(func.sum(Income.amount),0)).scalar()
    expenses=Expense.query.filter(Expense.user_id==user_id,Expense.spent_on>=start,Expense.spent_on<end).with_entities(func.coalesce(func.sum(Expense.amount),0)).scalar()
    by_category=Expense.query.join(ExpenseCategory).filter(Expense.user_id==user_id,Expense.spent_on>=start,Expense.spent_on<end).with_entities(ExpenseCategory.name,func.sum(Expense.amount)).group_by(ExpenseCategory.name).order_by(func.sum(Expense.amount).desc()).all()
    budgets=Budget.query.filter_by(user_id=user_id,month=month or date.today().strftime("%Y-%m")).all(); budget_total=sum((Decimal(str(b.amount)) for b in budgets),Decimal("0")); income=Decimal(str(income or 0)); expenses=Decimal(str(expenses or 0)); actual_month=month or date.today().strftime("%Y-%m")
    return {"month":actual_month,"income":income,"expenses":expenses,"net":income-expenses,"savings_rate":float(((income-expenses)/income)*100) if income else 0,"budget_total":budget_total,"category_breakdown":[{"name":n,"amount":Decimal(str(a or 0))} for n,a in by_category]}

def seed_default_categories(user_id,db):
    existing={c.name.lower() for c in ExpenseCategory.query.filter_by(user_id=user_id).all()}; defaults=[("Housing","#2563eb"),("Food","#16a34a"),("Transport","#f59e0b"),("Utilities","#7c3aed"),("Health","#dc2626"),("Shopping","#db2777"),("Entertainment","#0891b2"),("Education","#4f46e5"),("Other","#64748b")]
    for name,color in defaults:
        if name.lower() not in existing: db.session.add(ExpenseCategory(user_id=user_id,name=name,color=color))
    db.session.commit()

def dashboard_payload(user_id):
    summary=monthly_summary(user_id); goals=SavingsGoal.query.filter_by(user_id=user_id).all(); summary["goals"]=[{"name":g.name,"target":float(g.target_amount),"current":float(g.current_amount or 0),"progress":min(100,float((g.current_amount or 0)/g.target_amount*100)) if g.target_amount else 0} for g in goals]; return summary
