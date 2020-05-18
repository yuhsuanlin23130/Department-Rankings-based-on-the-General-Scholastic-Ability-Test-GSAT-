# open department_id108.csv, npy/model108_w.npy
# wirte 系所資訊 + 偏好係數 to fin/department_rank.csv 
    #(school_name,department_name,department_id,score)
import numpy as np
import pickle
import pandas as pd

def write_to_csv(year):
    #score = np.load('npy/model108_w.npy')
    score = np.load('%sfin/model%s_w_erlstp.npy'  % (year,year))
    score = np.round(score, 6)
    df1 = pd.read_csv('%sfin/department_id%s.csv'  % (year,year), encoding="utf-8", dtype=str)
    #df1 = df1.loc[df1['year'] == '108']
    print(df1['department_id'])
    with open('%sfin/department_dic_%s.pkl' % (year,year), 'rb') as f:
    	d_dict = pickle.load(f)
    
    all_list = []
    with open('%sfin/department_rank%s_erlstp.csv' % (year,year), 'w', encoding="utf-8") as f:
    	f.write('school_name,department_name,department_id,score\n')
    	for key, val in d_dict.items():
    		print(key)
    		row = df1.loc[df1['department_id']==key]
    		row = row.iloc[0]
    		all_list.append([row['school_name'],row['department_name'],key,score[val]])
    	all_list = sorted(all_list, key=lambda x:x[3], reverse=True)
    	for i in all_list:
    		line = '%s,%s,%s,%s\n' % (i[0],i[1],i[2],i[3])
    		f.write(line)


y = ['108']        #'104','105',
for i in y:
	write_to_csv(i)

