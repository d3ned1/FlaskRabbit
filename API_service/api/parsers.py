from datetime import datetime

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
                                  choices=[2, 10, 20, 30, 40, 50, 100],
                                  default=20, help='Results per page')

pagination_arguments.add_argument('year', type=lambda x: datetime.strptime(x, '%Y'),
                                  required=False,
                                  help='Filter by date')
