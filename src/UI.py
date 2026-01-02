import streamlit as st
from PIL import Image
import html
import ASCII_gen
import numpy as np
import cv2

st.set_page_config(page_title='ASCII Convertor', )
st.title('ASCII Convertor')

@st.cache_data(show_spinner=False)
def cached_make_ascii(img, **params):
    return ASCII_gen.make_ascii(img, **params)


if 'image' not in st.session_state:
    st.session_state['image'] = None
if 'ascii_art' not in st.session_state:
    st.session_state['ascii_art'] = None

image_type = st.selectbox('Upload Type', options=['Local File', 'Web File'])

if image_type=='Local File':
    file_image = st.file_uploader('Upload File', accept_multiple_files=False)

    if file_image:
        image = None
        try:
            image_PIL = Image.open(file_image)
            image = np.array(image_PIL)

        except Exception as e:
            st.error('Invaild File')
            print(e)

        if image is not None:
            st.session_state['image'] = image

elif image_type=='Web File':
    url = st.text_input('Enter URL')
    if url:
        image = None
        try:
            image = ASCII_gen.get_image_url(url)
            image =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            if image is not None:
                st.session_state['image'] = image
        except Exception as e:
            st.error('Invaild URL')
            print(e)

show_image = st.toggle('Show Selected Image')

if show_image:
    if st.session_state.image is not None:
        image_PIL = Image.fromarray(st.session_state.image)
        st.image(image_PIL, caption='ASCII Convertor', width='stretch')


with st.form('ascci_form'):

    with st.sidebar:
        st.title('ASCII Convertor Parameters')

        object_detection_method_str = st.selectbox('Object Detection Method',
                                                           options=['Segmentations', 'Thresholding'])

        object_detection_method = None

        if object_detection_method_str == 'Segmentations':
            object_detection_method = ASCII_gen.Mode.SEGMENTATION

        if object_detection_method_str == 'Thresholding':
            object_detection_method = ASCII_gen.Mode.THRESHOLD

        inverse_colors = st.toggle('Inverse Colors', value=False)

        histogram_normalization = st.toggle('Histogram Normalization', value=False)

        down_scale_factor = st.slider('Downscale Factor', 1, 128, value=32)

        threashold_value = st.slider('Threashold Value', 0, 255, value=128)

        padding_size = st.slider('Padding Size', 0, 32, value=10)
        padding_value = st.slider('Padding Value', 0, 255, value=0)



    convert_image = st.form_submit_button('Convert', disabled=st.session_state.image is None)

if convert_image:

    with st.spinner('Converting Image'):
       ascii_art_lines = ASCII_gen.make_ascii(st.session_state['image'],
                                              preprocess_mode=object_detection_method,
                                              down_scale_value=down_scale_factor,
                                              histogram_normalization=histogram_normalization,
                                              inverse_colors=inverse_colors,
                                              threshold=threashold_value,
                                              pad_len=padding_size,
                                              pad_value=padding_value
                                              )
    ascii_art_lines = [html.escape(line) for line in ascii_art_lines]

    ascii_art = '\n'.join(ascii_art_lines)
    st.session_state.ascii_art = ascii_art

if st.session_state.ascii_art:

    # ascii_art = html.escape(st.session_state.ascii_art)

    ascii_art = html.escape(st.session_state.ascii_art)
    num_lines = ascii_art.count('\n')+1
    font_size = 14
    line_height = 0.95
    padding = 10

    height_px = int(num_lines * line_height * font_size * padding)

    html_block = f"""
    <html>
    <head>
    <style>
    body {{
        margin: 0;
    }}
    pre {{
        font-family: 'JetBrains Mono', monospace;
        font-size: {font_size}px;
        line-height: {line_height};
        white-space: pre;          /* keep formatting */
        overflow-x: auto;          /* horizontal scroll */
        overflow-y: auto;          /* vertical scroll */
        width: max-content;        /* DO NOT wrap */
        padding: {padding // 2}px;
        color: white;
    }}
    .container {{
        overflow: auto;
        width: 100%;
        height: 600px;
    }}
    </style>
    </head>
    <body>
    <div class="container">
    <pre>{ascii_art}</pre>
    </div>
    </body>
    </html>
    """

    st.components.v1.html(html_block, height=height_px, scrolling=False)

    print()
    print(st.session_state.ascii_art)
