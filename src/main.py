"""
SmartLid 主程式
智慧馬桶蓋提醒系統核心控制程式
"""
import sys
import threading
from datetime import date
from signal import pause, signal, SIGINT

# 導入配置
from config import Config

# 導入各模組控制器
from controllers.audio_controller import AudioController
from controllers.servo_controller import ServoController
from sensors.reed_switch import ReedSwitch
from services.line_messaging import LineMessagingService


class SmartLidController:
    """SmartLid 主控制器"""
    
    def __init__(self):
        """初始化 SmartLid 控制器"""
        # 狀態變數
        self.countdown_timer = None
        self.is_countdown_active = False
        self.daily_alert_count = 0
        self.last_reset_date = date.today()
        
        # 初始化硬體模組
        self._init_hardware()
    
    def _init_hardware(self):
        """初始化所有硬體模組"""
        try:
            # 1. 初始化音效控制器
            print("\n[初始化] 載入音效系統...")
            self.audio = AudioController()
            
            # 2. 初始化磁簧開關
            print("\n[初始化] 載入磁簧開關...")
            self.reed_switch = ReedSwitch(pin=Config.REED_SWITCH_PIN)
            
            # 3. 初始化伺服馬達
            print("\n[初始化] 載入伺服馬達...")
            self.servo = ServoController(
                pin=Config.SERVO_PIN,
                duty_rest=Config.SERVO_DUTY_REST,
                duty_push=Config.SERVO_DUTY_PUSH,
                move_time=Config.SERVO_MOVE_TIME,
                stabilize_time=Config.SERVO_STABILIZE_TIME,
                push_hold_time=Config.SERVO_PUSH_HOLD_TIME
            )
            
            # 4. 初始化 LINE 服務
            print("\n[初始化] 載入 LINE 通知服務...")
            self.line_service = LineMessagingService(
                channel_access_token=Config.LINE_CHANNEL_ACCESS_TOKEN,
                user_id=Config.LINE_USER_ID
            )
            
            print("\n✅ 所有硬體模組初始化完成！\n")
            
        except Exception as e:
            print(f"\n❌ 硬體初始化失敗: {e}")
            sys.exit(1)
    
    def check_and_reset_daily_count(self):
        """檢查日期是否已變更，若變更則重置計數器"""
        current_date = date.today()
        if current_date != self.last_reset_date:
            print(f"\n📅 日期變更: {self.last_reset_date} → {current_date}")
            print(f"   前日提醒次數: {self.daily_alert_count} 次")
            self.daily_alert_count = 0
            self.last_reset_date = current_date
            print("   計數器已重置為 0")
    
    def trigger_alert_and_push(self):
        """定時器到期，觸發 Stage 1/Stage 2 動作"""
        if not self.is_countdown_active:
            return
        
        self.is_countdown_active = False
        
        # 檢查當前狀態: 磁鐵是否仍遠離 (HIGH = 1)
        if self.reed_switch.value == 1:
            print("\n⏰ 計時器到期！蓋子仍未放下。")
            
            # 檢查並重置每日計數
            self.check_and_reset_daily_count()
            
            # 累加計數
            self.daily_alert_count += 1
            
            # 判斷階段
            if self.daily_alert_count < Config.DAILY_ALERT_THRESHOLD:
                # === 階段1：本地提醒 ===
                print(f"\n🔔 [階段1 提醒] 當日第 {self.daily_alert_count} 次")
                
                # 播放提醒音效
                self.audio.play_alert1(Config.ALERT1_SOUND)
                
                # 啟動伺服馬達推動蓋子
                self.servo.push_lid_down()
                
            else:
                # === 階段2：嚴重警告 + LINE 通知 ===
                print(f"\n🚨 [階段2 警告] 當日第 {self.daily_alert_count} 次（已達門檻）")
                
                # 播放嚴重警告音效
                self.audio.play_alert2(Config.ALERT2_SOUND)
                
                # 啟動伺服馬達推動蓋子
                self.servo.push_lid_down()
                
                # 發送 LINE 通知
                self.line_service.send_alert(self.daily_alert_count)
        else:
            print("\n✅ 計時器到期前，蓋子已放下。無需提醒。")
    
    def start_countdown(self):
        """當馬桶蓋開啟時 (HIGH = 1)，啟動計時器"""
        if self.is_countdown_active:
            return
        
        print(f"\n[狀態] 馬桶蓋開啟 (HIGH)。{Config.LID_OPEN_TIMEOUT} 秒後將檢查並觸發動作...")
        
        self.countdown_timer = threading.Timer(Config.LID_OPEN_TIMEOUT, self.trigger_alert_and_push)
        self.countdown_timer.start()
        self.is_countdown_active = True
    
    def stop_countdown(self):
        """當馬桶蓋關閉時 (LOW = 0)，取消計時器"""
        if self.is_countdown_active:
            print("\n[狀態] 馬桶蓋已放下！取消計時器。")
            if self.countdown_timer:
                self.countdown_timer.cancel()
            self.is_countdown_active = False
    
    def on_lid_opened(self, device):
        """事件：訊號從 LOW 變為 HIGH (磁鐵遠離 -> 蓋子抬起)"""
        print("[偵測] 訊號 HIGH (1): 馬桶蓋抬起！")
        self.start_countdown()
    
    def on_lid_closed(self, device):
        """事件：訊號從 HIGH 變為 LOW (磁鐵靠近 -> 蓋子放下)"""
        print("[偵測] 訊號 LOW (0): 馬桶蓋放下！")
        self.stop_countdown()
    
    def cleanup(self):
        """處理程式結束時的安全清理"""
        print("\n偵測到 Ctrl+C。程式正在安全終止...")
        
        # 取消計時器
        if self.countdown_timer and self.countdown_timer.is_alive():
            self.countdown_timer.cancel()
        
        # 清理各模組
        self.servo.cleanup()
        self.reed_switch.cleanup()
        self.audio.cleanup()
        
        print("HW: 硬體清理完成。")
        sys.exit(0)
    
    def run(self):
        """啟動 SmartLid 系統"""
        # 綁定 GPIO 事件
        self.reed_switch.when_activated = self.on_lid_opened
        self.reed_switch.when_deactivated = self.on_lid_closed
        
        # 顯示啟動訊息
        print("=" * 60)
        print("🚽 SmartLid 核心控制程式 V7.0 啟動")
        print(f"   延遲通知時間: {Config.LID_OPEN_TIMEOUT} 秒")
        print(f"   Stage 2 門檻: 當日 {Config.DAILY_ALERT_THRESHOLD} 次")
        print(f"   馬達 PWM: {Config.SERVO_DUTY_REST:.1f}% -> {Config.SERVO_DUTY_PUSH:.1f}%")
        print(f"   推動停留時間: {Config.SERVO_PUSH_HOLD_TIME:.1f} 秒")
        print("=" * 60)
        
        # 檢查當前狀態
        if self.reed_switch.value == 1:
            print("\n[啟動檢測] 當前蓋子為「抬起」狀態，啟動計時器...")
            self.start_countdown()
        else:
            print("\n[啟動檢測] 當前蓋子為「放下」狀態。")
        
        # 註冊信號處理
        signal(SIGINT, lambda sig, frame: self.cleanup())
        
        # 保持程式運行
        print("\n程式正在監聽 GPIO 事件 (按 Ctrl+C 結束)...\n")
        try:
            pause()
        except KeyboardInterrupt:
            self.cleanup()


def main():
    """主函式"""
    try:
        controller = SmartLidController()
        controller.run()
    except Exception as e:
        print(f"\n❌ 程式執行錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
