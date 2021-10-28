from rest_framework.response import Response
from rest_framework.views import APIView

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
