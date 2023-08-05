# Search From Plot  

## 概要  
散布図または箱ひげ図からデータを抽出することができます  
関数を呼び出すと、tkウィンドウが立ち上がります  
ウィンドウに表示された図上をドラッグすることで範囲を指定でき、  
範囲内にプロットされているデータをDataFrameで受け取ることができます  

jupyter notebook上で使うことを想定しています  

## インストール
```bash
$ pip install sfplot
```

## 使い方  
サンプルデータにirisデータセットを利用します  
```python
from sklearn.datasets import load_iris
import seaborn as sns
iris_dataset = sns.load_dataset('iris')
iris_dataset.head(10)
```

![](https://gitlab.com/kegeppa/public/raw/master/SearchFromPlot/.sample_images/image_01.png)  

### 対散布図からデータを抽出  
* pandas DataFrameと、散布図にしたいカラム名を引数にしてSearchFromPlotを起動します  
  引数x,yには数値(int, float)型のカラムのみ指定可能です
```python
import sfplot
search_result_df = sfplot.scatter(iris_dataset, x='sepal_length', y='sepal_width')
```
* ウィンドウが起動します  
![](https://gitlab.com/kegeppa/public/raw/master/SearchFromPlot/.sample_images/image_02.png)  

* 取得したいデータの範囲をドラッグします  
![](https://gitlab.com/kegeppa/public/raw/master/SearchFromPlot/.sample_images/image_03.png)  

* 「4件取得」と書かれたボタンを押下すると、ウィンドウが閉じ、  
  選択範囲内のレコードを抽出したDataFrameを返却します  
```python
search_result_df
```
![](https://gitlab.com/kegeppa/public/raw/master/SearchFromPlot/.sample_images/image_04.png)  

* 一度に複数回範囲を選択することも可能です  
![](https://gitlab.com/kegeppa/public/raw/master/SearchFromPlot/.sample_images/image_05.png)  
![](https://gitlab.com/kegeppa/public/raw/master/SearchFromPlot/.sample_images/image_06.png)  

### 箱ひげ図からデータを抽出  
* pandas DataFrameと、箱ひげ図にしたいカラム名を引数にしてSearchFromPlotを起動します  
  引数xにはobject型のカラム、引数yには数値(int, float)型のカラムのみ指定可能です  
```python
search_result_df = sfplot.boxplot(iris_dataset, x='species', y='sepal_width')
```
* ウィンドウが起動します  
![](https://gitlab.com/kegeppa/public/raw/master/SearchFromPlot/.sample_images/image_07.png)  

* 操作方法は対散布図と同様です  
