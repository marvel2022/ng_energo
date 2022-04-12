from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse, Http404, HttpResponse
from django.core import serializers
from django.db.models import Q, F, Case, When
from django.views import View
from django.forms import modelformset_factory
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import random
import json

from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView,
	DeleteView,
)

from product.models import (
	Category, 
	Product, 
	Image,
	HomeImage,
	CertificateImage,
    PartnerImage,
)

from .models import (
	ClientView,
	Subscriber,
	ClientContact,
)

from .forms import (
	CategoryForm,
	ProductForm,
	ProductImagesForm,
	HomeImage,
)
# Create your views here.


class HomeListView(ListView):
	model = Product
	template_name='index.html'
	paginate_by = 9

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['category_list'] = Category.objects.all()
		print("first - context")
		context['home_image'] = HomeImage.objects.all()
		page = 'active'
		context['index'] = page
		print(context['index'])

		# <--------- recommended product --------->
		recommended_product = sorted(Product.objects.all(), key=lambda x: x.view_count)
		if len(recommended_product) >= 4:
			context['recommended_product'] = recommended_product[-4:]
		else:
			context["recommended_product"] = recommended_product
		# <--------- recommended product --------->

		return context

	def get_queryset(self):
		queryset=super().get_queryset()
		print("first - queryset")
		try:
			slug = self.kwargs.get('slug')
			category = Category.objects.get(slug=slug)
			return queryset.filter(category=category)
		except:
			return queryset
		


class ProductListView(ListView):
	model=Product
	template_name='products.html'

	paginate_by=9

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['category_list'] = Category.objects.all()
		if self.kwargs.get('slug'):
			slug = self.kwargs.get('slug')
			category = Category.objects.get(slug=slug)
			context['current_category'] = category
		print("second - context")
		
		# active page deffiner
		page = 'active'
		context['products'] = page
		print(context['products'])
		# -------------------

		# <--------- recommended product --------->
		recommended_product = sorted(Product.objects.all(), key=lambda x: x.view_count)
		if len(recommended_product) >= 4:
			context['recommended_product'] = recommended_product[-4:]
		else:
			context["recommended_product"] = recommended_product
		# <--------- recommended product --------->

		return context

	def get_queryset(self):
		queryset = super().get_queryset()
		print("second - queryset")
		try:
			slug = self.kwargs.get('slug')
			category = Category.objects.get(slug=slug)
			return queryset.filter(category=category)
		except:
			return queryset

class ProductDetailView(DetailView):
	model = Product
	template_name = 'product-detail.html'

	slug_field     = 'slug'
	slug_url_kwarg = 'slug'

	def get_client_ip(self, request, *args, **kwargs):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		print(ip)
		return ip

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		# active page deffiner
		page = 'active'
		context['products'] = page
		print(context['products'])
		# -------------------

		# <--------- view counter by ip ---------!>
		slug=self.kwargs.get('slug')
		product=Product.objects.get(slug=slug)
		client_ip = self.get_client_ip(self.request)
		ClientView.objects.get_or_create(client_ip=client_ip, product=product)
		# <--------- view counter by ip ---------!>

		# <--------- recommended product --------->
		recommended_product = sorted(Product.objects.all(), key=lambda x: x.view_count)
		if len(recommended_product) >= 4:
			context['recommended_product'] = recommended_product[-4:]
		else:
			context["recommended_product"] = recommended_product
		# <--------- recommended product --------->

		return context



class ProductSearch(ListView):
	model=Product
	template_name='index.html'
	paginate_by=9

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['category_list'] = Category.objects.all()
		context['home_image']    = HomeImage.objects.all()

		# active page deffiner
		page = 'active'
		context['index'] = page
		print(context['index'])
		# -------------------

		# <--------- recommended product --------->
		recommended_product = sorted(Product.objects.all(), key=lambda x: x.view_count)
		if len(recommended_product) >= 4:
			context['recommended_product'] = recommended_product[-4:]
		else:
			context["recommended_product"] = recommended_product
		# <--------- recommended product --------->
		
		return context
	
	def get_queryset(self):
		qs = super().get_queryset()
		query = self.request.GET.get('q')
		return qs.filter( Q(name__icontains=query) | Q(slug__icontains=query) | Q(description__icontains=query))	


