from projman.models import Task
from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.inclusion_tag('show_tasks.html')
def show_tasks(project, complete=0):
    tasks = Task.objects.filter(project=project.id, complete=complete).order_by('-completed' if complete else 'priority')

    if complete:
        tasks = tasks[:5]

    return locals()


@register.inclusion_tag('show_milestones.html')
def show_milestones(category):
    min_date = datetime.today() + timedelta(days=-7)
    milestones_active = category.milestone_set.filter(status__exact='active')
    milestones_onhold = category.milestone_set.filter(status__exact='onhold')
    mc = category.milestone_set.filter(status__exact='complete')

    milestones_complete = []
    for m in mc:
        if m.last_status_change().timestamp > min_date:
            milestones_complete.append(m)

    any_milestones = (milestones_active.count() or milestones_onhold.count() or len(milestones_complete))
    
    return locals()


@register.inclusion_tag('show_history.html')
def show_history(category):
    tasks = Task.objects.filter(project__category__exact=category).filter(complete=1).order_by('-completed')[:10]
    
    return locals()
    

@register.simple_tag
def colorizer(index, total):
    r = 225 / total
    c = index * r + 30

    return "#%02x%02x%02x" % (c, c, c)


def _perc_colorizer(perc):
    colors = ((175,0,0),(255,125,0),(0,175,0))
    grads = []
    
    def calc_grads(ca, cb, num):
        r1 = ca[0]
        g1 = ca[1]
        b1 = ca[2]
    
        r2 = cb[0]
        g2 = cb[1]
        b2 = cb[2]
    
        dr = float(r2 - r1) / float(num)
        dg = float(g2 - g1) / float(num)
        db = float(b2 - b1) / float(num)

        for i in range(num):
            r = r1 + int(dr * i)
            g = g1 + int(dg * i)
            b = b1 + int(db * i)
            
            r = 0 if r<0 else (255 if r>255 else r)
            g = 0 if g<0 else (255 if g>255 else g)
            b = 0 if b<0 else (255 if b>255 else b)
        
            grads.append((r,g,b))
    
    calc_grads(colors[0], colors[1], 50)
    calc_grads(colors[1], colors[2], 50)
    
    perc = int(perc) - 1
    perc = 0 if perc<0 else (99 if perc>99 else perc)
    
    return grads[perc]


@register.simple_tag
def perc_colorizer(perc):
    return "#%02x%02x%02x" % _perc_colorizer(perc)
    

@register.simple_tag
def perc_colorizer_dark(perc, amount):
    color = _perc_colorizer(perc)

    r = color[0] - amount
    g = color[1] - amount
    b = color[2] - amount
    
    r = 0 if r<0 else r
    g = 0 if g<0 else g
    b = 0 if b<0 else b
    
    return "#%02x%02x%02x" % (r,g,b)


@register.simple_tag
def milestone_deadline_color(milestone):
    days_remaining = milestone.days_remaining()

    if milestone.status == 'onhold':
        return '#888'

    if not milestone.status == 'complete':
        if days_remaining <= 0:
            return '#c00'
        elif days_remaining < 5:
            return '#e70'
        
        return '#000'
    
    return '#080'


@register.simple_tag
def milestone_days_remaining(milestone):
    days_remaining = milestone.days_remaining()
    append = "s" if days_remaining else ""
    
    if days_remaining >= 0:
        return "<strong>%d</strong> day%s remaining" % (days_remaining, append)
    else:
        return "OVERDUE!"


@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''
