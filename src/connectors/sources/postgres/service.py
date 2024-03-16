from fastapi import HTTPException
import asyncio
from threading import Thread, Event
import psycopg2
import logging
import time
from psycopg2 import sql

from .model import PostgresConnection


class PostgresService:
    def __init__(self, connection_info: PostgresConnection):
        self.dbname = connection_info.db
        self.user = connection_info.user
        self.password = connection_info.password
        self.host = connection_info.host
        self.port = connection_info.port
        self.listeners = {}  # Dictionary to track listener threads
        self.stop_events = {}  # Track stop events for each thread

    def connect_to_db(self):
        try:
            return psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                connect_timeout=3,
            )
        except psycopg2.OperationalError as e:
            # Handle the exception
            raise HTTPException(
                status_code=500, detail=f"Failed to connect to the database: {e}"
            )

    def create_notifier(self, table_name):
        # Ensure table_name is safe to insert into the SQL statement to prevent SQL injection
        # For example, by checking it against a list of known good table names
        # This is a basic check, adjust according to your context
        if not table_name.isidentifier():
            return "Invalid table name."

        function_sql = sql.SQL(
            """
            CREATE OR REPLACE FUNCTION nux_notify_function()
            RETURNS TRIGGER AS $$
            DECLARE
                payload TEXT;
                channel_name TEXT;
            BEGIN
                channel_name := TG_TABLE_NAME || '_changes';
                payload := row_to_json(NEW)::text;
                PERFORM pg_notify(channel_name, payload);
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER nux_notify_trigger
            AFTER INSERT ON {table}
            FOR EACH ROW EXECUTE FUNCTION nux_notify_function();
        """
        ).format(table=sql.Identifier(table_name))

        connection = self.connect_to_db()
        cursor = connection.cursor()

        try:
            cursor.execute(function_sql)
            connection.commit()
            return "Notification function and trigger created successfully for table: {}".format(
                table_name
            )
        except Exception as e:
            # It's usually a good idea to log the exception
            connection.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create notification function and trigger: {e}",
            )
        finally:
            self.close()

    def close(self):
        for table_name in list(self.listeners.keys()):
            self.stop_notifier(table_name)

        self.cursor.close()
        self.connection.close()

    # def stop_notifier(self, table_name):
    #     if table_name in self.listeners:
    #         logging.info(f"Stopping listener for {table_name}.")
    #         self.stop_events[table_name].set()  # Signal the thread to stop
    #         self.listeners[table_name].join()  # Wait for the thread to finish
    #         del self.listeners[table_name]  # Remove the thread from the registry
    #         del self.stop_events[table_name]  # Remove the event from the registry
    #     else:
    #         logging.warning(f"No active listener for {table_name} to stop.")

    def invoke_notifier(self, table_name):
        print(f"Invoking notifier for {table_name}")
        if table_name in self.listeners:
            return f"Listener already running for {table_name}."

        stop_event = Event()
        self.stop_events[table_name] = stop_event

        def listen_notifications():
            print(f"Starting listener for {table_name}.")
            conn = self.connect_to_db()
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute(f"LISTEN {table_name}_changes;")
            print(f"Listening for notifications on channel: {table_name}_changes.")
            try:
                while not stop_event.is_set():
                    conn.poll()
                    while conn.notifies:
                        notify = conn.notifies.pop(0)
                        payload = notify.payload
                        print(f"Received notification: {payload}")
                    time.sleep(1)
            finally:
                cur.close()
                conn.close()
                print(f"Stopped listener for {table_name}.")

        thread = Thread(target=listen_notifications, daemon=True)
        thread.start()
        self.listeners[table_name] = thread
