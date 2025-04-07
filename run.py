from app import create_app, db
from sqlalchemy import text

app = create_app()

# with app.app_context():
#     # Drop the table using text()
#     db.session.execute(text('DROP TABLE IF EXISTS flaged_incidents'))
#     db.session.commit()
#     # Recreate tables
#     db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
