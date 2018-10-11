from django.db import models
from django.contrib.auth import get_user_model

from datetime import datetime

User = get_user_model()
# Create your models here.


class TextModel(models.Model):
    TEXT_TYPES = (
        ('plant', '种植'),
        ('aquaculture', '水产养殖'),
        ('agri_industry', '农资业'),
        ('agri_and_sideline_industries', '农副加工业'),
        ('animal', '畜牧业'),
    )

    FILE_TYPES = (
        ('docx', 'word文档'),
        ('pptx', 'ppt文档'),
        ('xlsx', 'excel文档'),
        ('pdf', 'pdf文档'),
    )

    user = models.ForeignKey(User, default=None, related_name='text_of_user', verbose_name='上传用户', help_text='上传用户')
    text = models.FileField(max_length=79, upload_to='text/%Y/%m/%d', verbose_name='文档', help_text='文档')
    text_type = models.CharField(max_length=50, default='plant', choices=TEXT_TYPES, verbose_name='文档类型', help_text='文档类型')
    file_type = models.CharField(max_length=20, default='docx', choices=FILE_TYPES, verbose_name='上传文件的格式', help_text='上传文件的格式')
    file_size = models.CharField(default='', max_length=20, verbose_name='文件大小统计', help_text='文件大小统计')
    file_name = models.CharField(default='', max_length=59, verbose_name='文件名', help_text='文件名')
    download_nums = models.IntegerField(default=0, verbose_name='下载量', help_text='下载量')
    pdf_path = models.CharField(default='', max_length=120, verbose_name='pdf_地址', help_text='pdf_地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='文档添加时间', help_text='文档添加时间')

    def __str__(self):
        return self.get_text_type_display()

    class Meta:
        verbose_name = '文件上传表'
        verbose_name_plural = verbose_name

