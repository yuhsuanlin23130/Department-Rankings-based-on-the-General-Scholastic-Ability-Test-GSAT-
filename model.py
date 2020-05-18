#early stopping, at most 100000 epoch, learning rate = 0.05

import numpy as np  
import pickle
#import sys

#year = sys.argv[1]
#year = '107'

    
def main_func(year):
    # read department dict
    with open('%sfin/department_dic_%s.pkl'  % (year,year), 'rb') as f:
    	d_new = pickle.load(f)
    # read new student id dict
    with open('%sfin/student_dic_%s.pkl'  % (year,year), 'rb') as f:
    	s_new = pickle.load(f)
    with open('%sfin/student_choice_%s.pkl'  % (year,year), 'rb') as f:
    	sd_dict = pickle.load(f)
    #with open('fin/student_choice_state_106.pkl', 'rb') as f:
    #	s_state = pickle.load(f)
    print(sd_dict)
    print(len(s_new))
    print(len(sd_dict))
    
    snum = len(s_new.keys())
    dnum = len(d_new.keys())
    
    choice = np.zeros((snum, dnum)) # choices for all students
    choose = np.zeros((snum, dnum))  # final choice of student
    state = np.zeros((snum, dnum))  # 正備取係數
    
    
    for key, val in s_new.items():
    	index = [d_new[j] for j in sd_dict[key]]  #sd_dict[key]: the school ids of his choice
    	choice[val, index] = 1
    	choose[val, index[0]] = 1  #
    	#state[val, index] = s_state[key]
    
    print('fin create id', 'y: ', choose.shape, 'x: ', choice.shape)  #(38269,2033)

    indices = np.random.permutation(len(choose))  #randomly permute 0~len(choose)
    choose = choose[indices]  
    choice = choice[indices]
    state = state[indices]
    
    
    val = 0
    
    train_x = choice[val:]
    train_y = choose[val:]
    
    valid_x = choice[:val] #empty set
    valid_y = choose[:val]
    
    train_s = state[val:]
    valid_s = state[:val]
    
    sgd(train_y, train_x, 0.05, 100000, 0.00001, valid_y, valid_x, train_s, valid_s, year)  #learning rate, times,=100, lambda
    #adam(train_y, train_x, 0.05, 50, 0.00001, 0.9, 0.999, valid_y, valid_x)
    



def softmax(y): #y: vector  #for one student  #pt = [a1, 0, 0..., ]
	x = np.zeros(len(y))
	for i in range(len(y)):
		if y[i] != 0:
			x[i] = np.exp(y[i]) / np.sum(np.exp(y[y != 0]), axis=0)
	return x     #1*N, all possible choice of one student


def sgd(y, x, rate, t, l, valid_y, valid_x, train_s, valid_s, year): #rate: learning rate, t: times,=100
	w = np.zeros(len(x[0]))  #N    #initialize  # numpy array => store to .npy
	b1 = 0.01 # 正備取係數
	early_stopping = 20                ##########
	count = 0      # early stopping count
	last = 0      #last entropy loss
	best = np.zeros(len(x[0]))       #store the best w so far
    
    
	train_s = b1 * train_s #state

	print(x.shape, y.shape, w.shape)
	for i in range(t): #500 epochs
		for j, sample in enumerate(x):  #for each student #0,row1  1,row2  2,row3 
			a_t = sample * (w + train_s[j]) # a_t = [1, 0, 0..., ] #[w + state]
			pt = softmax(a_t)
			#print(pt, np.sum(pt))

			y_index = np.argmax(y[j]) #最大值之索引 (第一次出現), true label index    # the school chosen
			grad_w = -1 * pt
			grad_w[y_index] += 1  #if i == d1
			grad_w = -grad_w + l * w # regularize, l = lambda

			w -= rate * grad_w

        # w is computed
        #update loss after each epoch
		L, acc = loss(y, x, w, l, train_s)    # L < 0   # entropy loss: minimize -L
		#val_L, val_acc = loss(valid_y, valid_x, w, l, valid_s)
		val_L, val_acc = 0, 0
		print('epoch: ', i, 'loss: ', -L, 'train-acc: ', acc, '| val-loss: ', -val_L, 'val-acc: ', val_acc)
        
        
		if(-L < last):              #if loss < last loss
			count = 0
			best = w                #####
		else:
			print('no improve')      #if entropy loss continuously not improve...
			count += 1
		last = -L
		if(count >= early_stopping):
			break
        
	np.save('%sfin/model%s_w_erlstp.npy' % (year,year), best)    #最終排名結果 (by w)  ---end
    #np.save('npy/model%s_w.npy' % year, w) 
	return w


def loss(y, x, w, l, s): #y: matrix TxN, s: state
	acc = 0
	L = 0     # entropy loss: -L
	for i, sample in enumerate(x): #for each students
		y_index = np.argmax(y[i])  #最大值之索引    # the school he choose
		pt = sample * (w + s[i])
		pt = softmax(pt)
		pt = np.clip(pt, 1e-12, None)  #if pt[.]<1e-12 => pt[.]=1e-12
        
		L += np.log(pt[y_index])       # np.log(pt[y_index]) < 0

		# for accuracy
		y_predict = np.argmax(pt)  #目前預測他會選的學校 (by softmax)
		if(y_predict == y_index):  # y_index:真正選的學校
			acc += 1
	acc /= len(y)    #len(y):T
	L /= len(y)
	L -= 0.5 * l * np.sum(w ** 2)  #regularization
	return L, acc


y = ['104','105','106','107']       #104 105
for i in y:
    main_func(i)
    
    
