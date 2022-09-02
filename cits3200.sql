/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3306
 Source Schema         : cits3200

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 02/09/2022 13:51:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for apply
-- ----------------------------
DROP TABLE IF EXISTS `apply`;
CREATE TABLE `apply`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `flowid` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'Number of orders generated automatically',
  `userid` int UNSIGNED NOT NULL COMMENT 'id in user table',
  `start time` datetime NOT NULL COMMENT 'the start time of appointment',
  `end time` datetime NOT NULL COMMENT 'the end time of appointment',
  `title` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'Subject of appointment',
  `content` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'detail of appointment',
  `type` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'type of appointment',
  `status` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'status of appointment (approve refuse or undetermined )',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'createtime',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'changetime',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `FK4`(`userid` ASC) USING BTREE,
  CONSTRAINT `FK4` FOREIGN KEY (`userid`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'applytable' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of apply
-- ----------------------------

-- ----------------------------
-- Table structure for apply_detail
-- ----------------------------
DROP TABLE IF EXISTS `apply_detail`;
CREATE TABLE `apply_detail`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `fid` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'the flow id in apply table',
  `audituserid` int UNSIGNED NOT NULL COMMENT 'auditid in user table',
  `auditremark` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'describe why aggree or refuse',
  `audittime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'audittime',
  `status` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'status of appointment (approve refuse or undetermined )',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'apply_detailtable' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of apply_detail
-- ----------------------------

-- ----------------------------
-- Table structure for document_detail
-- ----------------------------
DROP TABLE IF EXISTS `document_detail`;
CREATE TABLE `document_detail`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `userid` int UNSIGNED NOT NULL COMMENT 'id in user table',
  `type` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'type of docunment',
  `status` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'status of document',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'createtime',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `FK3`(`userid` ASC) USING BTREE,
  CONSTRAINT `FK3` FOREIGN KEY (`userid`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'documenttable' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of document_detail
-- ----------------------------

-- ----------------------------
-- Table structure for payment_detail
-- ----------------------------
DROP TABLE IF EXISTS `payment_detail`;
CREATE TABLE `payment_detail`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `userid` int UNSIGNED NOT NULL COMMENT 'id in user table',
  `flowid` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT ' another Number of payment generated automatically by backend',
  `amount` decimal(9, 2) UNSIGNED NOT NULL COMMENT 'amount of payment',
  `status` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'status of payment',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'createtime',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `FK2`(`userid` ASC) USING BTREE,
  CONSTRAINT `FK2` FOREIGN KEY (`userid`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'paymenttable' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of payment_detail
-- ----------------------------

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `roleid` int UNSIGNED NOT NULL COMMENT 'roleid',
  `role_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'roleid',
  `remark` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'describe_permissions',
  `number` int NULL DEFAULT NULL COMMENT 'number_of_permissions',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'roletable' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of role
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `username` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'username',
  `display_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'userid',
  `password` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'password',
  `email` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'createtime',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'changetime',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'usertable' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of user
-- ----------------------------

-- ----------------------------
-- Table structure for user-role
-- ----------------------------
DROP TABLE IF EXISTS `user-role`;
CREATE TABLE `user-role`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `roleid` int UNSIGNED NOT NULL COMMENT 'roleid',
  `userid` int UNSIGNED NOT NULL COMMENT 'id in user table',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'createtime',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `FK1`(`userid` ASC) USING BTREE,
  CONSTRAINT `FK1` FOREIGN KEY (`userid`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'role_usertable' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of user-role
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
