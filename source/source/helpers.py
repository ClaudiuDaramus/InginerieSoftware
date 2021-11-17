from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from datetime import datetime


# def optionHelper(request, view, parameters):
#     meta = view.metadata_class()
#     data = meta.determine_metadata(request, view)
#     data.pop('renders')
#     data.pop('parses')
#     for key in parameters:
#         data[key] = parameters[key]
#     return data
#

class HelperFunctions:
    # these are some generic functions that are useful in the filtering process
    @staticmethod
    def stringOrNoneToFloat(stringField):
        return float(stringField) if stringField is not None else 0

    @staticmethod
    def stringToStringOrNone(stringField):
        if stringField in [None, '', 'None']:
            return None
        else:
            return stringField
        # return stringField if stringField != '' and stringField is not None and stringField != 'None' else None

    @staticmethod
    def stringOrNoneToStringList(stringField, splitter=','):
        return stringField.split(splitter) if stringField is not None else None

    @staticmethod
    def stringOrNoneToIntList(stringField, splitter=','):
        if stringField is None:
            return None

        return [int(element) for element in stringField.split(splitter)]

    @staticmethod
    def stringToDate(stringField, formatString='%Y-%m-%d %H:%M:%S'):
        stringDate = None
        try:
            stringDate = datetime.strptime(stringField, formatString)
        except ValueError as e:
            print('not a correct date or date format')
        finally:
            return stringDate

        # "%Y-%B-%dT%H:%M:%S-%H:%M"
        # "2015-02-24T13:00:00-08:00"

    @staticmethod
    def CSVtoJson(csvReader):
        header = None
        lines = []
        for row in csvReader:
            if csvReader.line_num == 1:
                header = row
            else:
                lines.append(row)

        content = []
        for line in lines:
            dictObject = {}
            for key, value in zip(header, line):
                dictObject[key] = value
            content.append(dictObject)
        return content

    @staticmethod
    def getStringFromList(list, joiner=' '):
        return joiner.join(list)

    @staticmethod
    def isEmptyDict(dictCall):
        return len(dictCall) == 0

    @staticmethod
    def wrapResponse(results=None, errors=None, info=None):
        return {
            'results': results,
            'errors': errors,
            'info': info,
        }


class APIExtended(GenericAPIView):

    def __init__(self, **kwargs):
        super(APIExtended, self).__init__(**kwargs)
        serializerClass = GenericAPIView.get_serializer_class(self)

        if serializerClass is None:
            raise Exception('There is no serializer attached to this model')

        self.fields = serializerClass.Meta.fields
        self.fieldsNormalized = serializerClass.Meta.fieldsNormalized
        self.parameters = {'model name': serializerClass.Meta.model.__name__,
                           'description': 'This endpoint\'s model has these fields: %s' %
                                          HelperFunctions.getStringFromList(self.fieldsNormalized, ', ')}
        self.oldState = None
        self.pathDict = {
            'create': None,
            'update': None,
            'delete': None,
            'list': None,
            'get': None,
            'default': None
        }

    def options(self, request, *args, **kwargs):

        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        data.pop('renders')
        data.pop('parses')

        # print(data.get('actions'))
        fields = None

        actions = data.get('actions')
        if actions is not None:
            if actions.get('POST'):
                fields = dict(actions.pop('POST'))
            if actions.get('GET'):
                fields = dict(actions.pop('GET'))

            print(fields)
            data['fields'] = {}
            for key in self.fields:
                data['fields'][key] = fields[key]

        for key in self.parameters:
            data[key] = self.parameters[key]

        return Response(data)

    def pathController(self, path):
        for key in self.pathDict:
            if key in path.split('/'):
                return self.pathDict[key]

        if self.pathDict.get('default') is not None:
            return self.pathDict['default']

        raise Exception('This is not a valid endpoint')


    def getRequestData(self, request):
        getSize = len(request.GET)
        postSize = len(request.data)

        getRequestDict = {}

        if getSize != 0:
            getRequestDict = request.GET
        elif postSize != 0:
            getRequestDict = request.data
        else:
            return {}
        print(getRequestDict)
        return getRequestDict
        # with generic view, mapping is not necessary
        #
        # getDict = {}
        # for fieldDB, fieldNormal in zip(self.fields, self.fieldsNormalized):
        #     print(fieldDB, fieldNormal)
        #     getDict[fieldDB] = getRequestDict.get(fieldNormal)
        #
        # print(getDict)
        # print(getDict, request.GET, request.data)
        # return getDict

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    # def changeState(self, serializer):
    #     if self.oldState is None:
    #         # we copy the initial state
    #         self.oldState = serializer.Meta.fields
    #         serializer.Meta.fields = self.fields
    #     else:
    #         serializer.Meta.fields = self.oldState
    #         self.oldState = None
    #
    #
    #     # elif serializer.__name__ != :
    #     #     serializer.Meta.fields = self.oldState
    #     #     self.oldState = None