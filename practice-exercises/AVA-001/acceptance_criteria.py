distance_km = 50
is_raining = False
has_bike = False
has_company_car = True
has_ride_service = True

if not distance_km:
    print('The dispatch will not be carried out.')

elif distance_km <= 15:
    if not is_raining:
        print('Dispatch will be carried out.')
    else:
        print('The dispatch will not be carried out.')

elif distance_km <= 50:
    if has_bike and not is_raining:
        print('Dispatch will be carried out.')
    else:
        print('The dispatch will not be carried out.')

else:
    if has_company_car or has_ride_service:
        print('Dispatch will be carried out.')
    else:
        print('The dispatch will not be carried out.')