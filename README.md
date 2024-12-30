# fb-analysis
Phân tích tin nhắn fb
#Hướng dẫn
### 1. Tải dữ liệu từ fb về
- vô đây : https://accountscenter.facebook.com/info_and_permissions/dyi
- rồi nhấn chọn tải thông tin xuống
- ![image](https://github.com/user-attachments/assets/d94d741f-189e-43ca-8451-de14216fc02d)
- sau đó chọn tài khoản muốn tải thông tin
- ![image](https://github.com/user-attachments/assets/8f3be867-78d8-4dc1-b61f-db98a77bb5dd) Nên chọn loại thông tin cụ thể
- tích chọn những thông tin cần tải rồi nhấn "Tiếp
- Chọn "Tải xuống thiết bị"
- Chọn khoảng thời gian muốn , chọn định dạng tải là "json" , chất lượng là cao nhất
- Nhấn tạo file và chờ tải về sau đó giải nén
### 2. Overview các hàm

| Tên hàm     | Mô tả      | 
|------------|------------|
| tien_xu_ly_du_lieu_tin_nhan_thu_muc  | Đầu vào là thư mục chức các file json. Hàm này để sử lí dữ liệu nếu bạn muốn phân tích tin nhắn của bạn với người khác hoặc trong nhóm chat  |
| tien_xu_ly_du_lieu_tin_nhan_thu_muc_mess_ca_nhan  |  Đầu vào là thư mục chức các file json. Hàm này để sử lí dữ liệu nếu bạn muốn phân tích tin nhắn cá nhân (kiểu 1 năm nhắn bao tin , nhắn gì ,...) | 
| ve_bieu_do_tin_nhan_va_so_tu  | Dùng để vẽ biểu đồ tin nhắn của bạn và người bạn nhắn tin hoặc các thành viên trong nhóm chat  | 
| phan_bo_tin_nhan_theo_thoi_gian  | Vẽ biểu đồ tần suất nhắn tin theo  giờ, tháng, tuần trong cuộc trò chuyện  |
| phan_tich_tan_suat_tu  | Phân tích top 10 từ bạn và mọi người dùng nhiều nhất  |
| phan_tich_tan_suat_emoji  | Danh sách số lần dùng emoji của mỗi người trong nhóm chat  |
| dem_tin_nhan_theo_nam  | Đêm số tin nhắn bạn nhắn mỗi năm |
| phan_tich_tu_theo_nam  | Top 10 từ dùng nhiều nhất ở mỗi năm  |

###3. Run code
 - Tải về và sử dụng
 - Sử dụng online - dùng cho người không biết code (rcm)
   + Truy cập : https://colab.research.google.com/drive/1wEZZ5wc893zfeBRaXCakjp9LnLb0yaIE?usp=sharing
   + Nhấn vô tệp rồi chọn lưu bản sao vào Drive 
   + Sau đó nhấn kết nối và chờ 1 chút để nó kết nối ![image](https://github.com/user-attachments/assets/8e80db2f-8f1f-48b8-a71a-ea4b78233382)
   + Tiếp nhấn vào biểu tượng thư mục và click chuột phải để tạo thư mục mới. Sau đó up load file json bạn muốn phân tích lên(muốn phân tích mấy file thì up từng đó lên) ![50](https://github.com/user-attachments/assets/b4fba5c2-1727-4c56-96c3-480332bbca1f)
   + Nó sẽ trông như vậy 
   + Sau đó nhấn "Ctrl+ F9" là thấy kết quả ![image](https://github.com/user-attachments/assets/95f06dd8-fb3c-44df-a699-ea225563a854)


