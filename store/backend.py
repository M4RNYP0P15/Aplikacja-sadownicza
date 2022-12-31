from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
# from django.db.models.query import Q


User_Model = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password= None, **kwargs):
        try:
            user = User_Model.objects.get(Q(username_iexact=username)|Q(email_iexact=username))
        except User_Model.DoesNotExist:
            User_Model().set_password(password)
            return
        except User_Model.MultipleObjectsReturned:
            user = User_Model.objects.filter(Q(username_iexact=username) | Q(email_iexact=username)).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user