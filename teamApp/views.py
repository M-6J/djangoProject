from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from taskApp.models import Task
from teamApp.forms import TeamCreationForm
from teamApp.models import Team


# ============================================= Managing Team Here From, ===============================================
# ===========================================  create, update, del, detail =============================================
# add decorators here, 'must be login-ed' for post, get
class TeamCreateView(CreateView):  # User can make a Team
    model = Team
    form_class = TeamCreationForm
    template_name = 'index.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = self.request.user
        obj.creator = user  # Creator -> creator&member
        obj.member = user
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return  # reverse to team detail


# add decorators here, 'creator only' for post, get
class TeamUpdateView(UpdateView):  # Creator can change team's name and description
    model = Team
    context_object_name = 'target_team'
    form_class = TeamCreationForm
    template_name = 'index.html'

    def get_success_url(self):
        return  # reverse to team detail


# add decorators here, 'creator only' for post, get
def del_team(request):  # Creator can del team
    pass


# add decorators here, 'member only' for post, get
class TeamDetailView(DetailView):
    model = Team
    template_name = 'index.html'
    context_object_name = 'target_team'

    # get this_team.pk
    def get_context_data(self, **kwargs):
        team = self.object

        # query members below, and keep in context
        object_list = User.objects.filter(team=team)
        context = super(TeamDetailView, self).get_context_data(object_list=object_list, **kwargs)

        # query tasks below, keep in context, and return context
        tasks = Task.objects.filter(team=team)
        context['tasks'] = tasks

        return context


# ============================================ Managing Members Here From, =============================================
# =========================================  add, del(quit), promote, degrade ==========================================
# add decorators here, 'creator and manager only' for post, get
def add_member(request):  # add member by input: email
    team = Team.objects.get(pk=request.GET('team_pk'))
    target = User.objects.get(email__exact=request.GET('target_user'))

    if team.member.contains(target):
        pass  # already invited! and just redirect to member managing url
    else:
        pass  # send complete!
    # send notice to user, you are invited to team -> this link: add user to member, and member redirect to team detail.
    pass


# add decorators here, 'creator, manager and self only' for post, get
def del_member(request):  # quit or del member, quit: self, del: manager or creator
    team = Team.objects.get(pk=request.GET('team_pk'))
    target = User.objects.get(email__exact=request.GET('target_user'))

    if team.member.contains(target):
        pass  # del target from member pool
    pass


# add decorators here, 'creator only' for post, get
def promote(request):
    team = Team.objects.get(pk=request.GET('team_pk'))
    if team == request.user.own_team:
        target = User.objects.get(pk=request.GET('user_pk'))
        team.manager.add(target)
        team.save()
    else:
        return HttpResponseForbidden

    return  # return to team detail


# add decorators here, 'creator only' for post, get
def degrade(request):
    team = Team.objects.get(pk=request.GET('team_pk'))
    if team == request.user.own_team:
        team.delete()
    else:
        return HttpResponseForbidden

    return  # return to main
