DROP TABLE IF EXISTS setter;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS giftee;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE giftee (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  selected TEXT 
);

CREATE TABLE setter (
  id INTEGER,
  gifter_id INTEGER, 
  giftee_id INTEGER, 
  FOREIGN KEY (gifter_id) REFERENCES user (id), 
  FOREIGN KEY (giftee_id) REFERENCES giftee (id)
  PRIMARY KEY (gifter_id, giftee_id)
);

INSERT INTO giftee VALUES (1, "Merai", "no");
INSERT INTO giftee VALUES (2, "Nathan", "no"); 
INSERT INTO giftee VALUES (3, "Rachael", "no"); 
INSERT INTO giftee VALUES (4, "Matt", "no"); 
INSERT INTO giftee VALUES (5, "Chantel", "no"); 
INSERT INTO giftee VALUES (6, "Ethan", "no"); 
INSERT INTO giftee VALUES (7, "Jonny", "no"); 
INSERT INTO giftee VALUES (8, "Noah", "no"); 
INSERT INTO giftee VALUES (9, "Zack", "no"); 
