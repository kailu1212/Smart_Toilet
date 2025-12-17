"""
磁簧開關（Reed Switch）感測器模組
用於偵測馬桶蓋開合狀態
"""
from gpiozero import DigitalInputDevice
from typing import Callable, Optional


class ReedSwitch:
    """磁簧開關感測器類別"""
    
    def __init__(self, pin: int):
        """
        初始化磁簧開關
        
        Args:
            pin: GPIO 針腳號碼
        """
        self.pin = pin
        self.device = DigitalInputDevice(pin)
        print(f"🧲 磁簧開關已初始化於 GPIO {pin}")
        
    @property
    def value(self) -> int:
        """
        取得當前狀態值
        
        Returns:
            0: LOW (磁鐵靠近，蓋子放下)
            1: HIGH (磁鐵遠離，蓋子抬起)
        """
        return self.device.value
    
    def is_closed(self) -> bool:
        """
        檢查磁簧開關是否閉合（蓋子是否放下）
        
        Returns:
            True: 蓋子放下（磁鐵靠近開關，LOW）
            False: 蓋子抬起（磁鐵遠離開關，HIGH）
        """
        return self.device.value == 0
    
    def is_open(self) -> bool:
        """
        檢查磁簧開關是否開啟（蓋子是否抬起）
        
        Returns:
            True: 蓋子抬起（HIGH）
            False: 蓋子放下（LOW）
        """
        return self.device.value == 1
    
    def wait_for_open(self, timeout: Optional[float] = None):
        """
        等待蓋子開啟
        
        Args:
            timeout: 超時時間（秒），None 表示無限等待
        """
        print("等待蓋子開啟...")
        self.device.wait_for_active(timeout=timeout)
        print("偵測到蓋子開啟")
    
    def wait_for_close(self, timeout: Optional[float] = None):
        """
        等待蓋子關閉
        
        Args:
            timeout: 超時時間（秒），None 表示無限等待
        """
        print("等待蓋子關閉...")
        self.device.wait_for_inactive(timeout=timeout)
        print("偵測到蓋子關閉")
    
    @property
    def when_activated(self):
        """蓋子開啟（HIGH）時的回調函數"""
        return self.device.when_activated
    
    @when_activated.setter
    def when_activated(self, callback: Callable):
        """設定蓋子開啟時的回調函數"""
        self.device.when_activated = callback
    
    @property
    def when_deactivated(self):
        """蓋子關閉（LOW）時的回調函數"""
        return self.device.when_deactivated
    
    @when_deactivated.setter
    def when_deactivated(self, callback: Callable):
        """設定蓋子關閉時的回調函數"""
        self.device.when_deactivated = callback
    
    def cleanup(self):
        """清理資源"""
        self.device.close()
        print("HW: 磁簧開關已清理。")

