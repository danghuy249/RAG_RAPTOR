import os
from dotenv import load_dotenv
from raptor import RetrievalAugmentation

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Bước 1: Thiết lập môi trường và cấu hình RAPTOR
# Khởi tạo với cấu hình mặc định
RA = RetrievalAugmentation()

# Bước 2: Thêm tài liệu vào cây truy vấn để index
# Đọc tài liệu từ file sample.txt
try:
    with open('sample.txt', 'r') as file:
        text = file.read()
    RA.add_documents(text)
except FileNotFoundError:
    print("File 'sample.txt' không tồn tại. Hãy đảm bảo file có mặt trong thư mục hiện tại.")
    exit()

# Bước 3: Thực hiện câu hỏi để tìm câu trả lời từ tài liệu đã index
question = "How did Cinderella reach her happy ending?"
answer = RA.answer_question(question=question)
print("Answer: ", answer)

# Bước 4: Lưu cây truy vấn đã xây dựng vào đường dẫn chỉ định
SAVE_PATH = "demo/cinderella"
RA.save(SAVE_PATH)

# Bước 5: Tải lại cây truy vấn đã lưu và tiếp tục sử dụng RAPTOR
RA = RetrievalAugmentation(tree=SAVE_PATH)
answer = RA.answer_question(question=question)
print("Answer after loading tree: ", answer)

# Lưu ý:
# Hãy đảm bảo bạn đã cài đặt tất cả phụ thuộc trước khi chạy file này:
# pip install -r requirements.txt
