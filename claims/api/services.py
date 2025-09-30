
"""
Additional functions for claim api that link data together.
"""
import pandas as pd
from claims.api.serializers import (
    AssessmentModelSerializer,
    CauseCategoryModelSerializer,
    HowCategoryModelSerializer,
    WhatCategoryModelSerializer
)
from claims.models import (
    WhatCategory,
    CauseCategory,
    HowCategory,
    HowQuestionTitle,
    HowQuestionOption,
    HowQuestion,
    WhatQuestionTitle,
    WhatQuestionOption,
    WhatQuestion,
    ApplicationCause,
    ApplicationHow,
    ApplicationWhat,
    AssessmentNote,
    HowQuestionAnswer,
    WhatQuestionAnswer,
    Claim
)
from system_management.amazons3 import(
    open_s3_file
)
from application.models import (
    Assessment
)


def application_link_data(df_types: pd.DataFrame) -> pd.DataFrame:
    """
    Application Type Categories and questions
    
    Args:
        df_types (DataFrame): application type data
    
    Returns:
        DataFrame: application type categories
    """
    df_types = df_types.assign(
        categories = ''
    )
    if not df_types.empty:
        categories = CauseCategory.objects.values(
            'id',
            'name',
            'application_type_id'
        ).filter(
            application_type_id__in = df_types['id'].values.tolist()
        )
        how_categories = HowCategory.objects.values(
            'id',
            'name',
            'cause_id'
        ).filter(
            cause_id__in = categories.values_list('id', flat=True)
        )
        what_categories = WhatCategory.objects.values(
            'id',
            'name',
            'cause_id'
        ).filter(
            cause_id__in = categories.values_list('id', flat=True)
        )
        df_cause = pd.DataFrame(categories)
        df_cause = df_cause.assign(
            what_category = '',
            how_category = ''
        )
        if categories.exists():
            df_what = pd.DataFrame(what_categories)
            df_what = df_what.assign(
                titles = ''
            )
            if what_categories.exists():
                df_what = get_what_question_title(df_what)
                df_cause['what_category'] = df_cause['id'].apply(
                    lambda cause_id:
                    df_what.loc[
                        df_what['cause_id'] == cause_id
                    ].to_dict('records')
                )

            df_how = pd.DataFrame(how_categories)
            if how_categories.exists():
                df_how = get_how_question_title(df_how)
                df_cause['how_category'] = df_cause['id'].apply(
                    lambda cause_id:
                    df_how.loc[
                        df_how['cause_id'] == cause_id
                    ].to_dict('records')
                )
        
            df_types['categories'] = df_types['id'].apply(
                lambda type_id:
                df_cause.loc[
                    df_cause['application_type_id'] == type_id
                ].to_dict('records')
            )
        
    return df_types


def get_what_question_title(df_what: pd.DataFrame) -> pd.DataFrame:
    """
    What Question Section
    
    Args:
        df_what (DataFrame): what category data
    
    Returns:
        DataFrame: what category question titles
    """
    
    question_titles = WhatQuestionTitle.objects.values(
        'id',
        'title',
        'what_id'
    ).filter(
       what_id__in =  df_what['id'].values.tolist()
    )
    
    df_titles = pd.DataFrame(question_titles)
    df_titles = df_titles.assign(
        questions = ''
    )
    if question_titles.exists():
        df_titles = get_what_questions_link(df_titles)

        df_what['titles'] = df_what['id'].apply(
            lambda what_id:
            df_titles.loc[
                df_titles['what_id'] == what_id
            ].to_dict('records')
        )

    return df_what


def get_what_questions_link(df_titles: pd.DataFrame) -> pd.DataFrame:
    """
    What Question section
    
    Args:
        df_what (DataFrame): what question title data
    
    Returns:
        DataFrame: what category questions
    """
    question = WhatQuestion.objects.values(
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
        'what_title_id'
    ).filter(
        what_title_id__in = df_titles['id'].values.tolist()
    )
    options = WhatQuestionOption.objects.values(
        'id',
        'option',
        'question_id'
    ).filter(
        question_id__in = question.values_list('id', flat=True)
    )
    df_question = pd.DataFrame(question)
    df_question = df_question.assign(
        options = ''
    )

    if question.exists(): 
        df_question['options'] = df_question['id'].apply(
            lambda question_id:
            list(options.filter(question_id = question_id))
        )
    
        df_titles['questions'] = df_titles['id'].apply(
            lambda what_title_id:
            df_question.loc[
                df_question['what_title_id'] == what_title_id
            ].to_dict('records')
        )

    return df_titles


