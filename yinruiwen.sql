/*
Navicat MySQL Data Transfer

Source Server         : 47.52.76.196_3306
Source Server Version : 50720
Source Host           : 47.52.76.196:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-03-07 10:27:31
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for yinruiwen
-- ----------------------------
DROP TABLE IF EXISTS `yinruiwen`;
CREATE TABLE `yinruiwen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bb` varchar(50) DEFAULT NULL,
  `nj` varchar(50) DEFAULT NULL,
  `ke` varchar(50) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `zyid` int(11) DEFAULT NULL,
  `download_url` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52332 DEFAULT CHARSET=utf8;
