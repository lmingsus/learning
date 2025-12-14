import uiautomator2 as u2
from typing import Optional

class LinePlugin:
    def __init__(self):
        self.device: Optional[u2.Device] = None
        self.package_name = "jp.naver.line.android"

    def initialize(self) -> None:
        """初始化 LINE 外掛"""
        try:
            # 連接到 Android 裝置
            self.device = u2.connect()
            print("成功連接到 Android 裝置")
        except Exception as e:
            print(f"連接裝置失敗: {str(e)}")

    def execute(self, action: str, **kwargs) -> bool:
        """執行 LINE 相關操作"""
        if not self.device:
            print("尚未連接到裝置")
            return False

        try:
            if action == "open_line":
                return self._open_line()
            elif action == "send_message":
                return self._send_message(kwargs.get("contact"), kwargs.get("message"))
            else:
                print(f"未支援的操作: {action}")
                return False
        except Exception as e:
            print(f"執行操作失敗: {str(e)}")
            return False

    def cleanup(self) -> None:
        """清理資源"""
        if self.device:
            self.device = None
            print("已中斷連接")

    def _open_line(self) -> bool:
        """開啟 LINE 應用程式"""
        try:
            self.device.app_start(self.package_name)
            print("已開啟 LINE")
            return True
        except Exception as e:
            print(f"開啟 LINE 失敗: {str(e)}")
            return False

    def _send_message(self, contact: str, message: str) -> bool:
        """傳送訊息給指定聯絡人"""
        try:
            # 確保 LINE 已開啟
            self._open_line()
            
            # 點擊聊天列表
            self.device(resourceId=f"{self.package_name}:id/chat_list_tab").click()
            
            # 搜尋聯絡人
            self.device(resourceId=f"{self.package_name}:id/search_button").click()
            self.device(resourceId=f"{self.package_name}:id/search_edit_text").set_text(contact)
            
            # 選擇聯絡人
            self.device(text=contact).click()
            
            # 輸入並發送訊息
            self.device(resourceId=f"{self.package_name}:id/message_edit_text").set_text(message)
            self.device(resourceId=f"{self.package_name}:id/send_button").click()
            
            print(f"已發送訊息給 {contact}")
            return True
        except Exception as e:
            print(f"發送訊息失敗: {str(e)}")
            return False

# 使用範例
if __name__ == "__main__":
    plugin = LinePlugin()
    plugin.initialize()
    
    # 開啟 LINE
    plugin.execute("open_line")
    
    # 發送訊息
    plugin.execute("send_message", contact="測試用戶", message="這是一條測試訊息")
    
    plugin.cleanup()