def get_how_question_title(df_how: pd.DataFrame) -> pd.DataFrame:
    """
    How Question Section
    
    Args:
        df_how (DataFrame): how category data
    
    Returns:
        DataFrame: how category question titles
    """
    
    question_titles = HowQuestionTitle.objects.values(
        'id',
        'title',
        'how_id'
    ).filter(
       how_id__in =  df_how['id'].values.tolist()
    )
    
    df_titles = pd.DataFrame(question_titles)
    df_titles = df_titles.assign(
        questions = ''
    )
    if question_titles.exists():
        df_titles = get_how_questions_link(df_titles)

        df_how['titles'] = df_how['id'].apply(
            lambda how_id:
            df_titles.loc[
                df_titles['how_id'] == how_id
            ].to_dict('records')
        )

    return df_how


def get_how_questions_link(df_titles: pd.DataFrame) -> pd.DataFrame:
    """
    How Question section
    
    Args:
        df_how (DataFrame): how question title data
    
    Returns:
        DataFrame: how category questions
    """
    question = HowQuestion.objects.values(
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
        'how_title_id'
    ).filter(
        how_title_id__in = df_titles['id'].values.tolist()
    )
    options = HowQuestionOption.objects.values(
        'id',
        'option',
        'question_id'
    ).filter(
        question_id__in = question.values_list('id', flat=True)
    )
    df_question = pd.DataFrame(question)
    df_question = df_question.assign(
        options = ''
    )

    if question.exists(): 
        df_question['options'] = df_question['id'].apply(
            lambda question_id:
            list(options.filter(question_id = question_id))
        )
    
        df_titles['questions'] = df_titles['id'].apply(
            lambda how_title_id:
            df_question.loc[
                df_question['how_title_id'] == how_title_id
            ].to_dict('records')
        )

    return df_titles


def get_claim_info_service(df_claim: pd.DataFrame) -> pd.DataFrame:
    """
    Claim info service for linked data to a claim
    
    Args:
        df_claim (DataFrame): claim application data
    
    Returns:
        DataFrame: info linked to claim
    """
    claim_id_list = df_claim['id'].values.tolist()

    how = ApplicationHow.objects.values(
        'claim_id',
        'how_id',
        'how_id__name'
    ).filter(
        claim_id__in = claim_id_list
    )

    df_claim = df_claim.assign(
        application_how = '',
        application_what = '',
        application_cause = '',
        questions = ''
    )
    df_claim['application_how'] = df_claim['id'].apply(
        lambda claim_id:
        how.first()
        if how.filter(claim_id = claim_id).exists()
        else
        ''
    )

    what = ApplicationWhat.objects.values(
        'claim_id',
        'what_id',
        'what_id__name'
    ).filter(
        claim_id__in = claim_id_list
    )

    df_claim['application_what'] = df_claim['id'].apply(
        lambda claim_id:
        what.first()
        if what.filter(claim_id = claim_id).exists()
        else
        ''
    )
    
    cause = ApplicationCause.objects.values(
        'claim_id',
        'cause_id',
        'cause_id__name'
    ).filter(
        claim_id__in = claim_id_list
    )
    
    df_claim['application_cause'] = df_claim['id'].apply(
        lambda claim_id:
        cause.first()
        if cause.filter(claim_id = claim_id).exists()
        else
        ''
    )
    df_claim = get_claim_details(df_claim)
    df_claim = get_claim_notes(df_claim)
    return df_claim


