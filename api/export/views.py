from enum import Enum
from rest_framework.response import Response
from rest_framework.decorators import api_view

from lib import warframe_export
from lib.classes.export import AppExports


@api_view(['GET'])
def export(request):
    export_name = request.GET.get("file")  # Get the export name from the request query

    if not export_name or not hasattr(AppExports, export_name):
        return Response({"error": "Invalid file name"}, status=400)

    export_enum = getattr(AppExports, export_name)  # Get the enum member dynamically
    return Response(warframe_export.export_open(export_enum.value))