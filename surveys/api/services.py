"""
Addtional Services for surveys when it comes to data linking.
"""
import pandas as pd
from surveys.models import (
    SurveyCategoryType,
    SurveyCategory,
    SurveyApplicationTitle,
    SurveyQuestion,
    SurveyAnswer,
    SurveyQuestionOption
)
from surveys.api.serializers import (
    SurveyCategoryTypeSerializer,
    SurveyApplicationTitleSerializer,
    SurveyCategorySerializer,
    SurveyAnswerLinkSerializer
)
from system_management.amazons3 import(
    open_s3_file
)


def get_survey_categories(df_survey: pd.DataFrame) -> pd.DataFrame:
    """Get survey categories.
    
    Args:
        df_survey (DataFrame): survey data
    
    Returns:
        DataFrame: survey categories
    """
    survey_id = df_survey['id'].values.tolist()[0]
    
    application_type_id = df_survey['application_type_id'].values.tolist()[0]
    
    categories = SurveyCategory.objects.filter(
        type_id=application_type_id
    )
    
    categories_serializer = SurveyCategorySerializer(categories, many=True)
    categories_data = categories_serializer.data
    df_categories = pd.DataFrame(categories_data)
    
    if not df_categories.empty:
        category_ids = df_categories['id'].values.tolist()
        
        category_types = SurveyCategoryType.objects.filter(
            category_id__in = category_ids
        )
        
        type_serializer = SurveyCategoryTypeSerializer(category_types, many=True)
        
        cat_type_data = type_serializer.data
        df_cat_type = pd.DataFrame(cat_type_data)
        
        if not df_cat_type.empty:
            cat_type_ids = df_cat_type['id'].values.tolist()
            application_title = SurveyApplicationTitle.objects.filter(
                subcategory_type_id__in = cat_type_ids
                )
            
            title_serializer =  SurveyApplicationTitleSerializer(application_title, many=True)
            title_data = title_serializer.data
            df_title = pd.DataFrame(title_data)
            
            if not df_title.empty:
                title_ids = df_title['id'].values.tolist()
                question =  SurveyQuestion.objects.values(
                    'id',
                    'question',
                    'question_type',
                    'is_mandatory',
                    'has_checkbox',
                    'has_selection',
                    'has_text',
                    'has_date',
                    'has_file',
                    'has_other_field',
                    'has_location',
                    'application_title_id'
                ).filter(
                    application_title_id__in =title_ids
                )

                df_questions = pd.DataFrame(question)
                df_questions = df_questions.assign(
                    options = '',
                    answers = ''
                )
                if question.exists():
                    question_ids = question.values_list('id', flat=True)
                    
                    options = SurveyQuestionOption.objects.values(
                        'id',
                        'option',
                        'question_id'
                    ).filter(
                        question_id__in = question_ids
                    )
                    
                    df_options = pd.DataFrame(options)
                    
                    if options.exists():
                        df_questions['options'] = df_questions['id'].apply(
                            lambda question_id:
                                df_options.loc[
                                    df_options['question_id'] == question_id
                                ].to_dict('records')
                        )
                    
                    answer = SurveyAnswer.objects.values(
                        'id', 
                        'answer', 
                        'question_id', 
                        'question__question_type', 
                        'survey_id'
                    ).filter(
                        question_id__in = question_ids,
                        survey_id = survey_id
                    )
                    
                    df_answer = pd.DataFrame(answer)
                    if answer.exists():
                        df_answer = df_answer.apply(
                            lambda series:
                            open_file_questions(series)
                            ,axis=1
                        )

                        df_questions['answers'] = df_questions['id'].apply(
                                lambda question_id:
                                    df_answer.loc[
                                        df_answer['question_id'] == question_id
                                    ].to_dict('records')
                        )
                    
                    df_title['questions'] = df_title['id'].apply(
                        lambda title_id:
                            df_questions.loc[
                                df_questions['application_title_id'] == title_id
                        ].to_dict('records')
                    )      
            
                df_cat_type ['titles'] = df_cat_type['id'].apply(
                        lambda category_type:
                            df_title.loc[
                                df_title['subcategory_type_id'] == category_type
                            ].to_dict('records')
                )
            
            df_categories['types'] = df_categories['id'].apply(
                lambda category:
                    df_cat_type .loc[
                        df_cat_type['category_id'] == category
                    ].to_dict('records')
            )

        df_survey['categories'] = df_survey['application_type_id'].apply(
            lambda application_type:
            df_categories.loc[
                df_categories['type_id'] == application_type
            ].to_dict('records')
        )
    return df_survey


def open_file_questions(series: pd.Series) -> pd.Series:
    """
    Open file questions.
    
    Args:
        series (Series): series
    
    Returns:
        Series: series
    """
    if series['question__question_type'] == 'file':
        series['answer'] = open_s3_file(series['answer'])
    return series


def open_file_series(series: pd.Series) -> pd.Series:
    """
    Open file questions.
    
    Args:
        series (Series): series
    
    Returns:
        Series: series
    """
    if series['question']['question_type'] == 'file':
        series['answer'] = open_s3_file(series['answer'])
    return series


def get_survey_answers(df_surveys: pd.DataFrame) -> pd.DataFrame:
    """
    Get survey answers.
    
    Args:
        df_surveys (DataFrame): survey data
    
    Returns:
        DataFrame: survey answers
    """
    survey_ids = df_surveys['id'].values.tolist()
    answers = SurveyAnswer.objects.filter(
        survey_id__in = survey_ids
    )

    serializer = SurveyAnswerLinkSerializer(answers, many=True)
    
    df_answers = pd.DataFrame(serializer.data)
    df_surveys = df_surveys.assign(
        categories = ''
    )
    if not df_answers.empty:
        df_surveys = df_surveys.apply(
            lambda series:
            get_answer_category(
                series,
                df_answers
            )
            ,axis=1
        )
    return df_surveys
    

