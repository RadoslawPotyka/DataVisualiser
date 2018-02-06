from wtforms.fields import StringField

from .models import ChartTitle, ChartOptions
from ..common.forms import FormHandler, DocumentBaseOptionsForm
from ..common.models import Axis


class ChartsFormHandler(FormHandler):
    """
    Class responsible for creating forms being used in charts module.
    """

    def map_document_options(self, document_options_form: DocumentBaseOptionsForm) -> ChartOptions:
        """
        Map chart document options form onto ChartOptions object.

        :param document_options_form: (DocumentBaseOptionsForm) form containing user input regarding options for a chart
        :return chart_options: (ChartOptions) chart options configuration object mapped from a form.
        """
        super().map_document_options(document_options_form=document_options_form)
        chart_options = ChartOptions()
        chart_options.description = document_options_form.free_text.data

        axis = Axis()
        axis.data_field = document_options_form.x_axis.data
        axis.name = document_options_form.x_axis_label.data
        axis.data_type = "datetime" if document_options_form.is_date_column.data else "auto"

        chart_options.x_axis = axis

        title = self.map_title(document_options_form.title)
        chart_options.title = title
        return chart_options

    def map_title(self, title_form: StringField) -> ChartTitle:
        """
        Map chart title string field onto ChartTitle object.

        :param title_form: (StringField) string field to extract title from
        :return title: (ChartTitle) chart title object with title extracted from provided string field.
        """
        title = ChartTitle()

        title.title = title_form.data
        title.font_style = "normal"
        title.colour = "red"
        title.font = "auto"

        return title
