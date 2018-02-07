from wtforms.fields import SelectField
from wtforms.validators import DataRequired

from .models import MapOptions
from ..common.forms import FormHandler, DocumentBaseOptionsForm
from ..common.models import Axis


class MapsFormHandler(FormHandler):
    """
    Class responsible for creating forms being used in maps module.
    """

    _default_size = 8.0
    _default_title = "My Map"

    def __init__(self, columns: [tuple], shapes: [tuple], shape_keys: any, colour_palette: [tuple], tiles: [tuple]):
        super().__init__(colour_palette=colour_palette, shape_keys=shape_keys, shapes=shapes, columns=columns)
        self.__supported_tiles = tiles

    def prepare_document_options_form(self) -> DocumentBaseOptionsForm:
        """
        Dynamically create wtforms derived DocumentOptionsForm object for document options creation based on supported
        columns provided with initialisation.

        :return form: (DocumentOptionsForm) document options form with commonly required fields.
        """

        class DocumentOptionsForm(DocumentBaseOptionsForm):
            pass

        DocumentOptionsForm.latitude = SelectField("Latitude Column", choices=self._columns,
                                                   validators=[DataRequired()])
        DocumentOptionsForm.longtitude = SelectField("Longtitude Column", choices=self._columns,
                                                     validators=[DataRequired()])
        DocumentOptionsForm.tiles = SelectField("Map Tiles", choices=self.__supported_tiles,
                                                validators=[DataRequired()])
        DocumentOptionsForm.title = self.prepare_title_form()

        form = DocumentOptionsForm
        return form

    def map_document_options(self, document_options_form: DocumentBaseOptionsForm) -> MapOptions:
        """
        Map chart document options form onto ChartOptions object.

        :param document_options_form: (DocumentBaseOptionsForm) form containing user input regarding options for a chart
        :return map_options: (ChartOptions) chart options configuration object mapped from a form.
        """
        super().map_document_options(document_options_form=document_options_form)
        map_options = MapOptions()
        map_options.description = document_options_form.free_text.data
        map_options.tiles = document_options_form.tiles.data

        latitude = Axis()
        latitude.data_field = document_options_form.latitude.data
        map_options.latitude = latitude

        longtitude = Axis()
        longtitude.data_field = document_options_form.longtitude.data
        map_options.longtitude = longtitude

        title = self.map_title(document_options_form.title)
        map_options.title = title

        return map_options