class ProductsSearch(ListView):
	model=Product
	template_name='products.html'
	paginate_by = 9

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['category_list'] = Category.objects.all()

		# active page deffiner
		page = 'active'
		context['products'] = page
		print(context['products'])
		# -------------------

		# <--------- recommended product --------->
		recommended_product = sorted(Product.objects.all(), key=lambda x: x.view_count)
		if len(recommended_product) >= 4:
			context['recommended_product'] = recommended_product[-4:]
		else:
			context["recommended_product"] = recommended_product
		# <--------- recommended product --------->
		
		return context
	
	def get_queryset(self):
		qs = super().get_queryset()
		query = self.request.GET.get('q')
		return qs.filter( Q(name__icontains=query) | Q(slug__icontains=query) | Q(description__icontains=query))





# @csrf_exempt
def SubscriptionCreateView(request):

	data = json.loads(request.body)
	email = data['email']

	done_action = {}

	try:
		validate_email(email)
	except ValidationError as e:
		print("bad email, details:", e)
		done_action['action'] = 'not_valid'
		
	else:
		print("good email")
		done_action['action'] = 'valid'
		sub, created = Subscriber.objects.get_or_create(email=email)
		if created == False:
			done_action['action'] = 'subscribed'
		else:
			message = Mail(
			from_email=settings.FROM_EMAIL,
			to_emails=sub.email,
			subject='Confirmation Email.',
			html_content='<b>Thank you for signing up for NG ENERGO news!</b>')
			sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
			response = sg.send(message)

	return JsonResponse(done_action, safe=False, status=200)

# @csrf_exempt
def ClientContactCreateView(request):

	data = json.loads(request.body)
	fullname = data['fullname']
	contactinfo = data['contactinfo']
	message = data['message']

	done_action = {}
	
	sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

	sub, created = ClientContact.objects.get_or_create(fullname=fullname, contactinfo=contactinfo, message=message)
	if created == False:
		try:
			validate_email(contactinfo)
			message = Mail(
					from_email=settings.FROM_EMAIL,
					to_emails='neftgazenergo@mail.ru',
					# to_emails='dovurovjamshid95@gmail.com',
					subject="NG ENERGO",
					html_content=(f"Ismi: {fullname}<br>Email: <a href='mailto:{contactinfo}'>{contactinfo}</a> <br><b>Xabar:</b> <br><br>{message}"))
			sg.send(message)
		except:
			message = Mail(
					from_email=settings.FROM_EMAIL,
					to_emails='neftgazenergo@mail.ru',
					# to_emails='dovurovjamshid95@gmail.com',
					subject="NG ENERGO",
					html_content=(f"Ismi: {fullname}<br>Tel: <a href='tel:{contactinfo}'>{contactinfo}</a> <br><b>Xabar:</b> <br><br>{message}"))
			sg.send(message)
		else:
			done_action['action'] = 'not_valid'

	done_action['action'] = 'done'
	return JsonResponse(done_action, safe=False, status=200)


# class AdminPanel(View):
# 	template_name='admin-panel/base.html'
# 	context={}
# 	def get(self, request, *args, **kwargs):
# 		# View count of all products
# 		self.context['view_count'] = sum(x.view_count for x in Product.objects.all())
# 		# --------------------------
# 		return render(
# 			request,
# 			self.template_name,
# 			self.context,
# 		)


# <---------- Category
# class AdminCategoryListView(ListView):
# 	model=Category
# 	template_name='admin-panel/category-list.html'
	
# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		# View count of all products
# 		context['view_count'] = sum(x.view_count for x in Product.objects.all())
# 		# --------------------------
# 		return context

# class AdminCategoryCreateView(CreateView):
# 	model=Category
# 	template_name='admin-panel/category-create.html'
# 	form_class=CategoryForm

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		# View count of all products
# 		context['view_count'] = sum(x.view_count for x in Product.objects.all())
# 		# --------------------------
# 		return context

