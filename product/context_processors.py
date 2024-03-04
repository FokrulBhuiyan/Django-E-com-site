from .models import Category

def categories(request):
    # categories = Category.objects.all()
    # print(categories)
    return {"categories": Category.objects.all()}