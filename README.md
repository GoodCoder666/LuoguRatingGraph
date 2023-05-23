# LuoguRatingGraph

洛谷 Rating 图表生成器。基于 Python 爬虫和 `pyecharts` 生成图表。

## 背景

5 月 22 日，洛谷添加了 Elo rating 机制，但是没有官方图表。所以做一个简易的图表生成器。

官方功能上线后会停止维护。

## 使用

```shell
git clone https://github.com/GoodCoder666/LuoguRatingGraph
cd LuoguRatingGraph
pip install -r requirements.txt
python3 main.py
```

安装依赖项后在根目录下运行 `main.py` 即可。需要提供自己的洛谷 cookie。

## 图表

程序运行后会自动生成 `rating.html` 图表文件。如需要调整大小，可修改程序 74，75 行的参数。