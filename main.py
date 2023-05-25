from src import ROOT
from __init__ import app


for route in ROOT:
    app.add_url_rule(route['path'], methods=route['methods'], view_func=route['function'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)