from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.repositories.user_repo import UserRepo

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    user_repo = UserRepo()

    if request.method == "POST":
        email = request.form.get("email")
        user = user_repo.get_by_email(email)

        # Enkel "dummy" inloggning. I en riktig app hade vi verifierat lösenord.
        if user:
            session.clear()
            session["user_id"] = user["id"]
            session["user_email"] = user["email"]
            session["is_admin"] = (user["role"] == "admin")
            flash(f"Välkommen {user['email']}!", "success")
            
            if session["is_admin"]:
                return redirect(url_for("admin.dashboard")) # Skickar till admin-sidan
            return redirect(url_for("public.index")) # Skickar till startsidan
        else:
            flash("Felaktig e-postadress.", "error")

    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Du har loggats ut.", "info")
    return redirect(url_for("public.index"))