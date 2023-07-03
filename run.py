from app import app,db

# run db migration
#with app.app_context():
 # db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

