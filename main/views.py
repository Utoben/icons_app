from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from .tasks import *

def home(request):
    images = Image.objects.all()
    user_profile = UserProfile.objects.get(user=request.user)

    choised_icons = user_profile.chosen_images.all()

    context = {
        'images': images,
        'title': 'Главная страница',
        'choised_icons': choised_icons,
    }
    return render(request, 'main/home.html', context)

def bucket_view(request):
    title = 'Значки в корзине'
    user_profile = UserProfile.objects.get(user=request.user)
    icons = user_profile.chosen_images.all()
    icons_count = icons.count()

    context = {
        'title' : title,
        'icons' : icons,
        'icons_count' : icons_count,
    }

    return render(request, 'main/bucket.html', context)

# роуты

def choise(request) -> JsonResponse:
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            image_id = request.POST.get('image_id')
            image = Image.objects.get(id=image_id)
            user_profile.chosen_images.add(image)
            user_profile.save()

            print(f'Картинка {image.pk} выбрана: {image.is_choised}')
            return JsonResponse({'success': True,})
        except Image.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image not found'})
    else:
        return JsonResponse({'success': False})
    
def clear_bucket(request) -> JsonResponse:
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.chosen_images.clear()
        print(f'Корзина очищена')
        return JsonResponse({'success': True,})
    else:
        return JsonResponse({'success': False})
    
def get_profile_info(request) -> JsonResponse:
    if request.method == 'GET':
        user_profile = UserProfile.objects.get(user=request.user)
        fullname = f'{user_profile.surname} {user_profile.name} {user_profile.patronymic}'
        phone = f'{user_profile.phone}'
        email = f'{user_profile.email}'
        print(f'Инфо по профилю передана: {fullname} {phone} {email}')

        return JsonResponse({'success': True, 'fullname': fullname, 'phone': phone, 'email': email,})
    else:
        return JsonResponse({'success': False})
    

# отправка заказа
def send_order(request) -> JsonResponse:
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        icons = get_userprofile(request.user)
        print(f'ИКОНКИ: {icons}')

        icons_names = get_icons_names(icons)
        print(f'ИКОНКИ: {icons_names}')

        count = icons.count()
        
        print(f'Пришли: {fullname} {phone} {email}')

        # отправка письма заказчику
        long_send_customer_email(fullname, phone, email, count)
        # отправка письма исполнителю
        long_send_order_email(email, icons_names, count)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
        
# выбор имен заказаных изображений
def get_icons_names(icons: list[Image]) -> str:
    return ', '.join([icon.file_name for icon in icons]) if icons else ''

# получение профиля пользователя
def get_userprofile(user) -> list[Image]:
    user_profile = UserProfile.objects.get(user=user)
    return user_profile.chosen_images.all()
