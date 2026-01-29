# auction-site-flask

#här är Lisa


classDiagram
    %% Webb-lager (Blueprints)
    class auth_bp {
        &lt;&lt;Blueprint&gt;&gt;
        +login()
        +logout()
    }
    class bid_bp {
        &lt;&lt;Blueprint&gt;&gt;
        +search()
        +place_bid(auction_id)
    }

    %% Logik-lager (Repositories)
    class BaseRepo {
        +query_all(sql, params)
        +query_one(sql, params)
        +execute(sql, params)
    }
    class UserRepo {
        +get_by_email(email)
    }
    class BidRepository {
        +create_bid()
        +get_top_bids()
        +search_auctions()
    }
    class AuctionRepo {
        &lt;&lt;Interface&gt;&gt;
        +get_by_id(id)
    }
    class VoteRepo {
        +count_likes(id)
        +count_dislikes(id)
    }

    %% Arv (Inheritance)
    BaseRepo &lt;|-- UserRepo
    BaseRepo &lt;|-- BidRepository
    BaseRepo &lt;|-- AuctionRepo
    BaseRepo &lt;|-- VoteRepo

    %% Relationer (Beroenden)
    auth_bp --&gt; UserRepo : använder
    bid_bp --&gt; BidRepository : använder
    bid_bp --&gt; VoteRepo : hämtar röster
    bid_bp --&gt; AuctionRepo : validerar status

    %% Databas
    BaseRepo --&gt; Database : kör SQL (database.db)