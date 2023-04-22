ALTER TABLE lianjia_nc ADD index houseID_index (house_id);
SHOW index from lianjia_nc; 
SELECT * FROM lianjia_nc WHERE 1=1
ALTER TABLE lianjia_nc ADD url VARCHAR(50);
update lianjia_nc as lj
set lj.url = concat("https://nc.lianjia.com/ershoufang/",
            convert((SELECT house_id
            from lianjia_nc as aa
            WHERE aa.house_id = lj.house_id),char),
            ".html") 
WHERE 1=1

UPDATE lianjia_nc f, lianjia_nc p
set f.url=concat("https://nc.lianjia.com/ershoufang/",
            convert(p.house_id,char),
            ".html") 
where f.house_id=p.house_id

 describe lianjia_nc;

 -- show index from	lianjia_nc

-- drop index houseID_index on lianjia_nc

alter table lianjia_nc modify column url varchar(100) DEFAULT NULL COMMENT '源地址';

SELECT `source`.`village_name` AS `小区名`, `source`.`district` AS `行政区`, `source`.`region` AS `地区`, `source`.`avg` AS `房价均值`, `source`.`count` AS `挂牌数`
FROM (SELECT `lianjia_nc`.`village_name` AS `village_name`, `lianjia_nc`.`district` AS `district`, `lianjia_nc`.`region` AS `region`, AVG(`lianjia_nc`.`unit_price`) AS `avg`, COUNT(*) AS `count` FROM `lianjia_nc`
GROUP BY `lianjia_nc`.`village_name`, `lianjia_nc`.`district`, `lianjia_nc`.`region`
ORDER BY `lianjia_nc`.`village_name` ASC, `lianjia_nc`.`district` ASC, `lianjia_nc`.`region` ASC) AS `source`
WHERE `source`.`count` > 8 ORDER BY `source`.`avg` DESC
LIMIT 100

SELECT `source`.`village_name` AS `小区名`, `source`.`district` AS `行政区`, `source`.`region` AS `地区`, `source`.`avg` AS `房价均值`, `source`.`count` AS `挂牌数`
FROM (SELECT `lianjia_nc`.`village_name` AS `village_name`, `lianjia_nc`.`district` AS `district`, `lianjia_nc`.`region` AS `region`, AVG(`lianjia_nc`.`unit_price`) AS `avg`, COUNT(*) AS `count` FROM `lianjia_nc`
GROUP BY `lianjia_nc`.`village_name`, `lianjia_nc`.`district`, `lianjia_nc`.`region`
ORDER BY `lianjia_nc`.`village_name` ASC, `lianjia_nc`.`district` ASC, `lianjia_nc`.`region` ASC) AS `source`
WHERE `source`.`count` > 8 ORDER BY `source`.`count` DESC
LIMIT 100

