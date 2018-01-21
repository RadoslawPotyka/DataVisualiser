from abc import abstractmethod

from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms.fields import SelectField, StringField, TextAreaField, FieldList, \
    FloatField, HiddenField, FormField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HTMLString, html_params, Select

from ..common.models import Layer, Document, DocumentOptions, DataSource


class ColourSelect(Select):
    """
    Renders a select field that supports options including additional html params.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected, html_attributes)`.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        for val, label, selected, html_attributes in field.iter_choices():
            html.append(self.render_option(val, label, selected, **html_attributes))
        html.append('</select>')
        return HTMLString(''.join(html))


class ColourSelectField(SelectField):
    """
    Renders select field with colourised option background based on field value. Uses custom colour select widget
    supporting html param providing. Requires proper html colour representation in value of the choices for selection.
    """
    widget = ColourSelect()

    def iter_choices(self):
        for value, label in self.choices:
            render_args = {'style': "background: " + value}
            yield (value, label, self.coerce(value) == self.data, render_args)


class BaseForm(FlaskForm):
    """
    Base class form flask wtforms. Contains method for mapping data from and to form object into respective objects that
    will be used later throughout the application.
    """

    def map_to_object(self, an_object: any) -> None:
        """
        Applies data from form to provided object. Method changes object in place and does not
        instantiate it.

        :param an_object: (any) object to map data to
        :return: None
        """
        return None

    def map_from_object(self, an_object: any) -> None:
        """
        Assign values of respective fields of provided object to a form.

        :param an_object: (any) object to map data from
        :return: None
        """
        return None


class LayerOptionsForm(BaseForm):
    """
    Class representing form for gathering user input regarding layer options.
    """
    layer_name = StringField("Label", validators=[Length(max=100)])

    opacity = FloatField("Opacity", default=0.8)
    size = FloatField("Size", default=1.21)
    remove_layer = SubmitField("Remove")


class FileForm(BaseForm):
    """
    Class representing form for gathering user input regarding data source and handling file upload.
    """
    data_source = FileField(label="Data")
    separator_type = SelectField("Columns separator",
                                 choices=[(",", "comma"), (";", "semicolon"), ("\t", "tab"), (" ", "space")],
                                 default=(",", "comma"))
    columns_row_index = IntegerField("Index of columns row", default=0)
    file_name = HiddenField(StringField())


class DocumentBaseOptionsForm(BaseForm):
    """
    Class representing form for gathering user input regarding document options usable for all documents in app.
    """
    free_text = TextAreaField(label="Description", validators=[Length(min=0, max=200)])
    x_axis_label = StringField(label="X column label", validators=[Length(max=50)])
    is_date_column = BooleanField(label="Click if the column contains dates")


class DocumentBaseForm(BaseForm):
    """
    Class representing form for gathering user input regarding whole document. Contains field, methods and sub-forms
    common for all types of documents
    """
    # data_source = FileField(label="Data")
    data_source = FormField(FileForm)
    file_name = HiddenField(StringField())
    layers = FieldList(FormField(LayerOptionsForm),
                       min_entries=1)

    submit_file = SubmitField("Submit file")
    submit_document = SubmitField("Create chart")
    add_layer = SubmitField("Add Layer")
    cancel = SubmitField("Dispose")
    edit_document = SubmitField("Edit chart")
    save_document = SubmitField("Save chart")

    def remove_layer(self):
        """
        Method checks which button for which existing layer of a document has been pressed. If it was button for edition
        returns layer that has the button pressed and removes it from field list. Otherwise the layer is only removed.

        :return edited_layer: layer that should be edited (None if layer was removed from the field list)
        """
        layer_list = []

        while len(self.layers):
            layer_entry = self.layers.pop_entry()
            if not layer_entry.remove_layer.data:
                layer_list.append(layer_entry)

        for layer in layer_list.reverse():
            self.layers.append_entry(layer)

    def submit_layer(self):
        """
        Appends newest layer form filled by user to list of layers in a form and prepares new, empty layer form.

        :return: None
        """
        self.layers.append_entry()

    def upload_file(self, file_name):
        """
        Assigns provided name to FileForm sub-form for later usage in the app.

        :param file_name: (str) file_name to assign to the document forms file form.
        :return:
        """
        self.data_source.file_name.data = file_name


class FormHandler(object):
    """
    Class responsible for preparing a form and mapping data from it.

    Args:
                columns([tuple]): list of tuples representing columns available for layer options form data field.
                shapes([tuple]): list of tuples representing shapes available for layer options form object_key.
                shape_keys(Enum): Enum object containing keys to translate from string value when mapping layers.
                colour_palette([tuple]): list of tuples representing available colours.

    Attributes:
        __supported_shapes([tuple]): list of tuples representing shapes available for layer options form object_key.
        __columns([tuple]): list of tuples representing columns available for layer options form data field.
        __shape_keys(Enum): Enum object containing keys to translate from string value when mapping layers.
        __colours([tuple]): list of tuples representing available colours.
    """

    __supported_shapes = None
    __columns = None
    __shape_keys = None
    __colours = None

    def __init__(self, columns: [tuple], shapes: [tuple], shape_keys: any, colour_palette: [tuple]):
        self.__columns = columns
        self.__supported_shapes = shapes
        self.__shape_keys = shape_keys
        self.__colours = colour_palette

    def __call__(self, *args, **kwargs):
        return self.__init__(*args, **kwargs)

    @staticmethod
    def prepare_empty_form():
        """
        Prepare empty form for first step of document preparation.

        :return form: (DocumentForm) basic document form.
        """

        class DocumentForm(DocumentBaseForm):
            pass

        form = DocumentForm()
        return form

    def prepare_document_form(self):
        """
        Prepare full document form with all fields necessary for creating functional documents.

        :return form: (DocumentForm) document form containing all fields, buttons and sub-forms.
        """

        class DocumentForm(DocumentBaseForm):
            pass

        layer_form = self.prepare_layer_form()
        DocumentForm.layers = FieldList(FormField(layer_form), min_entries=1)

        document_options_form = self.prepare_document_options_form()
        DocumentForm.document_options = FormField(document_options_form)

        form = DocumentForm()
        return form

    def prepare_document_options_form(self) -> DocumentBaseOptionsForm:
        """
        Dynamically create wtforms derived DocumentOptionsForm object for document options creation based on supported
        columns provided with initialisation.

        :return form: (DocumentOptionsForm) document options form with commonly required fields.
        """

        class DocumentOptionsForm(DocumentBaseOptionsForm):
            pass

        DocumentOptionsForm.x_axis = SelectField("X Column", choices=self.__columns, validators=[DataRequired()])
        DocumentOptionsForm.title = self.prepare_title_form()

        form = DocumentOptionsForm
        return form

    @staticmethod
    def prepare_title_form(document_type: str = "Document") -> StringField:
        """
        Prepare title form for document title assignment.

        :param document_type: (str) type of a document to set as the default value.
        :return title_form: (StringField) title form for a document.
        """
        default_title = "My " + document_type
        title_form = StringField("Title", default=default_title, validators=[DataRequired()])

        return title_form

    def prepare_layer_form(self) -> LayerOptionsForm:
        """
        Dynamically create wtforms derived LayerForm object for layer creation based on supported shapes, colours and
        columns provided with initialisation.

        :return form: (LayerOptionsForm) form instance for chart layer creation.
        """

        class LayerForm(LayerOptionsForm):
            pass

        LayerForm.data_field = SelectField("Column", choices=self.__columns, validators=[DataRequired()])
        LayerForm.shape = SelectField("Shape", choices=self.__supported_shapes, validators=[DataRequired()])
        LayerForm.colour = ColourSelectField("Colour", choices=self.__colours, validators=[DataRequired()])

        form = LayerForm
        return form

    @staticmethod
    def map_data_source(file_form: FileForm, is_file_uploaded: bool = False):
        """
        Instantiate DataSource object and map data from provided file_form to it. Depending whether the file from the
        form was previously submitted or not method will either secure the name of uploaded file or read it from.

        :param file_form: (FileForm) form containing user input for document data source.
        :param is_file_uploaded: (bool) boolean value determining whether the file from form was already uploaded.
        :return data_source: (DataSource) data source configuration object instance.
        """
        data_source = DataSource()

        separator = file_form.separator_type.data
        column_index = file_form.columns_row_index.data

        if is_file_uploaded:
            file_name = file_form.file_name.data
        else:
            file = file_form.data_source.data
            file_name = secure_filename(file.filename)

        data_source.file_name = file_name
        data_source.separator = separator
        data_source.column_index = column_index

        return data_source

    def map_to_document(self, document_form: DocumentBaseForm, document: Document) -> Document:
        """
        Map data from provided document_form and assign respective values from it to provided document object instance.

        :param document_form: (DocumentBaseForm) Base document form containing user input regarding document.
        :param document: (Document) document object instance to assign data from form.
        :return document: (Document) document object instance with assigned values.
        """
        document.model = self.map_document_options(document_options_form=document_form.document_options)
        document.model.layers = [self.map_layer(layer_entry) for layer_entry in document_form.layers.data]

        return document

    @abstractmethod
    def map_document_options(self, document_options_form: DocumentBaseOptionsForm) -> DocumentOptions:
        """
        Instantiate DocumentOptions object and map data from provided document_options_form to it.

        :param document_options_form: (DocumentBaseOptionsForm) document options form containing user input regarding
         document options.
        :return: (DocumentOptions) Instantiated document options with data mapped from provided form.
        """
        pass

    def map_title(self, title: StringField) -> str:
        """
        Return user input from provided title StringField.

        :param title: (StringField) field containing user input regarding document title.
        :return title: (str) user input regarding document title.
        """
        return title.data

    def map_layer(self, layer_form: dict) -> Layer:
        """
        Instantiate Layer object and map data from provided layer_form to it.

        :param layer_form: (dict) layer form dictionary containing user input regarding layer options.
        :return layer: (Layer) layer object instance containing options for a layer mapped from provided form.
        """
        layer = Layer()

        layer.axis.data_field = layer_form["data_field"]
        layer.axis.name = layer_form["layer_name"]

        layer.figure.size = layer_form["size"]
        layer.figure.object_key = self.__shape_keys[layer_form["shape"]]
        layer.figure.opacity = layer_form["opacity"]
        layer.figure.colour = layer_form["colour"]

        return layer
