import mysql.connector


def get_connection():
    return mysql.connector.connect(user='root',
                                   password='Yourface1234',
                                   host='127.0.0.1',
                                   database='imdb_solo_project')


# Does the given operation to the database
def perform_operation_on_db(op):
    cnx = get_connection()

    cursor = cnx.cursor()

    try:
        cursor.execute(op)
        cnx.commit()
        cnx.close()
    except mysql.connector.Error as err:
        print("Could not perform the given operation:\n"
              "%s" % op)
        print(err.msg)
        exit(1)


# adds the given director of the given episode to the database.
def add_person_to_database(p):
    # The IGNORE is there so that the same person won't be inserted twice.
    add_person = "INSERT IGNORE INTO person (person_id, person_name"

    person_id = "\"" + p.personID + "\""

    person_name = "\"" + p['name'] + "\""

    # only include the birthdate if IMDb has one listed
    if p.get('birth date') is None:
        add_person += ") VALUES (%s, %s)"
        person_results = add_person % (person_id, person_name)
    else:
        add_person += ", person_birthdate) VALUES (%s, %s, '%s')"
        person_results = add_person % (person_id, person_name, p.get('birth date'))

    perform_operation_on_db(person_results)

    print("Added person %s to the database" % person_name)