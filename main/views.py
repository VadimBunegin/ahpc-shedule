from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlencode
from datetime import datetime
from main.characteristic import ComparatorStrategy, Characteristic, ComparatorResult
from main.forms import EditProfileForm, ProductEditForm, ProductImageForm, UploadUserAvatarForm, \
    ProductAddingForm, CategoryCharacteristicForm, ComparingReviewForm, ApplicationForm, CategoryAddingForm, ProductCategoryForm
from main.forms import RegistrationForm, ProductCategoryEdit

from main.models import User, ComparingReview, Product, UserAvatar, ProductRateFact, \
    ProductCategory, CategoryCharacteristic, StoreManager, StoreProduct, Application, Store, CalcHistory

import datetime
import calendar
import locale
import sys
def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Расписание'}
    ]


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def calc(request):
    context = {}

    a = int(request.GET.get('v1', None))
    b = int(request.GET.get('v2', None))
    context['a'] = a
    context['b'] = b

    record = CalcHistory(
        date=datetime.datetime.now(),
        first=a,
        second=b,
    )

    record.save()
    records = CalcHistory.objects.order_by('-date')
    context['history'] = records

    return render(request, 'calculator.html', context)

def get_base_context(pagename, request):
    context = {'date': datetime.date.today(), 'app': Application.objects.filter(status='under consideration').count(),
               'apps': Application.objects.filter(status='under consideration'), 'pagename': pagename,
               'menu': get_menu_context(), 'week_day': datetime.date.today().strftime("%A")}

    if request.user.is_authenticated:
        context['avatar'] = request.user.get_avatar()
    return context


@login_required
def profile_page(request):
    context = {
        'menu': get_menu_context(),
        'pagename': 'Профиль',
        'votings_count': ComparingReview.objects.filter(author=request.user).count(),
        'ratefact_count': request.user.get_all_product_rate_facts().count(),
        'avatar': request.user.get_avatar(),
    }
    if request.user.is_store_manager():
        # TODO: здесь должны отображаться только товары того магазина, представителем которого юзер является
        context['products'] = Product.objects.all().order_by('rating')
    return render(request, 'pages/profile/profile.html', context)


@login_required
def profile_edit_page(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        'menu': get_menu_context(),
        'pagename': ' Редактирование профиля',
        'votings_count': ComparingReview.objects.filter(author=request.user).count(),
        'ratefact_count': ProductRateFact.objects.filter(user=request.user).count(),
        'form': EditProfileForm(),
        'user': get_object_or_404(User, id=user_id),
        'avatar': request.user.get_avatar()
    }
    context['form2'] = UploadUserAvatarForm(initial={
        'user': context['user']
    })
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        form2 = UploadUserAvatarForm(request.POST, request.FILES)

        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Изменения сохранены', 'alert-success')

        if form2.is_valid():
            try:
                avatar = UserAvatar.objects.filter(user=request.user)[0]
                avatar.user = form2.cleaned_data['user']
                avatar.image = form2.cleaned_data['image']
                avatar.save()
            except IndexError:
                form2.save()
            messages.success(request, 'Аватар сохранен', 'alert-success')
        return redirect('profile')
    return render(request, 'pages/profile/profile_edit.html', context)


def registration_page(request):
    if request.user.is_authenticated:
        messages.error(request, "Залогиненный пользователь не может регистрироваться",
                       extra_tags='alert-danger')
    context = get_base_context('Регистрация', request)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_pass = form.cleaned_data.get('password1')
            avatar = UserAvatar(
                user=user,
                image="https://html5book.ru/wp-content/uploads/2016/10/profile-image.png")
            avatar.save()
            user = authenticate(username=user.username, password=raw_pass)
            login(request, user)
            messages.info(request,
                          'Заполните специальную форму, если Вы - представитель колледжа',
                          'alert-info')
            return redirect(reverse('index'))
    else:
        form = RegistrationForm()
    context['form'] = form
    return render(request, 'registration/registration.html', context)


def registration_store_manager_page(request):
    context = get_base_context('Регистрация представителя', request)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка отправлена', 'alert-success')
            return redirect(reverse('index'))
        messages.error(request, 'Ошибка создания заявки', 'alert-danger')
    else:
        form = ApplicationForm(initial={'user': request.user, 'email': request.user.email})
    context['form'] = form
    return render(request, 'registration/store_manager_new.html', context)

@login_required
def category_add_page(request):
    if request.user.is_staff or request.user.is_store_manager:
        context = get_base_context('Добавление новой группы', request)
        context['form'] = ProductCategoryForm()

        if request.method == "POST":
            form = ProductCategoryForm(request.POST)

            if form.is_valid():
                product = form.save(commit=False)
                product.author = request.user
                product.save()
                context['product'] = product
                messages.success(request, 'Группа успешно создана', 'alert-success')
            else:
                messages.error(request, 'Ошибка создания группы', 'alert-danger')

            return redirect('catalog_reviews')

        return render(request, 'pages/category_add.html', context)

def category_delete(request, product_id):
    if request.user.is_staff or request.user.is_store_manager:
        product = get_object_or_404(ProductCategory, id=product_id)
        product.delete()
        messages.warning(request, 'Категория удалена', 'alert-warning')
    return redirect(reverse('catalog_reviews'))

def category_edit_page(request):
    context = get_base_context('Редактирование групп', request)
    context['category'] = ProductCategory.objects.all()
    return render(request, 'pages/category_edit.html', context)

