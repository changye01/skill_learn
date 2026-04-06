CREATE TABLE `supplier_order_m4x_task_detail` (
  `somtd_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `somt_id` int(10) unsigned NOT NULL COMMENT '任务表ID(somt_id)',
  `trade_order_code` varchar(32) NOT NULL COMMENT 'istore 订单号',
  `so_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '生成的采购单ID（PO单）',
  `so_code` varchar(32) NOT NULL DEFAULT '' COMMENT '采购单编号',
  `product_id` int(10) unsigned NOT NULL COMMENT 'istore product ID',
  `product_quantity` int(10) unsigned NOT NULL COMMENT '产品数量',
  `is_pushed` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'SRM系统是否已推送：1-是；0-否',
  `is_virtual_warehouse` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否为虚仓产品(产品来源为M4L-28或M4X-31)：1-是；0-否',
  `order_link_status` tinyint(4) DEFAULT '0' COMMENT '拍单链接检测状态 0-未检测 1-有效 2-无效 3-检测失败',
  `order_link_result` varchar(255) DEFAULT '' COMMENT '拍单链接检测结果描述',
  `create_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '最后更新时间',
  PRIMARY KEY (`somtd_id`),
  KEY `idx_somt_id` (`somt_id`),
  KEY `idx_trade_order_code` (`trade_order_code`),
  KEY `idx_so_id_somt_id` (`so_id`,`somt_id`)
) ENGINE=InnoDB AUTO_INCREMENT=312 DEFAULT CHARSET=utf8mb4 COMMENT='m4x产品销售订单任务详情表';
