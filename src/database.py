import psycopg2

from .exceptions import ServerError


class Database:
    def __init__(self, app):
        self.config = app.config
        self.logger = app.logger
        self.connection = None

    def get_mediafile(self, id):
        """ Returns data, mimetype """
        while True:
            connection = self.get_connection()
            try:
                with connection:
                    with connection.cursor() as cur:
                        table = self.config["DATABASE_TABLE"]
                        cur.execute(
                            f"SELECT data, mimetype FROM {table} WHERE id=%s",
                            [id],
                        )
                        row = cur.fetchone()
                        if not row:
                            raise ServerError(
                                f"The mediafile with id {id} could not be found."
                            )
                        return (row[0], row[1])
            except psycopg2.InterfaceError:
                self.connection = None
                self.logger.info("Database connection has been reset. Reconnect...")
            except psycopg2.Error as e:
                self.logger.error(f"Error during retrieving a mediafile: {repr(e)}")
                raise ServerError(f"Database error {e.pgcode}: {e.pgerror}")

    def get_connection(self):
        if not self.connection:
            self.connection = self.create_connection()
        return self.connection

    def create_connection(self):
        try:
            return psycopg2.connect(
                host=self.config["DATABASE_HOST"],
                port=self.config["DATABASE_PORT"],
                database=self.config["DATABASE_NAME"],
                user=self.config["DATABASE_USER"],
                password=self.config["DATABASE_PASSWORD"],
            )
        except psycopg2.Error as e:
            self.logger.error(f"Error during connect to the database: {repr(e)}")
            raise ServerError(f"Database connect error {e.pgcode}: {e.pgerror}")

    def shutdown(self):
        if self.connection:
            self.connection.close()
