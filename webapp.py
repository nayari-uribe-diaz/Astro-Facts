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
        year = int(request.args.get('year'))
        year_result = get_most_astronauts(year)
        over_year = get_overall_astronauts(year)
        space_missions = get_year_missions(year)
        return render_template('page2.html', options2=years, NationNumbers=year_result , OverNumbers=over_year, SpaceMissions=space_missions)
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
    return country + " had the most astronauts in " + str(year) + " with " + str(most_astronauts) + " astronauts nationwide."
 
 
def get_overall_astronauts(year):
    with open('astronauts.json') as astro_data:
        yr = json.load(astro_data)
    all_astronauts = 0
    for y in yr:
        if y["Profile"]["Selection"]["Year"]== year:
            if y["Profile"]["Astronaut Numbers"]["Overall"] > all_astronauts:
                all_astronauts = y["Profile"]["Astronaut Numbers"]["Overall"]
    return "In " + str(year) + ", there were " + str(all_astronauts) + " astronauts overall."
    
def get_year_missions(year):
    with open('astronauts.json') as astro_data:
        yr = json.load(astro_data)
    year_missions = Markup("<ul>")
    for y in yr:
        if y["Profile"]["Selection"]["Year"] == year:
            year_missions = year_missions + Markup("<li>" + y["Mission"]["Name"] + "</li>")
    year_missions = year_missions + Markup('</ul>')
    return "List of missions in " + str(year) + ": " + year_missions
 
@app.route("/p3")
def render_page3():
    missions=get_mission_options()
    if 'mission' in request.args: 
        mission = request.args.get('mission')
        mission_names = get_mission_names(mission)
        mission_year = get_mission_year(mission)
        return render_template('page3.html', options3=missions, MissionNames=mission_names, MissionYear=mission_year)
    return render_template('page3.html' , options3=missions)
    
    
def get_mission_options():
    with open('astronauts.json') as astro_data:
        mis = json.load(astro_data)
    missions = []
    for m in mis:
        if m["Mission"]["Name"] not in missions:
            missions.append(m["Mission"]["Name"])
    options3=""
    for s in missions:
        options3 += Markup("<option value=\"" + str(s) + "\">" + str(s) + "</option>")
    return options3
    
    
    
def get_mission_names(mission):
    with open('astronauts.json') as astro_data:
        mis = json.load(astro_data)
    names = Markup("<ul>")
    for m in mis:
        if m["Mission"]["Name"] == mission:
            names = names + Markup("<li>" + m["Profile"]["Name"] + "</li>")
    names = names + Markup("</ul>")
    return "List of the people who were on mission " + mission + ": " + names
    
    
def get_mission_year(mission):
    with open('astronauts.json') as astro_data:
        mis = json.load(astro_data)
    year = ""
    for m in mis:
        if m["Mission"]["Name"] == mission:
            year = int(m["Mission"]["Year"])
    return "Mission " + mission + " took place in " + str(year)
    
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url
    
    

if __name__=="__main__":
    app.run(debug=False)