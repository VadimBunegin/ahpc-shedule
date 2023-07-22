from __future__ import annotations

from typing import Optional, List

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.db.models import UniqueConstraint, QuerySet, Q
from django.templatetags.static import static

from main.characteristic import CharacteristicType, ComparatorStrategy


class User(AbstractUser):
    status = models.CharField(max_length=255)
    bonuses = models.IntegerField(default=0)

    def get_all_product_rate_facts(self):
        return ProductRateFact.objects.filter(user=self)

    def get_all_review_rate_facts(self):
        return ReviewRateFact.objects.filter(user=self)

    def get_all_rated_products(self):
        return [fact.product for fact in self.get_all_product_rate_facts()]

    def get_all_rated_reviews(self):
        return [fact.review for fact in self.get_all_review_rate_facts()]

    def is_store_manager(self):
        return StoreManager.objects.filter(user_id=self)

    def get_store(self):
        if not self.is_store_manager():
            raise PermissionError('Пользователь не является представителем магазина')

        store_manager = StoreManager.objects.filter(user_id=self)[0]
        store = store_manager.store
        return store

    def has_already_rated(self, object):
        if isinstance(object, Product):
            return ProductRateFact.objects.filter(user=self, product=object).count() > 0
        elif isinstance(object, ComparingReview):
            return ReviewRateFact.objects.filter(user=self, review=object).count() > 0

    def rate(self, object, rating):
        object.user_rated += 1
        object.rating += rating
        object.rating /= object.user_rated
        object.save()
        fact = ProductRateFact(user=self, product=object, rating=rating) if isinstance(object, Product) else ReviewRateFact(user=self, review=object, rating=rating)
        fact.save()

    def get_avatar(self):
        if self.useravatar_set.count() == 0:
            return static(UserAvatar.get_default_avatar_path())
        return self.useravatar_set.first().image.url


class CalcHistory(models.Model):
    date = models.DateTimeField(default=None)
    first = models.IntegerField(default=None)
    second = models.IntegerField(default=None)
    result = models.IntegerField(default=None)


class UserAvatar(models.Model):
    DEFAULT_AVATAR_PATH = 'imgs/profile_default_avatar.png'

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars')

    @staticmethod
    def get_default_avatar_path():
        return UserAvatar.DEFAULT_AVATAR_PATH

    def __str__(self):
        return self.image.url


class UserSettings(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)


class ProductCategory(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    rating = models.FloatField(default=0.0)
    user_rated = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=10, default='#FFFFFF')

    monday = models.CharField(max_length=300, default='-')
    tuesday = models.CharField(max_length=300, default='-')
    wednesday = models.CharField(max_length=300, default='-')
    thursday = models.CharField(max_length=300, default='-')
    friday = models.CharField(max_length=300, default='-')
    saturday = models.CharField(max_length=300, default='-')

    time = models.CharField(max_length=300, default='00:00')
    type = models.CharField(max_length=300, default='-')
    teacher = models.CharField(max_length=300, default='-')
    auditory = models.CharField(max_length=300, default='-')
    comments = models.CharField(max_length=300, default='-')
    week = models.IntegerField(default=1)

    type_tuesday = models.CharField(max_length=300, default='-')
    teacher_tuesday = models.CharField(max_length=300, default='-')
    auditory_tuesday = models.CharField(max_length=300, default='-')
    comments_tuesday = models.CharField(max_length=300, default='-')

    type_wednesday = models.CharField(max_length=300, default='-')
    teacher_wednesday = models.CharField(max_length=300, default='-')
    auditory_wednesday = models.CharField(max_length=300, default='-')
    comments_wednesday = models.CharField(max_length=300, default='-')

    type_thursday = models.CharField(max_length=300, default='-')
    teacher_thursday = models.CharField(max_length=300, default='-')
    auditory_thursday = models.CharField(max_length=300, default='-')
    comments_thursday = models.CharField(max_length=300, default='-')

    type_friday = models.CharField(max_length=300, default='-')
    teacher_friday = models.CharField(max_length=300, default='-')
    auditory_friday = models.CharField(max_length=300, default='-')
    comments_friday = models.CharField(max_length=300, default='-')

    type_saturday = models.CharField(max_length=300, default='-')
    teacher_saturday = models.CharField(max_length=300, default='-')
    auditory_saturday = models.CharField(max_length=300, default='-')
    comments_saturday = models.CharField(max_length=300, default='-')

    def __str__(self):
        return self.title

    def get_reviews_with_product(self):
        """
        Находим все обзоры, в которых участвует данный товар
        """
        return ComparingReview.objects.filter(Q(first=self) | Q(second=self)).order_by('-created_at')

    def get_comparable_products(self):
        """
        Находим все товары, которые сравнивались с данным в обзорах
        """
        reviews = self.get_reviews_with_product()
        comparing_products = []
        for review in reviews:
            comparing_products.append(
                {
                    'product': review.first if review.second==self else review.second,
                    'review': review
                }
            )
        return comparing_products

    @staticmethod
    def compare_products(product1: Product, product2: Product):
        if product1.category != product2.category:
            raise AttributeError('Нельзя сравнивать продукты из разных категорий')
        characteristics: QuerySet = product1.category.categorycharacteristic_set.all()
        result = {
            'first': product1,
            'second': product2,
            'comparation': {}
        }
        for characteristic in characteristics:
            comparator_cls = ComparatorStrategy.get_comparator_type(characteristic.comparator)

            p1_characteristic = product1.productcharacteristic_set.get(
                characteristic=characteristic
            )

            p2_characteristic = product2.productcharacteristic_set.get(
                characteristic=characteristic
            )

            if characteristic.comparator != ComparatorStrategy.RATING:
                comparator = comparator_cls(p1_characteristic, p2_characteristic)
            else:
                characteristic_rating = CategoryStringCharacteristicRating.objects.filter(
                    characteristic=characteristic
                ).order_by('rating')
                comparator = comparator_cls(
                    p1_characteristic,
                    p2_characteristic,
                    [{'value': item.value, 'rating': item.rating} for item in characteristic_rating]
                )
            compare = comparator.compare()
            result['comparation'][characteristic.name] = {
                'compare': compare
            }
        return result

    def is_confirmed(self):
        return StoreProduct.objects.filter(product=self)

    def get_images(self) -> List[str]:
        if self.productimage_set.count() == 0:
            return [static(ProductImage.get_default_image_path())]
        return [record.image.url for record in self.productimage_set.all()]


