from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# meta data about the our API's
schema_view = get_schema_view(
   openapi.Info(
      title="Tenure Tenant API",
      default_version='v1',
      description="""
                    This Ethiopian Tenure Tenant system  API is a restful web service that provides access to various features and functionalities of the Rental agreement platform. 
                    Users can use this API to interact with their account, manage their profile area, receive notifications, upload images and files, and perform various other actions 
                    related to the tenant and tenure system. 

                    This  API offers endpoints for user authentication, notification management, post management like image and files, and more. 
                    Developers can integrate this API into their applications to enable seamless interaction with the tenure tenant system and enhance the 
                    user experience.

                    For more details and usage instructions, please refer to the API documentation available at: [API Documentation](https://www.example.com/docs/)
                  """,
      terms_of_service="""
                         https://www.example.com/terms/
                       """,
      contact=openapi.Contact(email="tsiyong8@gmail.com", name="Zion", url="http://tsiyongashaw.netlify.app/"),
      license=openapi.License(name="House_Rental_agreement License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('Rent.urls') ),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  ] +  static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
