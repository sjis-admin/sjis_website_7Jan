from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rules.models import RuleCategory, Rule
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the database with rules from the Student Handbook'

    def handle(self, *args, **options):
        admin_user = User.objects.filter(is_superuser=True).first()
        
        categories_data = [
            {'name': 'Uniform & Appearance', 'icon': 'ri-shirt-line', 'description': 'Regulations regarding school dress code and personal grooming.'},
            {'name': 'Conduct & Ethics', 'icon': 'ri-scales-3-line', 'description': 'Fundamental ideas of self-discipline, harmony, and cooperation.'},
            {'name': 'Attendance & Leave', 'icon': 'ri-calendar-check-line', 'description': 'Rules regarding punctuality, leave of absence, and late attendance.'},
            {'name': 'Academic Excellence', 'icon': 'ri-book-open-line', 'description': 'Pass marks, promotion criteria, and assignment submissions.'},
            {'name': 'Safety & Prohibitions', 'icon': 'ri-shield-user-line', 'description': 'Prohibited items, bullying, and campus safety policies.'},
        ]

        # Create categories
        categories = {}
        for cat_data in categories_data:
            category, created = RuleCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'description': cat_data['description']
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_data["name"]}'))

        rules_data = [
            # Uniform
            {
                'title': 'General Uniform Cleanliness',
                'category': 'Uniform & Appearance',
                'severity': 'low',
                'description': 'Cleanliness and personal hygiene must be maintained at all times.',
                'applicable_to': 'All'
            },
            {
                'title': 'Boys Uniform Specification',
                'category': 'Uniform & Appearance',
                'severity': 'low',
                'description': 'Sky-blue shirt with monogram, grey pants, and black shoes/sneakers.',
                'applicable_to': 'Boys'
            },
            {
                'title': 'Girls Uniform Specification',
                'category': 'Uniform & Appearance',
                'severity': 'low',
                'description': 'Sky blue kameez, gray urna, belt, and salwar. Junior girls (III-V) wear sky blue top and gray skirts.',
                'applicable_to': 'Girls'
            },
            {
                'title': 'Grooming & Haircut',
                'category': 'Uniform & Appearance',
                'severity': 'low',
                'description': 'Boys must have a proper decent haircut; long hair/nails not permitted. No highlights/colors.',
                'applicable_to': 'Boys'
            },
            {
                'title': 'Jewelry & Cosmetics',
                'category': 'Uniform & Appearance',
                'severity': 'low',
                'description': 'Girls shall not wear jewelry, long nails, nail polish, or mehendi.',
                'applicable_to': 'Girls'
            },
            # Conduct
            {
                'title': 'Care for School Property',
                'category': 'Conduct & Ethics',
                'severity': 'medium',
                'description': 'Refrain from scribbling or scratching on desks, chairs, or walls. Keep premises clean.',
                'applicable_to': 'All'
            },
            {
                'title': 'Language Policy',
                'category': 'Conduct & Ethics',
                'severity': 'low',
                'description': 'Students should speak English in and out of their classrooms as part of language immersion.',
                'applicable_to': 'All'
            },
            {
                'title': 'Courteous Behavior',
                'category': 'Conduct & Ethics',
                'severity': 'medium',
                'description': 'Greet teachers wherever you meet them. Behave courteously wherever you go.',
                'applicable_to': 'All'
            },
            # Attendance
            {
                'title': 'Leave Validation',
                'category': 'Attendance & Leave',
                'severity': 'medium',
                'description': 'Leave must be validated by an application and doctor certificate in case of sickness.',
                'applicable_to': 'All'
            },
            {
                'title': 'Late Attendance Fine',
                'category': 'Attendance & Leave',
                'severity': 'medium',
                'description': 'Coming later than 1:15 PM subjects students to a fine of 100 Taka and requires a late slip.',
                'applicable_to': 'All'
            },
            {
                'title': 'Mandatory Attendance for Promotion',
                'category': 'Attendance & Leave',
                'severity': 'high',
                'description': '85% attendance is mandatory for promotion and registration for O/A Level exams.',
                'applicable_to': 'All'
            },
            # Academic
            {
                'title': 'Pass Marks Requirement',
                'category': 'Academic Excellence',
                'severity': 'high',
                'description': 'Pass marks in each subject for Grades III to X is 60%.',
                'applicable_to': 'All'
            },
            {
                'title': 'Assignment Submissions',
                'category': 'Academic Excellence',
                'severity': 'medium',
                'description': 'Assignments must be submitted within the deadline. No re-answering after submission.',
                'applicable_to': 'All'
            },
            {
                'title': 'Academic Integrity',
                'category': 'Academic Excellence',
                'severity': 'critical',
                'description': 'Any student caught cheating or copying in exams will face immediate Transfer Certificate (T.C.).',
                'applicable_to': 'All'
            },
            # Safety
            {
                'title': 'Mobile Phone & Electronics Ban',
                'category': 'Safety & Prohibitions',
                'severity': 'high',
                'description': 'Students must not use or carry mobile phones, cameras, or mechanical devices in school.',
                'applicable_to': 'All'
            },
            {
                'title': 'Anti-Bullying Policy',
                'category': 'Safety & Prohibitions',
                'severity': 'critical',
                'description': 'All forms of bullying are strictly prohibited and subject to immediate Transfer Certificate (T.C.).',
                'applicable_to': 'All'
            },
            {
                'title': 'Drugs & Prohibited Items',
                'category': 'Safety & Prohibitions',
                'severity': 'critical',
                'description': 'Possession of drugs, cigarettes, or explosives is strictly prohibited and leads to instant T.C.',
                'applicable_to': 'All'
            },
            {
                'title': 'Social Media Conduct',
                'category': 'Safety & Prohibitions',
                'severity': 'critical',
                'description': 'Using unethical, immoral, or slang language on social networks towards teachers or school leads to instant T.C.',
                'applicable_to': 'All'
            },
        ]

        for r_data in rules_data:
            rule, created = Rule.objects.get_or_create(
                title=r_data['title'],
                defaults={
                    'category': categories[r_data['category']],
                    'description': r_data['description'],
                    'severity': r_data['severity'],
                    'status': 'active',
                    'created_by': admin_user,
                    'applicable_to': r_data['applicable_to']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created rule: {r_data["title"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Rule already exists: {r_data["title"]}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated rules database.'))
