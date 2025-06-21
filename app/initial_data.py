from app.core.db import get_db_connection
def create_tables(): 
    queries = (
        """ 
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'order_status_enum') THEN
                CREATE TYPE order_status_enum AS ENUM (
                    'pending', 
                    'processing', 
                    'shipped', 
                    'delivered', 
                    'cancelled', 
                    'concluded'
                );
            END IF;
        END
        $$;
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        CREATE TABLE IF NOT EXISTS orders (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), 
            customer_id UUID NOT NULL,
            freight NUMERIC(10, 2) NOT NULL,
            status order_status_enum NOT NULL,
            total_price NUMERIC(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS order_product (
            order_id UUID NOT NULL,
            product_id UUID NOT NULL,
            quantity NUMERIC(10, 2) NOT NULL,
            unit_price NUMERIC(10, 2) NOT NULL,
            PRIMARY KEY (order_id, product_id),
            CONSTRAINT fk_order_product_orders
                FOREIGN KEY (order_id)
                REFERENCES orders(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        """
    )
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for command in queries:
                cur.execute(command)
            conn.commit()

def initialize_db(): 
    create_tables()
