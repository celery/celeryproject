from models import ExtendedFlatPage


def ext_flatpages(request):
    return {'ext_flatpages': ExtendedFlatPage.objects.all()}