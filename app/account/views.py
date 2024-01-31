import flask_login

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.account.forms import AccountForm
from app.crud import creat_account, fetch_account, fetch_accounts


blueprint = Blueprint('account', __name__, url_prefix='/account')


@flask_login.login_required
@blueprint.route('/', methods=['GET', 'POST'])
def get_create_page():
    accounts = fetch_accounts(flask_login.current_user)
    form = AccountForm()
    return render_template('edit/edit.html', form=form, accounts=accounts)


@flask_login.login_required
@blueprint.route('/account', methods=['GET', 'POST'])
def account_create():
    account_form = AccountForm(request.form)
    if not account_form.validate():
        flash('Invalid input.')
    account_data = account_form.data
    account_data.pop('submit')
    current_user = flask_login.current_user
    if not current_user:
        return redirect(url_for('index'))
    account_exists = fetch_account(account_data, current_user)
    if account_exists.id:
        flash('The account already exists')
    else:
        creat_account(account_data)
        flash('The account has been successfully added')
    return redirect(url_for('account.get_create_page'))
