# Here is some starter code to get the data:
import streamlit as st
from sklearn.datasets import fetch_openml
import altair as alt

@st.cache_data
def load_data():
    titanic_sklearn = fetch_openml('titanic', version = 1, as_frame = True)
    return titanic_sklearn.frame

df = load_data()

st.title('Titanic Data')

#fare histogram by class
st.header('Average Fare by Class')
fare_by_class = df.groupby('pclass')['fare'].mean().reset_index()
st.bar_chart(fare_by_class.set_index('pclass'))
min_fare = df['fare'].min()
max_fare = df['fare'].max()
st.write(f'Minimum Fare: ${min_fare:.2f}')
st.write(f'Maximum Fare: ${max_fare:.2f}')

#sidebar
st.sidebar.header('Passengers by Gender and Class')
sex_filter = st.sidebar.radio(
    'Select Sex',
    options=['All', 'male', 'female'],
    index=0 
)
class_filter = st.sidebar.radio(
    'Select Passenger Class',
    options=['All', 1, 2, 3],
    index=0
)

filtered_df = df.copy()

if sex_filter != 'All':
    filtered_df = df[df['sex'] == sex_filter]
if class_filter != 'All':
    filtered_df = filtered_df[filtered_df['pclass'] == class_filter]


st.sidebar.subheader('Passenger Info')
st.sidebar.dataframe(filtered_df)

#survival by class, age, and sex
st.title('Titanic Survival Analysis')

age_min, age_max = st.slider(
    'Select Age Range', min_value=0, max_value=85, value = (20,40)
)

select_class = st.selectbox('Select Passenger Class', options=['All', '1', '2', '3'])

filtered_data = df[(df['age'] >= age_min) & (df['age'] <= age_max)]


if select_class != 'All':
    filtered_data = filtered_data[filtered_data['pclass'] == int(select_class)]

male_data = filtered_data[filtered_data['sex'] == 'male']
female_data = filtered_data[filtered_data['sex'] == 'female']


def prepare_chart_data(data, gender):
    chart_data = data.groupby('survived').size().reset_index(name='count')
    chart_data['status'] = chart_data['survived'].replace({0: 'Deceased', 1: 'Survived'})
    chart_data['gender'] = gender
    return chart_data

male_chart_data = prepare_chart_data(male_data, 'Male')
female_chart_data = prepare_chart_data(female_data, 'Female')

col1, col2 = st.columns(2)

with col1:
    st.subheader('Male Survival')
    male_chart = alt.Chart(male_chart_data).mark_bar().encode(
        x=alt.X('status:N', title='Survival Status'),
        y=alt.Y('count:Q', title='Number of Passengers'),
        color=alt.Color('status:N', title='Survival Status')
    ).properties(title='Male Survival Count', width=300)
    st.altair_chart(male_chart, use_container_width=True)

with col2:
    st.subheader('Female Survival')
    female_chart = alt.Chart(female_chart_data).mark_bar().encode(
        x=alt.X('status:N', title='Survival Status'),
        y=alt.Y('count:Q', title='Number of Passengers'),
        color=alt.Color('status:N', title='Survival Status')
    ).properties(title='Female Survival Count', width=300)
    st.altair_chart(female_chart, use_container_width=True)
