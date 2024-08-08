# 极简智能
这是一款使用 `LangChain` 构建的 `LLM` web应用，你可以在这儿使用大模型提供的多种功能

**技术支持：**
- 前端基于 `vue` 框架开发，部分使用 `element ui`
- 业务逻辑后端基于 `springboot` + `mybatis plus` + `mysql` + `Redis` 开发
- 大模型后端使用 `FastAPI` 集成 `LangChain` 框架构建的 `LLM` 服务
- 前后端通信遵循 `RESTful` 风格
- 持续连接通讯使用 `Websocket` 协议

**在线预览：**
- [极简智能](http://1.92.148.127:8888)

## 首先运行后端项目

后端项目位于 `/back_end` 与`/fastApi`文件夹，按照以下步骤，即可成功运行该项目。

## 1. 安装 `jdk`
 安装 `jdk21` 并配置环境变量

## 2. 安装 IntelliJ IDEA
 从 [IntelliJ IDEA 官网](https://www.jetbrains.com/idea/) 下载并安装。

## 3. 打开 Spring Boot 项目

1. 使用 IntelliJ IDEA 打开项目。

## 4. 安装 Maven

1. 官方网站下载并安装 [Maven](https://maven.apache.org/).
2. 验证是否安装成功，命令行执行：

   ```bash
   mvn -v
   ```
如果出现版本信息，即安装成功。

## 5. 配置 Maven

1. `IDEA` 中设置 `Maven` 为自己安装的版本


## 6. 设置 MySQL 数据库

1. 安装 MySQL。
2. 为该项目创建数据库并配置用户权限。
3. 运行`/back_end/src/main/resources`目录下的`create_table.sql`脚本，建表

## 7. 安装redis

1. 安装 Redis。
2. 启动 Redis 服务器。

## 8. 配置 `application.properties` 信息
1. 在 `/back_end/src/main/resources` 下的 `application - 副本.properties` 重命名为 `application.properties`
2. 修改 `application.properties` 中相关数据库信息为自己前两步中配置的信息
   
## 9. 启动 `springboot` 项目
1. 在 `IDEA` 中启动该项目即可


## 10. 安装 `python3.11`

1. 从 Python 官网 下载并安装。
2. 验证是否安装成功，命令行执行：

   ```bash
   python3 --version
   ```
   出现版本信息，则安装成功。

## 11. 安装所需的包

1. 使用 `pip` 命令安装项目所需的包文件

## 12. 配置 `FastAPI` 项目
1. 详见 `/fastApi/README.md`

## 13. 运行 `FastAPI`项目
1. 用python运行fastapi后端

## 14. 注意事项：
- `FastAPI` 项目运行于 `8080` 端口，请勿修改，且确保无占用
- `FastAPI` 项目和 `springboot` 项目应运行于同一台主机之下

## 运行前端项目
前端项目是 `/front_end` 文件夹，按照以下步骤，即可成功运行该项目

## 1. 安装 `node.js`  
官网安装即可  
验证是否安装成功，命令行执行：  
```bash
npm --version
```
如果出现版本信息，即安装成功
## 2. 安装 `Vue CLI`  
命令行执行以下命令，全局安装 `Vue CLI`  
```bash
npm install -g @vue/cli
```
验证是否安装成功，命令行执行：  
```bash
vue --version
```
如果出现版本信息，即安装成功
## 3. 下载依赖 `module`  
在 `/front_end` 目录下，命令行执行：  
```bash
npm install
```
## 4. 运行项目，命令行执行（二者选其一即可）：  
 - 先启动后端程序，进行数据库-后端-前端真实运行(必须先运行前面的后端程序)：  
 ```bash
 npm run serve:dev
 ```  
 - 连接作者服务器上运行的后端程序(可以不启动后端程序)：  
 ```bash
 npm run serve:pro
 ```  