from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from accounts.mixins import AdminRequiredMixin, StudentRequiredMixin
from accounts.models import User

from .forms import AcademicRecordForm, SkillForm, StudentProfileForm
from .models import AcademicRecord, Skill, StudentProfile


# ─── ADMIN VIEWS ────────────────────────────────────────────────

class StudentListView(AdminRequiredMixin, ListView):
    model = StudentProfile
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        qs = StudentProfile.objects.select_related('user').order_by('-created_at')
        branch = self.request.GET.get('branch')
        year = self.request.GET.get('year')
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        if branch:
            qs = qs.filter(branch=branch)
        if year:
            qs = qs.filter(year=year)
        if status:
            qs = qs.filter(placement_status=status)
        if search:
            qs = qs.filter(user__full_name__icontains=search) | qs.filter(roll_number__icontains=search)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['branch_choices'] = StudentProfile.BRANCH_CHOICES
        ctx['year_choices'] = StudentProfile.YEAR_CHOICES
        ctx['status_choices'] = StudentProfile.STATUS_CHOICES
        return ctx


class StudentDetailView(AdminRequiredMixin, DetailView):
    model = StudentProfile
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        return StudentProfile.objects.select_related('user').prefetch_related('academic_records', 'skills')


class AdminCreateStudentView(AdminRequiredMixin, View):
    template_name = 'students/student_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': StudentProfileForm()})

    def post(self, request):
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Create user account first
            email = request.POST.get('email')
            full_name = request.POST.get('full_name')
            password = request.POST.get('password')
            user = User.objects.create_user(email=email, password=password, full_name=full_name, role='student')
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Student created successfully.')
            return redirect('students:student_list')
        return render(request, self.template_name, {'form': form})


class UpdatePlacementStatusView(AdminRequiredMixin, View):
    def post(self, request, pk):
        student = get_object_or_404(StudentProfile, pk=pk)
        status = request.POST.get('placement_status')
        if status in dict(StudentProfile.STATUS_CHOICES):
            student.placement_status = status
            student.save()
            messages.success(request, 'Placement status updated.')
        return redirect('students:student_detail', pk=pk)


# ─── STUDENT VIEWS ───────────────────────────────────────────────

class MyProfileView(StudentRequiredMixin, View):
    template_name = 'students/my_profile.html'

    def get(self, request):
        try:
            profile = StudentProfile.objects.prefetch_related(
                'academic_records', 'skills'
            ).get(user=request.user)
        except StudentProfile.DoesNotExist:
            profile = None
        return render(request, self.template_name, {'profile': profile})


class CreateProfileView(StudentRequiredMixin, View):
    template_name = 'students/profile_form.html'

    def get(self, request):
        if StudentProfile.objects.filter(user=request.user).exists():
            return redirect('students:my_profile')
        return render(request, self.template_name, {'form': StudentProfileForm()})

    def post(self, request):
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('students:my_profile')
        return render(request, self.template_name, {'form': form})


class UpdateProfileView(StudentRequiredMixin, View):
    template_name = 'students/profile_form.html'

    def get(self, request):
        profile = get_object_or_404(StudentProfile, user=request.user)
        form = StudentProfileForm(instance=profile)
        return render(request, self.template_name, {'form': form, 'update': True})

    def post(self, request):
        profile = get_object_or_404(StudentProfile, user=request.user)
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('students:my_profile')
        return render(request, self.template_name, {'form': form, 'update': True})


class AddAcademicRecordView(StudentRequiredMixin, View):
    template_name = 'students/academic_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': AcademicRecordForm()})

    def post(self, request):
        profile = get_object_or_404(StudentProfile, user=request.user)
        form = AcademicRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.student = profile
            record.save()
            messages.success(request, 'Academic record added.')
            return redirect('students:my_profile')
        return render(request, self.template_name, {'form': form})


class AddSkillView(StudentRequiredMixin, View):
    template_name = 'students/skill_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': SkillForm()})

    def post(self, request):
        profile = get_object_or_404(StudentProfile, user=request.user)
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.student = profile
            skill.save()
            messages.success(request, 'Skill added.')
            return redirect('students:my_profile')
        return render(request, self.template_name, {'form': form})
