import psutil
import pystray
from PIL import Image, ImageDraw, ImageFont
import time
from threading import Thread

def create_battery_image(percentage):
    # 增大图像尺寸到96x96
    image = Image.new('RGBA', (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制背景方形
    if percentage <= 20:
        bg_color = 'red'
    elif percentage <= 50:
        bg_color = 'yellow'
    else:
        bg_color = 'green'
    
    # 调整方形大小，保持适当边距
    draw.rectangle([6, 6, 90, 90], fill=bg_color)
    
    try:
        # 将字体大小增加到64
        font = ImageFont.truetype("msyh.ttc", 64)
    except:
        font = ImageFont.load_default()
    
    # 计算文字位置使其居中
    text = f"{percentage}"
    text_width = draw.textlength(text, font=font)
    text_height = 64  # 调整估计字体高度以匹配新的字体大小
    
    x = (96 - text_width) // 2
    y = (96 - text_height) // 2
    
    # 绘制文字描边来实现加粗效果
    draw.text((x-2, y), text, font=font, fill='black')
    draw.text((x+2, y), text, font=font, fill='black')
    draw.text((x, y-2), text, font=font, fill='black')
    draw.text((x, y+2), text, font=font, fill='black')
    draw.text((x-1, y-1), text, font=font, fill='black')
    draw.text((x+1, y-1), text, font=font, fill='black')
    draw.text((x-1, y+1), text, font=font, fill='black')
    draw.text((x+1, y+1), text, font=font, fill='black')
    
    # 绘制主文字，改为黑色
    draw.text((x, y), text, font=font, fill='black')
    
    return image

def update_battery(icon):
    while True:
        try:
            battery = psutil.sensors_battery()
            if battery:
                percentage = int(battery.percent)
                icon.icon = create_battery_image(percentage)
                icon.title = f"电池电量: {percentage}%"
        except Exception as e:
            print(f"更新电池信息时出错: {e}")
        time.sleep(60)

def exit_action(icon):
    icon.stop()    # 停止图标
    
def main():
    # 创建初始图标
    battery = psutil.sensors_battery()
    initial_percentage = int(battery.percent) if battery else 0
    
    icon = pystray.Icon(
        "battery",
        create_battery_image(initial_percentage),
        title=f"电池电量: {initial_percentage}%",
        menu=pystray.Menu(    # 添加菜单项
            pystray.MenuItem("退出", exit_action)
        )
    )
    
    # 启动更新线程
    Thread(target=update_battery, args=(icon,), daemon=True).start()
    
    # 运行图标
    icon.run()

if __name__ == "__main__":
    main()