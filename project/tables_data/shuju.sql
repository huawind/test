CREATE TABLE `deal_foodtypes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `typeid` varchar(10) NOT NULL,
  `typename` varchar(20) NOT NULL,
  `typesort` int(11) NOT NULL,
  `childtypenames` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
);

insert into deal_foodtypes(typeid,typename,childtypenames,typesort)
values("88","全部","全部分类:0",1),
("99","相机","全部分类:0#单反:999#数码相机:998",2),
("100","女装","全部分类:0#冬装:1001#夏装:1002",3),
("101","美容/美颜/香水","全部分类:0#面膜:1001#护肤品:1002#香水:1003",4),
("102","手机","全部分类:0#苹果:3001#小米:3002#华为:3003#三星:3004#联想:3005#vivo:3006",5),
("104","户外用品","全部分类:0#自行车:4001#烧烤架:4002#帐篷:4003#运动器具:4004",6),
("105","书籍资料","全部分类:0#文学著作:5001#考研资料:5002#小说:5003:其他#:5004",7),
("106","鞋包配饰","全部分类:0#女包:6001#男包:6002#旅行箱:6003#配饰:6004",8);
CREATE TABLE `axf_goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productid` varchar(10) NOT NULL,
  `productimg` varchar(150) NOT NULL,
  `productname` varchar(50) NOT NULL,
  `productlongname` varchar(100) NOT NULL,
  `isxf` tinyint(1) DEFAULT NULL,
  `pmdesc` varchar(10) NOT NULL,
  `specifics` varchar(20) NOT NULL,
  `price` varchar(10) NOT NULL,
  `marketprice` varchar(10) NOT NULL,
  `categoryid` varchar(10) NOT NULL,
  `childcid` varchar(10) NOT NULL,
  `childcidname` varchar(10) NOT NULL,
  `dealerid` varchar(10) NOT NULL,
  `storenums` int(11) NOT NULL,
  `productnum` int(11) NOT NULL,
  PRIMARY KEY (`id`)
)
-- root root123456
insert into deal_goods(productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,marketprice,categoryid,childcid,childcidname,dealerid,storenums,productnum)
 values("10000","/static/home/img/3.jpg","衣服风衣","均码 中款收腰款 洋气好看",0,0,"L",60.00,90.00,100,1002,"夏装","500",1,0),
("20001","/static/home/img/4.jpg","面膜"," 百雀羚小雀幸静润补水保湿面膜贴20片女蚕丝 清爽弹润 提亮肤",0,0,"20片",59.00,80.00,101,2001,"面膜","500",1,0),
("30001","/static/home/img/5.jpg","苹果手机"," 9成新国航16g苹果6s王者荣耀刺激战场运行流畅用过苹果的人都知道6s是2g运行",0,0,"1",1200.00,2000.00,102,3001,"苹果","500",1,0),
("40001","/static/home/img/6.jpg","笔记本"," 只撕过一页其他完好全新 正版",0,0,"1",4.00,10.00,105,5004,"其他","500",1,0),
("50001","/static/home/img/6.jpg","相机"," 9层新 数码相机功能齐全拍照清晰照亮你的美",0,0,"1",500.00,1200.00,99,998,"数码相机","500",1,0);