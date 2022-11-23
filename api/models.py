from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
import datetime 


# Create your models here.
class BearerAuthentication(TokenAuthentication):
    '''
    Simple token based authentication using utvsapitoken.

    Clients should authenticate by passing the token key in the 'Authorization'
    HTTP header, prepended with the string 'Bearer '.  For example:

    Authorization: Bearer 956e252a-513c-48c5-92dd-bfddc364e812
    '''
    keyword = 'Bearer'  


class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    sent = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    data = models.JSONField(blank=True, null=True)
    result_format = models.JSONField(blank=True, null=True)
    is_active = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=now, blank=True)
    

class UserCompany(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    user_input = models.JSONField(blank=True, null=True)
    programx_output = models.JSONField(blank=True, null=True)


# RecommendedLead is merged into UserLead with is_recommended distinction
class UserLead(models.Model):
    user_company_id = models.IntegerField(blank=True, null=True)
    lead_name = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)    
    contact_number = models.CharField(max_length=100, blank=True, null=True)    
    recommended_lead_notes = models.JSONField(blank=True, null=True)
    user_notes = models.TextField(blank=True, null=True)
    is_recommended = models.BooleanField(default=False)
    status = models.CharField(max_length=100, blank=True, null=True) 
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)  


class Communication(models.Model):
    user_company_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True) 


# Dataset
class SynergyMission(models.Model):
    company_name = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    parent_company_or_financial_sponsor = models.TextField(blank=True, null=True)
    hq_address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    mission_statement = models.TextField(blank=True, null=True)
    vision_statement = models.TextField(blank=True, null=True)
    culture_and_values = models.TextField(blank=True, null=True)
    workplace_culture = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    supply_chain_position = models.TextField(blank=True, null=True)
    employees = models.TextField(blank=True, null=True)
    key_employees = models.TextField(blank=True, null=True)
    locations = models.TextField(blank=True, null=True)
    hospitals = models.TextField(blank=True, null=True)
    naics_six_digit_industry = models.TextField(blank=True, null=True)
    industry_reference_code = models.TextField(blank=True, null=True)
    industry_growth_rate = models.TextField(blank=True, null=True)
    previous_year_igr = models.TextField(blank=True, null=True)
    down_up_previous_year = models.TextField(blank=True, null=True)
    down_up_five_year = models.TextField(blank=True, null=True)
    specialty = models.TextField(blank=True, null=True)
    speciality_growth_rate = models.TextField(blank=True, null=True)
    speciality_interests = models.TextField(blank=True, null=True)
    buyouts = models.TextField(blank=True, null=True)
    attribute_interests = models.TextField(blank=True, null=True)
    sector_focus = models.TextField(blank=True, null=True)
    preferred_ebitda = models.TextField(blank=True, null=True)
    preferred_revenue = models.TextField(blank=True, null=True)
    preferred_ev = models.TextField(blank=True, null=True)
    typical_equity_investments = models.TextField(blank=True, null=True)
    cash_balance = models.TextField(blank=True, null=True)
    profits = models.TextField(blank=True, null=True)
    functional_descriptors = models.TextField(blank=True, null=True)
    geographic_reach = models.TextField(blank=True, null=True)
    us_geographic_reach = models.TextField(blank=True, null=True)
    us_areas_of_expansion_left = models.TextField(blank=True, null=True)
    areas_of_interest = models.TextField(blank=True, null=True)
    products = models.TextField(blank=True, null=True)
    services = models.TextField(blank=True, null=True)
    target_consumer = models.TextField(blank=True, null=True)
    primary_contact = models.TextField(blank=True, null=True)
    industry_trends = models.TextField(blank=True, null=True)
    consumer_demands_for_industry = models.TextField(blank=True, null=True)
    # mission_similarity = models.TextField(blank=True, null=True)
    nlp_similiarity_of_descriptions = models.TextField(blank=True, null=True)
    number_of_firms_in_industry = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    score = models.TextField(blank=True, null=True)
    relationships = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)


class GrowthRate(models.Model):
    specialty = models.TextField(blank=True, null=True)
    growth_rate = models.TextField(blank=True, null=True)


