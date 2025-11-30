from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import RuleCategory, Rule, Violation
from django.db.models import Count
from django.db.models import Q


@login_required
def rule_list(request, category_id=None):
    """
    List rules, optionally filtered by category
    """
    # Start with all active rules
    rules = Rule.objects.filter(status='active')
    
    # If a specific category is provided, filter by that category
    if category_id:
        category = get_object_or_404(RuleCategory, id=category_id)
        rules = rules.filter(category=category)
        
    # Optional search and filtering
    query = request.GET.get('query', '')
    severity = request.GET.get('severity', '')
    
    if query:
        rules = rules.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if severity:
        rules = rules.filter(severity=severity)
    
    # Get all categories for the sidebar/filter
    categories = RuleCategory.objects.all()
    
    context = {
        'rules': rules,
        'categories': categories,
        'selected_category': category_id if category_id else None,
        'query': query,
        'selected_severity': severity,
        'severity_choices': Rule.SEVERITY_CHOICES
    }
    
    return render(request, 'rules/rule_list.html', context)

@login_required
def rule_category_list(request):
    """List all rule categories"""
    categories = RuleCategory.objects.annotate(rule_count=Count('rules'))
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'rules/category_list.html', context)

@login_required
def rule_detail(request, rule_id):
    """
    Display detailed information about a specific rule
    """
    # Fetch the rule with related information
    rule = get_object_or_404(Rule, id=rule_id)
    
    # Get related documents
    documents = rule.documents.all()
    
    # Get recent violations for this rule
    recent_violations = Violation.objects.filter(rule=rule).order_by('-reported_at')[:5]
    
    # Count of total violations
    total_violations = rule.violations.count()
    
    context = {
        'rule': rule,
        'documents': documents,
        'recent_violations': recent_violations,
        'total_violations': total_violations,
        'can_report_violation': request.user.is_authenticated
    }
    
    return render(request, 'rules/rule_detail.html', context)

@login_required
def rule_dashboard(request):
    """Dashboard view for rules and violations"""
    # Get total number of active rules
    total_active_rules = Rule.objects.filter(status='active').count()
    
    # Get total number of rule categories
    total_categories = RuleCategory.objects.count()
    
    # Get recent violations
    recent_violations = Violation.objects.order_by('-reported_at')[:5]
    
    # Get violation status summary
    violation_status_summary = Violation.objects.values('status').annotate(count=Count('status'))
    
    context = {
        'total_active_rules': total_active_rules,
        'total_categories': total_categories,
        'recent_violations': recent_violations,
        'violation_status_summary': violation_status_summary,
    }
    
    return render(request, 'rules/dashboard.html', context)

@login_required
def report_violation(request, rule_id):
    """Report a violation of a specific rule"""
    rule = get_object_or_404(Rule, id=rule_id)
    
    # Get all users except the current user
    users = User.objects.exclude(id=request.user.id)
    
    if request.method == 'POST':
        offender_username = request.POST.get('offender')
        description = request.POST.get('description')
        evidence = request.FILES.get('evidence')
        
        try:
            offender = User.objects.get(username=offender_username)
            violation = Violation.objects.create(
                rule=rule,
                reported_by=request.user,
                offender=offender,
                description=description,
                evidence=evidence
            )
            messages.success(request, 'Violation reported successfully!')
            return redirect('rule_detail', rule_id=rule.id)
        except User.DoesNotExist:
            messages.error(request, 'Invalid user selected.')
    
    context = {
        'rule': rule,
        'users': users,
    }
    return render(request, 'rules/report_violation.html', context)

# Additional helper function for searching and filtering
@login_required
def search_rules(request):
    """Search and filter rules"""
    query = request.GET.get('query', '')
    category = request.GET.get('category')
    severity = request.GET.get('severity')

    rules = Rule.objects.filter(status='active')

    if query:
        rules = rules.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )

    if category:
        rules = rules.filter(category__id=category)

    if severity:
        rules = rules.filter(severity=severity)

    context = {
        'rules': rules,
        'categories': RuleCategory.objects.all(),
        'query': query,
        'selected_category': category,
        'selected_severity': severity
    }

    return render(request, 'rules/search_rules.html', context)

# Violation tracking view for administrators
@login_required
def violation_tracking(request):
    """Track and manage rule violations"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Administrator rights required.')
        return redirect('rule_dashboard')

    violations = Violation.objects.all().select_related('rule', 'reported_by', 'offender')

    # Filtering options
    status = request.GET.get('status')
    if status:
        violations = violations.filter(status=status)

    context = {
        'violations': violations,
        'status_choices': Violation.STATUS_CHOICES
    }

    return render(request, 'rules/violation_tracking.html', context)

# Public-facing views (no login required)
def public_rules_list(request):
    """
    Public view for browsing school rules and regulations
    """
    # Get all active rules
    rules = Rule.objects.filter(status='active').select_related('category')
    
    # Get all categories for filtering
    categories = RuleCategory.objects.all()
    
    # Optional filtering
    category_id = request.GET.get('category')
    severity = request.GET.get('severity')
    query = request.GET.get('query', '')
    
    if category_id:
        rules = rules.filter(category__id=category_id)
    
    if severity:
        rules = rules.filter(severity=severity)
    
    if query:
        rules = rules.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    context = {
        'rules': rules,
        'categories': categories,
        'selected_category': category_id,
        'selected_severity': severity,
        'query': query,
        'severity_choices': Rule.SEVERITY_CHOICES
    }
    
    return render(request, 'rules/rules_public.html', context)

def public_category_view(request, category_id):
    """
    Public view for viewing rules in a specific category
    """
    category = get_object_or_404(RuleCategory, id=category_id)
    rules = Rule.objects.filter(category=category, status='active')
    
    context = {
        'category': category,
        'rules': rules,
        'all_categories': RuleCategory.objects.all()
    }
    
    return render(request, 'rules/category_public.html', context)

def public_rule_detail(request, rule_id):
    """
    Public view for viewing detailed information about a specific rule
    """
    rule = get_object_or_404(Rule, id=rule_id, status='active')
    
    # Get related documents
    documents = rule.documents.all()
    
    # Get related rules in the same category
    related_rules = Rule.objects.filter(
        category=rule.category, 
        status='active'
    ).exclude(id=rule.id)[:3]
    
    context = {
        'rule': rule,
        'documents': documents,
        'related_rules': related_rules
    }
    
    return render(request, 'rules/rule_public_detail.html', context)