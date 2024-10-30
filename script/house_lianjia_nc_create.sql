/*
Navicat MySQL Data Transfer

Source Server         : s17
Source Server Version : 8.0.32
Source Host           : localhost:3306
Source Database       : house

Target Server Type    : MYSQL
Target Server Version : 50642
File Encoding         : 65001

Date: 2023-03-17 21:58:02
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for lianjia_nc
-- ----------------------------
DROP TABLE IF EXISTS `lianjia_nc`;
CREATE TABLE `lianjia_nc` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键自增',
  `house_id` varchar(20) COMMENT '房屋编号',
  `title` varchar(255) NOT NULL COMMENT '标题',
  `house_struct` varchar(20) NOT NULL COMMENT '房屋结构',
  `floor_info` varchar(20) NOT NULL COMMENT '楼层信息 ',
  `total_floor` tinyint NOT NULL COMMENT '楼层总数',
  `direction` varchar(20) DEFAULT NULL COMMENT '房屋朝向',
  `total_area` smallint NOT NULL COMMENT '总面积',
  `village_name` varchar(40) NOT NULL COMMENT '小区名称',
  `district` varchar(20) NOT NULL COMMENT '所属区县',
  `region` varchar(20) DEFAULT NULL COMMENT '地区',
  `fitment` varchar(20) DEFAULT NULL COMMENT '装修情况',
  `elevator_rate` varchar(20) DEFAULT NULL COMMENT '梯户比例',
  `start_time` DATE DEFAULT NULL COMMENT '挂牌时间',
  `house_usage` varchar(20) DEFAULT NULL COMMENT '房屋用途',
  `house_property` varchar(20) DEFAULT NULL COMMENT '房屋产权',
  `total_price` smallint NOT NULL COMMENT '总价',
  `unit_price` MEDIUMINT NOT NULL COMMENT '每平方价',
  `mortgage_info` varchar(20) DEFAULT NULL COMMENT '抵押信息',
  `url` varchar(127) DEFAULT NULL COMMENT '源地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
