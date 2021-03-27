import pymysql

def insert_fencer(conn, fencer_id, first_name, middle_name,
                last_name, active):
    '''Inserts fencer info from student into database if not already in the database.
        If the fencer to be inserted is already in the database but their status is inactive,
        then we simply update their status to be active'''
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        # first check if fencer with that fencer id already exists
        curs.execute('''select * from fencer where fencer_id=%s''',
                    [fencer_id])
        exists = curs.fetchall()
        print("exists:", exists)
        if len(exists) > 0:
            # this fencer is already in the database, but inactive,
            # so we will update their status to be active
            aon = exists[0]['active']
            fencer_name = exists[0]["first_name"] + " " + exists[0]["middle_name"] + " " + exists[0]["last_name"]
            if aon == 0:
                fencer_idt = exists[0]['fencer_id']
                curs.execute('''update fencer
                                set active = 1
                                where fencer_id=%s''', [fencer_idt])
                conn.commit()
                return '''Fencer with the USA Fencing ID {} ({}) is now in the database.
                    Please select your name from the picklist or contact admin if you cannot find it.'''.format(
                        fencer_id, fencer_name)
            return '''Fencer with the USA Fencing ID {} ({}) is already in the database.
                    Please select your name from the picklist or contact admin.'''.format(
                        fencer_id, fencer_name)
        curs.execute('''insert into fencer (fencer_id, first_name,
                    middle_name, last_name, active)
                    values (%s,%s,%s,%s,%s)''',
                    [fencer_id,first_name, middle_name, last_name,
                    active])
        conn.commit()
        #returns True if successful, False otherwise
        return True
    except Exception as err:
        print("Cannot insert new fencer because:", err)
        return False

def get_all_active_fencers(conn):
    '''get all active/competing fencers sorted by their first name'''
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        curs.execute('''select fencer_id, first_name, middle_name,
                        last_name from fencer where active = 1
                        order by first_name''')
        fetched = curs.fetchall()
        #returns True if successful, False otherwise
        return fetched
    except Exception as err:
        print(err)
        return False

def insert_tournament_result(conn, fencer_id, tournament_name,
        tournament_type, tournament_date, event_type, fencer_place,
        num_competitors):
    '''inserting tournament result for the fencer whose id is
    fencer_id'''
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        rating_pctg = int(round(100*fencer_place/num_competitors))
        curs.execute('''insert into record (fencer_id, tournament_name,
                    tournament_type, tournament_date, event_type, fencer_place,
                    num_competitors, rating_pctg)
                    values (%s,%s,%s,%s,%s,%s,%s,%s)''',
                    [fencer_id, tournament_name, tournament_type,
                    tournament_date, event_type, fencer_place, num_competitors,
                    rating_pctg])
        conn.commit()
        #returns True if successful, False otherwise
        return True
    except Exception as err:
        print(err)
        return False

def get_top_three_fencers(conn, eventName):
    '''getting top three fencers in event (eventName) in
    (ttype) tournament'''
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        curs.execute(
        '''select r.fencer_id, f.first_name, f.middle_name,
		        f.last_name, r.rating_pctg, r.tournament_name, year(r.tournament_date) as tournament_date,
                r.fencer_place, r.num_competitors
            from record r
            join (select fencer_id, MIN(rating_pctg) rating_pctg from record
                    where tournament_type = 'National' and event_type= %s group by fencer_id) b
	            on b.fencer_id = r.fencer_id and b.rating_pctg = r.rating_pctg
            join fencer f on f.fencer_id = b.fencer_id
            where event_type = %s and tournament_type='National'
            group by r.fencer_id order by r.rating_pctg;''',
             [eventName, eventName])
        national = curs.fetchall()
        three = {}
        curs.execute(
        '''select r.fencer_id, f.first_name, f.middle_name,
		        f.last_name, r.rating_pctg, r.tournament_name, year(r.tournament_date) as tournament_date,
                r.fencer_place, r.num_competitors
            from record r
            join (select fencer_id, MIN(rating_pctg) rating_pctg from record
                    where tournament_type = 'Regional' and event_type= %s group by fencer_id) b
	            on b.fencer_id = r.fencer_id and b.rating_pctg = r.rating_pctg
            join fencer f on f.fencer_id = b.fencer_id
            where event_type = %s and tournament_type='Regional'
            group by r.fencer_id order by r.rating_pctg;''',
             [eventName, eventName])
        regional = curs.fetchall()
        three["National"] = national
        three["Regional"] = regional
        return three
    except Exception as err:
        print("Cannot get top three fencers for {}, because of {}".format(
            eventName, err))
        return False

def get_all_fencers(conn, eventName):
    '''getting top three fencers in event (eventName) in
    (ttype) tournament, sorted by percentage'''
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        curs.execute('''select r.fencer_id, f.first_name, f.middle_name,
            f.last_name, r.rating_pctg, r.tournament_name, year(r.tournament_date) as tournament_date,
            r.fencer_place, r.num_competitors, r.tournament_type
            from record r join
            fencer f using (fencer_id)
            where event_type=%s
            order by r.rating_pctg asc''',
             [eventName])
        allTypes = curs.fetchall()
        three = {}
        national = [i for i in allTypes if i["tournament_type"]=="National"]
        regional = [i for i in allTypes if i["tournament_type"]=="Regional"]
        three["National"] = national
        three["Regional"] = regional
        return three
    except Exception as err:
        print("Cannot get top all fencers for {}, because of {}".format(
            eventName, err))
        return False


if __name__ == "__main__":
    conn = pymysql.connect(
        host="****************",
                user="****************",
                password="****************",
                database="****************"
    )
    print(get_top_three_fencers(conn, "D1WE"))
    # insert_fencer(conn, 12345, "test", "", "testing", 1)