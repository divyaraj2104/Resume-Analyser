import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel


def load_data(data):
	df = pd.read_csv(data)
	return df


def vectorize_text_to_cosine_mat(data):
	count_vect = CountVectorizer()
	cv_mat = count_vect.fit_transform(data)
	cosine_sim_mat = cosine_similarity(cv_mat)
	return cosine_sim_mat


@st.cache
def get_recommendation(title, cosine_sim_mat, df, num_of_rec=10):
	course_indices = pd.Series(
	    df.index, index=df['course_title']).drop_duplicates()
	idx = course_indices[title]
	sim_scores = list(enumerate(cosine_sim_mat[idx]))
	sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
	selected_course_indices = [i[0] for i in sim_scores[1:]]
	selected_course_scores = [i[0] for i in sim_scores[1:]]
	result_df = df.iloc[selected_course_indices]
	result_df['similarity_score'] = selected_course_scores
	final_recommended_courses = result_df[[
	    'course_title', 'similarity_score', 'url', 'price', 'num_subscribers']]
	return final_recommended_courses.head(num_of_rec)


RESULT_TEMP = """
<div style="width:90%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 60px;
box-shadow:0 0 15px 5px #ccc; background-color: #000080;
  border-left: 5px solid #6c6c6c;">
<h4 style="color:white">{}</h4>
<p style="color:white;"><span style="color:white;"></span>{}</p>
<p style="color:white;"><span style="color:white;">Score::</span>{}</p>
<p style="color:white;"><span style="color:white;">Link:</span><a href="{}",target="_blank">Link</a></p>
<p style="color:white;"><span style="color:white;">Price:</span>{}</p>
<p style="color:white;"><span style="color:white;"> Students:</span>{}</p>
</div>
"""


@st.cache
def search_term_if_not_found(term, df):
	result_df = df[df['course_title'].str.contains(term)]
	return result_df


def main():
	st.title("Course Recommendation Module")
	menu = ["Recommend", "Home", "About"]
	choice = st.sidebar.selectbox("Menu", menu)
	df = load_data(r"C:\Users\rct14\Desktop\8thsem\project\python\CourseRecommendation\udemy_courses.csv")
	if choice == "Home":
		st.subheader("Home")
		st.dataframe(df.head(500))
	elif choice == "Recommend":
		st.subheader("Recommend Courses")
		cosine_sim_mat = vectorize_text_to_cosine_mat(df['course_title'])
		search_term = st.text_input("Search")
		# num_of_rec = st.sidebar.number_input("Number", 4, 30, 7)
		num_of_rec = 7
		if st.button("Recommend"):
			if search_term is not None:
				try:
					results = get_recommendation(search_term, cosine_sim_mat, df, num_of_rec)
					with st.beta_expander("Results as JSON"):
						results_json = results.to_dict('index')
						st.write(results_json)

					for row in results.iterrows():
						rec_title = row[1][0]
						rec_score = row[1][1]
						rec_url = row[1][2]
						rec_price = row[1][3]
						rec_num_sub = row[1][4]
						stc.html(RESULT_TEMP.format(rec_num_sub, rec_score, rec_title,
						         rec_url, rec_price, cnt), height=700)
				except Exception as e:
					results= e
					st.warning(results)
					st.info("Suggested Options include")
					result_df = search_term_if_not_found(search_term,df)
					# st.dataframe(result_df)
					cnt=0
					for row in result_df.iterrows():
						rec_title = row[1][0]
						cnt=cnt+1
						rec_score = row[1][1]
						rec_url = row[1][2]
						rec_price = row[1][3]
						rec_num_sub = row[1][4]
						stc.html(RESULT_TEMP.format(cnt, rec_score, rec_num_sub,
						         rec_url, rec_price, rec_title), height=280)
					
	else:
		st.subheader("Smart Resume Analyzer")
if __name__ == '__main__':
	main()
 
 