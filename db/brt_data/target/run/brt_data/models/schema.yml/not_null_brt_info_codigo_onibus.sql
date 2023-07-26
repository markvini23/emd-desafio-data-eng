select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select codigo_onibus
from "brt-gps"."raw"."brt_info"
where codigo_onibus is null



      
    ) dbt_internal_test