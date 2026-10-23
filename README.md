# Kiểm thử tự động website SauceDemo bằng Selenium

## 1. Thông tin đề tài

- **Tên đề tài:** Kiểm thử tự động website thương mại điện tử demo bằng Selenium WebDriver.
- **Mục tiêu:** Thực hành tự động hóa các luồng đăng nhập, giỏ hàng, sắp xếp sản phẩm và đăng xuất; xác minh kết quả bằng assertion.
- **Phạm vi:** 8 test case chức năng trên website SauceDemo.
- **Website:** [https://www.saucedemo.com/](https://www.saucedemo.com/)
- **Công nghệ:** Python, Selenium WebDriver, Pytest và Google Chrome.

## 2. Giới thiệu Selenium

Selenium là bộ công cụ mã nguồn mở dùng để tự động hóa trình duyệt web. Selenium WebDriver cung cấp API để chương trình giao tiếp với trình duyệt, tìm phần tử giao diện, nhập dữ liệu, nhấn nút và đọc trạng thái trang. Trong project này, Python viết kịch bản, Selenium điều khiển Chrome và Pytest tổ chức/chạy test, cung cấp fixture và tổng hợp kết quả.

Trong kiểm thử thủ công, người kiểm thử tự thao tác và ghi nhận kết quả qua từng lần chạy. Kiểm thử tự động dùng mã lệnh để lặp lại các thao tác và assertion, phù hợp với các luồng ổn định cần chạy thường xuyên. Selenium hỗ trợ nhiều trình duyệt và tương tác gần với hành vi người dùng, nhưng test giao diện có thể nhạy với thay đổi giao diện, locator, tốc độ mạng và trạng thái website; Selenium cũng không thay thế mọi loại kiểm thử (ví dụ kiểm thử hiệu năng chuyên sâu).

## 3. Giới thiệu website kiểm thử

SauceDemo (giao diện có thương hiệu Swag Labs) là website thực hành kiểm thử luồng cửa hàng trực tuyến, không phải cửa hàng thương mại thật. Các chức năng trong phạm vi gồm đăng nhập thành công/thất bại, xử lý username trống, thêm/xóa sản phẩm, sắp xếp giá, xác minh sản phẩm trong giỏ và đăng xuất.

- **Tài khoản demo:** `standard_user`
- **Mật khẩu demo:** `secret_sauce`
- Website công khai có thể thay đổi, gián đoạn hoặc giới hạn truy cập; test cần Internet và phụ thuộc vào dịch vụ bên ngoài.

## 4. Môi trường và công cụ

Thông tin môi trường đã xác minh khi chạy test trên máy hiện tại:

| Thành phần | Phiên bản/trạng thái |
|---|---|
| Hệ điều hành | Microsoft Windows 11 Home Single Language, build 10.0.26200 |
| Python | 3.12.8 |
| Google Chrome | 155.0.8059.85 |
| Selenium | 4.51.0 |
| Pytest | 9.1.1 |
| pip | 26.2.2 |
| Driver trình duyệt | Selenium Manager tự quản lý khi khởi tạo `webdriver.Chrome()` |

Phiên bản trên máy khác có thể khác; kiểm tra Python và thư viện bằng `python --version`, `python -m pip show selenium pytest`. Trên Windows PowerShell, kiểm tra Chrome tại vị trí cài đặt mặc định bằng `(Get-Item "$env:ProgramFiles\Google\Chrome\Application\chrome.exe").VersionInfo.ProductVersion`. Dự án không cần cài WebDriver Manager: Selenium 4 có Selenium Manager để tìm/tải driver tương thích khi cần; lần khởi chạy đầu tiên có thể cần Internet.

## 5. Cấu trúc thư mục

```text
selenium-automation-testing/
├── pages/
│   ├── __init__.py
│   ├── cart_page.py
│   ├── inventory_page.py
│   └── login_page.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_saucedemo.py
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

- `pages/`: Page Object cho màn hình đăng nhập, danh sách sản phẩm và giỏ hàng.
- `tests/conftest.py`: tùy chọn Pytest, fixture mở/đóng Chrome và đăng nhập dùng chung.
- `tests/test_saucedemo.py`: 8 test case có assertion độc lập.
- `requirements.txt`: dependency cần thiết.
- `pytest.ini`: cấu hình tự tìm test.
- `.gitignore`: loại trừ môi trường ảo, cache, log và kết quả tạm.

## 6. Cài đặt môi trường

1. Cài Python 3 và Google Chrome nếu máy chưa có.
2. Mở thư mục project trong VS Code.
3. Tạo môi trường ảo tại thư mục gốc.
4. Kích hoạt môi trường và cài dependency:

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Nếu PowerShell chặn kích hoạt script, dùng Command Prompt:

```bat
.venv\Scripts\activate.bat
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Kiểm tra phiên bản đã cài:

```bash
python --version
python -m pip show selenium pytest
```

## 7. Hướng dẫn chạy test

Chạy toàn bộ test, Chrome hiển thị giao diện:

```bash
python -m pytest -v
```

Chạy file test:

```bash
python -m pytest tests/test_saucedemo.py -v
```

Chạy riêng một test case:

```bash
python -m pytest tests/test_saucedemo.py::test_login_success -v
```

Chạy toàn bộ test ở chế độ headless:

```bash
python -m pytest -v --headless
```

Mỗi test nhận một Chrome mới và fixture luôn gọi `quit()` sau khi test kết thúc, kể cả khi có lỗi. Các thao tác chờ phần tử/trang sử dụng explicit wait; không dùng `time.sleep()`.

Với giao diện React hiện tại, một số điều khiển của SauceDemo được kích hoạt bằng `element.click()` qua Selenium `execute_script`, sau đó test vẫn chờ và xác minh trạng thái giao diện. Cách này được dùng cho các nút/đường dẫn không ổn định khi Chrome headless mô phỏng click; nếu cần kiểm thử tọa độ chuột thực tế, có thể thay bằng `WebElement.click()` hoặc `ActionChains` và xác minh lại trên môi trường đích.

## 8. Danh sách test case

| ID | Tên test case | Mục tiêu | Tiền điều kiện | Dữ liệu kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|---|
| TC01 | Đăng nhập thành công | Xác minh tài khoản hợp lệ vào danh sách hàng | Website truy cập được | `standard_user` / `secret_sauce` | URL chứa `inventory.html`, danh sách sản phẩm hiển thị |
| TC02 | Đăng nhập sai thông tin | Kiểm tra lỗi khi thông tin không hợp lệ | Đang ở trang đăng nhập | `invalid_user` / `wrong_password` | Thông báo sai username/password hiển thị |
| TC03 | Username bỏ trống | Kiểm tra validation bắt buộc | Đang ở trang đăng nhập | Username trống, mật khẩu demo | Hiển thị “Epic sadface: Username is required” |
| TC04 | Thêm sản phẩm vào giỏ | Kiểm tra badge số lượng | Đã đăng nhập | Sauce Labs Backpack | Badge giỏ hàng hiển thị số `1` |
| TC05 | Xóa sản phẩm khỏi giỏ | Kiểm tra thao tác xóa | Đã đăng nhập | Sauce Labs Backpack | Giỏ trống, badge bị xóa |
| TC06 | Sắp xếp giá tăng dần | Kiểm tra thứ tự giá sau sắp xếp | Đã đăng nhập | Tùy chọn giá thấp đến cao | Dãy giá bằng dãy đã sắp xếp tăng dần |
| TC07 | Tên và giá trong giỏ | Kiểm tra dữ liệu sản phẩm giữa trang hàng và giỏ | Đã đăng nhập | Sauce Labs Backpack | Tên và giá trong giỏ trùng sản phẩm đã chọn |
| TC08 | Đăng xuất | Kiểm tra kết thúc phiên người dùng | Đã đăng nhập | Tài khoản demo | Quay lại trang đăng nhập |

## 9. Chi tiết các bước kiểm thử

| ID | Mục đích và tiền điều kiện | Các bước và dữ liệu đầu vào | Kết quả mong đợi và assertion |
|---|---|---|---|
| TC01 | Kiểm tra luồng đăng nhập; cần website hoạt động. | Mở trang; nhập `standard_user`, `secret_sauce`; nhấn Login. | Chờ URL có `inventory.html`; assertion xác nhận vùng danh sách sản phẩm hiển thị. |
| TC02 | Đảm bảo thông tin sai không đăng nhập được. | Mở trang; nhập `invalid_user`, `wrong_password`; nhấn Login. | Assertion kiểm tra thông báo lỗi chứa nội dung username/password không khớp. |
| TC03 | Xác minh kiểm tra trường bắt buộc. | Mở trang; để username trống; nhập `secret_sauce`; nhấn Login. | Assertion so sánh thông báo với `Epic sadface: Username is required`. |
| TC04 | Xác minh thêm hàng vào giỏ. | Đăng nhập bằng fixture; thêm `Sauce Labs Backpack`. | Assertion kiểm tra badge có giá trị số nguyên `1`. |
| TC05 | Xác minh xóa hàng đã chọn. | Đăng nhập; thêm ba lô; mở giỏ; nhấn Remove. | Assertion kiểm tra tên hàng không còn và badge giỏ hàng không tồn tại. |
| TC06 | Xác minh chức năng sắp xếp. | Đăng nhập; chọn `Price (low to high)`; đọc tất cả giá. | Assertion yêu cầu có nhiều giá và danh sách giá bằng bản sắp xếp tăng dần. |
| TC07 | Xác minh tính nhất quán thông tin hàng. | Đăng nhập; đọc giá ba lô ở danh sách; thêm vào giỏ và mở giỏ. | Assertion kiểm tra có tên sản phẩm và giá Decimal trong giỏ bằng giá ban đầu. |
| TC08 | Xác minh đăng xuất. | Đăng nhập; mở menu; chọn Logout. | Chờ nút Login hiển thị; assertion xác nhận URL trang đăng nhập. |

## 10. Kết quả thực nghiệm

Đã chạy thực tế ngày **23/10/2026** bằng `.venv\Scripts\python.exe -m pytest -v --headless` trên Chrome 155.0.8059.85, Python 3.12.8, Selenium 4.51.0 và Pytest 9.1.1. Lần xác minh cuối: **8 passed in 53.90s**.

| Test Case ID | Kết quả thực tế | Trạng thái | Ghi chú |
|---|---|---|---|
| TC01 | Chuyển đến trang danh sách; vùng sản phẩm hiển thị | PASS | Đăng nhập demo thành công |
| TC02 | Thông báo username/password không khớp hiển thị | PASS | Đăng nhập sai bị từ chối |
| TC03 | Thông báo username bắt buộc hiển thị | PASS | Validation hoạt động |
| TC04 | Badge giỏ hàng hiển thị số `1` | PASS | Đã thêm Sauce Labs Backpack |
| TC05 | Sản phẩm bị xóa; giỏ rỗng và badge biến mất | PASS | Xác minh sau thao tác Remove |
| TC06 | Danh sách giá bằng thứ tự tăng dần | PASS | Đã chọn Price (low to high) |
| TC07 | Tên và giá Sauce Labs Backpack trong giỏ khớp | PASS | Giá được so sánh bằng Decimal |
| TC08 | Quay lại trang đăng nhập sau Logout | PASS | Nút Login hiển thị |

## 11. Phân tích kết quả

- Tổng test case: 8.
- PASS: 8; FAIL: 0; NOT RUN: 0.
- Tỷ lệ thành công: 100% (8/8 test trong lần chạy nêu trên).
- Trong quá trình hoàn thiện, lần chạy đầu phát hiện thao tác menu và một số điều khiển React chưa được kích hoạt ổn định bằng click chuột headless. Locator/kiểu kích hoạt đã được điều chỉnh; lần chạy đầy đủ cuối cùng đạt 8/8 PASS.

## 12. Ưu điểm, hạn chế và hướng phát triển

- Page Object giúp tách locator/thao tác màn hình khỏi kịch bản kiểm thử.
- Fixture tạo trình duyệt riêng cho từng test, hạn chế phụ thuộc trạng thái và luôn đóng trình duyệt.
- `data-test` là locator dễ đọc; tuy nhiên thay đổi giao diện/thuộc tính của website vẫn có thể làm test cần cập nhật.
- Một số điều khiển React dùng `execute_script` để phát sự kiện click; cách này xác minh luồng giao diện nhưng không mô phỏng hoàn toàn tọa độ chuột vật lý.
- Website demo và driver phụ thuộc Internet; chờ điều kiện bằng explicit wait giảm lỗi do tải trang chậm nhưng không thể loại bỏ gián đoạn bên ngoài.
- Có thể mở rộng kiểm thử checkout, xác thực dữ liệu, trình duyệt khác, chụp ảnh lỗi và báo cáo HTML hoặc tích hợp CI/CD.

## 13. Kết luận

Project áp dụng Python, Selenium WebDriver, Pytest fixture, explicit wait và Page Object để tự động hóa 8 luồng SauceDemo. Trong lần chạy thực tế được ghi nhận, cả 8 test đều PASS; kết quả này chỉ phản ánh trạng thái website và môi trường tại thời điểm chạy.

## 14. Tài liệu tham khảo

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Documentation](https://docs.python.org/3/)
- [SauceDemo](https://www.saucedemo.com/)

## 15. Thông tin repository

**GitHub Repository:** Chưa cập nhật
