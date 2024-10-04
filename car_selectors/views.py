from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from car_selectors.models import CarType

@api_view(['GET'])
def car_search(request):
    query = request.query_params.get('query', '')
    words = [word.strip() for word in query.split()]
    words.sort(key=len, reverse=True)

    search_query = Q()

    for word in words:
        if word.isdigit() and 1900 <= int(word) <= 2200:
            year = int(word)
            search_query &= (Q(start_year__lte=year) & (Q(end_year__gte=year) | Q(end_year__isnull=True)))
        elif len(word) <= 3 and word.isupper():
            # Assume it's a region, probably would be better if I had a separate table for regions
            search_query &= (
                Q(model__make__region__icontains=word) |
                Q(model__make__name__icontains=word) |
                Q(name__icontains=word) | 
                Q(model__name__icontains=word) 
            )
        else:
            search_query &= (
                Q(model__make__name__icontains=word) |
                Q(model__name__icontains=word) |  
                Q(name__icontains=word) | 
                Q(model__make__region__icontains=word)
            )

    filtered_car_types = CarType.objects.filter(search_query).select_related('model__make')
    # print(filtered_car_types.query)
    items = []
    for car_type in filtered_car_types:
        items.append({
            "make": car_type.model.make.name + ((" (" + car_type.model.make.region + ")") if car_type.model.make.region else ""),
            "model": car_type.model.name,
            "car_type": car_type.name + " (" + str(car_type.start_year) + "-" + (str(car_type.end_year) if car_type.end_year else "") + ")",
            "car_type_id": car_type.id,
        })

    return Response({'items': items})