def get_claim_details(df_claim: pd.DataFrame) -> pd.DataFrame:
    """
    Get claim questions for how and what categories
        
    Args:
        df_claim (DataFrame): claim application data
    
    Returns:
        DataFrame: Questions based on how and what category
    """
    claim_id_list = df_claim['id'].values.tolist()
    what_category = ApplicationWhat.objects.values(
        'what_id',
        'claim_id'
    ).filter(
        claim_id__in = claim_id_list
    )

    how_category = ApplicationHow.objects.values(
        'how_id',
        'claim_id'
    ).filter(
        claim_id__in = claim_id_list
    )
            
    what_questions =  get_claim_detail_what(claim_id_list, what_category)
    how_questions =  get_claim_detail_how(claim_id_list, how_category)
    
    if not what_questions.empty and how_questions.empty:
        df_claim['details'] = df_claim['id'].apply(
            lambda claim_id:
            {
                'what_questions':what_questions.loc[
                    what_questions['what_id'] == what_category.first()['what_id']
                ].to_dict('records'),
                'how_questions':''
            }
            if what_category.filter(claim_id = claim_id).exists()
            else
            {
                'what_questions':'',
                'how_questions':''
            }
        )
    elif what_questions.empty and not how_questions.empty:
        df_claim['details'] = df_claim['id'].apply(
            lambda claim_id:
            {
                'what_questions':'',
                'how_questions':how_questions.loc[
                    how_questions['how_id'] == how_category.first()['how_id']
                ].to_dict('records')
            }
            if how_category.filter(claim_id = claim_id).exists()
            else
            {
                'what_questions':'',
                'how_questions':''
            }
        )
    elif not what_questions.empty and not how_questions.empty:    
        df_claim['details'] = df_claim['id'].apply(
            lambda claim_id:
            {
                'what_questions':what_questions.loc[
                    what_questions['what_id'] == what_category.first()['what_id']
                ].to_dict('records'),

                'how_questions':how_questions.loc[
                    how_questions['how_id'] == how_category.first()['how_id']
                ].to_dict('records')
            }
            if how_category.filter(claim_id = claim_id).exists() and \
                what_category.filter(claim_id = claim_id).exists()
            else
            {
                'what_questions':'',
                'how_questions':''
            }
        )
    return df_claim


def get_claim_detail_what(claim_id_list, what_category) -> pd.DataFrame:
    """
    Get the assigned what category questions
    
    Args:
        claim_id_list: claim ids
        what_category: Selected claim what categroy
    
    Returns:
        DataFrame: Questions based what selection
    """
    if what_category.exists():
        what_category = what_category.values_list('what_id', flat=True)
            
        what_titles = WhatQuestionTitle.objects.values(
            'id',
            'title',
            'what_id'
        ).filter(
            what_id__in = what_category
        )
        
        df_what_titles = pd.DataFrame(what_titles)
                    
        df_what_titles = df_what_titles.assign(
            questions = ''
        )

        if not df_what_titles.empty:
            what_questions = WhatQuestion.objects.values(
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
                'what_title_id'
            ).filter(
                what_title__in = what_titles.values_list('id', flat=True)
            )
            
            df_questions = pd.DataFrame(what_questions)
            
            if not df_questions.empty:
                what_options = WhatQuestionOption.objects.values(
                    'id',
                    'option',
                    'question_id'
                ).filter(
                    question_id__in = what_questions.values_list('id', flat=True)
                )

                what_answers = WhatQuestionAnswer.objects.values(
                    'id', 
                    'answer', 
                    'claim_id', 
                    'question_id',
                ).filter(
                    claim_id__in = claim_id_list,
                    question_id__in = what_questions.values_list('id', flat=True)

                )

                df_questions = df_questions.assign(
                    options = '',
                    answer = ''
                )

                df_questions = df_questions.apply(
                    lambda row:
                        assign_what_question(row, what_options, what_answers)
                    ,axis=1   
                )

                df_what_titles['questions'] = df_what_titles['id'].apply(
                    lambda title_id:
                    df_questions.loc[
                        df_questions['what_title_id'] == title_id
                    ].to_dict('records')
                )

            what_questions = df_what_titles

    else:
        what_questions = pd.DataFrame()
    
    return what_questions


