from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from utilities import *

# import dash
# import dash_html_components as html

app = Flask(__name__)

# using these lists to display the dropdown
cities = [
    "Calgary", "Camrose", "Cranbrook",
    "Edmonton", "Fort St John", "Kamloops", "Kelowna", "Lethbridge",
    "Medicine Hat", "Nelson", "Olds", "Penticton", "Port Alberni",
    "Quesnel", "Red Deer", "Regina",
    "Salmon Arm", "Saskatoon", "Stettler", "Swift Current",
    "Terrace", "Trail", "Vernon", "Wainwright",
    "White Rock", "Williams lake", "Yorkton"
]

departments = [
    "All Departments", "Department 1", "Department 2", "Department 3",
    "Department 4", "Department 5", "Department 6", "Department 7",
    "Department 8", "Department 9", "Department 10", "Department 11",
    "Department 12", "Department 13", "Department 14"
]


@app.route("/")
@app.route("/sales")
def index():
    default = "Calgary"
    return render_template("base1.html", cities=cities, default=default, message="Static Sales Dashboard")


@app.route("/predictions")
def index2():
    default_dept = "All Departments"
    return render_template("base2.html", cities=cities, departments=departments, default_dept=default_dept, message="Predictions Dashboard")


@app.route("/sales/result", methods=["POST", "GET"])
def sales_data():
    if request.method == "POST":
        cityname = request.form.getlist("city")[0]
        data = static_data(cityname)
        # finding the city selected and making it first in the list for display to be consistent // couldn't find a way to used selected option
        cities_copy = cities.copy()
        ind = cities_copy.index(cityname)
        cities_copy[ind], cities_copy[0] = cities_copy[0], cities_copy[ind]
        default = cityname
        return render_template("sales.html", result=data, city=cityname, cities=cities_copy, default=default)


@app.route("/predictions/result", methods=["POST", "GET"])
def sales_predictions():
    cities_copy = cities.copy()
    departments_copy = departments.copy()
    if request.method == "POST":
        cityname = request.form.getlist("city")[0]
        department = request.form.getlist("department")[0]
        department_lower = str.lower(department.replace(" ", ""))
        # finding the city and department selected and making it first in the list for display to be consistent // couldn't find a way to used selected option
        ind = cities_copy.index(cityname)
        cities_copy[ind], cities_copy[0] = cities_copy[0], cities_copy[ind]
        dept_ind = departments_copy.index(department)
        departments_copy[dept_ind], departments_copy[0] = departments_copy[0], departments_copy[dept_ind]

        if department_lower == "alldepartments":
            data_base, data_weather = citylevel(cityname)
            return render_template(
                "city_predictions.html",
                result_base=data_base,
                result_weather=data_weather,
                city=cityname,
                cities=cities_copy,
                departments=departments_copy
            )
        else:
            data_base, data_weather = deptlevel(cityname, department_lower)
            if data_base and data_weather:
                return render_template(
                    "dept_predictions.html",
                    result_base=data_base,
                    result_weather=data_weather,
                    city=cityname,
                    department=department,
                    cities=cities_copy,
                    departments=departments_copy
                )
            else:
                return render_template("no_model.html",
                                       city=cityname,
                                       department=department,
                                       cities=cities_copy,
                                       departments=departments_copy)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="Page not found"), 404


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
