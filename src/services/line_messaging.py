"""
LINE Messaging API 服務模組
使用 LINE Messaging API 發送推播訊息（Push Message）
"""
import requests
from typing import Optional


class LineMessagingService:
    """LINE Messaging API 服務"""
    
    def __init__(self, channel_access_token: str, user_id: str):
        """
        初始化 LINE Messaging API 服務
        
        Args:
            channel_access_token: LINE Channel Access Token
            user_id: 接收訊息的 LINE User ID
            
        如何取得 Token 和 User ID:
        1. 前往 LINE Developers Console: https://developers.line.biz/
        2. 建立 Provider 和 Messaging API Channel
        3. 在 Channel 的 "Messaging API" 頁籤取得 Channel Access Token
        4. 加 LINE Bot 為好友後，透過 Webhook 或測試工具取得 User ID
        
        注意：Push Message 每月有免費額度限制
        """
        self.channel_access_token = channel_access_token.strip()
        self.user_id = user_id.strip()
        self.api_url = "https://api.line.me/v2/bot/message/push"
        print("LINE: Messaging API 服務已初始化 (LIVE 模式)")
    
    def send_alert(self, alert_count: int) -> bool:
        """
        發送提醒訊息到 LINE
        
        Args:
            alert_count: 當日提醒次數
            
        Returns:
            bool: 發送成功返回 True，失敗返回 False
        """
        try:
            message = f"🚽 SmartLid 提醒\n\n今天已經是第 {alert_count} 次忘記放下馬桶蓋了！\n請養成良好習慣喔 😊"
            
            headers = {
                "Authorization": f"Bearer {self.channel_access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "to": self.user_id,
                "messages": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
            
            print(f"📤 正在發送 LINE 通知（第 {alert_count} 次提醒）...")
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("✅ LINE 通知發送成功！")
                return True
            else:
                print(f"❌ LINE 通知發送失敗: HTTP {response.status_code}")
                print(f"   錯誤訊息: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ LINE API 請求超時")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ LINE API 請求失敗: {e}")
            return False
        except Exception as e:
            print(f"❌ 發送 LINE 通知時發生錯誤: {e}")
            return False
    
    def send_message(self, message: str) -> bool:
        """
        發送文字訊息到 LINE
        
        Args:
            message: 要發送的訊息內容
            
        Returns:
            bool: 發送成功返回 True，失敗返回 False
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.channel_access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "to": self.user_id,
                "messages": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.success(f"LINE 訊息發送成功: {message[:50]}...")
                return True
            else:
                logger.error(f"LINE 訊息發送失敗: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"發送 LINE 訊息時發生錯誤: {e}")
            return False
    
    def send_flex_message(self, alt_text: str, flex_contents: dict) -> bool:
        """
        發送 Flex Message（彈性訊息）
        
        Args:
            alt_text: 替代文字（當無法顯示 Flex Message 時顯示）
            flex_contents: Flex Message 的內容
            
        Returns:
            bool: 發送成功返回 True
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.channel_access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "to": self.user_id,
                "messages": [
                    {
                        "type": "flex",
                        "altText": alt_text,
                        "contents": flex_contents
                    }
                ]
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.success("Flex Message 發送成功")
                return True
            else:
                logger.error(f"Flex Message 發送失敗: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"發送 Flex Message 時發生錯誤: {e}")
            return False
    
    def send_alert(self, alert_count: int, today_date: str) -> bool:
        """
        發送馬桶蓋提醒通知
        
        Args:
            alert_count: 今日累計未落蓋次數
            today_date: 日期字串
            
        Returns:
            bool: 發送成功返回 True
        """
        message = f"""⚠️ SmartLid 馬桶蓋提醒 ⚠️

📅 日期: {today_date}
🔔 今日累計未落蓋次數: {alert_count} 次

請記得隨手將馬桶蓋放下喔！🚽
養成良好衛生習慣 💪"""
        
        return self.send_message(message)
    
    def send_alert_flex(self, alert_count: int, today_date: str) -> bool:
        """
        發送馬桶蓋提醒通知（Flex Message 版本，更美觀）
        
        Args:
            alert_count: 今日累計未落蓋次數
            today_date: 日期字串
            
        Returns:
            bool: 發送成功返回 True
        """
        flex_contents = {
            "type": "bubble",
            "hero": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "⚠️ SmartLid 提醒",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#FF6B6B"
                    }
                ],
                "backgroundColor": "#FFF3E0",
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📅",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": f"日期: {today_date}",
                                "size": "sm",
                                "color": "#666666",
                                "margin": "md"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🔔",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": f"今日累計: {alert_count} 次",
                                "size": "md",
                                "color": "#FF6B6B",
                                "weight": "bold",
                                "margin": "md"
                            }
                        ],
                        "margin": "lg"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": "請記得隨手將馬桶蓋放下喔！🚽",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": "養成良好衛生習慣 💪",
                        "size": "sm",
                        "color": "#4CAF50",
                        "wrap": True,
                        "margin": "md"
                    }
                ]
            }
        }
        
        return self.send_flex_message("SmartLid 馬桶蓋提醒", flex_contents)
    
    def send_daily_summary(self, date: str, total_count: int) -> bool:
        """
        發送每日統計摘要
        
        Args:
            date: 日期字串
            total_count: 當日總次數
            
        Returns:
            bool: 發送成功返回 True
        """
        emoji = "✅" if total_count < 2 else "⚠️"
        comment = "今日表現良好！" if total_count < 2 else "請多加注意衛生習慣"
        
        message = f"""📊 SmartLid 每日報告

📅 日期: {date}
📈 今日未落蓋次數: {total_count} 次

{emoji} {comment}"""
        
        return self.send_message(message)
    
    def test_connection(self) -> bool:
        """
        測試 LINE Messaging API 連線
        
        Returns:
            bool: 連線成功返回 True
        """
        logger.info("測試 LINE Messaging API 連線...")
        return self.send_message("🔧 SmartLid 系統測試訊息\n系統運作正常！")


