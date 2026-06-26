import duckdb
import random
from datetime import date, timedelta
from faker import Faker

fake = Faker('en_IN')
random.seed(42)
Faker.seed(42)

DB_PATH = "data/ecommerce.duckdb"
con = duckdb.connect(DB_PATH)

# ── DROP TABLES (in reverse order to respect FK dependencies) ──────────────────

con.execute("DROP TABLE IF EXISTS reviews")
con.execute("DROP TABLE IF EXISTS returns")
con.execute("DROP TABLE IF EXISTS shipments")
con.execute("DROP TABLE IF EXISTS payments")
con.execute("DROP TABLE IF EXISTS order_items")
con.execute("DROP TABLE IF EXISTS orders")
con.execute("DROP TABLE IF EXISTS coupons")
con.execute("DROP TABLE IF EXISTS products")
con.execute("DROP TABLE IF EXISTS suppliers")
con.execute("DROP TABLE IF EXISTS categories")
con.execute("DROP TABLE IF EXISTS customers")
con.execute("DROP TABLE IF EXISTS customer_segments")

# ── CREATE TABLES ──────────────────────────────────────────────────────────────

con.execute("""
    CREATE TABLE customer_segments (
        segment_id          INTEGER PRIMARY KEY,
        segment_name        VARCHAR NOT NULL,
        segment_description VARCHAR
    )
""")

con.execute("""
    CREATE TABLE customers (
        customer_id    INTEGER PRIMARY KEY,
        segment_id     INTEGER REFERENCES customer_segments(segment_id),
        first_name     VARCHAR NOT NULL,
        last_name      VARCHAR NOT NULL,
        email          VARCHAR NOT NULL UNIQUE,
        contact_number VARCHAR,
        city           VARCHAR,
        state          VARCHAR,
        country        VARCHAR DEFAULT 'India',
        signup_date    DATE NOT NULL,
        birth_date     DATE,
        is_active      BOOLEAN DEFAULT TRUE
    )
""")

con.execute("""
    CREATE TABLE categories (
        category_id          INTEGER PRIMARY KEY,
        category_name        VARCHAR NOT NULL UNIQUE,
        category_description VARCHAR
    )
""")

con.execute("""
    CREATE TABLE suppliers (
        supplier_id         INTEGER PRIMARY KEY,
        supplier_name       VARCHAR NOT NULL,
        country             VARCHAR,
        supplier_rating     DECIMAL(3,1),
        contract_start_date DATE
    )
""")

con.execute("""
    CREATE TABLE products (
        product_id     INTEGER PRIMARY KEY,
        category_id    INTEGER REFERENCES categories(category_id),
        supplier_id    INTEGER REFERENCES suppliers(supplier_id),
        product_name   VARCHAR NOT NULL,
        price          DECIMAL(10,2) NOT NULL,
        cost_price     DECIMAL(10,2) NOT NULL,
        stock_quantity INTEGER DEFAULT 0,
        launch_date    DATE,
        is_active      BOOLEAN DEFAULT TRUE
    )
""")

con.execute("""
    CREATE TABLE coupons (
        coupon_id        INTEGER PRIMARY KEY,
        coupon_code      VARCHAR NOT NULL UNIQUE,
        discount_percent DECIMAL(5,2) NOT NULL,
        start_date       DATE NOT NULL,
        end_date         DATE NOT NULL,
        is_active        BOOLEAN DEFAULT TRUE
    )
""")

con.execute("""
    CREATE TABLE orders (
        order_id         INTEGER PRIMARY KEY,
        customer_id      INTEGER REFERENCES customers(customer_id),
        coupon_id        INTEGER REFERENCES coupons(coupon_id),
        order_date       DATE NOT NULL,
        order_status     VARCHAR,
        shipping_address VARCHAR,
        total_amount     DECIMAL(10,2)
    )
""")

