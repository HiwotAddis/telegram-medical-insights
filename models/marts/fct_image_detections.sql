with detections as (
    select
        message_id,
        object_class,
        confidence_score
    from raw.image_detections
),

messages as (
    select message_id from {{ ref('fct_messages') }}
)

select
    d.message_id,
    d.object_class,
    d.confidence_score
from detections d
join messages m on d.message_id = m.message_id
