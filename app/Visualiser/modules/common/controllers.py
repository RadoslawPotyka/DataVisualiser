from abc import abstractmethod
from werkzeug.utils import secure_filename

from .forms import FormHandler
from .services import CommonServiceProvider as Services
from .errors import VisualiserError, UnhandledError


class BaseController(object):
    """
    Base interface for view controllers. Gathers and handles data for later display to user and communicates with
    services depending on the context.

    Attributes:
        _template_path: (str) path to the template that will be rendered in the application.
        _working_context_service: (Services.WorkingContextService) Service for interacting with the context of the
                                                                   application
        _router_state_service: (Services.RouterStateService) Service for rendering and redirecting views.

    Args:
        template_path: (str) path to the template that will be rendered in the application.
        working_context_service: (Services.WorkingContextService) Service for interacting with the context of the
                                                                   application
        router_state_service: (Services.RouterStateService) Service for rendering and redirecting views.
    """

    def __init__(self,
                 template_path: str = "",
                 working_context_service: Services.WorkingContextService = Services.WorkingContextService,
                 router_state_service: Services.RouterStateService = Services.RouterStateService):
        self._template_path = template_path
        self._working_context_service = working_context_service
        self._router_state_service = router_state_service

    @abstractmethod
    def activate(self):
        """
        Activate the controller. Method should return either rendered template or redirect user to a proper page.
        Method should be called in blueprints respective endpoint to display the correct view to the user.

        :return: rendered template for a view or redirect to another page.
        """
        return self._router_state_service.render(template_path=self._template_path, controller=self)

    def on_error_occurred(self, error: Exception, next_state: str = ".index"):
        """
        Action to perform when an error occurred during controller activation. Method notifies the user about the error
        and switches route state to the one provided via params or to the index page of the current module.

        :param error: (Exception) exception that occurred during application runtime..
        :param next_state: (str) route path for the state the application should switch to.
        """
        self._router_state_service.notify(message=str(error), status="danger")
        return self._router_state_service.go(state=next_state)


class DocumentBaseEditController(BaseController):
    """
    Base controller for document edition. Contains all necessary methods, data for proper form handling, parsing
    and submitting

    Attributes:
        _form_creator: (FormHandler) form handler object for form parsing and preparation.
        _file_service: (Services.FileService) Service for file handling, reading and parsing.
        _document_service: (Services.DocumentService) Service for document handling.
        _is_empty: (bool) determines whether the form is initialised for the first time throughout the current
        context of the application
        _is_submitting: (bool) param determining whether the form used by controller is ready for submission and posting
        _form: (Form) form object instance used by the controller.

    Args:
        form_creator: (str) form handler object for form parsing and preparation.
        file_service: (Services.FileService) Service for file handling, reading and parsing.
        document_service: (Services.DocumentService) Service for document handling.
    """
    _form = None
    _form_creator = None
    _is_empty = False
    _is_submitting = False

    def __init__(self,
                 template_path: str = "",
                 document_service: Services.DocumentService = Services.DocumentService,
                 file_service: Services.FileService = Services.FileService,
                 form_creator: FormHandler = FormHandler):
        super().__init__(template_path=template_path)
        self._document_service = document_service
        self._file_service = file_service
        self._form_creator = form_creator

    def activate(self, is_empty: bool = True):
        """
        :param is_empty: (bool) determines whether the controller form data is empty or filled with data.
        :return: call to the form_action method resolving in proper template rendering or view redirection.
        """
        try:
            self._is_empty = is_empty
            self.prepare_form()
            return self.form_action()
        except VisualiserError as error:
            return self.on_error_occurred(error=error)
        except Exception:
            return self.on_error_occurred(error=UnhandledError(), next_state=".index")

    def prepare_form(self):
        """
        Prepares and parses form that will be used by controller.

        :return: None
        """
        creator = self._get_form_creator()

        if self._is_empty:
            self.form = creator.prepare_empty_form()
        else:
            self.form = creator.prepare_document_form()

    def _get_form_creator(self):
        """
        Instantiates and returns form handler based on data provided by services assigned to the controller.

        :return: (FormHandler) FormHandler instance with data applied from the services.
        """
        return self._form_creator(columns=self._working_context_service.get_file_columns(),
                                  shapes=self._document_service.get_supported_shapes(),
                                  shape_keys=self._document_service.get_supported_shape_keys(),
                                  colour_palette=self._document_service.get_supported_colours())

    @property
    def is_empty(self):
        return self._is_empty

    @property
    def is_submitting(self):
        return self._is_submitting

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, form: any):
        self._form = form

    def on_file_uploaded(self):
        """
        Action to perform when the file is submitted by the user. Using assigned form handler maps data from the form
        to a DataSource object, saves the file in the upload folder, saves the column of mentioned file for later
        usage and then reinstantiates the form for user input changes to apply to it.

        :return: Rendered controller template.
        """
        creator = self._get_form_creator()
        data_source = creator.map_data_source(self.form.data_source)

        file = self.form.data_source.data_source.data
        file_name = secure_filename(file.filename)
        file.save(self._working_context_service.get_upload_folder() + file_name)

        self._working_context_service.save_file_columns(self._file_service.read_columns(data_source=data_source))

        self.prepare_form()
        self.form.upload_file(data_source.file_name)

        return self._router_state_service.render(template_path=self._template_path, controller=self)

    def on_layer_submitted(self):
        """
        Action to perform when the layer is submitted by the user. Appends new layer entry to a form layers field list
        and returns rendered template.

        :return: Rendered controller template.
        """
        self.form.submit_layer()
        return self._router_state_service.render(template_path=self._template_path, controller=self)

    def on_layer_removed(self):
        """
        Action to perform when document layer is removed by user.

        :return: Rendered controller template.
        """
        self.form.remove_layer()
        return self._router_state_service.render(template_path=self._template_path, controller=self)

    @abstractmethod
    def on_form_submitted(self, is_valid: bool = False):
        """
        Action to perform when the form is submitted by the user.

        :return: Rendered controller template.
        """
        return self._router_state_service.render(template_path=self._template_path, controller=self)

    @abstractmethod
    def on_document_disposed(self):
        """
        Action to perform when the form is disposed by the user.

        :return: Redirect to the index of the page.
        """
        return self._router_state_service.go('index')

    def on_document_saved(self):
        """
        Action to perform when the document is saved.

        :return: None
        """
        pass

    def on_document_edited(self):
        """
        Method that will be called when document is edited.

        :return: Rendered controller template.
        """
        self.prepare_form()
        return self._router_state_service.render(template_path=self._template_path, controller=self)

    def on_form_initialised(self):
        return self._router_state_service.render(template_path=self._template_path, controller=self)

    def on_error_occurred(self, error, next_state: str = ".edit"):
        return super().on_error_occurred(error, next_state)

    def form_action(self):
        """
        Get's user action by checking pressed button. If controller is empty returns call to on_initialised method.
        Each possible button pressed is resolved by assigned function and by calling router service method redirects
        user to a certain view or displays template.

        :return: rendered template or route redirect depending on the form state
        """
        is_valid = self.form.validate_on_submit()

        if self.is_empty:
            return self.on_form_initialised()
        elif self.form.submit_file.data:
            return self.on_file_uploaded()
        elif self.form.add_layer.data:
            return self.on_layer_submitted()
        elif self.form.submit_document.data:
            return self.on_form_submitted(is_valid=is_valid)
        elif self.form.cancel.data:
            return self.on_document_disposed()
        elif self.form.save_document.data:
            return self.on_document_saved()
        elif self.form.edit_document.data:
            return self.on_document_edited()
        else:
            return self.on_layer_removed()