class IBIS(models.Model):
    naics_code = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    growth_rate_2021 = models.TextField(blank=True, null=True)
    

class ProductBasket(models.Model):
    specialty = models.TextField(blank=True, null=True)
    product_basket = models.TextField(blank=True, null=True) 


class Relationship(models.Model):
    investor = models.TextField(blank=True, null=True)
    relationship_basket = models.TextField(blank=True, null=True)
 

# # Temporary Model    
# class ProgramXOutput(models.Model):
#     company_name = models.TextField(blank=True, null=True)
#     url = models.TextField(blank=True, null=True)
#     parent_company_or_financial_sponsor = models.TextField(blank=True, null=True)
#     hq_address = models.TextField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     mission_statement = models.TextField(blank=True, null=True)
#     vision_statement = models.TextField(blank=True, null=True)
#     culture_and_values = models.TextField(blank=True, null=True)
#     workplace_culture = models.TextField(blank=True, null=True)
#     type = models.TextField(blank=True, null=True)
#     supply_chain_position = models.TextField(blank=True, null=True)
#     employees = models.TextField(blank=True, null=True)
#     key_employees = models.TextField(blank=True, null=True)
#     locations = models.TextField(blank=True, null=True)
#     hospitals = models.TextField(blank=True, null=True)
#     naics_six_digit_industry = models.TextField(blank=True, null=True)
#     industry_reference_code = models.TextField(blank=True, null=True)
#     industry_growth_rate = models.TextField(blank=True, null=True)
#     previous_year_igr = models.TextField(blank=True, null=True)
#     down_up_previous_year = models.TextField(blank=True, null=True)
#     down_up_five_year = models.TextField(blank=True, null=True)
#     specialty = models.TextField(blank=True, null=True)
#     speciality_growth_rate = models.TextField(blank=True, null=True)
#     speciality_interests = models.TextField(blank=True, null=True)
#     buyouts = models.TextField(blank=True, null=True)
#     attribute_interests = models.TextField(blank=True, null=True)
#     sector_focus = models.TextField(blank=True, null=True)
#     pref_ebitda = models.TextField(blank=True, null=True)
#     pref_rev = models.TextField(blank=True, null=True)
#     pref_ev = models.TextField(blank=True, null=True)
#     typical_equity_investment = models.TextField(blank=True, null=True)
#     cash_balance = models.TextField(blank=True, null=True)
#     profits = models.TextField(blank=True, null=True)
#     functional_descriptors = models.TextField(blank=True, null=True)
#     geographic_reach = models.TextField(blank=True, null=True)
#     us_geographic_reach = models.TextField(blank=True, null=True)
#     us_areas_of_expansion_left = models.TextField(blank=True, null=True)
#     areas_of_interest = models.TextField(blank=True, null=True)
#     products = models.TextField(blank=True, null=True)
#     target_consumer = models.TextField(blank=True, null=True)
#     primary_contact = models.TextField(blank=True, null=True)
#     industry_trends = models.TextField(blank=True, null=True)
#     consumer_demands_for_industry = models.TextField(blank=True, null=True)
#     nlp_similiarity_of_descriptions = models.TextField(blank=True, null=True)
#     number_of_firms_in_industry = models.TextField(blank=True, null=True)
#     notes = models.TextField(blank=True, null=True)
#     score = models.TextField(blank=True, null=True)
#     relationships = models.TextField(blank=True, null=True)
#     cash_opp_cond = models.TextField(blank=True, null=True)
#     supply_chain_value = models.TextField(blank=True, null=True)
#     first_condition = models.TextField(blank=True, null=True)
#     second_condition = models.TextField(blank=True, null=True)
#     fifth_condition = models.TextField(blank=True, null=True)
#     ninth_condition = models.TextField(blank=True, null=True)
#     tenth_condition = models.TextField(blank=True, null=True)
#     eleventh_condition = models.TextField(blank=True, null=True)
#     twelfth_condition = models.TextField(blank=True, null=True)
#     thirteenth_condition = models.TextField(blank=True, null=True)
#     fourteenth_condition = models.TextField(blank=True, null=True)