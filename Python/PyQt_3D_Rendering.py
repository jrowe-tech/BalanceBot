import plotly.graph_objects as go
import random
#import pandas as pd

pointAmount = 4
pointDisplacement = 1

randomPoints = lambda: [random.randrange(-pointDisplacement, pointDisplacement) for id in range(pointAmount)]

xPoints = randomPoints()
yPoints = randomPoints()
zPoints = randomPoints()

fig = go.Figure(data=[go.Mesh3d(
x = xPoints,
y = yPoints,
z = zPoints,
color='blue',
opacity=0.50)
]
)

fig.show()