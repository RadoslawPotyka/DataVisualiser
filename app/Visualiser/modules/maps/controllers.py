import pandas as pd

from .services import MapsServiceProvider as Services
from .forms import MapsFormHandler
from .models import MapDocument
from ..common.controllers import DocumentBaseEditController


class MapBaseEditController(DocumentBaseEditController):
    def __init__(self,
                 template_path: str = "",
                 document_service: Services.MapService = Services.MapService,
                 form_creator: MapsFormHandler = MapsFormHandler):
        super().__init__(template_path=template_path, document_service=document_service, form_creator=form_creator)

    def on_form_submitted(self, is_valid: bool = False):
        pass

    def on_document_disposed(self):
        return self._router_state_service.go('maps.index')

    def _get_form_creator(self) -> MapsFormHandler:
        """
        Instantiates and returns form handler based on data provided by services assigned to the controller.

        :return: (FormHandler) FormHandler instance with data applied from the services.
        """
        return self._form_creator(columns=self._working_context_service.get_file_columns(),
                                  shapes=self._document_service.get_supported_shapes(),
                                  shape_keys=self._document_service.get_supported_shape_keys(),
                                  colour_palette=self._document_service.get_supported_colours(),
                                  tiles=self._document_service.get_supported_tiles())


class MapEditController(MapBaseEditController):
    """
    Controller for handling Map edition and Map form handling.
    """

    def __init__(self,
                 template_path: str = "",
                 map_service: Services.MapService = Services.MapService,
                 form_creator: MapsFormHandler = MapsFormHandler):
        super().__init__(template_path=template_path, document_service=map_service, form_creator=form_creator)

    def on_form_submitted(self, is_valid: bool = False):
        if is_valid:
            return self._router_state_service.submit('maps.create')
        return self._router_state_service.render(template_path=self._template_path, controller=self)

    def on_document_disposed(self):
        return self._router_state_service.go('maps.index')


class MapCreateController(MapBaseEditController):
    __map_resources = None
    __map_options = None

    def __init__(self,
                 template_path: str = "",
                 map_service: Services.MapService = Services.MapService,
                 form_creator: MapsFormHandler = MapsFormHandler,
                 document_create_service: Services.FoliumService = Services.FoliumService):
        super().__init__(document_service=map_service, form_creator=form_creator, template_path=template_path)
        self._document_creator_service = document_create_service

    def load_map(self, map_document: MapDocument) -> None:
        """

        :param map_document:
        :return: None
        """
        map_object = self._document_creator_service.generate_map(map_document=map_document)
        path_to_map = self._document_creator_service.export_map(map_object=map_object)
        self.__map_resources = path_to_map

    def setup_data_source(self) -> pd.DataFrame:
        creator = self._get_form_creator()
        data_source = creator.map_data_source(self.form.data_source, is_file_uploaded=True)
        data_source.data = self._file_service.read_file(data_source=data_source)

        return data_source

    def on_document_saved(self):
        super().on_document_saved()

    def on_form_submitted(self, is_valid: bool = True):
        super().on_form_submitted()
        creator = self._get_form_creator()

        map_document = MapDocument()
        creator.map_to_document(document=map_document, document_form=self.form)
        self.__map_options = map_document.model

        map_document.data_source = self.setup_data_source()
        self.load_map(map_document=map_document)

        return self._router_state_service.render(template_path=self._template_path, controller=self)

    def on_document_edited(self):
        return self._router_state_service.submit('maps.edit')

    @property
    def map_options(self):
        return self.__map_options

    @property
    def map_resources(self):
        return self.__map_resources

    def on_document_disposed(self):
        super().on_document_disposed()
        return self._router_state_service.go('maps.index')