con.execute("""
    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id      INTEGER REFERENCES orders(order_id),
        product_id    INTEGER REFERENCES products(product_id),
        quantity      INTEGER NOT NULL,
        unit_price    DECIMAL(10,2) NOT NULL,
        line_total    DECIMAL(10,2) NOT NULL
    )
""")

con.execute("""
    CREATE TABLE payments (
        payment_id     INTEGER PRIMARY KEY,
        order_id       INTEGER REFERENCES orders(order_id),
        payment_method VARCHAR,
        payment_amount DECIMAL(10,2) NOT NULL,
        payment_date   DATE NOT NULL,
        payment_status VARCHAR
    )
""")

con.execute("""
    CREATE TABLE shipments (
        shipment_id     INTEGER PRIMARY KEY,
        order_id        INTEGER REFERENCES orders(order_id),
        ship_date       DATE,
        delivery_date   DATE,
        shipping_cost   DECIMAL(8,2),
        carrier         VARCHAR,
        shipping_status VARCHAR
    )
""")

con.execute("""
    CREATE TABLE returns (
        return_id     INTEGER PRIMARY KEY,
        order_id      INTEGER REFERENCES orders(order_id),
        order_item_id INTEGER REFERENCES order_items(order_item_id),
        return_date   DATE NOT NULL,
        return_reason VARCHAR,
        refund_amount DECIMAL(10,2)
    )
""")

con.execute("""
    CREATE TABLE reviews (
        review_id    INTEGER PRIMARY KEY,
        customer_id  INTEGER REFERENCES customers(customer_id),
        product_id   INTEGER REFERENCES products(product_id),
        rating       INTEGER NOT NULL,
        review_title VARCHAR,
        review_text  VARCHAR,
        review_date  DATE NOT NULL
    )
""")

# ── SEED DATA ──────────────────────────────────────────────────────────────────

# 1. customer_segments
segments = [
    (1, 'Premium',    'High value customers with frequent purchases'),
    (2, 'Regular',    'Average customers with moderate purchase frequency'),
    (3, 'Occasional', 'Customers who buy rarely or seasonally'),
    (4, 'New',        'Customers who signed up in the last 90 days'),
    (5, 'Churned',    'Customers inactive for more than 6 months'),
]
con.executemany("INSERT INTO customer_segments VALUES (?,?,?)", segments)

# 2. customers
CITIES_STATES = [
    ('Mumbai', 'Maharashtra'), ('Delhi', 'Delhi'), ('Bangalore', 'Karnataka'),
    ('Hyderabad', 'Telangana'), ('Chennai', 'Tamil Nadu'), ('Pune', 'Maharashtra'),
    ('Kolkata', 'West Bengal'), ('Ahmedabad', 'Gujarat'), ('Jaipur', 'Rajasthan'),
    ('Surat', 'Gujarat')
]
customers = []
for i in range(1, 501):
    city, state = random.choice(CITIES_STATES)
    signup = fake.date_between(start_date='-3y', end_date='-1m')
    birth  = fake.date_between(start_date='-55y', end_date='-18y')
    customers.append((
        i,
        random.randint(1, 5),
        fake.first_name(),
        fake.last_name(),
        fake.unique.email(),
        fake.phone_number(),
        city, state, 'India',
        signup, birth,
        random.choice([True, True, True, False])
    ))
con.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", customers)

# 3. categories
categories = [
    (1,  'Electronics',     'Gadgets, devices and accessories'),
    (2,  'Clothing',        'Men, women and kids apparel'),
    (3,  'Books',           'Fiction, non-fiction and academic'),
    (4,  'Home & Kitchen',  'Furniture, cookware and decor'),
    (5,  'Sports',          'Fitness equipment and sportswear'),
    (6,  'Beauty',          'Skincare, haircare and cosmetics'),
    (7,  'Toys',            'Kids toys and games'),
    (8,  'Grocery',         'Food, beverages and daily essentials'),
    (9,  'Footwear',        'Shoes, sandals and boots'),
    (10, 'Stationery',      'Pens, notebooks and office supplies'),
    (11, 'Automotive',      'Car and bike accessories'),
    (12, 'Health',          'Medicines, supplements and medical devices'),
    (13, 'Travel',          'Luggage, bags and travel accessories'),
    (14, 'Music',           'Instruments and audio equipment'),
    (15, 'Pet Supplies',    'Food and accessories for pets'),
]
con.executemany("INSERT INTO categories VALUES (?,?,?)", categories)

