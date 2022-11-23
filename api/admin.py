from django.contrib import admin
from api.models import *
from django.urls import path
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import csv


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


class GrowthRateAdmin(admin.ModelAdmin):
    list_display = ('specialty', 'growth_rate')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_data = csv.DictReader(decoded_file)
            count = 1  # To avoid header values

            for fields in csv_data:
                if count == 1:
                    pass
                else:
                    created = GrowthRate.objects.update_or_create(
                        specialty=fields['specialty'],
                        growth_rate=fields['growth_rate']
                    )
                count = count + 1
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


class IBISAdmin(admin.ModelAdmin):
    list_display = ('naics_code', 'title', 'growth_rate_2021')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_data = csv.DictReader(decoded_file)
            count = 1  # To avoid header values

            for fields in csv_data:
                if count == 1:
                    pass
                else:
                    created = IBIS.objects.update_or_create(
                        naics_code=fields['naics_code'],
                        title=fields['title'],
                        growth_rate_2021=fields['growth_rate_2021']
                    )
                count = count + 1
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


class ProductBasketAdmin(admin.ModelAdmin):
    list_display = ('specialty', 'product_basket')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_data = csv.DictReader(decoded_file)
            count = 1  # To avoid header values

            for fields in csv_data:
                if count == 1:
                    pass
                else:
                    created = ProductBasket.objects.update_or_create(
                        specialty=fields['specialty'],
                        product_basket=fields['product_basket']
                    )
                count = count + 1
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('investor', 'relationship_basket')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_data = csv.DictReader(decoded_file)
            count = 1  # To avoid header values

            for fields in csv_data:
                if count == 1:
                    pass
                else:
                    created = Relationship.objects.update_or_create(
                        investor=fields['investor'],
                        relationship_basket=fields['relationship_basket']
                    )
                count = count + 1
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


class SynergyMissionAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'url',
        'parent_company_or_financial_sponsor',
        'hq_address',
        'description',
        'mission_statement',
        'vision_statement',
        'culture_and_values',
        'workplace_culture',
        'type',
        'supply_chain_position',
        'employees',
        'key_employees',
        'locations',
        'hospitals',
        'naics_six_digit_industry',
        'industry_reference_code',
        'industry_growth_rate',
        'previous_year_igr',
        'down_up_previous_year',
        'down_up_five_year',
        'specialty',
        'speciality_growth_rate',
        'speciality_interests',
        'buyouts',
        'attribute_interests',
        'sector_focus',
        'preferred_ebitda',
        'preferred_revenue',
        'preferred_ev',
        'typical_equity_investments',
        'cash_balance',
        'profits',
        'functional_descriptors',
        'geographic_reach',
        'us_geographic_reach',
        'us_areas_of_expansion_left',
        'areas_of_interest',
        'products', 
        'services',
        'target_consumer',
        'primary_contact',
        'industry_trends',
        'consumer_demands_for_industry',
        'nlp_similiarity_of_descriptions',
        'number_of_firms_in_industry',
        'notes',
        'score',
        'relationships'
    )

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_data = csv.DictReader(decoded_file)
            count = 1  # To avoid header values

            for fields in csv_data:
                if count == 1:
                    pass
                else:
                    print(fields)
                    created = SynergyMission.objects.update_or_create(
                        company_name=fields['company_name'],
                        url=fields['url'],
                        parent_company_or_financial_sponsor=fields['parent_company_or_financial_sponsor'],
                        hq_address=fields['hq_address'],
                        description=fields['description'],
                        mission_statement=fields['mission_statement'],
                        vision_statement=fields['vision_statement'],
                        culture_and_values=fields['culture_and_values'],
                        workplace_culture=fields['workplace_culture'],
                        type=fields['type'],
                        supply_chain_position=fields['supply_chain_position'],
                        employees=fields['employees'],
                        key_employees=fields['key_employees'],
                        locations=fields['locations'],
                        hospitals=fields['hospitals'],
                        naics_six_digit_industry=fields['naics_six_digit_industry'],
                        industry_reference_code=fields['industry_reference_code'],
                        industry_growth_rate=fields['industry_growth_rate'],
                        previous_year_igr=fields['previous_year_igr'],
                        down_up_previous_year=fields['down_up_previous_year'],
                        down_up_five_year=fields['down_up_five_year'],
                        specialty=fields['specialty'],
                        speciality_growth_rate=fields['speciality_growth_rate'],
                        speciality_interests=fields['speciality_interests'],
                        buyouts=fields['buyouts'],
                        attribute_interests=fields['buyouts'],
                        sector_focus=fields['sector_focus'],
                        preferred_ebitda=fields['preferred_ebitda'],
                        preferred_revenue=fields['preferred_revenue'],
                        preferred_ev=fields['preferred_ev'],
                        typical_equity_investments=fields['typical_equity_investments'],
                        cash_balance=fields['cash_balance'],
                        profits=fields['profits'],
                        functional_descriptors=fields['functional_descriptors'],
                        geographic_reach=fields['geographic_reach'],
                        us_geographic_reach=fields['us_geographic_reach'],
                        us_areas_of_expansion_left=fields['us_areas_of_expansion_left'],
                        areas_of_interest=fields['areas_of_interest'],
                        products=fields['products'],
                        services=fields['services'],
                        target_consumer=fields['target_consumer'],
                        primary_contact=fields['primary_contact'],
                        industry_trends=fields['industry_trends'],
                        consumer_demands_for_industry=fields['consumer_demands_for_industry'],
                        # mission_similarity = fields[],,
                        nlp_similiarity_of_descriptions=fields['nlp_similiarity_of_descriptions'],
                        number_of_firms_in_industry=fields['number_of_firms_in_industry'],
                        notes=fields['notes'],
                        score=fields['score'],
                        relationships=fields['relationships'],
                    )
                count = count + 1
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


# Register your models here.
admin.site.register(Question)
admin.site.register(UserCompany)
admin.site.register(UserLead)
# admin.site.register(GrowthRate)
# admin.site.register(IBIS)
# admin.site.register(ProductBasket)
# admin.site.register(Relationship)
# admin.site.register(SynergyMission)
admin.site.register(Contact)
admin.site.register(Communication)

# Register your modelAdmins here.
admin.site.register(GrowthRate, GrowthRateAdmin)
admin.site.register(IBIS, IBISAdmin)
admin.site.register(ProductBasket, ProductBasketAdmin)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(SynergyMission, SynergyMissionAdmin)
