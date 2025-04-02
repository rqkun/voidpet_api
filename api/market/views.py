from rest_framework.response import Response
from rest_framework.decorators import api_view

from lib import warframe_market

@api_view(['GET'])
def riven(request):
    type_name = request.GET.get("type")  # Get the export name from the request query

    if not type_name or not type_name in ["items","attributes"]:
        return Response({"error": "Invalid type", "valid_types":["items","attributes"]}, status=400)
    else:
        if type_name=="items":
            return Response(warframe_market.rivens_info("items"))
        else: return Response(warframe_market.rivens_info("attributes"))
