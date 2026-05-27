# شرح مشروع Buildly

هذا الملف هو خريطة فهم للمشروع كما هو موجود في الكود: ماذا يفعل كل جزء، ما المعمارية المستخدمة، كيف يمر الطلب من الواجهة إلى الباك إند، ولماذا استخدمنا Docker ومحرر الأكواد.

## 1. الصورة العامة

المشروع Full Stack:

- Frontend: React + Vite، موجود في `frontend`.
- Backend: Django + Django REST Framework، موجود في `backendPBL/projectBPL`.
- Database: SQLite عبر Django ORM، الملف هو `backendPBL/projectBPL/db.sqlite3`.
- Docker: مستخدم لتشغيل كود الطالب داخل حاوية معزولة، وليس لتشغيل كل المشروع.

الفكرة: منصة تعلم بالاعتماد على المشاريع. يوجد نوعان من المستخدمين:

- Learner: يتسجل، يدخل كورسات، يبدأ مشاريع، يحل مهام، يشغل كود، ويسلم.
- Admin/Instructor: ينشئ كورسات ومشاريع ومهام، يراجع التسليمات، ويضع تقييم.

## 2. المعمارية: هل هي MVT أم Layered؟

الجواب المختصر: المشروع يستخدم الاثنين، لكن كل واحدة في مستوى مختلف.

### MVT داخل Django

Django أصلا مبني على MVT:

- Model: ملفات `models.py`، تمثل الجداول والعلاقات.
- View: ملفات `views.py`، تستقبل الطلب وتعالج المنطق وترجع Response.
- Template: في Django التقليدي تكون HTML داخل backend. هنا لا توجد Templates فعلية لأن React أخذت دور واجهة العرض.

بما أن المشروع REST API، فالـ Template لم تعد صفحة Django HTML، بل أصبحت React في `frontend/src/pages`.

### Layered Architecture على مستوى Full Stack

المشروع أيضا Layered:

- Presentation Layer: صفحات ومكونات React.
- API Client Layer: ملف `frontend/src/services/api.js`.
- Routing Layer: ملفات `urls.py` في Django.
- Controller/API Layer: ملفات `views.py`.
- Validation/Serialization Layer: ملفات `serializers.py`.
- Domain/Data Layer: ملفات `models.py` ودوالها.
- Persistence Layer: SQLite + Django ORM.

### كيف اندمجوا؟

بدل هذا الشكل التقليدي:

`Django URL -> Django View -> Django Template`

صار الشكل:

`React Page -> api.js -> Django URL -> DRF View -> Serializer -> Model/ORM -> JSON -> React State -> UI`

يعني MVT موجودة في backend، لكن الـ Template انتقلت إلى React. والـ Layered architecture واضحة لأن كل مسؤولية مفصولة في طبقة.

## 3. Backend: الملفات الأساسية

### `backendPBL/projectBPL/manage.py`

نقطة تشغيل أوامر Django. منه نشغل:

- `python manage.py runserver`
- `python manage.py migrate`
- `python manage.py createsuperuser`

هو يحدد إعدادات المشروع عبر:

`DJANGO_SETTINGS_MODULE = projectBPL.settings`

### `backendPBL/projectBPL/requirements.txt`

قائمة مكتبات backend:

- `Django`: إطار العمل.
- `djangorestframework`: بناء REST API.
- `djangorestframework-simplejwt`: JWT login tokens.
- `django-cors-headers`: السماح للـ frontend بالتواصل مع backend.
- `django-reversion`: حفظ نسخ من تعديلات المشاريع.
- `python-decouple`: لإدارة الإعدادات، لكنه غير مستخدم كثيرا حاليا في `settings.py`.

### `backendPBL/projectBPL/db.sqlite3`

قاعدة البيانات المحلية. ليست كودا، لكنها تحتوي البيانات الفعلية أثناء التطوير.

### `backendPBL/projectBPL/media/`

مجلد رفع الملفات. حاليا فيه ملفات starter code للمشاريع داخل `media/project_starters`.

### `backendPBL/projectBPL/projectBPL/settings.py`

إعدادات Django كلها:

