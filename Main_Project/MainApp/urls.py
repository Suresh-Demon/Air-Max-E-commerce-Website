from django.urls import path
from MainApp import views
from django.conf.urls.static import static
from Main_Project import settings

urlpatterns = [
   path('',views.home),
   path('footer',views.footer),
   path('product',views.product),
   path('search/',views. search_product, name='search_product'),  
   path('search/<str:name>/',views. search_product, name='search_product_by_name'),
   path('register/',views.register,name='register'),
   path('login',views.user_login,name='login'),
   path('contact',views.contact),
   path('about',views.about),
   path('logout',views.user_logout),
   path('pdetails/<pid>',views.pdetails),
   path('pcatfilter/<cv>',views.pcatfilter),
   path('sort/<sv>',views.sort),
   path('range',views.range),
   path('addtocart/<pid>',views.addtocart),
   path('viewcart',views.viewcart),
   path('updateqtyProduct/<qv>/<cid>',views.updateqtyProduct),
   path('updateqty/<qv>/<cid>',views.updateqty),
   path('remove/<cid>',views.remove),
   path('removeorder/<oid>',views.removeorder),
   path('placeorder',views.placeorder),
   path('makepayment/<oid>',views.makepayment),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)