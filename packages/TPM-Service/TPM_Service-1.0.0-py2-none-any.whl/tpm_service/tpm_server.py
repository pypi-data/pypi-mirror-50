from app import app, login_manager, db
from views import views_init

app.logger.info("login manager init")
login_manager.init_app(app)
app.logger.info("db init")
db.create_all()
app.logger.info("views init")
views_init()

if __name__ == '__main__':
    app.run('0.0.0.0', '5000',  debug=True)