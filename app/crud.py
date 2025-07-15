from .database import get_connection

def get_top_products(limit=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT object_class AS product, COUNT(*) AS count
        FROM mart.fct_image_detections
        GROUP BY object_class
        ORDER BY count DESC
        LIMIT %s
    """, (limit,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [{"product": row[0], "count": row[1]} for row in results]

def get_channel_activity(channel):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT channel_name, date_day::text, COUNT(*) AS message_count
        FROM mart.fct_messages
        WHERE channel_name = %s
        GROUP BY channel_name, date_day
        ORDER BY date_day
    """, (channel,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [{"channel": row[0], "date": row[1], "message_count": row[2]} for row in results]

def search_messages(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT message_id, message, message_date::text, channel_name
        FROM mart.fct_messages
        WHERE LOWER(message) LIKE %s
        ORDER BY message_date DESC
        LIMIT 50
    """, ('%' + query.lower() + '%',))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [{
        "message_id": row[0],
        "message": row[1],
        "date": row[2],
        "channel": row[3]
    } for row in results]
