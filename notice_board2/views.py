from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy
from hitcount.views import HitCountDetailView
from .models import NoticeBoard, GRADE_CHOICES
from .forms import NoticeBoardForm

class NoticeBoardListView(ListView):
    """
    List view for notices with multiple filtering options
    """
    model = NoticeBoard
    template_name = 'notice_board2/list.html'
    context_object_name = 'notices'
    paginate_by = 9

    def get_queryset(self):
        # Base queryset (removed status='published' as it doesn't exist in the model)
        queryset = NoticeBoard.objects.all()
        
        # Search handling
        search_query = self.request.GET.get('search')
        if search_query:
            if search_query.lower() == 'academic':
                queryset = queryset.filter(Q(title__icontains='Academic') | Q(content__icontains='Academic'))
            elif search_query.lower() == 'holiday':
                queryset = queryset.filter(Q(title__icontains='Holiday') | Q(content__icontains='Holiday'))
            elif search_query.lower() == 'exam':
                queryset = queryset.filter(Q(title__icontains='Exam') | Q(title__icontains='Assessment') | Q(content__icontains='Exam'))
            else:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) | 
                    Q(content__icontains=search_query)
                )

        # Grade filtering
        grade_id = self.request.GET.get('grade')
        if grade_id:
            queryset = queryset.filter(target_grades__id=grade_id)

        # Sorting
        sort_by = self.request.GET.get('sort', 'newest')
        if sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grades'] = GRADE_CHOICES  # Directly reference the global GRADE_CHOICES
        return context


class NoticeBoardDetailView(HitCountDetailView):
    """
    Detailed view of a specific notice
    """
    model = NoticeBoard
    template_name = 'notice_board2/detail.html'
    context_object_name = 'notice'
    count_hit = True

class NoticeBoardCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating new notices
    """
    model = NoticeBoard
    form_class = NoticeBoardForm
    template_name = 'notice_board2/create.html'
    success_url = reverse_lazy('notice_board2:list')

    def form_valid(self, form):
        """
        Automatically set the creator and add success message
        """
        form.instance.created_by = self.request.user
        messages.success(
            self.request, 
            'Notice has been successfully created!'
        )
        return super().form_valid(form)

class NoticeBoardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating existing notices
    """
    model = NoticeBoard
    form_class = NoticeBoardForm
    template_name = 'notice_board2/create.html'
    success_url = reverse_lazy('notice_board2:list') 

    def test_func(self):
        """
        Ensure only creator or staff can update
        """
        notice = self.get_object()
        return self.request.user == notice.created_by or self.request.user.is_staff

    def form_valid(self, form):
        """
        Add success message on update
        """
        messages.success(
            self.request, 
            'Notice has been successfully updated!'
        )
        return super().form_valid(form)

class NoticeBoardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting notices
    """
    model = NoticeBoard
    template_name = 'notice_board2/delete.html'
    success_url = reverse_lazy('notice_board2:list')

    def test_func(self):
        """
        Ensure only creator or staff can delete
        """
        notice = self.get_object()
        return self.request.user == notice.created_by or self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        """
        Add success message on delete
        """
        messages.success(
            request, 
            'Notice has been successfully deleted!'
        )
        return super().delete(request, *args, **kwargs)


# from django.contrib import messages
# from django.db.models import Q
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.views.generic import (
#     ListView, 
#     DetailView, 
#     CreateView, 
#     UpdateView, 
#     DeleteView
# )
# from django.urls import reverse_lazy
# from hitcount.views import HitCountDetailView
# from django.shortcuts import render
# from django.core.paginator import Paginator
# from django.utils import timezone

# from .models import NoticeBoard, GRADE_CHOICES
# from .forms import NoticeBoardForm

# def notice_board(request):
#     """
#     Function-based view for displaying notices with pagination
#     """
#     notices = NoticeBoard.objects.all()
    
#     # Get the latest date of posted notices
#     latest_notice_date = NoticeBoard.objects.latest('created_at').created_at if notices.exists() else None

#     paginator = Paginator(notices, 9)  # Show 9 notices per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'notice_board2/notice_board.html', {
#         'page_obj': page_obj,
#         'latest_notice_date': latest_notice_date
#     })

# class NoticeBoardListView(ListView):
#     """
#     List view for notices with multiple filtering options
#     """
#     model = NoticeBoard
#     template_name = 'notice_board2/list.html'
#     context_object_name = 'notices'
#     paginate_by = 9

#     def get_queryset(self):
#         queryset = NoticeBoard.objects.all()

#         grade_filter = self.request.GET.get('grade', None)
#         search_query = self.request.GET.get('search', None)

#         if grade_filter:
#             queryset = queryset.filter(target_grades__name=grade_filter)

#         if search_query:
#             queryset = queryset.filter(
#                 Q(title__icontains=search_query) | 
#                 Q(content__icontains=search_query)
#             )

#         return queryset.distinct()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['grades'] = GRADE_CHOICES
#         return context

# class NoticeBoardDetailView(HitCountDetailView):
#     """
#     Detailed view of a specific notice
#     """
#     model = NoticeBoard
#     template_name = 'notice_board2/detail.html'
#     context_object_name = 'notice'
#     count_hit = True

# class NoticeBoardCreateView(LoginRequiredMixin, CreateView):
#     """
#     View for creating new notices
#     """
#     model = NoticeBoard
#     form_class = NoticeBoardForm
#     template_name = 'notice_board2/create.html'
#     success_url = reverse_lazy('notice_board:list')

#     def form_valid(self, form):
#         """
#         Automatically set the creator and add success message
#         """
#         form.instance.created_by = self.request.user
#         messages.success(
#             self.request, 
#             'Notice has been successfully created!'
#         )
#         return super().form_valid(form)

# class NoticeBoardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     """
#     View for updating existing notices
#     """
#     model = NoticeBoard
#     form_class = NoticeBoardForm
#     template_name = 'notice_board2/create.html'
#     success_url = reverse_lazy('notice_board:list')

#     def test_func(self):
#         """
#         Ensure only creator or staff can update
#         """
#         notice = self.get_object()
#         return self.request.user == notice.created_by or self.request.user.is_staff

#     def form_valid(self, form):
#         """
#         Add success message on update
#         """
#         messages.success(
#             self.request, 
#             'Notice has been successfully updated!'
#         )
#         return super().form_valid(form)

# class NoticeBoardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     """
#     View for deleting notices
#     """
#     model = NoticeBoard
#     template_name = 'notice_board2/delete.html'
#     success_url = reverse_lazy('notice_board:list')

#     def test_func(self):
#         """
#         Ensure only creator or staff can delete
#         """
#         notice = self.get_object()
#         return self.request.user == notice.created_by or self.request.user.is_staff

#     def delete(self, request, *args, **kwargs):
#         """
#         Add success message on delete
#         """
#         messages.success(
#             request, 
#             'Notice has been successfully deleted!'
#         )
#         return super().delete(request, *args, **kwargs)