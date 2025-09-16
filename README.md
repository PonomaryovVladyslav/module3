# Demo Shop (Django) (module3)

A small teaching/demo project that showcases a minimal shop with products, orders, and refunds. It is intended to be shown to students as a non‑empty project with ready data and images.

## Highlights
- Store page with a responsive, card‑based product grid
- User auth: register, login, logout
- Wallet balance display for the signed‑in user
- Create orders and view “My orders” with refund requests
- Admin pages to add/edit products and review refunds
- Polished dark UI built with simple CSS (no framework)

## Admin access (for demo)
- Username: `admin`
- Password: `1`

## Included demo data
- A SQLite database `db.sqlite3` is included so the app opens with products, orders, and users already present.
- Sample product images are included under `media/products/` so the UI looks populated out of the box.

If you prefer to start from scratch, you can delete `db.sqlite3` and the `media/` folder and then run migrations to create a fresh database.

## Quickstart
1) Create a virtual environment and install dependencies

````bash
python3 -m venv .venv
source .venv/bin/activate  # on Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
````

2) Run the development server (uses the included SQLite DB and images)

````bash
python manage.py runserver
````

3) Visit the app
- Store: `http://127.0.0.1:8000/`


## Notes
- Product images are stored in `media/products/` (Django `ImageField(upload_to='products/')`).
- The UI aims to be minimal and readable for instruction purposes; feel free to extend components or styles in `static/css/styles.css` and `static/js/main.js`.
- If you reset the database, create a new superuser:

````bash
python manage.py migrate
python manage.py createsuperuser
````

Enjoy teaching with a ready-to-show, non‑empty project!
