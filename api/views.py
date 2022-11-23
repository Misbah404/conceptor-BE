from urllib import response
from django.http import JsonResponse
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, UpdateAPIView
from api.models import *
from api.serializers import *
from . import ai
import json


def get_communication_totals(user_company_id, leads):
    communication = Communication.objects.filter(user_company_id=user_company_id)
    serializer = CommunicationSerializer(communication, many=True)    
    communications = serializer.data

    count = 0
    totals = {}
    
    for communication in communications:
        for lead in leads:
            if lead['status'].lower() == communication['status'].lower():
                count = count + 1
                totals[communication['status']] = count
        else:
            totals[communication['status']] = count
        count = 0
    return totals    
    

class SendEmail(APIView):
    permission_classes = [AllowAny]
    
    """ Send Email """
    def post(self, request, format=None):
        try:
            type = request.data['type']   
            
            if type == 'try':
                email = request.data['email']
                
                contact = Contact(
                    email=email,
                    type=type
                )
                contact.save()
                subject = 'Conceptor - Try it out'
                html_content = f'<p>New Email: {email}</p>'
                
            elif type == 'contact':
                name = request.data['name']
                email = request.data['email']
                message = request.data['message']
                
                contact = Contact(
                    name=name,
                    email=email,
                    message=message,
                    type=type
                )
                contact.save()  
                subject = 'Conceptor - Contact us'
                html_content = f'<p>Name: {name}</p><p>Email: {email}</p><p>Message: {message}</p><br/>'
                
            else:
                return JsonResponse({'error' : 'Invalid type!'}, status=500)    
            
            # Sending of Email
            msg = EmailMessage(
                subject,
                html_content,
                settings.SENDGRID_FROM_EMAIL,
                [settings.SENDGRID_TO_EMAIL,]
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            return Response({'message' : 'Email sent successfully'})
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)    


class Register(CreateAPIView):
    permission_classes = [AllowAny]
  
    """ Register """
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ChangePassword(UpdateAPIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]
  
    """ Change Password """
    def put(self, request, *args, **kwargs):
        type = request.data['type']
        if type == 'change':
            serializer = ChangePasswordSerializer(data=request.data,
                                            context={'request': request})
        elif type == 'reset':
            serializer = ResetPasswordSerializer(data=request.data,
                                            context={'request': request})     
        else:
            return JsonResponse({'error' : 'Invalid type for changing password!'}, status=500)                    
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
        
class ForgotPassword(UpdateAPIView):
    permission_classes = [AllowAny]
  
    """ Forgot Password """
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                url = f"{settings.DOMAIN_URL}/reset-password/{uidb64}/{token}"
                
                # Sending of Email
                html_content = f'<p>To initiate the password reset process for your account, click this <a href="{url}">link</a>.</p>'
                message = EmailMessage(
                    "Conceptor - Reset Password",
                    html_content,
                    settings.SENDGRID_FROM_EMAIL,
                    [email,]
                )
                message.content_subtype = "html"  # Main content is now text/html
                message.send()           
                return JsonResponse({
                    'email': email
                })
            else:
                return JsonResponse({
                    'email': email,
                    'error': 'Email does not exist!',
                }, status=500)            
        except Exception as e:
            return JsonResponse({
                'email': email,
                'error': str(e)
            }, status=500)


class ResetPassword(APIView):
    permission_classes = [AllowAny]
    
    """ Reset Password """
    def get(self, request, *args, **kwargs):
        try:
            if 'uidb64' not in kwargs or 'token' not in kwargs:
                return JsonResponse({"error": "The URL path must contain 'uidb64' and 'token' parameters!"}, status=500)
                
            user = self.get_user(kwargs['uidb64'])

            if user is not None:
                token = kwargs['token']
                token = self.get_token(user.id, token)
                
                if token is not None:
                    return JsonResponse({
                        'token': token.key,
                        'user_id': user.pk,
                        'email': user.email
                    })
                else:
                    return JsonResponse({"error": "User token not valid!"}, status=500)
            else:
                return JsonResponse({"error": "User does not exist!"}, status=500)
                
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)
    
    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            user = None
        return user
    
    def get_token(self, uid, token):
        try:
            token = Token.objects.get(user_id=uid, key=token)
            if token is not None:
                new_token = Token.objects.filter(user_id=uid)
                new_key = new_token[0].generate_key()
                new_token.update(key=new_key)
                token = new_token[0]
        except Exception:
            token = None
        return token
            

