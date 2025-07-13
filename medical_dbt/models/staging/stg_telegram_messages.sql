
with source as (
    select * from {{ source('public', 'raw_telegram_messages') }}
),

renamed as (
    select
        message_id::bigint as message_id,
        date::timestamp as message_date,
        sender_id::text as sender_id,
        text::text as message_text,
        channel::text as channel,
        has_photo::boolean as has_photo
    from source
)

select * from renamed
