with alerts as (

    select * from {{ ref('alerts') }}

),

final as (

    select
      alert_id,
      fips_id

    from alerts

)

select * from final
