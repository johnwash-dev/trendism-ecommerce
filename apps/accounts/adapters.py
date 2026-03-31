import uuid
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        """
        If a user with this email already exists, connect the social account
        instead of creating a new user.
        """
        email = sociallogin.account.extra_data.get("email")

        if not email:
            return

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return

        if sociallogin.is_existing:
            return

        sociallogin.connect(request, user)

    def populate_user(self, request, sociallogin, data):
        
        user = super().populate_user(request, sociallogin, data)
        
        if not user.username:
            email = data.get("email")
            if email:
                base_username = email.split('@')[0]
                
                if User.objects.filter(username=base_username).exists():
                    user.username = f"{base_username}_{uuid.uuid4().hex[:4]}"
                else:
                    user.username = base_username
            else:
                user.username = f"user_{uuid.uuid4().hex[:8]}"
        
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        return user
