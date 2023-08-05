# VoiceAI Python SDK 兼测试脚本

该项目封装了Voice AI声纹云HTTP接口，可做Python SDK。

项目结构：

```
--- pyvoiceai   Python SDK核心代码

--- example        SDK具体功能测试示例
    --- asr  语音转文字
    --- asv  活体检测
    --- vpr  声纹验证
    --- dia  人声分割
    --- test   语音云功能测试示例
    
--- demo        定制测试
    -- bank 民生银行VPR定制测试
    -- bank_asr  民生银行ASR定制测试
    -- bank_help POC测试格式转换为民生银行格式
    -- weibin_asr 定制脚本

--- poc         POC测试脚本

```


## 一.环境配置

1. 测试环境： `Python3.5+` (Python版本越高越好), 兼容Python2.7

2. 安装SDK：

```
pip install -U pyvoiceai
```

也可直接安装：

```
python setup.py install
```


## 二.Example

进入`example`.

### (1).声纹批量注册和验证:VPR测试

每个人的口腔和喉结构造不同,导致声音的差异性，此差异性可通过声纹来进行识别，借此可应用于防伪，身法识别等场景。

参数说明如下：

```
@author VoiceAI
@desc VPR声纹注册验证批量测试, 验证音频与同个组的所有用户的注册声纹进行比对
        此脚本可以计算1：1 EER等错误率, 1:N Top1/Top10命中率
@date 20180928

@usage
    >> python vpr_batch_test.py model_short_cn_dnn ./wav ./output_model_short_cn_dnn ./report_model_short_cn_dnn 16000 3 e

    args:
        model_short_cn_dnn		    16K算法模型
        ./wav	                    测试文件路径，内部结构为：[[对象文件夹] -> [register][verify]]，register为注册源文件夹，verify为验证源文件夹，详见例子
        ./output_model_short_cn_dnn	结果分数输出路径
        ./report_model_short_cn_dnn	简单测试报告输出路径
        16000                       采样率
        3                           线程数
        e                           e表示计算EER,如果是t则计算TOP,et两者都运算
```

快速运行：

```
./vpr_batch_short_cn_dnn_test.sh
```

### (2).音频活体检测:ASV测试

检测声音是否是没有经过二次处理的，可应用于防录音攻击。

参数说明如下：

```
@author VoiceAI
@desc ASV活体检测批量测试： 附计算EER
@date 20180928

@usage
    >> python asv_test.py  model_short_cn_dnn ./wav ./output_model_short_cn_dnn ./report_model_short_cn_dnn 16000

    args:
        model_short_cn_dnn		16K算法模型
        ./wav	                测试文件路径
        ./output_model_short_cn_dnn	结果输出路径
        ./report_model_short_cn_dnn	简单测试报告输出路径
        16000                       采样率
```

快速运行：

```
./asv_test.sh
```

### (3).人声分割处理:DIA测试

音频可能夹杂着不同的声音，需要进行声音分离。

原理：

已知`./wav`文件夹下有若干音频, 处理后会生成不同的子文件夹对应相应的音频。

参数说明如下：

```
@author VoiceAI
@desc DIA人声分割批量测试, 该脚本可以连续工作，每完成一个音频切割将会加一把完成锁
@date 20180928

@usage
    >> python dia_test.py  model_common_short ./wav ./output_model_common_short ./report_model_common_short 8000

    args:
        model_common_short		算法模型
        ./wav	                测试文件路径
        ./output_model_common_short	结果输出路径
        ./report_model_common_short	简单测试报告输出路径
        8000                        采样率
```

快速运行：

```
./dia_test.sh
```

### (4).语音识别处理:ASR测试

说明如下：

```
    # 16000 			表示采样率
    # MODEL_ASR_POWER 	是电力模型名，常量定义在sdk中
    # File_Name 		需要识别的音频
    # 800 				间歇时间，识别是实时识别，发送间歇800毫秒，当服务器性能良好，可以设置100毫秒
    txt = c.asr(16000, MODEL_ASR_POWER, File_Name, 100)
```

快速运行：

```
python asr_demo.py ./asrtxt.wav
```

## 三. POC测试

```
T1-T4 依赖 vpr_batch_test.py   声纹注册验证相关
T5-T6 依赖 asv_test.py         活体检测相关
T7    依赖 dia_test.py         人声分割相关
```

见[poc说明](/poc/script/readme.txt)，执行请在命令行运行`*.bat`

## 四. 定制化测试

民生银行测试见:

1. [声纹识别验证测试](/demo/bank/readme.txt)
2. [语音识别测试](/demo/bank_asr/readme.txt)

其他测试：

1. [模拟录音ASR](/demo/weibin_asr/asr_diy.py)

```
#    # 每次发送32000个字节，可自己调节
#    python asr_diy.py  ./asr.wav 32000
```


# 如何发布PYPI包

编辑`setup.py`修改`Version = '1.3.3'`：

```
python setup.py publish
```