@login_required
def product_add_page(request):
    if request.user.is_staff or request.user.is_store_manager:
        context = get_base_context('Добавление нового поля', request)
        context['form'] = ProductAddingForm()
        context['image_form'] = ProductImageForm(initial={
            'product': 1
        })

        if request.method == "POST":
            form = ProductAddingForm(request.POST)

            if form.is_valid():
                product = form.save(commit=False)
                product.author = request.user
                product.save()
                context['product'] = product
                messages.success(request, 'Поле успешно создано', 'alert-success')
            else:
                messages.error(request, 'Ошибка создания поля', 'alert-danger')

            return redirect('catalog_reviews')

        return render(request, 'pages/product/add_product.html', context)



@login_required
def product_edit_page(request, product_id):
    if request.user.is_staff or request.user.is_store_manager:
        context = get_base_context('Поля', request)
        context['product'] = get_object_or_404(Product, id=product_id)
        context['form'] = ProductEditForm(instance=context['product'])
        if request.method == "POST":
            product = get_object_or_404(Product, id=product_id)
            form = ProductEditForm(request.POST)
            if form.is_valid():
                product.category = form.cleaned_data['category']
                product.monday = form.cleaned_data['monday']
                product.tuesday = form.cleaned_data['tuesday']
                product.wednesday = form.cleaned_data['wednesday']
                product.thursday = form.cleaned_data['thursday']
                product.friday = form.cleaned_data['friday']
                product.saturday = form.cleaned_data['saturday']
                product.type = form.cleaned_data['type']
                product.comments = form.cleaned_data['comments']
                product.time = form.cleaned_data['time']
                product.auditory = form.cleaned_data['auditory']
                product.teacher = form.cleaned_data['teacher']
                product.week = form.cleaned_data['week']
                product.type_tuesday = form.cleaned_data['type_tuesday']
                product.comments_tuesday = form.cleaned_data['comments_tuesday']
                product.auditory_tuesday = form.cleaned_data['auditory_tuesday']
                product.teacher_tuesday = form.cleaned_data['teacher_tuesday']
                product.type_wednesday = form.cleaned_data['type_wednesday']
                product.comments_wednesday = form.cleaned_data['comments_wednesday']
                product.auditory_wednesday = form.cleaned_data['auditory_wednesday']
                product.teacher_wednesday = form.cleaned_data['teacher_wednesday']
                product.type_thursday = form.cleaned_data['type_thursday']
                product.comments_thursday = form.cleaned_data['comments_thursday']
                product.auditory_thursday = form.cleaned_data['auditory_thursday']
                product.teacher_thursday = form.cleaned_data['teacher_thursday']
                product.type_friday = form.cleaned_data['type_friday']
                product.comments_friday = form.cleaned_data['comments_friday']
                product.auditory_friday = form.cleaned_data['auditory_friday']
                product.teacher_friday = form.cleaned_data['teacher_friday']
                product.type_saturday = form.cleaned_data['type_saturday']
                product.comments_saturday = form.cleaned_data['comments_saturday']
                product.auditory_saturday = form.cleaned_data['auditory_saturday']
                product.teacher_saturday = form.cleaned_data['teacher_saturday']
                product.save()
                messages.success(request, 'Изменения сохранены', 'alert-success')
                return redirect('catalog_reviews')
    return render(request, 'pages/product/product_edit_page.html', context)

def product_delete(request, product_id):
    if request.user.is_staff or request.user.is_store_manager:
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.warning(request, 'Поле удалено', 'alert-warning')
    return redirect(reverse('catalog_reviews'))


@login_required
def applications_page(request):
    if request.user.is_staff or request.user.is_store_manager:
        context = get_base_context('Заявки', request)
        context['avatar'] = request.user.get_avatar()
        context['apps'] = Application.objects.filter(status='under consideration')
    else:
        raise PermissionError('К сожалению, вам отказано в доступе к данной странице')
    return render(request, 'pages/moderation/applications.html', context)


def application_accept(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if not Store.objects.filter(name=application.store_name, address=application.store_address):
        store = Store(name=application.store_name)
        store.save()
    else:
        store = Store.objects.filter(name=application.store_name,
                                     address=application.store_address)[0]

    store_manager = StoreManager(store=store, user=application.user)
    store_manager.save()

    application.status = 'accepted'
    application.save()

    messages.success(request, 'Заявка одобрена', 'alert-success')
    return redirect(reverse('applications'))


def application_reject(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    application.status = 'rejected'
    application.save()
    messages.warning(request, 'Заявка отклонена', 'alert-warning')
    return redirect(reverse('applications'))


def catalog_reviews(request):
    context = get_base_context('Расписание', request)
    context['products'] = Product.objects.all().order_by('-rating')
    context['categories'] = ProductCategory.objects.all()
    if 'category' in request.GET:
        # фильтруем по категории
        category_id = request.GET.get('category')
        try:
            category = get_object_or_404(ProductCategory, id=int(category_id))
            context['filter_category_id'] = category_id
            reviews = Product.objects.filter(category_id=category)
        except ValueError:
            raise Http404
    else:
        reviews = ComparingReview.objects.all()
    context['reviews'] = reviews
    context['review'] = Product.objects.filter(category_id=-1)
    return render(request, 'pages/catalog/catalog_reviews.html', context)
