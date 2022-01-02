from numpy.lib.function_base import select
from pandas.core.indexes.datetimes import DatetimeIndex
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_cases = pd.read_csv('https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_CasSelonStatutVaccinalEtAge.csv',parse_dates=["Date"], index_col='Date')
df_hosp = pd.read_csv('https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_HospitalisationsSelonStatutVaccinalEtAge.csv',parse_dates=["Date"], index_col='Date')
df_cases = df_cases.rename(columns={'GrAge_Declaration':'Age','Nb_Nvx_Cas': 'Occurences'})
df_hosp = df_hosp.rename(columns={'GrAge_Admission':'Age','Nb_Nvelles_Hosp': 'Occurences'})


st.write("""
# Quebec Covid Case & Hospitalization Tracker
* Data Source: "https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/"
---

""")
col1, col2 = st.columns([2,2])

with st.form(key='my_key'):
    select_data = col1.selectbox('Select Data', ['Cases','Hospitalizations','Both'])
    select_age = col1.selectbox('Select Age Group',['Over 50', 'Under 50', 'All Ages'])
    select_dates = col1.selectbox('Date Range',['All Time ', 'Last 30 days'])


def dated(select_dates):
    if select_dates == 'Last 30 Days':
        return -30
    else:
        return

@st.cache(suppress_st_warning=True)
def transform_df(df='All',age='All',timeframe=0):
    if select_age == 'All Ages':
        df['Age'] = df['Age'].replace({'0-9 ans': 'Under 50','10-19 ans': 'Under 50','20-29 ans': 'Under 50','30-39 ans': 'Under 50','40-49 ans': 'Under 50'})
        df['Age'] = df['Age'].replace({'50-59 ans': 'Over 50','60-69 ans': 'Over 50','70-79 ans': 'Over 50','80-89 ans': 'Over 50','90 ans et plus': 'Over 50'})
        df = df[df['Age'] != 'Inconnu']
        df_pivot = pd.pivot_table(data=df, index= [df.index,'Age'] ,columns='Statut_Vaccinal', values='Occurences', aggfunc=np.sum).reset_index().rename_axis(None,axis=1)
        df_pivot['Total'] = df_pivot['Non-vacciné'] + df_pivot['Vacciné 1 dose'] + df_pivot['Vacciné 2 doses']
        df_pivot = df_pivot.groupby('Date').agg(np.sum).reset_index()
        df_output = df_pivot.iloc[timeframe:]

    else:
        df['Age'] = df['Age'].replace({'0-9 ans': 'Under 50','10-19 ans': 'Under 50','20-29 ans': 'Under 50','30-39 ans': 'Under 50','40-49 ans': 'Under 50'})
        df['Age'] = df['Age'].replace({'50-59 ans': 'Over 50','60-69 ans': 'Over 50','70-79 ans': 'Over 50','80-89 ans': 'Over 50','90 ans et plus': 'Over 50'})
        df = df[df['Age'] != 'Inconnu']
        df_pivot = pd.pivot_table(data=df, index= [df.index,'Age'] ,columns='Statut_Vaccinal', values='Occurences', aggfunc=np.sum).reset_index().rename_axis(None,axis=1)
        df_pivot['Total'] = df_pivot['Non-vacciné'] + df_pivot['Vacciné 1 dose'] + df_pivot['Vacciné 2 doses']
        df_output = df_pivot[df_pivot['Age'] == age]
        df_output = df_output.iloc[timeframe:]

   
    return df_output

def plot_Graph(data):
    if select_age == 'All Ages':
        fig, ax = plt.subplots()

        ax.plot(data['Date'],data['Non-vacciné'], label='Unvaccinated', color='blue')
        ax.set_ylabel('Cases', color='blue')

        ax.plot(data['Date'],data['Vacciné 1 dose'], label = '1 Dose')
        ax.plot(data['Date'],data['Vacciné 2 doses'], label = '2 Dose')
        plt.xticks(rotation=90)
        plt.legend()
        col2.write('Total ' + select_data + ' for ' + str(data.iloc[-1]['Date']) + ': ' + str(data.iloc[-1]['Total']))
        col2.write('% of ' + select_data  + ' unvaccinated' +': ' + str(data.iloc[-1]['Non-vacciné']/data.iloc[-1]['Total']*100) + '%')
        col2.write('% of ' + select_data + ' reltive to population' + ': ' + str(data.iloc[-1]['Non-vacciné']/1610000*100) + '%')
        col2.write('% of ' + select_data + ' Fully vaccinated' + ': ' + str(data.iloc[-1]['Vacciné 2 doses']/data.iloc[-1]['Total']*100)+ '%')
        col2.write('% of ' + select_data + ' reltive to population' + ': ' + str(data.iloc[-1]['Vacciné 2 doses']/6872850*100)+ '%')
        st.pyplot(fig)
    else:
        fig, ax = plt.subplots()

        ax.plot(data['Date'],data['Non-vacciné'], label='Unvaccinated', color='blue')
        ax.set_ylabel('Cases', color='blue')

        ax.plot(data['Date'],data['Vacciné 1 dose'], label = '1 Dose')
        ax.plot(data['Date'],data['Vacciné 2 doses'], label = '2 Dose')
        plt.xticks(rotation=90)
        plt.legend()
        col2.write('Total ' + select_data + ' for ' + str(data.iloc[-1]['Date']) + ': ' + str(data.iloc[-1]['Total']))
        col2.write('% of ' + select_data  + ' Unvaccinated' +': ' + str(data.iloc[-1]['Non-vacciné']/data.iloc[-1]['Total']*100) + '%')
        col2.write('% of ' + select_data + ' reltive to population' + ': ' + str(data.iloc[-1]['Non-vacciné']/1610000*100) + '%')
        col2.write('% of ' + select_data + ' Unvaccinated' + ': ' + str(data.iloc[-1]['Vacciné 2 doses']/data.iloc[-1]['Total']*100)+ '%')
        col2.write('% of ' + select_data + ' reltive to population' + ': ' + str(data.iloc[-1]['Vacciné 2 doses']/6872850*100)+ '%')


        st.pyplot(fig)

def plot_2_graphs():
    data = transform_df(df_cases,select_age,dated(select_dates))
    data2 = transform_df(df_hosp,select_age,dated(select_dates))
    fig, ax = plt.subplots()


    ax.plot(data['Date'],data['Total'], color='blue')
    ax.set_ylabel('Cases', color='blue')
    # ax.plot(data['Date'],data['Vacciné 1 dose'], label = '1 Dose')
    # ax.plot(data['Date'],data['Vacciné 2 doses'], label = '2 Dose')
    ax.legend()

    ax2 = ax.twinx()
    ax2.plot(data2['Date'],data2['Total'], label='Hospitalization',color = 'red')
    ax2.set_ylabel('Hospilizations', color='red')
    # ax2.plot(data2['Date'],data2['Vacciné 1 dose'], label = '1 Dose')
    # ax2.plot(data2['Date'],data2['Vacciné 2 doses'], label = '2 Dose')

    plt.xticks(rotation=90)
    st.pyplot(fig)
    st.write(str(data.iloc[-1]['Date']) + ': ' + str(data.iloc[-1]['Total']))

# plot_Graph(transform_df (df_cases,'Under 50',dated('Last 30 days')))



if select_data == 'Cases':
    plot_Graph(transform_df(df_cases,select_age,dated(select_dates)))
elif select_data == 'Hospitalizations':
    plot_Graph(transform_df(df_hosp,select_age,dated(select_dates)))
else:
    plot_2_graphs()



