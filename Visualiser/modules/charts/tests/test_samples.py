import pandas as pd
from Visualiser.modules.charts.models import *


class ChartSampleGenerator(object):
    """
    Class for chart sample creating.
    """

    @staticmethod
    def create_chart():
        df = ChartSampleGenerator.create_data_source()
        chart = Chart()
        chart.data_source = df

        chart_options = ChartOptions()
        chart_options.title = ChartSampleGenerator.create_sample_title()
        chart_options.description = "TEST"
        chart_options.x_axis = ChartSampleGenerator.create_sample_axis("numbers")

        layer = ChartSampleGenerator.add_line_layer("squares")
        chart_options.layers.append(layer)

        chart.chart_options = chart_options
        return chart

    @staticmethod
    def create_data_source():
        data_source = []
        for i in range(30):
            data_source.append([i, i**2, i**3, "2017-11-" + str(i)])

        df = pd.DataFrame(data_source, columns=["numbers", "squares", "cubes", "dates"])

        return df

    @staticmethod
    def add_line_layer(column):
        layer = ChartLayer()
        layer.axis = ChartSampleGenerator.create_sample_axis(column)
        layer.figure = ChartSampleGenerator.create_line()

        return layer

    @staticmethod
    def create_line():
        line = ChartFigure()
        line.colour = "purple"
        line.opacity = 0.5
        line.shape = "line"

        return line

    @staticmethod
    def create_square():
        line = ChartFigure()
        line.colour = "purple"
        line.opacity = 0.5
        line.shape = "square"

        return line

    @staticmethod
    def create_triangle():
        line = ChartFigure()
        line.colour = "purple"
        line.opacity = 0.5
        line.shape = "triangle"

        return line

    @staticmethod
    def create_point():
        line = ChartFigure()
        line.colour = "purple"
        line.opacity = 0.5
        line.shape = "circle"

        return line

    @staticmethod
    def create_sample_axis(column_name):
        axis = Axis()
        axis.data_field = column_name
        axis.name = column_name.upper()

        return axis

    @staticmethod
    def create_sample_title():
        chart_title = ChartTitle()

        chart_title.colour = "red"
        chart_title.title = "Demo chart"
        chart_title.font_style = "bold"
        chart_title.font = "times"
        return chart_title
