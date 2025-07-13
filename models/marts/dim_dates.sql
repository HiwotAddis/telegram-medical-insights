select distinct
    date_trunc('day', message_date) as date_day
from {{ ref('stg_telegram_messages') }}
