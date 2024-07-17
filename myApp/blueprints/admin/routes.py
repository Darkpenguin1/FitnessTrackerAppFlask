"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from myApp import db
from myApp.models import User, Exercise
from sqlalchemy.exc import IntegrityError
from flask_admin import Admin

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route("/admin/")
@login_required
def admin_home():
    return render_template("view.html", values=User.query.all())
"""