def get_claim_detail_how(claim_id_list, how_category) -> pd.DataFrame:
    """
    Get the assigned how category questions
    
    Args:
        claim_id_list: claim ids
        what_category: Selected claim how categroy
    
    Returns:
        DataFrame: Questions based how selection
    """
    if how_category.exists():
        how_category = how_category.values_list('how_id', flat=True)
        
        how_titles = HowQuestionTitle.objects.values(
            'id',
            'title',
            'how_id'
        ).filter(
            how_id__in = how_category
        )

        df_how_titles = pd.DataFrame(how_titles)
        
        df_how_titles = df_how_titles.assign(
            questions = ''
        )

        if not df_how_titles.empty:
            how_questions = HowQuestion.objects.values(
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
                'how_title_id'
            ).filter(
                how_title_id__in = how_titles.values_list('id', flat=True)
            )
            
            df_questions = pd.DataFrame(how_questions)
            
            if not df_questions.empty:
                how_options = HowQuestionOption.objects.values(
                    'id',
                    'option',
                    'question_id'
                ).filter(
                    question_id__in = how_questions.values_list('id', flat=True)
                )
                how_answers = HowQuestionAnswer.objects.values(
                    'id', 
                    'answer', 
                    'claim_id', 
                    'question_id',
                ).filter(
                    claim_id__in = claim_id_list,
                    question_id__in = how_questions.values_list('id', flat=True)
                )

                df_questions = df_questions.assign(
                    options = '',
                    answer = ''
                )

                df_questions = df_questions.apply(
                    lambda row:
                        assign_how_question(row, how_options, how_answers)
                    ,axis=1   
                )
                    
                df_how_titles['questions'] = df_how_titles['id'].apply(
                    lambda title_id:
                    df_questions.loc[
                        df_questions['how_title_id'] == title_id
                    ].to_dict('records')
                )

            how_questions = df_how_titles

    else:
        how_questions = pd.DataFrame()

    return how_questions


def assign_how_question(row, how_options, how_answers):
    """
    Assign how question.

    :param row:
        row object
    :param how_options:
        how options data
    :param how_answers:
        how answers data
    :return:
        row object
    """

    how_options = how_options.filter(
        question_id = row['id']
    )
    if how_options.exists():
        row['options'] = list(how_options.values('id', 'option'))
    else:
        row['options'] = ''

    how_answers = how_answers.filter(
        question_id = row['id']
    )

    if how_answers.exists():
        answer_list = list(how_answers.values('id', 'answer'))
        if row['question_type'] == 'file':
            answer_list[0]['answer'] = open_s3_file(answer_list[0]['answer'])
        elif row['question_type'] == 'date':
            answer_list[0]['answer'] = str(answer_list[0]['answer']).replace('T', ' ')
        row['answer'] = answer_list

    else:
        row['answer'] = ''

    return row


def assign_what_question(row, what_options, what_answers):
    """
    Assign what question.

    :param row:
        row object
    :param what_options:
        what options data
    :param what_answers:
        what answers data
    :return:
        row object
    """
    what_options = what_options.filter(
        question_id = row['id']
    )
    if what_options.exists():
        row['options'] = list(what_options.values('id', 'option'))
    else:
        row['options'] = []

    what_answers = what_answers.filter(
        question_id = row['id']
    )

    if what_answers.exists():
        answer_list = list(what_answers.values('id', 'answer'))
        if row['question_type'] == 'file':
            answer_list[0]['answer'] = open_s3_file(answer_list[0]['answer'])
        elif row['question_type'] == 'date':
            answer_list[0]['answer'] = str(answer_list[0]['answer']).replace('T', ' ')
        row['answer'] = answer_list
    
    else:
        row['answer'] = []
    return row


