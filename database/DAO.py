from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAnni():
            conn = DBConnect.get_connection()

            result = []

            cursor = conn.cursor(dictionary=True)
            query = """select distinct `year` 
                        from teams t 
                        where t.`year` >= 1980"""

            cursor.execute(query)

            for row in cursor:
                result.append(row['year'])

            cursor.close()
            conn.close()
            return result

    @staticmethod
    def getSquadreAnno(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.name , t.teamCode , sum(s.salary ) as StipendioTotale
from salaries s , teams t , appearances a 
where s.`year` = t.`year` and t.`year` = a.`year` and a.`year` = %s and t.ID = a.teamID and a.playerID = s.playerID 
group by t.ID , t.teamCode
"""

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append((row['teamCode'], row['name'], row['StipendioTotale']))

        cursor.close()
        conn.close()
        return result
