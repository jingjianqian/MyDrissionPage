import re

from githubMd2Blog.MyFileUtil import MyFileUtil


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
    my_file_util = MyFileUtil('E:\\tiktok')
    files = my_file_util.list_folder_files()
    print(files)
    sql_str = """
    	SELECT 
	T1.PERIOD_MONTH AS PERIOD,
	T1.MATER_NAME,
	ROUND(T1.IN_TOTAL/10000,2) AS IN_TOTAL,
	ROUND(T1.OUT_TOTAL/10000,2) AS OUT_TOTAL,
	CASE WHEN T2.STOCK_TOTAL IS NULL THEN 0 ELSE ROUND(T2.STOCK_TOTAL/10000,2) END AS STOCK_TOTAL
FROM (
	SELECT 
		P.PERIOD_MONTH,
		IOC.COMPANY_CODE,
		IOC.MATER_NAME,
		CASE WHEN SUM(IOC.IN_TOTAL) IS NULL THEN 0 ELSE ROUND(SUM(IOC.IN_TOTAL),2) END AS IN_TOTAL,
		CASE WHEN SUM(IOC.OUT_TOTAL) IS NULL THEN 0 ELSE ROUND(SUM(IOC.OUT_TOTAL),2)  END AS OUT_TOTAL
	FROM DWD_EQU.T_DWD_MATER_INOUT_COUNT IOC
	LEFT JOIN DW_EQU.T_DW_EQU_PERIOD P ON  IOC.PERIOD_DAY =P.PERIOD_DAY 
	WHERE 1=1 
    AND P.PERIOD_MONTH >= %{ :STARTTIME }
    AND P.PERIOD_MONTH <= %{ :ENDTIME }
    AND IOC.COMPANY_CODE = %{ :COMPANY_ID }
	GROUP BY P.PERIOD_MONTH,IOC.COMPANY_CODE,IOC.MATER_NAME
) T1 LEFT JOIN (
	SELECT 
		PERIOD_MONTH,
		MATER_NAME,
		STOCK_TOTAL,
		COMPANY_CODE
	FROM (
		SELECT 
			P.PERIOD_MONTH,
			SC.PERIOD_DAY,
			SC.MATER_NAME,
			SC.STOCK_TOTAL AS STOCK_TOTAL,
			SC.COMPANY_CODE,
			ROW_NUMBER() OVER(PARTITION BY P.PERIOD_MONTH,SC.MATER_NAME ORDER BY SC.PERIOD_DAY DESC) AS RN
		FROM (
			SELECT 
				PERIOD_DAY,
				MATER_NAME,
				COMPANY_CODE,
				CASE WHEN SUM(STOCK_TOTAL) IS NULL THEN 0 ELSE ROUND(SUM(STOCK_TOTAL),2) END AS STOCK_TOTAL
			FROM DWD_EQU.T_DWD_MATER_STOCK_COUNT SC
			GROUP BY PERIOD_DAY,MATER_NAME,COMPANY_CODE
		) SC
		LEFT JOIN DW_EQU.T_DW_EQU_PERIOD P ON  SC.PERIOD_DAY = P.PERIOD_DAY 
		WHERE 1=1 
        AND P.PERIOD_MONTH >= %{ :STARTTIME }
        AND P.PERIOD_MONTH <= %{ :ENDTIME }
				AND SC.COMPANY_CODE = %{ :COMPANY_ID }
	    AND SC.STOCK_TOTAL !=0 
	) T WHERE RN=1
) T2 ON (T1.PERIOD_MONTH=T2.PERIOD_MONTH AND T1.MATER_NAME=T2.MATER_NAME AND T1.COMPANY_CODE = T2.COMPANY_CODE)
       """
    # tuples = ('success', 'C://')
    # print(tuples[0])
    # sql_tables = extract_table_name_from_sql(sql_str)
    # for item in sql_tables:
    #     print('select count(*) from ' + item + ';')
    # print(sql_tables)

    url_re = r"!\[.*?\]\((.*ipython.*?)\)"
    str_s = r"""
    ![](./res/python-ipython.png)
    ![123](http://localhost/res/python-ipython.png)
    #### Sublime Text - 高级文本编辑器
    
    ![](./res/python-sublime.png)
    """
    result = re.findall(url_re, str_s, flags=0)
    print(1)
    print(result)
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



