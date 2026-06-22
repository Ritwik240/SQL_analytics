-- 1. customer_segments
CREATE TABLE customer_segments (
    segment_id          INTEGER       PRIMARY KEY,
    segment_name        VARCHAR(50)   NOT NULL,
    segment_description VARCHAR(255)
);

-- 2. customers
CREATE TABLE customers (
    customer_id         INTEGER       PRIMARY KEY,
    segment_id          INTEGER       REFERENCES customer_segments(segment_id),
    first_name          VARCHAR(50)   NOT NULL,
    last_name           VARCHAR(50)   NOT NULL,
    email               VARCHAR(100)  NOT NULL UNIQUE,
    contact_number      VARCHAR(15),
    city                VARCHAR(50),
    state               VARCHAR(50),
    country             VARCHAR(50)   DEFAULT 'India',
    signup_date         DATE          NOT NULL,
    birth_date          DATE,
    is_active           BOOLEAN       DEFAULT TRUE
);

-- 3. categories
CREATE TABLE categories (
    category_id          INTEGER       PRIMARY KEY,
    category_name        VARCHAR(50)   NOT NULL UNIQUE,
    category_description VARCHAR(255)
);

-- 4. suppliers
CREATE TABLE suppliers (
    supplier_id            INTEGER       PRIMARY KEY,
    supplier_name          VARCHAR(100)  NOT NULL,
    country                VARCHAR(50),
    supplier_rating        DECIMAL(3,1)  CHECK (supplier_rating BETWEEN 1.0 AND 5.0),
    contract_start_date    DATE
);

-- 5. products
CREATE TABLE products (
    product_id      INTEGER        PRIMARY KEY,
    category_id     INTEGER        REFERENCES categories(category_id),
    supplier_id     INTEGER        REFERENCES suppliers(supplier_id),
    product_name    VARCHAR(100)   NOT NULL,
    price           DECIMAL(10,2)  NOT NULL,
    cost_price      DECIMAL(10,2)  NOT NULL,
    stock_quantity  INTEGER        DEFAULT 0,
    launch_date     DATE,
    is_active       BOOLEAN        DEFAULT TRUE
);

-- 6. coupons
CREATE TABLE coupons (
    coupon_id        INTEGER       PRIMARY KEY,
    coupon_code      VARCHAR(20)   NOT NULL UNIQUE,
    discount_percent DECIMAL(5,2)  NOT NULL CHECK (discount_percent BETWEEN 0 AND 100),
    start_date       DATE          NOT NULL,
    end_date         DATE          NOT NULL,
    is_active        BOOLEAN       DEFAULT TRUE
);

-- 7. orders
CREATE TABLE orders (
    order_id          INTEGER        PRIMARY KEY,
    customer_id       INTEGER        REFERENCES customers(customer_id),
    coupon_id         INTEGER        REFERENCES coupons(coupon_id),
    order_date        DATE           NOT NULL,
    order_status      VARCHAR(20)    CHECK (order_status IN ('Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled')),
    shipping_address  VARCHAR(255),
    total_amount      DECIMAL(10,2)
);

-- 8. order_items
CREATE TABLE order_items (
    order_item_id   INTEGER        PRIMARY KEY,
    order_id        INTEGER        REFERENCES orders(order_id),
    product_id      INTEGER        REFERENCES products(product_id),
    quantity        INTEGER        NOT NULL CHECK (quantity > 0),
    unit_price      DECIMAL(10,2)  NOT NULL,
    line_total      DECIMAL(10,2)  NOT NULL
);

-- 9. payments
CREATE TABLE payments (
    payment_id      INTEGER        PRIMARY KEY,
    order_id        INTEGER        REFERENCES orders(order_id),
    payment_method  VARCHAR(20)    CHECK (payment_method IN ('Credit Card', 'Debit Card', 'UPI', 'Wallet', 'Net Banking')),
    payment_amount  DECIMAL(10,2)  NOT NULL,
    payment_date    DATE           NOT NULL,
    payment_status  VARCHAR(20)    CHECK (payment_status IN ('Pending', 'Completed', 'Failed', 'Refunded'))
);

-- 10. shipments
CREATE TABLE shipments (
    shipment_id      INTEGER        PRIMARY KEY,
    order_id         INTEGER        REFERENCES orders(order_id),
    ship_date        DATE,
    delivery_date    DATE,
    shipping_cost    DECIMAL(8,2),
    carrier          VARCHAR(50)    CHECK (carrier IN ('BlueDart', 'DTDC', 'Delhivery', 'FedEx')),
    shipping_status  VARCHAR(20)    CHECK (shipping_status IN ('In Transit', 'Delivered', 'Delayed', 'Returned'))
);

-- 11. returns
CREATE TABLE returns (
    return_id      INTEGER        PRIMARY KEY,
    order_id       INTEGER        REFERENCES orders(order_id),
    order_item_id  INTEGER        REFERENCES order_items(order_item_id),
    return_date    DATE           NOT NULL,
    return_reason  VARCHAR(50)    CHECK (return_reason IN ('Damaged', 'Wrong Item', 'Late Delivery', 'Changed Mind', 'Defective')),
    refund_amount  DECIMAL(10,2)
);

-- 12. reviews
CREATE TABLE reviews (
    review_id     INTEGER       PRIMARY KEY,
    customer_id   INTEGER       REFERENCES customers(customer_id),
    product_id    INTEGER       REFERENCES products(product_id),
    rating        INTEGER       NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_title  VARCHAR(100),
    review_text   VARCHAR(1000),
    review_date   DATE          NOT NULL
);