# 4. suppliers
SUPPLIER_COUNTRIES = ['India', 'China', 'USA', 'Germany', 'Japan']
suppliers = []
for i in range(1, 31):
    suppliers.append((
        i,
        fake.company(),
        random.choice(SUPPLIER_COUNTRIES),
        round(random.uniform(1.0, 5.0), 1),
        fake.date_between(start_date='-5y', end_date='-1y')
    ))
con.executemany("INSERT INTO suppliers VALUES (?,?,?,?,?)", suppliers)

# 5. products
products = []
for i in range(1, 101):
    price      = round(random.uniform(99, 49999), 2)
    cost_price = round(price * random.uniform(0.3, 0.65), 2)
    products.append((
        i,
        random.randint(1, 15),
        random.randint(1, 30),
        fake.catch_phrase(),
        price,
        cost_price,
        random.randint(0, 500),
        fake.date_between(start_date='-3y', end_date='-1m'),
        random.choice([True, True, True, True, False])
    ))
con.executemany("INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?)", products)

# 6. coupons
COUPON_PREFIXES = ['SAVE', 'DEAL', 'OFFER', 'SALE', 'FEST', 'FLAT']
coupons = []
used_codes = set()
for i in range(1, 51):
    start = fake.date_between(start_date='-1y', end_date='today')
    end   = start + timedelta(days=random.randint(7, 60))
    while True:
        code = f"{random.choice(COUPON_PREFIXES)}{random.randint(10, 999)}"
        if code not in used_codes:
            used_codes.add(code)
            break
    coupons.append((
        i,
        code,
        round(random.uniform(5, 70), 2),
        start,
        end,
        random.choice([True, True, False])
    ))
con.executemany("INSERT INTO coupons VALUES (?,?,?,?,?,?)", coupons)

# 7. orders
ORDER_STATUSES = ['Pending', 'Confirmed', 'Shipped', 'Delivered', 'Delivered',
                  'Delivered', 'Cancelled']
orders = []
for i in range(1, 2001):
    order_date = fake.date_between(start_date='-2y', end_date='today')
    coupon_id  = random.choice([None, None, None, random.randint(1, 50)])
    orders.append((
        i,
        random.randint(1, 500),
        coupon_id,
        order_date,
        random.choice(ORDER_STATUSES),
        fake.address().replace('\n', ', '),
        None  # total_amount updated after order_items are inserted
    ))
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", orders)

# 8. order_items
order_items = []
item_id = 1
order_totals = {}
for order_id, *_ in orders:
    num_items = random.randint(1, 5)
    order_total = 0
    for _ in range(num_items):
        product    = random.choice(products)
        product_id = product[0]
        unit_price = product[4]  # price column
        quantity   = random.randint(1, 4)
        line_total = round(unit_price * quantity, 2)
        order_items.append((item_id, order_id, product_id, quantity,
                            unit_price, line_total))
        order_total += line_total
        item_id += 1
    order_totals[order_id] = round(order_total, 2)
con.executemany("INSERT INTO order_items VALUES (?,?,?,?,?,?)", order_items)

# update total_amount on orders
for order_id, total in order_totals.items():
    con.execute("UPDATE orders SET total_amount = ? WHERE order_id = ?",
                [total, order_id])

