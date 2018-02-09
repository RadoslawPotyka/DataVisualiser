from .services import ChartServiceProvider as Services
from .forms import ChartsFormHandler
from .models import Chart
from ..common.controllers import DocumentBaseEditController
from ..common.models import DataSource


class ChartEditController(DocumentBaseEditController):
    """
    Controller for handling chart edition and chart form handling.

    Args:
        chart_service: (ChartService) charts specific document service.
        form_creator: (ChartsFormHandler) charts specific form handler.
    """

    def __init__(self,
                 template_path: str = "",
                 chart_service: Services.ChartService = Services.ChartService,
                 form_creator: ChartsFormHandler = ChartsFormHandler):
        super().__init__(template_path=template_path, document_service=chart_service, form_creator=form_creator)

    def on_form_submitted(self, is_valid: bool = False):
        """
        Action to perform when the form is submitted by the user. Depending whether controllers form is valid or not
        either returns rendered view template or redirects to charts.create route.

        :param is_valid: (bool) param determining whether form is valid.
        :return: rendered view template or redirect to charts creation url.
        """
        if is_valid:
            return self._router_state_service.submit('charts.create')
        return self._router_state_service.render(template_path=self._template_path, controller=self)

    def on_document_disposed(self):
        return self._router_state_service.go('charts.index')


class ChartCreateController(DocumentBaseEditController):
    """
    Controller handling creation of the chart by parsing data from form into chart document object and creating it
    using provided document_create_service.

    Args:
        chart_service: (ChartService) charts specific document service.
        form_creator: (ChartsFormHandler) charts specific form handler.
        document_create_service (BokehService) bokeh service for creating and exporting plots.

    Attributes:
        @property chart_options: (ChartOptions) options for a chart parsed from controllers form.
        @property bokeh_resources: (TemplateResourcesData) template resources for bokeh library.
        @property chart_resources: (TemplateResourcesData) template resources for generated bokeh plot.
        _document_creator_service: (BokehService) bokeh service for creating and exporting plots.
    """
    __chart_resources = None
    __bokeh_resources = None
    __chart_options = None

    def __init__(self,
                 template_path: str = "",
                 chart_service: Services.ChartService = Services.ChartService,
                 form_creator: ChartsFormHandler = ChartsFormHandler,
                 document_create_service: Services.BokehService = Services.BokehService):
        super().__init__(document_service=chart_service, form_creator=form_creator, template_path=template_path)
        self._document_creator_service = document_create_service

    def load_plot(self, chart: Chart) -> None:
        """
        Create plot from chart document object instance using controllers document creator service and assigns
        template resources from generated plot to controllers properties.

        :param chart: (Chart) chart object instance to generate plot from.
        :return: None
        """
        plot = self._document_creator_service.generate_plot(chart)

        self.__bokeh_resources = self._document_creator_service.get_bokeh_resources()
        self.__chart_resources = self._document_creator_service.export_plot(plot)

    def setup_data_source(self, datetime_columns: [str] = None) -> DataSource:
        """
        Map data from controllers form data source sub-form and read file from generated data source.

        :param datetime_columns: (list(str)) list of datetime columns in the data source.
        :return data_source: (DataSource)
        """
        creator = self._get_form_creator()
        data_source = creator.map_data_source(self.form.data_source, is_file_uploaded=True)
        data_source.datetime_columns = datetime_columns  # if len(datetime_columns) > 0 else False
        data_source.data = self._file_service.read_file(data_source=data_source)

        return data_source

    def on_document_saved(self):
        super().on_document_saved()

    def on_form_submitted(self, is_valid: bool = True):
        super().on_form_submitted()
        creator = self._get_form_creator()

        chart = Chart()
        creator.map_to_document(document=chart, document_form=self.form)
        self.__chart_options = chart.model

        x_axis = self.__chart_options.x_axis
        parse_dates = [x_axis.data_field] if x_axis.data_type == "datetime" else False

        chart.data_source = self.setup_data_source(datetime_columns=parse_dates)
        self.load_plot(chart=chart)

        return self._router_state_service.render(template_path=self._template_path, controller=self)

    def on_document_edited(self):
        return self._router_state_service.submit('charts.edit')

    @property
    def chart_options(self):
        return self.__chart_options

    @property
    def chart_resources(self):
        return self.__chart_resources

    @property
    def bokeh_resources(self):
        return self.__bokeh_resources

    def on_document_disposed(self):
        super().on_document_disposed()
        return self._router_state_service.go('charts.index')


class ChartDisplayController(object):
    """
    Controller responsible for handling chart creation. Contains all methods necessary for creating and storing
    charts with options provided by form data and pandas data frame object with values loaded from uploaded file.

    Attributes:
        __bokeh_resources(TemplateResourcesData): standard css and js resources for bokeh charts.
        __chart_resources(TemplateResourcesData): js and html resources for particular bokeh charts.
    """

    __chart_resources = None
    __bokeh_resources = None

    def load_demo_plot(self):
        chart = Services.ChartService.get_demo_chart()
        plot = Services.BokehService.generate_plot(chart)

        self.__bokeh_resources = Services.BokehService.get_bokeh_resources()
        self.__chart_resources = Services.BokehService.export_plot(plot)

    def load_plot(self, chart: Chart):
        """

        :param chart:
        :return:
        """
        plot = Services.BokehService.generate_plot(chart)

        self.__bokeh_resources = Services.BokehService.get_bokeh_resources()
        self.__chart_resources = Services.BokehService.export_plot(plot)

    @property
    def chart_resources(self):
        return self.__chart_resources

    @property
    def bokeh_resources(self):
        return self.__bokeh_resources
