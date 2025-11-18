# Odoo 问货模块 (odoo_ask) - 测试与验证指南

本文档提供了使用 Docker 部署和测试 `odoo_ask` 模块的说明。

## 1. 先决条件

-   本地计算机已安装并正在运行 Docker。
-   已安装 Docker Compose。

## 2. 部署步骤

1.  **启动服务**:
    在项目根目录（`docker-compose.yml` 文件所在的位置）打开一个终端，并运行以下命令：
    ```bash
    docker-compose up -d
    ```
    此命令将下载所需的镜像（PostgreSQL 和 Odoo）并启动两项服务。`odoo_ask` 模块将直接挂载到 Odoo 容器中。

2.  **访问 Odoo**:
    等待一分钟让服务完成初始化。您可以使用 `docker-compose logs -f odoo` 查看日志。一旦看到服务器正在运行的消息，请打开您的网页浏览器并访问：
    `http://localhost:8069`

3.  **创建新数据库**:
    -   在 Odoo 的欢迎界面上，系统会提示您创建一个新数据库。
    -   `docker-compose.yml` 已经预先配置了数据库连接，但您需要创建供 Odoo 使用的初始数据库。
    -   填写表单：
        -   **主控密码 (Master Password)**: 这是一个用于保护数据库管理页面的密码。请设置一个容易记住的密码，例如 `master_password`。
        -   **数据库名称 (Database Name)**: `odoo` (这应与 `docker-compose.yml` 中的 `POSTGRES_DB` 值匹配)。
        -   **邮箱 (Email)**: `admin` (这将是您的管理员用户名)。
        -   **密码 (Password)**: `admin` (您的管理员密码)。
        -   **语言 (Language)**: English 或 Chinese
        -   **国家 (Country)**: Your country
        -   **加载演示数据 (Load demonstration data)**: 勾选此框以获得一些可供使用的示例数据。
    -   点击“创建数据库 (Create database)”。

4.  **安装 `odoo_ask` 模块**:
    -   数据库创建后，您将自动登录。
    -   点击顶部的“应用 (Apps)”菜单。
    -   在搜索框中，移除默认的“Apps”过滤器，然后输入 `Ask Management`。
    -   您应该能看到“Ask Management”模块。点击“激活 (Activate)”按钮进行安装。

## 3. 功能测试计划

### 测试用例 1: 销售人员创建问货单

1.  **登录**: 以销售用户身份登录（您可能需要创建一个新用户并将其分配到“Ask Management / Sales”用户组）。
2.  **导航**: 前往 `问货管理 (Ask Management)` -> `问货单 (Ask Orders)`。
3.  **创建**: 点击“创建 (Create)”以生成一个新的问货单。
    -   选择一个 `客户 (Customer)`。
    -   设置一个 `目标交付日期 (Target Delivery Date)`。
    -   在“问货明细 (Ask Lines)”标签页中，添加一个产品并设置 `问货数量 (Ask Quantity)`。
4.  **提交**: 保存订单，并将其状态从“草稿 (Draft)”更改为“已提交 (Submitted)”。
5.  **验证**: 确认订单已正确保存并处于“已提交 (Submitted)”状态。

### 测试用例 2: 每日截单定时任务

1.  **触发定时任务**: 您可以等待定时任务在其预定时间（23:59）运行，或手动触发它。
    -   要手动触发：
        -   启用开发者模式（设置 -> 激活开发者模式）。
        -   导航至 `设置 (Settings)` -> `技术 (Technical)` -> `计划操作 (Scheduled Actions)`。
        -   找到“Ask: Daily Cutoff Process”并点击“手动运行 (Run Manually)”。
2.  **验证**:
    -   返回到您创建的问货单。
    -   检查其 `状态 (state)` 是否已变为“已锁定 (Locked)”。
    -   在“问货明细 (Ask Lines)”中，验证 `有效问货数量 (Valid Ask Quantity)` 现在是否具有您在 `问货数量 (Ask Quantity)` 中输入的值。
    -   检查问货明细行上的 `截单日志 (Cutoff Log)` 字段，查看审计消息。

### 测试用例 3: 采购仪表盘

1.  **登录**: 以采购用户身份登录（将一个用户分配到“Ask Management / Procurement”用户组）。
2.  **导航**: 前往 `问货管理 (Ask Management)` -> `采购仪表盘 (Procurement Dashboard)`。
3.  **验证**:
    -   您应该能看到一个数据透视表。
    -   验证该表是否正确地按产品汇总了所有已锁定问货单的 `有效问货数量 (Valid Ask Quantity)`。

### 测试用例 4: 仓库人员创建预留

1.  **登录**: 以仓库用户身份登录（将一个用户分配到“Ask Management / Warehouse”用户组）。
2.  **导航**: 前往 `问货管理 (Ask Management)` -> `预留 (Reservations)`。
3.  **创建**: 创建一个新的预留。
    -   选择您想要预留的产品的对应 `问货明细 (Ask Line)`。
    -   输入 `预留数量 (Reserved Quantity)`。
    -   在 `预留给销售员 (Reserved for Salesperson)` 字段中将其分配给一个销售员。
4.  **验证**:
    -   预留应处于“已预留 (Reserved)”状态。
    -   返回到对应的 `问货明细 (Ask Line)`，检查 `预留数量 (Reserved Quantity)` 字段是否已更新。

### 测试用例 5: 出库验证（保守型检查）

1.  **创建销售订单和发货单**:
    -   作为销售用户，为已有预留的同一产品创建一个销售订单。
    -   确认该销售订单以生成一个发货单（出库）。
2.  **尝试验证（错误的用户）**:
    -   以一个 **并非** 被分配到该预留的销售员的用户身份登录。
    -   前往 `库存 (Inventory)` 应用，找到该发货单，然后点击“验证 (Validate)”。
3.  **验证（失败）**:
    -   系统应阻止验证，并显示一个 `ValidationError` 消息，指出该产品已被预留。
4.  **尝试验证（正确的用户）**:
    -   以 **被** 分配到该预留的销售员（`reserved_to_sales_id`）的身份登录。
    -   前往同一个发货单，然后点击“验证 (Validate)”。
5.  **验证（成功）**:
    -   系统应允许验证继续进行。

## 4. 停止环境

要停止 Docker 容器，请在您的终端中运行以下命令：
```bash
docker-compose down
```
要同时移除数据库卷（这将删除所有数据），请运行：
```bash
docker-compose down -v