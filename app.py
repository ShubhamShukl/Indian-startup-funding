import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Indian Startup Funding Analysis app')

# df = pd.read_csv('startup_funding.csv')
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

def load_overall_analysis():
    st.title('Overall Analysis')
    col1,col2,col3,col4 = st.columns(4)

    # total invested amount
    with col1:
        total = round(df['amount'].sum())
        st.metric('Total investment', str(total)+' Cr')

    # maximum amount infused
    with col2:
        # max_investment_in = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).index[0]
        max_investment = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        # st.metric('Maximum amount invested in','Startup: ' + max_investment_in)
        st.metric('Amount: ',str(max_investment)+' Cr')

    # average funding
    with col3:
        avg_fund = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('Average funding: ', str(avg_fund)+' Cr')

    # total startup funded
    with col4:
        num_startup = df['startup'].nunique()
        st.metric('Total Funded Startups: ', num_startup)

    st.header('MoM Graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig6, ax6 = plt.subplots()
    ax6.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig6)


def load_investor_details(investor):
    st.title(investor)
    # recent 5 invests
    last_5df = df[df['investors'].str.contains(investor)].head(5)[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('most recent investments')
    st.dataframe(last_5df)

    col1,col2 = st.columns(2)

    with col1:
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False)
        st.subheader('Biggest investments')
        # st.dataframe(big_series)
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels = vertical_series.index, autopct='%0.5f%%')
        st.pyplot(fig1)

    col3, col4 = st.columns(2)

    with col3:
        stagewise_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Stages invested')
        fig2, ax2 = plt.subplots()
        ax2.pie(stagewise_series, labels=stagewise_series.index, autopct='%0.5f%%')
        st.pyplot(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Cities invested')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index , autopct='%0.5f%%')
        st.pyplot(fig3)

    # year-on-year graph

    yoy_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YoY investments')
    fig4, ax4 = plt.subplots()
    ax4.plot(yoy_series.index,yoy_series.values)
    st.pyplot(fig4)

# st.dataframe(df.describe())

st.sidebar.title('Startup funding analysis')
options = st.sidebar.selectbox('Select', ['Overall analysis','Startup','Investor analysis'])

if options == 'Overall analysis':
    # st.title('Overall analysis')
    load_overall_analysis()
    # btn0 = st.sidebar.button('Show overall analysis')
    # if btn0:
        #load_overall_analysis()
elif options == 'Startup':
    st.sidebar.selectbox('Select startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
elif options == 'Investor analysis':
    selected_investor = st.sidebar.selectbox('Investor analysis',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
    # st.title('Investor Analysis')