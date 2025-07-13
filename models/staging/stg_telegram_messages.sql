with raw as (
    select * from raw.telegram_messages
)

select
    id as message_id,
    channel,
    date::timestamp as message_date,
    sender_id,
    message,
    has_media,
    length(message) as message_length
from raw
