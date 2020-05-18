#dict => store to .pkl     ## numpy array store to .npy
# sgd 前處理
import pandas as pd
import pickle


def build_dict_new(year):
# 有扣掉 只有一個系所可選而且真選了那間 的學生
	df1 = pd.read_csv('./%sfin/newstudent/student%s_fin.csv'  % (year,year), encoding="utf-8", dtype=str)
	#df1.dropna(inplace=True)               # 刪除連備取都沒有的
	df1 = df1[ df1['state'].notnull() ]
    
	df2 = pd.read_csv('./%sfin/school_choose%s_fin.csv' % (year,year), encoding="utf-8", dtype=str) 
	print(df1) 
    
	student = df2['student_id'].unique() # 沒有選擇學校的學生不算入
	snum = len(student)

	print(student, snum)

	department = pd.concat([df1['department_id'], df2['department_id']]).unique() # 有人填or有人選的系所 
	dnum = len(department)     # 2038(all) -> 2008 => 30 沒人選
	dnum2 = df2['department_id'].unique()
	for i in dnum2:
		if i not in department:   #check  
			print(i)
	print(len(df2['department_id'].unique()), dnum)  #1995:最終選擇 2008:有人填or有人選

	# create new department id
	print(len(department) )
	d_new = dict()
	for i in range(len(department)):
		d_new[department[i]] = i
	with open('%sfin/department_dic_%s.pkl' % (year,year), 'wb') as f:
		pickle.dump(d_new, f, pickle.HIGHEST_PROTOCOL)

	# create new student id
	sd_dict = dict()
	s_new = dict()
	snum = 0
	for i in range(len(student)):  #for each student
		choose_temp = df2.loc[df2['student_id'] == student[i]]
		choice_temp = df1.loc[df1['student_id'] == student[i]]
		if(not choice_temp.empty and choice_temp.shape[0] > 1): # 如果是沒選的才加入
			s_new[student[i]] = snum
			sd_dict[student[i]] = [choose_temp.iloc[0]['department_id']] # first: final select

			for j, row in choice_temp.iterrows():
				if(row['department_id'] != sd_dict[student[i]][0]): # 未選的科系
					sd_dict[student[i]].append(row['department_id'])
			snum += 1
		#else:
			#print(choice_temp.shape)    #(0, 6)   #(1, 6) #只有一個系所可選
            
	with open('%sfin/student_choice_%s.pkl' % (year,year), 'wb') as f:
    #with open('fin/student_choice_%s_minus1.pkl' % year, 'wb') as f:
		pickle.dump(sd_dict, f, pickle.HIGHEST_PROTOCOL)
	with open('%sfin/student_dic_%s.pkl'  % (year,year), 'wb') as f:
    #with open('fin/student_dic_%s_minus1.pkl' % year, 'wb') as f:
		pickle.dump(s_new, f, pickle.HIGHEST_PROTOCOL)
	print(len(s_new.keys()))  #38269
	pass


y = ['107']       
for i in y:
	build_dict_new(i)



