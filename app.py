from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
import random
import fun
import pymysql

app = Flask(__name__)

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

PSW = "***************"

@app.route('/')
def index():
    return render_template('index.html',
            page_title="AFA Virtual Leaderboard",)

@app.route('/submitResult/', methods=['GET', 'POST'])
def submit_result():
    conn = pymysql.connect(
                host="apexleaderboard.mysql.pythonanywhere-services.com",
                user="apexleaderboard",
                password="DBVirtualLeaderBoardDB",
                database="apexleaderboard$leaderboard"
            )
    if request.method == 'POST':
        result_inserted = False
        try:
            password = request.form.get('password-ts')
            if password != PSW:
                activeFencers = fun.get_all_active_fencers(conn)
                return render_template('submitResult.html',
                        flashedMessage = "Wrong password; result not submitted.",
                        result_inserted = 'Failure',
                        page_title="Result Submission",
                        activeFencers = activeFencers)
            fencer_id = int(request.form.get('nameForm'))
            tournament_name = request.form.get('tournamentName')
            tournament_type = request.form.get('tournamentType')
            tournament_year = request.form.get('tournamentDate')
            tournament_date = tournament_year + "-00-00"
            fencer_place = int(request.form.get('placement'))
            num_competitors = int(request.form.get('numCompetitors'))
            division = request.form.get('division')
            weapon = request.form.get('weaponType')
            ev = request.form.get('eventType')
            event_type = ev
            if division == "Women":
                event_type += "W"
            else:
                event_type += "M"
            if weapon == "Foil":
                event_type += "F"
            else:
                event_type += "E"
            result_inserted = fun.insert_tournament_result(conn, fencer_id, tournament_name,
                tournament_type, tournament_date, event_type, fencer_place,
                num_competitors)
        except Exception as err:
            print(err)
        return render_template('index.html',
            page_title="AFA Virtual Leaderboard",
            result_inserted = result_inserted,
            flashedMessage = "Tournament result was successfully submitted!")
    else: #get
        activeFencers = fun.get_all_active_fencers(conn)
        return render_template('submitResult.html', page_title="Result Submission",
                        activeFencers = activeFencers)

@app.route('/specificEvent/<eventCode>', methods= ['GET', 'POST'])
def specificEvent(eventCode):
    events = {'D1WE': "D1 Women's Epee", 'D1AWE': "D1A Women's Epee", 'D2WE': "D2 Women's Epee",
              'D3WE': "D3 Women's Epee", 'JNRWE': "Junior Women's Epee", 'CDTWE': "Cadet Women's Epee",
              'Y14WE': "Y14 Women's Epee", 'Y12WE': "Y12 Women's Epee", 'Y10WE': "Y10 Women's Epee",
              'V40WE': "VET40 Women's Epee", 'V50WE': "VET50 Women's Epee", 'VETCOWE': "VETCO Women's Epee",
              'D1WF': "D1 Women's Foil", 'D1AWF': "D1A Women's Foil", 'D2WF': "D2 Women's Foil",
              'D3WF': "D3 Women's Foil", 'JNRWF': "Junior Women's Foil", 'CDTWF': "Cadet Women's Foil",
              'Y14WF': "Y14 Women's Foil", 'Y12WF': "Y12 Women's Foil", 'Y10WF': "Y10 Women's Foil",
              'V40WF': "VET40 Women's Foil", 'V50WF': "VET50 Women's Foil", 'VETCOWF': "VETCO Women's Foil",
              'D1ME': "D1 Men's Epee", 'D1AME': "D1A Men's Epee", 'D2ME': "D2 Men's Epee",
              'D3ME': "D3 Men's Epee", 'JNRME': "Junior Men's Epee", 'CDTME': "Cadet Men's Epee",
              'Y14ME': "Y14 Men's Epee", 'Y12ME': "Y12 Men's Epee", 'Y10ME': "Y10 Men's Epee",
              'V40ME': "VET40 Men's Epee", 'V50ME': "VET50 Men's Epee", 'VETCOME': "VETCO Men's Epee",
              'D1MF': "D1 Men's Foil", 'D1AMF': "D1A Men's Foil", 'D2MF': "D2 Men's Foil",
              'D3MF': "D3 Men's Foil", 'JNRMF': "Junior Men's Foil", 'CDTMF': "Cadet Men's Foil",
              'Y14MF': "Y14 Men's Foil", 'Y12MF': "Y12 Men's Foil", 'Y10MF': "Y10 Men's Foil",
              'V40MF': "V40 Men's Foil", 'V50MF': "VET50 Men's Foil", 'VETCOMF': "VETCO Men's Foil",
              }
    eventName = events[eventCode]
    conn = pymysql.connect(
                host="****************",
                user="****************",
                password="****************",
                database="****************",
            )
    topThree = True
    allTypes = fun.get_top_three_fencers(conn, eventCode)
    forNational = allTypes["National"]
    forRegional = allTypes["Regional"]
    if request.method == "POST":
        topOrAll = request.form.get('topOrAll')
        # print("topOrAll:", topOrAll)
        if topOrAll == "View All Results":
            topThree = False
            allTypes = fun.get_all_fencers(conn, eventCode)
            forNational = allTypes["National"]
            forRegional = allTypes["Regional"]
        elif topOrAll == "View Personal Bests":
            topThree = True
            allTypes = fun.get_top_three_fencers(conn, eventCode)
            forNational = allTypes["National"]
            forRegional = allTypes["Regional"]
    topOrAll_title = "(Personal Bests)" if topThree else "(All Results)"
    return render_template('event.html',
            page_title="AFA Virtual Leaderboard",
            eventName = eventName, forNational=forNational,
            forRegional = forRegional,
            topThree = topThree,
            topOrAll_title = topOrAll_title)

@app.route('/addFencer/', methods=['GET', 'POST'])
def addFencer():
    if request.method == "GET":
        return render_template("addFencer.html", page_title="Adding new fencer")
    else:
        password = request.form.get('password-ts')
        if password != PSW:
            return render_template('addFencer.html',
                    flashedMessage = "Wrong password; fencer not added to database.",
                    result_inserted = 'Failure',
                    page_title="Adding new fencer")
        result_inserted = False
        try:
            conn = pymysql.connect(
                host="****************",
                user="****************",
                password="****************",
                database="****************"
            )
            firstName = request.form.get("firstName")
            middleName = request.form.get("middleName")
            lastName = request.form.get("lastName")
            fencingID = int(request.form.get("fencingID"))
            isAC = request.form.get("isActiveCompeting")
            active = 1
            if isAC == "No":
                active = 0
            result_inserted = fun.insert_fencer(conn, fencingID, firstName, middleName,
                lastName, active)
            activeFencers = fun.get_all_active_fencers(conn)
            if result_inserted != True:
                flashedMessage = result_inserted
                return render_template('submitResult.html',
                    page_title="AFA Virtual Leaderboard",
                    flashedMessage = flashedMessage,
                    result_inserted = result_inserted,
                    activeFencers = activeFencers)
        except Exception as err:
            print("Cannot insert new fencer. Error:", err)
        return render_template('submitResult.html',
            page_title="AFA Virtual Leaderboard",
            result_inserted = result_inserted,
            flashedMessage = "New fencer has been inserted into database!",
            activeFencers = activeFencers)


if __name__ == '__main__':
    app.debug = True
    app.run()