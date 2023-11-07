import re

def extract_table_name_from_sql(sql_str):
    # remove the /* */ comments
    q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql_str)

    # remove whole line -- and # comments
    lines = [line for line in q.splitlines() if not re.match("^\s*(--|#)", line)]

    # remove trailing -- and # comments
    q = " ".join([re.split("--|#", line)[0] for line in lines])

    # split on blanks, parens and semicolons
    tokens = re.split(r"[\s)(;]+", q)

    # scan the tokens. if we see a FROM or JOIN, we set the get_next
    # flag, and grab the next one (unless it's SELECT).

    result = set()
    get_next = False
    for token in tokens:
        if get_next:
            if token.lower() not in ["", "select"]:
                result.add(token)
            get_next = False
        get_next = token.lower() in ["from", "join"]

    return result

if __name__ == '__main__':
    sql_str = """
    SELECT 
u.ID AS OPERATOR_ID                  -- 操作人员ID
,u.Name_	AS OPERATOR_NAME           -- 机手姓名
,u.IDNumber AS OPERATOR_IDCRAD	     -- 身份证号
,u.Phone AS OPERATOR_PHONE	         -- 手机号
,u.Nature	AS OPERATOR_NATAURE        -- 人员属性
,u.NatureCode	AS OPERATOR_NATURE_CODE-- 人员属性编码
,u.BelongProject	AS MANAGE_ORG      -- 所属组织
,o2.EASID	AS MANAGER_ORG_ID          -- 所属组织ID
,u.UserOrg AS USE_ORG	               -- 在用组织（进退场）
,o.EASID	AS USE_ORG_ID              -- 在用组织ID（进退场）
,o.EASCODE	AS USE_ORG_CODE          -- 在用组织编码（进退场）
,u.OpDeviceType AS OPERA_DEVICE_TYPE	-- 可操作性设备类型
,u.OpDeviceTypeIDS AS OPERADEVICE_TYPEIDS	-- 可操作性设备类型IDS（Code）
,case when equ.SPECIALEQUIPMENTCODE is null then '0' else equ.SPECIALEQUIPMENTCODE end AS IS_SPEC_EQU -- 是否特征设备
,CASE WHEN SignTimes >= 1 THEN 1 ELSE 0 END IS_SIGN  -- 是否安全操作规程交底
,TO_CHAR(SYSDATE,'yyyyMM') AS PERIOD_MONTH
,TO_CHAR(SYSDATE,'yyyyMMdd') AS PERIOD_DAY
from EQU.T_ODS_SB_OPERATOR u
LEFT JOIN EQU.T_ODS_MAININFOORG o ON u.UserOrgID = o.BIZID
LEFT JOIN EQU.T_ODS_MAININFOORG o2 ON u.BelongProjectID = o2.BIZID
LEFT JOIN EQU.T_ODS_LQ_EQU_USEREQURELATION ul ON ul.USERID=u.ID AND ul.IsEnable =1 AND ul.IsMain = 1
LEFT JOIN EQU.T_ODS_MAININFODEVICEINFO equ ON equ.ID=ul.EQUID
WHERE u.IsEnable = 1
AND u.UserOrgID IS NOT NULL 
AND u.UserOrg not like '%本部' 
AND u.UserOrg not like '%中心' 
AND u.UserOrg not like '%租赁站'SELECT 
	T.DEVICE_ID,
	T.PRESPOT_CHECKSTATE,
	T.PRESPOT_CHECKTIME,
	DEVICE.SPECIALEQUIPMENT AS IS_SPECIAL_EQU,
	DEVICE.MANAGEMENTORGCODE AS MANAGE_ORG_CODE,
	DEVICE.MANAGEMENTORG AS MANAGE_ORG,
	DEVICE.DEVICENATURE AS DEVICE_NATURE,
	CP.COMPANY_ID,
	CP.COMPANY_CODE,
	CP.ORG_ID
FROM (
	SELECT 
		DISTINCT 
		SUBSTR(bc.CREATORDATE,0,10) AS PRESPOT_CHECKTIME,
		ORG.EASID AS ORG_ID,
		bc.BELONGDEVICEID AS DEVICE_ID,
		bc.ISPASSCHECK AS PRESPOT_CHECKSTATE
	FROM EQU.T_ODS_LQ_EQU_BEFOREWORKCHECK bc 
	LEFT JOIN (SELECT EASID,BizID FROM EQU.T_ODS_MainInfoOrg WHERE IsEntity = '是' AND SUBSTR(NAME_, LENGTH(NAME_)-1, LENGTH(NAME_)) != '中心'
    AND SUBSTR(NAME_, LENGTH(NAME_)-1, LENGTH(NAME_))  != '本部') ORG ON bc.USEORGBIZID=ORG.BizID  -- 组织表
    WHERE ORG.EASID IS NOT NULL 
    AND IsEnable=1
	ORDER BY SUBSTR(bc.CREATORDATE,0,10),ORG.EASID,bc.BELONGDEVICEID,bc.ISPASSCHECK
) T LEFT JOIN EQU.T_ODS_MAININFODEVICEINFO DEVICE ON T.DEVICE_ID=DEVICE.ID
LEFT JOIN DWD_HR.T_DWD_COMPANY CP ON CP.ORG_ID=T.ORG_ID

UNION ALL 

SELECT 
	T.DEVICE_ID,
	T.PRESPOT_CHECKSTATE,
	T.PRESPOT_CHECKTIME,
	DEVICE.SPECIALEQUIPMENT AS IS_SPECIAL_EQU,
	DEVICE.MANAGEMENTORGCODE AS MANAGE_ORG_CODE,
	DEVICE.MANAGEMENTORG AS MANAGE_ORG,
	DEVICE.DEVICENATURE AS DEVICE_NATURE,
	'00000000-0000-0000-0000-000000000000CCE7AED4' AS COMPANY_ID,
	'01' AS COMPANY_CODE,
	'00000000-0000-0000-0000-000000000000CCE7AED4' AS ORG_ID
FROM (
	SELECT 
		DISTINCT 
		SUBSTR(bc.CREATORDATE,0,10) AS PRESPOT_CHECKTIME,
		ORG.EASID AS ORG_ID,
		bc.BELONGDEVICEID AS DEVICE_ID,
		bc.ISPASSCHECK AS PRESPOT_CHECKSTATE
	FROM EQU.T_ODS_LQ_EQU_BEFOREWORKCHECK bc 
	LEFT JOIN (SELECT EASID,BizID FROM EQU.T_ODS_MainInfoOrg WHERE IsEntity = '是' AND SUBSTR(NAME_, LENGTH(NAME_)-1, LENGTH(NAME_)) != '中心'
    AND SUBSTR(NAME_, LENGTH(NAME_)-1, LENGTH(NAME_))  != '本部') ORG ON bc.USEORGBIZID=ORG.BizID  -- 组织表
    WHERE ORG.EASID IS NOT NULL 
    AND IsEnable=1
	ORDER BY SUBSTR(bc.CREATORDATE,0,10),ORG.EASID,bc.BELONGDEVICEID,bc.ISPASSCHECK
) T LEFT JOIN EQU.T_ODS_MAININFODEVICEINFO DEVICE ON T.DEVICE_ID=DEVICE.ID


       """
    # tuples = ('success', 'C://')
    # print(tuples[0])
    sql_tables = extract_table_name_from_sql(sql_str)
    for item in sql_tables:
        print('select count(*) from ' + item + ';')
    print(sql_tables)

    url_re = r"!\[.*?\]\((.*?)\)"
    str_s = r"""
    ![](./res/python-ipython.png)
    ![123](http://localhost/res/python-ipython.png)
    #### Sublime Text - 高级文本编辑器
    
    ![](./res/python-sublime.png)
    """
    result = re.findall(url_re, str_s, flags=0)
    img_htt_p = r"!\[.*?\]\((http.*?)\)"
    img_htt_path = r"!\[.*?\]\((.*?)\)"
    for img in result:
        if img.startswith('http'):
            print('http开头')
        elif img.startswith('./') or img.startswith('/') or img.startswith('\\'):
            folders = img.split('/')
            # if folders[0] == '.':
            #     # for folder in folders:
            #     #     print(folder)
            #     for index in range(len(folders)):
            #         if index == 0:
            #             pass
            #         elif index == len(folders)-1:
            #             pass
            #         else:
            #             print(folders[index])

        else:
            print('未知路径')



