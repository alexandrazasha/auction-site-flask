PRAGMA foreign_keys = ON;

-- Auctions (objekt som auktioneras)
CREATE TABLE IF NOT EXISTS auctions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  category TEXT,
  starting_bid INTEGER NOT NULL DEFAULT 0,
  end_datetime TEXT NOT NULL,         -- ISO-sträng, t.ex. "2026-01-20 18:00:00"
  is_closed INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Bids (bud)
CREATE TABLE IF NOT EXISTS bids (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  auction_id INTEGER NOT NULL,
  bidder_email TEXT NOT NULL,
  amount INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (auction_id) REFERENCES auctions(id) ON DELETE CASCADE
);

-- Likes/Dislikes (röst per auktion)
-- value: +1 = like, -1 = dislike
CREATE TABLE IF NOT EXISTS votes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  auction_id INTEGER NOT NULL,
  value INTEGER NOT NULL CHECK (value IN (1, -1)),
  voter_email TEXT,                    -- valfritt (kan vara NULL om ni inte vill koppla till användare)
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (auction_id) REFERENCES auctions(id) ON DELETE CASCADE
);

-- Users (enkel auth-stomme)
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL DEFAULT 'user',   -- 'user' eller 'admin'
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Seed (lite testdata så Person 1 kan lista saker direkt)
INSERT INTO auctions (title, description, category, starting_bid, end_datetime)
VALUES
('Vintage klocka', 'Fin klocka i bra skick.', 'Accessoarer', 100, datetime('now', '+2 days')),
('Skidor', 'Skidor för alpint, längd 170.', 'Sport', 500, datetime('now', '+5 days'));

INSERT INTO users (email, role)
VALUES
('admin@example.com', 'admin'),
('user@example.com', 'user');
