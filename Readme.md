Summary
The FastAPI app is set up in main.py with endpoints for users, transactions, search, and logs.

SQLAlchemy is used for ORM with a SQLite database (can later upgrade to PostgreSQL).

Models represent core classes like User, Account, Inventory (singleton with partitions), Item, Category, Transaction, Deposit, and ExternalSystem.

Endpoints provide basic API routes.

CRUD functions and utility modules are stubbed for further development.

This is a basic scratch project that you can extend based on your project requirements.
You now have a basic project skeleton that you can download and run. Just install the requirements (using pip install -r requirments.txt) and start the app with:
uvicorn app.main:app --reload