# Kanban Desk
A web application that functions as a personal management tool for creating projects and managing tasks. - 05/2023

Operating System: macOS Ventura 13.2.1
PostgreSQL: postgres (PostgreSQL) 15.2
pgAdmin 4: v7.1

### pip freeze:
asgiref==3.6.0
Django==4.2.1
django-appconf==1.0.5
django-compressor==4.3.1
django-libsass==0.9
libsass==0.22.0
psycopg2==2.9.6
python-dotenv==1.0.0
rcssmin==1.1.1
rjsmin==1.2.1
sqlparse==0.4.4

### Week 01
## Create a Django project and connect to PostgreSQL
Reference article: https://medium.com/@9cv9official/creating-a-django-web-application-with-a-postgresql-database-on-windows-c1eea38fe294

### Troubleshooting - python and pip commands were not working as expected
Issue: After creating the virtual environment, Django should not automatically be installed. But when I checked the Django version it was returning a version number. 

Fix: `alias python` and `which python` were showing `python: aliased to /usr/bin/python3`
This means that the Python command was aliased to `/usr/bin/python3`, which is the system Python installation. This means that if I installed packages using the `python` command, I would be installing them to the system Python installation and not the virtual environment.

1. `unalias python` and `unalias pip` to remove the aliases
2. `alias` to make sure the alias is removed
3. While in the virtual enviroment, `which python` now points the correct venv/bin/
4. `python -m django --version` not correctly says `No module named django`

### Set up a virtual environment
1. Make sure python is installed - `python --version`
2. Create a virtual environment - `python -m venv venv`
3. Activate virtual environment - `source venv/bin/activate`

### Create a Django project and run server
1. Install Django - `pip install django`
2. Check Django version - `django-admin version` or `python -m django --version`
3. Create a django project named config - `django-admin startproject config .`
4. Run server - `python manage.py runserver`

#### Note
`You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions. Run 'python manage.py migrate' to apply them.`
1. This is a normal message when first creating a django project. Run `python manage.py migrate` to update the database schema.

### Next, install PostgreSQL and pgAdmin
PostgreSQL is the relational database management system (RDBMS) that runs in the background to manage the retrieval of data from your PostgreSQL database.

PgAdmin is a client tool used to manage PostgreSQL databases, where you can create and modify databases, tables, views, and more through a graphical interface. It also allows you to run SQL queries, create backups, and manage server connections.

### Install PostgreSQL
1a. Install PostgreSQL from https://www.postgresql.org/download/macosx/

Issue: `psql` is included with the download but was returning `zsh: command not found: psql`

Fix: I needed to add the path to psql in `/Library` to my `$PATH` environment variable and update my 
`.bash_profile` file

1b. Find where `psql` is located using `sudo find / -name psql`
2b. Edit the `.bash_profile` file - `sudo nano ~/.bash_profile`
3b. Add `export PATH="/Library/PostgreSQL/15/bin:$PATH"`
4b. reload `.bash_profile` in my terminal using `source ~/.bash_profile`
5b. `which psql` now shows `/Library/PostgreSQL/15/bin/psql`

Issue: `psql` asks for passqord from the current user.

Fix: "you're not providing a username in the command so it's using your current username that you're logged in as which doesn't have permission"
https://stackoverflow.com/questions/31125740/postgresql-keeps-prompting-for-a-password-i-never-gave-in-powershell

2a. When I installed PostgreSQL from postgresql.org I created a superuser called `postgres`
3a. Run `psql -U postgres` and enter the password. If you forgot the password, you need to reinstall PostgreSQL.
4a. `\q` to quit

### Install pgAdmin
https://www.pgadmin.org/

### Install psycopg2
https://www.psycopg.org/install/
Psycopg acts as the PostgreSQL database adapter for Django, enabling Django to communicate with the PostgreSQL database. Without it, I cannot run migrations.

#### Django 4.2 release notes
Psycopg 3 support
Django now supports psycopg version 3.1.8 or higher. 

`psycopg2` has prerequisites `python3-dev libpq-dev`. 
I tried to install `psycopg2` but got `Error: pg_config executable not found.`
I know `pg_config` is installed because `sudo find / -name pg_config` shows the location in `/Library` but `which pg_config` is empty. I needed to run `source ~/.bash_profile` to reload `.bash_profile`. I should've restarted the Terminal beforehand.

