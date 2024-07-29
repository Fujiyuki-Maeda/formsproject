# Standard library imports
import csv
import os
from datetime import datetime

# Related third party imports
import phonenumbers
from phonenumbers.phonenumberutil import format_number, PhoneNumberFormat
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.contrib import messages

# Local imports
from .filters import ItemFilter
from .forms import ItemForm, JapanesePhoneNumberField
from .models import Item


# Create your views.py

# 検索一覧画面
class ItemFilterView(LoginRequiredMixin, FilterView):
    model = Item
    filterset_class = ItemFilter
    # デフォルトの並び順を新しい順とする
    queryset = Item.objects.all().order_by('-created_at')

    # クエリ未指定の時に全件検索を行うために以下のオプションを指定（django-filter2.0以降）
    strict = False

    # 1ページあたりの表示件数
    paginate_by = 10

    # 検索条件をセッションに保存する or 呼び出す
    def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)


# 詳細画面
class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item


# 登録画面
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['phone_number'] = JapanesePhoneNumberField(region='JP')
        return form

# 更新画面
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['phone_number'] = JapanesePhoneNumberField(region='JP')
        return form


# 削除画面
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('index')

def post_export(request):
    # CSVファイルの保存先ディレクトリ
    csv_dir = os.path.join(os.path.expanduser("~"), "OneDrive", "デスクトップ", "csv")

    
    # ディレクトリが存在しない場合は作成する
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    
    # CSVファイルのパス
    csv_path = os.path.join(csv_dir, "会員データ取込用.csv")
    
    # データの取得
    items = Item.objects.all()
    
    # ユーザーに確認を取る
    if request.method == 'POST':
        if 'export' in request.POST:
            # データがある場合のみCSVファイルを作成する
            if items.exists():
                # CSVファイルの書き込み
                with open(csv_path, "w", newline="", encoding="Shift-JIS") as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # ヘッダーを追加
                    writer.writerow([
                        '会員証コード(10桁)', '有効フラグ(0:無効 1:有効)', '会員コード(10桁)', '会員名称',
                        '郵便番号', '住所1', '住所2', 'TEL', '携帯電話', '連絡先(住所)', '連絡先TEL',
                        'ＥメールアドレスＰＣ', 'Ｅメールアドレス携帯', '会員名（カナ）', 'コメント1',
                        '入会日付(yyyy-mm-dd)', '会員有効日付(yyyy-mm-dd)', '生年月日(yyyy-mm-dd)',
                        '性別(1:男 2:女)', 'ランク(任意)', '警告区分(0:一般 7:警告1 8:警告2 9:ブラック)',
                        '地域コード', '最終来店日付(yyyy-mm-dd)', '証明の種類(0:なし 1:免許証 2:保険証 3:学生証 4:パスポート)',
                        '入会店舗コード', 'ポイント残', 'DM可否(0:可 1:不可)', 'ポイント有効期限', 'インボイス登録番号',
                        'インボイス登録年月日'
                    ])
                    
                    # データを書き込む
                    for post in items:
                        current_date = datetime.now().strftime('%Y-%m-%d')
                        csv_data = f"{post.birth_year}/{post.birth_month}/{post.birth_day}"
                        
                        # 電話番号の整形
                        phone_number = phonenumbers.parse(str(post.phone_number), 'JP')
                        formatted_phone_number = format_number(phone_number, PhoneNumberFormat.NATIONAL)
                        
                        writer.writerow([post.member_no, 1, post.member_no, post.name, post.zip_code, post.prefecture, 
                                     post.city + post.address1 + post.address2, formatted_phone_number, formatted_phone_number,
                                     "","","","",post.furigana,"",current_date,"",
                                     csv_data,post.gender,"","","","",post.id_number,1])
                
                # データ削除の処理を追加
                items.delete()
                
                # ダウンロードのためのレスポンスを返す
                response = HttpResponse(content_type='text/csv; charset=UTF-8')
                response['Content-Disposition'] = f'attachment; filename="会員データ取込用.csv"'
                
                return response
            else:
                messages.warning(request, 'エクスポートするデータがありません。')
        elif 'cancel' in request.POST:
            messages.info(request, 'エクスポートをキャンセルしました。')
            
        return redirect('index')
    
    # 確認画面を表示
    return render(request, 'formsapp/export_confirm.html', {'items': items})#formsappから入れないとエラー