class ProductImage(models.Model):
    DEFAULT_IMAGE_PATH = 'imgs/src/logo_notitle.png'
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images', blank=True)

    @staticmethod
    def get_default_image_path():
        return ProductImage.DEFAULT_IMAGE_PATH


class CategoryCharacteristic(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    value_type = models.IntegerField(choices=CharacteristicType.choices,
                                     default=0)  # 0 - число, 1 - строка
    category = models.ForeignKey(to=ProductCategory,
                                 on_delete=models.CASCADE)
    comparator = models.IntegerField(choices=ComparatorStrategy.choices,
                                     default=ComparatorStrategy.SMALLER)

    def __str__(self):
        return f'Характеристика "{self.name}". ' \
               f'Тип: "{CharacteristicType.get_name_by_value(self.value_type)}". ' \
               f'Стратегия сравнения: "{ComparatorStrategy.get_name_by_value(self.comparator)}"'


class CategoryStringCharacteristicRating(models.Model):
    characteristic = models.ForeignKey(to=CategoryCharacteristic, on_delete=models.CASCADE)
    value = models.CharField(max_length=3000)
    rating = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['characteristic', 'rating'], name='unique_votefact')
        ]

    @staticmethod
    @transaction.atomic  # <--- Если приложение умрёт в функции -
    # мы не приведём БД в неконсистентное состояние
    def insert_new_rating(rating_list: QuerySet,
                          characteristic: CategoryCharacteristic,
                          rating: int) -> CategoryStringCharacteristicRating:
        rating_list = rating_list.filter(rating__gte=rating).order_by('-rating')
        for entry in rating_list:
            entry.rating += 1
            entry.save()
        return CategoryStringCharacteristicRating.objects.create(
            characteristic=characteristic, rating=rating
        )

    def add_new(self, characteristic: CategoryCharacteristic, rating: Optional[int] = None):
        # Если пустой рейтинг - ставим в конец
        if characteristic.value_type != CharacteristicType.str:
            raise ValueError('Only string characteristics allowed')

        rating_list = CategoryStringCharacteristicRating.objects.filter(
            characteristic=characteristic
        )

        if rating_list.count() == 0:
            return CategoryStringCharacteristicRating.objects.create(
                characteristic=characteristic, rating=1
            )

        if rating is None:
            max_rating = rating_list.order_by('-rating').first().rating
            return CategoryStringCharacteristicRating.objects.create(
                characteristic=characteristic, rating=max_rating + 1
            )

        return self.insert_new_rating(rating_list, characteristic, rating)


class ProductCharacteristic(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    characteristic = models.ForeignKey(to=CategoryCharacteristic, on_delete=models.CASCADE)
    value = models.CharField(max_length=300)


class Store(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300, default='')
    logo = models.ImageField(upload_to='store_logos', default='default_store_logo.png')

    def __str__(self):
        return self.name


class StoreManager(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    store = models.ForeignKey(to=Store, on_delete=models.CASCADE)


class StoreProduct(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    store = models.ForeignKey(to=Store, on_delete=models.CASCADE)


class Application(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    email = models.EmailField()
    store_name = models.CharField(max_length=300)
    store_address = models.IntegerField(default=0)
    status = models.CharField(max_length=300, default='under consideration')


class ComparingReview(models.Model):
    name = models.CharField(max_length=300)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    description = models.TextField()
    first = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='first')
    second = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='second')
    view_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    user_rated = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_images(self):
        return {
            'first': self.first.get_images()[0],
            'second': self.second.get_images()[0]
        }


class ProductRateFact(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    rating = models.IntegerField()


class ReviewRateFact(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    review = models.ForeignKey(to=ComparingReview, on_delete=models.CASCADE)
    rating = models.IntegerField()
