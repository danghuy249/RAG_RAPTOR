# Import thư viện os để làm việc với hệ thống
import os
# Import thư viện dotenv để đọc biến môi trường từ file .env
from dotenv import load_dotenv
# Import class RetrievalAugmentation từ module raptor
from raptor import RetrievalAugmentation

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy API key từ biến môi trường và gán vào biến môi trường OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Bước 1: Thiết lập môi trường và cấu hình RAPTOR
# Khởi tạo đối tượng RetrievalAugmentation với cấu hình mặc định
RA = RetrievalAugmentation()

# Bước 2: Thêm tài liệu vào cây truy vấn để index
# Đọc nội dung từ file sample.txt
try:
    # Mở và đọc file sample.txt
    with open('demo/sample.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    # Thêm nội dung văn bản vào cây truy vấn
    RA.add_documents(text)
except FileNotFoundError:
    # In thông báo lỗi nếu không tìm thấy file
    print("File 'sample.txt' không tồn tại. Hãy đảm bảo file có mặt trong thư mục hiện tại.")
    exit()
except Exception as e:
    print(f"Có lỗi xảy ra khi đọc file: {str(e)}")
    exit()

# Bước 3: Thực hiện câu hỏi để tìm câu trả lời từ tài liệu đã index
# Định nghĩa câu hỏi cần tìm câu trả lời
question = "How did Cinderella reach her happy ending?"
try:
    # Gọi hàm trả lời câu hỏi từ cây truy vấn
    answer = RA.answer_question(question=question)
    # In câu trả lời ra màn hình
    print("Answer: ", answer)
except Exception as e:
    print(f"Có lỗi xảy ra khi trả lời câu hỏi: {str(e)}")
    exit()

# Bước 4: Lưu cây truy vấn đã xây dựng vào đường dẫn chỉ định
# Định nghĩa đường dẫn lưu cây truy vấn
SAVE_PATH = "demo/cinderella"
try:
    # Lưu cây truy vấn vào đường dẫn đã chỉ định
    RA.save(SAVE_PATH)
except Exception as e:
    print(f"Có lỗi xảy ra khi lưu cây truy vấn: {str(e)}")
    exit()

# Bước 5: Tải lại cây truy vấn đã lưu và tiếp tục sử dụng RAPTOR
try:
    # Tạo đối tượng RetrievalAugmentation mới với cây truy vấn đã lưu
    RA = RetrievalAugmentation(tree=SAVE_PATH)

    tree = RA.tree
    nodes = tree.all_nodes
    n_layers = tree.num_layers
    tree.root_nodes
except Exception as e:
    print(f"Có lỗi xảy ra khi tải lại cây truy vấn: {str(e)}")
    exit()

def print_tree_layers(root_nodes):
    """
    Iterates over the tree from the root nodes and prints node index and text layer by layer.

    Args:
      root_nodes: A dictionary mapping node index to Node objects.
    """
    if not root_nodes:
        print("Không có root nodes để hiển thị")
        return
        
    all_nodes = tree.all_nodes
    current_layer = list(root_nodes.values())  # Convert root_nodes to a list for iteration
    level = 0
    while current_layer:
        print(f"================= Level {level} ================= ")
        next_layer = []
        for node in current_layer:
            if node:  # Check if node exists
                print(f"Index: {node.index}, Text: {node.text}\n")
                next_layer.extend(all_nodes.get(child_index) for child_index in node.children if child_index in all_nodes)
        
        current_layer = [node for node in next_layer if node]  # Filter out None values
        level += 1

try:
    print_tree_layers(tree.root_nodes)

    # Thực hiện truy vấn lại với cây đã tải
    answer = RA.answer_question(question=question)
    # In kết quả sau khi tải lại cây truy vấn
    print("Answer after loading tree: ", answer)
except Exception as e:
    print(f"Có lỗi xảy ra khi in cây hoặc truy vấn lại: {str(e)}")

# Lưu ý:
# Hãy đảm bảo bạn đã cài đặt tất cả phụ thuộc trước khi chạy file này:
# pip install -r requirements.txt
