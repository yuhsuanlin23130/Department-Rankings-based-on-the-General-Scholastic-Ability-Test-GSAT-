

### 說明
104到108年度學測偏好分數排名。<br>
<p>令某年度申請入學有系所數目 N、學生數目 T，則假設對所有考生有一組偏好分數<span>$$a_1$$</span>~<span>$$a_n$$</span>，</p><p>使得某學生t選擇系所<span>\(d_1\)</span>的機率為 <span>$$P_{t_1}= \frac{ e^{a_{d_1}} }{ e^{a_{d_1}}+e^{a_{d_2}}+ \cdots +e^{a_{d_k}} }  $$</span>。</p>
		<p>為了估計這組偏好分數，我們使用 <span>$$ Cross Entropy Loss:$$</span><span>$$ \max \sum_{i=1}^N y_i log P_{t_i} - \lambda \sum_{i=1}^N {a_i}^2 $$</span>。</p>
<p> 將申請入學各考生一階通過的系所作為考生可能的選擇集合，以考生最後錄取的科系為考生最後的選擇，據此資料用stochastic gradient descent (sgd) 演算法最小化Cross Entropy Loss，計算各年度的偏好分數。</p>
<p>此分數不代表系所之間的優劣，而是考生的選擇及偏好。</p>
		<p>關於此模型可參考：</p>
		<ul>
			<li>
				<a href="https://en.wikipedia.org/wiki/Softmax_function">Softmax function</a>
			</li>
			<li>
				<a  href="https://en.wikipedia.org/wiki/Cross_entropy">Cross entropy</a>
			</li>
		</ul>

### 執行環境
Python3 (+ Jupyter Notebook)

### 目錄結構說明
爬蟲-108年學測交叉查榜.ipynb: 以selenium搭配Xpath從交叉查榜網站爬取爬取資料集
             
資料集
10\*fin/
* department_id10\*.csv
* school_choose10\*_fin.csv
* student10\*_fin.csv

資料前處理: 過濾備不上的考生、只有一個系所可選的考生等，以dict資料結構儲存考生與其正備取科系
* preprocess1_delba.py
* preprocess2_test.py

sgd 模型
* model.py
* model_tocsv.py

模型輸出檔案
10\*fin/
* department_dic_10\*.pkl
* student_choice_10\*.pkl
* student_dic_10\*.pkl
* model10\*_w_erlstp.npy: 各科系偏好分數

各科系排名結果整理
* department_rank10\*_erlstp (0.05) v.csv