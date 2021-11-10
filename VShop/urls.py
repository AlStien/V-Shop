from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include('rest_framework.urls')),
    path('', include('base.urls')),
    path('api/Account/', include('base.api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('seller/', include('seller_product.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
