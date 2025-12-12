from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# ------------------ ADMIN DATA ------------------
admins = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'email': 'admin@srinivasatailors.com'
    }
}

# ------------------ CUSTOMER DATABASE ------------------
CUSTOMERS_FILE = 'customers.json'


def load_customers():
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'r') as f:
            return json.load(f)
    return []


def save_customers(customers):
    with open(CUSTOMERS_FILE, 'w') as f:
        json.dump(customers, f, indent=2)


customers_db = load_customers()

# ------------------ YOUR LOCAL IMAGES ------------------
# Put these files in:  static/images/
#   logo.png, sherwani.jpg, lehenga.jpg
YOUR_IMAGES = {
    'logo': '/static/images/logo.png',
    'sherwani': '/static/images/sherwani.jpg',
    'lehenga': '/static/images/lehenga.jpg'
}

# ------------------ TEMPLATES ------------------

HOME_TEMPLATE = '''
<!DOCTYPE html><html><head><title>Srinivasa Tailors</title><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>*{margin:0;padding:0;box-sizing:border-box;}body{font-family:Arial,sans-serif;background:#000;color:#fff;min-height:100vh;}
.top-menu{position:fixed;top:0;left:0;right:0;height:70px;background:rgba(20,20,20,0.98);backdrop-filter:blur(15px);z-index:1000;display:flex;align-items:center;padding:0 15px;box-shadow:0 4px 20px rgba(255,0,0,0.3);border-bottom:2px solid #e74c3c;}
.menu-logo{height:50px;width:auto;border-radius:10px;margin-right:15px;filter:brightness(1.2);}.menu-title{font-size:22px;font-weight:bold;margin-right:auto;text-shadow:0 0 10px #e74c3c;}
.menu-buttons{display:flex;gap:10px;}.nav-btn{padding:10px 20px;background:linear-gradient(45deg,#e74c3c,#c0392b);color:#fff;border:2px solid #e74c3c;border-radius:20px;font-size:13px;font-weight:bold;cursor:pointer;transition:all 0.3s;text-decoration:none;}
.nav-btn:hover{transform:translateY(-2px);box-shadow:0 5px 15px rgba(231,76,60,0.6);}.main-content{padding:90px 20px 20px;}.hero-section{text-align:center;margin-bottom:40px;}
.hero-section h1{font-size:32px;margin-bottom:15px;color:#e74c3c;text-shadow:0 0 20px #e74c3c;}.hero-section p{font-size:18px;}.clothes-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;}
.cloth-card{background:rgba(30,30,30,0.9);border:2px solid #333;border-radius:15px;overflow:hidden;box-shadow:0 10px 30px rgba(231,76,60,0.3);transition:transform 0.3s;}
.cloth-card:hover{transform:translateY(-8px);border-color:#e74c3c;box-shadow:0 20px 40px rgba(231,76,60,0.5);}.cloth-image{width:100%;height:250px;object-fit:cover;}
.success-message{position:fixed;top:90px;right:10px;background:rgba(39,174,96,0.95);color:#fff;padding:15px;border-radius:10px;box-shadow:0 5px 20px rgba(39,174,96,0.5);z-index:1001;max-width:80vw;}
@media (max-width:480px){.menu-buttons{position:absolute;top:70px;right:10px;background:rgba(20,20,20,0.95);padding:10px;border-radius:10px;flex-direction:column;gap:5px;}}</style></head>
<body>{% with messages=get_flashed_messages() %}{% if messages %}<div class="success-message">{{ messages[0] }}</div>{% endif %}{% endwith %}
<div class="top-menu"><img src="{{ logo }}" alt="Logo" class="menu-logo"><div class="menu-title">Srinivasa Tailors</div><div class="menu-buttons">{% if not session %}<a href="/admin-login" class="nav-btn">👑 Admin</a>{% else %}<a href="/admin-dashboard" class="nav-btn">👑 Dashboard</a><a href="/logout" class="nav-btn">🚪 Logout</a>{% endif %}</div></div>
<div class="main-content"><div class="hero-section"><h1> Premium Tailoring</h1><p>Custom Stitching | Wedding Collection</p></div>
<div class="clothes-grid">
{% for cloth in clothes %}
  <div class="cloth-card">
    <img src="{{ cloth.image }}" alt="{{ cloth.name }}" class="cloth-image">
    <div style="padding:20px;text-align:center;">
      <div style="font-size:20px;">{{ cloth.name }}</div>
      <div style="font-size:24px;color:#e74c3c;font-weight:bold;">{{ cloth.price }}</div>
    </div>
  </div>
{% endfor %}
</div></div>
<script>setTimeout(()=>{document.querySelector('.success-message')?.remove();},5000);</script></body></html>
'''

