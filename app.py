from flask import Flask, request
from flask import render_template, redirect, url_for
import uuid
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
# from db import add_new_day, len_db, show_day
import db
import json
from bson.objectid import ObjectId

from flask import session

app = Flask(__name__)

app.secret_key = 'this is secret key!'


@app.route('/')
def index():
    # print(session)
    if 'loggedin' in session:
        # print("Id user when log in: ", session['ids'])
        # print(session['ids'])
        # show current your money
        this_month = db.get_all_transactions()
        current_money = 0
        income_money = 0
        outcome_money = 0
        categories = [0, 0, 0, 0, 0]
        for item in this_month:
            # print(ObjectId(item['id_user']) == ObjectId(session['ids']))
            # print('Id user retrived from db: ', item['id_user'])

            # kiem tra id user tuong ung
            if ObjectId(item['id_user']) == ObjectId(session['ids']):
                if item['type'] == 'Income':
                    income_money += int(item['expense'])
                elif item['type'] == 'Outcome':
                    outcome_money += int(item['expense'])

            if ObjectId(item['id_user']) == ObjectId(session['ids']):
                if item['category'] == 'Personal':
                    categories[0] += int(item['expense'])
                elif item['category'] == 'Health':
                    categories[1] += int(item['expense'])
                elif item['category'] == 'Family':
                    categories[2] += int(item['expense'])
                elif item['category'] == 'Debt/Loan':
                    categories[3] += int(item['expense'])
                elif item['category'] == 'Income':
                    categories[4] += int(item['expense'])

        current_money = income_money - outcome_money

        # show the main page
        return render_template('index.html', current=current_money, income=income_money, outcome=outcome_money, data=db.get_all_transactions(), categories=categories)
    else:
        return redirect('/login')


@app.route('/add_transaction/')
def show_add_transaction_page():
    if 'loggedin' in session:
        return render_template('form.html')
    return redirect('/login')


@app.route('/add_transaction/', methods=["POST"])
def add_new_transaction():
    if 'loggedin' in session:
        expense_total = request.form.get('expense')
        category = request.form.get('category')
        note = request.form.get('note')
        date = request.form.get('date')
        wallet = request.form.get('wallet')
        in_out = request.form.get('inout')

        new_trans = db.db_add_new_transaction(
            session['ids'],
            expense_total,
            category,
            note,
            date,
            wallet,
            in_out
        )
    
    # should redirect back to charts.html, not index.html
        return redirect(url_for('go_to_charts_page'))
    return redirect('/login')


@app.route('/charts/')
def go_to_charts_page():
    # return render_template('charts.html', data=db.get_all_transactions(), current=current_money, income=income_money, outcome=outcome_money)
    if 'loggedin' in session:
        data = db.get_all_transactions()
        # print(data)
        lst_income = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        lst_outcome = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        lst_totalIncomeOutcome = [50, 50]
        lst_categories = [0, 0, 0, 0, 0] # [Personal, Health, Family, Debt/Loan, Income]
        
        # su dung tung gia tri trong list lst_date lam gia tri de tuong ung voi so thang
        # if sum(lst_income) != 0 and sum(lst_outcome) != 0:
        for item in data:
            # kiem tra id_user tuong ung
            if ObjectId(item['id_user']) == ObjectId(session['ids']):
                date = item['date']
                # print(type(date))
                if item['type'] == 'Income':
                    lst_income[int(date.split('-')[1]) - 1] += int(item['expense'])
                elif item['type'] == 'Outcome':
                    lst_outcome[int(date.split('-')[1]) - 1] += int(item['expense'])

            if ObjectId(item['id_user']) == ObjectId(session['ids']):
        # print(lst_income)
            # print(lst_income)
                if sum(lst_income) != 0 or sum(lst_outcome) != 0:
                    lst_totalIncomeOutcome = [sum(lst_income), sum(lst_outcome)]

            if ObjectId(item['id_user']) == ObjectId(session['ids']):
                # category = item['category']
                # print("Aloooooooooo", category, lst_categories[1])
                if item['category'] == 'Personal':
                    lst_categories[0] += int(item['expense'])
                elif item['category'] == 'Health':
                    lst_categories[1] += int(item['expense'])
                elif item['category'] == 'Family':
                    lst_categories[2] += int(item['expense'])
                elif item['category'] == 'Debt/Loan':
                    lst_categories[3] += int(item['expense'])
                elif item['category'] == 'Income':
                    lst_categories[4] += int(item['expense'])

        # print(lst_totalIncomeOutcome)
        # lst_totalIncomeOutcome = [70, 30]



        return render_template('charts.html', data=db.get_all_transactions(), income=json.dumps(lst_income), outcome=json.dumps(lst_outcome), totalIncomeOutCome=json.dumps(lst_totalIncomeOutcome), id_user=ObjectId(session['ids']), categories=json.dumps(lst_categories))
    return redirect('/login')


@app.route('/charts/', methods=["POST"])
def show_info():
    if 'loggedin' in session:
        return redirect(url_for('go_to_charts_page'))
    return redirect('/login')


@app.route('/delete/<id_item>')
def delete_item(id_item):
    if "loggedin" in session:
        db.delete_item_from_db(id_item)
        return redirect(url_for('go_to_charts_page'))
    return redirect('/login')


@app.route('/edit/<id_item>')
def go_to_edit(id_item):
    # db.update_item_from_db(id_item)
    # should go to page form.html
    if "loggedin" in session:
        return render_template('edit_form.html')
    return redirect('/login')

@app.route('/edit/<id_item>', methods=['POST'])
def edit_item(id_item):
    if "loggedin" in session:
        expense = request.form.get('edit_expense')
        category = request.form.get('edit_category')
        note = request.form.get('edit_note')
        date = request.form.get('edit_date')
        wallet = request.form.get('edit_wallet')
        in_out = request.form.get('in_outcome')

        item_updated = db.update_item_from_db(
            id_item, expense, category, note, date, wallet, in_out)

        return redirect(url_for('go_to_charts_page'))
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', user_valid='', pass_valid='')
    elif request.method == 'POST':
        form = request.form
        username = form.get('username')
        password = form.get('password')

        valid_user = db.get_user_by_name(username)

        if valid_user:
            if valid_user['password'] == password:
                session['loggedin'] = True
                session['username'] = username
                session['ids'] = str(valid_user['_id'])
                return redirect('/')
            else:
                return render_template('login.html', user_valid='', password_valid='Wrong password!')
        else:
            return render_template('login.html', user_valid='user not exist', pass_valid='')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        form = request.form
        username = form.get('username')
        email = form.get('email')
        password = form.get('password')
        exist_user = db.get_user_by_name(username)
        if exist_user:
            return render_template('register.html', message='Name already been used!')
        else:
            db.create_new_user(username, email, password)
            return redirect('/login')


@app.route('/logout')
def logout():
    del session['loggedin']
    del session['username']
    del session['ids']
    return redirect('/login')


if __name__ == '__main__':
    app.debug = True
    app.run()