1. `pip install psycopg2` now works

### Set up environment variables
Environment variables are needed to keep sensitive information from public repositories.

1. Run `pip install python-dotenv`
2. Create `.env` file and add needed variables
3. In `settings.py`, add
```
import os
from dotenv import load_dotenv

load_dotenv()
```
4. Use `os.environ.get('DB_PORT')` to retrieve the variable

### Create a superuser
1. `python manage.py createsuperuser`

### One way to check if PostgreSQL is running
1. `ps auxwww | grep postgres`

### Test connection to PostgreSQL data table
1. After updating  `DATABASES = { ... }` run server
```
DATABASES = {
  ‘default’: {
    ‘ENGINE’: ‘django.db.backends.postgresql_psycopg2’,
    ‘NAME’: ‘yourproject’,
    ‘USER’: ‘yourprojectuser’,
    ‘PASSWORD’: ‘password’,
    ‘HOST’: ‘localhost’,
    ‘PORT’: ‘’,
  }
}
```

## Set up Authentication
Reference article: https://learndjango.com/tutorials/django-login-and-logout-tutorial
Now that Django is connected to PostgreSQL, let's set up authentication. Django has a built-in `auth` app and it's included as an installed app when you create an empty Django project. 
```
INSTALLED_APPS = [
    ...
    "django.contrib.auth",  
    ...
]
```
### Create a root URL pattern that directs to auth's built-in URL Patterns 
Think of the project's `urls.py` file as the root that delegates URL requests to branch `urls.py` files from other applications.

The `include()` function within the `urls.py` files allows you to include the URLs defined by another  `urls.py` file, usually from another app.
```
urlpatterns = [
    ...
    path('auth/', include('django.contrib.auth.urls')),
]
```
The code above means to include the URL patterns in the `auth` app under the `/auth/` URL prefix.

When a user makes a request to a Django web application, the request is passed to the Django URL resolver, which examines the URL and tries to match it with a pattern defined in the `urls.py` file in the root project folder. It can either call the associated view function while also passing the HTTP request as an argument, or it might need to direct to another `urls.py` from another app. If no match is found, Django returns a 404 error.

### The built-in URLs provided by Django's auth app:
`auth/login/`: Displays the login form and handles authentication.
`auth/logout/`: Logs the user out and redirects them to the login page.
`auth/password_change/`: Displays the form to change the user's password.
`auth/password_change/done/`: Displays a message that the password was changed successfully.
`auth/password_reset/`: Displays the form to reset the user's password.
`auth/password_reset/done/`: Displays a message that an email has been sent with instructions to reset the password.
`auth/reset/<uidb64>/<token>/`: Displays the form to create a new password after a successful password reset request.
`auth/reset/done/`: Displays a message that the password was reset successfully.

### Django's default location for `auth` templates
By default, Django looks for the `auth` HTML templates in `/templates/registration`.
1. Create the folder directories - `mkdir templates/registration`
2. Create a `templates/registration/login.html` file
```
<!-- templates/registration/login.html -->
<h2>Log In</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Log In</button>
</form>
```
### But how do we know that `auth/login/` which calls the `LoginView` returns a template specifically named `login.html`? 
If we go to the Django GitHub repo, we can check out the `auth` app and all of its files.
On line 72, it says `template_name = "registration/login.html"` confirming the name of the template that will be rendered. If the `login.html` file is found, it will be used as the template to render the response.
https://github.com/django/django/blob/main/django/contrib/auth/views.py#L72

### Tell Django to look for a templates folder at the project level
```
# django_project/settings.py
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / "templates"],
        ...
    },
]
```
### Specify where to redirect the user upon a successful login
```
# django_project/settings.py
LOGIN_REDIRECT_URL = "/"
```
### Test login
1. Go to `http://localhost:8000/auth/login/` and test sign in
2. On success, it should redirect to `/`

## Create the Home page
1. The `base.html` template
```
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{% block title %}Django Auth Tutorial{% endblock %}</title>
</head>
<body>
  <main>
    {% block content %}
    {% endblock %}
  </main>
</body>
</html>
```
2. Create the `home.html` template
```
<!-- templates/home.html -->
{% extends 'base.html' %}

{% block title %}Home{% endblock %}

{% block content %}
{% if user.is_authenticated %}
  Hi {{ user.username }}!
{% else %}
  <p>You are not logged in</p>
  <a href="{% url 'login' %}">Log In</a>
{% endif %}
{% endblock %}
```
## Context Processors
How does `home.html` have access to the `user` object?
`Context processors`are Python functions that are used to add data to templates globally as long as you add them to `TEMPLATES` in `settings.py`.

