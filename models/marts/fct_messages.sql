select
    message_id,
    channel as channel_name,
    date_trunc('day', message_date) as date_day,
    sender_id,
    has_media,
    message_length
from {{ ref('stg_telegram_messages') }}
