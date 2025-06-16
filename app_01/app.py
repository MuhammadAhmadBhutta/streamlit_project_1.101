import streamlit as st
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
import google.generativeai as genai

# --- Page Config ---
st.set_page_config(page_title="💬 Gemini Chatbot", layout="centered")

# --- API KEY Input ---
api_key = st.text_input("🔑 Enter Gemini API Key", type="password")

# --- Initialize Gemini ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

# --- Session States ---
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = "uploader_1"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "analysis_outputs" not in st.session_state:
    st.session_state.analysis_outputs = []

# --- Function: Get Gemini Response ---
def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"

# --- Function: Export chat to TXT ---
def export_chat_to_txt(messages):
    txt = ""
    for msg in messages:
        role = "You" if msg["role"] == "user" else "Gemini"
        txt += f"{role}: {msg['content']}\n\n"
    return txt

# --- Function: Export chat to PDF ---
def export_chat_to_pdf(messages):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFont("Helvetica", 11)
    width, height = 595, 842
    y = height - 40
    for msg in messages:
        role = "You" if msg["role"] == "user" else "Gemini"
        lines = [f"{role}: {msg['content']}"]
        for line in lines:
            split_lines = line.split('\n')
            for part in split_lines:
                if y < 40:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 11)
                    y = height - 40
                pdf.drawString(40, y, part[:1000])
                y -= 20
    pdf.save()
    buffer.seek(0)
    return buffer

# --- Function: Display formatted response ---
def display_response(title, content):
    st.markdown("---")
    st.markdown(f"### 🧠 {title}")
    st.markdown(content)

# --- Title ---
st.title("🤖 Gemini 2.0 Flash Chatbot")

# --- Chat Input ---
user_input = st.text_input("💬 You:", key="user_input")

if st.button("Send", disabled=not api_key):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = get_gemini_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# --- File Upload & Analysis ---
uploaded_file = st.file_uploader("📁 Upload file (image/text/pdf)", type=["png", "jpg", "jpeg", "txt", "pdf"], key=st.session_state.uploader_key)
if uploaded_file and api_key:
    file_type = uploaded_file.type
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    if file_type.startswith("image/"):
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="🖼️ Uploaded Image", use_container_width=True)
            response = model.generate_content([
                image,
                "Describe this image in detail like an expert analyst."
            ])
            st.session_state.analysis_outputs.append({
                "source": "🖼️ Image Analysis by Gemini",
                "content": response.text
            })
        except Exception as e:
            st.error(f"Failed to analyze image: {e}")

    elif file_type.startswith("text/"):
        try:
            content = uploaded_file.read().decode("utf-8")
            st.text_area("📄 Text File Content", content, height=200)
            analysis_prompt = f"Analyze this text file content in detail:\n\n{content}"
            response = get_gemini_response(analysis_prompt)
            st.session_state.analysis_outputs.append({
                "source": "📄 Text Analysis by Gemini",
                "content": response
            })
        except Exception as e:
            st.error(f"Failed to analyze text: {e}")

    else:
        st.info("📂 File uploaded. Preview not available.")

# --- Display Chat Messages ---
for msg in st.session_state.messages:
    role = "🧑‍💻 You" if msg["role"] == "user" else "🤖 Gemini"
    with st.chat_message(role):
        st.markdown(msg["content"])

# --- Display Analysis Outputs ---
for item in st.session_state.analysis_outputs:
    display_response(item["source"], item["content"])

# --- Export Options ---
txt_data = export_chat_to_txt(st.session_state.messages)
st.download_button("⬇️ Download TXT", txt_data, "chat.txt", mime="text/plain")

pdf_file = export_chat_to_pdf(st.session_state.messages)
st.download_button("⬇️ Download PDF", pdf_file, "chat.pdf", mime="application/pdf")

# --- Clear Chat Button ---
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.session_state.analysis_outputs = []
    st.session_state.input_key = f"user_input_{len(st.session_state.messages)}"
    st.session_state.uploader_key = f"uploader_{len(st.session_state.messages)}"
    st.rerun()
