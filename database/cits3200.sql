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

 Date: 15/09/2022 18:36:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'documenttable' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of document_detail
-- ----------------------------

-- ----------------------------
-- Table structure for event
-- ----------------------------
DROP TABLE IF EXISTS `event`;
CREATE TABLE `event`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `userid` int UNSIGNED NOT NULL COMMENT 'id in user table',
  `firstname` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'firstname',
  `lastname` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'lastname',
  `start time` datetime NOT NULL COMMENT 'the start time of appointment',
  `end time` datetime NOT NULL COMMENT 'the end time of appointment',
  `content` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'detail of appointment',
  `email` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'phone-number',
  `diet` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'diet',
  `guests` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'guests',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'create-time',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'change time',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'event table' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of event
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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'paymenttable' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of payment_detail
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `password` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'password',
  `email` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'createtime',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'changetime',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'usertable' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('matt', 2, '123123', '22546998@qq.com', '2022-09-14 21:58:47', '2022-09-14 21:58:47');
INSERT INTO `user` VALUES ('mards', 3, '200456', '22220808@gmail', '2022-09-15 13:46:30', '2022-09-15 13:46:30');
INSERT INTO `user` VALUES ('abc', 4, '123456', '123456@gmail.com', '2022-09-15 13:52:32', '2022-09-15 13:52:32');
INSERT INTO `user` VALUES ('abcdd', 5, 'abcdd', 'abcdd@gmail.com', '2022-09-15 14:41:04', '2022-09-15 14:41:04');
INSERT INTO `user` VALUES ('bbbb', 6, 'bbbb', 'bbbb@gamil.com', '2022-09-15 14:43:47', '2022-09-15 14:43:47');
INSERT INTO `user` VALUES ('cccc', 7, 'cccc', 'cccc@gmail.com', '2022-09-15 14:44:52', '2022-09-15 14:44:52');
INSERT INTO `user` VALUES ('dddd', 8, 'dddd', 'dddd@gmail.com', '2022-09-15 14:46:20', '2022-09-15 14:46:20');

-- ----------------------------
-- Table structure for user-role
-- ----------------------------
DROP TABLE IF EXISTS `user-role`;
CREATE TABLE `user-role`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `role_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'role name(user or admin)',
  `userid` int UNSIGNED NOT NULL COMMENT 'id in user table',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'createtime',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `FK1`(`userid` ASC) USING BTREE,
  CONSTRAINT `FK1` FOREIGN KEY (`userid`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'roletable' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of user-role
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
