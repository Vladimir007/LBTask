from shop.models import Document, DocumentType, User, Store, AccessGroup


class SQLGenerator:
    def __init__(self, table_name):
        self.table_name = table_name
        self.order = None
        self.fields = []
        self.joins = []
        self.filters = []

    def add_fields(self, *args, table=None):
        if table is None:
            table = self.table_name

        for field in args:
            self.fields.append('"{0}"."{1}"'.format(table, field))

    def join_table(self, table, field_on, table_field, join_type='INNER JOIN'):
        self.joins.append('{0} "{1}" ON ("{2}"."{3}" = "{1}"."{4}")'.format(
            join_type, table, self.table_name, table_field, field_on
        ))

    def add_filter(self, sql_filter):
        self.filters.append(sql_filter)

    def add_order(self, field, descending=False, table=None):
        if table is None:
            table = self.table_name
        self.order = 'ORDER BY "{0}"."{1}" {2}'.format(table, field, 'DESC' if descending else 'ASC')

    def generate(self):
        sql = 'SELECT {0} FROM "{1}" {2} WHERE ({3})'.format(
            ', '.join(self.fields),
            self.table_name,
            ' '.join(self.joins),
            ' AND '.join(self.filters),
        )
        if self.order is not None:
            sql += ' ' + self.order
        return sql


class DocumentsListSQL:
    def __init__(self, user, **kwargs):
        self.user = user
        if self.user.group_id is None:
            self.queryset = Document.objects.none()
            return
        self.document_table = Document._meta.db_table
        self.doctype_table = DocumentType._meta.db_table
        self.store_table = Store._meta.db_table
        self.user_table = User._meta.db_table
        self.joins = []
        self.filters = []
        self.search_data = kwargs
        self.queryset = Document.objects.raw(self.generate_sql())

    def access_subquery(self):
        sql = SQLGenerator(DocumentType._meta.db_table)
        sql.add_fields('id')
        m2m_table = AccessGroup._meta.get_field('doctypes').m2m_db_table()
        doctype_col = AccessGroup._meta.get_field('doctypes').m2m_reverse_name()
        accessg_col = AccessGroup._meta.get_field('doctypes').m2m_column_name()

        sql.join_table(m2m_table, doctype_col, 'id')
        sql.add_filter('"{0}"."{1}" = {2}'.format(m2m_table, accessg_col, self.user.group_id))
        return sql.generate()

    def generate_sql(self):
        sql_generator = SQLGenerator(Document._meta.db_table)
        sql_generator.add_fields('doc_date')
        sql_generator.add_fields('id')
        sql_generator.add_fields('name', table=self.doctype_table)
        sql_generator.add_fields('name', table=self.store_table)
        sql_generator.add_fields('first_name', 'last_name', 'patronymic', table=self.user_table)

        sql_generator.join_table(self.doctype_table, 'id', 'doc_type_id')
        sql_generator.join_table(self.store_table, 'id', 'store_id')
        sql_generator.join_table(self.user_table, 'id', 'author_id')

        sql_generator.add_filter('"{0}"."doc_type_id" IN ({1})'.format(Document._meta.db_table, self.access_subquery()))

        store_filter = self.search_data.get('store')
        if store_filter:
            sql_generator.add_filter('UPPER("{0}"."name") LIKE UPPER(\'%%{1}%%\')'
                                     .format(Store._meta.db_table, store_filter))

        author_filter = self.search_data.get('author')
        if author_filter:
            sql_generator.add_filter('"{0}"."author_id" = {1}'.format(Document._meta.db_table, author_filter.id))

        doctype_filter = self.search_data.get('doc_type')
        if doctype_filter:
            sql_generator.add_filter('"{0}"."doc_type_id" = {1}'.format(Document._meta.db_table, doctype_filter.id))

        date_from = self.search_data.get('doc_date_from')
        if date_from:
            sql_generator.add_filter('"{0}"."doc_date" > \'{1}\''
                                     .format(Document._meta.db_table, date_from))
        date_to = self.search_data.get('doc_date_to')
        if date_to:
            sql_generator.add_filter('"{0}"."doc_date" < \'{1}\''
                                     .format(Document._meta.db_table, date_to))

        sql_generator.add_order("doc_date")
        return sql_generator.generate() + ';'
