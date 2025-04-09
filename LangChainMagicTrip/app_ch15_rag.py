'''
Create a new LangServe application.
langchain app new [OPTIONS] NAME
langchain app new langserveapp_250405


cd ./langserveapp_250405

檔案：pyproject.toml
[tool.poetry.dependencies]
python = "^3.12"
uvicorn = "^0.23.2"
langserve = {extras = ["server"], version = "0.3.1"}
pydantic = ">2"
langchain = "0.3.20"
langchain-openai = "0.3.9"
langchain-community = "0.3.19"
langchain-qdrant = "0.2.0"
qdrant-client = "^1.13.3"


poetry add langchain-openai langchain-community langchain-qdrant qdrant-client
失敗的話，改 pydantic = ">2"

更新相依套件
poetry update

清除現有的虛擬環境：
poetry env remove python
重新建立虛擬環境
poetry install


進入虛擬環境
poetry env activate

顯示當前已啟動的虛擬環境訊息
poetry env info

列出與 project 相關的虛擬環境
poetry env list

啟動 LangServe 伺服器
langchain serve
或 poetry run langchain serve



'''



''' ch15.4 容器化

使用 Docker 建立映像檔（image）：
docker build . -t langserveapi-250407:latest
docker build .，. 表示當前目錄作為 build context，也就是包含 Dockerfile 與其他所需檔案的位置。
標籤（tag）：-t langserveapi-250407:latest，映像檔名稱:映像檔的標籤

執行容器：
docker run -d -p 8080:8080 --name langserveapi-250407 langserveapi-250407:latest
-d: (detach) 在背景執行容器
-p 8080:8080: 連接埠映射，主機端口（host port） : 容器端口（container port），容器內部的 8080 端口映射到主機的 8080 端口
--name langserveapi-250407: 指定容器名稱為 langserveapi-250407
langserveapi-250407:latest: 要運行的映像檔名稱和標籤
容器啟動後，可以透過 http://localhost:8080 訪問應用程式
容器會在背景運行，不會佔用當前終端

# 檢視運行中的容器
docker ps
# 停止容器
docker stop langserveapi-250407
# 啟動已存在的容器
docker start langserveapi-250407
# 移除容器
docker rm langserveapi-250407


'''



''' Ch15.5 LangServe 容器映像登錄
Azure：建立容器登錄

docker run -it hello-world

登入容器 ACR(Azure Container Registry)
docker login myregistry.azurecr.io
例如 docker login lanchainbook250407.azurecr.io 
需要輸入 使用者名稱username 和 密碼password

把本地的映像檔打上新的標籤，即加上登入伺服器
docker tag langserveapi-250407:latest lanchainbook250407.azurecr.io/langserveapi-250408:latest
langserveapi-250407:latest: 現有映像檔的名稱和標籤
lanchainbook250407.azurecr.io/langserveapi-250408:latest：新的映像檔名稱和標籤（在 ACR 中）

推送到 ACR 
docker push lanchainbook250407.azurecr.io/langserveapi-250408:latest
推送完成後可以查看
'''


'''ch15.6 部屬
應用程式服務 - 建立 Web 應用程式
容器 - Linux
容器 - Azure Container Registry - 
'''