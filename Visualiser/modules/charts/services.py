from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import CDN

from ..common.models import TemplateResourcesData
from ..common.creators import DocumentFactory
from .creators import ChartRecipes
from .models import Chart
from .tests.test_samples import ChartSampleGenerator


class ChartService(object):
    """
    Service handling all basic operations on charts like fetching or saving them.
    """

    @staticmethod
    def get_chart(chart_id: int) -> Chart:
        """
        Returns chart configuration object for a chart with given id. Communicates with external database api to fetch
        chart.
        :param chart_id: (int) id of a chart that should be returned. If none provided will return the demo chart.
        :return:
        """
        if chart_id is None:
            raise ValueError("No id provided.")
        else:
            raise ConnectionError("No external service implemented.")

    @staticmethod
    def get_demo_chart() -> Chart:
        """
        Returns the demo chart generated from test_samples.

        :return chart: (Chart) chart object configuration for demo chart.
        """
        chart = ChartSampleGenerator.create_chart()
        return chart

    @staticmethod
    def get_supported_recipes() -> ChartRecipes:
        return ChartRecipes


class BokehService(object):
    """
    Static service handling Bokeh chart generation and export.
    """

    @staticmethod
    def generate_plot(chart: Chart) -> figure:
        """
        Generate plot for given pandas DataFrame and chart options. Returns created plot object

        :param chart: (Chart) options for a chart display and shapes.
        :return plot: (bokeh.plotting.figure) bokeh plot object
        """
        factory = DocumentFactory(recipes=ChartService.get_supported_recipes())
        plot = factory.create_object(document=chart)

        return plot

    @staticmethod
    def get_bokeh_resources() -> TemplateResourcesData:
        """
        Get meta resources for bokeh plots. Returns object containing lists of all necessary links and scripts to
        display and embed bokeh chart.

        :return template_resources: (TemplateResourcesData) object containing list of resources for bokeh plots.
        """
        template_resources = TemplateResourcesData()
        template_resources.js = CDN.js_files[0]
        template_resources.css = CDN.css_files[0]

        return template_resources

    @staticmethod
    def export_plot(plot: figure) -> TemplateResourcesData:
        """
        Export plot data. Returns object containing list of all files necessary for embedding the plot data. Does not
        contain meta data for bokeh plots.
        :param plot: (bokeh.plotting.figure) bokeh figure object to export resources from.
        :return template_resources: (TemplateResourcesData) object containing lists of all resources for provided plot.
        """
        template_resources = TemplateResourcesData()
        template_resources.js, template_resources.html = components(plot)

        return template_resources
