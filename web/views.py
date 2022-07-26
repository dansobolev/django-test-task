import json

from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Bill, Shop, Entity, Customer
from .utils import convert_str_to_date_object
from .serializers import EntitySerializer


class FileUploadView(APIView):

    parser_classes = (MultiPartParser, )

    def save_data_to_db(self, data: dict):
        for bill in data['bills']:
            shop_name = bill['shop']
            shop, _ = Shop.objects.get_or_create(shop_name=shop_name)
            customer_name = bill['user']
            customer, _ = Customer.objects.get_or_create(customer_name=customer_name)

            bill_data = {
                'user': customer,
                'bill_id': bill['bill_id'],
                'shop': shop,
                'bill_sum': sum([entity['price'] for entity in bill['items']]),
            }
            bill_obj = Bill.objects.create(**bill_data)

            for entity in bill['items']:
                entity_data = {
                    'name': entity['name'],
                    'quantity': entity['quantity'],
                    'price': entity['price'],
                    'entity_sum': entity['quantity'] * entity['price'],
                    'bill': bill_obj
                }
                Entity.objects.create(**entity_data)

    def post(self, request):
        data = request.data['file'].read()
        data = json.loads(data)
        self.save_data_to_db(data)
        return Response({'Status': 'File has been successfully uploaded'})


class ListGoodsBoughtByCustomer(APIView):

    def get(self, request, customer_id):
        bills = [bil.id for bil in Bill.objects.filter(user=customer_id)]
        customer_goods = [obj.name for obj in Entity.objects.filter(bill__in=bills)]
        return Response(customer_goods)


class ListShopsByCustomer(APIView):

    def get(self, request, customer_id):
        customer_shops = [bil.shop.shop_name for bil in Bill.objects.filter(user=customer_id)]
        return Response(set(customer_shops))


class ListGoodIntervalDate(APIView):

    def get(self, request, customer_id):
        start = convert_str_to_date_object(request.GET['start'])
        end = convert_str_to_date_object(request.GET['end'])

        bills = Bill.objects.filter(user=customer_id).\
            filter(created_at__gte=start, created_at__lte=end)
        return Response([bill.bill_sum for bill in bills])


class ListBillsWithGoodsWithingDataIntervals(APIView):

    def get(self, request, customer_id):
        specific = request.GET.get('specific')
        if not specific:
            start = convert_str_to_date_object(request.GET['start'])
            end = convert_str_to_date_object(request.GET['end'])
            bills_list = Bill.objects.filter(user=customer_id). \
                filter(created_at__gte=start, created_at__lte=end)
        else:
            specific = convert_str_to_date_object(specific)
            bills_list = Bill.objects.filter(user=customer_id). \
                filter(created_at=specific)

        customer_goods = EntitySerializer(Entity.objects.filter(bill__in=[bill.id for bill in bills_list]), many=True)

        return Response(customer_goods.data)
