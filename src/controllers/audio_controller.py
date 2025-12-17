"""
音效播放控制器
用於播放提醒音效
"""
import os
from pathlib import Path
from pygame import mixer, error


class AudioController:
    """音效播放控制器"""
    
    def __init__(self):
        """初始化音效系統"""
        try:
            if not mixer.get_init():
                mixer.init(44100, -16, 2)
            print("HW: Pygame Mixer 音訊系統已初始化。")
        except Exception as e:
            print(f"FATAL: 初始化 Pygame Mixer 失敗: {e}")
            raise
    
    def play_sound(self, filename: str, blocking: bool = True) -> bool:
        """
        播放音效
        
        Args:
            filename: 音效檔案路徑
            blocking: 是否等待播放完畢（預設 True）
        
        Returns:
            bool: 播放成功返回 True，失敗返回 False
        """
        try:
            if not os.path.exists(filename):
                print(f"❌ 錯誤: 找不到音效檔案 '{filename}'")
                return False
            
            print(f"🔊 正在播放: {filename}")
            
            # 載入並播放音效
            mixer.music.load(filename)
            mixer.music.play()
            
            if blocking:
                # 等待播放完成
                while mixer.music.get_busy():
                    mixer.time.Clock().tick(10)
            
            print(f"✅ 音效播放完成: {filename}")
            return True
            
        except error as e:
            print(f"❌ Pygame 錯誤: {e}")
            return False
        except Exception as e:
            print(f"❌ 播放音效時發生錯誤: {e}")
            return False
    
    def play_alert1(self, sound_file: str) -> bool:
        """
        播放階段1提醒音效
        
        Args:
            sound_file: 音效檔案路徑
            
        Returns:
            bool: 播放成功返回 True
        """
        print("🎵 [階段1] 播放提醒音效...")
        return self.play_sound(sound_file, blocking=True)
    
    def play_alert2(self, sound_file: str) -> bool:
        """
        播放階段2提醒音效
        
        Args:
            sound_file: 音效檔案路徑
            
        Returns:
            bool: 播放成功返回 True
        """
        print("🎵 [階段2] 播放嚴重提醒音效...")
        return self.play_sound(sound_file, blocking=True)
    
    def stop(self):
        """停止所有音效"""
        mixer.stop()
        print("已停止所有音效")
    
    def cleanup(self):
        """清理音效系統"""
        try:
            mixer.quit()
            print("HW: Pygame Mixer 已清理。")
        except Exception as e:
            print(f"清理 Pygame Mixer 時發生錯誤: {e}")

