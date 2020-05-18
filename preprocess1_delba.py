# 刪除備不上的
import pandas as pd
from collections import defaultdict

def build_csv(year):
# 扣掉只有一個的/備取XX之後的
	df1 = pd.read_csv('./%sfin/student%s_fin.csv' % (year,year), encoding="utf-8", dtype=str)
	#df1.dropna(inplace=True)              # 刪除連備取都沒有的
	df1 = df1[ df1['state'].notnull() ]
	#df1.to_csv('temp.csv')
	df2 = pd.read_csv('./%sfin/school_choose%s_fin.csv' % (year,year), encoding="utf-8", dtype=str)
	print(df1)
 
# 外加備不理它，一樣當作有這個選擇
	maxstate = defaultdict(lambda: 0)   #某科系 最後錄取的學生 是備幾
	for index, row in df1.iterrows():    #for each student
		r = df2.loc[(df2['student_id']==row['student_id'])&(df2['department_id']==row['department_id'])]
		if(not r.empty): # 有學生選擇
			if('外加備' in row['state'] or '正' in row['state']):  #外加備 => -備
				continue
			elif('備' in row['state']):
				s = int(row['state'].split('備')[1])    #備幾
				if(s > maxstate[row['department_id']]):
					maxstate[row['department_id']] = s
			else:
				print(row)
		print(row['department_id'], maxstate[row['department_id']])  ###
        
	with open('./%sfin/newstudent/student%s_fin.csv'% (year,year), 'w', encoding="utf-8") as f:
		f.write('school_id,department_id,student_id,student_name,state,location1\n')
		for index, row in df1.iterrows():
			if('備' in row['state'] and '外加備' not in row['state']):
				print(s, maxstate[row['department_id']])
				s = int(row['state'].split('備')[1])
				if(s > maxstate[row['department_id']]): # 比最高錄取多的   ##########刪除備不上的
					continue
			f.write('%s,%s,%s,%s,%s,%s\n' % (row['school_id'],row['department_id'],row['student_id'],row['student_name'],row['state'],row['location1'])) 
                #正, 外加備, (一部分)備   
                
y = ['106']      #104-107:外加備, 108:-備  ,
for i in y:
 	build_csv(i)
     


