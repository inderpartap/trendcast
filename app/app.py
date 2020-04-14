from flask import Flask, render_template, jsonify, request, redirect
from utilities import *
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
def sales_data():
   if request.method == 'POST':
      cityname = request.form.getlist('city')[0]
      data = static_data(cityname)
      return render_template("sales.html",result = data, city = cityname)

@app.route('/predictions/result',methods = ['POST', 'GET'])
def sales_predictions():
   if request.method == 'POST':
      cityname = request.form.getlist('city')[0]
      department = request.form.getlist('department')[0]
      department = str.lower(department.replace(" ", ""))
      if department == 'alldepartments':
        data_base, data_weather  = citylevel(cityname)
        return render_template("city_predictions.html", result_base = data_base, result_weather = data_weather, city = cityname)
      else:
        data_base, data_weather = deptlevel(cityname, department)
        return render_template("dept_predictions.html",result = data, city = cityname, department = department)
      


@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html', title='Page not found'), 404


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0' , port=5000)
