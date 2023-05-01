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
-- Table structure for lianjia_nc_new
-- ----------------------------
DROP TABLE IF EXISTS `lianjia_nc_new`;
CREATE TABLE `lianjia_nc_new` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键自增',
  `url` varchar(100) UNIQUE COMMENT 'url',  
  `village_name` varchar(40) NOT NULL COMMENT '小区名称', 
  `unit_price` MEDIUMINT NOT NULL COMMENT '每平方价',
  `district` varchar(20) NOT NULL COMMENT '所属区县',
  `region` varchar(20) DEFAULT NULL COMMENT '地区',
  `sale_date` DATE DEFAULT NULL COMMENT '开盘时间',
  `deliver_date` DATE DEFAULT NULL COMMENT '开盘时间',
  `house_usage` varchar(20) DEFAULT NULL COMMENT '房屋用途（住宅？）',
  `house_property` varchar(20) DEFAULT NULL COMMENT '房屋产权',
  `building_type` varchar(20) NOT NULL COMMENT '建筑类型(高层?)',
  `developer_name` varchar(100) DEFAULT NULL COMMENT '开发商名',
  `specials` varchar(100) DEFAULT NULL COMMENT '特色',
  `house_num` MEDIUMINT DEFAULT NULL COMMENT '规划户数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
