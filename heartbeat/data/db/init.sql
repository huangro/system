-- init
insert into service_platform(id, title, secret_key, mode, status, mail_list, created_at, updated_at) values(1, '电视淘宝服务', sha1('tvmall'), 'PORT', 1, 'huangfeilong@zhiping.tv;zhangyouliang@zhiping.tv', now(), now());
insert into control_point(sid, title, slot, url, status, created_at, updated_at) values(1, '电视淘宝首页', 'home', '/hd/entry/index', 1, now(), now());
insert into control_point(sid, title, slot, url, status, created_at, updated_at) values(1, '分会场列表页', 'campaigns', '/cms/campaigns/2014/parallel-room?roomId=545246af35c472e748000058', 1, now(), now());
insert into control_point(sid, title, slot, url, status, created_at, updated_at) values(1, '店铺承接页', 'seller', '/hd/seller/index/692200515.html', 1, now(), now());
insert into control_point(sid, title, slot, url, status, created_at, updated_at) values(1, '抽奖页面', 'draw', '/cms/campaigns/2014/lottery1111_huashu?stbid=1104024011600024C102B0CB&nav_source=s-1-entry-item-2', 1, now(), now());
insert into control_point(sid, title, slot, url, status, created_at, updated_at) values(1, '库存STOCK接口', 'stock', '/api/v1/te_jia/item/te_stock?tids=38887184600', 1, now(), now());
insert into control_point(sid, title, slot, url, status, created_at, updated_at) values(1, '支付宝二维码获取接口', 'qrcode', '/api/v1/account/alipay_qrcode_gen?user_credentials=rUshE2H3EQKFDGm24Xf', 1, now(), now());
insert into control_point(sid, title, slot, url, status, created_at, updated_at) values(1, '商品详情页', 'itemshow', '/hd/common/item/show/5452679b77656247f7020000.html', 1, now(), now());

insert into service_platform(id, title, secret_key, mode, status, mail_list, created_at, updated_at) values(2, 'sc-gw01服务器', sha1('sc-gw01'), 'PASV', 1, 'huangfeilong@zhiping.tv;zhangyouliang@zhiping.tv', now(), now());
insert into control_point(sid, title, slot, url, status, created_at, updated_at) values(2, 'sc-gw01服务器状态', 'sc-gw01-info', '', 1, now(), now());