- `INSTALLED_APPS`: يفعّل Django apps و DRF و CORS و JWT و apps المحلية.
- `DATABASES`: يستخدم SQLite.
- `AUTH_USER_MODEL = account.CustomUser`: يغير User الافتراضي إلى موديل مخصص.
- `REST_FRAMEWORK`: يحدد JWT authentication وأن أغلب endpoints تحتاج login افتراضيا.
- `SIMPLE_JWT`: أعمار access/refresh token.
- `CORS_ALLOW_ALL_ORIGINS = True`: يسمح للواجهة الأمامية بالطلبات أثناء التطوير.
- `MEDIA_URL` و `MEDIA_ROOT`: لإرجاع الملفات المرفوعة.

### `backendPBL/projectBPL/projectBPL/urls.py`

الراوتر الرئيسي للـ backend. يوزع الطلبات:

- `/admin/` إلى Django admin.
- `/api/account/` إلى تطبيق الحسابات.
- `/api/courses/` إلى تطبيق المسارات.
- `/api/projects/` إلى تطبيق المشاريع.
- `/api/progress/` إلى تطبيق التقدم.
- ويضيف خدمة ملفات `media` أثناء التطوير.

### `backendPBL/projectBPL/projectBPL/asgi.py` و `wsgi.py`

مداخل تشغيل Django على السيرفرات. في التطوير غالبا لا تعدلها.

## 4. تطبيق account

المسار: `backendPBL/projectBPL/account`

مسؤوليته: التسجيل، الدخول، الخروج، البروفايل، نوع المستخدم، وتحديد مستوى المتعلم بعد quiz.

### `account/models.py`

فيه:

- `CustomUserManager`: طريقة إنشاء المستخدمين والسوبر يوزر باستخدام email بدلا من username.
- `CustomUser`: موديل المستخدم المخصص.

أهم الحقول:

- `email`: هو حقل الدخول الأساسي.
- `user_type`: إما `learner` أو `admin`.
- `is_rated`: هل عمل اختبار مستوى.
- `level`: beginner/intermediate/advanced.
- `enrolled_courses_titles`: قائمة JSON لعناوين المسارات المنضم لها.

وفيه دوال مثل:

- `is_learner`
- `is_admin`
- `add_enrolled_course`
- `remove_enrolled_course`
- `is_enrolled_in_course`

### `account/serializers.py`

طبقة التحقق والتحويل:

- `RegisterLearnerSerializer`: يتحقق من email/password ويجبر النوع learner.
- `RegisterAdminSerializer`: نفس الفكرة لكن النوع admin.
- `LoginSerializer`: يتحقق من email/password ويعمل authenticate.
- `ProfileSerializer`: يرجع بيانات المستخدم، ويضيف معلومات المسارات للمتعلمين فقط.

### `account/views.py`

نقاط API للحساب:

- `RegisterLearnerView`: إنشاء متعلم + توليد JWT tokens.
- `RegisterAdminView`: إنشاء مشرف + توليد JWT tokens.
- `LoginView`: تسجيل الدخول + توليد tokens.
- `LogoutView`: يعمل blacklist للـ refresh token.
- `ProfileView`: عرض وتعديل البروفايل.
- `SubmitQuizView`: يحفظ مستوى المتعلم بعد الاختبار.

### `account/views_dashboard.py`

واجهات Dashboard للمتعلم:

- `LearnerDashboardView`: يرجع إحصائيات، مسارات، تقدم، إشعارات، نشاطات، ومشاريع مقترحة.
- `LearnerProgressAPIView`: يرجع تفاصيل تقدم المتعلم.

جزء من البيانات هنا محاكاة/fake stats، وجزء فعلي مثل اقتراح المشاريع حسب `user.level`.

### `account/urls.py`

يربط endpoints مثل:

- `/register/learner/`
- `/register/admin/`
- `/login/`
- `/logout/`
- `/profile/`
- `/quiz/submit/`
- `/learner/dashboard/`
- `/learner/progress/`

### `account/admin.py`, `apps.py`, `tests.py`, `migrations/`

- `admin.py`: يسجل `CustomUser` في Django admin.
- `apps.py`: تعريف التطبيق.
- `tests.py`: ملف اختبارات، حاليا شبه فارغ.
- `migrations/`: تاريخ إنشاء وتعديل جدول المستخدم.

## 5. تطبيق courses

المسار: `backendPBL/projectBPL/courses`

مسؤوليته: المسارات التعليمية، إنشاؤها وتعديلها وحذفها، وانضمام المتعلمين لها.

### `courses/models.py`

فيه موديل `Course`.

أهم الحقول:

- `title`, `description`
- `level`
- `category`
- `estimated_duration`
- `projects_count`
- `is_public`
- `instructor`: مشرف أنشأ المسار.
- `enrolled_learners`: علاقة ManyToMany مع المتعلمين.
- `is_active`: للحذف الناعم soft delete.

أهم الدوال:

- `save`: يمنع غير المشرف من إنشاء Course.
- `update_projects_count`: يحسب عدد المشاريع النشطة داخل المسار.
- `add_learner`: يضيف متعلم للمسار ويحدّث قائمة المستخدم.
- `remove_learner`
- `can_update_title`: يتحقق من عدم تكرار عنوان المسار.

### `courses/serializers.py`

فيه serializers حسب العملية:

- `CourseCreateSerializer`: تحقق إنشاء المسار.
- `CourseListSerializer`: بيانات مختصرة لقائمة المسارات.
- `CourseDetailSerializer`: تفاصيل مسار مع مشاريعه.
- `CourseUpdateSerializer`: تحقق تعديل المسار.
- `CourseEnrollmentSerializer`: تحقق انضمام المتعلم.

### `courses/views.py`

واجهات API:

- `CreateCourseView`: إنشاء مسار، للمشرف فقط.
- `UpdateCourseView`: تعديل مسار.
- `RetrieveCourseView`: جلب مسار للمشرف.
- `DeleteCourseView`: حذف ناعم بتغيير `is_active = False`.
- `ConfirmDeleteCourseView`: معلومات تأكيد قبل الحذف.
- `ListCoursesView`: للـ admin يرجع كل النشط، للـ learner يرجع public فقط.
- `CourseDetailView`: تفاصيل المسار ومشاريعه.
- `JoinCourseView`: انضمام متعلم.
- `UserEnrolledCoursesView`: مساراتي.
- `CheckEnrollmentView`: هل المتعلم منضم لهذا المسار؟

### `courses/urls.py`

يربط:

- `/api/courses/`
- `/api/courses/create/`
- `/api/courses/<id>/`
- `/api/courses/<id>/update/`
- `/api/courses/<id>/delete/`
- `/api/courses/<id>/details/`
- `/api/courses/<id>/join/`
- `/api/courses/my-courses/`

## 6. تطبيق projects

المسار: `backendPBL/projectBPL/projects`

مسؤوليته: المشاريع، ملفات البداية، المهام، تشغيل الكود، التسليمات، مراجعة المهام، وإصدارات المشروع.

### `projects/models.py`

فيه أربعة موديلات رئيسية:

#### `Project`

يمثل مشروع داخل Course.

أهم الحقول:

- `course`: المشروع تابع لأي مسار.
- `title`, `description`
- `requirements`, `objectives`, `resources`
- `estimated_time`
- `level`
- `language`
- `order`: ترتيب المشروع داخل المسار.
- `is_active`

الدالة `save` تعطي order تلقائيا إذا لم يحدد، وتحدث عدد المشاريع في المسار عند إنشاء مشروع جديد.

#### `ProjectStarterFile`

ملف بداية للمشروع، OneToOne مع Project، مثل ملف template أو starter code.

#### `ProjectTask`

مهمة داخل المشروع:

- نوعها `text` أو `code` أو `file`.
- فيها `expected_answer`, `hint`, `teaching`, `order`.

#### `TaskSubmission`

تسليم الطالب لمهمة معينة:

- `answer`
- `status`
- `is_completed`
- `admin_feedback`
- `is_correct`
- أوقات الحفظ والإكمال.

### `projects/serializers.py`

فيه:

- `ProjectCreateSerializer`: تحقق إنشاء المشروع وربطه بـ `course_id`.
- `ProjectListSerializer`: عرض مشاريع مختصر.
- `ProjectDetailSerializer`: تفاصيل مشروع، ويضيف starter file إن وجد.
- `ProjectUpdateSerializer`: تعديل المشروع.
- `ProjectDeleteConfirmationSerializer`: بيانات شاشة تأكيد الحذف.
- `ProjectStarterFileSerializer`: تحويل رابط الملف المرفوع.
- `ProjectTaskSerializer`: تحويل مهام المشروع.
- `TaskSubmissionSerializer`: تحويل تسليمات المهام.

### `projects/views.py`

هذا أكبر ملف في backend.

أهم الـ views:

- `CreateProjectView`: إنشاء مشروع.
- `ListProjectsView`: قائمة المشاريع مع فلترة اختيارية حسب `course_id`.
- `ProjectDetailView`: تفاصيل مشروع.
- `CourseProjectsView`: مشاريع مسار محدد.
- `UpdateProjectView`: تعديل مشروع.
- `DeleteProjectView`: حذف مشروع.
- `ConfirmDeleteProjectView`: تأكيد الحذف.
- `StartProjectView`: يبدأ مشروع للمتعلم، ويتأكد أن المتعلم منضم للمسار وأن المشاريع السابقة مكتملة.
- `UploadStarterFileView`: رفع starter file.
- `CreateProjectTaskView`: إنشاء مهمة.
- `ProjectTasksListView`: جلب مهام مشروع.
- `ProjectTaskDeleteView`: حذف مهمة.
- `ExecuteCodeView`: تشغيل كود الطالب داخل Docker.
- `SaveTaskSubmissionView`: حفظ إجابة المهمة.
- `GetTaskSubmissionView`: جلب إجابة محفوظة.
- `AdminTaskFeedbackView`: ملاحظات المشرف على مهمة.
- `AdminGetStudentSubmissionView`: جلب تسليم طالب لمهمة.
- `ProjectVersionHistoryView`: تاريخ نسخ المشروع عبر django-reversion.
- `ProjectRollbackView`: الرجوع لنسخة سابقة.

### `projects/urls.py`

يربط endpoints مثل:

- `/api/projects/create/`
- `/api/projects/<id>/`
- `/api/projects/<id>/update/`
- `/api/projects/<id>/start/`
- `/api/projects/<id>/starter-file/`
- `/api/projects/<project_id>/tasks/`
- `/api/projects/tasks/create/`
- `/api/projects/code/execute/`
- `/api/projects/tasks/<task_id>/save/`
- `/api/projects/tasks/<task_id>/feedback/`
- `/api/projects/versions/<project_id>/`
- `/api/projects/rollback/<project_id>/<version_id>/`

## 7. تطبيق progress

المسار: `backendPBL/projectBPL/progress`

مسؤوليته: تقدم الطالب على مستوى المشروع كاملا، وليس كل مهمة منفردة.

### `progress/models.py`

فيه `ProjectProgress`:

- `user`
- `project`
- `status`: not_started / in_progress / completed.
- `progress_percentage`
- `started_at`, `completed_at`
- `is_graded`, `feedback`, `grade_stars`

وفيه قيد `unique_together = (user, project)` حتى لا يوجد أكثر من progress لنفس الطالب ونفس المشروع.

### `progress/views.py`

فيه:

- `UserProjectProgressView`: يرجع تقدم كل مشاريع المستخدم.
- `CompleteProjectView`: يجعل المشروع completed.
- `ProjectProgressDetailView`: تفاصيل تقدم مشروع واحد.
- `AdminProjectSubmissionsView`: كل الطلاب الذين أكملوا مشروع معين.
- `AdminProjectReviewView`: تقييم نهائي من المشرف.
- `AdminSingleSubmissionView`: جلب تقييم طالب معين.

ملاحظة تقنية: في `AdminProjectReviewView` يستخدم `status.HTTP_400_BAD_REQUEST` لكن `status` غير مستورد من DRF في أعلى الملف. هذا قد يسبب خطأ عند هذا الفرع بالذات.

### `progress/urls.py`

يربط:

- `/api/progress/projects/`
- `/api/progress/projects/<project_id>/complete/`
- `/api/progress/projects/<project_id>/progress/`
- `/api/progress/projects/<project_id>/submissions/`
- `/api/progress/projects/<project_id>/review/`

## 8. Frontend: الملفات الأساسية

### `frontend/package.json`

تعريف مشروع React والحزم:

- `react`, `react-dom`
- `react-router-dom`: التنقل بين الصفحات.
- `axios`: طلبات HTTP.
- `@monaco-editor/react` و `monaco-editor`: محرر الأكواد.
- `vite`: dev server/build.

### `frontend/package-lock.json`

ملف مولد تلقائيا يثبت نسخ الحزم بدقة.

### `frontend/index.html`

قالب HTML الأساسي. فيه:

- `dir="rtl"` لأن الواجهة عربية.
- تحميل خط Cairo.
- `<div id="root"></div>` الذي يركب React داخله.

### `frontend/vite.config.js`

إعداد Vite:

- dev server على port `3000`.
- proxy من `/api` إلى `http://localhost:8000`.