1. Add the `context processors` to the `TEMPLATES` in `settings.py`. Some `context processors` are added to Django projects by default.
2. When a request is made, Django calls the `context processors` in the `TEMPLATES` list and adds their data to the template `context` variable which is a dictionary-like object for each request.
3. Then Django renders the template

Django provides several built-in context processors like the `contrib.auth.context_processors.auth` context processor, which adds the `user` and `perms` variables to the context. You can also write your own custom context processors to add additional variables to the context.

### Built-in template context processors
https://docs.djangoproject.com/en/4.2/ref/templates/api/#built-in-template-context-processors
https://github.com/django/django/blob/main/django/contrib/auth/context_processors.py#L49
4. The `contrib.auth.context_processors.auth context processor`: 
```
def auth(request):
    """
    Return context variables required by apps that use Django's authentication
    system.

    If there is no 'user' attribute in the request, use AnonymousUser (from
    django.contrib.auth).
    """wer
    if hasattr(request, "user"):
        user = request.user
    else:
        from django.contrib.auth.models import AnonymousUser

        user = AnonymousUser()

    return {
        "user": user,
        "perms": PermWrapper(user),
    }
```
## What is the `{% url 'login' %}` template tag?
`{% url 'login' %}` is a Django template tag to generate a URL that points to the login page. When you use this template tag, Django will search for the first URL pattern that has a name attribute equal to `'login'`, and will generate a URL that matches that pattern. 

The built-in `auth` app has a URL pattern with the name `name="login"` that maps the `LoginView`
https://github.com/django/django/blob/main/django/contrib/auth/urls.py#L10
```
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),

```
3. Update `login.html` to extend `base.html`
```
<!-- templates/registration/login.html -->
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<h2>Log In</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Log In</button>
</form>
{% endblock %}
```
## Cross-Site Request Forgery (CSRF) attack
This is a big topic. A `Cross-Site Request Forgery (CSRF)` attack is when a malicious website or application tries to trick a user's browser into making unauthorized HTTP requests to a different website or application.

### First, what is the sessionid cookie?
When a user authenticates with a Django website, the server generates a unique session ID and stores it on the server. The server then sends this session ID back to the user's browser as a `sessionid` cookie. The browser stores this cookie and sends it back to the server with every subsequent request, allowing the server to identify the user's session and retrieve the session data.

When a user makes an HTTP request to a Django application that requires authentication, the session ID cookie will be automatically included in the HTTP request headers.

### Secondly, What is the csrf token?
When Django renders a form, it automatically includes a hidden input field called `csrfmiddlewaretoken` that contains the CSRF token. This CSRF token is unique for each session, so each user has their own token.

The `csrfmiddlewaretoken` field is automatically included in all forms created using Django's built-in form handling utilities, such as the `forms.Form` or `forms.ModelForm` classes. It's also included in the HTML generated by Django's template engine when you use the `{{ csrf_token }}` template tag.

When a user submits a form that includes the `csrfmiddlewaretoken` field, Django checks that the token in the form data matches the token associated with the user's session. If the tokens don't match, Django raises a `Forbidden (403)` exception.

### What is the difference between sessionid cookie and csrf token?
The `sessionid` cookie is used to identify a user's session, while the `CSRF token` is used to protect against CSRF attacks with POST requests.

### Do all POST requests to Django require a sessionid and a csrf token?
By default, all POST requests to Django require a `CSRF token` to protect against CSRF attacks. However, the `sessionid` cookie is not required for every POST request. The `sessionid` cookie is only required if the user is authenticated and the view being accessed requires session data.

4. Add a URL pattern for the home page
```
from django.views.generic.base import TemplateView # new

urlpatterns = [
    ...
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # new
]
```
5. `TemplateView` is a generic view from Django
https://github.com/django/django/blob/main/django/views/generic/base.py#L220
```
class TemplateView(TemplateResponseMixin, ContextMixin, View):
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
```
6. Test logging in and logout using `http://localhost:8000/auth/logout/` or `http://localhost:8000/admin` and clikc Logout

