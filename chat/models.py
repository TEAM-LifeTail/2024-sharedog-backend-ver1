from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class Promise(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=100)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="promises_as_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="promises_as_user2")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """user1과 user2가 같으면 안 됨"""
        if self.user1 == self.user2:
            raise ValidationError("두 사람은 서로 다른 사람이어야 합니다.")

    def save(self, *args, **kwargs):
        """저장 전에 clean() 검증 실행"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"예약: {self.day} {self.time} - {self.place} ({self.user1} & {self.user2})"

class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name="chat_rooms")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["id"], name="unique_chat_room"
            )  # 중복 방지
        ]

    def __str__(self):
        return f"ChatRoom {self.id} - Participants: {', '.join(user.email for user in self.participants.all())}"
    
    def get_other_participant_name(self, current_user):
        # 참가자 중 현재 사용자를 제외한 다른 참가자 가져오기
        other_participants = self.participants.exclude(id=current_user.id)
        if other_participants.exists():
            # 첫 번째 다른 참가자의 이름을 반환
            return other_participants.first().user_name  # 또는 email, 원하는 필드로 수정 가능
        return None
    
# ✅ Message 모델 (sender_email → sender를 User로 변경)
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    promise = models.ForeignKey(Promise, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

    def __str__(self):
        return f"{self.sender.email}: {self.text[:30]}"