class Login(ObtainAuthToken):

    """ Login """

    def post(self, request, *args, **kwargs):
        userdata = request.data
        if 'email' in request.data:
            username = User.objects.filter(
                email=request.data['email']).values("username")
            if username:
                userdata = {
                    'username': username[0]["username"], 'password': request.data['password']}
            else:
                return JsonResponse({'non_field_errors': ['Unable to log in with provided credentials.']}, status=400)
              
        serializer = self.serializer_class(data=userdata,
                                           context={'request': request})

        # logging.info('ssss',request)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # token, _ = Token.objects.get_or_create(user=user)
        try:
            token = Token.objects.get(user=user)
            is_logged_once = 1
        except Token.DoesNotExist:
            is_logged_once = 0
            token = Token(user=user)
            token.save()

        return JsonResponse({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_logged_once': is_logged_once
        })


class Logout(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    """ Logout """
    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

        
class QuestionView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]
    
    """ Get decision tree question """
    def get(self, request, format=None):
        try:
            questions = Question.objects.get(is_active=1)
            serializer = QuestionSerializer(questions)
            serializer_data = serializer.data
            
            specialties = GrowthRate.objects.values_list('specialty', flat=True)
            functional_descriptors = SynergyMission.objects.values_list('functional_descriptors', flat=True)
            
            for x in serializer_data['data']['attributes']:
                if x['key'] == 'speciality_input':
                    x['options'] = self.get_options(specialties)
                    # print(f"speciality_input {x['options']}")
             
            for x in serializer_data['data']['goals']:                
                if x['key'] == 'recap-two' or x['key'] == 'sale-five':
                    x['options'] = self.get_options(functional_descriptors)     
                    # print(f"functional_descriptors {x['options']}")   
                
            return Response(serializer_data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)               
        
    """ Get decision tree question """
    def get_options(self, data):   
        new_string = '' 
        for i in data: 
            i = str(i)  + ','
            new_string = i + new_string 
        a_list = new_string.split(",") 

        final_list=[] 
        for i in a_list: 
            i = i.strip()
            if i not in final_list:
                final_list.append(i) 
                
        cleanedList = [x for x in final_list if str(x) != 'nan' and str(x) != ''] 
        sortedList = sorted(cleanedList)
        
        options = [{'label': x, 'value': x} for x in sortedList]
        return options        

class UserView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    """ Get user """
    def get(self, request, format=None):
        try:
            user = User.objects.get(pk=request.user.id)
            serializer = UserSerializer(user) 
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)            
      
    """ Update user """
    def put(self, request, format=None):
        # Create UserCompany with user, company_name, user_input
        try:
            username = request.data['username']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            defaults = {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
            user, _ = User.objects.update_or_create(pk=request.user.id, defaults=defaults)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)   
       
    """ Delete user """
    def delete(self, request, format=None):
        try:
            user = User.objects.get(pk=request.user.id)
            user.delete()
            return Response({'message' : 'User deleted successfully'})
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)  
        

class UserCompanyView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    """ Get user company """
    def get(self, request, format=None):
        try:
            user_company = UserCompany.objects.filter(user_id=request.user.id)
            serializer = UserCompanySerializer(user_company, many=True) 
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)            

    """ Submit user company """
    def post(self, request, format=None):
        # Create UserCompany with user, company_name, user_input
        try:
            company_name = request.data['company_name']
            
            user_company = UserCompany(
                user_id=request.user.id, 
                company_name=company_name
            )
            user_company.save()
            
            # Adding default communication type for lead management
            communication = Communication.objects.bulk_create([
                Communication( user_company_id = user_company.id, status = 'new lead' ),
                Communication( user_company_id = user_company.id, status = 'contacted' ),
                Communication( user_company_id = user_company.id, status = 'communicating' )
            ])

            serializer = UserCompanySerializer(user_company)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)   

    """ Update user company """
    def put(self, request, format=None):
        # Create UserCompany with user, company_name, user_input
        try:
            useraccess = User.objects.filter(pk=request.user.id , groups__name='full-access').exists()
            id = request.data['id']
            company_name = request.data['company_name']
            user_input = request.data['user_input']
            output = ai.ISP(user_input,useraccess)
            programx_output = output
            
            defaults = {
                'company_name': company_name,
                'user_input': user_input,
                'programx_output': programx_output
            }
            
            user_company, _ = UserCompany.objects.update_or_create(pk=id, defaults=defaults)
            serializer = UserCompanySerializer(user_company)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)   
       
    """ Delete user company """
    def delete(self, request, format=None):
        try:
            id = request.GET.get('id', '')
            user_company = UserCompany.objects.get(pk=id)
            user_company.delete()
            return Response({'message' : 'User company deleted successfully'})
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)  


