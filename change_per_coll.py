import psycopg2
from psycopg2 import Error
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
    handleid = input('Enter collection\'s handle (like 12345678/11111):')
    changepolicy(handleid)
except (Exception, Error) as error:
    print("Error PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.commit()
        connection.close()
        print("Connection PostgreSQL closed")


