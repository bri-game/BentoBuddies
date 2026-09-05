# Hướng phát triển sau chiến dịch 108 màn

Đã triển khai trong 0.3.0: ô chỉ định món, khóa hướng xoay, bánh tránh viền, nhiều hình dạng hộp/ngăn, kết hợp tối đa bốn luật, hướng dẫn theo cơ chế, bản đồ chín chuyến đi. Các hướng dưới đây là đề xuất, chưa được đưa vào bản APK này.

1. **Vách ngăn di chuyển được.** Người chơi chọn vị trí một vách trước khi xếp. Vách làm thay đổi khả năng đặt món và cách ngăn kem khỏi súp; đây là quyết định về cấu trúc hộp, không chỉ tăng số ô. Cần định nghĩa chạm cạnh qua vách và solver có cả trạng thái vách. Giới thiệu một vách/hai vị trí trước khi dùng nhiều vị trí.
2. **Yêu cầu về số lượng láng giềng.** Ví dụ súp cần đúng hai loại món chạm cạnh, hoặc bánh chỉ được chạm một món khác. Yêu cầu “đúng N” tạo bài toán đếm và suy luận mới. Hiển thị bộ đếm trực tiếp; tránh chỉ thêm câu chữ trên màn thắng/thua.
3. **Đơn hàng hai hộp.** Chia cùng một bộ nguyên liệu cho hai người bạn có sở thích khác nhau. Người chơi quyết định món nào đi đâu trước khi tối ưu vị trí. Khởi đầu với tổng diện tích nhỏ để không thu bé các điểm chạm.
4. **Huy hiệu tùy chọn khi chơi lại.** Hoàn thành với số lần xoay thấp hoặc không dùng gợi ý, nhưng không chặn tiến độ chính và không mất lượt. Chỉ đưa mục tiêu tối ưu khi solver đã chứng minh ngưỡng đạt được; đếm thao tác nhất quán qua hoàn tác/reset. Album có thể lưu huy hiệu theo từng hộp.
5. **Picnic hằng ngày và trang trí album.** Mỗi ngày một seed cố định có lời giải kiểm chứng và lựa chọn ngoại hình để sưu tầm. Nội dung hằng ngày vẫn cần bộ lọc trùng cấu trúc và nhịp mới lạ; thay màu không được tính là màn mới. Không cần phạt người chơi bỏ ngày.

Ưu tiên tiếp theo: thử người chơi ở các mốc 25/37/49 để đo hiểu luật, số lần xếp sai, dùng gợi ý và thoát màn; chỉnh mức khó trước khi thêm hệ thống giữ chân. Sau đó thử một chương 12 màn “vách ngăn” vì nó mở rộng quyết định không gian rõ nhất. Các nhãn độ khó hiện tại được sàng lọc bằng chỉ số solver và cấu trúc, chưa được hiệu chuẩn bằng người chơi.
