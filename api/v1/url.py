from django.conf.urls import patterns, include, url


urlpatterns = [
    url(r'^user/?', include('api.v1.user.url')),
    url(r'^visitor/?', include('api.v1.visitor.url')),
    url(r'^appointment/?', include('api.v1.appointments.url')),
    url(r'^appointment-logs/?', include('api.v1.appointment_logs.url')),
    url(r'^department/?', include('api.v1.department.url')),
    url(r'^visitor-group/?', include('api.v1.visitor_group.url')),
    url(r'^company/?', include('api.v1.company.url')),
    url(r'^restricted-item/?', include('api.v1.restricted_item.url')),
    url(r'^messages/?', include('api.v1.messages.url')),
    url(r'^login?', include('api.v1.login.url')),
    url(r'^settings/?', include('api.v1.settings.url')),
    url(r'^_changes/?', include('api.v1.changes.url')),
    url(r'^vehicle/?', include('api.v1.vehicle.url')),
]