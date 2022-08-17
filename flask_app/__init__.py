from flask import Flask

app = Flask("Painting_App_Server", 
            template_folder='flask_app/templates', 
            static_folder='flask_app/static',)

app.secret_key = 'rg52{4C"(dTo(m'
