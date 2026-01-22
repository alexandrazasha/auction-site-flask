from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(f):
    """En decorator för att säkerställa att användaren är en inloggad admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Du måste vara administratör för att se denna sida.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """Visar admin-panelens startsida."""
    return render_template("admin/dashboard.html")