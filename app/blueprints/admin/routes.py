from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from functools import wraps
from app.repositories.auction_repo import AuctionRepository
import datetime # Importera datetime för eventuell framtida datumvalidering

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
    """Visar admin-panelens startsida med en lista över alla auktioner."""
    auction_repo = AuctionRepository()
    all_auctions = auction_repo.get_all()
    return render_template("admin/dashboard.html", auctions=all_auctions)

@admin_bp.route("/auction/new", methods=["GET", "POST"])
@admin_required
def create_auction():
    """Hanterar skapandet av en ny auktion."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category")
        starting_bid_str = request.form.get("starting_bid", "").strip()
        end_datetime_str = request.form.get("end_datetime", "").strip()

        # Grundläggande validering
        if not title or not description or not end_datetime_str:
            flash("Titel, beskrivning och slutdatum är obligatoriska.", "error")
            return render_template("admin/auction_form.html", auction=None)

        try:
            starting_bid = int(starting_bid_str) if starting_bid_str else 0
            # Här kan du lägga till mer robust datumvalidering om du vill, t.ex.
            # datetime.datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            flash("Startbud måste vara ett heltal.", "error")
            return render_template("admin/auction_form.html", auction=None)

        auction_repo = AuctionRepository()
        try:
            auction_repo.create(title, description, category, starting_bid, end_datetime_str)
            flash("Ny auktion har skapats!", "success")
            return redirect(url_for("admin.dashboard"))
        except Exception as e: # Fånga eventuella databasfel
            flash(f"Ett fel uppstod vid skapandet av auktionen: {e}", "error")


    return render_template("admin/auction_form.html", auction=None) # Skickar med auction=None för att visa ett tomt formulär

@admin_bp.route("/auction/<int:auction_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_auction(auction_id):
    """Hanterar redigering av en befintlig auktion."""
    auction_repo = AuctionRepository()
    auction_to_edit = auction_repo.get_by_id(auction_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category")
        starting_bid_str = request.form.get("starting_bid", "").strip()
        end_datetime_str = request.form.get("end_datetime", "").strip()

        # Grundläggande validering
        if not title or not description or not end_datetime_str:
            flash("Titel, beskrivning och slutdatum är obligatoriska.", "error")
            return render_template("admin/auction_form.html", auction=auction_to_edit)

        try:
            starting_bid = int(starting_bid_str) if starting_bid_str else 0
            # Här kan du lägga till mer robust datumvalidering om du vill
        except ValueError:
            flash("Startbud måste vara ett heltal.", "error")
            return render_template("admin/auction_form.html", auction=auction_to_edit)

        try:
            auction_repo.update(auction_id, title, description, category, starting_bid, end_datetime_str)
            flash(f"Auktion '{title}' har uppdaterats!", "success")
            return redirect(url_for("admin.dashboard"))
        except Exception as e: # Fånga eventuella databasfel
            flash(f"Ett fel uppstod vid uppdatering av auktionen: {e}", "error")
            return render_template("admin/auction_form.html", auction=auction_to_edit)

    # För GET-request, visa formuläret med förifylld data
    return render_template("admin/auction_form.html", auction=auction_to_edit)