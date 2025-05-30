from backend.data_processing import generate_chart
from backend.data_processing import show_gender_distribution
#from backend.data_processing import selected_indicator, selected_year




def update_chart(state):
    state.chart_fig = generate_chart(state.selected_field)

# filter button
def filter_data(state):
    try:
        state.filtered_value = show_gender_distribution(state.selected_indicator, state.selected_year)
    except Exception as e:
        state.filtered_value = f"Fel: {e}"