# 	def get_success_url(self):
# 		view_name = 'core:category_list'
# 		return reverse(view_name)

# class AdminCategoryUpdateView(UpdateView):
# 	model=Category
# 	template_name='admin-panel/category.html'
# 	form_class=CategoryForm
# 	slug_field = 'slug'
# 	slug_url_kwarg = 'slug'

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		# View count of all products
# 		context['view_count'] = sum(x.view_count for x in Product.objects.all())
# 		# --------------------------
# 		return context

# 	def get_success_url(self):
# 		view_name = 'core:category_list'
# 		return reverse(view_name)

# class AdminCategoryDeleteView(DeleteView):
# 	model=Category
# 	template_name='admin-panel/category-delete.html'
# 	slug_field = 'slug'
# 	slug_url_kwarg = 'slug'

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		# View count of all products
# 		context['view_count'] = sum(x.view_count for x in Product.objects.all())
# 		# --------------------------
# 		return context

# 	def get_success_url(self):
# 		view_name="core:category_list"
# 		return reverse(view_name)
# <---------- End Category


# <---------- Product
# class AdminProductListView(ListView):
# 	model=Product
# 	template_name='admin-panel/product-list.html'

# 	paginate_by=9

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context['category_list'] = Category.objects.all()
# 		# View count of all products
# 		context['view_count'] = sum(x.view_count for x in Product.objects.all())
# 		# --------------------------
# 		return context

# 	def get_queryset(self):
# 		queryset = super().get_queryset()
# 		try:
# 			slug = self.kwargs.get('slug')
# 			category = Category.objects.get(slug=slug)
# 			return queryset.filter(category=category)
# 		except:
# 			return queryset

# class AdminProductDetailView(DetailView):
# 	template_name='admin-panel/product-detail.html'
# 	model = Product

# 	slug_field = 'slug'
# 	slug_url_kwarg = 'slug'


# class AdminProductCreateView(View):
# 	template_name='admin-panel/product-create.html'
# 	context={}

# 	def get(self, request, *args, **kwargs):
# 		ImageFormSet = modelformset_factory(Image, form=ProductImagesForm, extra=3)
# 		productForm = ProductForm()
# 		formset = ImageFormSet(queryset=Image.objects.none())
# 		self.context['productForm'] = productForm
# 		self.context['imageForm'] = formset
# 		# View count of all products
# 		self.context['view_count'] = sum(x.view_count for x in Product.objects.all())
#   		# --------------------------
# 		return render(request, self.template_name, self.context)

# 	def post(self, request, *args, **kwargs):
# 		# View count of all products
# 		self.context['view_count'] = sum(x.view_count for x in Product.objects.all())
# 		# --------------------------
# 		ImageFormSet = modelformset_factory(Image, form=ProductImagesForm, extra=3)
# 		if request.method == 'POST':
# 			productForm = ProductForm(request.POST)
# 			imageForm   = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
# 			if productForm.is_valid() and imageForm.is_valid():
# 				product_form = productForm.save(commit=False)
# 				product_form.published_at = timezone.now()
# 				product_form.save()

# 				for form in imageForm.cleaned_data:
# 					image   = form['image']
# 					caption = form['caption']
# 					images = Image.objects.create(product=product_form, image=image, caption=caption) 
# 					images.save()
# 				return reverse('core:product_detail', kwargs={"slug": product_form.slug})
# 		else:
# 			productForm = ProductForm()
# 			formset = ImageFormSet(queryset=Image.objects.none())
# 			self.context['productForm'] = productForm
# 			self.context['imageForm'] = formset
# 		return render(request, self.template_name, self.context)



# class AdminProductUpdateView(View):
# 	template_name='admin-panel/product-create.html'
# 	context={}

