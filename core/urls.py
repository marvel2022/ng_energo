from django.urls import path, include

from .views import (
    HomeListView,
    ProductListView,
    ProductDetailView,
    ProductSearch,
    ProductsSearch,
    AboutView,
    ContactView,

    SubscriptionCreateView,
    ClientContactCreateView,
    # confirm,

    # AdminPanel,
    
    # AdminCategoryListView,
    # AdminCategoryCreateView,
    # AdminCategoryUpdateView,
    # AdminCategoryDeleteView,

    # AdminProductListView,
    # AdminProductDetailView,
    # AdminProductCreateView,
    # AdminProductUpdateView,
    # AdminProductDeleteView,
)

app_name = 'core'

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('home/<slug:slug>/', HomeListView.as_view(), name='home'),

    path('category/', ProductListView.as_view(), name='category'),
    path('category/<slug:slug>/', ProductListView.as_view(), name='category'),


    path('detail/<slug:slug>/', ProductDetailView.as_view(), name='detail'),
    path('search/', ProductSearch.as_view(), name="search_view"),
    path('search-products/', ProductsSearch.as_view(), name="p_search_view"),

    # ------------ Admin Panel ------------
    # path('admin-panel/', AdminPanel.as_view(), name='admin_panel'),

    # path('admin-category-list/', AdminCategoryListView.as_view(), name='category_list'),
    # path('admin-category-create/', AdminCategoryCreateView.as_view(), name='category_create'),
    # path('admin-category-update/<slug:slug>/', AdminCategoryUpdateView.as_view(), name='category_update'),
    # path('admin-category-delete/<slug:slug>/', AdminCategoryDeleteView.as_view(), name='category_delete'),

    
    # path('admin-product-list/', AdminProductListView.as_view(), name='product_list'),
    # path('admin-product-detail/<slug:slug>/', AdminProductDetailView.as_view(), name='product_detail'),
    # path('admin-product-list/<slug:slug>/', AdminProductListView.as_view(), name='product_list'),
    # path('admin-product-create/', AdminProductCreateView.as_view(), name='product_create'),
    # path('admin-product-update/<slug:slug>/', AdminProductUpdateView.as_view(), name='product_update'),
    # path('admin-product-delete/<slug:slug>/', AdminProductDeleteView.as_view(), name='product_delete'),

    # path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    # path('category/update/', CategoryUpdateView.as_view(), name='category-update'),
    # path('category/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    
    # ------------ Admin Panel ------------

    path('aboutus/', AboutView.as_view(), name='aboutus'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('subscription/', SubscriptionCreateView, name='subscription'),
    path('contactinfo/', ClientContactCreateView, name='contactinfo'),
    # path('confirm/', confirm, name='confirm'),

]