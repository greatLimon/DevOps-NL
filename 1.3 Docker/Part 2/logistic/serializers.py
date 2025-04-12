from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']
    


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    product = ProductSerializer
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price'] 


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    # настройте сериализатор для склада
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for position in positions:
            obj = StockProduct(
                stock = stock, 
                product = position['product'], 
                quantity = position['quantity'],
                price = position['price']
                ).save()
        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for position in positions:
            try:
                obj = StockProduct.objects.get(stock = stock, product = position['product'])
                obj.quantity = position['quantity']
                obj.price = position['price']
            except ObjectDoesNotExist:
                obj = StockProduct(
                stock = stock, 
                product = position['product'], 
                quantity = position['quantity'],
                price = position['price']
                )
            obj.save()


        
        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
