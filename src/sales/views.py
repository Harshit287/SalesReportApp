from heapq import merge
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from numpy import product
from .models import Sale
from .forms import SaleSearchForm
from reports.forms import ReportForm
import pandas as pd
from .utils import get_customer_from_id,get_salesman_from_id,get_chart

# Create your views here.

def home_view(request):
    sales_df = None
    position_df = None
    merged_df = None
    df = None
    chart = None
    no_data = None

    search_form = SaleSearchForm(request.POST or None)
    report_form = ReportForm()

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
        print('date_from:', date_from, 'date_to:', date_to, 'chart_type:', chart_type)
        sale_qs = Sale.objects.filter(created__date__gte= date_from,created__date__lte= date_to)
        if len(sale_qs) > 0 :
            sales_df = pd.DataFrame(sale_qs.values())
            # print('Sales df')
            # print(sales_df)
            sales_df['customer_id'] =sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] =sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] =sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({'customer_id':'customer','salesman_id':'salesman','id':'sales_id'}, axis=1, inplace=True)
            # sales_df['sales_id'] = sales_df['id']
            
            position_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id' : pos.id,
                        'product' : pos.product.name,
                        'quantity' : pos.quantity,
                        'price' : pos.price,
                        'sales_id' : pos.get_sales_id()
                    }
                    position_data.append(obj)
            position_df = pd.DataFrame(position_data)
            # print('position df')
            # print(position_df)
            merged_df = pd.merge(sales_df,position_df,on='sales_id')

            df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')
            chart = get_chart(chart_type, sales_df, results_by)

            sales_df = sales_df.to_html()
            position_df = position_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()
            
        else:
            no_data = "No data is available in this date range!!"

    context = {
        'search_form' : search_form,
        'report_form' : report_form,
        'sales_df' : sales_df,
        'position_df' : position_df,
        'merged_df' : merged_df,
        'df' : df,
        'chart': chart,
        'no_data': no_data,
    }
    return render(request, 'sales/home.html', context)

class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'