import os
import streamlit as st
from image_generator import generate_image, decode_base64
from time import sleep

def local_css(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    css_path = os.path.join(dir_path, file_name)
    
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Arquivo CSS não encontrado em: {css_path}")

def main():
    st.set_page_config(
        page_title="🔥 DARK GENERATOR",
        page_icon="🖤",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CSS Customizado - Tema Vermelho/Preto
    st.markdown("""
    <style>
    :root {
        --primary: #ff2a2a;
        --secondary: #cc0000;
        --dark: #0a0a0a;
        --light: #ffffff;
    }
    
    .stApp {
        background-color: var(--dark);
        color: var(--light);
        font-family: 'Segoe UI', sans-serif;
    }
    
    .stTextArea>div>div>textarea, 
    .stSelectbox>div>div>select, 
    .stSlider>div>div>div>div {
        background-color: #1a1a1a !important;
        color: var(--light) !important;
        border: 1px solid var(--primary) !important;
        border-radius: 4px !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 8px rgba(255, 42, 42, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(255, 42, 42, 0.4) !important;
    }
    
    .header {
        border-bottom: 3px solid var(--primary);
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    }
    
    .header h1 {
        color: var(--primary);
        font-size: 2.8rem;
        text-shadow: 0 2px 4px rgba(255, 42, 42, 0.3);
        letter-spacing: -0.5px;
    }
    
    .stAlert {
        background-color: #1a1a1a !important;
        border-left: 4px solid var(--primary) !important;
    }
    
    .stSpinner>div>div {
        border-top-color: var(--primary) !important;
    }
    
    .stExpander>div>div {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class='header'>
            <h1>🔥 DARK GENERATOR</h1>
            <p>Generate hauntingly beautiful AI art</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("⚙️ CORE SETTINGS")
        engine_options = {
            "Stable Diffusion v1.6": "stable-diffusion-v1-6",
            "Stable Diffusion 512 v2.1": "stable-diffusion-512-v2-1",
            "Stable Diffusion XL": "stable-diffusion-xl-1024-v1-0"
        }
        selected_engine = st.selectbox("AI MODEL:", list(engine_options.keys()))
        
        size_options = ["512x512", "768x768", "1024x1024"]
        selected_size = st.selectbox("RESOLUTION:", size_options)
        
        advanced = st.expander("⚡ ADVANCED CONFIG")
        with advanced:
            cfg_scale = st.slider("CREATIVITY (CFG)", 1.0, 20.0, 7.0)
            steps = st.slider("DETAIL LEVEL", 10, 150, 30)
            samples = st.slider("IMAGE COUNT", 1, 4, 1)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        with st.form("prompt_form"):
            prompt = st.text_area(
                "YOUR DARK VISION:",
                placeholder="A crimson demon standing in ruined cathedral, hyper-detailed dark fantasy art",
                height=150
            )
            
            negative_prompt = st.text_area(
                "WHAT TO AVOID:",
                placeholder="bright colors, cartoon style, low quality",
                height=100
            )
            
            generate_button = st.form_submit_button(
                "🔥 SUMMON IMAGE",
                use_container_width=True
            )
    
    with col2:
        st.markdown("### 🔍 PREVIEW")
        image_placeholder = st.empty()
        image_placeholder.image("https://i.imgur.com/9p5SFLW.png", use_column_width=True)  # Imagem placeholder dark
        
        download_placeholder = st.empty()
    
    if generate_button and prompt:
        with st.spinner("🔥 CONJURING DARK VISIONS..."):
            try:
                width, height = map(int, selected_size.split("x"))
                
                response = generate_image(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    engine_id=engine_options[selected_engine],
                    steps=steps,
                    cfg_scale=cfg_scale,
                    samples=samples
                )
                
                if response and 'artifacts' in response:
                    st.balloons()
                    st.success("""
                    🔥 **SUMMONING SUCCESSFUL**  
                    *The dark energies have manifested your vision*
                    """)
                    
                    for idx, image in enumerate(response['artifacts']):
                        img_data = f"data:image/png;base64,{image['base64']}"
                        image_placeholder.image(img_data, use_column_width=True)
                        
                        download_placeholder.download_button(
                            label="⬇️ CLAIM IMAGE",
                            data=decode_base64(image['base64']),
                            file_name=f"dark_vision_{idx+1}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                else:
                    with st.empty():
                        for i in range(3):
                            st.error("🔥 DARK ENERGY UNSTABLE...")
                            sleep(0.3)
                            st.error("🔥🔥 ENTITY NOT RESPONDING...")
                            sleep(0.3)
                        st.error("""
                        💀 **SUMMONING FAILED**  
                        *The ancient ones remain silent*  
                        Try:  
                        - Strengthening your ritual (check connection)  
                        - Different incantation (new prompt)  
                        - Waiting for the stars to align (retry later)
                        """)
            
            except Exception as e:
                with st.empty():
                    for i in range(3):
                        st.error(f"💥 DIMENSIONAL COLLAPSE... {str(e)[:30]}")
                        sleep(0.3)
                    st.error(f"""
                    🩸 **ELDRITCH ERROR**  
                    `{str(e)}`  
                    *The forbidden knowledge remains elusive...*
                    """)

if __name__ == "__main__":
    main()