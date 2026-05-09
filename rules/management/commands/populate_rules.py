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
                'full_text': 'The main objective of the school uniform is to maintain uniformity in appearance. The school uniform has a significant impact on a student\'s life. Students should wear uniform all times during school hours. Cleanliness and personal hygiene must be maintained.',
                'applicable_to': 'All'
            },
            {
                'title': 'Boys Uniform Specification',
                'category': 'Uniform & Appearance',
                'severity': 'low',
                'description': 'Sky-blue shirt with monogram, grey pants, and black shoes/sneakers.',
                'full_text': 'The school uniform for boys is a sky-blue shirt (having a school monogram on the left side pocket) with a collar, grey (ash) pants, and must wear black shoes/sneakers/keds. The use of jeans clothes is forbidden. Shirts must be tucked in properly and no shabbiness in costumes and manners be allowed.',
                'applicable_to': 'Boys'
            },
            {
                'title': 'Girls Uniform Specification',
                'category': 'Uniform & Appearance',
                'severity': 'low',
                'description': 'Sky blue kameez, gray urna, belt, and salwar.',
                'full_text': 'The school uniform for junior girls (grades III to V) is a sky blue top and gray skirts with a monogram on left side. Uniform for senior girls (grade VI and above) is sky blue kameez (KvwgR), gray color urna (Iobv), belt, and salwar. During the winter students will use a navy blue blazer or sweater with a monogram.',
                'applicable_to': 'Girls'
            },
            {
                'title': 'Grooming & Haircut',
                'category': 'Uniform & Appearance',
                'severity': 'low',
                'description': 'Boys must have a proper decent haircut; long hair/nails not permitted.',
                'full_text': 'Boys must have a proper and decent haircut. Long hair, as well as long nails, are not permitted. Students are not allowed to highlight, colour, or tint their hair.',
                'applicable_to': 'Boys'
            },
            {
                'title': 'Jewelry & Cosmetics',
                'category': 'Uniform & Appearance',
                'severity': 'low',
                'description': 'Restrictions on jewelry, nail polish, and makeup for girls.',
                'full_text': 'Girl students shall not wear any jewelry, have long nails, or apply nail polish/kajal (KvRj), mehendi (‡bŠ) when they come to school. Girls must always make two plaits and tie up their hair properly using white/black bands or clips.',
                'applicable_to': 'Girls'
            },
            # Conduct
            {
                'title': 'Care for School Property',
                'category': 'Conduct & Ethics',
                'severity': 'medium',
                'description': 'Refrain from scribbling or scratching on desks, chairs, or walls.',
                'full_text': 'Students must learn to take care of the school property. They should refrain from scribbling or scratching on school desks, chairs, furniture or walls, etc. Students should keep the school premises clean by putting litter in the appropriate bins. Any damage to school property must be reported to the office at once. Students will be liable to pay for any damage caused by them.',
                'applicable_to': 'All'
            },
            {
                'title': 'Language Policy',
                'category': 'Conduct & Ethics',
                'severity': 'low',
                'description': 'English should be the medium of communication in and out of classrooms.',
                'full_text': 'Since a stronger emphasis is put on \'English Language\', students should speak English in and out of their classroom.',
                'applicable_to': 'All'
            },
            {
                'title': 'Courteous Behavior',
                'category': 'Conduct & Ethics',
                'severity': 'medium',
                'description': 'Greet teachers and behave respectfully wherever you go.',
                'full_text': 'Josephites should behave courteously wherever they go. They should always remember that the school is judged by their conduct. They should greet teachers wherever they meet them. At all times, students must behave themselves in a manner appropriate for the classroom.',
                'applicable_to': 'All'
            },
            # Attendance
            {
                'title': 'Leave Validation',
                'category': 'Attendance & Leave',
                'severity': 'medium',
                'description': 'Leave must be validated by an application and doctor certificate.',
                'full_text': 'Leave of absence should be validated by an application before/after the students return to school, showing valid reasons/Doctor certificate in case of sickness. Leave without valid reason will be subject to pay a fine of taka 100 (One hundred) only for each day.',
                'applicable_to': 'All'
            },
            {
                'title': 'Late Attendance Policy',
                'category': 'Attendance & Leave',
                'severity': 'medium',
                'description': 'Fines and procedures for arriving after the gate closes.',
                'full_text': 'School begins at 1:25 p.m. The gate closes for students at 1:15 pm. Students attending school later than 1:15 will not be allowed to attend class directly. Such students will have to obtain a late attendance slip from the office and take an excuse slip paying a fine of taka 100/- only.',
                'applicable_to': 'All'
            },
            {
                'title': '85% Attendance Rule',
                'category': 'Attendance & Leave',
                'severity': 'high',
                'description': 'Minimum attendance required for promotion and exam registration.',
                'full_text': 'Students who do not attend 85% of the school working days may not be promoted. For Class X, 85% attendance is mandatory/compulsory to register for the O\' Level Examinations from school.',
                'applicable_to': 'All'
            },
            # Academic
            {
                'title': 'Pass Marks Requirement',
                'category': 'Academic Excellence',
                'severity': 'high',
                'description': 'Minimum marks required in each subject for Grades III to X.',
                'full_text': 'Pass marks in each subject: For Grades III to X is 60%. A student may be detained if she/he fails in the same subject for two consecutive years. Students of classes III-X failing in three or more subjects will be given a Transfer Certificate (TC).',
                'applicable_to': 'All'
            },
            {
                'title': 'Academic Integrity',
                'category': 'Academic Excellence',
                'severity': 'critical',
                'description': 'Cheating and copying in examinations is strictly prohibited.',
                'full_text': 'Adopting unfair means in the examination: Any student who is caught cheating or copying will be given a severity of the case T.C. (Transfer Certificate). Any Students found tempering with result shall be given an instant T.C.',
                'applicable_to': 'All'
            },
            # Safety
            {
                'title': 'Mobile Phone & Electronics Ban',
                'category': 'Safety & Prohibitions',
                'severity': 'high',
                'description': 'Ban on phones, cameras, and recording devices.',
                'full_text': 'Students must not use or carry any mobile phone, camera, or mechanical device in the school. Toys, cosmetics, ornaments, records and recording devices, cassettes, iPod, MP3, MP4, video camera or any other cameras are strictly forbidden.',
                'applicable_to': 'All'
            },
            {
                'title': 'Anti-Bullying & Drugs Policy',
                'category': 'Safety & Prohibitions',
                'severity': 'critical',
                'description': 'Zero tolerance for bullying, drugs, and cigarettes.',
                'full_text': 'All forms of bullying are strictly prohibited in the school premises and subject to T.C. Consumption or possession of cigarettes, electronic cigarette, illegal commodities like drugs in the school premises by students is strictly prohibited and leads to an instant TC.',
                'applicable_to': 'All'
            },
            {
                'title': 'Social Media Conduct',
                'category': 'Safety & Prohibitions',
                'severity': 'critical',
                'description': 'Slang or unethical language on social networks is a punishable offense.',
                'full_text': 'Anyone found using unethical, immoral, slang language in any social network i.e. Facebook, Twitter, Instagram etc, towards any teacher or to the school may be given an instant T.C.',
                'applicable_to': 'All'
            },
        ]

        for r_data in rules_data:
            rule, created = Rule.objects.update_or_create(
                title=r_data['title'],
                defaults={
                    'category': categories[r_data['category']],
                    'description': r_data['description'],
                    'full_text': r_data['full_text'],
                    'severity': r_data['severity'],
                    'status': 'active',
                    'created_by': admin_user,
                    'applicable_to': r_data['applicable_to']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created rule: {r_data["title"]}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated rule: {r_data["title"]} with full text'))

        self.stdout.write(self.style.SUCCESS('Successfully populated rules database.'))
