from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

from main.models import User, Product, ProductImage, UserAvatar, \
    ComparingReview, CategoryCharacteristic, Application, ProductCategory


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    agreement_checked = forms.BooleanField(
        label='Я принимаю условия соглашения',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class CreateVotingForm(forms.Form):
    title = forms.CharField(
        label='Название голосования',
        required=True
    )
    description = forms.CharField(
        label='Описание голосования',
        required=True
    )
    type = forms.IntegerField(
        label='Тип голосования',
        min_value=1,
        max_value=3,
        required=True
    )


class EditVotingForm(forms.Form):
    title = forms.CharField(
        label='Название голосования',
        required=True
    )
    description = forms.CharField(
        label='Описание голосования',
        required=True
    )


class EditProfileForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        required=True
    )
    email = forms.CharField(
        label='Email',
        required=True
    )


class UploadUserAvatarForm(forms.ModelForm):
    class Meta:
        model = UserAvatar
        fields = ['user', 'image']
        widgets = {'user': forms.HiddenInput()}
        labels = {'image': 'Фотография профиля'}


class ProductAddingForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'time', 'week',
                  'monday', 'type', 'comments', 'auditory', 'teacher', 'tuesday',
                  'type_tuesday', 'comments_tuesday', 'auditory_tuesday', 'teacher_tuesday',
                  'wednesday', 'type_wednesday', 'comments_wednesday', 'auditory_wednesday', 'teacher_wednesday',
                  'thursday', 'type_thursday', 'comments_thursday', 'auditory_thursday', 'teacher_thursday',
                  'friday', 'type_friday', 'comments_friday', 'auditory_friday', 'teacher_friday',
                  'saturday', 'type_saturday', 'comments_saturday', 'auditory_saturday', 'teacher_saturday']
        labels = {'category': 'Группа',
                  'time': 'Время',
                  'week': 'Неделя',
                  'monday': 'Предмет понедельник',
                  'tuesday': 'Предмет вторник',
                  'wednesday': 'Предмет среда',
                  'thursday': 'Предмет четверг',
                  'friday': 'Предмет пятница',
                  'saturday': 'Предмет суббота',
                  'type': 'Тип понедельник',
                  'comments': 'Комментарий понедельник',
                  'auditory': 'Аудитория понедельник',
                  'teacher': 'Преподаватель понедельник',
                  'type_tuesday': 'Тип вторник',
                  'comments_tuesday': 'Комментарий вторник',
                  'auditory_tuesday': 'Аудитория вторник',
                  'teacher_tuesday': 'Преподаватель вторник',
                  'type_wednesday': 'Тип среда',
                  'comments_wednesday': 'Комментарий среда',
                  'auditory_wednesday': 'Аудитория среда',
                  'teacher_wednesday': 'Преподаватель среда',
                  'type_thursday': 'Тип четверг',
                  'comments_thursday': 'Комментарий четверг',
                  'auditory_thursday': 'Аудитория четверг',
                  'teacher_thursday': 'Преподаватель четверг',
                  'type_friday': 'Тип пятница',
                  'comments_friday': 'Комментарий пятница',
                  'auditory_friday': 'Аудитория пятница',
                  'teacher_friday': 'Преподаватель пятница',
                  'type_saturday': 'Тип суббота',
                  'comments_saturday': 'Комментарий суббота',
                  'auditory_saturday': 'Аудитория суббота',
                  'teacher_saturday': 'Преподаватель суббота'}
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }


class CategoryAddingForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', ]
        labels = {'name': 'имя'}


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'time', 'week',
                  'monday', 'type', 'comments', 'auditory', 'teacher', 'tuesday',
                  'type_tuesday', 'comments_tuesday', 'auditory_tuesday', 'teacher_tuesday',
                  'wednesday', 'type_wednesday', 'comments_wednesday', 'auditory_wednesday', 'teacher_wednesday',
                  'thursday', 'type_thursday', 'comments_thursday', 'auditory_thursday', 'teacher_thursday',
                  'friday', 'type_friday', 'comments_friday', 'auditory_friday', 'teacher_friday',
                  'saturday', 'type_saturday', 'comments_saturday', 'auditory_saturday', 'teacher_saturday']
        labels = {'category': 'Группа',
                  'time': 'Время',
                  'week': 'Неделя',
                  'monday': 'Предмет понедельник',
                  'tuesday': 'Предмет вторник',
                  'wednesday': 'Предмет среда',
                  'thursday': 'Предмет четверг',
                  'friday': 'Предмет пятница',
                  'saturday': 'Предмет суббота',
                  'type': 'Тип понедельник',
                  'comments': 'Комментарий понедельник',
                  'auditory': 'Аудитория понедельник',
                  'teacher': 'Преподаватель понедельник',
                  'type_tuesday': 'Тип вторник',
                  'comments_tuesday': 'Комментарий вторник',
                  'auditory_tuesday': 'Аудитория вторник',
                  'teacher_tuesday': 'Преподаватель вторник',
                  'type_wednesday': 'Тип среда',
                  'comments_wednesday': 'Комментарий среда',
                  'auditory_wednesday': 'Аудитория среда',
                  'teacher_wednesday': 'Преподаватель среда',
                  'type_thursday': 'Тип четверг',
                  'comments_thursday': 'Комментарий четверг',
                  'auditory_thursday': 'Аудитория четверг',
                  'teacher_thursday': 'Преподаватель четверг',
                  'type_friday': 'Тип пятница',
                  'comments_friday': 'Комментарий пятница',
                  'auditory_friday': 'Аудитория пятница',
                  'teacher_friday': 'Преподаватель пятница',
                  'type_saturday': 'Тип суббота',
                  'comments_saturday': 'Комментарий суббота',
                  'auditory_saturday': 'Аудитория суббота',
                  'teacher_saturday': 'Преподаватель суббота'}
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name']
        labels = {'name': 'Группа'}

class ProductCategoryEdit(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name']
        labels = {'name': 'Группа'}

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product', 'image']
        widgets = {'product': forms.HiddenInput()}
        labels = {'image': 'Загрузить фотографию'}


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['user', 'email', 'store_name']
        labels = {'store_name': 'Комментарий'}
        widgets = {'user': forms.HiddenInput(), 'email': forms.HiddenInput()}


class ComparingReviewForm(forms.ModelForm):
    class Meta:
        model = ComparingReview
        fields = ['name', 'author', 'description', 'first', 'second']
        widgets = {'author': forms.HiddenInput()}
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'first': 'Первый товар',
            'second': 'Второй товар'
        }


class CategoryCharacteristicForm(forms.ModelForm):
    class Meta:
        model = CategoryCharacteristic
        fields = ['name', 'description', 'category', 'value_type', 'comparator']
        widgets = {
            'category': forms.HiddenInput(),
            'name': forms.TextInput(),
            'description': forms.TextInput()
        }

    def __init__(self, cat_id, char_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('category_characteristics_edit',
                                          kwargs={'category_id': cat_id, 'char_id': char_id})
        self.helper.layout = Layout(
            Div(
                Div('name', css_class='col'),
                Div('description', css_class='col'),
                'category',
                Div('value_type', css_class='col'),
                Div('comparator', css_class='col'),
                Div(Submit('submit', 'Submit', css_class='btn btn-primary'), css_class='col'),
                css_class='row',
            ),
        )
