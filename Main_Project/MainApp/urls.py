from django.urls import path
from MainApp import views
from django.conf.urls.static import static
from Main_Project import settings

urlpatterns = [
   path('nav',views.navbar),
   path('',views.home),
   path('footer',views.footer),
   path('product',views.product),
   path('register',views.register),
   path('login',views.user_login),
   path('contact',views.contact),
   path('about',views.about),
   path('logout',views.user_logout),
   path('productpagi',views.productpagi),
   path('pdetails/<pid>',views.pdetails),
   path('pcatfilter/<cv>',views.pcatfilter),
   path('sort/<sv>',views.sort),
   path('range',views.range),
   path('addtocart/<pid>',views.addtocart),
   path('viewcart',views.viewcart),
   path('updateqty/<qv>/<cid>',views.updateqty),
   path('remove/<cid>',views.remove),
   path('placeorder',views.placeorder),
   path('makepayment',views.makepayment),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)