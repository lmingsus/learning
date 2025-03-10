import os
import errno
import json


# 設定 user_history.json 存放路徑
static_jsonn_path = os.path.join(os.path.dirname(__file__), 'static', 'jsonn')
# Path for static jsonn files
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            # 如果文件存在，則忽略
            pass
        else:
            raise

# function for create jsonn dir for some content
def make_static_jsonn_dir(static_jsonn_path: str = static_jsonn_path):
    try:
        os.makedirs(static_jsonn_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_jsonn_path):
            # 如果文件存在，則忽略
            pass
        else:
            raise


def read_user_history(json_path: str = static_jsonn_path) -> dict:
    """
    讀取 user_history.json 檔案，如果不存在則建立一個新的
    param json_path: str, default is static_jsonn_path
    return user_history: dict
    """
    if not os.path.exists(os.path.join(json_path, 'user_history.json')):
        # 如果 user_history.json 不存在，則建立一個新的
        # 設定格式
        user_history = {"Administrator": [], "users": {}, 
                        "Super_Administrator": ["U", # 銘
                                                "U" # 宇
                                                ]}
        try:
            with open(os.path.join(json_path, 'user_history.json'), 'w', encoding='utf-8') as f:
                json.dump(user_history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error writing user_history.json: {e}")
            raise e


    else:
        try:
            with open(os.path.join(json_path, 'user_history.json'), 'r', encoding='utf-8') as f:
                try:
                    user_history = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from user_history.json: {e}")
                    user_history = {"Administrator": [], "users": {}, 
                                    "Super_Administrator": ["U", # 銘
                                                            "U" # 宇
                                                            ]}
        except Exception as e:
            print(f"Error reading user_history.json: {e}")
            raise e
    return user_history



def start_user_history(user_history, event):
    """
    開始記錄使用者歷史資料，並建立相關資料欄位
    param user_history: dict
    param event: LineEvent
    return user_history: dict
    """
    if event.type == "postback":
        user_id = event.source.user_id
        event_info = {"timestamp": event.timestamp, 
                    "message": {"data": event.postback.data,
                                "params": event.postback.params,
                                }}
    
    elif event.type == "message":
        user_id = event.source.user_id
        event_info = {"timestamp": event.timestamp, 
                        "message": {"id": event.message.id,
                                    "text": event.message.text,
                                    "type": event.message.type,
                                    "quote_token": event.message.quote_token,
                                    }}



    # 抓取使用者資料、狀態
    if user_id in user_history["Administrator"]:
        # Administrator
        # 管理者讀取歷史資料
        # if user_input == 'check':
        #     if 
        pass
        user_history["users"][user_id]["history"].append(event_info)
        # user_status = user_history["users"][user_id]["status"]

    elif user_id in user_history["users"]:
        # old user
        # 舊用戶讀取歷史資料
        user_history["users"][user_id]["history"].append(event_info)

        if "status" not in user_history["users"][user_id]:
            # 更新建立底下資料欄位
            user_history["users"][user_id]["status"] = None

        # user_status = user_history["users"][user_id]["status"]

        if "favorite" not in user_history["users"][user_id]:
            # 更新建立底下資料欄位：展覽類別
            user_history["users"][user_id]["favorite"] = []

        if "love_exhi" not in user_history["users"][user_id]:
            # 更新建立底下資料欄位：：我的最愛展覽
            user_history["users"][user_id]["love_exhi"] = []
            # love_exhi = user_history["users"][user_id]["love_exhi"]
        
        if "love_firm" not in user_history["users"][user_id]:
            # 更新建立底下資料欄位：：我的最愛廠商
            user_history["users"][user_id]["love_firm"] = []

    else:
        # new user 
        # 新用戶建立底下資料欄位
        user_history["users"][user_id] = {}
        user_history["users"][user_id]["status"] = None
        # user_status = None
        user_history["users"][user_id]["favorite"] = []
        user_history["users"][user_id]["love_exhi"] = []
        user_history["users"][user_id]["love_firm"] = []
        user_history["users"][user_id]["history"] = [event_info]
    
    return user_history


def write_user_history(user_history, json_path: str = static_jsonn_path):
    """
    寫入 user_history.json 檔案
    param user_history: dict
    param json_path: str, default is static_jsonn_path
    """
    try:
        with open(os.path.join(json_path, 'user_history.json'), 'w', encoding='utf-8') as f:
            json.dump(user_history, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing user_history.json: {e}")
        raise e
