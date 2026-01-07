import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validasi_file(value):
    limit_mb = 5
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Ukuran file terlalu besar. Maksimal {limit_mb}MB.")
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.txt']
    if not ext.lower() in valid_extensions :
        raise ValidationError("Format file tidak didukung")
    
def user_dir(instance, filename):
    ext = filename.split('.')[-1]
    filename_baru = f"{uuid.uuid4()}.{ext}"
    return 'upload/user_{0}/{1}'.format(instance.user.id, filename_baru)

class Brankas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    judul = models.CharField(max_length=200)
    catatan = models.TextField(blank=True, null=True)
    file_rahasia = models.FileField(
        upload_to=user_dir,
        validators=[validasi_file],
        blank=True, null=True
        )

    waktu_dibuat = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.judul} - milik {self.user.username}"
    
    def delete(self, *args, **kwargs):
        if self.file_rahasia:
            self.file_rahasia.delete(save=False)
        super().delete(*args, **kwargs)
