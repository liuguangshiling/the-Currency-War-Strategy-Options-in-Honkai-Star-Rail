

import pyautogui
import os
import time
from pyscreeze import ImageNotFoundException

# ===================== 配置项（根据实际情况修改） =====================
# 基础路径
# BASE_PATH = os.path.join(os.getcwd(), 'gametupian').replace('\\', '/')
BASE_PATH = os.path.join(os.getcwd(), 'gametupian').replace('\\', '/')
STRATEGY_PATH = os.path.join(BASE_PATH, 'strategy').replace('\\', '/')

# 图片路径常量
IMG_1 = os.path.join(BASE_PATH, '1.png')
IMG_2 = os.path.join(BASE_PATH, '2.png')
IMG_3 = os.path.join(BASE_PATH, '3.png')
IMG_4 = os.path.join(BASE_PATH, '4.png')
IMG_5 = os.path.join(BASE_PATH, '5.png')
IMG_7 = os.path.join(BASE_PATH, '7.png')
IMG_OVERHEAT = os.path.join(STRATEGY_PATH, 'jingjiyanzhongguore.png').replace('\\', '/')
IMG_HAPPY = os.path.join(STRATEGY_PATH, 'huanyuqiyue.png').replace('\\', '/')
# 新增：蓝海策略图片路径，需你自行截取游戏内的蓝海截图，命名为 lanhai.png 放入 strategy 文件夹
IMG_BLUEOCEAN = os.path.join(STRATEGY_PATH, 'lanhai.png')

# 识别通用配置
CONFIDENCE = 0.9  # 置信度，动态场景建议0.7-0.8
GRAYSCALE = True  # 开启灰度匹配，大幅提升动态场景识别率
RETRY_TIMES = 3  # 单次识别最大重试次数
RETRY_INTERVAL = 0.5  # 重试间隔（秒）

# 各图片的搜索区域（格式：(左, 上, 宽, 高)）
# 可通过 pyautogui.displayMousePosition() 实时获取鼠标坐标来确定
REGION_1 = (1300, 920, 600, 100)  # 建议改成1.png按钮实际所在区域
REGION_STRATEGY = (180, 190, 1520, 220)  # 策略弹窗的大致区域
REGION_3 = (640, 950, 60, 60)
REGION_7 = (880, 950, 400, 70)
REGION_NORMAL = (0, 0, 1920, 1080)  # 其他图片默认全屏，建议逐步细化


# ===================== 通用工具函数 =====================
def click_image(img_path, region=None, retries=RETRY_TIMES, interval=RETRY_INTERVAL):
    """识别图片并点击，找不到返回None，不会抛异常"""
    for _ in range(retries):
        try:
            center = pyautogui.locateCenterOnScreen(
                img_path,
                confidence=CONFIDENCE,
                grayscale=GRAYSCALE,
                region=region
            )
            if center is not None:
                pyautogui.click(center)
                return center
        except pyautogui.ImageNotFoundException:
            # 捕获PyAutoGUI外层的识别失败异常，静默重试
            pass
        time.sleep(interval)
    return None