لكن في `api.js` يوجد base URL مباشر `http://localhost:8000/api`، لذلك الـ proxy ليس أساسيا حاليا.

### `frontend/src/main.jsx`

نقطة دخول React. يركب `<App />` داخل `root`.

### `frontend/src/App.jsx`

الراوتر الرئيسي للواجهة.

يضع:

- `AuthProvider`
- `BrowserRouter`
- `Navbar`
- `Routes`

ويحمي الصفحات عبر `PrivateRoute`. صفحات admin تستخدم `requireAdmin`.

### `frontend/src/services/api.js`

طبقة الاتصال مع backend.

فيه:

- axios instance مع `baseURL = http://localhost:8000/api`.
- request interceptor يضيف `Authorization: Bearer <access_token>`.
- response interceptor إذا جاء 401 يحاول refresh token ثم يعيد الطلب.
- `accountAPI`: login/register/profile/dashboard/quiz.
- `coursesAPI`: list/get/create/update/delete/join/myCourses.
- `projectsAPI`: list/get/create/update/delete/start/tasks/execute/save/progress/review/versions/rollback.

هذا الملف هو طبقة API Client في الـ Layered architecture.

### `frontend/src/contexts/AuthContext.jsx`

يدير حالة المصادقة:

- يقرأ user و tokens من `localStorage`.
- `login`: يستدعي API ثم يحفظ tokens.
- `register`: نفس الفكرة.
- `logout`: يحذف tokens ويستدعي endpoint الخروج.
- يعطي `isAdmin` و `isLearner` لباقي المكونات.

### `frontend/src/components/PrivateRoute.jsx`

يحمي الصفحات:

- إذا لم يكن المستخدم مسجلا، يحوله إلى `/login`.
- إذا الصفحة تتطلب admin والمستخدم ليس admin، يحوله إلى `/dashboard`.

### `frontend/src/components/Navbar.jsx`

شريط التنقل. يغير الروابط حسب نوع المستخدم:

- غير مسجل: login/register.
- admin: لوحة تحكم، مسارات، إضافة مسار، مشاريع، إضافة مشروع.
- learner: لوحة تحكم، مسارات، مساراتي، مشاريع.

## 9. Frontend pages

### `Home.jsx`

صفحة البداية/التعريف. تعرض فكرة المنصة وخطوات التعلم وأمثلة مشاريع.

### `Login.jsx`

نموذج تسجيل الدخول:

- يأخذ email/password.
- يستدعي `login` من `AuthContext`.
- حسب `user_type` يوجه إلى `/admin/dashboard` أو `/dashboard`.

### `Register.jsx`

نموذج إنشاء حساب:

- email/password/password2.
- يتحقق في الواجهة من تطابق كلمة المرور وطولها.
- يستدعي `register` من `AuthContext`.

### `LearnerDashboard.jsx`

لوحة المتعلم:

- يستدعي `accountAPI.getLearnerDashboard`.
- يعرض الإحصائيات، المسارات المنضم لها، التقدم، الإشعارات، النشاطات، والمشاريع المقترحة.

### `AdminDashboard.jsx`

لوحة المشرف:

- يجلب courses و projects.
- يحسب عدد المسارات والمشاريع والمتعلمين.
- يعرض آخر المسارات والمشاريع وروابط سريعة للإضافة.

### `CoursesList.jsx`

قائمة المسارات:

- يجلب المسارات من `coursesAPI.list`.
- للمتعلم قد يعرض quiz إذا لم يكن محدد المستوى.
- للـ admin تظهر أزرار تعديل/حذف.

### `CourseDetail.jsx`

تفاصيل مسار:

- يجلب `coursesAPI.getDetails`.
- يعرض معلومات المسار والمشاريع داخله.
- المتعلم يستطيع الانضمام.
- admin يستطيع تعديل أو حذف.

### `CourseCreate.jsx`

نموذج إنشاء مسار للـ admin.

يرسل إلى `coursesAPI.create`.

### `CourseEdit.jsx`

نموذج تعديل مسار.

يجلب البيانات القديمة عبر `coursesAPI.get` ثم يرسل update.

### `MyCourses.jsx`

يعرض المسارات التي انضم لها المتعلم عبر `coursesAPI.myCourses`.

### `ProjectsList.jsx`

قائمة المشاريع:

- يجلب المشاريع عبر `projectsAPI.list`.
- يجلب تقدم المستخدم عبر `projectsAPI.getProgress`.
- يصنف المشاريع حسب الحالة: لم يبدأ، قيد التنفيذ، مكتمل.
- يدعم فلترة المستوى.

### `ProjectDetail.jsx`

تفاصيل المشروع:

- يجلب المشروع.
- للمتعلم يعرض حالة التقدم وزر بدء/متابعة المشروع.
- للـ admin يعرض التسليمات والتقييمات.
- يعرض starter file إن وجد.
- يعرض سجل الإصدارات وال rollback للمشرف.

### `ProjectCreate.jsx`

إنشاء مشروع:

- يختار course.
- يدخل بيانات المشروع.
- يمكن رفع starter file.
- يمكن إضافة tasks قبل الحفظ.
- بعد إنشاء المشروع، يرفع الملف وينشئ المهام.

### `ProjectEdit.jsx`

تعديل مشروع:

- يجلب بيانات المشروع والمهام.
- يعدل بيانات المشروع.
- يضيف أو يحذف tasks.

### `ProjectWork.jsx`

صفحة العمل على المشروع وهي أهم صفحة للمتعلم:

- تجلب مهام المشروع.
- تعرض sidebar للمهام.
- إذا المهمة `code` تعرض Monaco Editor.
- إذا المهمة `text` تعرض textarea.
- تحفظ الإجابات تلقائيا كل 5 ثوان عبر `saveTaskSubmission`.
- زر تشغيل الكود يستدعي `projectsAPI.executeCode`.
- عند آخر مهمة، `complete` يجعل المشروع مكتملا.

### `ProjectReview.jsx`

صفحة مراجعة المشرف لتسليم طالب:

- يجلب المشروع والمهام.
- يجلب إجابات الطالب.
- يسمح بكتابة feedback لكل task.
- يسمح بإرسال تقييم نهائي stars + feedback.

### `QuizComponent.jsx`

اختبار تحديد مستوى المتعلم:

- أسئلة ثابتة داخل الواجهة.
- يحسب score.
- يحول score إلى beginner/intermediate/advanced.
- يرسل المستوى عبر callback إلى صفحة المسارات.

## 10. ملفات CSS

الملفات مثل:

- `App.css`
- `index.css`
- `Auth.css`
- `Dashboard.css`
- `Courses.css`
- `Projects.css`
- `ProjectWork.css`
- `Quiz.css`
- `Navbar.css`
- `Form.css`
- `Profile.css`
- `Home.css`

كلها مسؤولة عن شكل الصفحات والمكونات، وليس منطق البيانات.

## 11. محرر الأكواد

المحرر مبني بـ Monaco Editor، نفس المحرك المستخدم في VS Code تقريبا.

المسار الرئيسي:

- Frontend: `frontend/src/pages/ProjectWork.jsx`
- Backend: `backendPBL/projectBPL/projects/views.py` داخل `ExecuteCodeView`
- API wrapper: `frontend/src/services/api.js` داخل `projectsAPI.executeCode`
- Docker image: `docker/python-runner/Dockerfile`

كيف يعمل:

1. المتعلم يفتح مشروع.
2. `ProjectWork.jsx` يجلب المهام.
3. إذا كانت المهمة من نوع `code` يظهر `<Editor />`.
4. الكود محفوظ في state اسمه `code`.
5. عند الضغط على تشغيل، يستدعي:

   `projectsAPI.executeCode(code, project.language)`

6. هذا يرسل POST إلى:

   `/api/projects/code/execute/`

7. backend يستقبل الكود ويكتبه في ملف مؤقت اسمه `main.py`.
8. يشغل Docker container.
9. يرجع `stdout` أو `stderr` إلى الواجهة.
10. الواجهة تعرض الخرج في `output-box`.

ملاحظة مهمة: الواجهة تمرر `project.language`، لكن backend حاليا يشغل Python فقط لأنه يكتب دائما `main.py` ويستخدم صورة `python-runner-image`.

## 12. لماذا استخدمنا Docker؟

استخدمنا Docker بسبب تشغيل كود المستخدم.

تشغيل كود الطالب مباشرة على السيرفر خطر لأن الطالب قد يكتب:

- loop لا نهائي.
- كود يقرأ ملفات السيرفر.
- كود يستخدم الشبكة.
- كود يستهلك RAM/CPU.

في `ExecuteCodeView` يتم تشغيل:

