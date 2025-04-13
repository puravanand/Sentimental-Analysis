import streamlit as st
import pandas as pd
from textblob import TextBlob
from time import sleep  # Sleep function for simulating a long task


# Page settings
st.set_page_config(page_title="💬 Sentiment Analyzer", page_icon="🔥", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4B0082;'>🔥 Sentiment Analyzer for Product Reviews 🔥</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyze customer feelings using <b>TextBlob NLP</b> — Type or Upload!</p>", unsafe_allow_html=True)
st.write("---")

# ---------- Option 1: Text Input ----------
st.subheader("📝 Analyze Single Review (Manual Input)")
text_input = st.text_area("Enter your review:")

if st.button("🔍 Analyze Text"):
    if text_input:
        blob = TextBlob(text_input)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            result = "🟢 Positive"
        elif polarity < 0:
            result = "🔴 Negative"
        else:
            result = "🟡 Neutral"
        st.success(f"**Sentiment:** {result} (Polarity Score: {polarity:.2f})")
    else:
        st.warning("⚠️ Please enter some text!")

st.write("---")

# ---------- Option 2: CSV Upload ----------
st.subheader("📂 Bulk Review Analysis (Upload CSV)")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        with st.spinner('Processing your file... Please wait!'):
            sleep(2) 
        df = pd.read_csv(uploaded_file,encoding='latin1')
        df=df.head(1000)
        
        review_col=[col for col in df.columns if 'review' in col.lower()]
        if review_col:
          review_col_sel= st.selectbox("Select only Review column:- ",review_col)
          with st.spinner("Hang tight! We're analyzing your data..."):
            sleep(30)
          #DATA CLEANING
          # if already there is semintel analysis  column present in  our csv file  then remove it
          
          
          # possible name of sentimental column names
          possible_sentimental_keyword=['sentiment','emotions','polarity','opinion','label']
          
          # create a empty list which contains deleted  sentimental relatted columns
          deleted_col= []
          
          for col in df.columns:
            for keywords in possible_sentimental_keyword:
              if keywords in col.lower():
                deleted_col.append(col)
                break
              
          if deleted_col:
            df.drop(deleted_col,inplace=True,axis=1)
        
        
        
          # Remove the missing values from the Review Row
          df.dropna(subset=[review_col_sel],inplace=True)    
          # st.write(df.isnull().sum())
          
          # Remove the duplicates
          df.drop_duplicates(subset=[review_col_sel],inplace=True)
          
          # convert all values into the lowerCase
          df[review_col_sel]=df[review_col_sel].str.lower()
        
          # Remove  the unwanted character from here 
          df[review_col_sel]=df[review_col_sel].str.replace(r'[^a-zA-Z\s]','',regex=True)
          df[review_col_sel] = df[review_col_sel].str.strip()
          
          # correct each spelling 
          from spellchecker import SpellChecker
          spell=SpellChecker()
          corrected_review=[]
          for review in df[review_col_sel]:
            words=review.split()
            corrected_words=[]
            for word in words:
              correct_word=spell.correction(word)
              if correct_word is None:
                correct_word=""
              corrected_words.append(correct_word)
            correct_review=' '.join(corrected_words)
            corrected_review.append(correct_review)
          df[review_col_sel]=corrected_review
          def get_polarity(text):
            return TextBlob(text).sentiment.polarity
          df['Polarity'] = df[review_col_sel].apply(get_polarity)
          def get_sentiment(polarity):
            if polarity > 0:
              return "🟢 Positive"
            elif polarity < 0:
              return "🔴 Negative"
            else:
              return "🟡 Neutral"
          df['Sentiment'] = df['Polarity'].apply(get_sentiment)
          st.info("📄 Sentimental Analysis of uploaded data:")
          st.dataframe(df)


            
          

          
          
          
          
          
          
          
          
          
          
          
        else:
          st.error("❌ Review Column Not exists,upload another CSV which contains review column")
          
          
          

        
        
          

          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          

        # if 'review' in df.columns:
        # st.info("📄 Sentimental Analysis of uploaded data:")
       
        # st.write(len(df))
        # st.dataframe(df)

   

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
# import nltk 
# nltk.download('punkt')
