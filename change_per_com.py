
import psycopg2
from psycopg2 import Error
def CheckInputVar():
    handleid = input('Enter community\'s handle (like 12345678/11111):')
    comid= "select community_id from community2collection where " \
           "community_id IN (select resource_id from handle " \
           "where handle='" + handleid + "')"
    cursor.execute(comid)
    record = cursor.fetchall()
    rowCount = len(record)
    if rowCount == 0:
        print("There is no such community")
        exit()
    else:
        return handleid
def tableprepare():
    q = "delete from resourcepolicy where eperson_id IN (select uuid from eperson where email='andrie83@gmail.com')"
    cursor.execute(q)

def changepolicy(collection_id):
    s = "select uuid from item where owning_collection in" \
        " (select resource_id from handle where handle= \'" + collection_id + "\')"
    cursor.execute(s)
    rows = cursor.fetchall()
    count = 0
    cursor.execute("select uuid from epersongroup where name='Anonymous'")
    uuidAnonym = ''.join(cursor.fetchone())
    for row in rows:
        row = ''.join(row)
        q5 = "delete from resourcepolicy where dspace_object=\'" + row + "\'"
        cursor.execute(q5)
        s1 = "Insert into resourcepolicy(policy_id, resource_type_id, epersongroup_id, action_id, dspace_object) " \
             "values(getnextid('resourcepolicy'),2,\'" + uuidAnonym + "\', 0,\'" + row + "\')"
        cursor.execute(s1)
        count = count + 1
        bundle = "select bundle_id from item2bundle where item_id=\'" + row + "\'"
        cursor.execute(bundle)
        bun=cursor.fetchall()
        for b in bun:
            b=''.join(b)
            q4 = "delete from resourcepolicy where dspace_object=\'" + b + "\'"
            cursor.execute(q4)
            q6 = "select bitstream_id from bundle2bitstream where bundle_id=\'" + b + "\'"
            cursor.execute(q6)
            bit=cursor.fetchall()
            for bb in bit:
                bb=''.join(bb)
                q8 = "delete from resourcepolicy where dspace_object=\'" + bb + "\'"
                cursor.execute(q8)
                s3 = "Insert into resourcepolicy(policy_id, resource_type_id, epersongroup_id, action_id, dspace_object)" \
                     " values(getnextid('resourcepolicy'),2,\'" + uuidAnonym + "\', 0,\'" + bb + "\')"
                cursor.execute(s3)
            q7 = "delete from resourcepolicy where dspace_object=\'" + b + "\'"
            cursor.execute(q7)
            s2 = "Insert into resourcepolicy(policy_id, resource_type_id, epersongroup_id, action_id, dspace_object)" \
                 " values(getnextid('resourcepolicy'),2,\'" + uuidAnonym + "\', 0,\'" + b + "\')"
            cursor.execute(s2)

    print("There were", count, "items changed")
try:

    connection = psycopg2.connect(user="dspace",
                                  password="password",
                                  host="localhost",
                                  port="5432",
                                  database="dspace")

    cursor = connection.cursor()
    print("Information about PostgreSQL")
    print(connection.get_dsn_parameters(), "\n")
#    tableprepare()
    q= "select collection_id from community2collection where community_id in " \
       "(select resource_id from handle where handle=\'" + CheckInputVar() + "\')"
    cursor.execute(q)
    rows = cursor.fetchall()
    for r in rows:
        r = ''.join(r)
        q1="select handle from handle where resource_id=\'"+ r +"\'"
        cursor.execute(q1)
        han = ''.join(cursor.fetchone())
        changepolicy(han)


except (Exception, Error) as error:
    print("Error PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.commit()
        connection.close()
        print("Connection PostgreSQL closed")