## Logout Link
From reference: "if you think about it, we don't need to display anything on logout so there's no need for a template. All really we do after a successful "logout" request is redirect to another page"

### Add this code to `home.html` and `settings.py`
```
{% if user.is_authenticated %}
  Hi {{ user.username }}!
  <p><a href="{% url 'logout' %}">Log Out</a></p>
{% else %}
```
### Add `LOGOUT_REDIRECT_URL` to `settings.py`
1. Add `LOGOUT_REDIRECT_URL = "/"  # new`
2. We can replace `"/"` with `home` at the bottom of the `settings.py` file. Remember that the URL pattern `""` was assigned `name="home"` due to `path("", TemplateView.as_view(template_name="home.html"), name="home"),`
```
# django_project/settings.py
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
```

### Test Login and Logout
Congratulations! Login and Logout is that easy using Django.
The Django auth app provided us with built-in url and views for login and logout. All we needed to do was add a template for login. 

## Accounts App
Reference article: https://learndjango.com/tutorials/django-signup-tutorial
The next step is to create a Sign Up page. Since we're making our own view and url for registration, we need to create a dedicated app. Let's call it `accounts`.

1. Create a new app - `python manage.py startapp accounts`
2. Add to `INSTALLED_APPS`
3. Add a project-level URL for the `accounts` app - `path("accounts/", include("accounts.urls")),`

https://docs.djangoproject.com/en/4.2/ref/urls/#include
```
include(module, namespace=None)
namespace (str) – Instance namespace for the URL entries being included
```

The syntax of `include()` is `include(module, namespace=None)`, where `module` is the path to the module containing the URL patterns to include, and `namespace` is an optional string used to namespace the included URL patterns.

`module`
When you include an app's urls.py file like include("accounts.urls"), Django looks for the urls.py file inside the accounts app directory.

`namespace`
A `namespace` is basically giving a name to a specifc app's `urls.py` or `URL pattern`. So if you have `path('blog/', include('blog.urls', namespace='blog')),` then you can refer to the blog app's URL patterns like this `{% url 'blog:post_detail' post.slug %}`. `Namespaces` are useful when you have multiple apps that have their own URL patterns, and you want to differentiate them by namespace so that you can refer to them easily in your templates or code.

4. Create an app-level `urls.py` file for `accounts` app - `path("signup/", SignUpView.as_view(), name="signup"),`

In Django, the `reverse()` function and the `{% url %}` template tag serve a similar purpose, which is to create a URL for a given view.For example, `reverse('myapp:view-name')` would return the URL for the view with the name view-name in the myapp app. or example, `{% url 'myapp:view-name' %}` would output the URL for the view with the name view-name in the myapp app.

5. Create the view
```
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
```
 `success_url` is an attribute that can be set in a view to specify the URL to redirect to after a successful form submission or a successful view execution.

### Why use reverse_lazy() instead of reverse()?
Class-based views, unlike function views, need to be imported before you can resolve a URL. 

When a Django server starts, it stores URL patterns, their mappings to corresponding views, and Function-based views into memory. Therefore, the URLs for function-based views can be resolved immediately. On the other hand, class-based views are not loaded into memory until they are requested. This means that the URLs for class-based views cannot be resolved until the corresponding class-based view has been imported. That's why we use `reverse_lazy` instead of `reverse` for the `success_url` attribute in class-based views. 

If you try to use `reverse()` instead of `reverse_lazy()` for the success_url attribute in a class-based view, you will likely get an `import error`.

6. Create a new template `templates/registration/signup.html`
```
<!-- templates/registration/signup.html -->
{% extends "base.html" %}

{% block title %}Sign Up{% endblock %}

{% block content %}
  <h2>Sign up</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Sign Up</button>
  </form>
{% endblock %}
```
7. Test creating a user from `/accounts/signup`
The password needs to be complicated.

## Delete Account
Now, I need to allow a user to delete their own account.

### Custom DeleteView
1. `views.py`
```
@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('home')
    else:
        return render(request, 'delete_user.html')
```
2. `template`  
```
<h1>Delete Account</h1>
<p>Are you sure you want to delete your account? This cannot be undone.</p>
<form method="POST" action="{% url 'delete_account' %}">
  {% csrf_token %}
  <input type="submit" value="Delete">
</form>
```
3. `urls.py` with `path('delete/', delete_user, name='delete_account'),`

