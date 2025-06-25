# Импорт необходимых модулей и классов
from rest_framework import serializers  # Основной модуль для создания сериализаторов Django REST Framework

# Импорт моделей и валидаторов из приложения task
from task.models import (
    Category,
    File,
    Link,
    Location,
    Space,
    Status,
    Task,
    TaskLink,
    validate_notifications,
    validate_reminders,
    validate_status_settings,
    validate_time_intervals,
)


# Сериализатор для модели Space (рабочее пространство)
class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space  # Указываем модель, которую будем сериализовывать
        fields = '__all__'  # Включаем все поля модели в сериализатор
        read_only_fields = ['id', 'created_at']  # Поля, которые нельзя изменять при создании/обновлении

# Сериализатор для модели Status (статус задачи)
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ['id']  # ID нельзя изменять

# Сериализатор для модели Location (локация)
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['id']

# Сериализатор для модели Link (ссылка)
class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'
        read_only_fields = ['id']

# Сериализатор для модели File (файл)
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ['id']

# Сериализатор для модели Category (категория)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']

# Сериализатор для промежуточной модели TaskLink (связь задачи и ссылки)
class TaskLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLink
        fields = '__all__'
        read_only_fields = ['id']

# Главный сериализатор для модели Task (задача)
class TaskSerializer(serializers.ModelSerializer):
    # Определение полей для связей с другими моделями
    
    # Связь со статусом (внешний ключ)
    status = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(),  # Источник данных для выбора
        allow_null=True  # Разрешение null значения
    )
    
    # Связь с локацией
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), 
        allow_null=True
    )
    
    # Связь с исполнителем (пользователем)
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=Task._meta.get_field('assignee').remote_field.model.objects.all(),  # Автоматическое определение модели пользователя
        allow_null=True
    )
    
    # Связь с зависимостями (многие-ко-многим с самой моделью Task)
    dependencies = serializers.PrimaryKeyRelatedField(
        many=True,  # Указание на множественную связь
        queryset=Task.objects.all()  # Источник данных
    )
    
    # Связь с категориями
    categories = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Category.objects.all()
    )
    
    # Связь со ссылками
    links = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Link.objects.all()
    )
    
    # Вычисляемые поля (только для чтения)
    calculated_progress_dependencies = serializers.IntegerField(read_only=True)  # Прогресс зависимостей
    calculated_is_ready = serializers.BooleanField(read_only=True)  # Готовность задачи к выполнению
    
    # Поля с JSON-данными и валидацией
    time_intervals = serializers.JSONField(
        validators=[validate_time_intervals],  # Кастомный валидатор
        required=False  # Не обязательное поле
    )
    reminders = serializers.JSONField(
        validators=[validate_reminders],
        required=False
    )
    notifications = serializers.JSONField(
        validators=[validate_notifications],
        required=False
    )
    status_settings = serializers.JSONField(
        validators=[validate_status_settings],  # Валидатор для настроек статуса
        required=False
    )
    
    # Поле для работы с тегами (только для чтения)
    tags = serializers.SerializerMethodField()  # Специальное поле, значение которого определяется методом

    # Метод для получения списка тегов
    def get_tags(self, obj):
        return list(obj.tags.names())  # Преобразует QuerySet тегов в список имен

    class Meta:
        model = Task  # Основная модель для сериализатора
        fields = [  # Явное перечисление всех включаемых полей
            'id', 'task_name', 'description', 'priority', 'status', 
            'progress', 'created_at', 'updated_at', 'start_date', 
            'end_date', 'deadline', 'deleted_at', 'dependencies', 
            'categories', 'location', 'author', 'last_editor', 
            'assignee', 'complexity', 'risk_level', 'is_ready', 
            'is_recurring', 'needs_approval', 'is_template', 
            'is_deleted', 'estimated_duration', 'actual_duration', 
            'quality_rating', 'budget', 'cancel_reason', 
            'time_intervals', 'reminders', 'repeat_interval', 
            'next_activation', 'tags', 'notifications', 'links',
            'task_space', 'calculated_progress_dependencies', 
            'calculated_is_ready'
        ]
        read_only_fields = [  # Поля, недоступные для записи
            'id', 'created_at', 'updated_at', 'deleted_at',
            'author', 'last_editor', 'calculated_progress_dependencies',
            'calculated_is_ready'
        ]

    # Кастомная логика создания новой задачи
    def create(self, validated_data):
        
        # Извлечение данных для связей "многие-ко-многим"
        dependencies = validated_data.pop('dependencies', [])  # Зависимости
        categories = validated_data.pop('categories', [])  # Категории
        links = validated_data.pop('links', [])  # Ссылки
        
        # Установка автора задачи (текущий пользователь)
        user = self.context['request'].user
        validated_data['author'] = user
        
        # Создание основной задачи
        task = Task.objects.create(**validated_data)
        
        # Установка связей после создания задачи
        task.dependencies.set(dependencies)
        task.categories.set(categories)
        task.links.set(links)
        
        return task

    # Кастомная логика обновления существующей задачи
    def update(self, instance, validated_data):
        
        # Извлечение данных для связей "многие-ко-многим"
        dependencies = validated_data.pop('dependencies', None)
        categories = validated_data.pop('categories', None)
        links = validated_data.pop('links', None)
        
        # Установка последнего редактора (текущий пользователь)
        user = self.context['request'].user
        instance.last_editor = user
        
        # Обновление атрибутов задачи
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Обновление связей (если предоставлены новые значения)
        if dependencies is not None:
            instance.dependencies.set(dependencies)
        if categories is not None:
            instance.categories.set(categories)
        if links is not None:
            instance.links.set(links)
        
        # Сохранение изменений
        instance.save()
        return instance