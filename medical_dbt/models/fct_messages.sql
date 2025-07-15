
with base as (
    select
        msg.message_id,
        msg.sender_id,
        msg.message_text,
        msg.has_photo,
        msg.channel,
        msg.message_date::date as post_date  -- ✅ Renamed alias
    from {{ ref('stg_telegram_messages') }} msg
),

joined as (
    select
        base.message_id,
        base.sender_id,
        base.message_text,
        base.has_photo,
        dc.channel_id,
        dd.date_id,
        base.post_date,  -- ✅ Include it in select
        length(base.message_text) as message_length
    from base
    left join {{ ref('dim_channels') }} dc on base.channel = dc.channel
    left join {{ ref('dim_dates') }} dd on base.post_date = dd.date  -- ✅ Use updated alias
)

select * from joined
