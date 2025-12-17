"""
伺服馬達控制器模組
用於輔助馬桶蓋落下
"""
import RPi.GPIO as GPIO
from time import sleep


class ServoController:
    """SG90 伺服馬達控制器（使用 PWM 控制）"""
    
    def __init__(self, pin: int, duty_rest: float, duty_push: float, 
                 move_time: float, stabilize_time: float, push_hold_time: float):
        """
        初始化伺服馬達
        
        Args:
            pin: GPIO 針腳號碼
            duty_rest: 靜止角度的 PWM 佔空比
            duty_push: 推動角度的 PWM 佔空比
            move_time: 馬達轉動時間（秒）
            stabilize_time: 馬達啟動後穩定時間（秒）
            push_hold_time: 馬達推動角度後停留時間（秒）
        """
        self.pin = pin
        self.duty_rest = duty_rest
        self.duty_push = duty_push
        self.move_time = move_time
        self.stabilize_time = stabilize_time
        self.push_hold_time = push_hold_time
        
        # 設定 GPIO 模式
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
        # 建立 PWM 實例 (50Hz)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)
        
        print(f"⚙️ 伺服馬達已初始化於 GPIO {pin}")
        print(f"   靜止角度: {duty_rest}% | 推動角度: {duty_push}% | 停留時間: {push_hold_time}秒")
    
    def _change_angle(self, duty: float):
        """
        內部函式：變更 PWM 佔空比
        
        Args:
            duty: PWM 佔空比
        """
        self.pwm.ChangeDutyCycle(duty)
        sleep(self.move_time)
        
    def push_lid_down(self):
        """
        控制伺服馬達執行輕推落蓋的動作
        """
        print("⚙️ 馬達動作: 開始輕推落蓋...")
        
        try:
            # 啟動 PWM
            self._change_angle(self.duty_rest)
            sleep(self.stabilize_time)
            
            # 推動到指定角度
            print(f"   → 推動至 {self.duty_push}% 角度...")
            self._change_angle(self.duty_push)
            
            # 停留指定時間
            print(f"   → 維持角度 {self.push_hold_time} 秒...")
            sleep(self.push_hold_time)
            
            # 回到靜止位置
            print(f"   → 回到靜止位置 {self.duty_rest}%...")
            self._change_angle(self.duty_rest)
            
            # 停止 PWM 訊號
            self.pwm.ChangeDutyCycle(0)
            
            print("✅ 馬達動作完成！")
            
        except Exception as e:
            print(f"❌ 伺服馬達操作失敗: {e}")
    
    def cleanup(self):
        """清理 GPIO 資源"""
        try:
            if self.pwm:
                self.pwm.stop()
            print("HW: 伺服馬達已清理。")
        except Exception as e:
            print(f"清理伺服馬達時發生錯誤: {e}")

