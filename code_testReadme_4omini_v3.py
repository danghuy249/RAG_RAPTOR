# Import thư viện os để làm việc với hệ thống
import os
# Import thư viện dotenv để đọc biến môi trường từ file .env
from dotenv import load_dotenv
# Import class RetrievalAugmentation từ module raptor
from raptor import RetrievalAugmentation, RetrievalAugmentationConfig

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy API key từ biến môi trường và gán vào biến môi trường OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Bước 1: Thiết lập môi trường và cấu hình RAPTOR
# Tạo config với các tham số tùy chỉnh
config = RetrievalAugmentationConfig(
    # Cấu hình cho TreeBuilder
    tb_num_layers=3,              # Số layer trong cây (mặc định là 5)
    tb_top_k=3,                   # Số nodes được chọn trong mỗi layer
    tb_max_tokens=100,            # Số token tối đa cho mỗi node
    
    # Cấu hình cho TreeRetriever
    tr_top_k=5,                   # Số nodes được retrieve trong mỗi query
    tr_num_layers=2,              # Số layer được dùng để retrieve
    
    # Cấu hình cho ClusterTreeBuilder
    tree_builder_type="cluster",  # Loại tree builder
    tb_cluster_embedding_model="OpenAI",  # Model embedding cho clustering
    reduction_dimension=3,        # Số nodes tối đa trong mỗi cluster
)

# Khởi tạo RetrievalAugmentation với config
RA = RetrievalAugmentation(config=config)

# Bước 2: Thêm tài liệu vào cây truy vấn để index
# Đọc nội dung từ file sample.txt
try:
    # Mở và đọc file sample.txt
    with open('demo/sample.txt', 'r') as file:
        text = file.read()
    # Thêm nội dung văn bản vào cây truy vấn
    RA.add_documents(text)
except FileNotFoundError:
    # In thông báo lỗi nếu không tìm thấy file
    print("File 'sample.txt' không tồn tại. Hãy đảm bảo file có mặt trong thư mục hiện tại.")
    exit()

# Bước 3: Thực hiện câu hỏi để tìm câu trả lời từ tài liệu đã index
# Định nghĩa câu hỏi cần tìm câu trả lời
question = "How did Cinderella reach her happy ending?"
# Gọi hàm trả lời câu hỏi từ cây truy vấn
answer = RA.answer_question(question=question)
# In câu trả lời ra màn hình
print("Answer: ", answer)

# Bước 4: Lưu cây truy vấn đã xây dựng vào đường dẫn chỉ định
# Định nghĩa đường dẫn lưu cây truy vấn
SAVE_PATH = "demo/cinderella"
# Lưu cây truy vấn vào đường dẫn đã chỉ định
RA.save(SAVE_PATH)

# Bước 5: Tải lại cây truy vấn đã lưu và tiếp tục sử dụng RAPTOR
# Tạo đối tượng RetrievalAugmentation mới với cây truy vấn đã lưu
RA = RetrievalAugmentation(tree=SAVE_PATH)
# Thực hiện truy vấn lại với cây đã tải
answer = RA.answer_question(question=question)
# In kết quả sau khi tải lại cây truy vấn
print("Answer after loading tree: ", answer)

# Kiểm tra cây đã được tạo chưa
tree_path = os.path.join(SAVE_PATH, "tree.pkl")
print(f"\nKiểm tra cây:")
print(f"- Đường dẫn đầy đủ: {os.path.abspath(SAVE_PATH)}")
print(f"- File tree.pkl tồn tại: {os.path.exists(tree_path)}")

# Lưu ý:
# Hãy đảm bảo bạn đã cài đặt tất cả phụ thuộc trước khi chạy file này:
# pip install -r requirements.txt