# 	def get(self, request, slug, *args, **kwargs):
# 		obj = Product.objects.get(slug=slug)
# 		ImageFormSet = modelformset_factory(Image, form=ProductImagesForm, extra=3)
# 		productForm = ProductForm(instance=obj)
# 		formset = ImageFormSet(queryset=Image.objects.none())
# 		self.context['productForm'] = productForm
# 		self.context['imageForm'] = formset
# 		self.context['slug'] = slug
# 		# View count of all products
# 		self.context['view_count'] = sum(x.view_count for x in Product.objects.all())
#   		# --------------------------
# 		return render(request, self.template_name, self.context)

# 	def post(self, request, slug, *args, **kwargs):
# 		obj = Product.objects.get(slug=slug)
# 		self.context['slug'] = slug
# 		# View count of all products
# 		self.context['view_count'] = sum(x.view_count for x in Product.objects.all())
# 		# --------------------------
# 		ImageFormSet = modelformset_factory(Image, form=ProductImagesForm, extra=3)
# 		if request.method == 'POST':
# 			productForm = ProductForm(request.POST, instance=obj)
# 			imageForm   = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
# 			if productForm.is_valid() and imageForm.is_valid():
# 				product_form = productForm.save(commit=False)
# 				product_form.published_at = timezone.now()
# 				product_form.save()

# 				for form in imageForm.cleaned_data:
# 					image   = form['image']
# 					caption = form['caption']
# 					images = Image.objects.create(product=product_form, image=image, caption=caption) 
# 					images.save()
# 				return reverse('core:product_detail', kwargs={"slug": product_form.slug})
# 		else:
# 			productForm = ProductForm(instance=obj)
# 			formset = ImageFormSet(queryset=Image.objects.none())
# 			self.context['productForm'] = productForm
# 			self.context['imageForm'] = formset
# 		return render(request, self.template_name, self.context)


# class AdminProductDeleteView(DeleteView):
# 	model=Product
# 	template_name="admin-panel/product-delete.html"

# 	slug_field='slug'
# 	slug_url_kwarg='slug'

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		# View count of all products
# 		context['view_count'] = sum(x.view_count for x in Product.objects.all())
# 		# --------------------------
# 		return context

# 	def get_success_url(self):
# 		view_name="core:product_list"
# 		return reverse(view_name)


# <---------- End Product


class AboutView(View):
	template_name = 'aboutus.html'
	context={}
	def get(self, request, *args, **kwargs):
		# active page deffiner
		page = 'active'
		self.context['aboutus'] = page
		# -------------------
		self.context['cartificate_images'] = CertificateImage.objects.all()
		self.context['partner_images'] = PartnerImage.objects.all()
		return render(
			request,
			self.template_name, 
			self.context,
		)

class ContactView(View):
	template_name = 'contact.html'
	context={}
	def get(self, request, *args, **kwargs):
		# active page deffiner
		page = 'active'
		self.context['contact'] = page
		# -------------------
		return render(
			request,
			self.template_name, 
			self.context,
		)




from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
class LazyEncoder(DjangoJSONEncoder):
	def default(self, obj):
		if isinstance(obj, Decimal):
			return str(obj)
		return super().default(obj)

def search_query(request, *args, **kwargs):
	query = ''
	images_url = {}

	# data = json.loads(request.body)
	# query = data['query']
	query = request.GET.get('query')
	print(query)

	object_list = None
	if (len(query) > 0) and (query != "" or query != " "):
		print("length: ", len(query))
		object_list = Product.objects.filter(
			Q(name__icontains=query) | Q(slug__icontains=query) | Q(short_info__icontains=query) | Q(description__icontains=query) 
		)
	if object_list.count() > 0:
		for obj in object_list:
			if obj.imageURL:
				images_url[obj.pk] = obj.imageURL
		print(images_url)
		try:
			object_list_json = serializers.serialize('json', object_list, cls=LazyEncoder, ensure_ascii=True)
			# images_url_json =  json.dumps([images_url,])#serializers.serialize('json', [images_url, ])
		except Exception as e:
			print("Error occured: ", e)
		return JsonResponse({"instance":object_list_json, "images_url":images_url}, safe=False, status=200)
	else:
		object_list_json = "nothing"
		return JsonResponse(object_list_json, safe=False, status=200)
	return Http404