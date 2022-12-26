-- Products --
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    list_price INTEGER NOT NULL
);


-- Orders --
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actual_price INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY  (product_id) REFERENCES products(id)
);