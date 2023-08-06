import csv
from django.http import HttpResponse, Http404

def export_model_to_csv(model=None):
    """
    Export mode to csv
    :param model:
    :return: file response object (csv)
    """
    if model:
        model_class = model

        meta = model_class._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in model_class.objects.all():
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
    else:
        return Http404