class UserCompanyDetailView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    """ Get user company """
    def get(self, request, id, format=None):
        try:
            user_company = UserCompany.objects.get(pk=id)
            serializer = UserCompanySerializer(user_company) 
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)             

    """ Update user company """
    def put(self, request, id, format=None):
        # Create UserCompany with user, company_name, user_input
        try:
            useraccess = User.objects.filter(pk=request.user.id , groups__name='full-access').exists()
            company_name = request.data['company_name']
            user_input = request.data['user_input']
            output = ai.ISP(user_input,useraccess)
            programx_output = output
            
            defaults = {
                'company_name': company_name,
                'user_input': user_input,
                'programx_output': programx_output
            }
            
            user_company, _ = UserCompany.objects.update_or_create(pk=id, defaults=defaults)
            serializer = UserCompanySerializer(user_company)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)   
       
    """ Delete user company """
    def delete(self, request, id, format=None):
        try:
            user_company = UserCompany.objects.get(pk=id)
            user_company.delete()
            return Response({'message' : 'User company deleted successfully'})
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)  


class UserLeadView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    """ Get user lead """
    def get(self, request, format=None):
        try:
            user_company_id = request.GET.get('user_company_id', '')
            user_lead = UserLead.objects.filter(user_company_id=user_company_id)
            serializer = UserLeadSerializer(user_lead, many=True) 
            leads = serializer.data
            response = {}
            response['leads'] = leads
            response['total'] = len(leads)
            response['total_per_type'] = get_communication_totals(user_company_id, leads)
            return Response(response)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)            
      
    """ Submit user lead """
    def post(self, request, format=None):
        # Create UserCompany with user, company_name, user_input
        try:
            if request.data['is_recommended'] == 1:
                defaults = {}
                defaults['user_company_id'] = request.data['user_company_id']
                defaults['lead_name'] = request.data['lead_name']
                defaults['company_name'] = request.data['company_name']
                defaults['url'] = request.data['url']
                # defaults['location'] = request.data['location']
                defaults['email'] = request.data['email']
                defaults['contact_number'] = request.data['contact_number']
                defaults['recommended_lead_notes'] = request.data['recommended_lead_notes']
                defaults['user_notes'] = request.data['user_notes']
                defaults['is_recommended'] = request.data['is_recommended']
                defaults['state'] = request.data['state']
                defaults['country'] = request.data['country']
                defaults['status'] = 'new lead'
                user_lead, _ = UserLead.objects.update_or_create(user_company_id=request.data['user_company_id'], lead_name=request.data['lead_name'], defaults=defaults)
                serializer = UserLeadSerializer(user_lead)
                return Response(serializer.data)
            elif request.data['is_recommended'] == 0:
                user_lead = self.get_user_lead(request.data['user_company_id'], request.data['lead_name'])
                
                if user_lead is None:
                    user_lead = UserLead(
                        user_company_id = request.data['user_company_id'],
                        lead_name = request.data['lead_name'],
                        company_name = request.data['company_name'],
                        url = request.data['url'],
                        # location = request.data['location'],
                        email = request.data['email'],
                        contact_number = request.data['contact_number'],
                        recommended_lead_notes = request.data['recommended_lead_notes'],
                        user_notes = request.data['user_notes'],
                        is_recommended = request.data['is_recommended'],
                        state = request.data['state'],
                        country = request.data['country'],
                        status = 'new lead'
                    )
                    user_lead.save()
                    serializer = UserLeadSerializer(user_lead)
                    return Response(serializer.data)
                else:
                    return JsonResponse({'error' : 'Lead name already exists!'}, status=500)
            else:
                return JsonResponse({'error' : 'Invalid is_recommended value!'}, status=500)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)   
        
    """ Update user lead """
    def put(self, request, format=None):
        # Create UserCompany with user, company_name, user_input
        try:
            id = request.data['id']
            defaults = {}
            defaults['user_company_id'] = request.data['user_company_id']
            defaults['lead_name'] = request.data['lead_name']
            defaults['company_name'] = request.data['company_name']
            defaults['url'] = request.data['url']
            defaults['location'] = request.data['location']
            defaults['email'] = request.data['email']
            defaults['contact_number'] = request.data['contact_number']
            defaults['recommended_lead_notes'] = request.data['recommended_lead_notes']
            defaults['user_notes'] = request.data['user_notes']
            defaults['is_recommended'] = request.data['is_recommended']
            defaults['state'] = request.data['state']
            defaults['country'] = request.data['country']
            defaults['status'] = request.data['status']  
            user_lead, _ = UserLead.objects.update_or_create(pk=id, defaults=defaults)
            serializer = UserLeadSerializer(user_lead)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)   
       
    """ Delete user lead """
    def delete(self, request, format=None):
        try:
            id = request.GET.get('id', '')
            user_lead = UserLead.objects.get(pk=id)
            user_lead.delete()
            return Response({'message' : 'User lead deleted successfully'})
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)  
        
    def get_user_lead(self, user_company_id, lead_name):
        try:
            user_lead = UserLead.objects.get(user_company_id=user_company_id, lead_name=lead_name)
        except Exception:
            user_lead = None
        return user_lead
        

