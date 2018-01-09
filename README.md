功能
1.自动分析
2.选择答案

使用方式
1.python start.py
2.输入5点击确认,自动分析
  输入1选择答案1,输入2选择答案2,输入3选择答案3

思路
1.adb命令截图
2.裁剪问题区域
3.百度ocr识别内容
4.selenium打开百度自动搜索

依赖
pip install baidu-aip
pip install pillow
pip install selenium

问题
只针对1080 * 1920的设备,其他设备需修改代码
多设备需优化