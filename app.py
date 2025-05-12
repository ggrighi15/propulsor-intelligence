
import os
import streamlit.web.bootstrap

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    streamlit.web.bootstrap.run("app.py", "", [], port=port)
