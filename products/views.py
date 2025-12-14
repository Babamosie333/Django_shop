from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        """
        Start with active products, filter by category (slug)
        and search query (?q=).
        """
        qs = Product.objects.filter(is_active=True)
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            qs = qs.filter(category=category)

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(short_description__icontains=q)
                | Q(description__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        """
        Add categories and active_category to template context,
        plus current search query.
        """
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        category_slug = self.kwargs.get("category_slug")
        active_category = None
        if category_slug:
            active_category = get_object_or_404(Category, slug=category_slug)
        context["categories"] = categories
        context["active_category"] = active_category
        context["query"] = self.request.GET.get("q", "")
        return context

"""def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    active_category = None

    # search
    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        )

    # filter by category
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    # pagination: 6 per page
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": categories,
        "active_category": active_category,
        "page_obj": page_obj,
        "products": page_obj.object_list,
        "query": query,
    }
    return render(request, "products/product_list.html", context)"""


"""def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        "product": product,
        "related_products": related,
    }
    return render(request, "products/product_detail.html", context)"""

class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        """
        Add related products (same category) to context.
        """
        context = super().get_context_data(**kwargs)
        product = self.object
        related = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
        context["related_products"] = related
        return context