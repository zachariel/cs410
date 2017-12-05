#!/usr/bin/env python3

from pymysql import connect, err, sys, cursors


#cursor = conn.cursor( cursors.DictCursor )

majors = {}
def check_major(major):
    if not major in majors:
        majors[major] = []

def occupations(cursor):
    occupations = """SELECT
     occupation_data.title, occupation_data.description,
      SUBSTRING(occupation_data.onetsoc_code, 1, 2) as major
      FROM occupation_data
      """
    cursor.execute( occupations )

    data = cursor.fetchall()
    for row in data:
        major = row['major']
        check_major(major)

        majors[major].append( row['title'] )
        majors[major].append( row['description'] )


def reported_titles(cursor):
    query = """SELECT reported_job_title as title, SUBSTRING(onetsoc_code, 1, 2) as major FROM sample_of_reported_titles """
    cursor.execute( query )
    data = cursor.fetchall()
    for row in data:
        major = row['major']
        check_major(major)

        majors[major].append( row['title'] )

def alternate_titles(cursor):
    query = """SELECT alternate_title as title, SUBSTRING(onetsoc_code, 1, 2) as major FROM alternate_titles"""
    cursor.execute( query )
    data = cursor.fetchall()
    for row in data:
        major = row['major']
        check_major(major)

        majors[major].append( row['title'] )

def skills(cursor):
    query = """
    SELECT s.element_id, SUBSTRING(s.onetsoc_code, 1, 2) as major, `c`.`description`
    FROM skills s INNER JOIN content_model_reference c on s.element_id = c.element_id
    GROUP BY major, s.element_id;
    """

    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        major = row['major']
        check_major( major )
        majors[major].append( row['description'] )

def append_data(data, fields):
    for row in data:
        major = row['major']
        check_major( major )
        for field in fields:
            if not row[field] in majors[major]:
                majors[major].append( row[field] )


def abilities(cursor):
    query = """
    SELECT s.element_id, SUBSTRING(s.onetsoc_code, 1, 2) as major, `c`.`description`
    FROM abilities s INNER JOIN content_model_reference c on s.element_id = c.element_id
    GROUP BY major, s.element_id;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    append_data(data, ['description'])

def educations(cursor):
    query = """
    SELECT s.element_id, SUBSTRING(s.onetsoc_code, 1, 2) as major, `c`.`description`
    FROM education_training_experience s INNER JOIN content_model_reference c on s.element_id = c.element_id
    GROUP BY major, s.element_id;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    append_data(data, ['description'])

def tasks(cursor):
    query = """
    SELECT SUBSTRING(s.onetsoc_code, 1, 2) as major, task
    FROM emerging_tasks s;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    append_data(data, ['task'])

    query = """
    SELECT SUBSTRING(s.onetsoc_code, 1, 2) as major, dwa_title as title, description
    FROM tasks_to_dwas s LEFT JOIN dwa_reference d ON d.dwa_id = s.dwa_id LEFT JOIN content_model_reference c ON c.element_id =
    d.element_id;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    append_data(data, ['title', 'description'])

def knowledges(cursor):
    query = """
    SELECT s.element_id, SUBSTRING(s.onetsoc_code, 1, 2) as major, `c`.`description`
    FROM knowledge s INNER JOIN content_model_reference c on s.element_id = c.element_id
    GROUP BY major, s.element_id;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    append_data(data, ['description'])

def tools(cursor):
    query = """
    SELECT SUBSTRING(s.onetsoc_code, 1, 2) as major, s.t2_example as title
    FROM tools_and_technology s;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    append_data(data, ['title'])

def work_activities(cursor):
    query = """
    SELECT s.element_id, SUBSTRING(s.onetsoc_code, 1, 2) as major, `c`.`description`
    FROM work_activities s INNER JOIN content_model_reference c on s.element_id = c.element_id
    GROUP BY major, s.element_id;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    append_data(data, ['description'])

def work_styles(cursor):
    query = """
    SELECT s.element_id, SUBSTRING(s.onetsoc_code, 1, 2) as major, `c`.`description`
    FROM work_styles s INNER JOIN content_model_reference c on s.element_id = c.element_id
    GROUP BY major, s.element_id;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    append_data(data, ['description'])

def work_values(cursor):
    query = """
    SELECT s.element_id, SUBSTRING(s.onetsoc_code, 1, 2) as major, `c`.`description`
    FROM work_values s INNER JOIN content_model_reference c on s.element_id = c.element_id
    GROUP BY major, s.element_id;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    append_data(data, ['description'])


def main():
    try:
        with conn.cursor( cursors.DictCursor ) as cursor:
            occupations(cursor)
            reported_titles(cursor)
            alternate_titles(cursor)
            skills(cursor)
            abilities(cursor)
            #educations(cursor) #checkthis
            tasks(cursor)
            tools(cursor)
            knowledges(cursor)
            work_activities(cursor)
            work_styles(cursor)
            work_values(cursor)

    finally:
        conn.close()

    conn = connect( host='localhost', user='onet', passwd='onet_123', db="onet_22_1")
    for major, content in majors.items():
        with open("data/descriptions/major_" + major + ".txt" , "w") as f:
            try:
                f.write( " ".join(content) )
            except:
                print("Error: ", sys.exc_info()[0])

