from django.db import models
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField

class Item(models.Model):
    GENDER_CHOICES = [
        (1, '男性'),
        (2, '女性'),
    ]
    
    ID_CHOICES = [
        (1, '免許証'),
        (4, 'パスポート'),
        (5, 'その他(A4)'),
    ]


    member_no = models.CharField(
        verbose_name='会員番号',
        max_length=20,
    )

    id_number = models.IntegerField(
        verbose_name='証明の種類',
        choices=ID_CHOICES,
    )
    
    name = models.CharField(
        verbose_name='氏名',
        max_length=100,
    )

    furigana = models.CharField(
        verbose_name='フリガナ',
        max_length=100,
    )

    gender = models.IntegerField(
        verbose_name='性別',
        choices=GENDER_CHOICES,
    )

    birth_year = models.IntegerField(
        verbose_name='年',
        validators=[validators.MinValueValidator(1900), validators.MaxValueValidator(2100)],
    )

    birth_month = models.IntegerField(
        verbose_name='月',
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(12)],
    )

    birth_day = models.IntegerField(
        verbose_name='日',
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(31)],
    )

    phone_number = PhoneNumberField(
        verbose_name='電話番号',
        null=True,
        blank=True,
    )

    zip_code = models.CharField(
        verbose_name='郵便番号',
        max_length=7,
    )

    prefecture = models.CharField(
        verbose_name='都道府県',
        max_length=4,
    )

    city = models.CharField(
        verbose_name='市区町村',
        max_length=100,
    )

    address1 = models.CharField(
        verbose_name='住所1',
        max_length=100,
    )

    address2 = models.CharField(
        verbose_name='住所2',
        max_length=100,
        blank=True,
        null=True,
    )
    
    created_at = models.DateTimeField(
        verbose_name='登録日',
        auto_now_add=True
    )

    FULL_TO_HALF = {
    'ア': 'ｱ', 'イ': 'ｲ', 'ウ': 'ｳ', 'エ': 'ｴ', 'オ': 'ｵ',
    'カ': 'ｶ', 'キ': 'ｷ', 'ク': 'ｸ', 'ケ': 'ｹ', 'コ': 'ｺ',
    'サ': 'ｻ', 'シ': 'ｼ', 'ス': 'ｽ', 'セ': 'ｾ', 'ソ': 'ｿ',
    'タ': 'ﾀ', 'チ': 'ﾁ', 'ツ': 'ﾂ', 'テ': 'ﾃ', 'ト': 'ﾄ',
    'ナ': 'ﾅ', 'ニ': 'ﾆ', 'ヌ': 'ﾇ', 'ネ': 'ﾈ', 'ノ': 'ﾉ',
    'ハ': 'ﾊ', 'ヒ': 'ﾋ', 'フ': 'ﾌ', 'ヘ': 'ﾍ', 'ホ': 'ﾎ',
    'マ': 'ﾏ', 'ミ': 'ﾐ', 'ム': 'ﾑ', 'メ': 'ﾒ', 'モ': 'ﾓ',
    'ヤ': 'ﾔ', 'ユ': 'ﾕ', 'ヨ': 'ﾖ',
    'ラ': 'ﾗ', 'リ': 'ﾘ', 'ル': 'ﾙ', 'レ': 'ﾚ', 'ロ': 'ﾛ',
    'ワ': 'ﾜ', 'ヲ': 'ｦ', 'ン': 'ﾝ',
    'ガ': 'ｶﾞ', 'ギ': 'ｷﾞ', 'グ': 'ｸﾞ', 'ゲ': 'ｹﾞ', 'ゴ': 'ｺﾞ',
    'ザ': 'ｻﾞ', 'ジ': 'ｼﾞ', 'ズ': 'ｽﾞ', 'ゼ': 'ｾﾞ', 'ゾ': 'ｿﾞ',
    'ダ': 'ﾀﾞ', 'ヂ': 'ﾁﾞ', 'ヅ': 'ﾂﾞ', 'デ': 'ﾃﾞ', 'ド': 'ﾄﾞ',
    'バ': 'ﾊﾞ', 'ビ': 'ﾋﾞ', 'ブ': 'ﾌﾞ', 'ベ': 'ﾍﾞ', 'ボ': 'ﾎﾞ',
    'パ': 'ﾊﾟ', 'ピ': 'ﾋﾟ', 'プ': 'ﾌﾟ', 'ペ': 'ﾍﾟ', 'ポ': 'ﾎﾟ'
}

    def save(self, *args, **kwargs):
        self.furigana = self.convert_to_half_width(self.furigana)
        super().save(*args, **kwargs)

    def convert_to_half_width(self, text):
        return ''.join(self.FULL_TO_HALF.get(c, c) for c in text)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '会員'
        verbose_name_plural = '会員'
