# quebec_covid_webapp
Webapp to track covid cases in Quebec

This is a simple Web app I created with the Streamlit library to access covid data from the following sources:

* Case data: "https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_CasSelonStatutVaccinalEtAge.csv"
* Hospitalization data: "https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_HospitalisationsSelonStatutVaccinalEtAge.csv"

Using Pandas, I manipulated the data to plot them easily and categorize cases by age(Under 50, Over 50) and vaccine status.
