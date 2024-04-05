from flask import Flask, url_for, render_template, request
 #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

from markupsafe import Markup

import os
import json

app = Flask(__name__)


@app.route("/")
def render_main():
    nationalities = get_country_options()
    return render_template('home.html', options=nationalities)
    
    
    
@app.route("/p1")
def render_page1():
    nationalities = get_country_options()
    nationality = request.args.get('nationality')
    astronaut = request.args.get('astronaut')
    nat = get_longest_eva(astronaut)
    EVA_duration = "The astronaut: " + nat + "has the longest EVA duration in" + nat
    return render_template('page1.html', options=nationalities, EVA=EVA_duration)
 
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

def get_longest_eva(astronaut):
    with open('astronauts.json') as astro_data:
        nation = json.load(astro_data)
    highest_EVA  = 0
    nat = ""
    for n in nation:
        if n["Profile"]["Nationality"] == astronaut and n["Profile"]["Name"] == astronaut:
            if n["Lifetime Statistics"]["EVA duration"] > highest_EVA:
                highest_EVA = n["Lifetime Statistics"]["EVA duration"]
                nat = n["Profile"]["Name"]
    return nat
           

@app.route("/p2")
def render_page2():
 return render_template('page2.html')
 
 
 
@app.route("/p3")
def render_page3():
    
    return render_template('page3.html')
    
    

if __name__=="__main__":
    app.run(debug=False)