
  
    

  create  table "brt-gps"."raw"."brt_info__dbt_tmp"
  as (
    

SELECT codigo_onibus,
       latitude,
       longitude,
       velocidade
from raw.tb_brt_gps
  );
  