This works, but I want to use the built-in `DeleteView` instead.

### Built-in DeleteView by Django
Reference book: Django For Beginners by William S. Vincent

https://github.com/django/django/blob/main/django/views/generic/edit.py#LL268C1-L274C45
```
class BaseDeleteView(DeletionMixin, FormMixin, BaseDetailView):
    """
    Base view for deleting an object.

    Using this base class requires subclassing to provide a response mixin.
    """

    form_class = Form

    def post(self, request, *args, **kwargs):
        # Set self.object before the usual form processing flow.
        # Inlined because having DeletionMixin as the first base, for
        # get_success_url(), makes leveraging super() with ProcessFormView
        # overly complex.
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class DeleteView(SingleObjectTemplateResponseMixin, BaseDeleteView):
    """
    View for deleting an object retrieved with self.get_object(), with a
    response rendered by a template.
    """

    template_name_suffix = "_confirm_delete"
```
1. In `templates/home.html` add `<p><a href="{% url 'user_delete' user.pk %}">Delete Account</a></p>`
I'm redirecting to the `'user/<int:pk>/delete'` URL pattern and passing `user.pk` to the URL pattern and the corresponding view.

The order I'm going to do is `template, view, URL`.

2. Create the `user_delete.html` template
```
<!-- templates/user_delete.html -->
<h1>Delete Account</h1>
<form method="POST" action="">
  {% csrf_token %}
  <p>Are you sure you want to delete your account "{{ user.username }}"?</p>
  <input type="submit" value="Confirm">
</form>
```
`value="confirm"`
If the value attribute of the submit button is not set to `"Confirm"`, the view will assume that the user has canceled the delete operation and will simply redirect back to the `success_url`.
3. Create the `view`
```
class UserDeleteView(generic.edit.DeleteView):
    model = User
    success_url = reverse_lazy('home')
    template_name = 'user_delete.html'
```
4. In `accounts` URL patterns add `path('user/<int:pk>/delete', UserDeleteView.as_view(), name='user_delete'),`
5. Test deleting a user

### Deleting a user using a functional view instead
I could also delete a user without forcing the user to view a confirm template and clicking submit with value="Confirm". 

1. `urls.py` add `path('delete_user/', views.delete_user_view, name='delete_user'),`
2. `functional view` - On POST request delete user, else render html template
```
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def delete_user_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('home')
    else:
        return render(request, 'delete_user.html')
```
3. `template`
```
<form method="POST" action="{% url 'delete_user' %}">
    {% csrf_token %}
    <button type="submit">Delete My Account</button>
</form>
```

## Install SCSS
Now that the initial setup for `account` app is done. Let's install SCSS. I prefer to use SCSS because: 
1. The nesting structure using the brackets `{}`
2. `CSS Variables`

Reference sites: https://django-compressor.readthedocs.io/en/stable/quickstart.html#installation
https://pypi.org/project/django-libsass/

1. Make sure `pip` and `python` path is correct using `which` command
2. `pip install django_compressor django-libsass`

### Update Static variables in settings.py
3. Make sure `STATIC_ROOT` and `STATIC_URL` is correct
```
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'
```

### For django_compressor
3. Add `compressor` to `INSTALLED_APPS`
4. Update `STATIC_FINDERS`
```
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
```
### For django-libsass
5. Add `django_libsass.SassCompiler` to your `COMPRESS_PRECOMPILERS` setting
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

### Use the content type text/x-scss on your stylesheets, and have them compiled seamlessly into CSS
6. In `login_base.html` add
```
<head>
  {% load static %}
  {% load compress %}

  {% compress css %}
      <link rel="stylesheet" type="text/x-scss" href="{% static 'scss/_login.scss' %}" />
  {% endcompress %}
  <meta charset="utf-8">
  <title>{% block title %}Django Auth Tutorial{% endblock %}</title>
</head>
```
### Error: source_comments must be bool, not 'True'
7. In order for SCSS to work, I needed to wrap `os.environ.get('DEBUG')` with `bool()`.

### STATIC_ROOT
`STATIC_ROOT` is a setting in Django that defines the root directory where the `collectstatic` command should collect all the static files and then stores the files in that directory.

So I can actually recursively delete the `static` folder in the root directory, run `collectstatic` and Django will recreate the `static` folder at the root directory.

