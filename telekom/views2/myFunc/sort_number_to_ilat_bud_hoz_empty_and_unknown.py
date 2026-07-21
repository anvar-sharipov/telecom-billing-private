
# from datetime import date
# import datetime
# import math
# import time
# import os
import sqlite3

# {hozUsers: [numberEtrap, numberEtrap], budUsers: [numberEtrap, numberEtrap]}
def sort_number_to_ilat_bud_hoz_empty_and_unknown(*args):

    if 'Dashoguz' in args:
        my_dict = {}
        myConn = sqlite3.connect(r'C:\Apache24\\htdocs\Dashoguz_telekom\db.sqlite3')
        myCur = myConn.cursor()
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'H' AND telekom_usertable.etrap = 'Dashoguz';
        """)
        hozUsersList = myCur.fetchall()
        hozUsers = []
        for user in hozUsersList:
            hozUsers.append(f"{user[0]}{user[1]}")

        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'B' AND telekom_usertable.etrap = 'Dashoguz';
        """)
        budUsersList = myCur.fetchall()
        budUsers = []
        for user in budUsersList:
            budUsers.append(f"{user[0]}{user[1]}")

        myCur.execute("""
                SELECT number, etrap
                FROM telekom_usertable
                WHERE telekom_usertable.etrap = 'Dashoguz' AND telekom_usertable.is_enterprises AND telekom_usertable.hb_id IS NULL;
            """)
        UnknownEdaraList = myCur.fetchall()
        UnknowEdaraUsers = []
        for user in UnknownEdaraList:
            UnknowEdaraUsers.append(f"{user[0]}{user[1]}")

        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Dashoguz' AND telekom_usertable.name = '' AND telekom_usertable.surname = '';""")
        emptyIlatList = myCur.fetchall()
        emptyNumberUsers = []
        for user in emptyIlatList:
            emptyNumberUsers.append(f"{user[0]}{user[1]}")
        my_dict['hozUsers'] = hozUsers
        my_dict['budUsers'] = budUsers
        my_dict['UnknowEdaraUsers'] = UnknowEdaraUsers
        my_dict['emptyNumberUsers'] = emptyNumberUsers

    if 'Boldumsaz' in args:
        # Boldumsaz
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'H' AND telekom_usertable.etrap = 'Boldumsaz';
        """)
        hozUsersListBoldumsaz = myCur.fetchall()
        hozUsersBoldumsaz = []
        for user in hozUsersListBoldumsaz:
            hozUsersBoldumsaz.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'B' AND telekom_usertable.etrap = 'Boldumsaz'
        """)
        budUsersListBoldumsaz = myCur.fetchall()
        budUsersBoldumsaz = []
        for user in budUsersListBoldumsaz:
            budUsersBoldumsaz.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Boldumsaz' AND telekom_usertable.is_enterprises AND telekom_usertable.hb_id IS NULL;""")
        UnknownEdaraListBoldumsaz = myCur.fetchall()
        UnknowEdaraUsersBoldumsaz = []
        for user in UnknownEdaraListBoldumsaz:
            UnknowEdaraUsersBoldumsaz.append(f"{user[0]}{user[1]}")

        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Boldumsaz' AND telekom_usertable.name = '' AND telekom_usertable.surname = '';""")
        emptyIlatListBoldumsaz = myCur.fetchall()
        emptyNumberUsersBoldumsaz = []
        for user in emptyIlatListBoldumsaz:
            emptyNumberUsersBoldumsaz.append(f"{user[0]}{user[1]}")
        my_dict['hozUsersBoldumsaz'] = hozUsersBoldumsaz
        my_dict['budUsersBoldumsaz'] = budUsersBoldumsaz
        my_dict['UnknowEdaraUsersBoldumsaz'] = UnknowEdaraUsersBoldumsaz
        my_dict['emptyNumberUsersBoldumsaz'] = emptyNumberUsersBoldumsaz

    if 'Turkmenbashy' in args:
        # Turkmenbashy
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'H' AND telekom_usertable.etrap = 'Turkmenbashy'""")

        hozUsersListTurkmenbashy = myCur.fetchall()
        hozUsersTurkmenbashy = []
        for user in hozUsersListTurkmenbashy:
            hozUsersTurkmenbashy.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'B' AND telekom_usertable.etrap = 'Turkmenbashy'""")
        budUsersListTurkmenbashy = myCur.fetchall()
        budUsersTurkmenbashy = []
        for user in budUsersListTurkmenbashy:
            budUsersTurkmenbashy.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Turkmenbashy' AND telekom_usertable.is_enterprises AND telekom_usertable.hb_id IS NULL;""")
        UnknownEdaraListTurkmenbashy = myCur.fetchall()
        UnknowEdaraUsersTurkmenbashy = []
        for user in UnknownEdaraListTurkmenbashy:
            UnknowEdaraUsersTurkmenbashy.append(f"{user[0]}{user[1]}")

        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Turkmenbashy' AND telekom_usertable.name = '' AND telekom_usertable.surname = '';""")
        emptyIlatListTurkmenbashy = myCur.fetchall()
        emptyNumberUsersTurkmenbashy = []
        for user in emptyIlatListTurkmenbashy:
            emptyNumberUsersTurkmenbashy.append(f"{user[0]}{user[1]}")
        my_dict['hozUsersTurkmenbashy'] = hozUsersTurkmenbashy
        my_dict['budUsersTurkmenbashy'] = budUsersTurkmenbashy
        my_dict['UnknowEdaraUsersTurkmenbashy'] = UnknowEdaraUsersTurkmenbashy
        my_dict['emptyNumberUsersTurkmenbashy'] = emptyNumberUsersTurkmenbashy

    if 'Gorogly' in args:
        # Gorogly
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'H' AND telekom_usertable.etrap = 'Gorogly'
        """)
        hozUsersListGorogly = myCur.fetchall()
        hozUsersGorogly = []
        for user in hozUsersListGorogly:
            hozUsersGorogly.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'B' AND telekom_usertable.etrap = 'Gorogly'
        """)
        budUsersListGorogly = myCur.fetchall()
        budUsersGorogly = []
        for user in budUsersListGorogly:
            budUsersGorogly.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Gorogly' AND telekom_usertable.is_enterprises AND telekom_usertable.hb_id IS NULL;""")
        UnknownEdaraListGorogly = myCur.fetchall()
        UnknowEdaraUsersGorogly = []
        for user in UnknownEdaraListGorogly:
            UnknowEdaraUsersGorogly.append(f"{user[0]}{user[1]}")

        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Gorgly' AND telekom_usertable.name = '' AND telekom_usertable.surname = '';""")
        emptyIlatListGorogly = myCur.fetchall()
        emptyNumberUsersGorogly = []
        for user in emptyIlatListGorogly:
            emptyNumberUsersGorogly.append(f"{user[0]}{user[1]}")
        my_dict['hozUsersGorogly'] = hozUsersGorogly
        my_dict['budUsersGorogly'] = budUsersGorogly
        my_dict['UnknowEdaraUsersGorogly'] = UnknowEdaraUsersGorogly
        my_dict['emptyNumberUsersGorogly'] = emptyNumberUsersGorogly

    if 'Koneurgench' in args:
        # Koneurgench
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'H' AND telekom_usertable.etrap = 'Koneurgench'
        """)
        hozUsersListKoneurgench = myCur.fetchall()
        hozUsersKoneurgench = []
        for user in hozUsersListKoneurgench:
            hozUsersKoneurgench.append(f"{user[0]}{user[1]}")

        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'B' AND telekom_usertable.etrap = 'Koneurgench'
        """)
        budUsersListKoneurgench = myCur.fetchall()
        budUsersKoneurgench = []
        for user in budUsersListKoneurgench:
            budUsersKoneurgench.append(f"{user[0]}{user[1]}")

        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Koneurgench' AND telekom_usertable.is_enterprises AND telekom_usertable.hb_id IS NULL;""")
        UnknownEdaraListKoneurgench = myCur.fetchall()
        UnknowEdaraUsersKoneurgench = []
        for user in UnknownEdaraListKoneurgench:
            UnknowEdaraUsersKoneurgench.append(f"{user[0]}{user[1]}")

        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Koneurgench' AND telekom_usertable.name = '' AND telekom_usertable.surname = '';""")
        emptyIlatListKoneurgench = myCur.fetchall()
        emptyNumberUsersKoneurgench = []
        for user in emptyIlatListKoneurgench:
            emptyNumberUsersKoneurgench.append(f"{user[0]}{user[1]}")
        my_dict['hozUsersKoneurgench'] = hozUsersKoneurgench
        my_dict['budUsersKoneurgench'] = budUsersKoneurgench
        my_dict['UnknowEdaraUsersKoneurgench'] = UnknowEdaraUsersKoneurgench
        my_dict['emptyNumberUsersKoneurgench'] = emptyNumberUsersKoneurgench

    if 'Ruhubelent' in args:
        # Ruhubelent
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'H' AND telekom_usertable.etrap = 'Ruhubelent'
        """)
        hozUsersListRuhubelent = myCur.fetchall()

        hozUsersRuhubelent = []
        for user in hozUsersListRuhubelent:
            hozUsersRuhubelent.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'B' AND telekom_usertable.etrap = 'Ruhubelent'
        """)
        budUsersListRuhubelent = myCur.fetchall()
        budUsersRuhubelent = []
        for user in budUsersListRuhubelent:
            budUsersRuhubelent.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Ruhubelent' AND telekom_usertable.is_enterprises AND telekom_usertable.hb_id IS NULL;""")
        UnknownEdaraListRuhubelent = myCur.fetchall()
        UnknowEdaraUsersRuhubelent = []
        for user in UnknownEdaraListRuhubelent:
            UnknowEdaraUsersRuhubelent.append(f"{user[0]}{user[1]}")

        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Ruhubelent' AND telekom_usertable.name = '' AND telekom_usertable.surname = '';""")
        emptyIlatListRuhubelent = myCur.fetchall()
        emptyNumberUsersRuhubelent = []
        for user in emptyIlatListRuhubelent:
            emptyNumberUsersRuhubelent.append(f"{user[0]}{user[1]}")
        my_dict['hozUsersRuhubelent'] = hozUsersRuhubelent
        my_dict['budUsersRuhubelent'] = budUsersRuhubelent
        my_dict['UnknowEdaraUsersRuhubelent'] = UnknowEdaraUsersRuhubelent
        my_dict['emptyNumberUsersRuhubelent'] = emptyNumberUsersRuhubelent

    if 'Akdepe' in args:
        # Akdepe
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'H' AND telekom_usertable.etrap = 'Akdepe'
        """)
        hozUsersListAkdepe = myCur.fetchall()

        hozUsersAkdepe = []
        for user in hozUsersListAkdepe:
            hozUsersAkdepe.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'B' AND telekom_usertable.etrap = 'Akdepe'
        """)
        budUsersListAkdepe = myCur.fetchall()
        budUsersAkdepe = []
        for user in budUsersListAkdepe:
            budUsersAkdepe.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Akdepe' AND telekom_usertable.is_enterprises AND telekom_usertable.hb_id IS NULL;""")
        UnknownEdaraListAkdepe = myCur.fetchall()
        UnknowEdaraUsersAkdepe = []
        for user in UnknownEdaraListAkdepe:
            UnknowEdaraUsersAkdepe.append(f"{user[0]}{user[1]}")

        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'Akdepe' AND telekom_usertable.name = '' AND telekom_usertable.surname = '';""")
        emptyIlatListAkdepe = myCur.fetchall()
        emptyNumberUsersAkdepe = []
        for user in emptyIlatListAkdepe:
            emptyNumberUsersAkdepe.append(f"{user[0]}{user[1]}")
        my_dict['hozUsersAkdepe'] = hozUsersAkdepe
        my_dict['budUsersAkdepe'] = budUsersAkdepe
        my_dict['UnknowEdaraUsersAkdepe'] = UnknowEdaraUsersAkdepe
        my_dict['emptyNumberUsersAkdepe'] = emptyNumberUsersAkdepe

    if 'S.A.Nyyazow' in args:
        # S.A.Nyyazow
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'H' AND telekom_usertable.etrap = 'S.A.Nyyazow'
        """)
        hozUsersListNyyazow = myCur.fetchall()

        hozUsersNyyazow = []
        for user in hozUsersListNyyazow:
            hozUsersNyyazow.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            INNER JOIN telekom_hozorbudjet ON hb_id = telekom_hozorbudjet.id
            WHERE telekom_hozorbudjet.name = 'B' AND telekom_usertable.etrap = 'S.A.Nyyazow'
        """)

        budUsersListNyyazow = myCur.fetchall()
        budUsersNyyazow = []
        for user in budUsersListNyyazow:
            budUsersNyyazow.append(f"{user[0]}{user[1]}")
        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'S.A.Nyyazow' AND telekom_usertable.is_enterprises AND telekom_usertable.hb_id IS NULL;""")
        UnknownEdaraListNyyazow = myCur.fetchall()
        UnknowEdaraUsersNyyazow = []
        for user in UnknownEdaraListNyyazow:
            UnknowEdaraUsersNyyazow.append(f"{user[0]}{user[1]}")

        myCur.execute("""
            SELECT number, etrap
            FROM telekom_usertable
            WHERE telekom_usertable.etrap = 'S.A.Nyyazow' AND telekom_usertable.name = '' AND telekom_usertable.surname = '';""")
        emptyIlatListNyyazow = myCur.fetchall()
        emptyNumberUsersNyyazow = []
        for user in emptyIlatListNyyazow:
            emptyNumberUsersNyyazow.append(f"{user[0]}{user[1]}")
        
        my_dict['hozUsersNyyazow'] = hozUsersNyyazow
        my_dict['budUsersNyyazow'] = budUsersNyyazow
        my_dict['UnknowEdaraUsersNyyazow'] = UnknowEdaraUsersNyyazow
        my_dict['emptyNumberUsersNyyazow'] = emptyNumberUsersNyyazow


    return my_dict