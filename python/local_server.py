
# importing flask module
from flask import Flask

# initializing a variable of Flask
app = Flask(__name__)


# decorating index function with the app.route
@app.route('/sample')
def index():
   return "WELCOME!!! This is the home page {}".format(name)

if __name__ == "__main__":
   app.run()

