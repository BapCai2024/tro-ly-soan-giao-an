import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

# Cấu hình trang
st.set_page_config(page_title="Trợ Lý Soạn Giáo Án Tiểu Học", page_icon="📚")
st.title("📚 AI Soạn Giáo Án Tiểu Học (Theo CV 2345)")

# Nhập API Key
api_key = st.text_input("nhapmagooglekpi", type="password")

# Hàm đọc file PDF
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Hàm đọc file Word
def get_docx_text(docx_docs):
    text = ""
    for doc in docx_docs:
        doc_file = Document(doc)
        for para in doc_file.paragraphs:
            text += para.text + "\n"
    return text

if api_key:
    genai.configure(api_key=api_key)
    
    # Upload tài liệu
    uploaded_files = st.file_uploader("Tải lên tài liệu tham khảo (Sách GK, Tài liệu chuyên môn...)", 
                                      type=['pdf', 'docx'], accept_multiple_files=True)
    
    # Nhập yêu cầu cụ thể
    topic = st.text_area("Nhập tên bài dạy và yêu cầu cụ thể:", 
                         placeholder="Ví dụ: Soạn giáo án môn Tiếng Việt lớp 4, bài 'Cây gạo', dạy trong 2 tiết. Yêu cầu nhấn mạnh vào hoạt động nhóm.")
    
    if st.button("🚀 Soạn Giáo Án Ngay"):
        if not uploaded_files or not topic:
            st.warning("Vui lòng tải lên tài liệu và nhập yêu cầu!")
        else:
            with st.spinner("Đang đọc tài liệu và suy nghĩ..."):
                # Xử lý nội dung file
                raw_text = ""
                pdf_files = [f for f in uploaded_files if f.name.endswith('.pdf')]
                docx_files = [f for f in uploaded_files if f.name.endswith('.docx')]
                
                if pdf_files: raw_text += get_pdf_text(pdf_files)
                if docx_files: raw_text += get_docx_text(docx_files)

                # Cấu trúc lệnh (Prompt) chuyên cho giáo viên Tiểu học
                prompt = f"""
                Đóng vai là một giáo viên Tiểu học có kinh nghiệm và am hiểu Công văn 2345/BGDĐT-GDTH.
                Dựa vào tài liệu đính kèm bên dưới và yêu cầu: "{topic}".
                
                Hãy soạn một Kế hoạch bài dạy (Giáo án) chi tiết bao gồm:
                I. YÊU CẦU CẦN ĐẠT (Phẩm chất, Năng lực)
                II. ĐỒ DÙNG DẠY HỌC
                III. CÁC HOẠT ĐỘNG DẠY HỌC CHỦ YẾU (Chia rõ Hoạt động của GV và Hoạt động của HS)
                1. Khởi động
                2. Khám phá
                3. Luyện tập
                4. Vận dụng
                IV. ĐIỀU CHỈNH SAU BÀI DẠY
                
                Lưu ý: Ngôn ngữ sư phạm chuẩn mực, phù hợp tâm sinh lý học sinh tiểu học.
                
                Nội dung tài liệu tham khảo:
                {raw_text[:20000]} 
                """
                # Giới hạn text gửi đi để tránh lỗi quá tải token (khoảng 20k ký tự)

                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(prompt)
                    st.success("Đã soạn xong!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Có lỗi xảy ra: {e}")
else:
    st.info("Vui lòng nhập API Key để bắt đầu.")
