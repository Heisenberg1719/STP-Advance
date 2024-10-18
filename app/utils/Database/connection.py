import logging
import mysql.connector
from http import HTTPStatus
from mysql.connector import pooling


db_config = { # from app.utilities.config import db_config
    "user": "doadmin",
    "password": "AVNS_CYyYGjtzj0JkrSG_010",
    "host": "sotruepay-do-user-17718491-0.m.db.ondigitalocean.com",
    "database": "STP_Advance","port": 25060}


class MySQLDatabase:
    # Setting up the MySQL connection pool using credentials from db_config
    pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,  # Adjust as per the expected load
        **db_config  # Pass db_config dictionary containing credentials and settings
    )

    @classmethod
    def get_connection(cls):
        try:
            return cls.pool.get_connection()
        except mysql.connector.Error as e:
            logging.error(f"Error while getting connection from pool: {e}")
            return None

    @classmethod
    def execute_query(cls, query, params=None):
        connection = cls.get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query, params)
                connection.commit()
                return {"message": "Query executed successfully", "status": HTTPStatus.OK}
            except mysql.connector.Error as e:
                logging.error(f"Error executing query: {e}")
                return {"message": f"Error executing query: {e}", "status": HTTPStatus.INTERNAL_SERVER_ERROR}
            finally:
                cursor.close()
                connection.close()  # Return the connection to the pool
        else:
            logging.error("Failed to connect to the database.")
            return {"message": "Failed to connect to the database", "status": HTTPStatus.SERVICE_UNAVAILABLE}

    @classmethod
    def fetch_results(cls, query, params=None):
        """
        Fetch results using parameterized queries to prevent SQL injection.
        """
        connection = cls.get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return {"data": results, "status": HTTPStatus.OK}
            except mysql.connector.Error as e:
                logging.error(f"Error fetching results: {e}")
                return {"message": f"Error fetching results: {e}", "status": HTTPStatus.INTERNAL_SERVER_ERROR}
            finally:
                cursor.close()
                connection.close()  # Return the connection to the pool
        else:
            logging.error("Failed to connect to the database.")
            return {"message": "Failed to connect to the database", "status": HTTPStatus.SERVICE_UNAVAILABLE}

    @classmethod
    def execute_stored_procedure(cls, procedure_name, params=None):
        connection = cls.get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc(procedure_name, params)
                results = []
                for result in cursor.stored_results():
                    results.append(result.fetchall())
                connection.commit()
                return {"message": "Stored procedure executed successfully", "data": results, "status": HTTPStatus.OK}
            except mysql.connector.Error as e:
                logging.error(f"Error executing stored procedure: {e}")
                return {"message": f"Error executing stored procedure: {e}", "status": HTTPStatus.INTERNAL_SERVER_ERROR}
            finally:
                cursor.close()
                connection.close()  # Return the connection to the pool
        else:
            logging.error("Failed to connect to the database.")
            return {"message": "Failed to connect to the database", "status": HTTPStatus.SERVICE_UNAVAILABLE}
