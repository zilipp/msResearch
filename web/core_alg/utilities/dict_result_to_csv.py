import csv
from django.http import HttpResponse


def dict_result_to_csv(measurement_result, bone_type):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    writer = csv.writer(response)

    if bone_type == "Femur":
        writer.writerow(['FML', 'FEB', 'FHD', 'FMLD', 'FBML'])
        writer.writerow([measurement_result['fml'], measurement_result['feb'], measurement_result['fhd'],
                        measurement_result['fmld'], measurement_result['fbml']])
    elif bone_type == "Humerus":
        writer.writerow(['HML', 'HHD', 'HEB'])
        writer.writerow([measurement_result['hml'], measurement_result['hhd'], measurement_result['heb']])

    elif bone_type == "Tibia":
        writer.writerow(['TML', 'TPB'])
        writer.writerow([measurement_result['tml'], measurement_result['tpb']])
    else:
        writer.writerow(['RML', 'RMLD'])
        writer.writerow([measurement_result['rml'], measurement_result['rmld']])

    return response
