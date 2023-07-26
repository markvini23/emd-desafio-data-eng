CREATE SCHEMA raw;

CREATE TABLE raw.tb_brt_gps( codigo_onibus VARCHAR(20) NOT NULL,
 placa VARCHAR(10),
 linha SMALLINT,
 latitude FLOAT(10),
 longitude FLOAT(10),
 velocidade FLOAT(2),
 sentido VARCHAR(5),
 trajeto TEXT,
 hodometro FLOAT(10),
 dataPosicao DATE,
 horaPosicao TIME,
 dataHoraColeta TIMESTAMP);
