from rest_framework.response import Response
from rest_framework.decorators import api_view

from lib import warframe_status
from services.world import alert as alert_services
from services.world import event as event_services
from services.world import varzia as vault_services
from services.world import void as void_services
from services.world import invasion as invasion_services
@api_view(['GET'])
def world(request):
    return Response(warframe_status.world())


@api_view(['GET'])
def void(request):
    """Call the warframe status api for baro  data.

    Returns:
        dict: Json data of the api response.
    """
    return Response(void_services.info())


@api_view(['GET'])
def vault(request):
    """Call the warframe status api for varzia data.

    Returns:
        dict: Json data of the api response.
    """
    option = request.GET.get("option")  # Get the export name from the request query

    if option and option=="pack":
        return Response(vault_services.pack())
    else:    
        return Response(vault_services.info())


@api_view(['GET'])
def alert(request):
    """Call warframe status api for alert data.

    Returns:
        dict: alerts data | None
    """
    return Response(alert_services.info())


@api_view(['GET'])
def invasion(request):
    return Response(invasion_services.info())


@api_view(['GET'])
def event(request):
    """Call warframe status api for event data.

    Returns:
        dict: events data | None
    """
    return Response(event_services.info())