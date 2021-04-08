#
# Web application for f1
#

from flask import Flask, render_template, request
from web_data import create_race_df, race_by_year
from pretty_html_table import build_table


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/race', methods=["POST"])
def race():
    try:
        year = request.form['year']
        location = request.form['location']
        locations_dict = race_by_year(year)
        location_url = locations_dict[location.lower()]
        df1 = create_race_df(location_url)
        return build_table(df1, color='red_dark')

    except:
        return "404 ERROR: Race Not Found!"


if __name__ == '__main__':
    app.run(host='localhost')


    '''
    <label for="Years">Choose a year:</label>
    <select name="Years" id="year">
      <option value="2020">2020</option>
      <option value="2019">2019</option>
      <option value="2018">2018</option>
      <option value="2017">2017</option>
    </select>

    <br>
    <label for="Locations">Choose a location:</label>
    <select name="Locations" id="location">
      <option value="Bahrain">bahrain</option>
      <option value="Abu Dhabi">abu dhabi</option>
      <option value="Italy">italy</option>
      <option value="Austria">austria</option>
    </select>
    <br>
    <button type="button">Submit</button>
    '''