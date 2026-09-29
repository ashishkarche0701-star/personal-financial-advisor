from datetime import date
from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Income, Expense, ExpenseCategory, Budget, SavingsGoal
from services.finance_service import monthly_summary, dashboard_payload

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return redirect(url_for("main.dashboard")) if current_user.is_authenticated else render_template("landing.html")

@main_bp.route("/dashboard")
@login_required
def dashboard(): return render_template("dashboard.html", data=dashboard_payload(current_user.id))

@main_bp.route("/income", methods=["GET", "POST"])
@login_required
def income():
    if request.method == "POST":
        try: amount=Decimal(request.form["amount"]); received_on=date.fromisoformat(request.form["received_on"])
        except (KeyError,ValueError,InvalidOperation): flash("Enter a valid amount and date.","danger"); return redirect(url_for("main.income"))
        db.session.add(Income(user_id=current_user.id, source=request.form.get("source","").strip(), amount=amount, received_on=received_on, note=request.form.get("note","").strip())); db.session.commit(); flash("Income recorded.","success"); return redirect(url_for("main.income"))
    rows=Income.query.filter_by(user_id=current_user.id).order_by(Income.received_on.desc()).all(); return render_template("income.html",rows=rows,today=date.today().isoformat())

@main_bp.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():
    categories=ExpenseCategory.query.filter((ExpenseCategory.user_id==current_user.id)|(ExpenseCategory.user_id.is_(None))).order_by(ExpenseCategory.name).all()
    if request.method == "POST":
        try: amount=Decimal(request.form["amount"]); spent_on=date.fromisoformat(request.form["spent_on"]); category_id=int(request.form["category_id"])
        except (KeyError,ValueError,InvalidOperation): flash("Enter valid expense details.","danger"); return redirect(url_for("main.expenses"))
        category=ExpenseCategory.query.filter(ExpenseCategory.id==category_id,(ExpenseCategory.user_id==current_user.id)|(ExpenseCategory.user_id.is_(None))).first()
        if not category: flash("Invalid category.","danger"); return redirect(url_for("main.expenses"))
        db.session.add(Expense(user_id=current_user.id,category_id=category.id,amount=amount,spent_on=spent_on,merchant=request.form.get("merchant","").strip(),note=request.form.get("note","").strip())); db.session.commit(); flash("Expense recorded.","success"); return redirect(url_for("main.expenses"))
    rows=Expense.query.filter_by(user_id=current_user.id).order_by(Expense.spent_on.desc()).all(); return render_template("expenses.html",rows=rows,categories=categories,today=date.today().isoformat())

@main_bp.route("/budgets", methods=["GET", "POST"])
@login_required
def budgets():
    categories=ExpenseCategory.query.filter((ExpenseCategory.user_id==current_user.id)|(ExpenseCategory.user_id.is_(None))).order_by(ExpenseCategory.name).all(); month=request.args.get("month",date.today().strftime("%Y-%m"))
    if request.method == "POST":
        try: category_id=int(request.form["category_id"]); amount=Decimal(request.form["amount"]); month=request.form["month"]
        except (KeyError,ValueError,InvalidOperation): flash("Enter valid budget details.","danger"); return redirect(url_for("main.budgets"))
        existing=Budget.query.filter_by(user_id=current_user.id,category_id=category_id,month=month).first()
        if existing: existing.amount=amount
        else: db.session.add(Budget(user_id=current_user.id,category_id=category_id,month=month,amount=amount))
        db.session.commit(); flash("Budget saved.","success"); return redirect(url_for("main.budgets",month=month))
    rows=Budget.query.filter_by(user_id=current_user.id,month=month).all(); return render_template("budgets.html",rows=rows,categories=categories,month=month)

@main_bp.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    if request.method == "POST":
        try: target=Decimal(request.form["target_amount"]); current=Decimal(request.form.get("current_amount","0")); target_date=date.fromisoformat(request.form["target_date"]) if request.form.get("target_date") else None
        except (KeyError,ValueError,InvalidOperation): flash("Enter valid savings-goal details.","danger"); return redirect(url_for("main.goals"))
        db.session.add(SavingsGoal(user_id=current_user.id,name=request.form.get("name","").strip(),target_amount=target,current_amount=current,target_date=target_date)); db.session.commit(); flash("Savings goal added.","success"); return redirect(url_for("main.goals"))
    rows=SavingsGoal.query.filter_by(user_id=current_user.id).order_by(SavingsGoal.created_at.desc()).all(); return render_template("goals.html",rows=rows)

@main_bp.route("/reports")
@login_required
def reports(): return render_template("reports.html",data=monthly_summary(current_user.id,request.args.get("month",date.today().strftime("%Y-%m"))))

@main_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.name=request.form.get("name","").strip() or current_user.name
        try: current_user.monthly_income_target=Decimal(request.form.get("monthly_income_target","0"))
        except InvalidOperation: flash("Invalid income target.","danger"); return redirect(url_for("main.profile"))
        db.session.commit(); flash("Profile updated.","success")
    return render_template("profile.html")
