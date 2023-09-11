from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from DB import *
from Master_Menu import master_menu
from Master_DBDS import master_dbds
from Query_Generator import query_generator
from Query_Generator_Ext import query_generator_ext
from Master_Definition import master_definition
from Master_Categories import master_categories
from Master_Dictionary import master_dictionaries
from Master_DBDS_EXT import master_dbds_ext

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET123kjnsdfsdf9023112309KEY'
app.config['APP_KEY'] = b'zdNBrplLtMV7li4mBbzRmgg371uy4KdVxEHSPK6O0Qc='
app.config['USE_X_SENDFILE'] = True
CORS(app)
api = Api(app)

app.register_blueprint(master_menu)
app.register_blueprint(master_dbds)
app.register_blueprint(query_generator)
app.register_blueprint(query_generator_ext)
app.register_blueprint(master_definition)
app.register_blueprint(master_categories)
app.register_blueprint(master_dictionaries)
app.register_blueprint(master_dbds_ext)

@app.route('/')
def index():
    return 'Hi there!'

if __name__ == "__main__":
    app.run(debug=True, port = 5006)
