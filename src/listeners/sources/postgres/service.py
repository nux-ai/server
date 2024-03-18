from fastapi import HTTPException
import psycopg2
from psycopg2 import sql
from threading import Thread, Event
import time

from config import api_service_url

from .model import PostgresConnection
from utilities.transmit import Sender


class DatabaseManager:
    def __init__(self, connection_info: PostgresConnection):
        self.connection_info = connection_info

    def _connect_to_db(self):
        try:
            return psycopg2.connect(
                dbname=self.connection_info.db,
                user=self.connection_info.user,
                password=self.connection_info.password,
                host=self.connection_info.host,
                port=self.connection_info.port,
                connect_timeout=3,
            )
        except psycopg2.OperationalError as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to connect to the database: {e}"
            )

    def execute_sql(self, sql_statement, is_commit=False):
        conn = self._connect_to_db()
        cur = conn.cursor()
        try:
            cur.execute(sql_statement)
            if is_commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()


class NotificationManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.notifiers = {}

    def create_notification_trigger(self, table_name):
        if not table_name.isidentifier():
            raise ValueError("Invalid table name.")

        function_sql = sql.SQL(
            """
            CREATE OR REPLACE FUNCTION nux_notify_function()
            RETURNS TRIGGER AS $$
            BEGIN
                PERFORM pg_notify(TG_TABLE_NAME || '_changes', row_to_json(NEW)::text);
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'nux_notify_trigger') THEN
                    CREATE TRIGGER nux_notify_trigger
                    AFTER INSERT OR UPDATE OR DELETE ON {table}
                    FOR EACH ROW EXECUTE FUNCTION nux_notify_function();
                END IF;
            END
            $$;
        """
        ).format(table=sql.Identifier(table_name))

        self.db_manager.execute_sql(function_sql, is_commit=True)

    def start_notifier(self, table_name, sender):
        if table_name in self.notifiers:
            raise Exception(f"Notifier for {table_name} is already running.")

        notifier = Notifier(table_name, self.db_manager, sender)
        notifier.start()
        self.notifiers[table_name] = notifier

    def stop_notifier(self, table_name):
        if table_name in self.notifiers:
            self.notifiers[table_name].stop()
            del self.notifiers[table_name]
        else:
            print(f"No active notifier for {table_name} to stop.")


class Notifier:
    def __init__(self, table_name, db_manager: DatabaseManager, sender: Sender):
        self.table_name = table_name
        self.db_manager = db_manager
        self.sender = sender
        self.thread = None
        self.stop_event = Event()

    def _listen_notifications(self):
        conn = self.db_manager._connect_to_db()
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"LISTEN {self.table_name}_changes;")
        print(f"Listening for notifications on {self.table_name}_changes...")
        try:
            while not self.stop_event.is_set():
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    self.sender.send(notify.payload)
                time.sleep(1)
        except Exception as e:
            self.sender.send(f"Listener stopped: {e}")
        finally:
            cur.close()
            conn.close()

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = Thread(target=self._listen_notifications, daemon=True)
            self.thread.start()

    def stop(self):
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join()


class PostgresService:
    def __init__(self, connection_info: PostgresConnection):
        self.db_manager = DatabaseManager(connection_info)
        self.notification_manager = NotificationManager(self.db_manager)
        self.sender = Sender(
            endpoint=api_service_url + "/listeners/postgres",
            headers={"Authorization": f"Bearer {connection_info.nux_api_key}"},
        )

    def create_table(self, table_sql):
        pass
        # self.db_manager.execute_sql(table_sql, is_commit=True)
        # create table
        # document_elements (
        #     id character varying(255) not null default ('element_'::text || uuid_generate_v4 ()),
        #     text text not null,
        #     type varchar not null,
        #     metadata JSONB,
        #     file_id uuid not null,
        #     element_id varchar not null,
        #     embedding vector (1536)
        # );

    def setup_notifier_for_table(self, table_name):
        self.notification_manager.create_notification_trigger(table_name)
        self.notification_manager.start_notifier(table_name, self.sender)
