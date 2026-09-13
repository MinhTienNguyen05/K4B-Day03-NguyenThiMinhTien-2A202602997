# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Thị Minh Tiến
> **Mã Sinh Viên / Mã Học viên:** 2A202602997
> **Chủ đề Lựa chọn:** Trợ lý DataOps: Giám sát và Điều khiển Real-time Data Pipeline (Kafka & ClickHouse)

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá             | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm                                            |
| :--------------------------------- | :---------------: | :------------------------------------------------------------------------------------ |
| **1. Multi-step Reasoning**  |       5/ 5       | Bài toán có yêu cầu chia nhỏ nhiều bước suy luận nối tiếp nhau không?    |
| **2. Tool Interaction**      |       5 / 5       | Hệ thống có cần kết nối với MCP Server / Cơ sở dữ liệu bên ngoài không? |
| **3. Dynamic Decision**      |      5 / 5      | Bước tiếp theo có phụ thuộc vào kết quả quan sát bước trước không?     |
| **4. Long Horizon Goal**     |       3 / 5       | Hệ thống có phải giữ mục tiêu xuyên suốt qua nhiều lượt xử lý không?   |
| **TỔNG ĐIỂM AGENTIC FIT** | **18 / 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.*  |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
  {
    "step": 1,
    "query": "Tra cứu xem luồng dữ liệu giá vàng có đang bị trễ không (kiểm tra 30 phút qua). Nếu không có dữ liệu, hãy tự động restart lại tiến trình thu thập giá vàng (gold_api_poller).",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "control_kafka_crawler",
    "arguments": {
      "crawler_name": "gold_api_poller",
      "action": "restart"
    },
    "observation": {
      "status": "SUCCESS",
      "crawler": "gold_api_poller",
      "current_state": "RUNNING",
      "message": "Đã restart thành công tiến trình gold_api_poller."
    },
    "latency_ms": 5892.11
  },
  {
    "step": 2,
    "query": "Tra cứu xem luồng dữ liệu giá vàng có đang bị trễ không (kiểm tra 30 phút qua). Nếu không có dữ liệu, hãy tự động restart lại tiến trình thu thập giá vàng (gold_api_poller).",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ hệ thống Data Pipeline thành công.",
    "output": "🚀 [KAFKA SYSTEM] - Đã restart thành công tiến trình gold_api_poller.",
    "latency_ms": 10.0
  },
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [X] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).

- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt (1 lượt ở TC02, 1 lượt ở TC03, 2 lượt ở TC04, 1 lượt ở TC05)
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
