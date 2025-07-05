from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishlistViewSet, ProductViewSet, signup, login, invite_contributor, sync_user

router = DefaultRouter()
router.register(r'wishlists', WishlistViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('<int:wishlist_id>/invite/', invite_contributor, name='invite_contributor'),
    path('users/sync/', sync_user, name='sync_user'),
]
