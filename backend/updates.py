from backend.data_processing import generate_chart

def update_chart(state):
    state.chart_fig = generate_chart(state.selected_field)