from abc import abstractmethod

from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms.fields import SelectField, StringField, TextAreaField, FieldList, \
    FloatField, HiddenField, FormField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HTMLString, html_params, Select

from .models import Layer, Document, DocumentOptions, DataSource, FilterExpression
from .utils import StringTools


class ColourSelect(Select):
    """
    Renders a select field that supports options including additional html params.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of `(value, label, selected, html_attributes)`.
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


class LayerOptionsForm(FlaskForm):
    """
    Class representing form for gathering user input regarding layer options.
    """
    layer_name = StringField("Label", validators=[Length(max=100)])

    opacity = FloatField("Opacity", default=0.8)
    remove_layer = SubmitField("Remove")


class FileForm(FlaskForm):
    """
    Class representing form for gathering user input regarding data source and handling file upload.
    """
    data_source = FileField(label="File")
    separator_type = SelectField("Columns separator",
                                 choices=[(",", "comma"), (";", "semicolon"), ("\t", "tab"), (" ", "space")],
                                 default=(",", "comma"))
    columns_row_index = IntegerField("Index of columns row", default=0)
    file_name = HiddenField(StringField())
    should_fill_missing_data = BooleanField("Select if missing data should be filled", default=True)


class DocumentBaseOptionsForm(FlaskForm):
    """
    Class representing form for gathering user input regarding document options usable for all documents in app.
    """
    free_text = TextAreaField(label="Description", validators=[Length(min=0, max=200)])
    title = StringField("Title", default="My Document", validators=[DataRequired()])


class DocumentBaseForm(FlaskForm):
    """
    Class representing form for gathering user input regarding whole document. Contains field, methods and sub-forms
    common for all types of documents
    """
    data_source = FormField(FileForm)
    file_name = HiddenField(StringField())
    layers = FieldList(FormField(LayerOptionsForm),
                       min_entries=1)

    submit_file = SubmitField("Submit file")
    submit_document = SubmitField("Create")
    add_layer = SubmitField("Add Layer")
    cancel = SubmitField("Dispose")
    edit_document = SubmitField("Edit")
    save_document = SubmitField("Save")

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

        layer_list.reverse()

        for layer in layer_list:
            self.layers.append_entry(layer.data)

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
        _supported_shapes([tuple]): list of tuples representing shapes available for layer options form object_key.
        _columns([tuple]): list of tuples representing columns available for layer options form data field.
        _shape_keys(Enum): Enum object containing keys to translate from string value when mapping layers.
        _colours([tuple]): list of tuples representing available colours.
    """

    _supported_shapes = None
    _columns = None
    _shape_keys = None
    _colours = None
    _scale = 1.0
    _default_title = "My Document"
    _supported_conditions = [("", "None"), ("==", "="), ("!=", "!="),
                             ("<=", "<="), (">=", ">="), (">", ">"), ("<", "<")]
    _supported_collocations = [("&", "and"), ("|", "or")]
    _object_size_scales = [("1.25", "Thin"), ("2", "Medium"), ("3.5", "Thick")]

    def __init__(self, columns: [tuple], shapes: [tuple], shape_keys: any, colour_palette: [tuple]):
        self._columns = columns
        self._supported_shapes = shapes
        self._shape_keys = shape_keys
        self._colours = colour_palette

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

    @abstractmethod
    def prepare_document_options_form(self) -> DocumentBaseOptionsForm:
        """
        Dynamically create wtforms derived DocumentOptionsForm object for document options creation based on supported
        columns provided with initialisation.

        :return form: (DocumentOptionsForm) document options form with commonly required fields.
        """
        pass

    def prepare_title_form(self) -> StringField:
        """
        Prepare title form for document title assignment.

        :return title_form: (StringField) title form for a document.
        """
        title_form = StringField("Title", default=self._default_title, validators=[DataRequired()])
        return title_form

    def prepare_layer_form(self) -> LayerOptionsForm:
        """
        Dynamically create wtforms derived LayerForm object for layer creation based on supported shapes, colours and
        columns provided with initialisation.

        :return form: (LayerOptionsForm) form instance for chart layer creation.
        """

        class LayerForm(LayerOptionsForm):
            pass

        LayerForm.data_field = SelectField("Column", choices=self._columns, validators=[DataRequired()])
        LayerForm.shape = SelectField("Shape", choices=self._supported_shapes, validators=[DataRequired()])
        LayerForm.colour = ColourSelectField("Colour", choices=self._colours, validators=[DataRequired()])

        LayerForm.size = SelectField("Size", choices=self._object_size_scales)

        LayerForm.filter_expressions = FieldList(FormField(self.prepare_filter_form()), min_entries=2, max_entries=2)
        LayerForm.operator = SelectField("", choices=self._supported_collocations)

        form = LayerForm
        return form

    def prepare_filter_form(self) -> FlaskForm:
        """
        Dynamically create wtforms derived filter options form.

        :return form: (FilterOptionsForm) filter form for a singular filter expression
        """

        class FilterOptionsForm(FlaskForm):
            pass

        FilterOptionsForm.operator = SelectField("Condition", choices=self._supported_conditions)
        FilterOptionsForm.value = StringField("Value")

        form = FilterOptionsForm
        return form

    @staticmethod
    def map_data_source(file_form: FileForm, is_file_uploaded: bool = False) -> DataSource:
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
        elif file_form.data_source.data:
            file = file_form.data_source.data
            file_name = secure_filename(file.filename)
        else:
            raise FileNotFoundError()

        data_source.file_name = file_name
        data_source.separator = separator
        data_source.column_index = column_index
        data_source.should_fill_missing_data = file_form.should_fill_missing_data.data

        return data_source

    def map_to_document(self, document_form: DocumentBaseForm, document: Document) -> None:
        """
        Map data from provided document_form and assign respective values from it to provided document object instance.

        :param document_form: (DocumentBaseForm) Base document form containing user input regarding document.
        :param document: (Document) document object instance to assign data from form.
        :return document: None
        """
        document.model = self.map_document_options(document_options_form=document_form.document_options)
        document.model.layers = [self.map_layer(layer_entry) for layer_entry in document_form.layers.data]

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

        data_field = layer_form["data_field"]
        layer.axis.data_field = data_field
        layer.axis.name = layer_form["layer_name"]

        size = StringTools.to_float(string=layer_form["size"])
        layer.figure.size = size * self._scale

        layer.figure.object_key = self._shape_keys[layer_form["shape"]]
        layer.figure.opacity = layer_form["opacity"]
        layer.figure.colour = layer_form["colour"]
        layer.filter_expression = self.map_filters(layer_form=layer_form)

        return layer

    def map_filters(self, layer_form: dict) -> FilterExpression:
        """
        Map filter values from layers filter sub-form.

        :param layer_form: (dict) layer form dictionary to parse filter from
        :return filter_expression: (FilterExpression) parsed filter expression for a layer.
        """
        data_field = layer_form["data_field"]
        operator = layer_form["operator"]

        expr1 = self.map_filter(filter_entry=layer_form["filter_expressions"][0], data_field=data_field)
        expr2 = self.map_filter(filter_entry=layer_form["filter_expressions"][1], data_field=data_field)

        if expr1 is None:
            filter_expression = None
        elif expr2 is None:
            filter_expression = expr1
        else:
            expr1 = "({0})".format(expr1)
            expr2 = "({0})".format(expr2)
            filter_expression = FilterExpression(expression1=expr1, expression2=expr2, operator=operator)

        return filter_expression

    @staticmethod
    def map_filter(filter_entry: dict, data_field: str) -> FilterExpression:
        """
        Map single filter expression from filter form.

        :param filter_entry: (dict) filter form dictionary with values to map onto FilterExpression instance.
        :param data_field: (str) data field used for filter expression.
        :return filter_expression: (FilterExpression) mapped filter expression.
        """
        filter_expression = None

        if not (StringTools.is_empty(filter_entry["value"]) and StringTools.is_empty(filter_entry["operator"])):
            value = StringTools.parse(filter_entry["value"])
            filter_expression = FilterExpression(expression1=data_field,
                                                 operator=filter_entry["operator"],
                                                 expression2=value)

        return filter_expression
