from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='omesh',  # <-- change this
    database='shop_db'
)
cursor = conn.cursor(dictionary=True)

# Home
@app.route('/')
def home():
    return render_template('home.html')

# ---------------- SELLER ----------------
@app.route('/seller_register', methods=['GET', 'POST'])
def seller_register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM sellers WHERE username = %s", (username,))
        if cursor.fetchone():
            flash("Username already exists!")
            return redirect(url_for('seller_register'))

        cursor.execute("INSERT INTO sellers (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
        conn.commit()
        flash("Seller registered successfully!")
        return redirect(url_for('seller_login'))

    return render_template('seller_register.html')

@app.route('/seller_login', methods=['GET', 'POST'])
def seller_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM sellers WHERE username = %s AND password = %s", (username, password))
        seller = cursor.fetchone()
        if seller:
            return redirect(url_for('seller_dashboard', seller_id=seller['id']))
        else:
            flash("Invalid credentials")
            return redirect(url_for('seller_login'))
    return render_template('seller_login.html')

@app.route('/seller/<int:seller_id>')
def seller_dashboard(seller_id):
    cursor.execute("SELECT * FROM sellers WHERE id = %s", (seller_id,))
    seller = cursor.fetchone()
    cursor.execute("SELECT * FROM products WHERE seller_id = %s", (seller_id,))
    products = cursor.fetchall()

    cursor.execute("""
        SELECT products.name, COUNT(orders.id) AS order_count, SUM(products.price) AS total_revenue
        FROM products
        LEFT JOIN orders ON products.id = orders.product_id
        WHERE products.seller_id = %s
        GROUP BY products.name
    """, (seller_id,))
    chart_data = cursor.fetchall()

    product_names = [p['name'] for p in chart_data]
    order_counts = [p['order_count'] for p in chart_data]
    revenues = [p['total_revenue'] for p in chart_data]

    return render_template('seller_dashboard.html', seller_name=seller['name'],
                           products=products, seller_id=seller_id,
                           product_names=product_names,
                           order_counts=order_counts,
                           revenues=revenues)

@app.route('/seller/<int:seller_id>/add', methods=['POST'])
def add_product(seller_id):
    name = request.form['name']
    price = float(request.form['price'])
    cursor.execute("INSERT INTO products (name, price, seller_id) VALUES (%s, %s, %s)", (name, price, seller_id))
    conn.commit()
    return redirect(url_for('seller_dashboard', seller_id=seller_id))

@app.route('/seller/<int:seller_id>/delete/<int:product_id>')
def delete_product(seller_id, product_id):
    cursor.execute("DELETE FROM products WHERE id = %s AND seller_id = %s", (product_id, seller_id))
    conn.commit()
    return redirect(url_for('seller_dashboard', seller_id=seller_id))

@app.route('/seller/<int:seller_id>/orders')
def view_orders(seller_id):
    cursor.execute("""
        SELECT orders.*, products.name AS product_name, buyers.name AS buyer_name
        FROM orders
        JOIN products ON orders.product_id = products.id
        JOIN buyers ON orders.buyer_id = buyers.id
        WHERE products.seller_id = %s
    """, (seller_id,))
    orders = cursor.fetchall()

    cursor.execute("SELECT * FROM sellers WHERE id = %s", (seller_id,))
    seller = cursor.fetchone()
    session['seller_id'] = seller_id
    session['seller_name'] = seller['name']
    return render_template('seller_orders.html', orders=orders, seller_name=seller['name'])

@app.route('/seller/<int:seller_id>/orders/update/<int:order_id>', methods=['POST'])
def update_order_status(seller_id, order_id):
    new_status = request.form['status']
    cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, order_id))
    conn.commit()
    flash("Order status updated!")
    return redirect(url_for('view_orders', seller_id=seller_id))

# ---------------- BUYER ----------------
@app.route('/buyer_register', methods=['GET', 'POST'])
def buyer_register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM buyers WHERE username = %s", (username,))
        if cursor.fetchone():
            flash("Username already exists!")
            return redirect(url_for('buyer_register'))

        cursor.execute("INSERT INTO buyers (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
        conn.commit()
        flash("Buyer registered successfully!")
        return redirect(url_for('buyer_login'))

    return render_template('buyer_register.html')

@app.route('/buyer_login', methods=['GET', 'POST'])
def buyer_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM buyers WHERE username = %s AND password = %s", (username, password))
        buyer = cursor.fetchone()
        if buyer:
            session['buyer_id'] = buyer['id']
            session['buyer_name'] = buyer['name']
            return redirect(url_for('buyer_dashboard', buyer_id=buyer['id']))
        else:
            flash("Invalid credentials")
            return redirect(url_for('buyer_login'))
    return render_template('buyer_login.html')

@app.route('/buyer/<int:buyer_id>')
def buyer_dashboard(buyer_id):
    if 'buyer_id' not in session or session['buyer_id'] != buyer_id:
        flash("Please login first!")
        return redirect(url_for('buyer_login'))

    buyer_name = session['buyer_name']
    cursor.execute("""
        SELECT products.*, sellers.name AS seller_name
        FROM products
        JOIN sellers ON products.seller_id = sellers.id
    """)
    products = cursor.fetchall()

    return render_template('buyer_dashboard.html', products=products, buyer_name=buyer_name, buyer_id=buyer_id)

@app.route('/buyer/<int:buyer_id>/order/<int:product_id>', methods=['GET', 'POST'])
def place_order(buyer_id, product_id):
    if request.method == 'POST':
        address = request.form['address']
        mobile = request.form['mobile']
        payment_method = request.form['payment_method']

        cursor.execute("""
            INSERT INTO orders (buyer_id, product_id, status, address, mobile, payment_method)
            VALUES (%s, %s, 'Placed', %s, %s, %s)
        """, (buyer_id, product_id, address, mobile, payment_method))
        conn.commit()

        flash("✅ Order placed successfully!")
        return redirect(url_for('buyer_dashboard', buyer_id=buyer_id))
    return render_template('order_form.html', buyer_id=buyer_id)

@app.route('/buyer/<int:buyer_id>/orders')
def buyer_orders(buyer_id):
    if 'buyer_id' not in session or session['buyer_id'] != buyer_id:
        flash("Please login first!")
        return redirect(url_for('buyer_login'))

    cursor.execute("""
        SELECT orders.*, products.name AS product_name, sellers.name AS seller_name
        FROM orders
        JOIN products ON orders.product_id = products.id
        JOIN sellers ON products.seller_id = sellers.id
        WHERE orders.buyer_id = %s
    """, (buyer_id,))
    orders = cursor.fetchall()

    return render_template('buyer_orders.html', orders=orders, buyer_name=session['buyer_name'], buyer_id=buyer_id)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect(url_for('home'))

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