def wait_image(img_path, timeout=10, region=None, interval=0.5):
    """等待图片出现，超时返回None，不会抛异常"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            center = pyautogui.locateCenterOnScreen(
                img_path,
                confidence=CONFIDENCE,
                grayscale=GRAYSCALE,
                region=region
            )
            if center is not None:
                return center
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(interval)
    return None


# def try_strategy_flow():
#     """
#     蓝海策略流程：找蓝海→选蓝海→判断随机策略
#     :return: 命中目标策略返回True，否则返回False
#     """
#     # ========== 第一步：检测并选择蓝海策略 ==========
#     # 第一次检测蓝海
#     blue_ocean = click_image(IMG_BLUEOCEAN, region=REGION_STRATEGY)
#     if not blue_ocean:
#         # 没找到蓝海，点击3.png刷新一次
#         if not click_image(IMG_3, region=REGION_3):
#             # 连刷新按钮都找不到，直接失败
#             return False
#         time.sleep(1.5)  # 等待界面刷新
#         # 刷新后第二次检测蓝海
#         blue_ocean = click_image(IMG_BLUEOCEAN, region=REGION_STRATEGY)
#         if not blue_ocean:
#             # 刷新后还是没有蓝海，失败
#             return False
#
#     # 找到蓝海，点击7.png确认，进入随机策略界面
#     click_image(IMG_7, region=REGION_7)
#     time.sleep(2)  # 等待新界面加载，可根据游戏速度调整
#
#     # ========== 第二步：判断随机出的策略 ==========
#     # 判断是不是目标策略1：经济严重过热
#     if click_image(IMG_OVERHEAT, region=REGION_STRATEGY):
#         click_image(IMG_7, region=REGION_7)  # 选中后确认
#         return True
#
#     # 判断是不是目标策略2：欢愉契约
#     # if click_image(IMG_HAPPY, region=REGION_STRATEGY):
#     #     click_image(IMG_7, region=REGION_7)  # 选中后确认
#     #     return True
#
#     # ========== 第三步：非目标策略，选中后返回False走兜底 ==========
#     # 界面只有一个策略，直接点击策略区域中心即可选中
#     strategy_x = REGION_STRATEGY[0] + REGION_STRATEGY[2] // 2
#     strategy_y = REGION_STRATEGY[1] + REGION_STRATEGY[3] // 2
#     pyautogui.click(strategy_x, strategy_y)
#     # click_image(IMG_7, region=REGION_7)  # 确认选择
#     return False

def try_strategy_flow():
    """
    尝试识别策略图片并执行结束流程
    :return: 成功返回True，失败返回False
    """
    # 第一轮：直接尝试识别策略图
    if click_image(IMG_OVERHEAT, region=REGION_STRATEGY):
        click_image(IMG_7, region=REGION_7)
        return True
    # if click_image(IMG_HAPPY, region=REGION_STRATEGY):
    #     click_image(IMG_7, region=REGION_7)
    #     return True

    # 第二轮：点击3.png后再尝试
    if not click_image(IMG_3, region=REGION_3):
        return False
    time.sleep(1.5)

    if click_image(IMG_OVERHEAT, region=REGION_STRATEGY):
        click_image(IMG_7, region=REGION_7)
        return True
    # if click_image(IMG_HAPPY, region=REGION_STRATEGY):
    #     click_image(IMG_7, region=REGION_7)
    #     return True

    # 都没找到
    return False


# ===================== 主业务逻辑 =====================
def main_loop():
    time.sleep(2.5)
    while True:
        time.sleep(2.5)

        # 识别1.png，一次识别复用结果（原代码识别了两次，优化为一次）
        center_1 = click_image(IMG_1, region=REGION_1)
        if center_1 is None:
            print("未找到1.png，跳过本轮")
            continue
        x1, y1 = center_1

        time.sleep(1)
        pyautogui.click(330, 445)
        time.sleep(0.5)
        pyautogui.click(center_1)
        time.sleep(1)
        pyautogui.click(center_1)
        time.sleep(7)
        pyautogui.click(x1 + 100, y1)
        time.sleep(3)
        pyautogui.click(x1 + 100, y1)
        time.sleep(5.5)

        # 尝试策略流程，成功则退出循环
        if try_strategy_flow():
            print("匹配到策略，结束循环")
            break

        # 兜底流程
        print("未匹配到策略，执行兜底操作")
        pyautogui.click(400, 540)
        time.sleep(0.5)
        click_image(IMG_7, region=REGION_7)
        time.sleep(7)
        click_image(IMG_4, region=REGION_NORMAL)
        time.sleep(0.75)
        click_image(IMG_5, region=REGION_NORMAL)
        time.sleep(3)

        # 连续点击2.png
        center_2 = click_image(IMG_2, region=REGION_NORMAL)
        if center_2 is not None:
            time.sleep(0.5)
            pyautogui.click(center_2)
            time.sleep(0.5)
            pyautogui.click(center_2)
        print("本轮兜底流程执行完毕")


if __name__ == "__main__":
    # 依赖检查：需要安装 opencv-python 和 pillow
    # pip install opencv-python pillow
    main_loop()