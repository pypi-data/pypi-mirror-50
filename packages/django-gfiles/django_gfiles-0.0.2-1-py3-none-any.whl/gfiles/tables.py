import django_tables2 as tables
from .models import GenericFile, TrackTasks
from django_tables2_column_shifter.tables import ColumnShiftTable
from django_tables2.utils import A

TABLE_CLASS = "mogi table-bordered table-striped table-condensed table-hover"

class GFileTable(ColumnShiftTable):
    """ Class for django-tables2 table of :class:`gfiles.models.GenericFiles`.

    Inherits the ColumnShiftTable, that is a modified django-tables2 class that allows columns to be dynamically
    selected
    """
    filename = tables.Column(accessor='original_filename', verbose_name='Filename')

    class Meta:
        model = GenericFile
        attrs = {"class": TABLE_CLASS}
        fields = ('id', )


class GFileTableWithCheck(GFileTable):
    """ Class for django-tables2 table of :class:`gfiles.models.GenericFiles` with a check box column

    Inherits :class:`gfiles.models.GFileTable` and just adds checkbox.
    """
    check = tables.CheckBoxColumn(accessor="pk",
                                           attrs={
                                               "th__input": {"onclick": "toggle(this)"},
                                               "td__input": {"onclick": "addfile(this)"}},
                                           orderable=False)

    class Meta:
        model = GenericFile
        attrs = {"class": "table table-bordered table-striped table-condensed table-hover", }
        fields = ('id', 'filename', 'user', 'check')


class TrackTasksTable(ColumnShiftTable):
    progress = tables.LinkColumn('track_task_progress', text='progress', verbose_name='Monitor Progress', args=[A('pk')])
    delete = tables.LinkColumn('delete_track_task', text='delete', verbose_name='Delete', args=[A('pk')])
    class Meta:
        model = TrackTasks
        attrs = {"class": TABLE_CLASS}
        fields = ('id', 'user', 'name', 'taskid', 'state', 'result')