- `docker run --rm`
- mount للملف المؤقت إلى `/app`
- `--network none`: لا يوجد إنترنت.
- `--memory 100m`: حد RAM.
- `--cpus 0.5`: حد CPU.
- `timeout=5`: إيقاف التنفيذ الطويل.

وفي `Dockerfile`:

- يبدأ من `python:3.11-slim`.
- يحدد `WORKDIR /app`.
- ينشئ user اسمه `runner`.
- يشغل الكود كمستخدم غير root.
- الأمر الافتراضي `python3 main.py`.

قبل استخدام التشغيل يجب بناء الصورة:

```bash
cd docker/python-runner
docker build -t python-runner-image .
```

## 13. مسار request كامل: مثال login

1. المستخدم يكتب email/password في `Login.jsx`.
2. `handleSubmit` يستدعي `login` من `AuthContext`.
3. `AuthContext.login` يستدعي:

   `accountAPI.login(email, password)`

4. `api.js` يرسل:

   `POST http://localhost:8000/api/account/login/`

5. `projectBPL/urls.py` يحول `/api/account/` إلى `account.urls`.
6. `account/urls.py` يطابق `/login/` مع `LoginView`.
7. `LoginView.post` يستدعي `LoginSerializer`.
8. `LoginSerializer` يعمل validate و `authenticate`.
9. إذا صحيح، `LoginView` ينشئ JWT refresh/access.
10. يرجع JSON فيه user و tokens.
11. `AuthContext` يحفظ tokens و user في `localStorage`.
12. React يوجه المستخدم حسب نوعه.

## 14. مسار request كامل: مثال عرض المشاريع

1. `ProjectsList.jsx` يعمل `projectsAPI.list(courseId)`.
2. `api.js` يضيف Authorization header.
3. الطلب يصل إلى `/api/projects/`.
4. `projects/urls.py` يوجه إلى `ListProjectsView`.
5. DRF JWT يقرأ التوكن ويحدد `request.user`.
6. `ListProjectsView.get_queryset` يقرر:

   - admin يرى المشاريع النشطة كلها.
   - learner يرى مشاريع المسارات العامة فقط.

7. `ProjectListSerializer` يحول الـ QuerySet إلى JSON.
8. React يحفظ النتيجة في state ويعرض البطاقات.

## 15. مسار request كامل: تشغيل كود

1. الطالب يكتب كود في Monaco Editor.
2. يضغط زر تشغيل.
3. `ProjectWork.jsx` يستدعي `runCode`.
4. `runCode` يستدعي `projectsAPI.executeCode`.
5. POST إلى `/api/projects/code/execute/`.
6. `ExecuteCodeView` يأخذ `code`.
7. ينشئ TemporaryDirectory.
8. يكتب الكود في `main.py`.
9. يشغل Docker image.
10. Docker ينفذ `python3 main.py`.
11. backend يرجع `stdout`, `stderr`, `returncode`.
12. React يعرض الناتج.

## 16. ملفات ومجلدات لا تدرسها كسورس كود

- `frontend/node_modules`: مكتبات npm، مولدة.
- `backendPBL/projectBPL/venv`: بيئة Python، مولدة.
- `__pycache__`: ملفات Python compiled cache.
- `package-lock.json`: lock file مولد.
- `db.sqlite3`: قاعدة بيانات، ليست source code.
- `PBL.pdf`: ملف توثيق/عرض، ليس جزءا من التنفيذ.

## 17. ملاحظات مهمة أثناء الفهم

- المشروع ليس Django Templates، بل Django REST + React. لذلك لا تبحث عن HTML templates في backend.
- يوجد فصل جيد بين `views` و `serializers` و `models`، وهذا هو الجزء الأقرب للـ layered architecture.
- بعض منطق العمل موجود داخل `models.py` مثل `add_learner` و `update_projects_count`، وبعضه داخل `views.py` مثل بدء المشروع وتشغيل الكود. لذلك الطبقات موجودة لكن ليست صارمة 100%.
- Docker مستخدم فقط لتشغيل كود الطالب، وليس لتشغيل Django أو React.
- تشغيل أكثر من لغة برمجة غير مكتمل حاليا؛ Monaco يعرض لغة المشروع، لكن Docker backend ينفذ Python فقط.
- لم أستطع تشغيل `manage.py check` لأن Python داخل `venv` أعطى `Access is denied` على هذا الجهاز، و `python` غير موجود في PATH.

