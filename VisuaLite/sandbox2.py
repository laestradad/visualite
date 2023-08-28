import plotly.express as px
fig = px.colors.qualitative.swatches()
fig.write_html('test.html')

print(px.colors.qualitative.G10[10])

