
create table  iis_log
(
    Id  int   identity  primary key ,
    log_file_name varchar(100), 
    beijing_time        datetime,
    str_date  varchar(32),
    str_time  varchar(32),
    s_ip      varchar(50),
    cs_method  varchar(100), 
    cs_uri_stem   varchar(1000), 
    cs_uri_query  varchar(1000),
    s_port        varchar(100),
    cs_username   varchar(100),
    c_ip          varchar(100), 
    cs_User_Agent varchar(200),
    cs_Refer      varchar(200),
    sc_status      varchar(50),
    sc_substatus   varchar(50), 
    sc_win32_status varchar(50), 
    time_taken      int ,
    operate_time    datetime default getdate()
)     
    
    