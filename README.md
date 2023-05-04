# lrc_auto_rename

自动将lrc字幕文件更改到与音频文件名称一致，自动搜索文件夹下的所有mp3和lrc时间轴，按照时间轴长度一一对应，更改lrc字幕到音频文件的名称。

## 注意

由于lrc时间轴没有包含时长的全部信息，因而只能用最后一个出现的字幕的时间与音频的时间做模糊对应，在本程序里采用排序后对应的方式。

### 字幕和音频的对应可能不准，建议使用该程序后检查。

## 程序截图
![](https://raw.githubusercontent.com/bai0012/lrc_auto_rename/main/demo.png?token=GHSAT0AAAAAACAPNCMSPFNUXHJOFWZ7RCDKZCTIT4A)

（如截图中音轨25和11的顺序就颠倒了，这是lrc字幕存在的问题）

## 如何使用

### 使用源代码程序

首先安装python，已在python3.10.11上测试

拉取该repo，并且安装Python依赖项：

```git
git clone https://github.com/bai0012/lrc_auto_rename
```

```Powershell
cd lrc_auto_rename
```

```python
pip install -r requirements.txt 
```

使终端处于项目文件夹的基础上，运行

```Powershell
python main.py
```

在窗口中选择要处理文件夹路径，等待处理完成即可。


(本程序在GPT 4指导下完成)
