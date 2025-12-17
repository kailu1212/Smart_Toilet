"""
SmartLid 配置管理模組
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()


class Config:
    """SmartLid 基礎配置類"""
    
    # 專案路徑
    BASE_DIR = Path(__file__).parent.parent
    SRC_DIR = BASE_DIR / "src"
    DATA_DIR = BASE_DIR / "data"
    CONFIG_DIR = BASE_DIR / "config"
    LOGS_DIR = BASE_DIR / "logs"
    
    # 應用配置
    APP_NAME = os.getenv("APP_NAME", "SmartLid")
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # 磁簧開關 GPIO 配置
    REED_SWITCH_PIN = int(os.getenv("REED_SWITCH_PIN", "17"))
    
    # 伺服馬達 GPIO 配置
    SERVO_PIN = int(os.getenv("SERVO_PIN", "18"))
    SERVO_CLOSE_ANGLE = int(os.getenv("SERVO_CLOSE_ANGLE", "90"))
    SERVO_DUTY_REST = float(os.getenv("SERVO_DUTY_REST", "3.3"))
    SERVO_DUTY_PUSH = float(os.getenv("SERVO_DUTY_PUSH", "8.1"))
    SERVO_MOVE_TIME = float(os.getenv("SERVO_MOVE_TIME", "0.5"))
    SERVO_STABILIZE_TIME = float(os.getenv("SERVO_STABILIZE_TIME", "0.1"))
    SERVO_PUSH_HOLD_TIME = float(os.getenv("SERVO_PUSH_HOLD_TIME", "2.0"))
    
    # 計時配置
    LID_OPEN_TIMEOUT = int(os.getenv("LID_OPEN_TIMEOUT", "60"))  # 秒
    DAILY_ALERT_THRESHOLD = int(os.getenv("DAILY_ALERT_THRESHOLD", "2"))  # 次數
    
    # 音效配置
    ALERT1_SOUND = os.getenv("ALERT1_SOUND", "data/sounds/alert1.mp3")
    ALERT2_SOUND = os.getenv("ALERT2_SOUND", "data/sounds/alert2.mp3")
    
    # LINE Bot 配置
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
    LINE_USER_ID = os.getenv("LINE_USER_ID", "")
    
    # MQTT 配置（選用）
    MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
    MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    MQTT_TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "smartlid")
    
    # SQLite 資料庫配置
    DB_PATH = os.getenv("DB_PATH", "data/smartlid.db")
    
    # Flask Web Dashboard 配置
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """獲取所有配置"""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('_') and not callable(value)
        }
    
    @classmethod
    def display(cls):
        """顯示配置（隱藏敏感信息）"""
        config = cls.get_all()
        sensitive_keys = ["TOKEN", "SECRET", "PASSWORD"]
        
        for key, value in config.items():
            if any(sensitive in key.upper() for sensitive in sensitive_keys):
                print(f"{key}: ***")
            else:
                print(f"{key}: {value}")


# 創建全局配置實例
config = Config()

