from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime


def optionHelper(request, view, parameters):
    meta = view.metadata_class()
    data = meta.determine_metadata(request, view)
    data.pop('renders')
    data.pop('parses')
    for key in parameters:
        data[key] = parameters[key]
    return data


def getStringFromList(list, joiner=' '):
    return joiner.join(list)

class APIExtended(APIView):
    def __init__(self, serializerClass, **kwargs):
        super().__init__(**kwargs)

        self.fields = serializerClass.Meta.fields
        self.fieldsNormalized = serializerClass.Meta.fieldsNormalized
        self.parameters = {}

    def options(self, request, *args, **kwargs):
        data = optionHelper(request, self, self.parameters)
        return Response(data)

    def getTransform(self, request):
        getDict = {}
        for fieldDB, fieldNormal in zip(self.fields, self.fieldsNormalized):
            getDict[fieldDB] = request.GET.get(fieldNormal)
        return getDict

    def postTransform(self, request):
        getDict = {}
        for fieldDB, fieldNormal in zip(self.fields, self.fieldsNormalized):
            getDict[fieldDB] = request.data.get(fieldNormal)
        return getDict

    # these are some generic functions that are useful in the filtering process
    def stringOrNoneToFloat(self, stringField):
        return float(stringField) if stringField is not None else 0

    def stringToStringOrNone(self, stringField):
        if stringField in [None, '', 'None']:
            return None
        else:
            return stringField
        # return stringField if stringField != '' and stringField is not None and stringField != 'None' else None

    def stringOrNoneToStringList(self, stringField, splitter=','):
        return stringField.split(splitter) if stringField is not None else None

    def stringOrNoneToIntList(self, stringField, splitter=','):
        if stringField is None:
            return None

        return [int(element) for element in stringField.split(splitter)]

    def stringToDate(self, stringField, formatString='%Y-%m-%d %H:%M:%S'):
        stringDate = None
        try:
            stringDate = datetime.strptime(stringField, formatString)
        except ValueError as e:
            print('not a correct date or date format')
        finally:
            return stringDate

        # "%Y-%B-%dT%H:%M:%S-%H:%M"
        # "2015-02-24T13:00:00-08:00"

    def CSVtoJson(self, csvReader):
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