### STATIC_URL
`STATIC_URL` is the base URL for serving static files. It specifies the URL prefix that should be added to the URLs generated by the `{% static %}` template tag. For example, if you set `STATIC_URL = '/static/'`, then the `{% static 'file.png' %}` tag would generate a URL like `/static/file.png`.

When a web browser requests a static file, the web server serving your Django application will use the STATIC_URL to construct the URL that the browser should use to fetch the file from the server.

### python manage.py collectstatic
By default, `collectstatic` checks the static subdirectory of each installed app, as well as any other directories specified in `STATICFILES_DIRS`. 

## Add global SCSS variables
It will speed up development if I create some global variables and global classes throughout the application.

1. Create a folder location for global variables
I chose to put the `variables.scss` files in the project folder which is named `config`. The path is `config/static/sccs/variables.scss`
2. Import variables
In the `accounts` app's `scss` file, import the variables using `@import "../../../static/scss/variables.scss";` path
3. Create the classes
```
.primary-white {
  color: $primary-white-color;
}
```

## Add Authentication check 
I know I can add an authentication check in the `base.html` (my last workplace used that approach) template but theres a more efficient way I can go about this. I can create a `middleware` that checks if the `user.is_authenticated` and `redirect('login')`. 

This is more efficient because `middleware` can modify requests before passing them to the `view` and from the `view` to the `template`. Performing the authentication check during the HTTP request is more efficient than checking after the template has already rendered and redirecting then.

## take a break...

1. Create the `middleware.py` file. I choose to add it to the `config` folder.
2. Place the `'config.middleware.AuthMiddleware'` right after the `'django.contrib.auth.middleware.AuthenticationMiddleware'`. I had to do this because the `AuthMiddleware` was giving a `user does not exist error`. I realized it was because the built-in `auth` middleware is what creates the user object and also passes it to the context variable for all the templates.
```
class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.
        if not request.user.is_authenticated and request.path != reverse('login'):
            return redirect('login')
        response = self.get_response(request)
        # Code to be executed for each request/response after the view is called.
        return response
```
## response = self.get_response(request)
https://docs.djangoproject.com/en/4.2/topics/http/middleware/#writing-your-own-middleware
The order of the the HTTP request goes someting like this:
`client > incoming request > middleware(in order) > view > middleware(reverse order) > outgoing response > client`

The `response = self.get_response(request)` took some research for me to understand. Each middleware's `__init__` method runs once when the Django server runs. When an incoming request comes in, the `__call__` method is called for each middleware in the correct order. All the code before `response = self.get_response(request)` runs and sends the response to the next middleware or the view. Whichever is next in line. The code halts at that point for that middleware. Then, after the view returns the outgoing response, from reverse order, the middlewares run the code after `response = self.get_response(request)` and their `__call__` method completes. 

I'm assuming that the `__call__` method is only called once per client request/response for each middleware, and it just waits for the view's outgoing response after it calls `response = self.get_response(request)` and then resumes. Essentially, the `__call__` method for each middleware has 3 parts: the code that runs during the incoming request,`response = self.get_response(request)`, then the code that runs during the outgoing response.

The `@login_required` decorator before every view function is also an option. But I wanted the user authentication to occur globally.

Reference article: https://stackoverflow.com/questions/64471090/redirect-to-login-page-with-middleware-is-causing-too-many-redirects-issue
```
Just think about it for a second. 1, 2, 3. No? Ok, you send the person that is not authenticated to the login page. When he gets there, he is not authenticated, so you send him to the login page. When he gets there, he is not authententicated, so you send him to the login page. 
```
`request.path != reverse('login')`

## How to call a URL pattern by the app's namespace using the url template tag
1. Add the `namespace` to `include()`
2. From the app's `urls.py` file, set the `app_name = 'accounts'`
3. Example of using `url template tag`
```
<a class="k-btn teal-flat-btn full-width" href="{% url 'accounts:signup' %}">Create Account</a>
```

