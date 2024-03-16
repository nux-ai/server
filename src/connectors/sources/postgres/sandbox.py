import asyncio
import websockets
import psycopg2
import json

# Your provided connection details
HOST = "aws-0-us-east-1.pooler.supabase.com"
DATABASE_NAME = "postgres"
PORT = 5432  # Default PostgreSQL port, change if necessary
USER = ""
PASSWORD = ""

# Create a replication connection
conn = psycopg2.connect(
    dbname=DATABASE_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
)


def notify_client():
    # Connect to your PostgreSQL database
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Listen for notifications on a specific channel
    cur.execute("LISTEN documents;")

    print("Waiting for notifications on channel 'documents'")
    try:
        while True:
            # If there is new data available from the LISTEN command, fetch it
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                payload = notify.payload

                # Send the notification payload to the WebSocket client)

                print("Sent notification to WebSocket client:", payload)
    finally:
        # Cleanup: close the cursor and connection
        cur.close()
        conn.close()


notify_client()

# # Start the WebSocket server
# start_server = websockets.serve(notify_client, "localhost", 6789)

# # Run the server indefinitely
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

# import psycopg2
# import psycopg2.extras
# import select

# # Your updated connection details
# conn_info = "user=postgres.ajbmxtlpktvtcbtxxikl password=qQbj2eAbTXHAfzOQ host=aws-0-us-east-1.pooler.supabase.com port=5432 dbname=postgres"

# # Connect using a replication connection
# conn = psycopg2.connect(
#     conn_info, connection_factory=psycopg2.extras.LogicalReplicationConnection
# )
# conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

# # Obtain a replication cursor
# cur = conn.cursor()

# # Assuming the replication slot 'test_slot' and publication 'test_pub' have been created beforehand
# options = {"publication_names": "test_pub", "proto_version": "1"}


# # Define a callback function to process and acknowledge messages
# def consume_message(msg):
#     print("Received message:", msg.payload)
#     # Send feedback to PostgreSQL acknowledging the WAL data has been received
#     msg.cursor.send_feedback(flush_lsn=msg.data_start)


# try:
#     # Start the replication with the specified slot and options
#     cur.start_replication(slot_name="test_slot", options=options, decode=True)
#     # Process incoming messages with the consume_message callback
#     cur.consume_stream(consume_message)
# except KeyboardInterrupt:
#     # Gracefully handle a keyboard interrupt to stop the replication
#     print("Replication stopped by user.")
# finally:
#     # Ensure resources are cleaned up properly
#     cur.close()
#     conn.close()

# Ensure your script remains active to listen for changes. This example will not terminate.


# import os
# import pypgoutput


# def start_replication_reader():
#     HOST = "aws-0-us-east-1.pooler.supabase.com"
#     DATABASE_NAME = "postgres"
#     PORT = 5432  # Default PostgreSQL port, change if necessary
#     USER = "postgres.ajbmxtlpktvtcbtxxikl"
#     PASSWORD = "qQbj2eAbTXHAfzOQ"
#     PUBLICATION_NAME = "test_pub"
#     SLOT_NAME = "test_slot"

#     cdc_reader = pypgoutput.LogicalReplicationReader(
#         publication_name=PUBLICATION_NAME,
#         slot_name=SLOT_NAME,
#         host=HOST,
#         database=DATABASE_NAME,
#         port=PORT,
#         user=USER,
#         password=PASSWORD,
#     )
#     try:
#         for message in cdc_reader:
#             print(message.json(indent=2))
#     finally:
#         cdc_reader.stop()


# if __name__ == "__main__":
#     start_replication_reader()


# # conn = psycopg2.connect(HOST, DATABASE_NAME, USER, PASSWORD)


# # try:
# #     # Import the pypgoutput package or module

# #     # Initialize the logical replication reader with the provided details
# #     cdc_reader = pypgoutput.LogicalReplicationReader(
# #         publication_name=PUBLICATION_NAME,
# #         slot_name=SLOT_NAME,
# #         host=HOST,
# #         database=DATABASE_NAME,
# #         port=PORT,
# #         user=USER,
# #         password=PASSWORD,
# #     )

# #     # Iterate over the messages from the logical replication slot
# #     for message in cdc_reader:
# #         print(message.json(indent=2))

# # except ImportError:
# #     print("The 'pypgoutput' package is not installed or not available.")
# # except Exception as e:
# # print(f"An error occurred: {e}")


# # # import psycopg2

# # # # Connection parameters
# # conn_params = {
# #     "dbname": "postgres",
# #     "user": "postgres.ajbmxtlpktvtcbtxxikl",
# #     "password": "qQbj2eAbTXHAfzOQ",
# #     "host": "aws-0-us-east-1.pooler.supabase.com",
# # }

# # psycopg2.connect(**conn_params)

# # try:
# #     # Establishing the connection
# #     conn = psycopg2.connect(**conn_params)
# #     conn.autocommit = True
# #     cur = conn.cursor()

# #     # Execute SQL to create a publication for all tables
# #     cur.execute("CREATE PUBLICATION test_pub FOR ALL TABLES;")

# #     # Execute SQL to create a logical replication slot
# #     cur.execute(
# #         "SELECT * FROM pg_create_logical_replication_slot('test_slot', 'pgoutput');"
# #     )

# #     print("Publication and logical replication slot created successfully.")

# # except Exception as e:
# #     print(f"An error occurred: {e}")
# # finally:
# #     # Clean up by closing the cursor and connection
# #     if cur is not None:
# #         cur.close()
# #     if conn is not None:
# #         conn.close()
