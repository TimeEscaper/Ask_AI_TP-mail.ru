def profile_edit_display(request):
        if not request.user.is_authenticated():
            raise PermissionDenied

        if request.method == 'POST':

            form = UploadImgForm(request.POST, request.FILES)
            
            if form.is_valid():
                request_username = form.cleaned_data['username']
                request_password = form.cleaned_data['password']
                request_psw_confirm = form.cleaned_data['psw_confirm']
                request_email = form.cleaned_data['email']
                request_first_name = form.cleaned_data['first_name']
                request_last_name = form.cleaned_data['last_name']
                request_img = form.cleaned_data['img'];

                if request_password != request_psw_confirm:
                    return render(request, 'profile_edit.html', {'page_title': 'Edit Profile', 'errors': '1', 'input_username': request_username, 'input_email': request_email, 'input_first_name': request_first_name, 'input_last_name': request_last_name, })

                if request_username != request.user.username:
                    if User.objects.filter(username = request_username).exists():
                        return render(request, 'profile_edit.html', {'page_title': 'Edit Profile', 'errors': '2', 'input_username': request_username, 'input_email': request_email, 'input_first_name': request_first_name, 'input_last_name': request_last_name, })

                if request_email != request.user.email:
                    if User.objects.filter(email = request_email).exists():
                        return render(request, 'profile_edit.html', {'page_title': 'Edit Profile', 'errors': '3', 'input_username': request_username, 'input_email': request_email, 'input_first_name': request_first_name, 'input_last_name': request_last_name, })

                current_user = request.user

                current_user.username = request_username
                current_user.email = request_email
                current_user.first_name = request_first_name
                current_user.last_name = request_last_name
                current_user.avatar_file = request_img
                current_user.backend = 'django.contrib.auth.backends.ModelBackend'
                if request_password != '':
                    current_user.set_password(request_password)

                current_user.save()

                current_user_profile = UserProfile.objects.get(user_account = current_user)
                current_user_profile.avatar_file = request_img
                current_user_profile.save()

                new_user_session = auth.authenticate(username = request_username, password = request_password)
                auth.login(request, new_user_session)

                return HttpResponseRedirect(request.GET.get('continue', 'http://localhost/'))

        return render(request, 'profile_edit.html', {'page_title': 'Edit profile', 'errors': '0'})
