from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponse
import csv

from .models import Member, Homecell, Ministry, Family
from .forms import SignupForm, MemberForm, FamilyForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # If user is active (not requesting superadmin), log them in
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            return render(request, 'members/signup_pending.html', {'user': user})
    else:
        form = SignupForm()
    return render(request, 'members/signup.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    if user.is_super_admin():
        members = Member.objects.all()
    elif user.is_homecell_pastor():
        members = Member.objects.filter(homecell=user.homecell)
    elif user.is_ministry_leader():
        members = Member.objects.filter(ministry=user.ministry)
    else:
        members = Member.objects.none()

    total = members.count()
    per_homecell = members.values('homecell__name').annotate(count=models.Count('id'))
    per_ministry = members.values('ministry__name').annotate(count=models.Count('id'))

    # age groups
    ages = [m.age for m in members if m.age is not None]
    children = len([a for a in ages if a < 13])
    youth = len([a for a in ages if 13 <= a < 25])
    adults = len([a for a in ages if 25 <= a < 60])
    elderly = len([a for a in ages if a >= 60])

    return render(request, 'members/dashboard.html', {
        'members': members[:20],
        'total': total,
        'per_homecell': per_homecell,
        'per_ministry': per_ministry,
        'age_breakdown': {'children': children, 'youth': youth, 'adults': adults, 'elderly': elderly}
    })

@login_required
def members_list(request):
    user = request.user
    if user.is_super_admin():
        qs = Member.objects.all()
    elif user.is_homecell_pastor():
        qs = Member.objects.filter(homecell=user.homecell)
    elif user.is_ministry_leader():
        qs = Member.objects.filter(ministry=user.ministry)
    else:
        qs = Member.objects.none()

    query = request.GET.get('q')
    if query:
        qs = qs.filter(models.Q(first_name__icontains=query) | models.Q(last_name__icontains=query))

    return render(request, 'members/members_list.html', {'members': qs})

@login_required
def member_create(request):
    user = request.user
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
            return redirect('members_list')
    else:
        form = MemberForm()
        # pre-assign homecell/ministry based on user
        if user.is_homecell_pastor() and user.homecell:
            form.fields['homecell'].initial = user.homecell
        if user.is_ministry_leader() and user.ministry:
            form.fields['ministry'].initial = user.ministry
    return render(request, 'members/member_form.html', {'form': form})

@login_required
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    user = request.user
    # permission checks
    if user.is_homecell_pastor() and member.homecell != user.homecell:
        return HttpResponse('Forbidden', status=403)
    if user.is_ministry_leader() and member.ministry != user.ministry:
        return HttpResponse('Forbidden', status=403)

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('members_list')
    else:
        form = MemberForm(instance=member)
    return render(request, 'members/member_form.html', {'form': form, 'member': member})

@login_required
def export_members_csv(request):
    user = request.user
    if user.is_super_admin():
        qs = Member.objects.all()
    elif user.is_homecell_pastor():
        qs = Member.objects.filter(homecell=user.homecell)
    elif user.is_ministry_leader():
        qs = Member.objects.filter(ministry=user.ministry)
    else:
        qs = Member.objects.none()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="members.csv"'

    writer = csv.writer(response)
    writer.writerow(['First name','Last name','DOB','Homecell','Ministry','Status','Family'])
    for m in qs:
        writer.writerow([m.first_name, m.last_name, m.dob, getattr(m.homecell, 'name', ''), getattr(m.ministry, 'name', ''), m.status, getattr(m.family, 'family_name', '')])

    return response