from flask import Flask, url_for, render_template, request
 #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

from markupsafe import Markup

import os
import json

app = Flask(__name__)


@app.route("/")
def render_main():
    nationalities = get_country_options()
    years = get_year_options()
    return render_template('home.html', options=nationalities, options2=years)
    
    
@app.route("/p1")
def render_page1():
    nationalities = get_country_options()
    if "nationality" in request.args: 
        nationality = request.args.get('nationality')
        result = get_longest_eva(nationality)
        result2 = get_longest_mission(nationality)
        return render_template('page1.html', options=nationalities, EVA=result, Mission=result2)
    return render_template('page1.html' , options=nationalities)
    
    
def get_country_options():
    with open('astronauts.json') as astro_data:
        nat = json.load(astro_data)
    nationalities = []
    for n in nat:
        if n["Profile"]["Nationality"] not in nationalities:
            nationalities.append(n["Profile"]["Nationality"])
    options=""
    for t in nationalities:
        options += Markup("<option value=\"" + t + "\">" + t + "</option>")
    return options


def get_longest_eva(nationality):
    with open('astronauts.json') as astro_data:
        nat = json.load(astro_data)
    highest_EVA  = 0
    name = ""
    for n in nat:
        if n["Profile"]["Nationality"]== nationality:
            if n["Profile"]["Lifetime Statistics"]["EVA duration"] > highest_EVA:
                highest_EVA = n["Profile"]["Lifetime Statistics"]["EVA duration"]
                name = n["Profile"]["Name"]
    return "The astronaut: " + name + " has the longest EVA duration in " + nationality + " with EVA being " + str(highest_EVA) + " hours."


def get_longest_mission(nationality):
    with open('astronauts.json') as astro_data:
        nat = json.load(astro_data)
    highest_mission  = 0
    name = ""
    for n in nat:
        if n["Profile"]["Nationality"]== nationality:
            if n["Profile"]["Lifetime Statistics"]["Mission duration"] > highest_mission:
                highest_mission = n["Profile"]["Lifetime Statistics"]["Mission duration"]
                name = n["Profile"]["Name"]
    return "The astronaut: " + name + " has the longest mission duration in " + nationality + " with mission duration being " + str(highest_mission) + " hours."


@app.route("/p2")
def render_page2():
    years=get_year_options()
    if "year" in request.args: 
        year = request.args.get('year')
        year_result = get_most_astronauts(year)
        return render_template('page2.html', options2=years, NationNumbers=year_result)
    return render_template('page2.html' , options2=years)
 
def get_year_options():
    with open('astronauts.json') as astro_data:
        yr = json.load(astro_data)
    years = []
    for y in yr:
        if y["Profile"]["Selection"]["Year"] not in years:
            years.append(y["Profile"]["Selection"]["Year"])
    options2=""
    for r in years:
        options2 += Markup("<option value=\"" + str(r) + "\">" + str(r) + "</option>")
    return options2
 
 
def get_most_astronauts(year):
    with open('astronauts.json') as astro_data:
        yr = json.load(astro_data)
    most_astronauts= 0
    country = ""
    for y in yr:
        if y["Profile"]["Selection"]["Year"]== year:
            if y["Profile"]["Astronaut Numbers"]["Nationwide"] > most_astronauts:
                most_astronauts = y["Profile"]["Astronaut Numbers"]["Nationwide"]
                country = y["Profile"]["Nationality"]
    return country + " had the most astronauts in " + year + " with " + str(most_astronauts) + " astronauts nationwide."
 
 
@app.route("/p3")
def render_page3():
    
    return render_template('page3.html')
    
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url
    
    

if __name__=="__main__":
    app.run(debug=False)