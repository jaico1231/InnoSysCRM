
from django.urls import path
from shared.views.groups_view import GroupListView, GroupCreateView, GroupUpdateView, GroupDeleteView
from shared.views.menuView import ListMenuView, MenuItemCreateView, MenuItemListView, MenuUpdateView, MenuItemUpdateView, ToggleMenuEstadoView, ToggleMenuItelEstadoView#, ToggleMenuEstadoView
from shared.views.updateView import ConfirmCSVUploadView, generar_csv_modelo 
from shared.views.updateView import CargarCSVView
from shared.views.tercerosView import CargarTercerosCSVView,  TercerosListView, TercerosCreateView, TerceroUpdateView , TerceroDeleteView
from shared.views.indexView import index
from shared.views.inicialesView import DatosInicialesUpdateView, DatosInicialesView
from shared.views.usersView import PasswordChangeView, UserListView, UserCreateView, UserUpdateView, UserDelView, RenewPasswordView
from shared.views.loginView import LoginView, logout_view
from shared.views.notificaciones import get_notifications
from django.contrib.auth.decorators import login_required
from ROMIL_BETA1.urls import add_menu_name
app_name='shared'
urlpatterns=[
    path('', login_required(index.as_view()), name='index'),
    path('get_notifications/', login_required(get_notifications), name='get_notifications'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', login_required(logout_view), name='logout'),
    path('userlist/', login_required(add_menu_name('USUARIOS')(UserListView.as_view())), name='userlist'),
    path('usercreate', login_required(UserCreateView.as_view()), name='usercreate'),
    path('useredit/<int:pk>', login_required(UserUpdateView.as_view()), name='useredit'),
    path('userdel/<int:pk>', login_required(UserDelView.as_view()), name='userdel'),

    path('groupslist/', login_required(add_menu_name('GRUPOS')(GroupListView.as_view())), name='groupslist'),
    path('groupcreate', login_required(GroupCreateView.as_view()), name='groupcreate'),
    path('groupedit/<int:pk>', login_required(GroupUpdateView.as_view()), name='groupedit'),
    path('groupdel/<int:pk>', login_required(GroupDeleteView.as_view()), name='groupdel'),
    
    path('password_change/', login_required(PasswordChangeView.as_view()), name='password_change'),
    path('userpassword_change/<int:pk>', login_required(RenewPasswordView.as_view()), name='changepassword'),
    
    path('iniciales/', login_required(DatosInicialesView.as_view()), name='iniciales'),
    path('iniciales/int:pk/', login_required(DatosInicialesUpdateView.as_view()), name='inicialesUpdate'),

    path('generar_csv_modelo/<app_label>/<model_name>/', login_required(generar_csv_modelo), name='generar_csv_modelo'),
    
    #updateFiles
    path('cargar-terceros-csv/', login_required(CargarTercerosCSVView.as_view()), name='cargar_terceros_csv'),
    path('confirm_csv_upload/', login_required(ConfirmCSVUploadView.as_view()), name='confirm_csv_upload'),
    #MENU
    path('menu/', login_required(ListMenuView.as_view()), name='menu'),
    path('menu/edit/<int:pk>', login_required(MenuUpdateView.as_view()), name='editmenu'),
    path('menuitems/', login_required(MenuItemListView.as_view()), name='menuitems'),
    path('menuitems/create', login_required(MenuItemCreateView.as_view()), name='menuitemscreate'),
    path('menuitems/edit/<int:pk>', login_required(MenuItemUpdateView.as_view()), name='editmenuitem'),
    path('menu/toggle/<int:pk>', login_required(ToggleMenuEstadoView.as_view()), name='togglemenu'),
    path('menuitems/toggle/<int:pk>', login_required(ToggleMenuItelEstadoView.as_view()), name='togglemenuitem'),
    # TERCEROS
    path('terceros/', login_required(add_menu_name('TERCEROS')(TercerosListView.as_view())), name='terceros_list'),
    path('terceros/create', login_required(TercerosCreateView.as_view()), name='terceroscreate'),
    path('terceros/edit/<int:pk>', login_required(TerceroUpdateView.as_view()), name='tercerosedit'),
    path('terceros/delete/<int:pk>', login_required(TerceroDeleteView.as_view()), name='tercerosdel'),
]