def get_claim_notes(df_claim: pd.DataFrame) -> pd.DataFrame:
    """
    Get claim assessment notes
    
    Args:
        df_claim (DataFrame): claim application data
    
    Returns:
        DataFrame: Notes that are uploaded for the selected claim
    """
    claim_id_list = df_claim['id'].values.tolist()
    assessment_note = list(AssessmentNote.objects.values(            
        'id', 
        'note', 
        'file',  
        'claim_id',
        'assessment_id'
    ).filter(
        claim_id__in = claim_id_list
    ))

    df_assessment_note = pd.DataFrame(
        assessment_note
    )

    if not df_assessment_note.empty:
        df_assessment_note['file'] = df_assessment_note['file'].apply(
            lambda file: open_s3_file(file)
        )
        df_claim['notes'] = df_claim['id'].apply(
            lambda claim_id:
            df_assessment_note.loc[
                df_assessment_note['claim_id'] == claim_id
            ].to_dict('records')
        )

    return df_claim


def get_preview_report_info(df_application: pd.DataFrame) -> pd.DataFrame:
    """
    Preview data for application claims and their info
    
    Args:
        df_application (DataFrame): application data
    
    Returns:
        DataFrame: Application link information
    """
    application_id_list = df_application['id'].values.tolist()
    assessment = Assessment.objects.values(
            "id",
            "message",
            "scheduled_date_time",
            "end_date_time",
            "event_id",
            "summary",
            "video_link",
            "client_location",
            "application_id"
    ).filter(
        application_id__in = application_id_list
    )
    assessment_serializer = AssessmentModelSerializer(
        assessment, 
        many=True
    )
    df_assessment = pd.DataFrame(assessment_serializer.data)


    df_application = df_application.assign(
        assessment = '',
        claims = ''
    )

    if assessment.exists():
        df_application['assessment'] = df_application['id'].apply(
            lambda application_id:
            df_assessment.loc[
                df_assessment['application_id'] == application_id
            ].to_dict('records')
        )
    
    claims = Claim.objects.values(
        'id',
        'application_type_id',
        'application_type__name',
        'application_id'        
    ).filter(
        application_id__in = application_id_list
    )

    df_claims = pd.DataFrame(claims)
    df_claims = get_claim_info_service(df_claims)
    if not df_claims.empty:
        df_application['claims'] = df_application['id'].apply(
            lambda application_id:
            df_claims.loc[
                df_claims['application_id'] == application_id
            ].to_dict('records')
        )
    return df_application


def get_claim_categories(df_claim: pd.DataFrame):
    """
    Get categories selected for the claim
    
    Args:
        df_claim (DataFrame): claim application data
    
    Returns:
        DataFrame: Claim Categories linked on selected cause.
    """
    claim_id = df_claim['id'].values.tolist()[0]
    application_type_id = df_claim['application_type_id'].values.tolist()[0]
    cause = ApplicationCause.objects.values(
        'claim_id',
        'cause_id',
        'cause_id__name'
    ).filter(
        claim_id = claim_id
    )
    
    causes = CauseCategory.objects.filter(
        application_type_id = application_type_id
    )
    cause_serializer = CauseCategoryModelSerializer(causes, many=True)
    
    if not cause.exists():
        df_cause = pd.DataFrame(cause_serializer.data)
        df_cause_ids = df_cause['id'].values.tolist()
        what_categories = WhatCategory.objects.filter(
            cause_id__in = df_cause_ids
        )
        what_seriaizer = WhatCategoryModelSerializer(what_categories, many=True)

        how_categories = HowCategory.objects.filter(
            cause_id__in = df_cause_ids
        )

        how_serializer = HowCategoryModelSerializer(how_categories, many=True)
        categories = {
            'cause_categories': cause_serializer.data,
            'what_categories': what_seriaizer.data,
            'how_categories': how_serializer.data
        }
        return categories

    what_categories = WhatCategory.objects.filter(
        cause_id = cause.first()['cause_id']
    )
    what_seriaizer = WhatCategoryModelSerializer(what_categories, many=True)

    how_categories = HowCategory.objects.filter(
        cause_id = cause.first()['cause_id']
    )

    how_serializer = HowCategoryModelSerializer(how_categories, many=True)

    categories = {
        'cause_categories': cause_serializer.data,
        'what_categories': what_seriaizer.data,
        'how_categories': how_serializer.data
    }
    return categories
