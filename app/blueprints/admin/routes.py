# Denna fil innehåller alla routes för admin-panelen.
# Härifrån kan admin se alla auktioner, skapa nya, redigera, och ta bort dem.
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from functools import wraps
from app.repositories.auction_repo import AuctionRepository
import datetime # Importera datetime för eventuell framtida datumvalidering
from app.blueprints.public.routes import categories as all_categories # Importera kategorilistan
from app.repositories.bid_repo import BidRepository
# Skapar en Blueprint för admin-sidorna. Alla routes här kommer att börja med /admin
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            # Om användaren inte är admin, skicka dem till inloggningssidan
            flash("Du måste vara administratör för att se denna sida.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """Visar admin-panelens startsida med en lista över alla auktioner."""
    # Hämta alla auktioner från databasen via vårt repository
    auction_repo = AuctionRepository()
    all_auctions = auction_repo.get_all()
    return render_template("admin/dashboard.html", auctions=all_auctions)

@admin_bp.route("/auction/new", methods=["GET", "POST"])
@admin_required
def create_auction():
    """Hanterar skapandet av en ny auktion."""
    # Om förfrågan är en POST, betyder det att formuläret har skickats in
    if request.method == "POST":
        # Hämta data från formuläret. .strip() tar bort onödiga mellanslag.
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category")
        starting_bid_str = request.form.get("starting_bid", "").strip()
        end_datetime_from_form = request.form.get("end_datetime")

        end_datetime_for_db = None
        if end_datetime_from_form:
            try:
                # Konvertera från "YYYY-MM-DDTHH:MM" till ett datetime-objekt
                dt_object = datetime.datetime.fromisoformat(end_datetime_from_form)
                # Formatera om objektet till den sträng databasen förväntar sig: "YYYY-MM-DD HH:MM:SS"
                end_datetime_for_db = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                flash("Ogiltigt datumformat.", "error")
                return render_template("admin/auction_form.html", auction=None)

        # Enkel validering för att se till att viktiga fält inte är tomma
        if not title or not description or not end_datetime_for_db:
            flash("Titel, beskrivning och slutdatum är obligatoriska.", "error")
            # Skicka tillbaka användaren till formuläret om något saknas
            return render_template("admin/auction_form.html", auction=None)

        try:
            # Försök att omvandla startbudet till ett heltal.
            starting_bid = int(starting_bid_str) if starting_bid_str else 0
        except ValueError:
            # Om det inte går (t.ex. om någon skrivit bokstäver), visa ett fel.
            flash("Startbud måste vara ett heltal.", "error")
            return render_template("admin/auction_form.html", auction=None)

        auction_repo = AuctionRepository()
        try:
            # Anropa create-metoden i vårt repository för att spara i databasen
            auction_repo.create(title, description, category, starting_bid, end_datetime_for_db)
            flash("Ny auktion har skapats!", "success")
            return redirect(url_for("admin.dashboard"))
        except Exception as e: # Fånga eventuella databasfel
            flash(f"Ett fel uppstod vid skapandet av auktionen: {e}", "error")


    return render_template("admin/auction_form.html", auction=None, categories=all_categories) # För GET-request, visa ett tomt formulär

@admin_bp.route("/auction/<int:auction_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_auction(auction_id):
    """Hanterar redigering av en befintlig auktion."""
    auction_repo = AuctionRepository()
    auction_to_edit = auction_repo.get_by_id(auction_id)
    
    # Om förfrågan är en POST, betyder det att formuläret har skickats in
    if request.method == "POST":
        # Hämta den nya datan från formuläret
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category")
        starting_bid_str = request.form.get("starting_bid", "").strip()
        end_datetime_from_form = request.form.get("end_datetime")

        end_datetime_for_db = None
        if end_datetime_from_form:
            try:
                dt_object = datetime.datetime.fromisoformat(end_datetime_from_form)
                end_datetime_for_db = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                flash("Ogiltigt datumformat.", "error")
                return render_template("admin/auction_form.html", auction=auction_to_edit)

        # Samma validering som när vi skapar en ny auktion
        if not title or not description or not end_datetime_for_db:
            flash("Titel, beskrivning och slutdatum är obligatoriska.", "error")
            return render_template("admin/auction_form.html", auction=auction_to_edit)

        try:
            starting_bid = int(starting_bid_str) if starting_bid_str else 0
        except ValueError:
            flash("Startbud måste vara ett heltal.", "error")
            return render_template("admin/auction_form.html", auction=auction_to_edit)

        try:
            # Anropa update-metoden för att spara ändringarna i databasen
            auction_repo.update(auction_id, title, description, category, starting_bid, end_datetime_for_db)
            flash(f"Auktion '{title}' har uppdaterats!", "success")
            return redirect(url_for("admin.dashboard"))
        except Exception as e: # Fånga eventuella databasfel
            flash(f"Ett fel uppstod vid uppdatering av auktionen: {e}", "error")
            return render_template("admin/auction_form.html", auction=auction_to_edit)

    # För GET-request, visa formuläret med förifylld data och kategorier.
    return render_template("admin/auction_form.html", auction=auction_to_edit, categories=all_categories)

@admin_bp.route("/auction/<int:auction_id>/delete", methods=["POST"])
@admin_required
def delete_auction(auction_id):
    """Hanterar borttagning av en auktion."""
    auction_repo = AuctionRepository()
    # Anropa delete-metoden i repositoryt för att ta bort auktionen
    auction_repo.delete(auction_id)
    flash("Auktionen har tagits bort.", "success") # Visa ett meddelande
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/auction/<int:auction_id>/close", methods=["POST"])
@admin_required
def close_auction(auction_id):
    """Markerar en auktion som avslutad."""
    auction_repo = AuctionRepository()
    # Anropa metoden för att sätta is_closed = 1 i databasen
    auction_repo.mark_as_closed(auction_id)
    flash("Auktionen har markerats som avslutad.", "success") # Visa ett meddelande
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/bid/<int:bid_id>/delete", methods=["POST"])
@admin_required
def delete_bid(bid_id):
    """Hanterar borttagning av ett bud."""
    bid_repo = BidRepository()
    bid_repo.delete_bid(bid_id)
    flash("Budet har tagits bort.", "success")
    # Skicka tillbaka användaren till sidan de kom ifrån (request.referrer).
    # Om request.referrer är tom (t.ex. om de kom direkt hit), skicka dem till admin dashboard som en fallback.
    return redirect(request.referrer or url_for("admin.dashboard"))