CREATE OR REPLACE FUNCTION nux_notify_table_change()
RETURNS TRIGGER AS $$
DECLARE
    payload TEXT;
    channel_name TEXT;
BEGIN
    -- Construct the channel name to include the table name
    channel_name := TG_TABLE_NAME || '_changes';
    
    -- Convert the NEW row to JSON and store it in a TEXT variable
    payload := row_to_json(NEW)::text;
    
    -- Use the pg_notify function to send the notification with the dynamic payload
    -- and a channel name that includes the table name
    PERFORM pg_notify(channel_name, payload);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER table_change_trigger
AFTER INSERT OR UPDATE OR DELETE ON ethan_test
FOR EACH ROW EXECUTE FUNCTION notify_table_change();
