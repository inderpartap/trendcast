from flask import Flask, render_template, jsonify, request
import util as ut
# import dash
# import dash_html_components as html

app = Flask(__name__)

@app.route('/')
@app.route('/sales')
def index():
    return render_template("base1.html", message="Static Sales Dashboard");   

@app.route('/predictions')
def index2():
    return render_template("base2.html", message="Predictions Dashboard");   

@app.route('/sales/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      cityname = request.form.getlist('city')[0]
      data = ut.read_data(cityname)
      return render_template("sales.html",result = data, city = cityname)


@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html', title='Page not found'), 404


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0' , port=5000)
