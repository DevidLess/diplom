from django.urls import path, include
from .views import *

# from .views_.request import *
# from .views_.request_child import *
# from .views_.site import *
# from .views_.profile import *

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    # path('', CourtOrderListView.as_view(), name='home'),
    path("user_profile/", UserProfileDetailView.as_view(), name="user-profile-detail"),
    path(
        "user_profile/update/",
        UserProfileUpdateView.as_view(),
        name="user-profile-update",
    ),
    path("about/", AboutPageView.as_view(), name="about"),
    path("court-order/list/", CourtOrderListView.as_view(), name="court-order-list"),
    path(
        "court-order/detail/<int:pk>/",
        CourtOrderDetailView.as_view(),
        name="court-order-detail",
    ),
    path(
        "cancellation-request/list/",
        CancellationRequestListView.as_view(),
        name="cancellation-request-list",
    ),
    path(
        "cancellation-request/detail/<int:pk>/",
        CancellationRequestDetailView.as_view(),
        name="cancellation-request-detail",
    ),
    path(
        "cancellation-request/create/",
        CancellationRequestCreateView.as_view(),
        name="cancellation-request-create",
    ),
    path(
        "cancellation-request/create/<int:court_order_id>/",
        CancellationRequestCreateView.as_view(),
        name="cancellation-request-create-by-id",
    ),
    path(
        "cancellation-request/update/<int:pk>/",
        CancellationRequestUpdateView.as_view(),
        name="cancellation-request-update",
    ),
    path(
        "cancellation-request/delete/<int:pk>/",
        CancellationRequestDeleteView.as_view(),
        name="cancellation-request-delete",
    ),
    path(
        "docx/cancellation-request/<int:pk>/",
        docx_cancellation_request,
        name="docx-cancellation-request",
    ),
    path(
        "docx/fill-template/<int:template_pk>/<int:court_order_pk>/",
        docx_fill_template,
        name="docx-fill-template-for-court-order",
    ),
    path(
        "docx/fill-template/<int:template_pk>/",
        docx_fill_template,
        name="docx-fill-template",
    ),
    path("template/list/", TemplateListView.as_view(), name="template-list"),
    path(
        "template/detail/<int:pk>/",
        TemplateDetailView.as_view(),
        name="template-detail",
    ),
]
