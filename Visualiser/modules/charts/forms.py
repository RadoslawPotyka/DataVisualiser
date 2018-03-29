from wtforms.fields import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length

from .models import ChartTitle, ChartOptions
from ..common.forms import FormHandler, DocumentBaseOptionsForm
from ..common.models import Axis


class ChartsFormHandler(FormHandler):
    """
    Class responsible for creating forms being used in charts module.
    """

    _default_title = "My Chart"

    def __init__(self, columns: [tuple], shapes: [tuple], shape_keys: any, colour_palette: [tuple]):
        super().__init__(colour_palette=colour_palette, shape_keys=shape_keys, shapes=shapes, columns=columns)

    def prepare_document_options_form(self) -> DocumentBaseOptionsForm:
        """
        Dynamically create wtforms derived DocumentOptionsForm object for document options creation based on supported
        columns provided with initialisation.

        :return: form(DocumentOptionsForm) - document options form with commonly required fields.
        """

        class DocumentOptionsForm(DocumentBaseOptionsForm):
            pass

        DocumentOptionsForm.x_axis = SelectField("X axis column", choices=self._columns, validators=[DataRequired()])
        DocumentOptionsForm.title = self.prepare_title_form()
        DocumentOptionsForm.x_axis_label = StringField(label="X axis label", validators=[Length(max=50)])
        DocumentOptionsForm.is_date_column = BooleanField(label="Select if the column contains dates")

        form = DocumentOptionsForm
        return form

    def map_document_options(self, document_options_form: DocumentBaseOptionsForm) -> ChartOptions:
        """
        Map chart document options form onto ChartOptions object.

        :param document_options_form: (DocumentBaseOptionsForm) form containing user input regarding options for a chart
        :return: chart_options(ChartOptions) - chart options configuration object mapped from a form.
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
        :return: title(ChartTitle) - chart title object with title extracted from provided string field.
        """
        title = ChartTitle()

        title.title = title_form.data
        title.font_style = "normal"
        title.colour = "red"
        title.font = "auto"

        return title