# 9. payments
PAYMENT_METHODS  = ['Credit Card', 'Debit Card', 'UPI', 'Wallet', 'Net Banking']
PAYMENT_STATUSES = ['Completed', 'Completed', 'Completed', 'Failed', 'Refunded']
payments = []
for idx, (order_id, *rest) in enumerate(orders):
    order_date = rest[2]  # order_date position
    payments.append((
        idx + 1,
        order_id,
        random.choice(PAYMENT_METHODS),
        order_totals[order_id],
        order_date,
        random.choice(PAYMENT_STATUSES)
    ))
con.executemany("INSERT INTO payments VALUES (?,?,?,?,?,?)", payments)

# 10. shipments
CARRIERS  = ['BlueDart', 'DTDC', 'Delhivery', 'FedEx']
SHIP_STATUSES = ['Delivered', 'Delivered', 'In Transit', 'Delayed', 'Returned']
shipments = []
for idx, (order_id, _, __, order_date, order_status, *___) in enumerate(orders):
    if order_status in ('Pending', 'Confirmed', 'Cancelled'):
        continue
    ship_date     = order_date + timedelta(days=random.randint(1, 3))
    delivery_date = ship_date  + timedelta(days=random.randint(2, 7))
    shipments.append((
        idx + 1,
        order_id,
        ship_date,
        delivery_date,
        round(random.uniform(40, 200), 2),
        random.choice(CARRIERS),
        random.choice(SHIP_STATUSES)
    ))
con.executemany("INSERT INTO shipments VALUES (?,?,?,?,?,?,?)", shipments)

# 11. returns
RETURN_REASONS = ['Damaged', 'Wrong Item', 'Late Delivery', 'Changed Mind', 'Defective']
returns = []
return_id = 1
delivered_items = [
    (oi[0], oi[1]) for oi in order_items
    if any(o[0] == oi[1] and o[4] == 'Delivered' for o in orders)
]
sampled_returns = random.sample(delivered_items, min(300, len(delivered_items)))
for order_item_id, order_id in sampled_returns:
    order_date  = next(o[3] for o in orders if o[0] == order_id)
    return_date = order_date + timedelta(days=random.randint(3, 15))
    refund      = round(random.uniform(100, 5000), 2)
    returns.append((
        return_id, order_id, order_item_id,
        return_date,
        random.choice(RETURN_REASONS),
        refund
    ))
    return_id += 1
con.executemany("INSERT INTO returns VALUES (?,?,?,?,?,?)", returns)

# 12. reviews
reviews = []
review_id = 1
reviewed = set()
for order_item_id, order_id, product_id, *_ in order_items:
    if review_id > 1000:
        break
    customer_id = next(o[1] for o in orders if o[0] == order_id)
    if (customer_id, product_id) in reviewed:
        continue
    if random.random() < 0.2:  # ~20% of items get a review
        order_date   = next(o[3] for o in orders if o[0] == order_id)
        review_date  = order_date + timedelta(days=random.randint(1, 30))
        reviews.append((
            review_id,
            customer_id,
            product_id,
            random.randint(1, 5),
            fake.sentence(nb_words=6),
            fake.paragraph(nb_sentences=2),
            review_date
        ))
        reviewed.add((customer_id, product_id))
        review_id += 1
con.executemany("INSERT INTO reviews VALUES (?,?,?,?,?,?,?)", reviews)

con.close()
print("Data generation complete.")
print(f"  customer_segments : {len(segments)}")
print(f"  customers         : {len(customers)}")
print(f"  categories        : {len(categories)}")
print(f"  suppliers         : {len(suppliers)}")
print(f"  products          : {len(products)}")
print(f"  coupons           : {len(coupons)}")
print(f"  orders            : {len(orders)}")
print(f"  order_items       : {len(order_items)}")
print(f"  payments          : {len(payments)}")
print(f"  shipments         : {len(shipments)}")
print(f"  returns           : {len(returns)}")
print(f"  reviews           : {len(reviews)}")