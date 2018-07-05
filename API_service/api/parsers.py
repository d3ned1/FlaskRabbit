from flask_restplus import reqparse

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page',
                                  type=int,
                                  required=False,
                                  default=1,
                                  help='Page number')

pagination_arguments.add_argument('per_page',
                                  type=int,
                                  required=False,
                                  choices=[10, 20, 40, 80, 200],
                                  help='Results per page')

pagination_arguments.add_argument('year', type=int,
                                  required=False,
                                  help='Filter by date')
