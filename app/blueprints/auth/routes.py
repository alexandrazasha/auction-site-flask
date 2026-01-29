# Denna fil hanterar allt som har med inloggning och utloggning att göra.
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.repositories.user_repo import UserRepo

auth_bp = Blueprint("auth", __name__, url_prefix="/auth") # Korrekt: Ingen template_folder

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Skapa en instans av UserRepo för att kunna prata med databasen
    user_repo = UserRepo()

    # Koden inuti denna if-sats körs bara när användaren skickar in formuläret
    if request.method == "POST":
        # Hämta e-postadressen från formuläret
        email = request.form.get("email")
        # Försök hitta en användare i databasen med den e-postadressen
        user = user_repo.get_by_email(email)

        # Om en användare hittades:
        if user:
            # Rensa eventuell gammal sessionsdata
            session.clear()
            # Spara användarens info i sessionen, så vi vet vem som är inloggad
            session["user_id"] = user["id"]
            session["user_email"] = user["email"]
            session["is_admin"] = (user["role"] == "admin")
            flash(f"Välkommen {user['email']}!", "success")
            
            # Om användaren är en admin, skicka till admin-sidan
            if session["is_admin"]:
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("public.index")) # Annars, skicka till startsidan
        else:
            # Om ingen användare hittades, visa ett felmeddelande
            flash("Felaktig e-postadress.", "error")

    return render_template("auth/login.html") # Korrekt: Pekar på app/templates/auth/login.html

@auth_bp.route("/logout")
def logout():
    session.clear()
    # Visa ett meddelande om att utloggningen lyckades
    flash("Du har loggats ut.", "info")
    return redirect(url_for("public.index"))