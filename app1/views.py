from django.shortcuts import render, redirect
from .forms import ChatbotForm
from .models import Ticket
from .chatbot import recommend_action  # Ensure this import is correct

def chatbot_view(request):
    # Check if the request is a POST request
    if request.method == 'POST':
        # If 'resolved' is in POST data, handle the follow-up form
        if 'resolved' in request.POST:
            hw_type = request.POST.get('hw_type')
            apps_sw = request.POST.get('apps_sw')
            report_type = request.POST.get('report_type')
            report_desc = request.POST.get('report_desc')
            pc_ip = request.POST.get('pc_ip')
            resolved = 'resolved' in request.POST

            if resolved:
                # Save the Ticket model with the user's response if resolved
                action = request.POST.get('action')  # Retrieve action from POST data
                Ticket.objects.create(
                    hw_type=hw_type,
                    apps_sw=apps_sw,
                    report_type=report_type,
                    report_desc=report_desc,
                    pc_ip=pc_ip,
                    act_taken=action,
                    act_stat='Solved'
                )
   
        elif 'notresolved' in request.POST:
            hw_type = request.POST.get('hw_type')
            apps_sw = request.POST.get('apps_sw')
            report_type = request.POST.get('report_type')
            report_desc = request.POST.get('report_desc')
            pc_ip = request.POST.get('pc_ip')
            resolved = 'notresolved' in request.POST

            if resolved:
                # Save the Ticket model with the user's response if resolved
                action = request.POST.get('action')  # Retrieve action from POST data
                Ticket.objects.create(
                    hw_type=hw_type,
                    apps_sw=apps_sw,
                    report_type=report_type,
                    report_desc=report_desc,
                    pc_ip=pc_ip,
                    act_taken=action,
                    act_stat='NotSolved'
                )     
               
            
            # Redirect back to the initial form page or another page as needed
            return redirect('chatbot_view')
        else:
            # Handle initial form submission
            form = ChatbotForm(request.POST)
            if form.is_valid():
                hw_type = form.cleaned_data['hw_type']
                apps_sw = form.cleaned_data['apps_sw']
                report_type = form.cleaned_data['report_type']
                report_desc = form.cleaned_data['report_desc']
                pc_ip = form.cleaned_data['pc_ip']
                
                # Call the chatbot recommendation function
                action = recommend_action(hw_type, apps_sw, report_type, report_desc)
                
                # Render the response page with the chatbot action
                return render(request, 'chatbot_response.html', {
                    'hw_type': hw_type,
                    'apps_sw': apps_sw,
                    'report_type': report_type,
                    'report_desc': report_desc,
                    'pc_ip': pc_ip,
                    'action': action
                })
    else:
        # Initial GET request to show the form
        form = ChatbotForm()
    
    # Render the initial form page
    return render(request, 'chatbot_form.html', {'form': form})