## TEMPLATES 01
## Create the the Signup Page template and Login Page template
Note: There were a few things I noticed I needed to add to these pages 
1. Add `autofocus` to the first field of every form
2. Redirect to `home` on successful `signup` or `login` - `success_url = reverse_lazy("home")`
3. I needed to stop the `AutoMiddleware` from redirecting `admin` to `auth/login`.
```
def __call__(self, request):
    # Code to be executed for each request before the view (and later middleware) are called.
    if not request.user.is_authenticated and not request.path.startswith('/admin/') and request.path not in self.protected_paths:
        return redirect('login')
    response = self.get_response(request)
    # Code to be executed for each request/response after the view is called.
    return response
```
I noticed I had to use `self` in order to access the `protected_paths` variable. This made me realize `AutoMiddleware` is not a static class. 

`ME`
so django middleware are not static classes they need to be instantiated

`ChatGPT`
Yes, Django middleware classes are not static classes. They need to be instantiated because each middleware class instance can have its own state and behavior. When Django processes a request, it creates an instance of each middleware class defined in the MIDDLEWARE setting and invokes the __call__ method of each instance in the order specified.

### Redirect authenticated users to conditional view
After a successful login:
Custom AutheMiddleware redirects (most) requests to the `'login'` URL pattern. But once the user signs in, the `success_url` redirects to the `'home'` URL pattern. The home URL pattern then has a `redirect_view`. If the current user has any `projects` that exists, redirect to `'project:view'` else `'project:create'`.

## TEMPLATES 02
## Create the Nav template and General Sidebar template
I decided to add the navbar and sidebar in the `base.html`. 

### Add Logout functionality
1. I was able to easily set up `logout` adding `href="{% url 'logout' %}` to an `a element`.
2. Next, I set up `LOGOUT_REDIRECT_URL = "home"` to redirect the user to the `'home'` URL pattern.

### Set up the active and inactive nav items
Conditionally add the `active-item` class to the nav items that represent the current URL.

### HttpRequest.resolver_match
https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.resolver_match
An instance of `ResolverMatch` representing the `resolved URL`. This attribute is only set after URL resolving took place, which means it’s available in all views but not in middleware ...

1. Use `resolver_match` compare the resolved URL to a URL pattern name to conditionally add `active-item` class
```
<li class="{% if request.resolver_match.view_name == 'accounts:settings' %}active-item{% endif %}">
```
or
```
<li class="{% if '/project/' in request.path %}active-item{% endif %}">
```
## How to add variables to the context dictionary when using class-based views
The ContextMixin class is part of the django.views.generic.base module. It is a base class for many generic views, including TemplateView, ListView, DetailView, etc. The get_context_data method is defined in the ContextMixin class.

As you can see, the get_context_data method simply returns the kwargs dictionary, which represents the context data. It also adds the view key to the dictionary with the value being the current view instance.

Yes, super() is a built-in Python function that returns a temporary object of the superclass, allowing you to call its methods. In the context of Django views, super() is typically used to call the get_context_data method of the parent class.

def UserSettingsView(request):
    my_variable = 'my_value'
    context = {
        'my_variable': my_variable,
    }
    return render(request, 'user_settings.html', context)

class UserSettingsView(TemplateView):
    template_name = 'user_settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_variable'] = 'value'
        return context

In Django, the request object represents an HTTP request made by a client to a server. It is an instance of the HttpRequest class, 
















## Choices
https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices

Need to add UPDATE existing user.
### 04/2023 - I need to create ITBlog models and API endpoint for the ITBlog (React) frontend
1. Create a Django app - python manage.py startapp appname
2. In the settings.py, add app to INSTALLED_APPS
3. In the models.py, create models (need one-to-many relationship this time, Sqlite does not support ArrayField)
4. makemigrations and migrate - creates a set of instructions that Django can use to modify the database schema to match the new model definitions
5. In the admin.py, add models to admin panel
6. In the serializers.py, add serializers
7. In the views.py, create views ( views handle HTTP requests and returns a response)
8. In the urls.py, add views (URL patterns map URLs to a view functions)
9. Test on Postman
Notes: changed null=True to default=""

### How to set up Django and Gunicorn on Ubuntu server
1. Create a virtual environment - python3 -m venv venv
2. Activate virtual environment - source venv/bin/activate
2. Install dependencies - pip3 install -r requirements.txt
3. Install gunicorn - pip3 install gunicorn (this will add gunicorn to venv/bin/ )
4. Check if Gunicorn can host project - gunicorn <django project>.wsgi:application --bind 0.0.0.0:8000
5. Configure gunicorn service file: /etc/systemd/system/gunicorn.service
6. Run these commands: 
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    sudo systemctl status gunicorn
    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn