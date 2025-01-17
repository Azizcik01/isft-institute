#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from contextlib import closing

from django.db import connection
from django.shortcuts import render, redirect, HttpResponse

from base.custom import answered_dictfetchall
from core.models import ResultTest, Candidate


def vacancy(request):
    with closing(connection.cursor()) as cursor:
        sql = """
               SELECT id, quest AS question, "true" AS answer, a, b, c, d FROM core_test
               order by random() limit 20;
           """
        cursor.execute(sql)
        result = answered_dictfetchall(cursor)

    if request.POST:
        data = request.POST
        condidate = Candidate.objects.create(**{'FIO': data.get('fio', ), 'pasport_seria': data.get('seria', ),
                                                'pasport_number': data.get('seria_num', ), 'phone': data.get('phone', ),
                                                })
        test = ResultTest.objects.create(candidate=condidate, status='Boshlandi',
                                         test_ids=str(repr([x['id'] for x in result])),)
        request.session['test_id'] = test.id
        return HttpResponse(str(repr({"Natija": 'Oxshadi'})))

    ctx = {
        "quests": result
    }
    return render(request, 'pages/quiz.html', ctx)
