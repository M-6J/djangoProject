from django.http import JsonResponse

from profileApp.models import Notice
from teamApp.models import Team, Member


def accept(request, verif):  # accept invite with verif code: verif code generated in teamApp invite
    if Notice.objects.exists(verif__exact=verif):
        notice = Notice.objects.get(verif__exact=verif)
        target = Team.objects.get(pk=notice.team_pk)

        receiver = Member.objects.create(user=notice.receiver, role=0)

        target.member.add(receiver)
        target.save()

        notice.delete()

        return JsonResponse({'msg': 'success'})
    else:
        return JsonResponse({'msg': 'err 404'})
