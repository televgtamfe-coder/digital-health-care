---
name: python-data-processing
description: Python 数据处理与分析。当需要处理 Excel/CSV 文件、进行数据清洗、统计分析、数据可视化、或批量处理医学数据时使用此 skill。基于 DuckDB + pandas + openpyxl 技术栈，支持大文件高性能处理。
---

# Python 数据处理与分析 Skill

## 概述

面向美柚业务数据的 Python 数据处理工具集，覆盖 Excel/CSV 读取、SQL 查询、统计分析、数据清洗、批量处理等常见场景。

## 适用场景

- Excel 数据汇总与统计（问诊订单、社区发帖、健康记录等）
- CSV 批量处理与格式转换
- 数据清洗与质量检查
- 医学数据统计分析
- 数据可视化准备

## 技术栈

| 工具 | 用途 |
|------|------|
| DuckDB | 高性能 SQL 分析引擎，支持直接查询 Excel/CSV |
| pandas | DataFrame 操作与数据变换 |
| openpyxl | Excel 文件读写 |
| matplotlib/seaborn | 数据可视化 |

## 工作流

### Step 1: 理解需求

- 确认数据文件路径
- 明确分析目标（统计汇总/清洗/转换/可视化）
- 确定输出格式

### Step 2: 加载数据

使用 DuckDB 直接加载 Excel/CSV：

```python
import duckdb

# 直接查询 Excel（支持多 Sheet）
result = duckdb.sql("""
    SELECT * FROM 'data.xlsx'
""").df()

# 查询特定 Sheet
result = duckdb.sql("""
    SELECT * FROM read_xlsx('data.xlsx', sheet='Sheet1')
""").df()

# 查询 CSV
result = duckdb.sql("""
    SELECT * FROM 'data.csv'
""").df()
```

### Step 3: 执行分析

#### 数据探查

```python
# 查看表结构
duckdb.sql("DESCRIBE SELECT * FROM 'data.xlsx'").show()

# 统计行数
duckdb.sql("SELECT COUNT(*) FROM 'data.xlsx'").show()

# 查看前 N 行
duckdb.sql("SELECT * FROM 'data.xlsx' LIMIT 10").show()
```

#### 聚合统计

```python
duckdb.sql("""
    SELECT 
        category,
        COUNT(*) as cnt,
        AVG(amount) as avg_amount,
        MIN(amount) as min_amount,
        MAX(amount) as max_amount
    FROM 'data.xlsx'
    GROUP BY category
    ORDER BY cnt DESC
""").df()
```

#### 多表关联

```python
duckdb.sql("""
    SELECT o.*, c.name as customer_name
    FROM 'orders.xlsx' o
    JOIN 'customers.xlsx' c ON o.customer_id = c.id
""").df()
```

#### 数据清洗

```python
# 去重
duckdb.sql("""
    SELECT DISTINCT * FROM 'data.csv'
""").df()

# 处理空值
duckdb.sql("""
    SELECT 
        COALESCE(column_name, '默认值') as column_name,
        *
    FROM 'data.xlsx'
""").df()

# 类型转换
duckdb.sql("""
    SELECT 
        CAST(date_str AS DATE) as date,
        CAST(amount_str AS DOUBLE) as amount
    FROM 'data.csv'
""").df()
```

### Step 4: 输出结果

```python
# 导出为 Excel
result.to_excel('output.xlsx', index=False)

# 导出为 CSV
result.to_csv('output.csv', index=False)

# 导出为 JSON
result.to_json('output.json', orient='records', force_ascii=False)

# 导出为 Markdown 表格（适合嵌入报告）
print(result.to_markdown(index=False))
```

## 常用分析模式

### 模式 1: 问诊订单分析

```python
# 问诊量日趋势
duckdb.sql("""
    SELECT 
        DATE_TRUNC('day', created_at) as date,
        COUNT(*) as order_count
    FROM '问诊订单数据.xlsx'
    GROUP BY date
    ORDER BY date
""").df()

# 科室分布
duckdb.sql("""
    SELECT 
        department,
        COUNT(*) as cnt,
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as pct
    FROM '问诊订单数据.xlsx'
    GROUP BY department
    ORDER BY cnt DESC
""").df()
```

### 模式 2: 健康记录分析

```python
# 周期统计
duckdb.sql("""
    SELECT 
        user_id,
        AVG(cycle_days) as avg_cycle,
        STDDEV(cycle_days) as std_cycle,
        COUNT(*) as record_count
    FROM '健康记录.xlsx'
    GROUP BY user_id
    HAVING record_count >= 3
    ORDER BY std_cycle DESC
""").df()
```

### 模式 3: 社区数据统计

```python
# 发帖活跃度
duckdb.sql("""
    SELECT 
        DATE_TRUNC('week', post_time) as week,
        COUNT(*) as post_count,
        COUNT(DISTINCT user_id) as active_users
    FROM '社区发帖数据.xlsx'
    GROUP BY week
    ORDER BY week
""").df()
```

## 性能提示

- DuckDB 对 100MB+ 文件仍保持高性能（列式引擎）
- 大文件优先使用 DuckDB SQL 而非 pandas（避免全量加载到内存）
- 多次查询同一文件时，DuckDB 自动缓存解析结果
- 对于超大 Excel（>500MB），建议先转换为 CSV 或 Parquet

## 关键约束

- 数据文件路径需使用绝对路径
- Excel 日期列自动解析为 DATE 类型
- 列名含特殊字符时使用双引号包裹
- 敏感数据（患者信息等）处理需脱敏
