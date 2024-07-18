from flask import Blueprint, render_template
from flask_login import login_required


admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route("/")
@login_required
def admin_home():
    return render_template("admin.html")