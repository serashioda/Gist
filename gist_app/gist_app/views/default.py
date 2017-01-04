"""The main views for our Gist App."""

from pyramid.view import view_config, forbidden_view_config
from gist_app.models import Profile
from pyramid.httpexceptions import HTTPFound
import datetime
from gist_app.security import check_credentials
from pyramid.security import remember, forget


@view_config(route_name="list",
             renderer="../templates/list.jinja2")
def list_view(request):
    """A listing of profiles for the home page."""
    query = request.dbsession.query(Profile)
    profiles = query.order_by(Profile.date.desc()).all()
    return {
        "profiles": profiles,
    }


@view_config(route_name="detail",
             renderer="../templates/detail.jinja2")
def detail_view(request):
    """The detail page for an profile."""
    the_id = int(request.matchdict["id"])
    profile = request.dbsession.query(Profile).get(the_id)
    return {"profile": profile}


@view_config(
    route_name="create",
    renderer="../templates/add.jinja2",
    permission="add"
)
def create_view(request):
    """Create a new profile."""
    if request.POST:
        profile = Profile(
            name=request.POST["name"],
            favorite_food=request.POST["favorite_food"],
            date=datetime.datetime.now(),
            description=request.POST["description"]
        )
        request.dbsession.add(profile)
        return HTTPFound(request.route_url('list'))

    return {}


@view_config(
    route_name="edit",
    renderer="../templates/edit.jinja2",
    permission="add"
)
def edit_view(request):
    """Edit an existing profile."""
    the_id = int(request.matchdict["id"])
    profile = request.dbsession.query(Profile).get(the_id)
    if request.POST:
        profile.item = request.POST["name"]
        profile.favorite_food = request.POST["favorite_food"]
        profile.description = request.POST["description"]
        request.dbsession.flush()
        return HTTPFound(request.route_url('list'))

    form_fill = {
        "name": profile.item,
        "favorite_food": profile.favorite_food,
        "description": profile.description
    }
    return {"data": form_fill}



@view_config(route_name="login",
             renderer="../templates/login.jinja2",
             require_csrf=False)
def login_view(request):
    """Authenticate the incoming user."""
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(
                request.route_url("list"),
                headers=auth_head
            )

    return {}


@view_config(route_name="logout")
def logout_view(request):
    """Remove authentication from the user."""
    auth_head = forget(request)
    return HTTPFound(request.route_url("list"), headers=auth_head)


@forbidden_view_config(renderer="../templates/forbidden.jinja2")
def not_allowed_view(request):
    """Some special stuff for the forbidden view."""
    return {}


@view_config(route_name="delete", permission="delete")
def delete_view(request):
    """To delete individual items."""
    profile = request.dbsession.query(Profile).get(request.matchdict["id"])
    request.dbsession.delete(profile)
    return HTTPFound(request.route_url("list"))


@view_config(route_name="api_list", renderer="string")
def api_list_view(request):
    profiles = request.dbsession.query(Profile).all()
    output = [item.to_json() for item in profiles]
    return output