class UserLeadDetailView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    """ Get user lead """
    def get(self, request, id, format=None):
        try:
            user_lead = UserLead.objects.get(pk=id)
            serializer = UserLeadSerializer(user_lead)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)            

        
    """ Update user lead """
    def put(self, request, id, format=None):
        # Create UserCompany with user, company_name, user_input
        try:
            defaults = {}
            defaults['user_company_id'] = request.data['user_company_id']
            defaults['lead_name'] = request.data['lead_name']
            defaults['company_name'] = request.data['company_name']
            defaults['url'] = request.data['url']
            defaults['location'] = request.data['location']
            defaults['email'] = request.data['email']
            defaults['contact_number'] = request.data['contact_number']
            defaults['recommended_lead_notes'] = request.data['recommended_lead_notes']
            defaults['user_notes'] = request.data['user_notes']
            defaults['is_recommended'] = request.data['is_recommended']
            defaults['state'] = request.data['state']
            defaults['country'] = request.data['country']
            defaults['status'] = request.data['status']  
            user_lead, _ = UserLead.objects.update_or_create(pk=id, defaults=defaults)
            serializer = UserLeadSerializer(user_lead)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)   
       
    """ Delete user lead """
    def delete(self, request, id, format=None):
        try:
            user_lead = UserLead.objects.get(pk=id)
            user_lead.delete()
            return Response({'message' : 'User lead deleted successfully'})
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500) 


class CommunicationView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    """ Get communication status """
    def get(self, request, format=None):
        try:
            user_company_id = request.GET.get('user_company_id', '')
            communication = Communication.objects.filter(user_company_id=user_company_id)
            serializer = CommunicationSerializer(communication, many=True) 
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)            
      
    """ Submit communication status """
    def post(self, request, format=None):
        print(request.data)
        # Create UserCompany with user, company_name, user_input
        try:
            communication = Communication(
                user_company_id = request.data['user_company_id'],
                status = request.data['status'] 
            )
            communication.save()
            serializer = CommunicationSerializer(communication)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)   
        
    """ Update communication status """
    def put(self, request, format=None):
        # Create UserCompany with user, company_name, user_input
        try:
            id = request.data['id']
            defaults = {}
            defaults['user_company_id'] = request.data['user_company_id']
            defaults['status'] = request.data['status']  
            communication, _ = Communication.objects.update_or_create(pk=id, defaults=defaults)
            serializer = CommunicationSerializer(communication)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)   
       
    """ Delete communication status """
    def delete(self, request, format=None):
        try:
            id = request.GET.get('id', '')
            communication = Communication.objects.get(pk=id)
            communication.delete()
            return Response({'message' : 'Communication status deleted successfully'})
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)  


class ProgramX(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    """ Submit ISP input """    
    def put(self, request):
        try:
            useraccess = User.objects.filter(pk=request.user.id , groups__name='full-access').exists()
            id = request.data['id']
            company_name = request.data['company_name']
            user_input = request.data['user_input']            
            output = ai.ISP(user_input,useraccess)
            programx_output = output
            
            defaults = {
                'company_name': company_name,
                'user_input': user_input,
                'programx_output': programx_output
            }
            
            user_company, _ = UserCompany.objects.update_or_create(pk=id, defaults=defaults)
            serializer = UserCompanySerializer(user_company)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500) 
