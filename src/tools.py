"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# 1. KHAI BÁO TOOL SCHEMAS

TOOLS_SCHEMA = [
    {
        "name": "query_clickhouse_metrics",
        "description": "Tra cứu các chỉ số dữ liệu thời gian thực (số lượng bản ghi, độ trễ) từ ClickHouse.",
        "parameters": {
            "type": "object",
            "properties": {
                "metric_type": {
                    "type": "string",
                    "description": "Loại dữ liệu cần tra cứu (ví dụ: 'gold_price', 'exchange_rate')"
                },
                "time_range": {
                    "type": "string",
                    "description": "Khoảng thời gian tra cứu (ví dụ: '30m', '1h', '24h')"
                }
            },
            "required": ["metric_type", "time_range"]
        }
    },
    {
        "name": "control_kafka_crawler",
        "description": "Điều khiển trạng thái các tiến trình (polling services) đẩy dữ liệu vào Kafka.",
        "parameters": {
            "type": "object",
            "properties": {
                "crawler_name": {
                    "type": "string",
                    "description": "Tên tiến trình cần điều khiển (ví dụ: 'gold_api_poller', 'exchange_rate_poller')"
                },
                "action": {
                    "type": "string",
                    "description": "Hành động thực thi (ví dụ: 'start', 'stop', 'restart')"
                }
            },
            "required": ["crawler_name", "action"]
        }
    }
]


# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL

# Trạng thái giả lập của ClickHouse (Lưu lượng dữ liệu thời gian thực)
CLICKHOUSE_MOCK_DB = {
    "gold_price": {
        "30m": {"record_count": 0, "avg_latency_ms": 0, "status": "NO_DATA_LAG"},
        "1h": {"record_count": 1250, "avg_latency_ms": 45, "status": "NORMAL"}
    },
    "exchange_rate": {
        "30m": {"record_count": 300, "avg_latency_ms": 12, "status": "NORMAL"},
        "1h": {"record_count": 600, "avg_latency_ms": 15, "status": "NORMAL"}
    }
}

# Trạng thái giả lập của các Polling Services đẩy vào Kafka
KAFKA_CRAWLER_STATE = {
    "gold_api_poller": {
        "status": "STOPPED",
        "uptime": "0h",
        "last_error": "ConnectionTimeout"
    },
    "exchange_rate_poller": {
        "status": "RUNNING",
        "uptime": "120h",
        "last_error": "None"
    }
}

def execute_query_clickhouse_metrics(metric_type: str, time_range: str) -> str:
    """Thực thi truy vấn metrics từ ClickHouse"""
    data = CLICKHOUSE_MOCK_DB.get(metric_type, {}).get(time_range)
    if data:
        return json.dumps({
            "status": "SUCCESS",
            "metric": metric_type,
            "time_range": time_range,
            "data": data
        }, ensure_ascii=False)
    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không có dữ liệu metric cho '{metric_type}' trong khoảng thời gian '{time_range}'."
    }, ensure_ascii=False)


def execute_control_kafka_crawler(crawler_name: str, action: str) -> str:
    """Thực thi lệnh điều khiển custom polling service của Kafka"""
    if crawler_name not in KAFKA_CRAWLER_STATE:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Tiến trình crawler '{crawler_name}' không tồn tại trong hệ thống."
        }, ensure_ascii=False)

    action = action.lower()
    if action in ["start", "restart"]:
        KAFKA_CRAWLER_STATE[crawler_name]["status"] = "RUNNING"
        KAFKA_CRAWLER_STATE[crawler_name]["last_error"] = "None"
        msg = f"Đã {action} thành công tiến trình {crawler_name}."
    elif action == "stop":
        KAFKA_CRAWLER_STATE[crawler_name]["status"] = "STOPPED"
        msg = f"Đã dừng tiến trình {crawler_name}."
    else:
        return json.dumps({"status": "ERROR", "message": f"Hành động '{action}' không hợp lệ."}, ensure_ascii=False)

    return json.dumps({
        "status": "SUCCESS",
        "crawler": crawler_name,
        "current_state": KAFKA_CRAWLER_STATE[crawler_name]["status"],
        "message": msg
    }, ensure_ascii=False)


# 3. ROUTER & DISPATCHER

TOOL_ROUTER = {
    "query_clickhouse_metrics": execute_query_clickhouse_metrics,
    "control_kafka_crawler": execute_control_kafka_crawler
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)