def test_line_messaging(channel_access_token: Optional[str] = None, user_id: Optional[str] = None):
    """
    測試 LINE Messaging API 功能
    
    使用方式:
        python -c "from src.services.line_messaging import test_line_messaging; test_line_messaging('YOUR_TOKEN', 'YOUR_USER_ID')"
    """
    import os
    from datetime import datetime
    
    if channel_access_token is None:
        channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
    
    if user_id is None:
        user_id = os.getenv("LINE_USER_ID", "")
    
    if not channel_access_token or not user_id:
        print("❌ 錯誤: 請提供 LINE Channel Access Token 和 User ID")
        print("\n取得方式:")
        print("1. 前往 https://developers.line.biz/")
        print("2. 建立 Messaging API Channel")
        print("3. 取得 Channel Access Token 和 User ID")
        print("\n設定方式:")
        print("在 .env 檔案中加入:")
        print("LINE_CHANNEL_ACCESS_TOKEN=你的Token")
        print("LINE_USER_ID=你的UserID")
        return False
    
    print("🚀 開始測試 LINE Messaging API...")
    
    # 建立服務實例
    line_service = LineMessagingService(channel_access_token, user_id)
    
    # 測試1: 基本連線測試
    print("\n📝 測試 1: 基本文字訊息")
    if line_service.test_connection():
        print("✅ 測試通過")
    else:
        print("❌ 測試失敗")
        return False
    
    # 測試2: 發送提醒訊息
    print("\n📝 測試 2: 發送提醒訊息")
    today = datetime.now().strftime("%Y-%m-%d")
    if line_service.send_alert(alert_count=2, today_date=today):
        print("✅ 測試通過")
    else:
        print("❌ 測試失敗")
    
    # 測試3: 發送 Flex Message
    print("\n📝 測試 3: 發送 Flex Message（美化版）")
    if line_service.send_alert_flex(alert_count=2, today_date=today):
        print("✅ 測試通過")
    else:
        print("❌ 測試失敗")
    
    # 測試4: 發送每日摘要
    print("\n📝 測試 4: 發送每日摘要")
    if line_service.send_daily_summary(date=today, total_count=3):
        print("✅ 測試通過")
    else:
        print("❌ 測試失敗")
    
    print("\n✨ 測試完成！請檢查你的 LINE 是否收到訊息")
    return True


if __name__ == "__main__":
    # 直接執行此檔案進行測試
    test_line_messaging()