ADMIN_LOGIN_TEMPLATE = '''
<!DOCTYPE html><html><head><title>Admin Login</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>*{margin:0;padding:0;box-sizing:border-box;}body{font-family:Arial,sans-serif;height:100vh;background:#000;color:#fff;display:flex;flex-direction:column;}
.top-menu{position:fixed;top:0;left:0;right:0;height:70px;background:rgba(20,20,20,0.98);backdrop-filter:blur(15px);z-index:1000;display:flex;align-items:center;padding:0 15px;}
.menu-logo{height:50px;width:auto;border-radius:10px;margin-right:15px;}.menu-title{font-size:22px;font-weight:bold;margin-right:auto;text-shadow:0 0 10px #e74c3c;}.nav-btn{padding:10px 20px;background:linear-gradient(45deg,#e74c3c,#c0392b);color:#fff;border:2px solid #e74c3c;border-radius:20px;font-size:13px;font-weight:bold;text-decoration:none;}
.page-container{flex:1;display:flex;justify-content:center;align-items:center;padding:20px;background:radial-gradient(circle,rgba(231,76,60,0.1) 0%,transparent 70%);}.login-container{background:rgba(20,20,20,0.98);padding:40px;border-radius:20px;box-shadow:0 20px 50px rgba(231,76,60,0.5);width:95%;max-width:400px;text-align:center;border:3px solid #e74c3c;}
h2{color:#e74c3c;margin-bottom:30px;font-size:32px;text-shadow:0 0 20px #e74c3c;}input{width:100%;padding:18px;margin:12px 0;border:2px solid #444;border-radius:12px;background:#222;color:#fff;font-size:16px;}
input:focus{outline:none;border-color:#e74c3c;box-shadow:0 0 20px rgba(231,76,60,0.6);}button{width:100%;padding:18px;background:linear-gradient(45deg,#e74c3c,#c0392b);color:#fff;border:2px solid #e74c3c;border-radius:12px;font-size:18px;font-weight:bold;cursor:pointer;margin-top:15px;}
.error{color:#ff6b6b;background:rgba(231,76,60,0.2);padding:15px;border-radius:10px;margin:15px 0;border-left:5px solid #e74c3c;}</style></head><body>
<div class="top-menu"><img src="{{ logo }}" alt="Logo" class="menu-logo"><div class="menu-title">Srinivasa Tailors</div><a href="/" class="nav-btn">🏠 Home</a></div>
<div class="page-container"><div class="login-container"><h2>👑 Admin Login</h2>{% with messages=get_flashed_messages() %}{% if messages %}<div class="error">{{ messages[0] }}</div>{% endif %}{% endwith %}
<form method="POST"><input type="text" name="username" placeholder="👑 Admin Username" required><input type="password" name="password" placeholder="🔒 Password" required><button type="submit">🚀 Login</button></form></div></div></body></html>
'''

