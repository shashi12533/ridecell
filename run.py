from app import create_app

flask_app = create_app(rest=True)
flask_app.run(debug=True)
