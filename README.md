# Django-Basics

A Django learning project with two apps: `agency_request_form` (practicing `CreateView` + `ModelForm`) and `order_management` (the main app — multiple related models, built entirely with function-based views, no shortcuts).

## Folder structure

```
Django-Basics/
├── manage.py
├── .gitignore
├── test_app/ # project settings package
│ ├── init.py
│ ├── settings.py
│ ├── urls.py # root URL config — includes each app
│ ├── asgi.py
│ └── wsgi.py
│
├── agency_request_form/ # app: learning CreateView + ModelForm
│ ├── migrations/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py # AgencyRequestForm (ModelForm)
│ ├── models.py # AgencyRequest, Developer
│ ├── views.py # AgencyCreate (CreateView), update_request, delete_request
│ └── urls.py
│
├── homepage/ # small app: lists AgencyRequest entries
│ ├── migrations/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ └── views.py # ListAgencyRequest
│
├── order_management/ # MAIN APP — multi-model relationships
│ ├── migrations/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py # Users, Orders, OrderItems + signals
│ ├── views.py # home, order_form, order_view, order_delete, order_history
│ └── urls.py
│
└── templates/ # ALL templates live here, outside every app
├── order_management/
│ ├── base.html
│ ├── home.html
│ ├── order_form.html # shared by "place order" and "update order"
│ ├── order_history.html
│ ├── order_view.html
│ └── order_confirm_delete.html
└── agency_request_form/
└── agency_request_form.html # shared by CreateView and update_request
```

## Setup

```bash
git clone https://github.com/kabilraya/Django-Basics.git
cd Django-Basics

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install django mysqlclient
```

Configure `DATABASES` in `test_app/settings.py` (MySQL by default). To use SQLite instead:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

## URL routing

### `test_app/urls.py` (root config)

This is the entry point for every request. Django reads it top to bottom and stops at the first match.

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path("agency-request/", AgencyCreate.as_view(), name="agency_create"),
    path("", ListAgencyRequest.as_view(), name="agency_request_list"),
    path("update/<int:pk>", update_request, name="update_agency"),
    path("delete/<int:pk>", delete_request, name="delete_agency"),
    path("orders/", include("order_management.urls")),
]
```

| URL | View | What it does |
|---|---|---|
| `/admin/` | Django's built-in admin | Admin panel, needs `createsuperuser` first |
| `/agency-request/` | `AgencyCreate` (CBV) | Shows the blank agency request form; on submit, creates a new `AgencyRequest` row |
| `/` | `ListAgencyRequest` (CBV) | Lists all `AgencyRequest` entries — the homepage of this part of the project |
| `/update/<pk>` | `update_request` (function) | GET shows the form pre-filled for that row's `pk`; POST saves the edited values |
| `/delete/<pk>` | `delete_request` (function) | Deletes the `AgencyRequest` row with that `pk`, then redirects back to the list |
| `/orders/...` | — | Not a view itself. `include()` hands off anything starting with `orders/` to `order_management/urls.py`, which matches the rest of the path |

### `order_management/urls.py` (included under `orders/`)

Every path here is **prefixed with `orders/`** by the `include()` line above, so `""` below actually means `/orders/`, not the site root.

```python
urlpatterns = [
    path("", views.home, name="home"),
    path("place_order/", views.order_form, name="place_order"),
    path("order_history/", views.order_history, name="order_history"),
    path("order/<int:order_id>/", views.order_view, name="order_view"),
    path("order/<int:order_id>/update/", views.order_form, name="order_update"),
    path("order/<int:order_id>/delete/", views.order_delete, name="order_delete"),
]
```

| URL | View | What it does |
|---|---|---|
| `/orders/` | `home` | Landing page with two buttons: Place an Order, View Order History |
| `/orders/place_order/` | `order_form` | GET shows a blank order form; POST creates a new `Orders` row plus one `OrderItems` row per product |
| `/orders/order_history/` | `order_history` | Lists every order, newest first, each with View / Update / Delete links |
| `/orders/order/<order_id>/` | `order_view` | Read-only detail page: order info plus every item in it |
| `/orders/order/<order_id>/update/` | `order_form` | Same view as `place_order`, but with `order_id` captured from the URL — pre-fills the form from the existing order and its items, and updates/deletes/adds items on submit instead of creating a new order |
| `/orders/order/<order_id>/delete/` | `order_delete` | GET shows a confirm page with the order's details; POST actually deletes it (cascades to its items) |

Note that `place_order` and `order_update` are two different **names**, pointing at the **same view function** (`order_form`) — the view branches on whether `order_id` was captured from the URL, which is what lets one view and one template serve both "create" and "edit" without duplicating the form logic.

## Run

```bash
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

- Order management: `http://127.0.0.1:8000/orders/`
- Agency request list: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
