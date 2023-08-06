# -*- coding: utf-8 -*-

class SqliteSql:
    checkSkuCode = "select count(1) from PS_C_SKU where SKU_ECODE='%s'"  # 根据条码检索商品是否存在
    checkProCode = "select count(1) from PS_C_PRO where ECODE='%s'"  # 根据款号检索商品是否存在
    checkProGbcode = "select count(1) from PS_C_PRO where GBCODE='%s'"  # 根据国际码检索商品是否存在
    checkPro = "select count(1) from ps_c_pro where ecode='%s' "  # 根据款号检索该款是否存在
    getSku = """select a.id as BarCodeId,a.sku_ecode as BarCode,b.PS_C_PRO_ID as ProductId,b.cp_c_distrib_id as DistribId,'' as DistribidCode,'' as DistribidName,
           b.ps_c_brand_id as BrandId,'' as BrandCode,'' as BrandName, b.ecode as ProductCode,b.ename as ProductName,ifnull(b.txtdim3,'') as TxtDim3,ifnull(b.pricelist,0) as PriceList,
           ifnull(b.pricelower,0) as PriceLower,ifnull(b.proyear,-1) as Proyear,
           ifnull(b.numdim6,-1) as NumDim6,
           ifnull(b.largeclass,-1) as LargeClass,
           ifnull(b.sex,-1) as Sex,
           ifnull(b.prosea,-1) as Prosea,
           ifnull(b.promotiontype,-1) as PromotionType,
           ifnull(b.proline, -1) as ProLine,
           ifnull(b.numdim5,-1) as NumDim5,
           ifnull(b.series,-1) as Series,
           ifnull(b.proband,-1) as Proband,
           ifnull(b.pronature,-1) as Pronature,
           ifnull(b.numdim8,-1) as NumDim8,
           ifnull(b.priceband,-1) as PriceBand,
           ifnull(b.numdim9,-1) as NumDim9,
           ifnull(b.numdim3,-1) as NumDim3,
           ifnull(b.numdim11,-1) as NumDim11,
           ifnull(a.ps_c_spec1obj_id,-1) as Spec1Id,ifnull(a.ps_c_spec2obj_id,-1) as Spec2Id,ifnull(b.fabdesc,'') as  Fabdesc     
           from ps_c_sku a,ps_c_pro b  
           where a.sku_ecode='%s' and  a.ps_c_pro_id=b.ID  order by  a.sku_ecode  """  # 根据条码查询商品详细信息

    getSkus = """select a.id as BarCodeId,a.sku_ecode as BarCode,b.PS_C_PRO_ID as ProductId,b.cp_c_distrib_id as DistribId,'' as DistribidCode,'' as DistribidName,
           b.ps_c_brand_id as BrandId,'' as BrandCode,'' as BrandName, b.ecode as ProductCode,b.ename as ProductName,ifnull(b.txtdim3,'') as TxtDim3,ifnull(b.pricelist,0) as PriceList,
           ifnull(b.pricelower,0) as PriceLower,
           ifnull(b.proyear,-1) as Proyear,
           ifnull(b.numdim6,-1) as NumDim6,
           ifnull(b.largeclass,-1) as LargeClass,
           ifnull(b.sex,-1) as Sex,
           ifnull(b.prosea,-1) as Prosea,
           ifnull(b.promotiontype,-1) as PromotionType,
           ifnull(b.proline, -1) as ProLine,
           ifnull(b.numdim5,-1) as NumDim5,
           ifnull(b.series,-1) as Series,
           ifnull(b.proband,-1) as Proband,
           ifnull(b.pronature,-1) as Pronature,
           ifnull(b.numdim8,-1) as NumDim8,
           ifnull(b.priceband,-1) as PriceBand,
           ifnull(b.numdim9,-1) as NumDim9,
           ifnull(b.numdim3,-1) as NumDim3,
           ifnull(b.numdim11,-1) as NumDim11,
           ifnull(a.ps_c_spec1obj_id,-1) as Spec1Id,ifnull(a.ps_c_spec2obj_id,-1) as Spec2Id,ifnull(b.fabdesc,'') as  Fabdesc     
              from ps_c_sku a,ps_c_pro b  
           where a.sku_ecode in %s and  a.ps_c_pro_id=b.ID  order by  a.sku_ecode  """  # 根据条码查询商品详细信息

    searchSpecObjids = "select ecode,ps_c_specobj_ids from ps_c_pro where ecode='%s' "  # 根据款号查询该款的规格集合和款号
    getSpec1 = "select id,ecode,ename from ps_c_specobj where id in %s order by ecode "  # 根据款号对应的规格实例集合中颜色集合查询对应的颜色实例
    getSpec2 = "select id,ecode,ename,matrixcolno from ps_c_specobj where id in %s order by matrixcolno "  # 根据款号对应的规格实例集合中尺寸集合查询对应的尺寸实例
    getSkusByPro = "select a.id,a.sku_ecode,a.ps_c_spec1obj_id as spec1id,a.ps_c_spec2obj_id as spec2id  from ps_c_sku a,ps_c_pro b  where a.ps_c_pro_id=b.ID and b.ecode='%s' "  # 查询某个款号下所有条码信息（款号矩阵框需要）
    getProInfo = "select id,ecode,ename,pricelist from ps_c_pro where ecode like '%s' limit 0,10 "  # 左匹配查询款号信息
    deleteTableRow = "delete from %s where id =%s "  # 增量数据更新时删除对应表格对应ID的数据
    deleteTableRow1 = "delete from %s where %s "  # 增量数据更新时删除对应表格对应段的数据
    getTableModifiedDate = "select modifieddate from %s where id=%s "  # z查询对应表的对应修改时间字段值
    selectsql = "select %s from %s where %s"
    updatesql = " UPDATE %s SET %s  WHERE %s "

    # 挂单
    inPutData = "INSERT INTO %s %s VALUES %s;"  # 插入数据  %s 表名 %s 字段"()" %s ()
    getDataRetailByDesc= "SELECT %s FROM %s  WHERE %s ORDER BY %s "    # 查询 字段 表 条件 字段降序
    getDataRetail = "SELECT %s FROM %s  WHERE %s "  # 查询 字段 表 条件 字段降序
    changeDataRetail = " UPDATE %s SET %s  WHERE %s;"  # 更改 字段 表 条件
    deleteCashPayWay = "DELETE FROM %s WHERE %s"    # 删除现金付款方式

    getPayWayId="select PAY_WAY_ID from payment where pay_type='CASH'"
    changeCashPay="update DL_B_RETAILPAY_ITEM set PAY_AMT=((select PAY_AMT from DL_B_RETAILPAY_ITEM where DL_B_RETAIL_ID=%s and PAY_WAY_ID=%s ) -%s) where PAY_WAY_ID=%s and DL_B_RETAIL_ID=%s "

    # 零售价调整表操作 AC_F_RETAIL_PRICE_RES
    getRetailPrice = "select %s from %s where %s" # 从零售价表中查询

    # VIP
    # {'ENAME': 'selina', 'LASTDATE': None, 'ECODE': '18032900002', 'AVG_TIME_ACTUAL': None, 'ID': '334358385',
    #  'VP_C_VIPTYPE_ENAME': '快鱼普通卡', 'CONSUMER_STORE': None, 'CP_C_STORE_ID': '206598864953', 'AMT_ACTUAL': None,
    #  'ISACTIVE': 'Y', 'RETAIL_INTE': '0', 'NUMBER_CONSUMERS': 0, 'TIMES': None, 'BIRTHDATE': '2006-03-02',
    #  'MOBIL': '13698005414', 'SEX': 'W', 'INTE': '606', 'OPENDATE': 20180329}
    createVipTable = "CREATE TABLE IF NOT EXISTS VIP" \
                     "(ID INT PRIMARY KEY NOT NULL," \
                     "VP_C_VIP_ACC_ID INTEGER," \
                     "ECODE TEXT," \
                     "VP_C_VIPTYPE_ENAME TEXT," \
                     "ENAME TEXT," \
                     "CP_C_STORE_ID TEXT," \
                     "AVG_TIME_ACTUAL TEXT," \
                     "MOBIL TEXT," \
                     "CONSUMER_STORE TEXT," \
                     "AMT_ACTUAL TEXT," \
                     "SEX TEXT," \
                     "INTE TEXT," \
                     "DECDIM1 real," \
                     "ISLISTLIMIT TEXT," \
                     "DISCOUNT TEXT," \
                     "CP_C_EMP_ID TEXT," \
                     "VP_C_VIPTYPE_ID TEXT," \
                     "OPENDATE TEXT," \
                     "LASTDATE TEXT," \
                     "BIRTHDATE TEXT)"

    createVipIndex = "CREATE INDEX VIP_ECODE_MOBIL_STOREID ON VIP(ECODE,MOBIL,CP_C_STORE_ID)"
    getVip = "select * from VIP where MOBIL = '%s' OR ECODE = '%s'"  # 查询VIP
    getVipECode = "select * from VIP where ECODE = '%s'"  # 查询VIP
    insertVip = "REPLACE into VIP " \
                "(ID,MOBIL,ECODE,VP_C_VIPTYPE_ENAME," \
                "ENAME,CP_C_STORE_ID,AVG_TIME_ACTUAL,CONSUMER_STORE," \
                "AMT_ACTUAL,SEX,INTE,OPENDATE," \
                "LASTDATE,BIRTHDATE,VP_C_VIP_ACC_ID,DECDIM1,ISLISTLIMIT,DISCOUNT,CP_C_EMP_ID,VP_C_VIPTYPE_ID ) " \
                "values (?,?,?,?," \
                "?,?,?,?," \
                "?,?,?,?," \
                "?,?,?,?,?,?,?,?)"

    # 零售表相关
    # 头表
    # "CP_C_DISTRIB_ID integer," \
    # "CP_C_DISTRIB_ECODE TEXT," \
    # "CP_C_DISTRIB_ENAME TEXT," \
    createRetail = "CREATE TABLE IF NOT EXISTS DL_B_RETAIL(" \
                   "ID integer PRIMARY KEY AUTOINCREMENT NOT NULL," \
                   "BILL_NO TEXT," \
                   "BILL_DATE char(8)," \
                   "CP_C_SALER_ID TEXT," \
                   "CP_C_STORE_ID integer," \
                   "CP_C_STORE_ECODE TEXT," \
                   "CP_C_STORE_ENAME TEXT," \
                   "VP_C_VIP_ACC_ID INTEGER," \
                   "VP_C_VIP_ECODE TEXT," \
                   "VP_C_VIP_MOBIL TEXT," \
                   "RETAIL_TYPE varchar(20)," \
                   "REMARK TEXT," \
                   "TRANS_STATUS char(1)," \
                   "ORDER_STATUS char(1)," \
                   "IS_HOLD char(1)," \
                   "IS_ABNORMAL char(1)," \
                   "VIP_SCORE real," \
                   "CONSUME_SCORE real," \
                   "VIP_ADDRESS TEXT," \
                   "VIP_ENAME TEXT," \
                   "VIP_RECEIVER TEXT," \
                   "VIP_TEL TEXT," \
                   "VIP_PRO TEXT," \
                   "VIP_CITY TEXT," \
                   "VIP_DIST TEXT," \
                   "VIP_ADDRESS_REMARK TEXT," \
                   "VIP_EXPRESS_TYPE TEXT," \
                   "VIP_GET_TYPE TEXT," \
                   "STATUS TEXT," \
                   "STATUSID INTEGER," \
                   "STATUSNAME TEXT," \
                   "STATUSENAME TEXT," \
                   "STATUSTIME DATETIME," \
                   "CREATIONDATE DATETIME," \
                   "SUM_QTY_BILL real," \
                   "SUM_AMT_LIST real," \
                   "SUM_AMT_RETAIL real," \
                   "SUM_AMT_RECEIVABLE real," \
                   "SUM_AMT_ACTUAL real," \
                   "SUM_AMT_COST real," \
                   "SERIAL_NUMBER TEXT," \
                   "SUM_PAYMENT real," \
                   "PAY_CHANGE real," \
                   "OWNERID TEXT," \
                   "OWNERNAME TEXT," \
                   "OWNERENAME TEXT," \
                   "DELER_ID TEXT," \
                   "DELER_NAME TEXT," \
                   "DELER_ENAME TEXT," \
                   "TRANS_TIME datetime,"\
                   "FAILURE_REASON TEXT," \
                   "POS_NO TEXT," \
                   "DEL_TIME TEXT," \
                   "AMOUNT real," \
                   "WEATHER TEXT)"


    createRetailIndex="create index age_index_billno on DL_B_RETAIL (BILL_NO)"
    createRetailIndex1 = "create index age_index_id on DL_B_RETAIL (ID)"

    # 明细表
    createRetailItem = "CREATE TABLE IF NOT EXISTS DL_B_RETAIL_ITEM(" \
                       "ID integer PRIMARY KEY AUTOINCREMENT NOT NULL," \
                       "DL_B_RETAIL_ID INTEGER," \
                       "PS_C_PRO_ID INTEGER," \
                       "PS_C_PRO_ECODE varchar(20)," \
                       "PS_C_PRO_ENAME TEXT," \
                       "PRICE_LIST real," \
                       "RETAIL_PRICE real," \
                       "PRICE_RECEIVABLE real," \
                       "PRICE_ACTUAL real," \
                       "PS_C_CLR_ID INTEGER," \
                       "PS_C_CLR_ECODE varchar(20)," \
                       "PS_C_CLR_ENAME varchar(20)," \
                       "PS_C_SIZE_ID INTEGER," \
                       "PS_C_SIZE_ECODE varchar(20)," \
                       "PS_C_SIZE_ENAME varchar(50)," \
                       "PS_C_SKU_ID INTEGER," \
                       "PS_C_SKU_ECODE varchar(20)," \
                       "PS_C_PRO_PROMOTIONTYPE varchar(50)," \
                       "PS_C_PRO_PRONATURE varchar(50)," \
                       "FROM_BILL_ID INTEGER," \
                       "FROM_BILL_NO varchar(20)," \
                       "FROM_BILL_TIEM_ID INTEGER," \
                       "FROM_BILL_BILLDATE char(8)," \
                       "CP_C_SALER_ID INTEGER," \
                       "CP_C_SALER_ECODE varchar(20)," \
                       "CP_C_SALER_ENUMNO varchar(20)," \
                       "CP_C_SALER_ENAME varchar(50)," \
                       "POS_NO varchar(20)," \
                       "SALE_TYPE varchar(10)," \
                       "QTY_BILL real," \
                       "QTY_ORDER real," \
                       "AMT_LIST real," \
                       "AMT_RETAIL real," \
                       "AMT_RECEIVABLE real," \
                       "AMT_ACTUAL real," \
                       "VIP_SCORE real," \
                       "CONSUME_SCORE real," \
                       "PROMOTION_ID varchar(200)," \
                       "REMARK varchar(255)," \
                       "CREATIONDATE datetime," \
                       "DISCOUNT real," \
                       "SEX_ECODE TEXT," \
                       "AMOUNT real," \
                       "RETURN_CASE TEXT)"


    createRetailIndex2 = "create index age_index_dlbretailid on DL_B_RETAIL_ITEM (DL_B_RETAIL_ID)"

    # 零售付款明细表
    createRetailPayItem = "CREATE TABLE IF NOT EXISTS DL_B_RETAILPAY_ITEM(" \
                          "ID integer PRIMARY KEY AUTOINCREMENT NOT NULL," \
                          "DL_B_RETAIL_ID INTEGER," \
                          "PAY_WAY_ID INTEGER," \
                          "PAY_WAY_CODE varchar(20)," \
                          "PAY_WAY_NAME varchar(50)," \
                          "PAY_TYPE varchar(50)," \
                          "PAY_AMT real," \
                          "REMARK varchar(255)," \
                          "PAY_ACC varchar(50)," \
                          "PAY_NO varchar(255)," \
                          "COUPON_NO varchar(50)," \
                          "COUPON_AMT real," \
                          "OUT_TRADE_NO varchar(50)," \
                          "STATE char(1)," \
                          "CREATIONDATE datetime)"
    createRetailIndex3 = "create index age_index_dlbretailpayid on DL_B_RETAILPAY_ITEM (DL_B_RETAIL_ID)"

    # 零售促销执行明细表
    createRetailSalesItem = "CREATE TABLE IF NOT EXISTS DL_B_RETAILSALES_ITEM(" \
                          "ID integer PRIMARY KEY AUTOINCREMENT NOT NULL," \
                          "DL_B_RETAIL_ID INTEGER," \
                          "SALES_WAY_ID INTEGER," \
                          "SALES_WAY_NAME varchar(150)," \
                          "SALES_WAY_CODE varchar(50)," \
                          "QTY INTEGER," \
                          "PS_C_PRO_ECODE varchar(50)," \
                          "PS_C_SKU_ECODE varchar(50)," \
                          "DISCOUNT_AMT real," \
                          "CREATIONDATE datetime)"
    createRetailIndex4 = "create index age_index_dlbretailsalesid on DL_B_RETAILSALES_ITEM (DL_B_RETAIL_ID)"

    #零售单关联收货地址表
    createRetailAddressItem = "CREATE TABLE IF NOT EXISTS DL_B_RETAILADDRESS_ITEM (" \
                          "ID integer PRIMARY KEY AUTOINCREMENT NOT NULL," \
                          "DL_B_RETAIL_ID INTEGER," \
                          "ADDRESS_ID INTEGER," \
                          "RECEIVER varchar(50)," \
                          "MOBIL varchar(50)," \
                          "CP_C_PRO_ID INTEGER," \
                          "CP_C_CITY_ID INTEGER," \
                          "CP_C_DIST_ID INTEGER," \
                          "CP_C_PRO_ENAME varchar(50)," \
                          "CP_C_CITY_ENAME varchar(50)," \
                          "CP_C_DIST_ENAME varchar(50)," \
                          "ADDRESS varchar(150)," \
                          "POST varchar(10)," \
                          "REMARK varchar(150))"
    createRetailIndex5 = "create index age_index_dlbretailaddressid on DL_B_RETAILADDRESS_ITEM (DL_B_RETAIL_ID)"
    #假数据功能使用的表-start

    # 零售表相关
    # 头表
    createRetailJS = "CREATE TABLE IF NOT EXISTS DL_B_RETAIL_JS(" \
                   "ID integer PRIMARY KEY AUTOINCREMENT NOT NULL," \
                   "BILL_NO TEXT," \
                   "BILL_DATE char(8)," \
                   "CP_C_SALER_ID TEXT," \
                   "CP_C_STORE_ID integer," \
                   "CP_C_STORE_ECODE TEXT," \
                   "CP_C_STORE_ENAME TEXT," \
                   "VP_C_VIP_ACC_ID INTEGER," \
                   "VP_C_VIP_ECODE TEXT," \
                   "VP_C_VIP_MOBIL TEXT," \
                   "RETAIL_TYPE varchar(20)," \
                   "REMARK TEXT," \
                   "TRANS_STATUS char(1)," \
                   "ORDER_STATUS char(1)," \
                   "IS_HOLD char(1)," \
                   "IS_ABNORMAL char(1)," \
                   "VIP_SCORE real," \
                   "CONSUME_SCORE real," \
                   "VIP_ADDRESS TEXT," \
                   "VIP_ENAME TEXT," \
                   "VIP_RECEIVER TEXT," \
                   "VIP_TEL TEXT," \
                   "VIP_PRO TEXT," \
                   "VIP_CITY TEXT," \
                   "VIP_DIST TEXT," \
                   "VIP_ADDRESS_REMARK TEXT," \
                   "VIP_EXPRESS_TYPE TEXT," \
                   "VIP_GET_TYPE TEXT," \
                   "STATUS TEXT," \
                   "STATUSID INTEGER," \
                   "STATUSNAME TEXT," \
                   "STATUSENAME TEXT," \
                   "STATUSTIME DATETIME," \
                   "CREATIONDATE DATETIME," \
                   "SUM_QTY_BILL real," \
                   "SUM_AMT_LIST real," \
                   "SUM_AMT_RETAIL real," \
                   "SUM_AMT_RECEIVABLE real," \
                   "SUM_AMT_ACTUAL real," \
                   "SUM_AMT_COST real," \
                   "SERIAL_NUMBER TEXT," \
                   "SUM_PAYMENT real," \
                   "PAY_CHANGE real," \
                   "OWNERID TEXT," \
                   "OWNERNAME TEXT," \
                   "OWNERENAME TEXT," \
                   "DELER_ID TEXT," \
                   "DELER_NAME TEXT," \
                   "DELER_ENAME TEXT," \
                   "TRANS_TIME datetime," \
                   "FAILURE_REASON TEXT," \
                   "POS_NO TEXT," \
                   "DEL_TIME TEXT," \
                   "AMOUNT real," \
                   "WEATHER TEXT)"

    createRetailIndexJS = "create index age_index_billno_JS on DL_B_RETAIL_JS (BILL_NO)"
    createRetailIndex1JS = "create index age_index_id_JS on DL_B_RETAIL_JS (ID)"

    # 明细表
    createRetailItemJS = "CREATE TABLE IF NOT EXISTS DL_B_RETAIL_ITEM_JS(" \
                       "ID integer PRIMARY KEY AUTOINCREMENT NOT NULL," \
                       "DL_B_RETAIL_ID INTEGER," \
                       "PS_C_PRO_ID INTEGER," \
                       "PS_C_PRO_ECODE varchar(20)," \
                       "PS_C_PRO_ENAME TEXT," \
                       "PRICE_LIST real," \
                       "RETAIL_PRICE real," \
                       "PRICE_RECEIVABLE real," \
                       "PRICE_ACTUAL real," \
                       "PS_C_CLR_ID INTEGER," \
                       "PS_C_CLR_ECODE varchar(20)," \
                       "PS_C_CLR_ENAME varchar(20)," \
                       "PS_C_SIZE_ID INTEGER," \
                       "PS_C_SIZE_ECODE varchar(20)," \
                       "PS_C_SIZE_ENAME varchar(50)," \
                       "PS_C_SKU_ID INTEGER," \
                       "PS_C_SKU_ECODE varchar(20)," \
                       "PS_C_PRO_PROMOTIONTYPE varchar(50)," \
                       "PS_C_PRO_PRONATURE varchar(50)," \
                       "FROM_BILL_ID INTEGER," \
                       "FROM_BILL_NO varchar(20)," \
                       "FROM_BILL_TIEM_ID INTEGER," \
                       "FROM_BILL_BILLDATE char(8)," \
                       "CP_C_SALER_ID INTEGER," \
                       "CP_C_SALER_ECODE varchar(20)," \
                       "CP_C_SALER_ENUMNO varchar(20)," \
                       "CP_C_SALER_ENAME varchar(50)," \
                       "POS_NO varchar(20)," \
                       "SALE_TYPE varchar(10)," \
                       "QTY_BILL real," \
                       "QTY_ORDER real," \
                       "AMT_LIST real," \
                       "AMT_RETAIL real," \
                       "AMT_RECEIVABLE real," \
                       "AMT_ACTUAL real," \
                       "VIP_SCORE real," \
                       "CONSUME_SCORE real," \
                       "PROMOTION_ID varchar(200)," \
                       "REMARK varchar(255)," \
                       "CREATIONDATE datetime," \
                       "DISCOUNT real," \
                       "SEX_ECODE TEXT," \
                       "AMOUNT real," \
                       "VIPDEDUCTIONAMT real," \
                       "FROM_BILL_ADD_TYPE TEXT," \
                       "DMAL1 real," \
                       "DMAL2 real," \
                       "EXCHANGE_FLUG VARCHAR(10)," \
                       "RETURN_CASE TEXT)"

    createRetailIndex2JS = "create index age_index_dlbretailid_JS on DL_B_RETAIL_ITEM_JS (DL_B_RETAIL_ID)"

    # 零售付款明细表
    createRetailPayItemJS = "CREATE TABLE IF NOT EXISTS DL_B_RETAILPAY_ITEM_JS(" \
                          "ID integer PRIMARY KEY AUTOINCREMENT NOT NULL," \
                          "DL_B_RETAIL_ID INTEGER," \
                          "PAY_WAY_ID INTEGER," \
                          "PAY_WAY_CODE varchar(20)," \
                          "PAY_WAY_NAME varchar(50)," \
                          "PAY_TYPE varchar(50)," \
                          "PAY_AMT real," \
                          "REMARK varchar(255)," \
                          "PAY_ACC varchar(50)," \
                          "PAY_NO varchar(255)," \
                          "COUPON_NO varchar(50)," \
                          "COUPON_AMT real," \
                          "OUT_TRADE_NO varchar(50)," \
                          "STATE char(1)," \
                          "CREATIONDATE datetime)"
    createRetailIndex3JS = "create index age_index_dlbretailpayid_JS on DL_B_RETAILPAY_ITEM_JS (DL_B_RETAIL_ID)"

    # 零售促销执行明细表
    createRetailSalesItemJS = "CREATE TABLE IF NOT EXISTS DL_B_RETAILSALES_ITEM_JS(" \
                            "ID integer PRIMARY KEY AUTOINCREMENT NOT NULL," \
                            "DL_B_RETAIL_ID INTEGER," \
                            "SALES_WAY_ID INTEGER," \
                            "SALES_WAY_NAME varchar(150)," \
                            "SALES_WAY_CODE varchar(50)," \
                            "QTY INTEGER," \
                            "PS_C_PRO_ECODE varchar(50)," \
                            "PS_C_SKU_ECODE varchar(50)," \
                            "DISCOUNT_AMT real," \
                            "CREATIONDATE datetime)"
    createRetailIndex4JS = "create index age_index_dlbretailsalesid_JS on DL_B_RETAILSALES_ITEM_JS (DL_B_RETAIL_ID)"

    #假数据使用的表-end

    # 删除促销执行明细表
    deletePromotionExecItems = "delete from DL_B_RETAILSALES_ITEM where DL_B_RETAIL_ID=%s"
    getSalesItemsByRetailID = "select SALES_WAY_ID,SALES_WAY_NAME,SALES_WAY_CODE,QTY,PS_C_PRO_ECODE,PS_C_SKU_ECODE,DISCOUNT_AMT,CREATIONDATE from DL_B_RETAILSALES_ITEM where DL_B_RETAIL_ID=%s"
    #查询全渠道收货地址明细
    # getAddressByRetailID = "select DL_B_RETAIL_ID,RECEIVER,MOBIL,CP_C_PRO_ID,CP_C_CITY_ID,CP_C_DIST_ID,CP_C_PRO_ENAME,CP_C_CITY_ENAME,CP_C_DIST_ENAME,ADDRESS,POST,REMARK from DL_B_RETAILADDRESS_ITEM where DL_B_RETAIL_ID=%s"
    getAddressByRetailID2 = "select DL_B_RETAIL_ID,ADDRESS_ID,RECEIVER,MOBIL,CP_C_PRO_ID,CP_C_CITY_ID,CP_C_DIST_ID,CP_C_PRO_ENAME,CP_C_CITY_ENAME,CP_C_DIST_ENAME,ADDRESS,POST,REMARK from DL_B_RETAILADDRESS_ITEM where DL_B_RETAIL_ID=%s"

    #修改全渠道收获地址明细
    updateAddressByRetailID = "update DL_B_RETAIL set VIP_ENAME  = '%s',VIP_RECEIVER ='%s',VIP_PRO='%s',VIP_CITY='%s',VIP_DIST ='%s',VIP_ADDRESS='%s' where ID = %s"
    updateAddressByRetailID2 = "update DL_B_RETAILADDRESS_ITEM set ADDRESS_ID=%d ,RECEIVER = '%s',MOBIL ='%s',CP_C_PRO_ID=%d,CP_C_CITY_ID=%d,CP_C_DIST_ID=%d,CP_C_PRO_ENAME='%s',CP_C_CITY_ENAME='%s',CP_C_DIST_ENAME='%s',ADDRESS='%s',POST='%s' where DL_B_RETAIL_ID = %s"
    # 获取当天最大的流水号
    getRetailMaxSerialNum = "select max(SERIAL_NUMBER) as SERIAL_NUMBER from DL_B_RETAIL where BILL_DATE = '%s'"

    # {"EMPSINFO": [{"ID": 1, "ECODE": "asda", ...}], "USERSINFO": [{"ID": 1, "ECODE": "asda", ...}]}
    # 营业员表
    createEmpsTable = "CREATE TABLE IF NOT EXISTS EMPS" \
                     "(ID INT PRIMARY KEY NOT NULL," \
                     "ECODE TEXT," \
                     "ENUMNO TEXT," \
                     "ENAME TEXT," \
                     "CP_C_STORE_ID TEXT)"

    createEmpsIndex = "CREATE INDEX EMPS_ECODE_ENUMNO_CP_C_STORE_ID ON EMPS(ECODE,ENUMNO,CP_C_STORE_ID)"
    getEmps = "select * from EMPS ORDER BY ENUMNO"  # 查询营业员
    insertEmps = "REPLACE into EMPS " \
                "(ID,ECODE,ENUMNO,ENAME," \
                "CP_C_STORE_ID) " \
                "values (?,?,?,?," \
                "?)"
    deleteEmps = "DELETE FROM EMPS"

    # 用户表
    createUsersTable = "CREATE TABLE IF NOT EXISTS USERS" \
                     "(ID INT PRIMARY KEY NOT NULL," \
                     "NAME TEXT," \
                     "PASSWORD TEXT," \
                     "ENAME TEXT," \
                     "CP_C_STORE_ID TEXT," \
                     "CP_C_DISTRIB_ID TEXT)"

    createUsersIndex = "CREATE INDEX USERS_ECODE_CP_C_STORE_ID ON USERS(ECODE,CP_C_STORE_ID)"
    getUsers = "select * from USERS where NAME = '%s'"  # 查询用户
    usersLogin = "select * from USERS where NAME = '%s' and CP_C_STORE_ID = %s"  #验证用户
    insertUsers = "REPLACE into USERS " \
                "(ID,NAME,PASSWORD,ENAME," \
                "CP_C_STORE_ID,CP_C_DISTRIB_ID,LANGUAGE,LAWSPASSWORD) " \
                "values (?,?,?,?," \
                "?,?,?,?)"

    insertOrUpdateUsers= "REPLACE into USERS " \
                "(ID,NAME,PASSWORD,ENAME," \
                "CP_C_STORE_ID,CP_C_DISTRIB_ID,LANGUAGE) " \
                "values (?,?,?,?," \
                "?,?,?)"
    deleteUsers = "DELETE FROM USERS"
    updateUserPassWd = "update users set password='%s' where NAME='%s'"

    # 调价记录表
    createPosAdjTable = "CREATE TABLE IF NOT EXISTS AC_F_RETAIL_PRICE_RES(" \
                          "CP_C_STORE_ID integer," \
                          "CP_C_STORE_ECODE nvarchar(50)," \
                          "CP_C_STORE_ENAME nvarchar(50)," \
                          "PS_C_PRO_ID integer," \
                          "PS_C_PRO_ECODE nvarchar(50)," \
                          "PS_C_SKU_ID integer," \
                          "PS_C_SKU_ECODE nvarchar(50)," \
                          "PRICE_RETAIL real," \
                          "PS_C_PRO_ENAME nvarchar(50)," \
                          "PRICE_LIST real," \
                          "DISCOUNT real," \
                          "PRICE_RETAIL_OLD real," \
                          "PS_C_SKU_COLOR_ENAME nvarchar(50)," \
                          "PS_C_SKU_SIZE_ECODE nvarchar(50)," \
                          "PS_C_SKU_SIZE_ENAME nvarchar(50)," \
                          "MODIFIEDDATE text)"
    createRetailPriceProIndex = "CREATE INDEX age_index_proecode ON AC_F_RETAIL_PRICE_RES(PS_C_PRO_ECODE)"
    createRetailPriceSkuIndex = "CREATE INDEX age_index_skuecode ON AC_F_RETAIL_PRICE_RES(PS_C_SKU_ECODE)"
    deleteRetailPriceByStoreId = "delete from AC_F_RETAIL_PRICE_RES where CP_C_STORE_ID!=%s"

    # 创建库存表
    # createPosSkuStockTable = "CREATE TABLE IF NOT EXISTS SC_B_STOCK(" \
    #                     "CP_C_STORE_ID integer," \
    #                     "PS_C_PRO_ECODE nvarchar(50)," \
    #                     "PS_C_SKU_ECODE nvarchar(80)," \
    #                     "PRICE_LIST nvarchar(50)," \
    #                     "PRICECURRENT nvarchar(50)," \
    #                     "QTY_STOCK_ABLE nvarchar(50)," \
    #                     "CLR nvarchar(50)," \
    #                     "SIZE nvarchar(50)," \
    #                     "SEX nvarchar(50)," \
    #                     "STOCK_DATETIME date )"
    createPosSkuStockTable = "CREATE TABLE IF NOT EXISTS SC_B_STOCK(" \
                             "CP_C_STORE_ID integer," \
                             "PS_C_PRO_ECODE nvarchar(50)," \
                             "PS_C_SKU_ECODE nvarchar(80)," \
                             "QTY_STOCK_ABLE nvarchar(50)," \
                             "STOCK_DATETIME date )"
    createPosStockSkuIndex = "CREATE INDEX age_index_skuecode ON SC_B_STOCK(PS_C_SKU_ECODE)"
    deletePosStockByStoreId = "delete from SC_B_STOCK where CP_C_STORE_ID!=%s"

    #获取颜色信息，根据ecode排序
    getSpecColor = "select id, ecode, ename from PS_C_SPECOBJ where PS_C_SPEC_ID = 1 order by ecode"
    #获取尺寸信息，根据matrixcolno升序排序
    getSpecSize = "select id, ecode, ename, matrixcolno from PS_C_SPECOBJ where PS_C_SPEC_ID = 2 order by matrixcolno"

    # 获取商品属性
    getProperties = "select DISTINCT AD_PROCOLUMN_NAME from PS_C_PRODIM_ITEM"
    getItems = "select * from PS_C_PRODIM_ITEM"

    # 获取品牌表信息
    getBrands = "select * from PS_C_BRAND"

    # 获取配销中心信息
    getDistribInfo = "select id, ecode, ename from cp_c_distrib"

    #付款方式
    createPayMent = "CREATE TABLE IF NOT EXISTS PAYMENT(" \
                          "ID integer PRIMARY KEY AUTOINCREMENT NOT NULL," \
                          "PAY_WAY_ID INTEGER," \
                          "PAY_WAY_CODE varchar(20)," \
                          "PAY_WAY_NAME varchar(50)," \
                          "PAY_TYPE varchar(50)," \
                          "ISSYSTEM varchar(10))"
    deletePayMent = "DELETE FROM PAYMENT"
    insertPayMent = "INSERT into PAYMENT " \
                  "(PAY_WAY_ID,PAY_WAY_CODE,PAY_WAY_NAME,PAY_TYPE," \
                    "ISSYSTEM,ORDERNO) " \
                  "values (?,?,?,?," \
                    "?,?)"
    # 查询本地付款方式
    searchPayment = "select PAY_WAY_ID, PAY_WAY_CODE,PAY_WAY_NAME,PAY_TYPE,ISSYSTEM, ifnull(ORDERNO,'') as ORDERNO from PAYMENT"

    #获取零售表头
    getRetailsBill = """select bill_no,
                        ifnull(bill_date, '') as BILL_DATE,
                        ifnull(sum_qty_bill,0) as SUM_QTY_BILL,
                        ifnull(sum_amt_actual, 0.0) as SUM_AMT_ACTUAL,
                        ifnull(sum_payment,0.0) as SUM_PAYMENT,
                        ifnull(pay_change, 0.0) as PAY_CHANGE,
                        ifnull(ownerename, '') as OWNERENAME,
                        ifnull(order_status, '') as ORDER_STATUS,
                        ifnull(status, '0') as STATUS,
                        ifnull(trans_status, '') as TRANS_STATUS, 
                        ifnull(vp_c_vip_acc_id, '') as VP_C_VIP_ID,
                        ifnull(vp_c_vip_mobil,'') as VP_C_VIP_MOBIL,
                        ifnull(vip_score,0) as VIP_SCORE,
                        ifnull(consume_score, '') as CONSUME_SCORE,
                        ifnull(statusename, '') as STATUSENAME,
                        ifnull(statustime, '') as STATUSTIME,
                        ifnull(deler_ename, '') as DELER_ENAME,
                        ifnull(del_time,'') as DEL_TIME,
                        ifnull(remark, '') as REMARK,id as RETAILID,
                        ifnull(creationdate,'') as CREATIONDATE, 
                        ifnull(failure_reason, '') as FAILURE_REASON from %s where 1=1 %s order by case when order_status='0' then 0 else 1 end, bill_date desc,bill_no desc"""

    #获取零售表明细
    getRetailItems = """select ifnull(PS_C_PRO_ECODE, '') as PS_C_PRO_ECODE,			
			                    ifnull(PS_C_SKU_ECODE, '') as PS_C_SKU_ECODE,
			                    ifnull(PRICE_LIST, 0.0) as PRICE_LIST,
			                    ifnull(RETAIL_PRICE, 0.0) as RETAIL_PRICE,
			                    ifnull(PRICE_RECEIVABLE, 0.0) as PRICE_RECEIVABLE,
			                    ifnull(PRICE_ACTUAL,0.0) as PRICE_ACTUAL,
			                    ifnull(QTY_BILL, 0) as QTY_BILL,
			                    ifnull(AMT_ACTUAL,0.0) as AMT_ACTUAL,
			                    ifnull(CP_C_SALER_ENAME, '') as CP_C_SALER_ENAME,
			                    ifnull(SALE_TYPE, '') as SALE_TYPE,
			                    ifnull(CONSUME_SCORE, '') as CONSUME_SCORE,
			                    ifnull(PS_C_PRO_PROMOTIONTYPE, '') as PS_C_PRO_PROMOTIONTYPE,
			                    ifnull(PROMOTION_ID, '') as PROMOTION_ID,
			                    ifnull(PS_C_SIZE_ID,'') as PS_C_SIZE_ID,
			                    ifnull(PS_C_SIZE_ECODE,'') as PS_C_SIZE_ECODE,ifnull(PS_C_SIZE_ENAME,'') as PS_C_SIZE_ENAME,
			                    ifnull(PS_C_CLR_ID,'') as PS_C_CLR_ID,
			                    ifnull(PS_C_CLR_ECODE,'') as PS_C_CLR_ECODE,
			                    ifnull(PS_C_CLR_ENAME,'') as PS_C_CLR_ENAME from %s where dl_b_retail_id=%s"""

    #查询收银明细
    getRetailPayItems = """select ifnull(PAY_WAY_NAME, '') as PAY_WAY_NAME,ifnull(PAY_AMT, 0.0) as PAY_AMT from %s where dl_b_retail_id=%s"""

    #查询已收银未上传的单据
    # getRetailUnUpload = "select ID,BILL_NO,BILL_DATE,CP_C_SALER_ID,CP_C_STORE_ID,CP_C_STORE_ECODE,CP_C_STORE_ENAME,VP_C_VIP_ACC_ID,VP_C_VIP_ECODE  " \
    #                     ",VP_C_VIP_MOBIL,RETAIL_TYPE,REMARK,TRANS_STATUS,ORDER_STATUS,IS_HOLD,IS_ABNORMAL,VIP_SCORE,CONSUME_SCORE" \
    #                     ",VIP_ADDRESS,VIP_ENAME,VIP_RECEIVER,VIP_TEL,VIP_PRO,VIP_CITY,VIP_DIST,VIP_ADDRESS_REMARK,VIP_EXPRESS_TYPE" \
    #                     ",VIP_GET_TYPE,STATUS,STATUSID,STATUSNAME,STATUSENAME,STATUSTIME,CREATIONDATE,SUM_QTY_BILL,SUM_AMT_LIST,SUM_AMT_RETAIL" \
    #                     ",SUM_AMT_RECEIVABLE,SUM_AMT_ACTUAL,SUM_AMT_COST,SERIAL_NUMBER,SUM_PAYMENT,PAY_CHANGE,OWNERID,OWNERNAME,OWNERENAME,DELER_ID" \
    #                     ",DELER_NAME,DELER_ENAME,TRANS_TIME,FAILURE_REASON,POS_NO,DEL_TIME,AMOUNT,WEATHER  " \
    #                     "from DL_B_RETAIL where STATUS = 1 and TRANS_STATUS = 0 " \
    #                     "ORDER by STATUSTIME,TRANS_TIME ASC LIMIT 0,100"
    #2018-08-30修改：TRANS_STATUS不传入服务端
    getRetailUnUpload = "select ID,BILL_NO,BILL_DATE,CP_C_SALER_ID,CP_C_STORE_ID,CP_C_STORE_ECODE,CP_C_STORE_ENAME,VP_C_VIP_ACC_ID,VP_C_VIP_ECODE  " \
                        ",VP_C_VIP_MOBIL,RETAIL_TYPE,REMARK,ORDER_STATUS,IS_HOLD,IS_ABNORMAL,VIP_SCORE,CONSUME_SCORE" \
                        ",VIP_ADDRESS,VIP_ENAME,VIP_RECEIVER,VIP_TEL,VIP_PRO,VIP_CITY,VIP_DIST,VIP_ADDRESS_REMARK,VIP_EXPRESS_TYPE" \
                        ",VIP_GET_TYPE,STATUS,STATUSID,STATUSNAME,STATUSENAME,STATUSTIME,CREATIONDATE,SUM_QTY_BILL,SUM_AMT_LIST,SUM_AMT_RETAIL" \
                        ",SUM_AMT_RECEIVABLE,SUM_AMT_ACTUAL,SUM_AMT_COST,SERIAL_NUMBER,SUM_PAYMENT,PAY_CHANGE,OWNERID,OWNERNAME,OWNERENAME,DELER_ID" \
                        ",DELER_NAME,DELER_ENAME,TRANS_TIME,POS_NO,DEL_TIME,AMOUNT,WEATHER,BIGINT3," \
                        "CP_C_STORE_ID2 "\
                        "from DL_B_RETAIL where STATUS = 1 and TRANS_STATUS = 0 " \
                        "ORDER by BILL_NO DESC,STATUSTIME DESC ,TRANS_TIME ASC LIMIT 0,5"

    #查询已收银上传中，上传时间已经超时的单据
    getRetailTimeOut = "select ID,BILL_NO,BILL_DATE,CP_C_SALER_ID,CP_C_STORE_ID,CP_C_STORE_ECODE,CP_C_STORE_ENAME,VP_C_VIP_ACC_ID,VP_C_VIP_ECODE  " \
                        ",VP_C_VIP_MOBIL,RETAIL_TYPE,REMARK,ORDER_STATUS,IS_HOLD,IS_ABNORMAL,VIP_SCORE,CONSUME_SCORE" \
                        ",VIP_ADDRESS,VIP_ENAME,VIP_RECEIVER,VIP_TEL,VIP_PRO,VIP_CITY,VIP_DIST,VIP_ADDRESS_REMARK,VIP_EXPRESS_TYPE" \
                        ",VIP_GET_TYPE,STATUS,STATUSID,STATUSNAME,STATUSENAME,STATUSTIME,CREATIONDATE,SUM_QTY_BILL,SUM_AMT_LIST,SUM_AMT_RETAIL" \
                        ",SUM_AMT_RECEIVABLE,SUM_AMT_ACTUAL,SUM_AMT_COST,SERIAL_NUMBER,SUM_PAYMENT,PAY_CHANGE,OWNERID,OWNERNAME,OWNERENAME,DELER_ID" \
                        ",DELER_NAME,DELER_ENAME,TRANS_TIME,POS_NO,DEL_TIME,AMOUNT,WEATHER,BIGINT3,CP_C_STORE_ID2 from DL_B_RETAIL  " \
                        "where STATUS = 1 and TRANS_STATUS = 1 and TRANS_TIME <= datetime('%s','localtime') " \
                        "ORDER by BILL_NO DESC,STATUSTIME DESC,TRANS_TIME ASC LIMIT 0,5"

    #查询选中的单据
    getRetailSelected = "select ID,BILL_NO,BILL_DATE,CP_C_SALER_ID,CP_C_STORE_ID,CP_C_STORE_ECODE,CP_C_STORE_ENAME,VP_C_VIP_ACC_ID,VP_C_VIP_ECODE  " \
                        ",VP_C_VIP_MOBIL,RETAIL_TYPE,REMARK,ORDER_STATUS,IS_HOLD,IS_ABNORMAL,VIP_SCORE,CONSUME_SCORE" \
                        ",VIP_ADDRESS,VIP_ENAME,VIP_RECEIVER,VIP_TEL,VIP_PRO,VIP_CITY,VIP_DIST,VIP_ADDRESS_REMARK,VIP_EXPRESS_TYPE" \
                        ",VIP_GET_TYPE,STATUS,STATUSID,STATUSNAME,STATUSENAME,STATUSTIME,CREATIONDATE,SUM_QTY_BILL,SUM_AMT_LIST,SUM_AMT_RETAIL" \
                        ",SUM_AMT_RECEIVABLE,SUM_AMT_ACTUAL,SUM_AMT_COST,SERIAL_NUMBER,SUM_PAYMENT,PAY_CHANGE,OWNERID,OWNERNAME,OWNERENAME,DELER_ID" \
                        ",DELER_NAME,DELER_ENAME,TRANS_TIME,POS_NO,DEL_TIME,AMOUNT,WEATHER,BIGINT3,CP_C_STORE_ID2 " \
                        "from DL_B_RETAIL where STATUS = 1 and BILL_NO IN %s " \
                        "ORDER by STATUSTIME,TRANS_TIME ASC"

    #删除零售单数据
    delRetailData = "delete from %s where %s"

    #查询零售单明细
    getRetailItemById = "select ID,DL_B_RETAIL_ID,PS_C_PRO_ID,PS_C_PRO_ECODE,PS_C_PRO_ENAME,PRICE_LIST,RETAIL_PRICE,PRICE_RECEIVABLE" \
                        ",PRICE_ACTUAL,PS_C_CLR_ID,PS_C_CLR_ECODE,PS_C_CLR_ENAME,PS_C_SIZE_ID,PS_C_SIZE_ECODE,PS_C_SIZE_ENAME,PS_C_SKU_ID" \
                        ",PS_C_SKU_ECODE,PS_C_PRO_PROMOTIONTYPE,PS_C_PRO_PRONATURE,FROM_BILL_ID,FROM_BILL_NO,FROM_BILL_TIEM_ID,FROM_BILL_BILLDATE" \
                        ",CP_C_SALER_ID,CP_C_SALER_ECODE,CP_C_SALER_ENUMNO,CP_C_SALER_ENAME,POS_NO,SALE_TYPE,QTY_BILL,QTY_ORDER,AMT_LIST,AMT_RETAIL" \
                        ",AMT_RECEIVABLE,AMT_ACTUAL,VIP_SCORE,CONSUME_SCORE,PROMOTION_ID,REMARK,CREATIONDATE,DISCOUNT,SEX_ECODE,AMOUNT,RETURN_CASE,DMAL1,DMAL2,VARCHAR15 " \
                        "from DL_B_RETAIL_ITEM where DL_B_RETAIL_ID = %s"
    #查询零售单付款方式
    getRetailPayItemById = "select * from DL_B_RETAILPAY_ITEM where DL_B_RETAIL_ID = %s"
    #根据小票编号查询付款方式
    #getRetailPayItemsByBillNo = "select a.id as ID, a.DL_B_RETAIL_ID as DL_B_RETAIL_ID, a.PAY_WAY_ID as PAY_WAY_ID, a.PAY_WAY_CODE as PAY_WAY_CODE,a.PAY_WAY_NAME as PAY_WAY_NAME,a.PAY_AMT as PAY_AMT,a.REMARK as REMARK,a.PAY_ACC as PAY_ACC,a.PAY_NO as PAY_NO,a.COUPON_NO as COUPON_NO,a.COUPON_AMT as COUPON_AMT,a.CREATIONDATE as CREATIONDATE from DL_B_RETAILPAY_ITEM as a, DL_B_RETAIL as b where a.DL_B_RETAIL_ID=b.id and b.bill_no='%s'"
    getRetailPayItemsByBillNo = "select *,'' as document_number,'' as reference_number from DL_B_RETAILPAY_ITEM where DL_B_RETAIL_ID=(select ID from DL_B_RETAIL where bill_no='%s') "
    getRetailPayItemsByRetailId = "select *,'' as document_number,'' as reference_number from DL_B_RETAILPAY_ITEM where DL_B_RETAIL_ID=%s "
    getRetailIdByBillNo = "select ID from DL_B_RETAIL where bill_no = '%s'"
    #查询单据是否是异常单据
    getOrderIsAbNormal = "select IS_ABNORMAL from DL_B_RETAIL where BILL_NO = '%s'"
    #更新上传标志和上传
    updateRetailTransStatusAndTime = "update DL_B_RETAIL set TRANS_STATUS = 1,TRANS_TIME = '%s' where ID in %s"
    #vip追加
    addVipRetail = "update DL_B_RETAIL set VIP_SCORE=%s,VP_C_VIP_ACC_ID='%s',VP_C_VIP_ECODE='%s',VP_C_VIP_MOBIL='%s' where BILL_NO='%s'"

    # 根据付款类型删除付款不成功的付款方式
    deleteRetailPayByType = "delete from DL_B_RETAILPAY_ITEM where STATE != 1 and PAY_TYPE in %s "

    #更新上传标志和错误日志
    updateRetailTransStatusSuccess = "update DL_B_RETAIL set TRANS_STATUS = 2,FAILURE_REASON ='' where BILL_NO in %s"
    updateRetailTransStatusFailReason = """update DL_B_RETAIL set TRANS_STATUS = 0,FAILURE_REASON = "%s" where BILL_NO = '%s' """
    updateRetailTransStatusFailReasonApos = """update DL_B_RETAIL set TRANS_STATUS = 0,FAILURE_REASON = '%s' where BILL_NO = '%s' """
    delteRetailPayWayByBillNo = "delete from DL_B_RETAILPAY_ITEM where DL_B_RETAIL_ID = (select ID from DL_B_RETAIL where BILL_NO = '%s')"
    #查询单据上传状态
    selecttransstatus="select TRANS_STATUS from DL_B_RETAIL where BILL_NO='%s' "
    # 查询未上传小票数
    selectRetailNumNoUpload = "select COUNT(*) as num from DL_B_RETAIL where STATUS=1 and TRANS_STATUS in (0,1)"

    # 根据原单号查询本地异常单据或者已收银未上传的单据明细。
    getAbnormalRetailItemsByFromBillNo = "select * from dl_b_retail_item WHERE dl_b_retail_id in (select ID from dl_b_retail where (order_status='1' and IS_ABNORMAL='Y') or (status='1' and trans_status!='2')) and FROM_BILL_NO='%s' "

    #获取商品详情信息
    getProDetailInfo = "select * from ps_c_pro where ecode='%s'"

    # 根据ID获取订单商品信息（用于移动支付使用）
    getGoodsDetail = "select PS_C_SKU_ECODE as goods_id,PS_C_PRO_ENAME as goods_name,QTY_BILL as quantity,PRICE_ACTUAL as price from DL_B_RETAIL_ITEM where DL_B_RETAIL_ID=%s"

    #从本地获取调价记录
    getPriceAdjust = """select PS_C_PRO_ECODE,PS_C_PRO_ENAME,ifnull(PS_C_SKU_ECODE, '') as PS_C_SKU_ECODE,
                         PRICE_RETAIL,PRICE_LIST,DISCOUNT,PRICE_RETAIL,PRICE_RETAIL_OLD,
                          ifnull(PS_C_SKU_COLOR_ENAME, '') as PS_C_SKU_COLOR_ENAME, 
                          ifnull(PS_C_SKU_SIZE_ECODE, '') as PS_C_SKU_SIZE_ECODE,
                          ifnull(PS_C_SKU_SIZE_ENAME, '') as PS_C_SKU_SIZE_ENAME
                          from AC_F_RETAIL_PRICE_RES where %s"""
    getPriceAdjCount = "select count (*) as total from AC_F_RETAIL_PRICE_RES where %s"

    #调价记录查询语句
    getPriceAdjExist = "select count(1) from AC_F_RETAIL_PRICE_RES where %s"
    updatePriceAdj = "update AC_F_RETAIL_PRICE_RES set %s where %s"
    insertPriceAdj = "insert into AC_F_RETAIL_PRICE_RES %s values %s"
    PadjTableExit = "select * from sqlite_master where type='table' and name= 'AC_F_RETAIL_PRICE_RES'"

    #库存查询数据
    getStockNum = "select QTY_STOCK_ABLE,ifnull(MODIFYTIME,0) as MODIFYTIME from SC_B_STOCK where CP_C_STORE_ID=%s and PS_C_SKU_ECODE='%s'"  #暂时不用了
    getStockNums = "select PS_C_SKU_ECODE,QTY_STOCK_ABLE from SC_B_STOCK where CP_C_STORE_ID=%s and PS_C_SKU_ECODE in  %s "
    #本地未上传单据零售数量查询
    getRetailQtyBill = "select ifnull(sum(ifnull(qty_bill, 0)),0) as QTY_BILL  from dl_b_retail_item a,dl_b_retail b  where a.ps_c_sku_ecode='%s' and a.dl_b_retail_id=b.id and b.status=1 and b.trans_status in (0,1)"
    getRetailQtyBill1 = "select ifnull(sum(ifnull(qty_bill, 0)),0) as QTY_BILL,a.ps_c_sku_ecode as PS_C_SKU_ECODE  from dl_b_retail_item a,dl_b_retail b  where a.ps_c_sku_ecode in %s and a.dl_b_retail_id=b.id and b.status=1 and b.trans_status in (0,1) group by PS_C_SKU_ECODE"


    #库存相关
    #更新库存
    updateQty = "update SC_B_STOCK set QTY_STOCK_ABLE = %s,STOCK_DATETIME='%s',MODIFYTIME=%s where CP_C_STORE_ID=%s and PS_C_SKU_ECODE = '%s' and (MODIFYTIME is Null or MODIFYTIME <= %s) "
    insertStockQty = "insert into SC_B_STOCK %s values %s"

    # 离线促销相关
    deleteSalesData = "delete from PM_C_PROM_ACTI where ID not in (select ID from PM_C_PROM_ACTI where STORE_IDS like '%s')"
    deleteSalesItemData = "delete from %s where PM_C_PROM_ACTI_ID NOT in (select ID from PM_C_PROM_ACTI)"
    updateSalesData = "update PM_C_PROM_ACTI set STORE_IDS='%s'"
    SearchPromotionActi = """select ID as id,ENAME as ename,PROM_SCOPE as prom_scope,PROM_TYPE as prom_type,PROM_SCHEME_ECODE as prom_type_three,MEMBER_ONLY as members_only,ifnull(VP_C_VIPTYPE_IDS, '') as members_group,IS_RUN_OTHER_PRO as is_run_other_pro, IS_RUN_STORE_ACT as is_run_store_act, IS_RUN_VIP_DISCOUNT as is_run_vip_discount, MAX_TIMES as max_times, EXCHANGE_CONDITION as exchange_condition,GIFT_CONDITION as gift_condition,EORDER as prom_type_two_c,STATUSTIME as publish_date,FREQ_TYPE as FREQ_TYPE,FREQ_VALUE as FREQ_VALUE  from PM_C_PROM_ACTI where %s """

    #假数据功能相关
    getRetailJS="select * from DL_B_RETAIL_JS where cast(bill_date as INT)>=%s"
    getRetailitemJS = "select a.* from DL_B_RETAIL_ITEM_JS a,DL_B_RETAIL_JS b where cast(b.bill_date as INT)>=%s and a.DL_B_RETAIL_ID=b.ID "
    getRetailPayItemJS = "select a.* from DL_B_RETAILPAY_ITEM_JS a,DL_B_RETAIL_JS b where cast(b.bill_date as INT)>=%s and a.DL_B_RETAIL_ID=b.ID "
    getRetailSalesItemJS = "select a.* from DL_B_RETAILSALES_ITEM_JS a,DL_B_RETAIL_JS b where cast(b.bill_date as INT)>=%s and a.DL_B_RETAIL_ID=b.ID "



    deleteRetailJS="delete from DL_B_RETAIL_JS "
    deleteRetailitemJS = "delete from DL_B_RETAIL_ITEM_JS "
    deleteRetailPayItemJS = "delete from DL_B_RETAILPAY_ITEM_JS "
    deleteRetailSalesItemJS = "delete from DL_B_RETAILSALES_ITEM_JS "

    getRetailbyJS = "select * from DL_B_RETAIL where bill_date like '%s'  and STATUS=1 and ORDER_STATUS=1 "
    getRetailitembyJS = "select a.* from DL_B_RETAIL_ITEM a where a.DL_B_RETAIL_ID in %s "
    getRetailPayItembyJS = "select a.* from DL_B_RETAILPAY_ITEM a where a.DL_B_RETAIL_ID in %s "
    getRetailSalesItembyJS = "select a.* from DL_B_RETAILSALES_ITEM a where a.DL_B_RETAIL_ID in %s "

    getRetailbybilldate = "select * from DL_B_RETAIL where cast(bill_date as INT)>=%s  and STATUS=1 and ORDER_STATUS=1  "

    getRetailJSInfo="select * from %s where %s "
    deleteRetailJSInfo="delete from %s where %s "

    getRetailTotalamt="select sum(ifnull(sum_amt_actual,0)) as sum_amt from DL_B_RETAIL a where %s  and STATUS=1 and ORDER_STATUS=1 "

    getProInfoJS="select id,ecode,ename,pricelist from ps_c_pro where cast(pricelist as INT) <= %s limit 0,5 " #查询出某些价格范围内的商品

    getSkusByJS = """select a.id as BarCodeId,a.sku_ecode as BarCode,b.PS_C_PRO_ID as ProductId,b.cp_c_distrib_id as DistribId,'' as DistribidCode,'' as DistribidName,
               b.ps_c_brand_id as BrandId,'' as BrandCode,'' as BrandName, b.ecode as ProductCode,b.ename as ProductName,ifnull(b.txtdim3,'') as TxtDim3,ifnull(b.pricelist,0) as PriceList,
               ifnull(b.pricelower,0) as PriceLower,
               ifnull(b.proyear,-1) as Proyear,
               ifnull(b.numdim6,-1) as NumDim6,
               ifnull(b.largeclass,-1) as LargeClass,
               ifnull(b.sex,-1) as Sex,
               ifnull(b.prosea,-1) as Prosea,
               ifnull(b.promotiontype,-1) as PromotionType,
               ifnull(b.numdim5,-1) as NumDim5,
               ifnull(b.series,-1) as Series,
               ifnull(b.proband,-1) as Proband,
               ifnull(b.pronature,-1) as Pronature,
               ifnull(b.numdim8,-1) as NumDim8,
               ifnull(b.priceband,-1) as PriceBand,
               ifnull(b.numdim9,-1) as NumDim9,
               ifnull(b.numdim3,-1) as NumDim3,
               ifnull(b.numdim11,-1) as NumDim11,
               ifnull(a.ps_c_spec1obj_id,-1) as Spec1Id,ifnull(a.ps_c_spec2obj_id,-1) as Spec2Id,ifnull(b.fabdesc,'') as  Fabdesc,
               c.ecode as spec1ecode,c.ename as spec1ename, d.ecode as spec2ecode,d.ename as spec2ename   
               from ps_c_sku a,ps_c_pro b,ps_c_specobj c ,ps_c_specobj d
               where b.ecode = '%s' and  a.ps_c_pro_id=b.ID and c.id=a.ps_c_spec1obj_id and d.id=a.ps_c_spec2obj_id  order by  a.sku_ecode  """  # 根据条码查询商品详细信息

    selectBillNoListBlurry = "select BILL_NO from DL_B_RETAIL WHERE BILL_NO like '%s'"

if __name__ == '__main__':
    print(SqliteSql.getProInfo % '%rrrr')
    rr = (1, 2, 3)
    print(list(rr))
    tt = list(rr)
    print(tuple(tt))
