# Exit Ticket

## 1. Case nào nên dùng multi-agent? Vì sao?

Nên dùng multi-agent khi task phức tạp, gồm nhiều bước chuyên biệt và cần kiểm soát chất lượng theo từng giai đoạn. Ví dụ: research một chủ đề mới, tìm nguồn web, phân tích bằng chứng, rồi viết báo cáo có citations.

Lý do:

- Mỗi agent có responsibility riêng: Researcher tìm nguồn, Analyst phân tích, Writer tổng hợp.
- Shared state giúp debug rõ lỗi nằm ở bước nào.
- Supervisor routing giúp workflow có cấu trúc thay vì một prompt quá dài.
- Trace giúp quan sát latency, cost, route history và output từng agent.
- Guardrails như `max_iterations` giúp tránh vòng lặp vô hạn.

## 2. Case nào không nên dùng multi-agent? Vì sao?

Không nên dùng multi-agent khi task đơn giản và một LLM call có thể giải quyết tốt. Ví dụ: sửa câu văn ngắn, tóm tắt đoạn text nhỏ, trả lời câu hỏi fact đơn giản, hoặc format dữ liệu.

Lý do:

- Multi-agent tăng latency vì phải gọi nhiều agent tuần tự.
- Multi-agent tăng cost do nhiều LLM calls hơn baseline.
- Workflow phức tạp hơn, cần routing, state, trace và tests.
- Với task đơn giản, overhead lớn hơn lợi ích chất lượng.

## Final takeaway

Multi-agent phù hợp khi cần chất lượng, traceability và phân tách trách nhiệm. Single-agent phù hợp khi cần tốc độ, chi phí thấp và logic đơn giản.
