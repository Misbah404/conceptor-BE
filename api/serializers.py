from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from api.models import *
import random

misc_inc_possibilites = ['Type: Strategic Buyer', 'Type: Financial Buyer', 'Function Strength =',
                        'Workplace Culture Match', 'Same Cultural Value:', 'Similar Mission Statement',
                        'Similar Vision Statement']

operating_possiblites = [
    'Economies of Scale - Industry',
    'Economies of Scale - Specialty',
    'Similar Company Description'
    'Higher Growth Rate in Seller Industry',
    'Upstream Vertical Supply Chain Synergy',
    'Downstream Vertical Supply Chain Synergy',
    'Product Strengthening in',
    'Product Expansion in',
    'Geographic Strengthening in',
    'Geographic Expansion in',
]   

financial_possibilites = ['Cash for your Firms Opportunities',
                        'Tax Benefits - Buyer Profit Realization']  
    

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()
        
        print(f'user {user}')
        return user
    
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('new_password', 'confirm_password')
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})

        return attrs

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
    

class ResetPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Your old password was entered incorrectly. Please enter it again."})
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})

        return attrs

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        

class UserCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = '__all__'


class UserLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLead
        fields = '__all__'
           
        
class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = '__all__'
 

class SynergyMissionSerializer(serializers.ModelSerializer):
    # Temporary fields: cash_opp_cond - fourteenth_condition
    cash_opp_cond = serializers.SerializerMethodField()
    supply_chain_value = serializers.SerializerMethodField()
    first_condition = serializers.SerializerMethodField()
    second_condition = serializers.SerializerMethodField()
    fifth_condition = serializers.SerializerMethodField()
    ninth_condition = serializers.SerializerMethodField()
    tenth_condition = serializers.SerializerMethodField()
    eleventh_condition = serializers.SerializerMethodField()
    twelfth_condition = serializers.SerializerMethodField()
    thirteenth_condition = serializers.SerializerMethodField()
    fourteenth_condition = serializers.SerializerMethodField()
    bar_chart = serializers.SerializerMethodField()
    misc_synergies = serializers.SerializerMethodField()
    operating_synergies = serializers.SerializerMethodField()
    financial_synergies = serializers.SerializerMethodField()
    
    class Meta:
        model = SynergyMission
        fields = '__all__'
         
    def get_cash_opp_cond(self, obj):
        return random.choice([True, False])
    
    def get_supply_chain_value(self, obj):
        return 4

    def get_first_condition(self, obj):
        return random.choice([True, False])
    
    def get_second_condition(self, obj):
        return random.choice([True, False])
    
    def get_fifth_condition(self, obj):
        return random.choice([True, False])
    
    def get_ninth_condition(self, obj):
        return random.choice([True, False])
    
    def get_tenth_condition(self, obj):
        return random.choice([True, False])
    
    def get_eleventh_condition(self, obj):
        return random.choice([True, False])
    
    def get_twelfth_condition(self, obj):
        return random.choice([True, False])
    
    def get_thirteenth_condition(self, obj):
        return random.choice([True, False])    
    
    def get_fourteenth_condition(self, obj):
        return random.choice([True, False]) 

    def get_misc_synergies(self, obj):
        relationships = obj.relationships
        relationships = [relationship for relationship in relationships.split(',') if relationship]
        
        misc_output = []
        for i in relationships:
            for m in misc_inc_possibilites:
                if m in i:
                    misc_output.append(i)
        return misc_output 
    
    def get_operating_synergies(self, obj):
        relationships = obj.relationships
        relationships = [relationship for relationship in relationships.split(',') if relationship]
        
        operating_output = []
        for i in relationships:
            for o in operating_possiblites:
                if o in i:
                    operating_output.append(i)
        return operating_output 
    
    def get_financial_synergies(self, obj):
        relationships = obj.relationships
        relationships = [relationship for relationship in relationships.split(',') if relationship]  
        
        financial_output = []
        for i in relationships:
            for f in financial_possibilites:
                if f in i:
                    financial_output.append(i)
        return financial_output 
        
    def get_bar_chart(self, obj):
        bar1 = len(self.get_misc_synergies(obj))
        bar2 = len(self.get_operating_synergies(obj))
        bar3 = len(self.get_financial_synergies(obj))
        return [
            {
                "value": bar1,
                "color": "#BDC1FE",
                "percent": int(100* bar1 / len(misc_inc_possibilites))
            },
            {
                "value": bar2,
                "color": "#D0BBFE",
                "percent": int(100* bar2 / len(operating_possiblites))
            },
            {
                "value": bar3,
                "color": "#EABBFE",
                "percent": int(100 * bar3 / len(financial_possibilites))               
            }
        ]
    

# # Temporary ModelSerializer
# class ProgramXOutputSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProgramXOutput
#         fields = '__all__'