ADMIN_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html><html><head><title>Admin Dashboard</title><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>*{margin:0;padding:0;box-sizing:border-box;}body{font-family:Arial,sans-serif;background:#000;color:#fff;min-height:100vh;}
.top-menu{position:fixed;top:0;left:0;right:0;height:70px;background:rgba(20,20,20,0.98);backdrop-filter:blur(15px);z-index:1000;display:flex;align-items:center;padding:0 15px;}
.menu-logo{height:50px;width:auto;border-radius:10px;margin-right:15px;}.menu-title{font-size:22px;font-weight:bold;margin-right:auto;text-shadow:0 0 10px #e74c3c;}
.nav-btn{padding:10px 20px;background:linear-gradient(45deg,#e74c3c,#c0392b);color:#fff;border:2px solid #e74c3c;border-radius:20px;font-size:13px;font-weight:bold;text-decoration:none;margin-left:10px;}
.dashboard-content{padding:90px 20px;max-width:100%;}.welcome-section{text-align:center;margin-bottom:30px;}.welcome-section h1{font-size:32px;color:#e74c3c;text-shadow:0 0 30px #e74c3c;}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:25px;overflow-x:auto;}.tab-btn{padding:12px 20px;background:rgba(20,20,20,0.8);color:#fff;border:2px solid #333;border-radius:12px;cursor:pointer;font-weight:bold;font-size:14px;flex:1;min-width:120px;}
.tab-btn.active{background:linear-gradient(45deg,#e74c3c,#c0392b);border-color:#e74c3c;}.tab-content{display:none;background:rgba(20,20,20,0.95);padding:25px;border-radius:15px;border:2px solid #333;margin-bottom:20px;}
.tab-content.active{display:block;}.input-field{width:100%;padding:15px;background:#222;color:#fff;border:2px solid #444;border-radius:10px;font-size:16px;margin-bottom:12px;}
.input-field:focus{outline:none;border-color:#e74c3c;box-shadow:0 0 15px rgba(231,76,60,0.5);}.btn{padding:12px 25px;background:linear-gradient(45deg,#e74c3c,#c0392b);color:#fff;border:none;border-radius:12px;font-size:14px;font-weight:bold;cursor:pointer;margin:8px 5px 0 0;}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(231,76,60,0.5);}.btn-success{background:linear-gradient(45deg,#27ae60,#2ecc71);}.btn-edit{background:linear-gradient(45deg,#f39c12,#e67e22);}.btn-delete{background:linear-gradient(45deg,#e74c3c,#c0392b);}
.customer-card{background:rgba(46,204,113,0.2);border:3px solid #27ae60;border-radius:15px;padding:20px;margin:15px 0;}.customer-details{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:15px 0;font-size:13px;}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;}.stat-card{background:rgba(20,20,20,0.9);padding:25px;border-radius:15px;text-align:center;border:2px solid #333;}
@media (max-width:768px){.tabs{flex-direction:column;}.tab-btn{min-width:auto;}.dashboard-content{padding:80px 15px;}.welcome-section h1{font-size:28px;}}@media (max-width:480px){.customer-details{grid-template-columns:1fr;gap:8px;font-size:12px;}}</style>
</head><body>
<div class="top-menu"><img src="{{ logo }}" alt="Logo" class="menu-logo"><div class="menu-title">Srinivasa Tailors</div><a href="/" class="nav-btn">🏠 Home</a><a href="/logout" class="nav-btn">🚪 Logout</a></div>
<div class="dashboard-content"><div class="welcome-section"><h1>👑 Admin Dashboard</h1><p>Customer Management - <strong>{{ user }}</strong></p></div>
<div class="tabs"><button class="tab-btn active" onclick="showTab('stats')">📊 Stats</button><button class="tab-btn" onclick="showTab('customers')">👥 Customers</button><button class="tab-btn" onclick="showTab('add-customer')">➕ Add Customer</button></div>

<div id="stats" class="tab-content active"><div class="stats-grid">
  <div class="stat-card">
    <div style="font-size:45px;color:#e74c3c;">{{ total_customers }}</div>
    <div style="font-size:18px;">Total Customers</div>
  </div>
</div></div>

<div id="customers" class="tab-content">
  <div style="display:flex;flex-direction:column;gap:15px;margin-bottom:25px;">
    <input type="text" class="input-field" id="searchInput" placeholder="🔍 Search by Customer NAME..." onkeyup="searchByName()">
    <button class="btn" onclick="clearSearch()">🔄 Show All</button>
  </div>
  <div id="searchResults">
    {% if customers %}
      {% for customer in customers %}
      <div class="customer-card" style="display:none;" data-name="{{ customer.name.lower() }}">
        <h3>👤 {{ customer.name }} <span style="color:#27ae60;">(ID: {{ customer.id }})</span></h3>
        <div class="customer-details">
          <div><strong>📱</strong> {{ customer.phone }}</div>
          <div><strong>🏠</strong> {{ customer.address }}</div>
          <div><strong>📅</strong> {{ customer.order_date }}</div>
          <div><strong>👕</strong> {{ customer.extra1 }} ({{ customer.shirts_count|default(1) }})</div>
          <div><strong>👖</strong> {{ customer.extra2 }} ({{ customer.pants_count|default(1) }})</div>
          <div><strong>💰</strong> ₹{{ customer.order_amount|default('0') }}</div>
          <div><strong>💳</strong>
            <span style="{% if customer.payment_status == 'Paid' %}color:#27ae60{% elif customer.payment_status == 'Partial' %}color:#f39c12{% else %}color:#ff6b6b{% endif %}">
              {{ customer.payment_status|default('Pending') }}
            </span>
          </div>
        </div>
        <div style="margin-top:15px;">
          <button class="btn btn-edit" onclick="editCustomer({{ customer.id }})">✏️ Edit</button>
          <button class="btn btn-delete" onclick="deleteCustomer({{ customer.id }})">🗑️ Delete</button>
        </div>
      </div>
      {% endfor %}
    {% else %}
      <div style="text-align:center;color:#888;padding:40px;">No customers found</div>
    {% endif %}
  </div>
</div>

<div id="add-customer" class="tab-content">
  <h2 style="color:#e74c3c;margin-bottom:20px;">➕ Add New Customer (10 Fields)</h2>
  <form id="customerForm" method="POST" action="/add-customer">
    <input type="hidden" id="customerId" name="id" value="">
    <input type="text" class="input-field" name="name" id="name" placeholder="👤 Full Name" required>
    <input type="tel" class="input-field" name="phone" id="phone" placeholder="📱 Phone" required>
    <input type="text" class="input-field" name="address" id="address" placeholder="🏠 Address" required>
    <input type="date" class="input-field" name="order_date" id="order_date" value="{{ today }}" required>
    <input type="text" class="input-field" name="extra1" id="extra1" placeholder="👕 Shirt Size" required>
    <input type="text" class="input-field" name="extra2" id="extra2" placeholder="👖 Pant Size" required>
    <input type="number" class="input-field" name="shirts_count" id="shirts_count" placeholder="👕 Shirts Count" min="1" value="1">
    <input type="number" class="input-field" name="pants_count" id="pants_count" placeholder="👖 Pants Count" min="1" value="1">
    <input type="number" class="input-field" name="order_amount" id="order_amount" placeholder="💰 Amount (₹)" min="0" required>
    <select class="input-field" name="payment_status" id="payment_status" required>
      <option value="">💳 Payment Status</option>
      <option value="Paid">✅ Paid</option>
      <option value="Pending">⏳ Pending</option>
      <option value="Partial">↔️ Partial</option>
    </select>
    <button type="submit" class="btn btn-success">💾 Save Customer</button>
    <button type="button" class="btn" onclick="clearForm()">❌ Clear</button>
  </form>
</div></div>

<script>
customersData = {{ customers|tojson|safe }};

function showTab(tabName){
  document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById(tabName).classList.add('active');
}

function searchByName(){
  const input = document.getElementById('searchInput').value.trim().toLowerCase();
  const cards = document.querySelectorAll('.customer-card');
  cards.forEach(card => card.style.display = 'none');
  if(input === '') return;
  cards.forEach(card => {
    if(card.dataset.name.includes(input)) card.style.display = 'block';
  });
}

function clearSearch(){
  document.getElementById('searchInput').value = '';
  location.reload();
}

function editCustomer(id){
  const customer = customersData.find(c => c.id == id);
  if(customer){
    document.getElementById('customerId').value = customer.id;
    document.getElementById('name').value = customer.name || '';
    document.getElementById('phone').value = customer.phone || '';
    document.getElementById('address').value = customer.address || '';
    document.getElementById('order_date').value = customer.order_date || '{{ today }}';
    document.getElementById('extra1').value = customer.extra1 || '';
    document.getElementById('extra2').value = customer.extra2 || '';
    document.getElementById('shirts_count').value = customer.shirts_count || 1;
    document.getElementById('pants_count').value = customer.pants_count || 1;
    document.getElementById('order_amount').value = customer.order_amount || '';
    document.getElementById('payment_status').value = customer.payment_status || '';
    showTab('add-customer');
  }
}

function deleteCustomer(id){
  if(confirm('Delete customer?'))
    fetch('/delete-customer/' + id, {method:'POST'}).then(()=>location.reload());
}

function clearForm(){
  document.getElementById('customerForm').reset();
  document.getElementById('customerId').value = '';
  document.getElementById('order_date').value = '{{ today }}';
  document.getElementById('shirts_count').value = 1;
  document.getElementById('pants_count').value = 1;
}

document.getElementById('customerForm').addEventListener('submit', e=>{
  if(document.getElementById('customerId').value)
    e.target.action = '/edit-customer';
});
</script></body></html>
'''

# ------------------ ROUTES ------------------

@app.route('/', methods=['GET'])
def home():
    # Classic Suit removed: only 2 items now
    clothes = [
        {'name': 'Royal Sherwani', 'price': '₹25,999', 'image': YOUR_IMAGES['sherwani']},
        {'name': 'Designer Lehenga', 'price': '₹18,499', 'image': YOUR_IMAGES['lehenga']}
    ]
    return render_template_string(HOME_TEMPLATE, clothes=clothes, logo=YOUR_IMAGES['logo'], session=session)


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in admins and check_password_hash(admins[username]['password'], password):
            session['user'] = username
            session['type'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        flash('❌ Invalid credentials!')
    return render_template_string(ADMIN_LOGIN_TEMPLATE, logo=YOUR_IMAGES['logo'])


@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user' not in session or session.get('type') != 'admin':
        return redirect(url_for('admin_login'))

    today_str = datetime.now().strftime('%Y-%m-%d')
    return render_template_string(
        ADMIN_DASHBOARD_TEMPLATE,
        user=session['user'],
        logo=YOUR_IMAGES['logo'],
        customers=customers_db,
        total_customers=len(customers_db),
        today=today_str
    )


@app.route('/add-customer', methods=['POST'])
def add_customer():
    if 'user' not in session or session.get('type') != 'admin':
        return redirect(url_for('admin_login'))

    customer_data = {
        'id': len(customers_db) + 1,
        'name': request.form['name'],
        'phone': request.form['phone'],
        'address': request.form['address'],
        'order_date': request.form['order_date'],
        'extra1': request.form['extra1'],
        'extra2': request.form['extra2'],
        'shirts_count': request.form.get('shirts_count', '1'),
        'pants_count': request.form.get('pants_count', '1'),
        'order_amount': request.form.get('order_amount', '0'),
        'payment_status': request.form['payment_status']
    }
    customers_db.append(customer_data)
    save_customers(customers_db)
    flash('✅ Customer added successfully!')
    return redirect(url_for('admin_dashboard'))


@app.route('/edit-customer', methods=['POST'])
def edit_customer():
    if 'user' not in session or session.get('type') != 'admin':
        return redirect(url_for('admin_login'))

    customer_id = int(request.form['id'])
    for customer in customers_db:
        if customer['id'] == customer_id:
            customer.update({
                'name': request.form['name'],
                'phone': request.form['phone'],
                'address': request.form['address'],
                'order_date': request.form['order_date'],
                'extra1': request.form['extra1'],
                'extra2': request.form['extra2'],
                'shirts_count': request.form.get('shirts_count', '1'),
                'pants_count': request.form.get('pants_count', '1'),
                'order_amount': request.form.get('order_amount', '0'),
                'payment_status': request.form['payment_status']
            })
            break

    save_customers(customers_db)
    flash('✅ Customer updated successfully!')
    return redirect(url_for('admin_dashboard'))


@app.route('/delete-customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    if 'user' not in session or session.get('type') != 'admin':
        return redirect(url_for('admin_login'))

    global customers_db
    customers_db = [c for c in customers_db if c['id'] != customer_id]
    save_customers(customers_db)
    return 'OK'


@app.route('/logout')
def logout():
    session.clear()
    flash('✅ Logged out successfully!')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
