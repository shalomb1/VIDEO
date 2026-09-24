from google import genai
from PIL import Image
import io
import streamlit as st

# הגדרת עמוד
st.set_page_config(
    page_title='Google Gemini Media Generator', page_icon='✨', layout='centered'
)

st.title('✨ יוצר תמונות חכם באמצעות Google Gemini')
st.write('הזן את מפתח ה-API של Google AI Studio ואת הפרומפט שלך.')

# אתחול זיכרון פנימי
if 'generated_image' not in st.session_state:
  st.session_state.generated_image = None
if 'prompt_used' not in st.session_state:
  st.session_state.prompt_used = None

# שדה להזנת מפתח ה-API של גוגל
api_key = st.text_input(
    'הכנס את מפתח ה-API של Google (Gemini API Key):', type='password'
)

# שדה טקסט לפרומפט
prompt = st.text_area(
    'הכנס פרומפט לתמונה:',
    value=(
        'A beautiful scenic landscape with mountains and a river, digital art,'
        ' high quality'
    ),
    height=100,
)

# כפתור הפעלה
if st.button('צור תמונה עם Google 🚀', type='primary'):
  if not api_key:
    st.error('אנא הכנס מפתח Google API תקין.')
  elif not prompt:
    st.error('אנא הכנס פרומפט.')
  else:
    try:
      with st.spinner('יוצר תמונה באמצעות Google Gemini, אנא המתן...'):
        # אתחול הלקוח של גוגל עם המפתח שהוזן
        client = genai.Client(api_key=api_key)

        # יצירת תמונה באמצעות מודל תומך (לדוגמה imagen או מודל פלאש תומך)
        # ניתן להתאים את שם המודל בהתאם לצרכים שלך
        result = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=prompt,
            config=dict(number_of_images=1, output_mime_type='image/jpeg'),
        )

        for generated_image in result.generated_images:
          image = Image.open(io.BytesIO(generated_image.image.image_bytes))
          st.session_state.generated_image = image
          st.session_state.prompt_used = prompt

    except Exception as e:
      st.error(f'אירעה שגיאה בעת הפנייה לשירותי גוגל: {e}')

# הצגת התוצאה מתוך הזיכרון
if st.session_state.generated_image is not None:
  st.success('התמונה נוצרה בהצלחה!')
  st.image(
      st.session_state.generated_image,
      caption=st.session_state.prompt_used,
      use_container_width=True,
  )