def get_answer_category(
        series: pd.Series,
        df_answers: pd.DataFrame
        ) -> pd.Series:
    """
    Get answer category.
    
    Args:
        series (Series): series
        df_answers (DataFrame): survey answers
        df_options (DataFrame): survey options
    
    Returns:
        Series: series
    """
    df_answers = df_answers.loc[
        df_answers['survey_id'] == series['id']
    ]
    
    df_categories = pd.DataFrame(
        df_answers['category'].values.tolist()
    ).drop_duplicates()
    
    df_types = pd.DataFrame(
        df_answers['subcategory_type'].values.tolist()
    ).drop_duplicates()
    
    df_titles = pd.DataFrame(
        df_answers['application_title'].values.tolist()
    ).drop_duplicates()
    
    df_question = pd.DataFrame(
        df_answers['question'].values.tolist()
    )

    df_categories = df_categories.assign(
        types = ''
    )
    series['categories'] = ''
    
    if not df_answers.empty:

        if not df_types.empty:
            
            df_types = df_types.assign(
                titles = ''
            )

            if not df_titles.empty:
                df_answers = df_answers.apply(
                    lambda answer:
                    open_file_series(answer),
                    axis=1
                )

                df_answers = df_answers[['id', 'answer', 'question_id']]
                df_question['answers'] = df_question['id'].apply(
                    lambda question_id:
                    df_answers.loc[
                        df_answers['question_id'] == question_id
                    ].to_dict('records')
                )

                df_titles['questions'] = df_titles['id'].apply(
                    lambda title_id:
                    df_question.loc[
                        df_question['application_title_id'] == title_id
                    ].to_dict('records')
                )

                df_types['titles'] = df_types['id'].apply(
                    lambda type_id:
                    df_titles.loc[
                        df_titles['subcategory_type_id'] == type_id
                    ].to_dict('records')
                )

            df_categories['types'] = df_categories['id'].apply(
                lambda category_id:
                df_types.loc[
                    df_types['category_id'] == category_id
                ].to_dict('records')
            )
        
            series['categories'] = df_categories.to_dict('records')
    
    return series

def get_application_type_info(df_application_types: pd.DataFrame) -> pd.DataFrame:
    """
    Get application type info.
    
    Args:
        df_application_types (DataFrame): application types
    
    Returns:
        DataFrame: application type info
    """
    application_type_ids = df_application_types['id'].values.tolist()
    categories = SurveyCategory.objects.filter(
        type_id__in = application_type_ids
    )
    
    categories_serializer = SurveyCategorySerializer(categories, many=True)
    categories_data = categories_serializer.data
    df_categories = pd.DataFrame(categories_data)
    
    if not df_categories.empty:
        category_ids = df_categories['id'].values.tolist()
        
        category_types = SurveyCategoryType.objects.filter(
            category_id__in = category_ids
        )
        
        type_serializer = SurveyCategoryTypeSerializer(category_types, many=True)
        
        cat_type_data = type_serializer.data
        df_cat_type = pd.DataFrame(cat_type_data)
        
        if not df_cat_type.empty:
            df_cat_type['tab_name'] = df_cat_type['name'].apply(
                lambda name:
                str(name).replace(' ', '_')
            )
            cat_type_ids = df_cat_type['id'].values.tolist()
            application_title = SurveyApplicationTitle.objects.filter(
                subcategory_type_id__in = cat_type_ids
                )
            
            title_serializer =  SurveyApplicationTitleSerializer(application_title, many=True)
            title_data = title_serializer.data
            df_title = pd.DataFrame(title_data)
            
            if not df_title.empty:
                title_ids = df_title['id'].values.tolist()
                question =  SurveyQuestion.objects.values(
                    'id',
                    'question',
                    'question_type',
                    'is_mandatory',
                    'has_checkbox',
                    'has_selection',
                    'has_text',
                    'has_date',
                    'has_file',
                    'has_other_field',
                    'has_location',
                    'application_title_id'
                ).filter(
                    application_title_id__in =title_ids
                )

                df_questions = pd.DataFrame(question)
                df_questions = df_questions.assign(
                    options = '',
                    answers = ''
                )
                if question.exists():
                    question_ids = question.values_list('id', flat=True)
                    
                    options = SurveyQuestionOption.objects.values(
                        'id',
                        'option',
                        'question_id'
                    ).filter(
                        question_id__in = question_ids
                    )
                    
                    df_options = pd.DataFrame(options)
                    
                    if options.exists():
                        df_questions['options'] = df_questions['id'].apply(
                            lambda question_id:
                                df_options.loc[
                                    df_options['question_id'] == question_id
                                ].to_dict('records')
                        )
                    
                    df_title['questions'] = df_title['id'].apply(
                        lambda title_id:
                            df_questions.loc[
                                df_questions['application_title_id'] == title_id
                        ].to_dict('records')
                    )      
            
                df_cat_type ['titles'] = df_cat_type['id'].apply(
                        lambda category_type:
                            df_title.loc[
                                df_title['subcategory_type_id'] == category_type
                            ].to_dict('records')
                )
            
            df_categories['types'] = df_categories['id'].apply(
                lambda category:
                    df_cat_type .loc[
                        df_cat_type['category_id'] == category
                    ].to_dict('records')
            )
        
        df_application_types['categories'] = df_application_types['id'].apply(
            lambda application_type:
            df_categories.loc[
                df_categories['type_id'] == application_type
            ].to_dict('records')
        )

    return df_application_types
